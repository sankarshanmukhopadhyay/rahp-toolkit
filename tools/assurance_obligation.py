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


def _digest(payload: dict[str, Any], prefix: str) -> str:
    value = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()[:20]
    return f"{prefix}:{value}"


def proposition_key(
    *,
    target_profile: str,
    subject_id: str,
    proposition_ids: list[str] | None = None,
    evidence_requirement_ids: list[str] | None = None,
    material_boundary: str = "",
) -> str:
    """Return durable semantic identity for the assurance proposition.

    Evidence requirement IDs and source revisions deliberately do not participate in
    durable identity. They refine how the same proposition is tested and may change as
    a model gap is repaired or evidence becomes stale. Including them here would create
    a second active obligation merely because the evidence contract became more precise.

    ``evidence_requirement_ids`` remains in the signature for source compatibility with
    callers that already pass it; use :func:`evidence_contract_key` when evidence-contract
    identity is needed.
    """
    payload = {
        "target_profile": target_profile.strip(),
        "subject_id": subject_id.strip(),
        "proposition_ids": _canonical_strings(proposition_ids),
        "material_boundary": material_boundary.strip(),
    }
    if not payload["target_profile"] or not payload["subject_id"]:
        raise ValueError("target_profile and subject_id are required")
    return _digest(payload, "rahp-obligation")


def evidence_contract_key(proposition: str, evidence_requirement_ids: list[str] | None = None) -> str:
    if not proposition.strip():
        raise ValueError("proposition key is required")
    return _digest({
        "proposition_key": proposition.strip(),
        "evidence_requirement_ids": _canonical_strings(evidence_requirement_ids),
    }, "rahp-evidence-contract")


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
    key = proposition_key(
        target_profile=target_profile,
        subject_id=subject_id,
        proposition_ids=proposition_ids,
        material_boundary=material_boundary,
    )
    requirement_ids = _canonical_strings(evidence_requirement_ids)
    return {
        "schema": SCHEMA,
        "proposition_key": key,
        "evidence_contract_key": evidence_contract_key(key, requirement_ids),
        "state": state,
        "action_owner": deepcopy(action_owner or defaults["action_owner"]),
        "artifact_to_produce": deepcopy(artifact_to_produce or defaults["artifact_to_produce"]),
        "producer": deepcopy(producer or defaults["producer"]),
        "source_pins": deepcopy(source_pins or []),
        "evidence_requirement_ids": requirement_ids,
        "lineage": deepcopy(lineage or []),
        "supersedes": [],
    }


def transition_obligation(existing: dict[str, Any], *, state: str, evidence_requirement_ids: list[str] | None = None,
                          source_pins: list[dict[str, Any]] | None = None, lineage: dict[str, Any] | None = None,
                          action_owner: dict[str, Any] | None = None, artifact_to_produce: dict[str, Any] | None = None,
                          producer: dict[str, Any] | None = None) -> dict[str, Any]:
    """Advance an active obligation without changing its durable proposition identity."""
    if state not in STATE_DEFAULTS:
        raise ValueError(f"unsupported obligation state {state!r}")
    out = deepcopy(existing)
    out["schema"] = SCHEMA
    out["state"] = state
    ids = _canonical_strings(evidence_requirement_ids if evidence_requirement_ids is not None else out.get("evidence_requirement_ids"))
    out["evidence_requirement_ids"] = ids
    out["evidence_contract_key"] = evidence_contract_key(str(out["proposition_key"]), ids)
    if source_pins is not None:
        out["source_pins"] = deepcopy(source_pins)
    defaults = STATE_DEFAULTS[state]
    out["action_owner"] = deepcopy(action_owner or defaults["action_owner"])
    out["artifact_to_produce"] = deepcopy(artifact_to_produce or defaults["artifact_to_produce"])
    out["producer"] = deepcopy(producer or defaults["producer"])
    history = out.setdefault("lineage", [])
    if lineage is not None and lineage not in history:
        history.append(deepcopy(lineage))
    out.setdefault("supersedes", [])
    return out


def self_test() -> int:
    first = proposition_key(target_profile="dtg", subject_id="relationship-correlation-privacy", proposition_ids=["P5", "P2", "P4"], material_boundary="relationship edge correlation")
    replay = proposition_key(target_profile="dtg", subject_id="relationship-correlation-privacy", proposition_ids=["P4", "P2", "P5"], material_boundary="relationship edge correlation")
    assert first == replay
    refined = proposition_key(target_profile="dtg", subject_id="relationship-correlation-privacy", proposition_ids=["P2", "P4", "P5"], evidence_requirement_ids=["ER-REL-DID-AB"], material_boundary="relationship edge correlation")
    assert refined == first, "evidence-contract refinement must not create a new active obligation"
    changed_boundary = proposition_key(target_profile="dtg", subject_id="relationship-correlation-privacy", proposition_ids=["P2", "P4", "P5"], material_boundary="different material boundary")
    assert changed_boundary != first

    gap = new_obligation(target_profile="dtg", subject_id="credential-id-correlation", state="model-gap", proposition_ids=["CREDENTIAL-ID-CROSS-CONTEXT"])
    acquired = transition_obligation(gap, state="evidence-acquirable", evidence_requirement_ids=["ER-CREDENTIAL-ID-AB"], producer={"mode": "registered-executable", "id": "composed-unlinkability-v1"})
    assert acquired["proposition_key"] == gap["proposition_key"]
    assert acquired["evidence_contract_key"] != gap["evidence_contract_key"]
    assert acquired["action_owner"]["surface"] == "evidence-producer"

    failed = transition_obligation(acquired, state="remediation-required")
    assert failed["proposition_key"] == gap["proposition_key"]
    assert failed["artifact_to_produce"]["kind"] == "implementation-remediation"

    print("PASS semantic obligation identity survives model, evidence and remediation transitions")
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
