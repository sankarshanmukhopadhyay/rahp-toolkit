#!/usr/bin/env python3
"""Validate RAHP v2.2.0 evidence production and realization assurance release."""
from pathlib import Path
import json, yaml
ROOT=Path(__file__).resolve().parents[1]
def y(rel): return yaml.safe_load((ROOT/rel).read_text(encoding='utf-8')) or {}
def main():
    q=y('method/v2.2-release-qualification.yaml'); status=y('PROJECT-STATUS.yaml'); rel=y('method/release.yaml')['release']; ver=y('method/versioning.yaml'); errors=[]
    if q.get('release')!='v2.2.0': errors.append('qualification release must be v2.2.0')
    if q.get('qualification')!='evidence-production-and-realization-assurance': errors.append('qualification theme mismatch')
    if str(status.get('stable_release'))!='2.2.0' or str(status.get('development_target'))!='2.2.0': errors.append('project version must be 2.2.0')
    if status.get('qualification_status')!='qualified': errors.append('qualification status must be qualified')
    if rel.get('version')!='2.2.0' or rel.get('tag')!='v2.2.0': errors.append('release declaration mismatch')
    if rel.get('theme')!='Evidence Production and Realization Assurance': errors.append('release theme mismatch')
    if (rel.get('name') or {}).get('common')!='Common Four-ring': errors.append('release codename mismatch')
    if ver.get('stable_release')!='v2.2.0': errors.append('versioning stable_release mismatch')
    compat=status.get('compatibility') or {}; contracts=ver.get('contracts') or {}
    if compat.get('engine_contract')!='rahp-engine-contract-v1' or str(contracts.get('engine_revision'))!='1.3': errors.append('engine compatibility changed')
    if compat.get('normalized_result_schema')!=1 or compat.get('evidence_retention_contract')!='rahp-evidence-retention-v1': errors.append('result/evidence compatibility changed')
    required=['schemas/rahp-assurance-obligation-v1.schema.json','tools/assurance_obligation.py','tools/evidence_producer_controller.py','tools/evidence_producer_scheduler.py','tools/evidence_provenance_router.py','tools/assurance_invariants.py','tools/actor_dependency_invariants.py','tools/evidence_topology_invariants.py','tools/human_choice_invariants.py','tools/current_portfolio_assessor.py','tools/vdc_vac_evidence_adapter.py','clean-room/current-portfolio-run-spec.json','instances/dtg/reviews/current-portfolio-2026-09-07/assurance-record.md','instances/dtg/reviews/current-portfolio-2026-09-07/assurance-terminal-machine.json','instances/dtg/reviews/current-portfolio-2026-09-07/proposition-matrix.json','docs/releases/v2.2.0.md']
    for item in required:
        if not (ROOT/item).is_file(): errors.append(f'missing v2.2 qualification artifact: {item}')
    caps=q.get('qualified_capabilities') or {}
    for key in ('semantic_assurance_obligation','deterministic_obligation_identity','evidence_producer_registry_and_dispatch','evidence_provenance_routing','bounded_assurance_invariant_waves','current_portfolio_clean_room_execution','normative_realization_separation','explicit_runtime_evidence_gaps','durable_residual_owner_transfer'):
        if not caps.get(key): errors.append(f'missing qualified capability: {key}')
    inv=q.get('invariants') or {}
    for key in ('missing_evidence_never_pass','component_pass_not_composition_pass','workflow_success_not_assurance_success','normative_convergence_not_implementation_conformance','runtime_properties_require_runtime_evidence','generic_core_target_agnostic','residuals_require_durable_owners'):
        if not inv.get(key): errors.append(f'missing invariant: {key}')
    run=q.get('qualification_run') or {}
    if run.get('terminal_state')!='TERMINAL_INDETERMINATE_EVIDENCE_REQUIRED' or run.get('consumer_posture')!='AMBER': errors.append('current portfolio qualification must preserve bounded indeterminate/AMBER result')
    if run.get('historical_inputs_used') is not False: errors.append('current portfolio qualification must be clean-room')
    pkg=json.loads((ROOT/'package.json').read_text())
    if pkg.get('version')!='2.2.0': errors.append('root package version mismatch')
    portable=y('examples/portable-instance/data/instance.yaml')
    if str((portable.get('instance') or {}).get('toolkit_version'))!='v2.2.0': errors.append('portable fixture version mismatch')
    if errors:
        for e in errors: print('ERROR:',e)
        return 1
    print('PASS v2.2.0 qualified: evidence production and realization assurance with preserved compatibility boundaries.')
    return 0
if __name__=='__main__': raise SystemExit(main())
