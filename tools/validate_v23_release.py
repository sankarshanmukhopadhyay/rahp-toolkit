#!/usr/bin/env python3
"""Validate RAHP v2.3.0 portable coverage and source-preserving assurance release."""
from pathlib import Path
import json, yaml
ROOT=Path(__file__).resolve().parents[1]
def y(rel): return yaml.safe_load((ROOT/rel).read_text(encoding='utf-8')) or {}
def main():
    q=y('method/v2.3-release-qualification.yaml'); status=y('PROJECT-STATUS.yaml'); rel=y('method/release.yaml')['release']; ver=y('method/versioning.yaml'); errors=[]
    if q.get('release')!='v2.3.0': errors.append('qualification release must be v2.3.0')
    if q.get('qualification')!='portable-coverage-and-source-preserving-assurance': errors.append('qualification theme mismatch')
    if str(status.get('stable_release'))!='2.3.0' or str(status.get('development_target'))!='2.3.0': errors.append('project version must be 2.3.0')
    if status.get('qualification_status')!='qualified': errors.append('qualification status must be qualified')
    if rel.get('version')!='2.3.0' or rel.get('tag')!='v2.3.0': errors.append('release declaration mismatch')
    if rel.get('theme')!='Portable Coverage and Source-Preserving Assurance': errors.append('release theme mismatch')
    if (rel.get('name') or {}).get('common')!='Common Five-ring': errors.append('release codename mismatch')
    if ver.get('stable_release')!='v2.3.0': errors.append('versioning stable_release mismatch')
    compat=status.get('compatibility') or {}; contracts=ver.get('contracts') or {}
    if compat.get('engine_contract')!='rahp-engine-contract-v1' or str(contracts.get('engine_revision'))!='1.3': errors.append('engine compatibility changed')
    if compat.get('normalized_result_schema')!=1 or compat.get('evidence_retention_contract')!='rahp-evidence-retention-v1': errors.append('result/evidence compatibility changed')
    required=['profiles/dtg/coverage/data-rooms.yaml','method/resilience/README.md','method/mappings/resilience-to-assurance.yaml','tools/resilience_propositions.py','tools/resilience_evidence.py','docs/releases/v2.3.0.md']
    for item in required:
        if not (ROOT/item).is_file(): errors.append(f'missing v2.3 qualification artifact: {item}')
    caps=q.get('qualified_capabilities') or {}
    for key in ('generic_capability_coverage_model','persona_coverage_pack','data_rooms_coverage_pack','current_vti_openvtc_evidence_reconciliation','source_preserving_resilience_propositions','deterministic_runtime_evidence_obligations','upstream_dependency_and_residual_ownership','deferred_evidence_semantics'):
        if not caps.get(key): errors.append(f'missing qualified capability: {key}')
    inv=q.get('invariants') or {}
    for key in ('missing_evidence_never_pass','component_pass_not_composition_pass','workflow_success_not_assurance_success','normative_convergence_not_implementation_conformance','runtime_properties_require_runtime_evidence','generic_core_target_agnostic','residuals_require_durable_owners','source_findings_are_not_silently_reinterpreted'):
        if not inv.get(key): errors.append(f'missing invariant: {key}')
    pkg=json.loads((ROOT/'package.json').read_text())
    if pkg.get('version')!='2.3.0': errors.append('root package version mismatch')
    portable=y('examples/portable-instance/data/instance.yaml')
    if str((portable.get('instance') or {}).get('toolkit_version'))!='v2.3.0': errors.append('portable fixture version mismatch')
    if errors:
        for e in errors: print('ERROR:',e)
        return 1
    print('PASS v2.3.0 qualified: portable coverage and source-preserving assurance with preserved compatibility boundaries.')
    return 0
if __name__=='__main__': raise SystemExit(main())
