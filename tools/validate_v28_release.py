#!/usr/bin/env python3
"""Validate v2.8 release qualification claims without publishing."""
from __future__ import annotations

import json
from pathlib import Path
import re
import sys
import yaml

from validate_v28_release_evidence import assess as assess_evidence

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "engine_contract": "rahp-engine-contract-v1",
    "engine_revision": "1.3",
    "normalized_result_schema": 1,
    "evidence_retention_contract": "rahp-evidence-retention-v1",
}
GATES = {
    "full_regression",
    "typescript_conformance",
    "stable_compatibility",
    "docs_rendering",
    "publication_metadata",
    "release_publication_preflight",
    "security_review",
    "owner_approval",
}
CAPABILITIES = {
    "comparative_assurance",
    "adversarial_assurance",
    "agent_authority_and_continuity",
    "lifecycle_continuation_authority",
    "consumer_interaction_evidence",
    "observability_harm_vectors",
    "release_publication_hardening",
}
SHA = re.compile(r"^[0-9a-f]{40}$")


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    try:
        q = yaml.safe_load((root / "method/v2.8-release-qualification.yaml").read_text(encoding="utf-8")) or {}
        e = json.loads((root / "method/v2.8-release-evidence.json").read_text(encoding="utf-8"))
        c = yaml.safe_load((root / "method/v2.8-release-candidate.yaml").read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError, json.JSONDecodeError) as exc:
        return [f"cannot read v2.8 qualification artifacts: {exc}"]

    if q.get("release") != "v2.8.0":
        errors.append("release must be v2.8.0")
    if q.get("qualification") != "comparative-adversarial-consumer-interaction-assurance":
        errors.append("qualification theme mismatch")
    if q.get("stable_compatibility") != EXPECTED:
        errors.append("stable compatibility differs from the declared v2.8 boundary")
    if set(q.get("qualified_capabilities") or {}) != CAPABILITIES:
        errors.append("qualified capability inventory is incomplete")
    if set(q.get("release_gates") or {}) != GATES:
        errors.append("release gate inventory is incomplete")

    for name, state in (q.get("qualified_capabilities") or {}).items():
        if state not in {"PENDING", "PASS", "FAIL", "INDETERMINATE"}:
            errors.append(f"invalid capability state {name}: {state}")
    for gate, state in (q.get("release_gates") or {}).items():
        if state not in {"PENDING", "PASS", "FAIL", "INDETERMINATE"}:
            errors.append(f"invalid gate state {gate}: {state}")

    for name, path in (q.get("evidence") or {}).items():
        if name == "tracking_issue":
            if path != "https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1034":
                errors.append("unexpected tracking issue")
        elif not isinstance(path, str) or not (root / path).is_file():
            errors.append(f"missing qualification evidence document {name}: {path}")

    cand = c.get("candidate") or {}
    if cand.get("version") != "2.8.0" or cand.get("proposed_tag") != "v2.8.0":
        errors.append("candidate version/tag mismatch")
    if cand.get("base_tag") != "v2.7.0":
        errors.append("candidate base tag must remain v2.7.0")
    if cand.get("stable_contract") != {
        "engine": "rahp-engine-contract-v1",
        "engine_revision": "1.3",
        "result_schema": 1,
        "evidence_retention": "rahp-evidence-retention-v1",
    }:
        errors.append("candidate stable contract mismatch")
    if cand.get("codename") != "Common Birdwing":
        errors.append("candidate codename mismatch")

    cut = q.get("release_cut") or {}
    state = q.get("state")
    if cut.get("independent_adoption") != "NOT_YET_TESTED":
        errors.append("independent adoption cannot be silently promoted")
    if cut.get("selected_common_name") != "Common Birdwing" or cut.get("selected_scientific_name") != "Troides helena":
        errors.append("release codename identity mismatch")

    if state == "PREQUALIFICATION":
        if cut.get("publication_authorized") is not False:
            errors.append("prequalification cannot authorize publication")
        if cut.get("candidate_sha") is not None:
            errors.append("prequalification candidate_sha must be null")
        errors.extend(assess_evidence(e, require_pass=False))
    elif state == "QUALIFIED":
        if any(v != "PASS" for v in (q.get("release_gates") or {}).values()):
            errors.append("qualified release requires all gates PASS")
        if any(v != "PASS" for v in (q.get("qualified_capabilities") or {}).values()):
            errors.append("qualified release requires all declared capabilities PASS")
        if cut.get("publication_authorized") is not True:
            errors.append("qualified release requires publication authorization")
        sha = cut.get("candidate_sha")
        if not isinstance(sha, str) or not SHA.fullmatch(sha):
            errors.append("qualified release requires full candidate SHA")
        if e.get("candidate_sha") != sha:
            errors.append("qualification/evidence candidate SHA mismatch")
        errors.extend(assess_evidence(e, require_pass=True))
    else:
        errors.append("state must be PREQUALIFICATION or QUALIFIED")
    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS v2.8 qualification declaration")
    return 0


if __name__ == "__main__":
    sys.exit(main())
