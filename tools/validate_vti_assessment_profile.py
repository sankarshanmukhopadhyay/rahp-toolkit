#!/usr/bin/env python3
"""Validate the RAHP VTI composition assessment profile and submissions."""
from __future__ import annotations

from pathlib import Path
import json
import sys
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "vti-assessment.schema.json"
PROFILE_PATH = ROOT / "profiles" / "dtg" / "vti-assessment-profile.yaml"
SUBMISSION_PATH = ROOT / "examples" / "cross-spec" / "vti-assessment" / "false-independence.yaml"

EXPECTED_VTI_COMMIT = "75391a27a5d9a1794266b2e3bdeb8be68fa4db40"
EXPECTED_FALSE_INDEPENDENCE = {
    "VTI-CMP-070",
    "VTI-CMP-071",
    "VTI-CMP-072",
    "VTI-CMP-073",
    "VTI-CMP-074",
}
EXPECTED_EVIDENCE_IDS = {f"SR-XSP-FI-{i:03d}" for i in range(1, 8)}


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(value, dict):
        raise AssertionError(f"{path}: top-level value must be a mapping")
    return value


def validate_profile(profile: dict[str, Any]) -> None:
    source = profile.get("vti_source") or {}
    if source.get("document_status") != "Working Draft 0.1.0":
        raise AssertionError("profile must pin VTI Working Draft 0.1.0")
    if source.get("commit") != EXPECTED_VTI_COMMIT:
        raise AssertionError("profile VTI commit pin drifted")

    dispositions = profile.get("dispositions") or {}
    if set(dispositions) != {"supported", "refuted", "indeterminate"}:
        raise AssertionError("profile must define supported/refuted/indeterminate only")

    rules = set(profile.get("non_inference_rules") or [])
    if "missing evidence != supported" not in rules:
        raise AssertionError("profile must preserve missing-evidence boundary")
    if "component conformance != composition assurance" not in rules:
        raise AssertionError("profile must preserve conformance/assurance boundary")

    families = {entry.get("family"): entry for entry in profile.get("requirement_map") or []}
    false_independence = families.get("false-independence")
    if not false_independence:
        raise AssertionError("false-independence requirement mapping missing")
    if set(false_independence.get("requirements") or []) != EXPECTED_FALSE_INDEPENDENCE:
        raise AssertionError("false-independence requirement map incomplete")
    if false_independence.get("evidence_state") != "verified":
        raise AssertionError("completed false-independence family must remain verified")


def validate_submission(submission: dict[str, Any], schema: dict[str, Any]) -> None:
    errors = sorted(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(submission),
        key=lambda error: list(error.path),
    )
    if errors:
        detail = "; ".join(f"{'/'.join(map(str, e.path)) or '<root>'}: {e.message}" for e in errors)
        raise AssertionError(f"submission schema validation failed: {detail}")

    if submission["vti_source"]["commit"] != EXPECTED_VTI_COMMIT:
        raise AssertionError("submission source pin does not match profile")
    if set(submission["requirements"]) != EXPECTED_FALSE_INDEPENDENCE:
        raise AssertionError("submission does not cover the complete false-independence requirement set")

    ids = [item["id"] for item in submission["evidence"]]
    if len(ids) != len(set(ids)):
        raise AssertionError("duplicate evidence identifiers are not permitted")
    if set(ids) != EXPECTED_EVIDENCE_IDS:
        raise AssertionError("submission must preserve SR-XSP-FI-001..007 evidence lineage")

    for item in submission["evidence"]:
        ref = ROOT / item["ref"]
        if item["kind"] in {"test", "fixture"} and not ref.exists():
            raise AssertionError(f"referenced executable evidence does not exist: {item['ref']}")

    if submission["reassessment"]["state"] != "current":
        raise AssertionError("first published assessment must be current")
    if not submission["counter_cases"]:
        raise AssertionError("legitimate counter-cases must not be omitted")
    if not submission["residual_uncertainty"]:
        raise AssertionError("residual uncertainty must remain explicit")


def self_test(schema: dict[str, Any], submission: dict[str, Any]) -> None:
    bad = dict(submission)
    bad["evidence"] = []
    errors = list(Draft202012Validator(schema).iter_errors(bad))
    if not errors:
        raise AssertionError("negative fixture: missing evidence unexpectedly validates")

    bad_disposition = dict(submission)
    bad_disposition["disposition"] = "pass"
    if not list(Draft202012Validator(schema).iter_errors(bad_disposition)):
        raise AssertionError("negative fixture: unsafe PASS disposition unexpectedly validates")


def main() -> int:
    try:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        profile = load_yaml(PROFILE_PATH)
        submission = load_yaml(SUBMISSION_PATH)
        validate_profile(profile)
        validate_submission(submission, schema)
        self_test(schema, submission)
    except (OSError, json.JSONDecodeError, yaml.YAMLError, AssertionError) as exc:
        print(f"FAIL VTI assessment profile: {exc}", file=sys.stderr)
        return 1

    print("PASS VTI assessment profile")
    print(f"- source: Working Draft 0.1.0 @ {EXPECTED_VTI_COMMIT}")
    print("- first submission: RAHP-VTI-FI-001")
    print("- requirements: " + ", ".join(sorted(EXPECTED_FALSE_INDEPENDENCE)))
    print("- boundary: independent assurance evidence; no VTI conformance authority claimed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
