#!/usr/bin/env python3
"""Report corpus provenance and upstream drift without changing corpus semantics.

The portfolio monitor is used as a discovery/scope registry. Each corpus source pin
remains authoritative for reproducibility. Network mode uses the GitHub REST API;
o external GitHub SDK is required.
"""
from __future__ import annotations
import argparse, fnmatch, json, os, re, sys, urllib.error, urllib.request
from pathlib import Path
import yaml
from corpus_claim_integrity import derive_claim_state

ROOT=Path(__file__).resolve().parent.parent
SOURCES=ROOT/'corpora'/'sources.yaml'
SHA_RE=re.compile(r'^[0-9a-f]{40}$')


def load_yaml(path):
    return yaml.safe_load(path.read_text(encoding='utf-8')) or {}


def fetch_text(url):
    headers={'User-Agent':'rahp-corpus-status'}
    token=os.getenv('GITHUB_TOKEN') or os.getenv('GH_TOKEN')
    if token: headers['Authorization']=f'Bearer {token}'
    req=urllib.request.Request(url,headers=headers)
    with urllib.request.urlopen(req,timeout=30) as r:
        return r.read().decode('utf-8')


def api_json(url):
    headers={'Accept':'application/vnd.github+json','User-Agent':'rahp-corpus-status'}
    token=os.getenv('GITHUB_TOKEN') or os.getenv('GH_TOKEN')
    if token: headers['Authorization']=f'Bearer {token}'
    req=urllib.request.Request(url,headers=headers)
    with urllib.request.urlopen(req,timeout=30) as r:
        return json.loads(r.read().decode('utf-8'))


def head_sha(repo, branch):
    return api_json(f'https://api.github.com/repos/{repo}/commits/{branch}')['sha']


def compare_files(repo, base, head):
    data=api_json(f'https://api.github.com/repos/{repo}/compare/{base}...{head}')
    return [f['filename'] for f in data.get('files',[])]


def matches_any(path, patterns):
    return any(fnmatch.fnmatch(path, pat) for pat in patterns)


def portfolio_entries(manifest):
    reg=manifest.get('portfolio_registry') or {}
    repo=reg.get('repository'); branch=reg.get('branch','main'); path=reg.get('path')
    if not (repo and path): return {}
    text=fetch_text(f'https://raw.githubusercontent.com/{repo}/{branch}/{path}')
    doc=yaml.safe_load(text) or {}
    return {x.get('repo'):x for x in doc.get('repositories',[]) if isinstance(x,dict) and x.get('repo')}


def entries():
    manifest=load_yaml(SOURCES)
    byid={}
    for item in manifest.get('sources',[]):
        byid[item['corpus_id']]=item
    return manifest,byid


def corpus_record(item):
    doc=load_yaml(ROOT/item['corpus_file'])
    return doc.get('corpus') or {}

def annotate_claim_integrity(results, byid):
    for result in results:
        item=byid.get(result.get('corpus_id')) or {}
        if not item:
            continue
        corpus=corpus_record(item)
        result['claim_integrity']=derive_claim_state(corpus,result.get('status'))
    return results


