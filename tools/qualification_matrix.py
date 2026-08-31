#!/usr/bin/env python3
from __future__ import annotations
import argparse, importlib.util, json, shutil, subprocess, sys, urllib.error
from pathlib import Path


def run_case(rahp: Path, root: Path, case: dict, nonce: str) -> dict:
    work=root/'work'/case['id']
    if work.exists(): shutil.rmtree(work)
    work.mkdir(parents=True)
    subprocess.run([sys.executable,str(rahp/'tools'/'clean_room_execute.py'),'--spec',str(rahp/case['spec']),'--rahp',str(rahp),'--workspace',str(work),'--nonce',nonce],check=True)
    terminal=json.loads((work/'output'/'clean-room-terminal.json').read_text())
    if terminal['outcome'] != case['expected_outcome']: raise AssertionError(f"{case['id']}: {terminal['outcome']} != {case['expected_outcome']}")
    if case.get('expected_reason') and terminal['reason_code'] != case['expected_reason']: raise AssertionError(f"{case['id']}: {terminal['reason_code']} != {case['expected_reason']}")
    if terminal.get('stranded') is not False or terminal.get('terminal') is not True: raise AssertionError(f"{case['id']}: non-terminal/stranded result")
    dest=root/'qualification-output'/case['id']
    if dest.exists(): shutil.rmtree(dest)
    shutil.copytree(work/'output',dest)
    return terminal


def transport_failure_recovery(dpip: Path) -> dict:
    path=dpip/'scripts'/'rahp_return.py'; spec=importlib.util.spec_from_file_location('q318_dpip_return',path); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    examination={
      'applicability':'applicable','conclusion':'PASS','evidence_summary':'Bounded specialist proposition satisfied.',
      'action':'Preserve the bounded evidence contract.',
      'assessor_result':{'schema':'rahp-assessor-result/v1','assessor':'dpip','assessment_id':'dpip:q318','outcome':'PASS','reason_code':'bounded-pass','evidence_used':[],'residual_risk':'None within scope.','action_required':'Preserve the bounded evidence contract.'}
    }
    issue={'number':149,'html_url':'https://example.invalid/dpip/149','labels':[{'name':'source:rahp'},{'name':'run:complete'}],
           'body':'```yaml\nsource:\n  system: RAHP\n  repository: example/rahp\n  issue: 309\n```'}
    dpip_comments=[{'body':'```yaml\ndpip_examination:\n'+''.join('  '+line+'\n' for line in __import__('yaml').safe_dump(examination,sort_keys=False).splitlines())+'```'}]
    rahp_comments=[]; fail={'delivery':True}; calls={'delivery_posts':0}
    def fake_api(method,repo,path,token,payload=None):
        if method=='GET' and repo=='example/dpip' and path.startswith('issues/149/comments'): return list(dpip_comments)
        if method=='GET' and repo=='example/rahp' and path.startswith('issues/309/comments'): return list(rahp_comments)
        if method=='POST' and repo=='example/dpip' and path=='issues/149/comments': dpip_comments.append({'body':payload['body']}); return {}
        if method=='POST' and repo=='example/rahp' and path=='issues/309/comments':
            calls['delivery_posts']+=1
            if fail['delivery']: raise urllib.error.URLError('qualification injected transport failure')
            rahp_comments.append({'body':payload['body']}); return {}
        if method=='POST' and repo=='example/rahp' and path=='issues/309/labels': return {}
        if method=='DELETE' and repo=='example/rahp': return {}
        raise AssertionError(f'unexpected API call: {method} {repo} {path}')
    mod.api=fake_api
    try:
        mod.process_issue('example/dpip','example/rahp',issue,'dpip-token','rahp-token')
        raise AssertionError('injected transport failure did not fail delivery')
    except urllib.error.URLError:
        pass
    outboxes=[c for c in dpip_comments if 'rahp-return-outbox:v1:149:' in c.get('body','')]
    acks=[c for c in dpip_comments if 'rahp-return-ack:v1:149:' in c.get('body','')]
    if len(outboxes)!=1 or acks or rahp_comments: raise AssertionError('failed delivery did not leave exactly one pending outbox')
    fail['delivery']=False
    mod.process_issue('example/dpip','example/rahp',issue,'dpip-token','rahp-token')
    mod.process_issue('example/dpip','example/rahp',issue,'dpip-token','rahp-token')
    outboxes=[c for c in dpip_comments if 'rahp-return-outbox:v1:149:' in c.get('body','')]
    acks=[c for c in dpip_comments if 'rahp-return-ack:v1:149:' in c.get('body','')]
    returns=[c for c in rahp_comments if '<!-- dpip-return:example/dpip#149 -->' in c.get('body','')]
    if len(outboxes)!=1 or len(acks)!=1 or len(returns)!=1: raise AssertionError('retry was not idempotent/durably acknowledged')
    return {'injected_failure':True,'pending_outbox_after_failure':True,'automatic_retry_succeeded':True,'idempotent_delivery':True,'delivery_attempts':calls['delivery_posts']}


