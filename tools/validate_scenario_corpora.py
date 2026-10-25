#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import argparse, sys, yaml
from portable_catalogue import validate_block
from corpus_claim_integrity import static_claim_errors
ROOT=Path(__file__).resolve().parent.parent

def load(path): return yaml.safe_load(path.read_text(encoding='utf-8')) or {}

def selected_ids(registry_path: str|None, composition_id: str|None, manifest_sources: dict) -> set[str]|None:
    if not registry_path and not composition_id: return None
    if not registry_path or not composition_id: raise ValueError('--registry and --composition must be supplied together')
    rp=Path(registry_path); rp=rp if rp.is_absolute() else ROOT/rp
    reg=load(rp)
    if reg.get('deprecated') and reg.get('canonical_registry'): reg=load(ROOT/reg['canonical_registry'])
    item=next((x for x in reg.get('compositions',[]) if x.get('id')==composition_id),None)
    if not item: raise ValueError(f'Unknown composition id: {composition_id}')
    wanted={item.get('corpus_id'),*(c.get('corpus_id') for c in item.get('components',[]))}; wanted.discard(None)
    # Recursively include manifest dependencies.
    queue=list(wanted)
    while queue:
        cid=queue.pop()
        for dep in (manifest_sources.get(cid) or {}).get('dependencies') or []:
            if dep not in wanted: wanted.add(dep); queue.append(dep)
    return wanted

