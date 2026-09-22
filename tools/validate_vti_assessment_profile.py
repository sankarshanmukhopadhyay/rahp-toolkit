#!/usr/bin/env python3
"""Validate the RAHP VTI composition assessment profile and all submissions."""
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
SUBMISSION_DIR = ROOT / "examples" / "cross-spec" / "vti-assessment"

EXPECTED_VTI_COMMIT = "75391a27a5d9a1794266b2e3bdeb8be68fa4db40"
EXPECTED_DOCUMENT_STATUS = "Working Draft 0.1.0"


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(value, dict):
        raise AssertionError(f"{path}: top-level value must be a mapping")
    return value


def requirement_map(profile: dict[str, Any]) -> dict[str, dict[str, Any]]:
    entries = profile.get("requirement_map") or []
    mapped: dict[str, dict[str, Any]] = {}
    for entry in entries:
        family = str(entry.get("family") or "").strip()
        if not family or family in mapped:
            raise AssertionError(f"profile contains invalid or duplicate family: {family!r}")
        mapped[family] = entry
    return mapped


def validate_profile(profile: dict[str, Any]) -> dict[str, dict[str, Any]]:
    source = profile.get("vti_source") or {}
    if source.get("document_status") != EXPECTED_DOCUMENT_STATUS:
        raise AssertionError(f"profile must pin VTI {EXPECTED_DOCUMENT_STATUS}")
    if source.get("commit") != EXPECTED_VTI_COMMIT:
        raise AssertionError("profile VTI commit pin drifted")

    dispositions = profile.get("dispositions") or {}
    if set(dispositions) != {"supported", "refuted", "indeterminate"}:
        raise AssertionError("profile must define supported/refuted/indeterminate only")

    rules = set(profile.get("non_inference_rules") or [])
    for required in {
        "missing evidence != supported",
        "component conformance != composition assurance",
        "protocol completion != trust-outcome completion",
    }:
        if required not in rules:
            raise AssertionError(f"profile missing non-inference rule: {required}")

    families = requirement_map(profile)
    if not any(entry.get("evidence_state") == "verified" for entry in families.values()):
        raise AssertionError("profile must contain at least one verified assessment family")
    return families


def validate_schema(
    submission: dict[str, Any],
    schema: dict[str, Any],
    path: Path,
) -> None:
    errors = sorted(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(submission),
        key=lambda error: list(error.path),
    )
    if errors:
        detail = "; ".join(
            f"{'/'.join(map(str, e.path)) or '<root>'}: {e.message}" for e in errors
        )
        raise AssertionError(f"{path.name}: schema validation failed: {detail}")


def validate_submission(
    submission: dict[str, Any],
    schema: dict[str, Any],
    families: dict[str, dict[str, Any]],
    path: Path,
) -> None:
    validate_schema(submission, schema, path)

    source = submission["vti_source"]
    if source["commit"] != EXPECTED_VTI_COMMIT:
        raise AssertionError(f"{path.name}: source pin does not match active profile")
    if source["document_status"] != EXPECTED_DOCUMENT_STATUS:
        raise AssertionError(f"{path.name}: document status does not match active profile")

    family = submission["family"]
    mapping = families.get(family)
    if mapping is None:
        raise AssertionError(f"{path.name}: unknown assessment family {family!r}")

    expected_requirements = set(mapping.get("requirements") or [])
    actual_requirements = set(submission["requirements"])
    evidence_state = mapping.get("evidence_state")
    if evidence_state != "verified" and submission["disposition"] != "indeterminate":
        raise AssertionError(
            f"{path.name}: non-verified family {family!r} may only publish an indeterminate assessment"
        )
    if actual_requirements != expected_requirements:
        raise AssertionError(
            f"{path.name}: requirements {sorted(actual_requirements)} do not exactly "
            f"match profile family {family}: {sorted(expected_requirements)}"
        )

    ids = [item["id"] for item in submission["evidence"]]
    if len(ids) != len(set(ids)):
        raise AssertionError(f"{path.name}: duplicate evidence identifiers are not permitted")

    for item in submission["evidence"]:
        ref = ROOT / item["ref"]
        if item["kind"] in {"test", "fixture"} and not ref.exists():
            raise AssertionError(
                f"{path.name}: referenced executable evidence does not exist: {item['ref']}"
            )

    state = submission["reassessment"]["state"]
    if state == "current" and submission["disposition"] == "supported" and not submission["evidence"]:
        raise AssertionError(f"{path.name}: current supported assessment cannot have no evidence")
    if not submission["counter_cases"]:
        raise AssertionError(f"{path.name}: legitimate counter-cases must not be omitted")
    if not submission["residual_uncertainty"]:
        raise AssertionError(f"{path.name}: residual uncertainty must remain explicit")


