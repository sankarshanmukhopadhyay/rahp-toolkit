#!/usr/bin/env python3
"""Validate v2.10 release qualification claims without publishing."""
from __future__ import annotations
import json,re,sys
from pathlib import Path
import yaml
from validate_v210_release_evidence import assess as assess_evidence
ROOT=Path(__file__).resolve().parents[1]
EXPECTED={"engine_contract":"rahp-engine-contract-v1","engine_revision":"1.3","normalized_result_schema":1,"evidence_retention_contract":"rahp-evidence-retention-v1"}
GATES={"full_regression","typescript_conformance","stable_compatibility","docs_rendering","publication_metadata","release_publication_preflight","security_review","owner_approval"}
CAPABILITIES={"source_and_claim_integrity","read_only_result_explanation","reproducible_adoption","consumer_conformance_and_external_returns","governed_publication_ownership","monitor_and_review_integrity","release_supply_chain_reproducibility"}
SHA=re.compile(r"^[0-9a-f]{40}$")
def validate(root: Path=ROOT)->list[str]:
    errors=[]
    try:
        q=yaml.safe_load((root/"method/v2.10-release-qualification.yaml").read_text(encoding="utf-8")) or {}
        e=json.loads((root/"method/v2.10-release-evidence.json").read_text(encoding="utf-8"))
        c=yaml.safe_load((root/"method/v2.10-release-candidate.yaml").read_text(encoding="utf-8")) or {}
    except (OSError,yaml.YAMLError,json.JSONDecodeError) as exc: return [f"cannot read v2.10 qualification artifacts: {exc}"]
    if not all(isinstance(x,dict) for x in (q,e,c)): return ["qualification artifacts must be mappings"]
    if not all(isinstance(q.get(k),dict) for k in ("release_gates","qualified_capabilities","evidence","release_cut","bounded_or_residual")): return ["qualification mappings missing or malformed"]
    if q.get("release")!="v2.10.0": errors.append("release must be v2.10.0")
    if q.get("qualification")!="operational-integrity-reproducibility-governed-assurance-interoperability": errors.append("qualification theme mismatch")
    if q.get("stable_compatibility")!=EXPECTED: errors.append("stable compatibility differs from the declared v2.10 boundary")
    if set(q.get("qualified_capabilities") or {})!=CAPABILITIES: errors.append("qualified capability inventory is incomplete")
    if set(q.get("release_gates") or {})!=GATES: errors.append("release gate inventory is incomplete")
    for n,s in (q.get("qualified_capabilities") or {}).items():
        if s not in {"PENDING","PASS","FAIL","INDETERMINATE"}: errors.append(f"invalid capability state {n}: {s}")
    for n,s in (q.get("release_gates") or {}).items():
        if s not in {"PENDING","PASS","FAIL","INDETERMINATE"}: errors.append(f"invalid gate state {n}: {s}")
    expected_evidence={"candidate_manifest":"method/v2.10-release-candidate.yaml","release_evidence":"method/v2.10-release-evidence.json","release_notes":"docs/releases/v2.10.0.md","security_disposition":"docs/review/current-main-release-security-disposition-2026-11-25.md","tracking_issue":"https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1179"}
    if q["evidence"]!=expected_evidence: errors.append("qualification evidence inventory or identity mismatch")
    for name,path in (q.get("evidence") or {}).items():
        if name=="tracking_issue":
            if path!="https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1179": errors.append("unexpected tracking issue")
        elif not isinstance(path,str) or not (root/path).is_file(): errors.append(f"missing qualification evidence document {name}: {path}")
    cand=c.get("candidate") or {}
    if cand.get("version")!="2.10.0" or cand.get("proposed_tag")!="v2.10.0": errors.append("candidate version/tag mismatch")
    if cand.get("base_tag")!="v2.9.0": errors.append("candidate base tag must remain v2.9.0")
    if cand.get("source_base_sha")!="89831dd739625a416e5b4d84e3486bbfbed5243f": errors.append("candidate source base must pin the v2.9.0 release commit")
    if cand.get("stable_contract")!={"engine":"rahp-engine-contract-v1","engine_revision":"1.3","result_schema":1,"evidence_retention":"rahp-evidence-retention-v1"}: errors.append("candidate stable contract mismatch")
    if cand.get("codename")!="Common Banded Peacock": errors.append("candidate codename mismatch")
    cut=q.get("release_cut") or {}
    if cut.get("independent_adoption")!="NOT_YET_TESTED": errors.append("independent adoption cannot be silently promoted")
    if cut.get("selected_common_name")!="Common Banded Peacock" or cut.get("selected_scientific_name")!="Papilio crino": errors.append("release codename identity mismatch")
    if set(c.get("qualified_scope") or []) != CAPABILITIES: errors.append("candidate scope mismatch")
    if cand.get("publication_authorized") is not False or cand.get("release_sha") is not None or cand.get("status")!="prequalification": errors.append("candidate record must remain historical and non-authorizing")
    if c.get("release_gates") != {gate:"PENDING" for gate in GATES}: errors.append("candidate gates must remain pending")
    if (c.get("adoption") or {}).get("independent_participant")!="NOT_YET_TESTED" or (c.get("adoption") or {}).get("terminal_assurance_claim") is not False: errors.append("candidate adoption boundary mismatch")
    residual=q.get("bounded_or_residual") or {}
    if residual.get("independent_adoption")!="NOT_YET_TESTED" or residual.get("issue_958_admin_and_human_review_evidence")!="NOT_VERIFIED" or residual.get("registry_live_interoperability")!="PARTIALLY_QUALIFIED" or residual.get("monitored_event_canonical_accounting")!="WORK_OPEN": errors.append("residual boundary cannot be promoted")
    if residual.get("people_impact_causal_pathways")!="ZERO_QUALIFIED_PATHWAYS" or residual.get("deployment_runtime_evidence")!="SOURCE_PINNED_BOUNDED": errors.append("people-impact or deployment residual cannot be promoted")
    state=q.get("state")
    if state=="PREQUALIFICATION":
        if any(x!="PENDING" for x in q["release_gates"].values()) or any(x!="PENDING" for x in q["qualified_capabilities"].values()): errors.append("prequalification cannot claim passed gates or capabilities")
        if residual.get("historical_squash_dco")!="DISCREPANCY_REQUIRES_OWNER_DISPOSITION": errors.append("historical DCO disposition remains pending")
        if cut.get("publication_authorized") is not False: errors.append("prequalification cannot authorize publication")
        if cut.get("candidate_sha") is not None: errors.append("prequalification candidate_sha must be null")
        errors.extend(assess_evidence(e,require_pass=False))
    elif state=="QUALIFIED":
        if residual.get("historical_squash_dco")!="DISCLOSED_OWNER_ACCEPTED": errors.append("qualified release requires explicit historical DCO disposition")
        owner=(e.get("gates") or {}).get("owner_approval") or {}
        if owner.get("historical_dco_disposition")!="ACCEPT_DISCLOSED_EXCEPTION": errors.append("owner evidence must explicitly accept disclosed historical DCO exception")
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
    print("PASS v2.10 qualification declaration"); return 0
if __name__=="__main__": sys.exit(main())