def main()->int:
    ap=argparse.ArgumentParser(description='Validate RAHP scenario corpora, optionally scoped to one profile composition.')
    ap.add_argument('--registry'); ap.add_argument('--composition')
    args=ap.parse_args()
    patdoc=load(ROOT/'method/scenario-patterns.yaml'); patterns={p['id'] for p in patdoc.get('patterns',[])}
    errors=[]; corpora=0; scenarios=0
    manifest_path=ROOT/'corpora/sources.yaml'; manifest=load(manifest_path) if manifest_path.exists() else {}
    manifest_sources={x.get('corpus_id'):x for x in manifest.get('sources',[]) if isinstance(x,dict)}
    if not manifest_sources: errors.append('corpora/sources.yaml defines no corpus sources')
    if not patterns: errors.append('method/scenario-patterns.yaml defines no patterns')
    try: wanted=selected_ids(args.registry,args.composition,manifest_sources)
    except ValueError as e: print('ERROR',e); return 1
    corpus_docs={}
    for corpus_path in (ROOT/'corpora').glob('*.yaml'):
        if corpus_path.name!='sources.yaml':
            candidate=load(corpus_path).get('corpus') or {}
            if candidate.get('id'): corpus_docs[candidate['id']]=candidate
    for path in sorted((ROOT/'corpora').glob('*.yaml')):
        if path.name=='sources.yaml': continue
        doc=load(path); c=doc.get('corpus') or {}; cid=c.get('id')
        if wanted is not None and cid not in wanted: continue
        corpora+=1
        for f in ('id','title','adapter_version','description','scenarios'):
            if not c.get(f): errors.append(f'{path.relative_to(ROOT)}: corpus.{f} is required')
        source_cfg=manifest_sources.get(cid)
        if not source_cfg: errors.append(f'{path.relative_to(ROOT)}: corpus id {cid} missing from corpora/sources.yaml')
        elif source_cfg.get('corpus_file')!=str(path.relative_to(ROOT)): errors.append(f'{path.relative_to(ROOT)}: sources.yaml corpus_file mismatch for {cid}')
        for claim_error in static_claim_errors(c, source_cfg):
            errors.append(f'{path.relative_to(ROOT)}: {claim_error}')
        if source_cfg and source_cfg.get('update_mode')=='derived':
            if not c.get('depends_on'): errors.append(f'{path.relative_to(ROOT)}: derived corpus requires corpus.depends_on')
            dep_ids={d.get('corpus_id') for d in (c.get('depends_on') or []) if isinstance(d,dict)}
            for dep in source_cfg.get('dependencies') or []:
                if dep not in dep_ids: errors.append(f'{path.relative_to(ROOT)}: missing declared dependency {dep}')
            for dependency in c.get('depends_on') or []:
                if not isinstance(dependency,dict):
                    errors.append(f'{path.relative_to(ROOT)}: dependency must be a mapping'); continue
                parent=corpus_docs.get(dependency.get('corpus_id'))
                if not parent: continue
                declared=dependency.get('source_commit')
                parent_pin=parent.get('source_commit')
                if declared and declared!=parent_pin:
                    if c.get('source_commit')=='derived-from-pinned-dependencies':
                        errors.append(f'{path.relative_to(ROOT)}: dependency {dependency.get("corpus_id")} pin differs from parent while claiming derived-from-pinned-dependencies')
                    elif not c.get('provenance_note'):
                        errors.append(f'{path.relative_to(ROOT)}: divergent dependency pin requires corpus.provenance_note')
            if c.get('evidence_grade')=='source-pinned' and c.get('provenance_status')=='composition-review-pending':
                errors.append(f'{path.relative_to(ROOT)}: source-pinned grade contradicts pending composition review')
        else:
            for f in ('source_repository','source_path','source_commit'):
                if not c.get(f): errors.append(f'{path.relative_to(ROOT)}: corpus.{f} is required')
            if source_cfg:
                src=source_cfg.get('source') or {}
                for f in ('repository','paths'):
                    if not src.get(f): errors.append(f'{path.relative_to(ROOT)}: sources.yaml source.{f} is required')
                if src.get('repository') and c.get('source_repository')!=src.get('repository'): errors.append(f'{path.relative_to(ROOT)}: source_repository differs from corpora/sources.yaml')
                authority_pin=src.get('authority_pin')
                if authority_pin and c.get('source_commit')!=authority_pin: errors.append(f'{path.relative_to(ROOT)}: source_commit differs from sources.yaml authority_pin')
                if c.get('provenance_status')=='authoritative-source-pinned-scenario-review-pending' and c.get('evidence_grade'):
                    errors.append(f'{path.relative_to(ROOT)}: evidence_grade cannot be declared while scenario requalification is pending')
        seen=set()
        for s in c.get('scenarios') or []:
            scenarios+=1; sid=str(s.get('id') or '')
            if not sid: errors.append(f'{path.relative_to(ROOT)}: scenario id required'); continue
            if sid in seen: errors.append(f'{path.relative_to(ROOT)}: duplicate scenario id {sid}')
            seen.add(sid)
            for f in ('title','domain','primary_goal','primary_pressure','priority','scenario_patterns'):
                if not s.get(f): errors.append(f'{path.relative_to(ROOT)}:{sid}: {f} is required')
            refs=s.get('scenario_patterns') or []
            if not isinstance(refs,list): errors.append(f'{path.relative_to(ROOT)}:{sid}: scenario_patterns must be a list'); continue
            for ref in refs:
                if ref not in patterns: errors.append(f'{path.relative_to(ROOT)}:{sid}: unknown scenario pattern {ref}')
            if c.get('assurance_catalogue'): validate_block(s.get('portable_assurance'),f'{path.relative_to(ROOT)}:{sid}',errors,required=True)
    if corpora==0: errors.append('no selected corpora found')
    if wanted is None:
        for cid,item in manifest_sources.items():
            cf=ROOT/str(item.get('corpus_file',''))
            if not cf.exists(): errors.append(f'corpora/sources.yaml: {cid} references missing {item.get("corpus_file")}')
    else:
        missing=wanted-{load(p).get('corpus',{}).get('id') for p in (ROOT/'corpora').glob('*.yaml') if p.name!='sources.yaml'}
        for cid in sorted(missing): errors.append(f'selected corpus id not found: {cid}')
    if errors:
        for e in errors: print('ERROR',e)
        print(f'Scenario corpus validation failed: {len(errors)} error(s).'); return 1
    scope=f' for {args.composition}' if wanted is not None else ''
    print(f'Scenario corpus validation clean{scope}: {corpora} corpus/corpora, {scenarios} scenarios, {len(patterns)} portable patterns.')
    return 0
if __name__=='__main__': raise SystemExit(main())
