#!/usr/bin/env python3
"""Finite RAHP assessment lifecycle controller."""
from __future__ import annotations
import argparse, json, uuid
from typing import Any

STATES = (
    "DISCOVERED", "QUALIFIED", "ROUTED", "ASSESSMENT_REQUIRED",
    "EVIDENCE_REQUIRED", "EVIDENCE_READY", "ASSESSED", "TERMINAL",
)
TERMINALS = {"PASS", "FAIL", "INDETERMINATE", "NOT_APPLICABLE", "UNMAPPED"}
RESILIENCE_DISPOSITIONS = {
    "executed",
    "not-applicable",
    "required-but-not-executed",
}
ALLOWED = {
    "DISCOVERED": {"QUALIFIED", "TERMINAL"},
    "QUALIFIED": {"ROUTED", "TERMINAL"},
    "ROUTED": {"ASSESSMENT_REQUIRED", "TERMINAL"},
    "ASSESSMENT_REQUIRED": {"EVIDENCE_REQUIRED", "EVIDENCE_READY", "ASSESSED", "TERMINAL"},
    "EVIDENCE_REQUIRED": {"EVIDENCE_READY", "TERMINAL"},
    "EVIDENCE_READY": {"ASSESSED", "TERMINAL"},
    "ASSESSED": {"TERMINAL"},
    "TERMINAL": set(),
}


def _resilience_record(
    disposition: str,
    reason: str,
    provenance: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if disposition not in RESILIENCE_DISPOSITIONS:
        raise ValueError(f"invalid resilience disposition: {disposition}")
    if not isinstance(reason, str) or not reason.strip():
        raise ValueError("resilience disposition requires a non-empty reason")
    if provenance is not None and not isinstance(provenance, dict):
        raise ValueError("resilience provenance must be an object")
    if disposition == "not-applicable" and not provenance:
        raise ValueError("not-applicable resilience disposition requires provenance")
    return {
        "disposition": disposition,
        "reason": reason.strip(),
        **({"provenance": provenance} if provenance else {}),
    }


def resilience_disposition(record: dict[str, Any]) -> dict[str, Any]:
    """Return a validated, fail-closed resilience disposition.

    Historical v1 lifecycle records did not carry a capability manifest. They remain
    readable, but absence is interpreted as unresolved rather than as a resilience
    PASS. This compatibility rule is intentionally stricter than the legacy record.
    """
    capabilities = record.get("capabilities")
    if capabilities is None:
        return _resilience_record(
            "required-but-not-executed",
            "legacy assessment has no recorded resilience disposition",
            {"source": "compatibility-default", "decision": "fail-closed"},
        )
    if not isinstance(capabilities, dict):
        raise ValueError("assessment capabilities must be an object")
    value = capabilities.get("resilience")
    if value is None:
        return _resilience_record(
            "required-but-not-executed",
            "assessment has no recorded resilience disposition",
            {"source": "compatibility-default", "decision": "fail-closed"},
        )
    if not isinstance(value, dict):
        raise ValueError("resilience capability record must be an object")
    return _resilience_record(
        str(value.get("disposition", "")),
        value.get("reason"),
        value.get("provenance"),
    )


def set_resilience_disposition(
    record: dict[str, Any],
    disposition: str,
    reason: str,
    provenance: dict[str, Any] | None = None,
) -> dict[str, Any]:
    value = _resilience_record(disposition, reason, provenance)
    capabilities = record.setdefault("capabilities", {})
    if not isinstance(capabilities, dict):
        raise ValueError("assessment capabilities must be an object")
    capabilities["resilience"] = value
    return record


def new_lifecycle(assessment_id: str, mode: str = "steady-state", lineage: dict[str, Any] | None = None) -> dict[str, Any]:
    if mode not in {"steady-state", "clean-room"}:
        raise ValueError("mode must be steady-state or clean-room")
    return {
        "schema": "rahp-assessment-lifecycle/v1",
        "assessment_id": assessment_id,
        "mode": mode,
        "state": "DISCOVERED",
        **({"lineage": lineage} if lineage else {}),
        "capabilities": {
            "resilience": _resilience_record(
                "required-but-not-executed",
                "resilience applicability has not yet been resolved",
                {"source": "controller-default", "decision": "fail-closed"},
            )
        },
        "history": [{"from": None, "to": "DISCOVERED", "reason": "assessment discovered"}],
        "blocking_reason": None,
    }


def transition(record: dict[str, Any], to_state: str, reason: str, *, blocking_reason: dict[str, Any] | None = None, terminal_outcome: str | None = None) -> dict[str, Any]:
    current = str(record.get("state"))
    if to_state not in ALLOWED.get(current, set()):
        raise ValueError(f"illegal transition {current} -> {to_state}")
    if to_state == "TERMINAL":
        if terminal_outcome not in TERMINALS:
            raise ValueError("terminal transition requires PASS/FAIL/INDETERMINATE/NOT_APPLICABLE/UNMAPPED")
        record["terminal_outcome"] = terminal_outcome
    elif terminal_outcome is not None:
        raise ValueError("terminal_outcome only valid for TERMINAL")
    record["state"] = to_state
    record["blocking_reason"] = blocking_reason
    record.setdefault("history", []).append({"from": current, "to": to_state, "reason": reason})
    return record


def apply_assessor_result(record: dict[str, Any], assessor_result: dict[str, Any]) -> dict[str, Any]:
    outcome = assessor_result.get("outcome")
    if outcome not in {"PASS", "FAIL", "INDETERMINATE", "NOT_APPLICABLE"}:
        raise ValueError("invalid assessor result outcome")
    if record.get("state") == "EVIDENCE_READY":
        transition(record, "ASSESSED", "specialist assessor evaluated evidence")
    elif record.get("state") != "ASSESSED":
        raise ValueError(f"assessor result cannot be applied from {record.get('state')}")
    return transition(record, "TERMINAL", f"specialist assessor returned {outcome}", terminal_outcome=outcome)


def plugin_error(record: dict[str, Any], code: str, message: str) -> dict[str, Any]:
    return transition(
        record,
        "TERMINAL",
        "specialist assessor execution failed",
        terminal_outcome="INDETERMINATE",
        blocking_reason={"code": code, "message": message},
    )


def clean_room_lineage(instance: str, snapshot: str, nonce: str | None = None) -> dict[str, Any]:
    token = nonce or uuid.uuid4().hex
    return {
        "schema": "rahp-clean-room-lineage/v1",
        "instance": instance,
        "snapshot": snapshot,
        "run_id": token,
        "isolation": {
            "historical_state_allowed": False,
            "historical_evidence_allowed": False,
            "coalescing_allowed": False,
            "fresh_assessor_lineage_required": True,
        },
    }


def may_coalesce(existing: dict[str, Any], incoming: dict[str, Any]) -> bool:
    if incoming.get("mode") == "clean-room" or existing.get("mode") == "clean-room":
        return False
    return existing.get("assessment_id") == incoming.get("assessment_id") and existing.get("state") != "TERMINAL"


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("clean-room-lineage")
    p.add_argument("--instance", required=True)
    p.add_argument("--snapshot", required=True)
    p.add_argument("--nonce")
    p = sub.add_parser("new")
    p.add_argument("--assessment-id", required=True)
    p.add_argument("--mode", choices=["steady-state", "clean-room"], default="steady-state")
    args = ap.parse_args()
    if args.cmd == "clean-room-lineage":
        print(json.dumps(clean_room_lineage(args.instance, args.snapshot, args.nonce), indent=2))
    else:
        print(json.dumps(new_lifecycle(args.assessment_id, args.mode), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
