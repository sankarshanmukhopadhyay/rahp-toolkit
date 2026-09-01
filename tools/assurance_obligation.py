#!/usr/bin/env python3
"""Semantic identity and ownership helpers for persistent RAHP assurance obligations.

Assessment attempts remain immutable terminal records. This module models the active
obligation that may survive an INDETERMINATE or FAIL attempt and identifies who must
produce which substantive artifact next.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from copy import deepcopy
from typing import Any

SCHEMA = "rahp-assurance-obligation/v1"

STATE_DEFAULTS: dict[str, dict[str, Any]] = {
    "model-gap": {
        "action_owner": {"surface": "specialist-profile"},
        "artifact_to_produce": {
            "kind": "evidence-requirement",
            "description": "Define a canonical evidence requirement, accepted evidence class, and producer binding for the unresolved assurance proposition.",
        },
        "producer": {"mode": "not-yet-defined"},
    },
    "evidence-acquirable": {
        "action_owner": {"surface": "evidence-producer"},
        "artifact_to_produce": {
            "kind": "runtime-evidence",
            "description": "Produce attributable pinned evidence satisfying the registered evidence requirement contract.",
        },
        "producer": {"mode": "registered-executable"},
    },
    "evidence-external": {
        "action_owner": {"surface": "external"},
        "artifact_to_produce": {
            "kind": "runtime-evidence",
            "description": "Supply the named external evidence package in an accepted provenance class.",
        },
        "producer": {"mode": "external"},
    },
    "evidence-stale": {
        "action_owner": {"surface": "evidence-producer"},
        "artifact_to_produce": {
            "kind": "runtime-evidence",
            "description": "Regenerate comparable evidence against the current immutable source pins.",
        },
        "producer": {"mode": "registered-executable"},
    },
    "evidence-produced": {
        "action_owner": {"surface": "specialist-profile"},
        "artifact_to_produce": {
            "kind": "other",
            "description": "Produce a scoped specialist assessment result consuming the supplied evidence.",
        },
        "producer": {"mode": "registered-executable"},
    },
    "remediation-required": {
        "action_owner": {"surface": "implementation"},
        "artifact_to_produce": {
            "kind": "implementation-remediation",
            "description": "Remediate the failed assurance surface and provide regression evidence against the same bounded proposition.",
        },
        "producer": {"mode": "external"},
    },
    "upstream-action": {
        "action_owner": {"surface": "specification"},
        "artifact_to_produce": {
            "kind": "spec-change",
            "description": "Produce the upstream normative or governance change required to resolve the assurance proposition.",
        },
        "producer": {"mode": "external"},
    },
    "controller-error": {
        "action_owner": {"surface": "rahp"},
        "artifact_to_produce": {
            "kind": "controller-repair",
            "description": "Repair the RAHP controller, contract, or transport defect and add a regression test.",
        },
        "producer": {"mode": "registered-executable", "id": "rahp-controller"},
    },
}


def _canonical_strings(values: list[str] | None) -> list[str]:
    return sorted({str(value).strip() for value in (values or []) if str(value).strip()})


def proposition_key(
    *,
    target_profile: str,
    subject_id: str,
    proposition_ids: list[str] | None = None,
    evidence_requirement_ids: list[str] | None = None,
    material_boundary: str = "",
) -> str:
    """Return stable semantic identity independent of issue/referral lineage.

    Immutable source revisions deliberately do not participate directly. A source change
    creates a new obligation only when the material boundary/proposition itself changes;
    otherwise it advances lineage and may move the obligation to evidence-stale.
    """
    payload = {
        "target_profile": target_profile.strip(),
        "subject_id": subject_id.strip(),
        "proposition_ids": _canonical_strings(proposition_ids),
        "evidence_requirement_ids": _canonical_strings(evidence_requirement_ids),
        "material_boundary": material_boundary.strip(),
    }
    if not payload["target_profile"] or not payload["subject_id"]:
        raise ValueError("target_profile and subject_id are required")
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()[:20]
    return f"rahp-obligation:{digest}"


def new_obligation(
    *,
    target_profile: str,
    subject_id: str,
    state: str,
    proposition_ids: list[str] | None = None,
    evidence_requirement_ids: list[str] | None = None,
    material_boundary: str = "",
    source_pins: list[dict[str, Any]] | None = None,
    lineage: list[dict[str, Any]] | None = None,
    action_owner: dict[str, Any] | None = None,
    artifact_to_produce: dict[str, Any] | None = None,
    producer: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if state not in STATE_DEFAULTS:
        raise ValueError(f"unsupported obligation state {state!r}")
    defaults = STATE_DEFAULTS[state]
    return {
        "schema": SCHEMA,
        "proposition_key": proposition_key(
            target_profile=target_profile,
            subject_id=subject_id,
            proposition_ids=proposition_ids,
            evidence_requirement_ids=evidence_requirement_ids,
            material_boundary=material_boundary,
        ),
        "state": state,
        "action_owner": deepcopy(action_owner or defaults["action_owner"]),
        "artifact_to_produce": deepcopy(artifact_to_produce or defaults["artifact_to_produce"]),
        "producer": deepcopy(producer or defaults["producer"]),
        "source_pins": deepcopy(source_pins or []),
        "evidence_requirement_ids": _canonical_strings(evidence_requirement_ids),
        "lineage": deepcopy(lineage or []),
        "supersedes": [],
    }


def self_test() -> int:
    first = proposition_key(
        target_profile="dtg",
        subject_id="relationship-correlation-privacy",
        proposition_ids=["P5", "P2", "P4"],
        material_boundary="relationship edge correlation",
    )
    replay = proposition_key(
        target_profile="dtg",
        subject_id="relationship-correlation-privacy",
        proposition_ids=["P4", "P2", "P5"],
        material_boundary="relationship edge correlation",
    )
    assert first == replay

    distinct = proposition_key(
        target_profile="dtg",
        subject_id="relationship-correlation-privacy",
        proposition_ids=["P2", "P4", "P5"],
        evidence_requirement_ids=["ER-RELATIONSHIP-AB"],
        material_boundary="relationship edge correlation",
    )
    assert distinct != first

    gap = new_obligation(
        target_profile="dtg",
        subject_id="credential-id-correlation",
        state="model-gap",
        proposition_ids=["CREDENTIAL-ID-CROSS-CONTEXT"],
    )
    assert gap["action_owner"]["surface"] == "specialist-profile"
    assert gap["artifact_to_produce"]["kind"] == "evidence-requirement"
    assert gap["producer"]["mode"] == "not-yet-defined"

    failed = new_obligation(
        target_profile="dtg",
        subject_id="device-metadata-privacy",
        state="remediation-required",
        evidence_requirement_ids=["ER-DEVICE-METADATA-AB"],
    )
    assert failed["action_owner"]["surface"] == "implementation"
    assert failed["artifact_to_produce"]["kind"] == "implementation-remediation"

    print("PASS semantic assurance obligation identity and ownership defaults")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    parser.error("no action selected")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
