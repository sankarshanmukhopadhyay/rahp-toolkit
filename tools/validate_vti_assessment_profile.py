#!/usr/bin/env python3
"""Validate the RAHP VTI composition assessment profile and all submissions."""
from __future__ import annotations

from pathlib import Path
import json
import re
import sys
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "vti-assessment.schema.json"
PROFILE_PATH = ROOT / "profiles" / "dtg" / "vti-assessment-profile.yaml"
SUBMISSION_DIR = ROOT / "examples" / "cross-spec" / "vti-assessment"

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
    if source.get("repository") != "trustoverip/dtgwg-vti-spec":
        raise AssertionError("profile must identify the authoritative VTI repository")
    if not str(source.get("document_status") or "").startswith("Working Draft "):
        raise AssertionError("profile must pin an explicit VTI Working Draft status")
    if not re.fullmatch(r"[0-9a-f]{40}", str(source.get("commit") or "")):
        raise AssertionError("profile VTI commit must be an immutable lowercase 40-hex SHA")

    dispositions = profile.get("dispositions") or {}
    if set(dispositions) != {"supported", "refuted", "indeterminate"}:
        raise AssertionError("profile must define supported/refuted/indeterminate only")

    rules = set(profile.get("non_inference_rules") or [])
    for required in {
        "missing evidence != supported",
        "component conformance != composition assurance",
        "protocol completion != trust-outcome completion",
        "cryptographic verification != current authority",
    }:
        if required not in rules:
            raise AssertionError(f"profile missing non-inference rule: {required}")

    families = requirement_map(profile)
    expected_complete_families = {
        family for family, entry in families.items()
        if entry.get("evidence_state") == "verified"
    }
    for family in expected_complete_families:
        entry = families.get(family)
        if not entry:
            raise AssertionError(f"required assessment family missing from profile: {family}")
        if entry.get("evidence_state") != "verified":
            raise AssertionError(f"{family}: complete family must remain verified")
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
    expected_source: dict[str, Any],
    path: Path,
) -> None:
    validate_schema(submission, schema, path)

    source = submission["vti_source"]
    if source["commit"] != expected_source.get("commit"):
        raise AssertionError(f"{path.name}: source pin does not match active profile")
    if source["document_status"] != expected_source.get("document_status"):
        raise AssertionError(f"{path.name}: document status does not match active profile")

    family = submission["family"]
    mapping = families.get(family)
    if mapping is None:
        raise AssertionError(f"{path.name}: unknown assessment family {family!r}")

    expected_requirements = set(mapping.get("requirements") or [])
    actual_requirements = set(submission["requirements"])
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
        validate_submission(submission, schema, families, profile["vti_source"], path)

        assessment_id = submission["assessment_id"]
        if assessment_id in assessment_ids:
            raise AssertionError(f"duplicate assessment_id across submissions: {assessment_id}")
        assessment_ids.add(assessment_id)

        family = submission["family"]
        if family in submitted_families:
            raise AssertionError(f"multiple complete submissions currently claim family: {family}")
        submitted_families.add(family)
        submissions.append(submission)

    expected_complete_families = {
        family for family, entry in families.items()
        if entry.get("evidence_state") == "verified"
    }
    missing = expected_complete_families - submitted_families
    if missing:
        raise AssertionError(f"expected complete assessment families missing: {sorted(missing)}")

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
            load_yaml(PROFILE_PATH)["vti_source"],
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
    source = profile["vti_source"]
    print(f"- source: {source['document_status']} @ {source['commit']}")
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
