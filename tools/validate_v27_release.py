#!/usr/bin/env python3
"""Validate v2.7 release qualification claims without approving publication."""
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "engine_contract": "rahp-engine-contract-v1",
    "engine_revision": "1.3",
    "normalized_result_schema": 1,
    "evidence_retention_contract": "rahp-evidence-retention-v1",
}
GATES = {
    "full_regression", "typescript_conformance", "stable_compatibility",
    "docs_rendering", "publication_metadata", "security_review", "owner_approval",
}
EXPERIMENTAL = {
    "optional-reasoning-trace", "sociotechnical-assurance",
    "r1-evidence-adequacy", "r2-temporal-provenance",
    "r3-reproducibility-challenge",
}


def validate(root: Path = ROOT) -> list[str]:
    errors = []
    try:
        q = yaml.safe_load((root / "method/v2.7-release-qualification.yaml").read_text()) or {}
    except (OSError, yaml.YAMLError) as exc:
        return [f"cannot read v2.7 qualification: {exc}"]
    if q.get("release") != "v2.7.0":
        errors.append("release must be v2.7.0")
    if q.get("qualification") != "post-v26-maintenance-and-optional-reasoning-profiles":
        errors.append("qualification theme mismatch")
    if q.get("stable_compatibility") != EXPECTED:
        errors.append("stable compatibility contract differs from v2.6")
    if set(q.get("experimental_profiles") or []) != EXPERIMENTAL:
        errors.append("experimental profile inventory changed without review")
    if set((q.get("release_gates") or {})) != GATES:
        errors.append("release gate inventory is incomplete")
    for gate, state in (q.get("release_gates") or {}).items():
        if state not in {"PENDING", "PASS", "FAIL", "INDETERMINATE"}:
            errors.append(f"invalid gate state {gate}: {state}")
    for name, state in (q.get("qualified_capabilities") or {}).items():
        if state not in {"PENDING", "PASS", "FAIL", "INDETERMINATE"}:
            errors.append(f"invalid qualified capability state {name}: {state}")
    for name, path in (q.get("evidence") or {}).items():
        if name == "tracking_issue":
            if path != "https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/941":
                errors.append("unexpected tracking issue")
        elif not isinstance(path, str) or not (root / path).is_file():
            errors.append(f"missing qualification evidence document {name}: {path}")
    cut = q.get("release_cut") or {}
    if cut.get("manual_publication_required") is not True:
        errors.append("manual publication is mandatory")
    if cut.get("independent_adoption") != "NOT_YET_TESTED":
        errors.append("independent adoption cannot be silently promoted")
    if q.get("state") == "PREQUALIFICATION":
        if cut.get("publication_authorized") is not False:
            errors.append("prequalification cannot authorize publication")
        if cut.get("candidate_sha") is not None or not cut.get("selected_common_name") or not cut.get("selected_scientific_name"):
            errors.append("prequalification requires a governed name but no qualified SHA")
    elif q.get("state") == "QUALIFIED":
        if any(state != "PASS" for state in (q.get("release_gates") or {}).values()):
            errors.append("qualified release requires all gates PASS")
        if cut.get("publication_authorized") is not True:
            errors.append("qualified release requires explicit publication authorization")
        if not all(cut.get(key) for key in ("candidate_sha", "selected_common_name", "selected_scientific_name")):
            errors.append("qualified release requires pinned SHA and governed name")
    else:
        errors.append("state must be PREQUALIFICATION or QUALIFIED")
    return errors


def main():
    errors = validate()
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS v2.7 qualification declaration structure; no independent evidence provenance verification")
    return 0


if __name__ == "__main__":
    sys.exit(main())