def evaluate(item, network=True, portfolio=None):
    c=corpus_record(item)
    cid=item['corpus_id']
    if item.get('update_mode')=='derived':
        return {'corpus_id':cid,'corpus_file':item['corpus_file'],'status':'DEPENDENCY_REVIEW_REQUIRED',
                'reason':'Derived corpus status depends on semantic baselines of its declared dependencies.',
                'dependencies':item.get('dependencies',[])}
    src=item.get('source') or {}
    pinned=str(c.get('source_commit') or '')
    out={'corpus_id':cid,'corpus_file':item['corpus_file'],'repository':src.get('repository'),
         'branch':src.get('branch','main'),'pinned_commit':pinned,
         'portfolio_repository':src.get('portfolio_repository'),'relationship_to_portfolio':src.get('relationship_to_portfolio')}
    if portfolio is not None:
        pr=src.get('portfolio_repository')
        meta=portfolio.get(pr) if pr else None
        out['portfolio_match']=bool(meta)
        if meta:
            out['portfolio_metadata']={k:meta.get(k) for k in ('workstream','role','lifecycle','reporting_weight','default_branch')}
        elif pr:
            out.update(status='PORTFOLIO_SCOPE_MISMATCH',reason=f'Configured portfolio repository {pr} is absent from the DTG Portfolio Monitor registry.')
            return out
    if not SHA_RE.match(pinned):
        out.update(status='UNPINNED_REVIEW_REQUIRED',
                   reason='Corpus uses a non-immutable source snapshot. Review against a concrete commit before advancing provenance.')
        if network:
            out['observed_head']=head_sha(src['repository'],src.get('branch','main'))
        else:
            out['observed_head']=src.get('observed_head_at_bootstrap')
        return out
    if not network:
        out.update(status='PINNED_NOT_CHECKED', reason='Immutable source pin is present; network drift check was not requested.')
        return out
    head=head_sha(src['repository'],src.get('branch','main')); out['observed_head']=head
    if head==pinned:
        out.update(status='UP_TO_DATE',reason='Pinned commit equals current tracked branch HEAD.')
        return out
    files=compare_files(src['repository'],pinned,head)
    relevant=[p for p in files if matches_any(p,src.get('paths',[]))]
    out['changed_files']=files; out['relevant_changed_files']=relevant
    if relevant:
        out.update(status='CORPUS_REVIEW_REQUIRED',reason='Tracked source material changed after the pinned commit.')
    else:
        out.update(status='SOURCE_CHANGED_NO_CORPUS_IMPACT',reason='Repository HEAD changed, but no configured corpus source path changed.')
    return out


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--offline',action='store_true',help='Validate/report without contacting GitHub.')
    ap.add_argument('--json',dest='json_path',help='Write machine-readable report to this path.')
    ap.add_argument('--markdown',dest='md_path',help='Write human-readable report to this path.')
    ap.add_argument('--fail-on-review',action='store_true',help='Exit 2 when any corpus requires review.')
    ap.add_argument('--fail-on-error',action='store_true',help='Exit 3 only for operational/configuration failures (for CI health checks).')
    args=ap.parse_args()
    manifest,byid=entries(); results=[]; portfolio=None; portfolio_error=None
    if not args.offline:
        try: portfolio=portfolio_entries(manifest)
        except (urllib.error.URLError,KeyError,ValueError,yaml.YAMLError) as e: portfolio_error=str(e)
    for item in manifest.get('sources',[]):
        try: results.append(evaluate(item,network=not args.offline,portfolio=portfolio))
        except (urllib.error.URLError,KeyError,ValueError) as e:
            results.append({'corpus_id':item.get('corpus_id'),'corpus_file':item.get('corpus_file'),'status':'CHECK_FAILED','reason':str(e)})
    # Refine derived states from dependency results.
    status_by={r['corpus_id']:r['status'] for r in results}
    for r in results:
        item=byid.get(r['corpus_id'],{})
        if item.get('update_mode')=='derived':
            deps=item.get('dependencies',[])
            if deps and all(status_by.get(d) in {'UP_TO_DATE','SOURCE_CHANGED_NO_CORPUS_IMPACT','PINNED_NOT_CHECKED'} for d in deps):
                r['status']='DERIVED_BASELINES_STABLE' if args.offline else 'RECOMPOSITION_NOT_TRIGGERED'
                r['reason']='Declared dependency baselines do not currently require semantic review.'
    annotate_claim_integrity(results,byid)
    report={'version':1,'portfolio_registry':manifest.get('portfolio_registry',{}),'portfolio_registry_status':('not-checked' if args.offline else ('ok' if portfolio is not None else 'check-failed')),'portfolio_registry_error':portfolio_error,'results':results}
    if args.json_path:
        p=Path(args.json_path); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(report,indent=2)+'\n')
    lines=['# RAHP corpus source status','', '| Corpus | Status | Claim state | Pinned source | Observed head |','|---|---|---|---|---|']
    for r in results:
        claim=(r.get('claim_integrity') or {}).get('state','unknown')
        lines.append(f"| `{r['corpus_id']}` | **{r['status']}** | **{claim}** | `{str(r.get('pinned_commit','—'))[:12]}` | `{str(r.get('observed_head','—'))[:12]}` |")
    lines+=['','## Detail','']
    for r in results:
        lines += [f"### {r['corpus_id']}", '', r.get('reason',''), '']
        if r.get('relevant_changed_files'):
            lines += ['Relevant changed files:'] + [f"- `{x}`" for x in r['relevant_changed_files']] + ['']
    md='\n'.join(lines).rstrip()+'\n'
    if args.md_path:
        p=Path(args.md_path); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(md)
    else:
        print(md,end='')
    review={'UNPINNED_REVIEW_REQUIRED','CORPUS_REVIEW_REQUIRED','DEPENDENCY_REVIEW_REQUIRED','CHECK_FAILED','PORTFOLIO_SCOPE_MISMATCH'}
    if args.fail_on_review and any(r['status'] in review for r in results): return 2
    operational={'CHECK_FAILED','PORTFOLIO_SCOPE_MISMATCH'}
    if args.fail_on_error and any(r['status'] in operational for r in results): return 3
    return 0

if __name__=='__main__': raise SystemExit(main())
