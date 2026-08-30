#!/usr/bin/env python3
"""Validate the stable v1 engine contract, revision governance and conformance fixtures."""
from __future__ import annotations
import json, pathlib, re, sys
try:
    import yaml, jsonschema
except ImportError:
    sys.exit('requires PyYAML and jsonschema')
ROOT=pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'tools'))
from engine_contract import validate_result, load_result, retention_plan

def fail(msg): print('ERROR:',msg); return 1

def main():
    errors=0
    contract=yaml.safe_load((ROOT/'method/engine-contract.yaml').read_text())
    contract_id=str(contract.get('id',''))
    contract_family=contract.get('contract_family')
    contract_revision=str(contract.get('contract_revision',''))
    if contract_id!='rahp-engine-contract-v1': errors+=fail(f'engine contract id must remain rahp-engine-contract-v1, got {contract_id!r}')
    if contract_family!=1: errors+=fail(f'engine contract family must be 1, got {contract_family!r}')
    if not re.fullmatch(r'1\.\d+', contract_revision): errors+=fail(f'engine contract revision must be a v1-family minor revision such as 1.2, got {contract_revision!r}')
    if contract.get('status')!='stable': errors+=fail('current engine contract revision must be declared stable')

    stages=contract.get('execution_model',{}).get('stages') or []
    expected=['source','observation','trigger','assessment','evidence','evaluation','finding','disposition','remediation','retest','baseline']
    if stages!=expected: errors+=fail(f'engine stages must be {expected}, got {stages}')
    ops={x.get('id') for x in contract.get('operations') or []}
    required={'validate-profile','observe-source','correlate-trigger','scaffold-assessment','classify-evidence','evaluate-assurance','validate-assessment','normalize-result','plan-retention','plan-remediation','evaluate-retest','promote-disposition'}
    if not required<=ops: errors+=fail('engine contract missing operations: '+', '.join(sorted(required-ops)))

    policy=yaml.safe_load((ROOT/'method/evidence-retention.yaml').read_text())
    classes=policy.get('classes') or {}
    if set(classes)!={'ephemeral','referenced','durable','exemplar'}: errors+=fail('retention classes must be ephemeral/referenced/durable/exemplar')
    if classes.get('ephemeral',{}).get('repository')!='forbidden': errors+=fail('ephemeral evidence must be forbidden from repository')

    fixtures=sorted((ROOT/'tests/conformance/engine').glob('*/result.json'))
    if not fixtures: errors+=fail('no engine conformance fixtures')
    for result_path in fixtures:
        exp=yaml.safe_load((result_path.parent/'expected.yaml').read_text())
        actual=validate_result(result_path,quiet=True)
        if actual != bool(exp['valid']): errors+=fail(f'{result_path.parent.name}: expected valid={exp["valid"]}, got {actual}')
        if actual and 'retention' in exp:
            plan=retention_plan(load_result(result_path)); got=sorted({a['class'] for a in plan['actions'] if a['action']=='commit'})
            want=sorted(exp['retention'].get('repository_classes') or [])
            if got!=want: errors+=fail(f'{result_path.parent.name}: retention repository classes {got}, expected {want}')

    versioning=yaml.safe_load((ROOT/'method/versioning.yaml').read_text())
    stable_release=str(versioning.get('stable_release',''))
    if not re.fullmatch(r'v\d+\.\d+\.\d+', stable_release): errors+=fail('stable toolkit release metadata must identify a semantic vMAJOR.MINOR.PATCH version')
    contracts=versioning.get('contracts',{})
    if contracts.get('engine')!=contract_id: errors+=fail('versioning engine contract id mismatch')
    if contracts.get('engine_family')!=contract_family: errors+=fail('versioning engine family mismatch')
    if str(contracts.get('engine_revision',''))!=contract_revision: errors+=fail('versioning engine revision mismatch')
    engine_policy=(versioning.get('compatibility') or {}).get('engine_contract') or {}
    if engine_policy.get('family_identifier')!=contract_id: errors+=fail('engine compatibility family identifier mismatch')
    if str(engine_policy.get('current_revision',''))!=contract_revision: errors+=fail('engine compatibility current revision mismatch')
    if engine_policy.get('breaking_change_requires')!='new_contract_id': errors+=fail('breaking engine changes must require a new contract id')
    if engine_policy.get('additive_operation_requires')!='minor_revision': errors+=fail('additive engine operations must require a minor revision')
    if engine_policy.get('additive_invariant_requires')!='minor_revision': errors+=fail('additive engine invariants must require a minor revision')
    if contracts.get('result_schema')!=1: errors+=fail('stable v1 normalized result schema must remain version 1')
    if contracts.get('evidence_retention')!='rahp-evidence-retention-v1': errors+=fail('stable v1 evidence retention contract must remain rahp-evidence-retention-v1')

    from engine_contract import correlate_trigger
    lifecycle=sorted((ROOT/'tests/conformance/lifecycle').glob('*/input.json'))
    if not lifecycle: errors+=fail('no lifecycle conformance fixtures')
    for ip in lifecycle:
        inp=json.loads(ip.read_text()); exp=json.loads((ip.parent/'expected.json').read_text()); got=correlate_trigger(inp['observation'],inp.get('open_assessments') or [])
        if got!=exp: errors+=fail(f'{ip.parent.name}: lifecycle correlation mismatch {got} != {exp}')

    from assurance import load_json as load_assurance_json, validate_document, infer_residual, retest_outcome
    assurance_fixtures=sorted((ROOT/'tests/conformance/assurance').glob('*/evaluation.json'))
    if not assurance_fixtures: errors+=fail('no assurance conformance fixtures')
    for ep in assurance_fixtures:
        value=load_assurance_json(ep); verr=validate_document(value,'assurance-evaluation.schema.json')
        if verr: errors+=fail(f'{ep.parent.name}: invalid assurance fixture: {verr}')
        inferred=infer_residual(value.get('signals') or [],value.get('control_evidence') or [],value.get('assurance_evidence') or [])
        if inferred != value['residual']['status']: errors+=fail(f'{ep.parent.name}: inferred residual {inferred} != declared {value["residual"]["status"]}')
    for schema_name,fixture in [('remediation-manifest.schema.json',ROOT/'tests/conformance/remediation/valid.json'),('retest.schema.json',ROOT/'tests/conformance/retest/valid.json')]:
        verr=validate_document(load_assurance_json(fixture),schema_name)
        if verr: errors+=fail(f'{fixture.relative_to(ROOT)} invalid: {verr}')
    if retest_outcome('finding','controlled')!='resolved': errors+=fail('retest finding -> controlled must resolve')
    if retest_outcome('controlled','finding')!='regression': errors+=fail('retest controlled -> finding must regress')

    durable=sorted(ROOT.glob('instances/*/reviews/*.result.json'))
    for result_path in durable:
        if not validate_result(result_path,quiet=True): errors+=fail(f'durable normalized result invalid: {result_path.relative_to(ROOT)}')
    if errors: print(f'Engine contract validation failed: {errors} error(s)'); return 1
    print(f'Engine contract valid: {contract_id} revision {contract_revision}; {len(fixtures)} result fixture(s); {len(assurance_fixtures)} assurance fixture(s); {len(lifecycle)} lifecycle fixture(s); {len(durable)} durable normalized result(s); stable toolkit release {stable_release}')
    return 0
if __name__=='__main__': raise SystemExit(main())