def discover_submissions() -> list[Path]:
    paths = sorted(SUBMISSION_DIR.glob("*.yaml"))
    if not paths:
        raise AssertionError("no VTI assessment submissions found")
    return paths


def validate_collection(
    schema: dict[str, Any],
    profile: dict[str, Any],
) -> list[dict[str, Any]]:
    families = validate_profile(profile)
    submissions: list[dict[str, Any]] = []
    assessment_ids: set[str] = set()
    submitted_families: set[str] = set()

    for path in discover_submissions():
        submission = load_yaml(path)
        validate_submission(submission, schema, families, path)

        assessment_id = submission["assessment_id"]
        if assessment_id in assessment_ids:
            raise AssertionError(f"duplicate assessment_id across submissions: {assessment_id}")
        assessment_ids.add(assessment_id)

        family = submission["family"]
        if family in submitted_families:
            raise AssertionError(f"multiple complete submissions currently claim family: {family}")
        submitted_families.add(family)
        submissions.append(submission)

    verified_families = {
        family for family, entry in families.items() if entry.get("evidence_state") == "verified"
    }
    missing = verified_families - submitted_families
    if missing:
        raise AssertionError(
            f"verified assessment families missing submissions: {sorted(missing)}"
        )

    return submissions


def self_test(schema: dict[str, Any], submissions: list[dict[str, Any]]) -> None:
    sample = submissions[0]

    bad = dict(sample)
    bad["evidence"] = []
    if not list(Draft202012Validator(schema).iter_errors(bad)):
        raise AssertionError("negative fixture: missing evidence unexpectedly validates")

    bad_disposition = dict(sample)
    bad_disposition["disposition"] = "pass"
    if not list(Draft202012Validator(schema).iter_errors(bad_disposition)):
        raise AssertionError("negative fixture: unsafe PASS disposition unexpectedly validates")

    bad_family = dict(sample)
    bad_family["family"] = "unknown-family"
    try:
        validate_submission(
            bad_family,
            schema,
            requirement_map(load_yaml(PROFILE_PATH)),
            Path("negative-unknown-family.yaml"),
        )
    except AssertionError:
        pass
    else:
        raise AssertionError("negative fixture: unknown family unexpectedly validates")


def main() -> int:
    try:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        profile = load_yaml(PROFILE_PATH)
        submissions = validate_collection(schema, profile)
        self_test(schema, submissions)
    except (OSError, json.JSONDecodeError, yaml.YAMLError, AssertionError) as exc:
        print(f"FAIL VTI assessment profile: {exc}", file=sys.stderr)
        return 1

    print("PASS VTI assessment profile")
    print(f"- source: {EXPECTED_DOCUMENT_STATUS} @ {EXPECTED_VTI_COMMIT}")
    print(f"- submissions: {len(submissions)}")
    for submission in sorted(submissions, key=lambda item: item["assessment_id"]):
        print(
            f"- {submission['assessment_id']}: {submission['family']} / "
            f"{submission['disposition']} / "
            f"{', '.join(submission['requirements'])}"
        )
    print("- boundary: independent assurance evidence; no VTI conformance authority claimed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
