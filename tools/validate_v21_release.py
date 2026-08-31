#!/usr/bin/env python3
"""Validate RAHP v2.1.0 qualified autonomous assurance plane."""
from pathlib import Path
import json, yaml
ROOT=Path(__file__).resolve().parents[1]
def y(rel): return yaml.safe_load((ROOT/rel).read_text(encoding='utf-8')) or {}
def main():
    q=y('method/v2.1-release-qualification.yaml'); status=y('PROJECT-STATUS.yaml'); rel=y('method/release.yaml')['release']; ver=y('method/versioning.yaml'); errors=[]
    if q.get('release')!='v2.1.0': errors.append('qualification release must be v2.1.0')
    if q.get('qualification')!='qualified-autonomous-assurance-plane': errors.append('qualification theme mismatch')
    if str(status.get('stable_release'))!='2.1.0' or str(status.get('development_target'))!='2.1.0': errors.append('project version must be 2.1.0')
    if status.get('qualification_status')!='qualified': errors.append('qualification status must be qualified')
    if rel.get('version')!='2.1.0' or rel.get('tag')!='v2.1.0': errors.append('release declaration mismatch')
    if rel.get('theme')!='Qualified Autonomous Assurance Plane': errors.append('release theme mismatch')
    if (rel.get('name') or {}).get('common')!='Common Acacia Blue': errors.append('release codename mismatch')
    if ver.get('stable_release')!='v2.1.0': errors.append('versioning stable_release mismatch')
    compat=status.get('compatibility') or {}; contracts=ver.get('contracts') or {}
    if compat.get('engine_contract')!='rahp-engine-contract-v1' or str(contracts.get('engine_revision'))!='1.3': errors.append('engine compatibility changed')
    if compat.get('normalized_result_schema')!=1 or compat.get('evidence_retention_contract')!='rahp-evidence-retention-v1': errors.append('result/evidence compatibility changed')
    run=q.get('qualification_run') or {}
    if run.get('operator_actions_after_trigger')!=0 or run.get('stranded_runs')!=0: errors.append('qualification must record zero operator actions and zero stranded runs')
    required=[
      'method/schema/assurance-run-state.schema.json','tools/assurance_fsm.py','tools/assurance_watchdog.py','tools/assurance_record.py',
      'tools/autonomous_assurance_controller.py','tools/clean_room_execute.py','tools/text_assertion_probe.py','tools/evidence_assertion_assessor.py',
      'clean-room/qualification/evidence-33350790322.json','docs/zero-touch-qualification-2026-08-31.md','docs/releases/v2.1.0.md']
    for item in required:
        if not (ROOT/item).is_file(): errors.append(f'missing v2.1 qualification artifact: {item}')
    for key in ('missing_evidence_never_pass','component_pass_not_composition_pass','workflows_not_authoritative_controller_state','human_machine_terminal_equivalence','evidence_classes_remain_distinct','generic_core_target_agnostic'):
        if not (q.get('invariants') or {}).get(key): errors.append(f'missing invariant: {key}')
    pkg=json.loads((ROOT/'package.json').read_text())
    if pkg.get('version')!='2.1.0': errors.append('root package version mismatch')
    portable=y('examples/portable-instance/data/instance.yaml')
    if str((portable.get('instance') or {}).get('toolkit_version'))!='v2.1.0': errors.append('portable fixture version mismatch')
    if errors:
        for e in errors: print('ERROR:',e)
        return 1
    print('PASS v2.1.0 qualified: zero-touch autonomous assurance plane with preserved compatibility boundaries.')
    return 0
if __name__=='__main__': raise SystemExit(main())
