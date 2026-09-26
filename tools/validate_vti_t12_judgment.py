#!/usr/bin/env python3
"""Validate the T12 VTI release/upstream judgment package."""
from __future__ import annotations

from pathlib import Path
import json
import sys
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "vti-programme-t12.yaml"
PROFILE = ROOT / "profiles" / "dtg" / "vti-assessment-profile.yaml"
SUBMISSIONS = ROOT / "examples" / "cross-spec" / "vti-assessment"
PROJECT_STATUS = ROOT / "PROJECT-STATUS.yaml"
PACKAGE = ROOT / "package.json"
DOC = ROOT / "docs" / "vti-release-upstream-judgment.md"


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(value, dict):
        raise AssertionError(f"{path}: top-level value must be a mapping")
    return value


def validate() -> None:
    data = load_yaml(DATA)
    profile = load_yaml(PROFILE)
    status = load_yaml(PROJECT_STATUS)
    package = json.loads(PACKAGE.read_text(encoding="utf-8"))

    vti = data.get("vti_source") or {}
    profile_vti = profile.get("vti_source") or {}
    for field in ("repository", "document_status", "commit"):
        if vti.get(field) != profile_vti.get(field):
            raise AssertionError(f"T12 VTI source {field} does not match active assessment profile")
    if vti.get("drift_detected") is not False:
        raise AssertionError("T12 package must not claim a clean judgment while VTI drift is detected")

    release = data.get("release_judgment") or {}
    current = str(release.get("current_stable_release") or "")
    if release.get("disposition") != "minor_release_warranted":
        raise AssertionError("T12 release disposition must be explicit")
    parts = current.split(".")
    expected = f"{parts[0]}.{int(parts[1]) + 1}.0"
    if str(release.get("candidate_next_version") or "") != expected:
        raise AssertionError(f"candidate next minor must be {expected}")
    repository_version = str(package.get("version") or "")
    status_version = str(status.get("stable_release") or "")
    if repository_version != status_version:
        raise AssertionError("repository package and PROJECT-STATUS release surfaces disagree")

    def semver_tuple(value: str) -> tuple[int, int, int]:
        parts = value.split(".")
        if len(parts) != 3:
            raise AssertionError(f"invalid semantic version: {value}")
        return tuple(int(part) for part in parts)

    # T12 is immutable historical evidence for the v2.4 release decision. Later
    # qualified toolkit releases must not invalidate that historical judgment.
    # The current repository may therefore advance beyond the approved next minor,
    # provided it has not regressed below the release T12 justified.
    if semver_tuple(repository_version) < semver_tuple(expected):
        raise AssertionError(
            f"repository release {repository_version} predates T12-approved minimum {expected}"
        )
    if release.get("version_commitment_authorized") is not False:
        raise AssertionError("T12 must not silently authorize a version commitment")
    if release.get("release_cut_authorized") is not False:
        raise AssertionError("T12 must not silently authorize a release cut")
    if release.get("codename_selected") is not False:
        raise AssertionError("release codename must remain unselected until release time")

    compat = release.get("compatibility") or {}
    expected_compat = {
        "engine_contract": "rahp-engine-contract-v1",
        "engine_revision": "1.3",
        "normalized_result_schema": 1,
        "evidence_retention_contract": "rahp-evidence-retention-v1",
    }
    for key, expected_value in expected_compat.items():
        if compat.get(key) != expected_value:
            raise AssertionError(f"compatibility drift in {key}")

    reconciliation = data.get("programme_reconciliation") or {}
    mappings = profile.get("requirement_map") or []
    if reconciliation.get("family_count") != len(mappings):
        raise AssertionError("T12 family count does not match active VTI profile")
    submissions = sorted(SUBMISSIONS.glob("*.yaml"))
    if reconciliation.get("current_submissions") != len(submissions):
        raise AssertionError("T12 submission count does not match assessment directory")
    by_family = {entry.get("family"): entry for entry in mappings}
    verified = [family for family, entry in by_family.items() if entry.get("evidence_state") == "verified"]
    if reconciliation.get("verified_supported_families") != len(verified):
        raise AssertionError("T12 verified-family count does not match profile")
    if (by_family.get("privacy-composition") or {}).get("evidence_state") != "specialist_evidence_required":
        raise AssertionError("privacy specialist-evidence boundary changed")
    if (by_family.get("component-substitution") or {}).get("evidence_state") != "evidence_required":
        raise AssertionError("component-substitution evidence gate changed")

    upstream = data.get("upstream_packaging") or {}
    if upstream.get("write_authorized") is not False:
        raise AssertionError("T12 package must not authorize upstream writes")
    candidates = upstream.get("clarification_candidates") or []
    ids = [item.get("id") for item in candidates]
    if not ids or len(ids) != len(set(ids)):
        raise AssertionError("clarification candidate IDs must be non-empty and unique")
    allowed = {"candidate", "defer_pending_existing_issue"}
    for item in candidates:
        if item.get("disposition") not in allowed:
            raise AssertionError(f"invalid clarification disposition: {item.get('disposition')}")

    decisions = data.get("next_decisions") or []
    if {item.get("id") for item in decisions} != {"release-cut", "upstream-write"}:
        raise AssertionError("T12 must preserve both explicit approval gates")
    if not all(item.get("requires_explicit_approval") is True for item in decisions):
        raise AssertionError("T12 critical decisions must require explicit approval")

    doc = DOC.read_text(encoding="utf-8")
    required_doc_terms = [
        f"v{current}",
        f"v{expected}",
        vti["commit"],
        "RAHP-VTI-PRV-001",
        "component substitution remains `evidence_required`",
        "VTI-CLAR-001",
        "VTI-CLAR-002",
        "VTI-CLAR-003",
        "VTI-CLAR-004",
        "VTI-CLAR-005",
        "VTI-CLAR-006",
        "release cut",
        "upstream write",
    ]
    for term in required_doc_terms:
        if term not in doc:
            raise AssertionError(f"T12 documentation missing required term: {term}")


def main() -> int:
    try:
        validate()
    except (OSError, ValueError, json.JSONDecodeError, yaml.YAMLError, AssertionError) as exc:
        print(f"FAIL VTI T12 release/upstream judgment: {exc}", file=sys.stderr)
        return 1
    print("PASS VTI T12 release/upstream judgment")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
