#!/usr/bin/env python3
"""Validate v2.9 release qualification claims without publishing."""
from __future__ import annotations
import json,re,sys
from pathlib import Path
import yaml
from validate_v29_release_evidence import assess as assess_evidence
ROOT=Path(__file__).resolve().parents[1]
EXPECTED={"engine_contract":"rahp-engine-contract-v1","engine_revision":"1.3","normalized_result_schema":1,"evidence_retention_contract":"rahp-evidence-retention-v1"}
GATES={"full_regression","typescript_conformance","stable_compatibility","docs_rendering","publication_metadata","release_publication_preflight","security_review","owner_approval"}
CAPABILITIES={"people_impact_pathways","source_qualified_corpus_evidence","lifecycle_and_control_consequence_assurance","source_pinned_runtime_and_witness_evidence","assurance_registry_discovery","release_supply_chain_reproducibility","contribution_and_license_governance"}
SHA=re.compile(r"^[0-9a-f]{40}$")
def validate(root: Path=ROOT)->list[str]:
    errors=[]
    try:
        q=yaml.safe_load((root/"method/v2.9-release-qualification.yaml").read_text(encoding="utf-8")) or {}
        e=json.loads((root/"method/v2.9-release-evidence.json").read_text(encoding="utf-8"))
        c=yaml.safe_load((root/"method/v2.9-release-candidate.yaml").read_text(encoding="utf-8")) or {}
    except (OSError,yaml.YAMLError,json.JSONDecodeError) as exc: return [f"cannot read v2.9 qualification artifacts: {exc}"]
    if q.get("release")!="v2.9.0": errors.append("release must be v2.9.0")
    if q.get("qualification")!="evidence-qualified-impact-source-authority-reproducible-assurance": errors.append("qualification theme mismatch")
    if q.get("stable_compatibility")!=EXPECTED: errors.append("stable compatibility differs from the declared v2.9 boundary")
    if set(q.get("qualified_capabilities") or {})!=CAPABILITIES: errors.append("qualified capability inventory is incomplete")
    if set(q.get("release_gates") or {})!=GATES: errors.append("release gate inventory is incomplete")
    for n,s in (q.get("qualified_capabilities") or {}).items():
        if s not in {"PENDING","PASS","FAIL","INDETERMINATE"}: errors.append(f"invalid capability state {n}: {s}")
    for n,s in (q.get("release_gates") or {}).items():
        if s not in {"PENDING","PASS","FAIL","INDETERMINATE"}: errors.append(f"invalid gate state {n}: {s}")
    for name,path in (q.get("evidence") or {}).items():
        if name=="tracking_issue":
            if path!="https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1126": errors.append("unexpected tracking issue")
        elif not isinstance(path,str) or not (root/path).is_file(): errors.append(f"missing qualification evidence document {name}: {path}")
    cand=c.get("candidate") or {}
    if cand.get("version")!="2.9.0" or cand.get("proposed_tag")!="v2.9.0": errors.append("candidate version/tag mismatch")
    if cand.get("base_tag")!="v2.8.0": errors.append("candidate base tag must remain v2.8.0")
    if cand.get("source_base_sha")!="7cd34ed53c537a43c0c5ed1a526a3748055e3f1c": errors.append("candidate source base must pin the v2.8.0 release commit")
    if cand.get("stable_contract")!={"engine":"rahp-engine-contract-v1","engine_revision":"1.3","result_schema":1,"evidence_retention":"rahp-evidence-retention-v1"}: errors.append("candidate stable contract mismatch")
    if cand.get("codename")!="Common Windmill": errors.append("candidate codename mismatch")
    cut=q.get("release_cut") or {}
    if cut.get("independent_adoption")!="NOT_YET_TESTED": errors.append("independent adoption cannot be silently promoted")
    if cut.get("selected_common_name")!="Common Windmill" or cut.get("selected_scientific_name")!="Atrophaneura polyeuctes": errors.append("release codename identity mismatch")
    state=q.get("state")
    if state=="PREQUALIFICATION":
        if cut.get("publication_authorized") is not False: errors.append("prequalification cannot authorize publication")
        if cut.get("candidate_sha") is not None: errors.append("prequalification candidate_sha must be null")
        errors.extend(assess_evidence(e,require_pass=False))
    elif state=="QUALIFIED":
        if any(v!="PASS" for v in (q.get("release_gates") or {}).values()): errors.append("qualified release requires all gates PASS")
        if any(v!="PASS" for v in (q.get("qualified_capabilities") or {}).values()): errors.append("qualified release requires all declared capabilities PASS")
        if cut.get("publication_authorized") is not True: errors.append("qualified release requires publication authorization")
        sha=cut.get("candidate_sha")
        if not isinstance(sha,str) or not SHA.fullmatch(sha): errors.append("qualified release requires full candidate SHA")
        if e.get("candidate_sha")!=sha: errors.append("qualification/evidence candidate SHA mismatch")
        errors.extend(assess_evidence(e,require_pass=True))
    else: errors.append("state must be PREQUALIFICATION or QUALIFIED")
    return errors
def main()->int:
    errors=validate()
    if errors:
        for error in errors: print("ERROR:",error)
        return 1
    print("PASS v2.9 qualification declaration"); return 0
if __name__=="__main__": sys.exit(main())
