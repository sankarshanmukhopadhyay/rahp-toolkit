#!/usr/bin/env python3
"""Turn declared evidence predicates into a bounded portable assessor result.

This assessor judges only the configured proposition. It does not infer general safety
from successful probes and therefore emits explicit boundedness in its result.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any
import yaml

def load(path:Path)->dict[str,Any]:
    text=path.read_text(encoding='utf-8'); value=json.loads(text) if path.suffix=='.json' else yaml.safe_load(text)
    if not isinstance(value,dict): raise ValueError('document root must be a mapping')
    return value

def assess(config:dict[str,Any], ledger:dict[str,Any])->dict[str,Any]:
    by_id={str(x.get('requirement_id')):x for x in ledger.get('requirements',[]) or [] if isinstance(x,dict)}
    used=[]; failed=[]; missing=[]
    for rid in config.get('requirement_ids',[]):
        item=by_id.get(str(rid)); used.append(str(rid))
        if not item or item.get('attempt_state')!='EXECUTED' or item.get('result')=='NOT_EVIDENCED': missing.append(str(rid))
        elif item.get('result')!='SATISFIED': failed.append(str(rid))
    if missing:
        outcome='INDETERMINATE'; reason='evidence-required'; residual=f"Required evidence unavailable for: {', '.join(missing)}"; action='Produce the named attributable evidence and rerun the same bounded proposition.'
    elif failed:
        outcome=str(config.get('failure_outcome') or 'FAIL'); reason=str(config.get('failure_reason_code') or 'configured-proposition-failed'); residual=str(config.get('failure_residual_risk') or f"Configured assurance proposition failed at: {', '.join(failed)}"); action=str(config.get('failure_action_required') or 'Remediate the configured specification/control predicate and rerun against a new immutable source pin.')
    else:
        outcome=str(config.get('success_outcome') or 'PASS'); reason=str(config.get('success_reason_code') or 'configured-proposition-satisfied'); residual=str(config.get('success_residual_risk') or 'No residual established within the explicitly bounded proposition; no broader safety claim is made.'); action=str(config.get('success_action_required') or 'Preserve the tested normative predicate and rerun on material changes.')
    return {'schema':'rahp-assessor-result/v1','assessor':str(config.get('assessor') or 'rahp-evidence-assertion-assessor'),'assessment_id':str(config.get('assessment_id') or 'portable:configured-proposition'),'outcome':outcome,'reason_code':reason,'evidence_used':used,'residual_risk':residual,'action_required':action,'boundedness':str(config.get('boundedness') or 'Only the configured source/evidence proposition is assessed.'),'confidence':str(config.get('confidence') or 'high when source pins and probe provenance are valid')}

def self_test()->int:
    cfg={'requirement_ids':['ER-1'],'failure_reason_code':'guardrail-absent'}
    passed={'requirements':[{'requirement_id':'ER-1','attempt_state':'EXECUTED','result':'SATISFIED'}]}; assert assess(cfg,passed)['outcome']=='PASS'
    failed={'requirements':[{'requirement_id':'ER-1','attempt_state':'EXECUTED','result':'ABSENT'}]}; assert assess(cfg,failed)['outcome']=='FAIL'
    assert assess(cfg,{'requirements':[]})['outcome']=='INDETERMINATE'
    print('PASS evidence_assertion_assessor self-test'); return 0

def main()->int:
    p=argparse.ArgumentParser(); p.add_argument('--self-test',action='store_true'); p.add_argument('--config',type=Path); p.add_argument('--ledger',type=Path); p.add_argument('--output',type=Path); a=p.parse_args()
    if a.self_test:return self_test()
    if not a.config or not a.ledger or not a.output:p.error('--config --ledger --output required')
    result=assess(load(a.config),load(a.ledger)); a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8'); return 0
if __name__=='__main__': raise SystemExit(main())
