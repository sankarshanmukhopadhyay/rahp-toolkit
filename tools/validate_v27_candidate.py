#!/usr/bin/env python3
"""Validate a non-publishing v2.7 candidate manifest; never qualify a release."""
from __future__ import annotations

from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "method/v2.7-release-candidate.yaml"
REQUIRED_GATES = (
    "full_regression", "typescript_conformance", "stable_compatibility",
    "docs_rendering", "publication_metadata", "security_review", "owner_approval",
)
ALLOWED_GATE_STATES = {"PENDING", "PASS", "FAIL", "INDETERMINATE"}


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    try:
        manifest = yaml.safe_load((root / "method/v2.7-release-candidate.yaml").read_text(encoding="utf-8")) or {}
        release = yaml.safe_load((root / "method/release.yaml").read_text(encoding="utf-8")) or {}
        versioning = yaml.safe_load((root / "method/versioning.yaml").read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError) as exc:
        return [f"cannot load release declarations: {exc}"]
    candidate = manifest.get("candidate") or {}
    if manifest.get("contract") != "rahp-release-candidate-qualification/v1":
        errors.append("candidate contract mismatch")
    if candidate.get("version") != "2.7.0" or candidate.get("proposed_tag") != "v2.7.0":
        errors.append("candidate version mismatch")
    if candidate.get("status") != "prequalification" or candidate.get("publication_authorized") is not False:
        errors.append("candidate must remain non-publishing prequalification")
    if candidate.get("release_sha") is not None or candidate.get("codename") != "Common Rose":
        errors.append("candidate requires governed name but cannot claim qualified release SHA")
    current = (release.get("release") or {})
    if current.get("tag") != "v2.7.0" or current.get("status") != "candidate":
        errors.append("current declaration must be non-publishing v2.7 candidate")
    if versioning.get("stable_release") != "v2.7.0":
        errors.append("stable versioning declaration changed before qualification")
    expected = {
        "engine": "rahp-engine-contract-v1",
        "engine_revision": "1.3",
        "result_schema": 1,
        "evidence_retention": "rahp-evidence-retention-v1",
    }
    if candidate.get("stable_contract") != expected:
        errors.append("candidate stable contract declarations differ from baseline")
    if (manifest.get("adoption") or {}).get("independent_participant") != "NOT_YET_TESTED":
        errors.append("independent adoption status cannot be promoted without evidence")
    if (manifest.get("adoption") or {}).get("terminal_assurance_claim") is not False:
        errors.append("candidate must not claim terminal assurance")
    gates = manifest.get("release_gates") or {}
    if set(gates) != set(REQUIRED_GATES):
        errors.append("release gate inventory incomplete or contains unexpected gates")
    for name, state in gates.items():
        if state not in ALLOWED_GATE_STATES:
            errors.append(f"invalid release gate state {name}: {state}")
    for key, path in (manifest.get("evidence") or {}).items():
        if key == "release_issue":
            if path != "https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/941":
                errors.append("unexpected release tracker")
        elif not isinstance(path, str) or not (root / path).is_file():
            errors.append(f"missing candidate evidence document: {key} ({path})")
    for path in manifest.get("required_tests") or []:
        if not isinstance(path, str) or not path.startswith("tests/") or not (root / path).is_file():
            errors.append(f"missing candidate test: {path}")
    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS v2.7.0 candidate manifest structurally valid; NOT qualified or authorized for publication")
    return 0


if __name__ == "__main__":
    sys.exit(main())
