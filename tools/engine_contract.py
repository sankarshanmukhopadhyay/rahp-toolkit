#!/usr/bin/env python3
"""RAHP v1 stable language-neutral engine-contract utility.

This Python command is a reference adapter for the contract, not the normative
RAHP implementation. Other implementations MUST consume the same schemas,
contract and conformance fixtures rather than copy Python behaviour.
"""
from __future__ import annotations
import argparse, hashlib, json, pathlib, sys
from typing import Any
try:
    import yaml, jsonschema
except ImportError:
    sys.exit("engine_contract.py requires PyYAML and jsonschema: pip install -r requirements.txt")
ROOT=pathlib.Path(__file__).resolve().parent.parent
CONTRACT=ROOT/'method'/'engine-contract.yaml'
RETENTION=ROOT/'method'/'evidence-retention.yaml'
RESULT_SCHEMA=ROOT/'method'/'schema'/'rahp-result.schema.json'

def load_yaml(path:pathlib.Path)->dict[str,Any]:
    v=yaml.safe_load(path.read_text(encoding='utf-8')) or {}
    if not isinstance(v,dict): raise SystemExit(f"expected mapping: {path}")
    return v

def load_result(path:pathlib.Path)->dict[str,Any]:
    try: v=json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError as e: raise SystemExit(f"invalid JSON {path}: {e}")
    if not isinstance(v,dict): raise SystemExit('result root must be an object')
    return v

def semantic_errors(result:dict[str,Any])->list[str]:
    out=[]
    for ev in result.get('evidence') or []:
        if ev.get('class')=='referenced':
            for req in ('uri','sha256','collected_at','sensitivity'):
                if not ev.get(req): out.append(f"referenced evidence {ev.get('id','?')} missing {req}")
        if ev.get('class')=='ephemeral' and result.get('status')=='dispositioned':
            out.append(f"dispositioned result must not depend on ephemeral evidence {ev.get('id','?')}")
    if result.get('status')=='dispositioned' and (result.get('disposition') or {}).get('outcome')=='pending':
        out.append('dispositioned result cannot have pending outcome')
    evaluations=result.get('evaluations') or []
    declared=result.get('assurance_summary')
    if declared is not None:
        states=('assured','controlled','finding','assurance-gap','review-required','not-assessed','not-applicable')
        actual={k:0 for k in states}
        for item in evaluations:
            state=((item.get('residual') or {}).get('status'))
            if state in actual: actual[state]+=1
        for key,value in declared.items():
            if key not in actual: out.append(f'assurance_summary contains unknown state {key}')
            elif value != actual[key]: out.append(f'assurance_summary.{key} must equal {actual[key]}')
    if not result.get('findings') and declared and (declared.get('assurance-gap',0) or declared.get('review-required',0) or declared.get('not-assessed',0)):
        if (result.get('disposition') or {}).get('outcome')=='no-material-assurance-impact':
            out.append('zero findings with unresolved assurance states cannot be dispositioned as no-material-assurance-impact')
    closure=result.get('closure')
    if closure:
        if result.get('status')!='dispositioned':
            out.append('issue closure eligibility requires a dispositioned result')
        if closure.get('reviewed_revision') != (result.get('target') or {}).get('reviewed_revision'):
            out.append('closure.reviewed_revision must equal target.reviewed_revision')
    return out

def validate_result(path:pathlib.Path,quiet=False)->bool:
    result=load_result(path); schema=json.loads(RESULT_SCHEMA.read_text(encoding='utf-8'))
    errors=[]
    for e in jsonschema.Draft202012Validator(schema).iter_errors(result):
        loc='.'.join(str(x) for x in e.absolute_path) or '<root>'; errors.append(f"{loc}: {e.message}")
    errors.extend(semantic_errors(result))
    if not quiet:
        if errors:
            print(f"INVALID {path}"); [print('  - '+e) for e in errors]
        else: print(f"VALID {path}")
    return not errors

def retention_plan(result:dict[str,Any])->dict[str,Any]:
    policy=load_yaml(RETENTION); classes=policy['classes']; actions=[]
    for ev in result.get('evidence') or []:
        cls=ev['class']; spec=classes[cls]
        actions.append({'id':ev['id'],'class':cls,'repository':spec['repository'],
                        'retention_days':spec.get('default_retention_days'),
                        'action': 'commit' if spec['repository']=='allowed' else ('manifest-only' if spec['repository']=='manifest-only' else 'do-not-commit')})
    return {'policy':policy['id'],'assessment':result['assessment']['id'],'actions':actions}

def correlate_trigger(observation:dict[str,Any], assessments:list[dict[str,Any]])->dict[str,Any]:
    key=observation.get('assessment_key')
    for item in assessments:
        if item.get('key')==key and item.get('status') in ('in-progress','open'):
            return {'action':'coalesce','assessment_key':key,'assessment_id':item.get('id')}
    return {'action':'create','assessment_key':key}

def cmd_describe(_):
    c=load_yaml(CONTRACT)
    print(f"{c['title']} [{c['id']}]")
    print('Execution model: '+' -> '.join(c['execution_model']['stages']))
    print('Operations:')
    for op in c['operations']: print(f"  {op['id']}: {', '.join(op['inputs'])} -> {', '.join(op['outputs'])}")

def cmd_validate(a):
    raise SystemExit(0 if validate_result(a.result) else 1)

def cmd_retention(a):
    if not validate_result(a.result,quiet=True):
        validate_result(a.result); raise SystemExit(1)
    print(json.dumps(retention_plan(load_result(a.result)),indent=2))

def cmd_explain(a):
    from explain_result import explain_file, render_markdown
    try:
        explanation = explain_file(a.result, a.freshness, a.run_id)
    except (OSError, ValueError) as exc:
        raise SystemExit(f"explanation rejected: {exc}")
    print(json.dumps(explanation, indent=2, sort_keys=True) if a.format == "json" else render_markdown(explanation))


def cmd_hash(a):
    h=hashlib.sha256()
    with a.file.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    print(h.hexdigest())

def main():
    ap=argparse.ArgumentParser(description=__doc__); sub=ap.add_subparsers(dest='command',required=True)
    p=sub.add_parser('describe'); p.set_defaults(func=cmd_describe)
    p=sub.add_parser('validate-result'); p.add_argument('result',type=pathlib.Path); p.set_defaults(func=cmd_validate)
    p=sub.add_parser('retention-plan'); p.add_argument('result',type=pathlib.Path); p.set_defaults(func=cmd_retention)
    p=sub.add_parser('sha256'); p.add_argument('file',type=pathlib.Path); p.set_defaults(func=cmd_hash)
    p=sub.add_parser('explain',help='read-only normalized-result explanation')
    p.add_argument('result',type=pathlib.Path)
    p.add_argument('--format',choices=('json','markdown'),default='json')
    p.add_argument('--freshness',type=pathlib.Path)
    p.add_argument('--run-id')
    p.set_defaults(func=cmd_explain)
    a=ap.parse_args(); a.func(a)
if __name__=='__main__': main()
