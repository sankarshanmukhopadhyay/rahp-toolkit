#!/usr/bin/env python3
"""Canonical finite-state machine for RAHP assurance runs.

Workflows are transports. This module owns legal assurance-controller transitions.
It intentionally models non-PASS outcomes and controller faults as first-class states
so no human action is needed merely to advance the machinery.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from copy import deepcopy
from typing import Any

SCHEMA = "rahp-assurance-run-state/v1"

TERMINAL_STATES = {
    "TERMINAL_PASS": ("PASS", "assurance-satisfied"),
    "TERMINAL_FAIL": ("FAIL", "assurance-failed"),
    "TERMINAL_NOT_APPLICABLE": ("NOT_APPLICABLE", "not-applicable"),
    "TERMINAL_INDETERMINATE_EVIDENCE_REQUIRED": ("INDETERMINATE", "evidence-required"),
    "TERMINAL_INDETERMINATE_MODEL_GAP": ("INDETERMINATE", "model-gap"),
    "TERMINAL_UPSTREAM_ACTION": ("UPSTREAM_ACTION", "upstream-action"),
    "ERROR_CONTRACT_INCOMPATIBLE": ("ERROR", "contract-incompatible"),
    "ERROR_CONTROLLER": ("ERROR", "controller-error"),
}

RETRYABLE_STATES = {"ERROR_TRANSPORT_RETRYABLE"}

ALLOWED = {
    None: {"OBSERVED"},
    "OBSERVED": {"GATHERED", "ERROR_TRANSPORT_RETRYABLE", "ERROR_CONTROLLER"},
    "GATHERED": {"MATERIALITY_COMPLETE", "ERROR_CONTRACT_INCOMPATIBLE", "ERROR_CONTROLLER"},
    "MATERIALITY_COMPLETE": {
        "ASSESSMENT_COMPLETE",
        "TERMINAL_NOT_APPLICABLE",
        "ERROR_CONTRACT_INCOMPATIBLE",
        "ERROR_CONTROLLER",
    },
    "ASSESSMENT_COMPLETE": {
        "SPECIALIST_REQUIRED",
        "RECONCILED",
        "TERMINAL_PASS",
        "TERMINAL_FAIL",
        "TERMINAL_INDETERMINATE_EVIDENCE_REQUIRED",
        "TERMINAL_INDETERMINATE_MODEL_GAP",
        "TERMINAL_UPSTREAM_ACTION",
        "ERROR_CONTROLLER",
    },
    "SPECIALIST_REQUIRED": {"SPECIALIST_IN_PROGRESS", "ERROR_TRANSPORT_RETRYABLE", "ERROR_CONTROLLER"},
    "SPECIALIST_IN_PROGRESS": {
        "SPECIALIST_RETURN_READY",
        "TERMINAL_INDETERMINATE_MODEL_GAP",
        "ERROR_CONTRACT_INCOMPATIBLE",
        "ERROR_CONTROLLER",
    },
    "SPECIALIST_RETURN_READY": {"SPECIALIST_RETURNED", "ERROR_TRANSPORT_RETRYABLE", "ERROR_CONTRACT_INCOMPATIBLE"},
    "SPECIALIST_RETURNED": {"RECONCILED", "ERROR_CONTRACT_INCOMPATIBLE", "ERROR_CONTROLLER"},
    "RECONCILED": set(TERMINAL_STATES),
    "ERROR_TRANSPORT_RETRYABLE": {
        "OBSERVED",
        "SPECIALIST_REQUIRED",
        "SPECIALIST_RETURN_READY",
        "SPECIALIST_RETURNED",
        "ERROR_CONTROLLER",
    },
}
for state in TERMINAL_STATES:
    ALLOWED[state] = set()


def stable_assessment_id(subject: dict[str, Any], source_pins: list[dict[str, Any]]) -> str:
    payload = {"subject": subject, "source_pins": source_pins}
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()[:20]
    return f"rahp:{digest}"


def new_run(subject: dict[str, Any], source_pins: list[dict[str, Any]], correlation_key: str | None = None) -> dict[str, Any]:
    if not isinstance(subject, dict) or not subject.get("type") or not subject.get("id"):
        raise ValueError("subject.type and subject.id are required")
    if not source_pins:
        raise ValueError("at least one immutable source pin is required")
    assessment_id = stable_assessment_id(subject, source_pins)
    return {
        "schema": SCHEMA,
        "assessment_id": assessment_id,
        "correlation_key": correlation_key or assessment_id,
        "subject": deepcopy(subject),
        "source_pins": deepcopy(source_pins),
        "state": None,
        "terminal": False,
        "history": [],
        "evidence": [],
        "residuals": [],
        "actions": [],
    }


def transition(run: dict[str, Any], to_state: str, reason: str, event_id: str | None = None, **updates: Any) -> dict[str, Any]:
    current = run.get("state")
    if run.get("terminal"):
        if current == to_state:
            return run
        raise ValueError(f"terminal run cannot transition from {current} to {to_state}")
    if to_state not in ALLOWED.get(current, set()):
        raise ValueError(f"illegal assurance transition {current!r} -> {to_state!r}")

    # Idempotency: the same event may be replayed but may not mutate history twice.
    if event_id and any(item.get("event_id") == event_id for item in run.get("history", [])):
        return run

    run["history"].append({"from": current, "to": to_state, "reason": reason, **({"event_id": event_id} if event_id else {})})
    run["state"] = to_state
    for key, value in updates.items():
        run[key] = deepcopy(value)

    if to_state in TERMINAL_STATES:
        outcome, default_reason = TERMINAL_STATES[to_state]
        run["terminal"] = True
        run["outcome"] = updates.get("outcome", outcome)
        run["reason_code"] = updates.get("reason_code", default_reason)
    else:
        run["terminal"] = False
    return run


def terminal_from_specialist(conclusion: str, reason_code: str | None = None) -> str:
    value = (conclusion or "").upper()
    reason = (reason_code or "").lower()
    if value == "PASS":
        return "TERMINAL_PASS"
    if value == "FAIL":
        return "TERMINAL_FAIL"
    if value == "NOT_APPLICABLE":
        return "TERMINAL_NOT_APPLICABLE"
    if value == "INDETERMINATE":
        return "TERMINAL_INDETERMINATE_MODEL_GAP" if reason == "model-gap" else "TERMINAL_INDETERMINATE_EVIDENCE_REQUIRED"
    raise ValueError(f"unsupported specialist conclusion {conclusion!r}")


def stranded(run: dict[str, Any]) -> bool:
    return not run.get("terminal") and run.get("state") not in RETRYABLE_STATES


def self_test() -> int:
    subject = {"type": "cross-specification", "id": "cred-spec×zkp", "components": ["cred-spec", "zkp"]}
    pins = [{"repository": "example/specs", "revision": "a" * 40}]
    first = new_run(subject, pins)
    second = new_run(subject, pins)
    assert first["assessment_id"] == second["assessment_id"]

    transition(first, "OBSERVED", "fresh source observation", "evt-1")
    transition(first, "OBSERVED", "fresh source observation", "evt-1")
    assert len(first["history"]) == 1
    transition(first, "GATHERED", "subject/evidence gathered")
    transition(first, "MATERIALITY_COMPLETE", "privacy proposition material")
    transition(first, "ASSESSMENT_COMPLETE", "bounded RAHP assessment complete")
    transition(first, "SPECIALIST_REQUIRED", "privacy specialist required")
    transition(first, "SPECIALIST_IN_PROGRESS", "DPIP admitted")
    transition(first, "SPECIALIST_RETURN_READY", "portable assessor result constructed")
    transition(first, "SPECIALIST_RETURNED", "durable outbox delivered")
    transition(first, "RECONCILED", "RAHP reconciled specialist result")
    final = terminal_from_specialist("INDETERMINATE", "model-gap")
    transition(first, final, "unmapped evidence proposition routed to model gap")
    assert first["terminal"] and first["outcome"] == "INDETERMINATE" and first["reason_code"] == "model-gap"
    assert not stranded(first)

    retry = new_run({"type": "implementation", "id": "example/runtime"}, pins)
    transition(retry, "OBSERVED", "observed")
    transition(retry, "ERROR_TRANSPORT_RETRYABLE", "specialist transport unavailable")
    assert not retry["terminal"] and not stranded(retry)
    transition(retry, "OBSERVED", "automatic retry")

    invalid = new_run({"type": "specification", "id": "example/spec"}, pins)
    try:
        transition(invalid, "TERMINAL_PASS", "cannot skip assessment")
        raise AssertionError("illegal transition was accepted")
    except ValueError:
        pass

    print("PASS assurance_fsm self-test")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    parser.error("only --self-test is currently exposed; workflows import this module for transitions")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