def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument('--manifest',type=Path,required=True); p.add_argument('--rahp',type=Path,required=True); p.add_argument('--root',type=Path,required=True); p.add_argument('--nonce',required=True); a=p.parse_args()
    rahp=a.rahp.resolve(); root=a.root.resolve(); manifest=json.loads(a.manifest.read_text()); results=[]; instances=set()
    for case in manifest['cases']:
        spec_doc=json.loads((rahp/case['spec']).read_text()); instances.add(spec_doc['run']['instance'])
        results.append(run_case(rahp,root,case,f"{a.nonce}-{case['id']}"))
    missing_types=set(manifest.get('required_subject_types',[]))-{r['subject']['type'] for r in results}
    if missing_types: raise AssertionError(f"missing subject types: {sorted(missing_types)}")
    missing_profiles=set(manifest.get('required_profiles',[]))-instances
    if missing_profiles: raise AssertionError(f"missing profiles: {sorted(missing_profiles)}")
    if manifest.get('require_zero_stranded') and any(r.get('stranded') for r in results): raise AssertionError('stranded qualification run')

    replay_case=next(c for c in manifest['cases'] if c['id']=='a2a-standalone'); current=next(r for c,r in zip(manifest['cases'],results) if c['id']=='a2a-standalone')
    replay=run_case(rahp,root,{**replay_case,'id':'a2a-standalone-replay'},f"{a.nonce}-replay")
    if replay['assessment_id'] != current['assessment_id']: raise AssertionError('replay changed assessment identity')

    prior=next(r for c,r in zip(manifest['cases'],results) if c['id']=='a2a-prior-pin')
    if prior['assessment_id']==current['assessment_id']: raise AssertionError('new source pin did not create reassessment identity')
    current_record=json.loads((root/'qualification-output'/'a2a-standalone'/'assurance-terminal-machine.json').read_text())
    run_lineage=(current_record.get('lineage') or {}).get('run') or {}
    if run_lineage.get('reassessment_of') != prior['assessment_id'] or not run_lineage.get('supersession_rule'): raise AssertionError('reassessment/supersession lineage not preserved')

    transport=transport_failure_recovery(root/'work'/'dtg-composite'/'dpip')
    summary={
      'schema':'rahp-zero-touch-qualification/v1','issue':manifest.get('issue'),'operator_actions_after_trigger':0,'stranded_runs':0,
      'profiles':sorted(instances),'cases':[{'subject':r['subject'],'assessment_id':r['assessment_id'],'outcome':r['outcome'],'reason_code':r['reason_code'],'state':r['state'],'terminal':r['terminal']} for r in results],
      'replay':{'same_assessment_id':True,'assessment_id':current['assessment_id']},
      'reassessment':{'prior_assessment_id':prior['assessment_id'],'new_assessment_id':current['assessment_id'],'different_source_pin_identity':True,'lineage_preserved':True},
      'transport_failure_recovery':transport
    }
    out=root/'qualification-output'; out.mkdir(exist_ok=True); (out/'qualification-summary.json').write_text(json.dumps(summary,indent=2)+'\n'); print(json.dumps(summary,indent=2)); return 0

if __name__=='__main__': raise SystemExit(main())
