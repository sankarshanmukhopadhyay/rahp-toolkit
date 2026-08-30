#!/usr/bin/env python3
"""Finite RAHP assessment lifecycle controller."""
from __future__ import annotations
import argparse, json, pathlib, uuid
from typing import Any

STATES = (
    "DISCOVERED", "QUALIFIED", "ROUTED", "ASSESSMENT_REQUIRED",
    "EVIDENCE_REQUIRED", "EVIDENCE_READY", "ASSESSED", "TERMINAL",
)
TERMINALS = {"PASS", "FAIL", "INDETERMINATE", "NOT_APPLICABLE", "UNMAPPED"}
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


def new_lifecycle(assessment_id: str, mode: str = "steady-state", lineage: dict[str, Any] | None = None) -> dict[str, Any]:
    if mode not in {"steady-state", "clean-room"}:
        raise ValueError("mode must be steady-state or clean-room")
    return {
        "schema": "rahp-assessment-lifecycle/v1",
        "assessment_id": assessment_id,
        "mode": mode,
        "state": "DISCOVERED",
        **({"lineage": lineage} if lineage else {}),
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
