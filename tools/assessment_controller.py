#!/usr/bin/env python3
"""Finite RAHP assessment lifecycle controller."""
from __future__ import annotations
import argparse, json, uuid
from pathlib import Path
from typing import Any

try:
    from .execution_telemetry import build_event, lifecycle_metrics, write_event
except ImportError:
    try:
        from tools.execution_telemetry import build_event, lifecycle_metrics, write_event
    except ImportError:  # direct script execution from tools/
        from execution_telemetry import build_event, lifecycle_metrics, write_event

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
FULL_STACK_LENSES = ("rahp", "security", "composition", "drarm", "specialist")
LENS_MATERIALITY = {"applicable", "not-applicable", "not-material", "uncertain"}
LENS_EXECUTION = {"executed", "required-but-not-executed", "referred", "no-applicable-producer"}
LENS_RESULTS = {"PASS", "FAIL", "INDETERMINATE", "KNOWN_RESIDUAL", "N/A", "PENDING"}
EVIDENCE_MATURITY = {
    "none", "modeled", "source-only", "implementation", "automated-conformance",
    "runtime", "induced-failure", "fleet-adversarial",
}
PROCESS_STATES = {"in-progress", "complete", "error"}
ASSURANCE_STATES = {"pending", "pass", "fail", "indeterminate", "not-applicable", "upstream-action", "error"}
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
    """Return a validated, fail-closed resilience disposition."""
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


def resilience_applicability(
    target_class: str,
    policy: dict[str, Any] | None = None,
) -> dict[str, str]:
    """Resolve resilience applicability from explicit target class and profile policy.

    The decision deliberately avoids source-text keyword inference. Ambiguity fails
    closed as unresolved, leaving the capability required-but-not-executed.
    """
    if not isinstance(target_class, str) or not target_class.strip():
        raise ValueError("target_class must be a non-empty string")
    target_class = target_class.strip()
    policy = policy or {}
    required = set(policy.get("required_for") or [])
    not_applicable = set(policy.get("not_applicable_for") or [])
    overlap = required & not_applicable
    if overlap:
        raise ValueError("resilience applicability policy conflicts for: " + ", ".join(sorted(overlap)))
    if target_class in required:
        return {"decision": "required", "target_class": target_class}
    if target_class in not_applicable:
        return {"decision": "not-applicable", "target_class": target_class}
    return {"decision": "unresolved", "target_class": target_class}


def apply_resilience_applicability(
    record: dict[str, Any],
    target_class: str,
    policy: dict[str, Any] | None = None,
    *,
    policy_source: str = "profile-policy",
) -> dict[str, Any]:
    decision = resilience_applicability(target_class, policy)
    provenance = {
        "source": policy_source,
        "target_class": decision["target_class"],
        "decision": decision["decision"],
    }
    if decision["decision"] == "not-applicable":
        return set_resilience_disposition(
            record,
            "not-applicable",
            f"resilience policy marks target class {target_class!r} not applicable",
            provenance,
        )
    if decision["decision"] == "required":
        return set_resilience_disposition(
            record,
            "required-but-not-executed",
            f"resilience assessment required for target class {target_class!r}",
            provenance,
        )
    return set_resilience_disposition(
        record,
        "required-but-not-executed",
        f"resilience applicability unresolved for target class {target_class!r}",
        provenance,
    )


def _default_lens_record(lens: str) -> dict[str, Any]:
    return {
        "materiality": "uncertain",
        "execution": "required-but-not-executed",
        "result": "PENDING",
        "evidence_maturity": "none",
        "reason": f"{lens} applicability has not yet been resolved",
        "provenance": {"source": "controller-default", "decision": "fail-closed"},
    }


def set_run_dimensions(
    record: dict[str, Any],
    *,
    process_state: str | None = None,
    assurance_state: str | None = None,
    evidence_maturity: str | None = None,
) -> dict[str, Any]:
    if process_state is not None:
        if process_state not in PROCESS_STATES:
            raise ValueError(f"invalid process_state: {process_state}")
        record["process_state"] = process_state
    if assurance_state is not None:
        if assurance_state not in ASSURANCE_STATES:
            raise ValueError(f"invalid assurance_state: {assurance_state}")
        record["assurance_state"] = assurance_state
    if evidence_maturity is not None:
        if evidence_maturity not in EVIDENCE_MATURITY:
            raise ValueError(f"invalid evidence_maturity: {evidence_maturity}")
        record["evidence_maturity"] = evidence_maturity
    return record


def set_lens_disposition(
    record: dict[str, Any],
    lens: str,
    *,
    materiality: str,
    execution: str,
    result: str,
    evidence_maturity: str,
    reason: str,
    provenance: dict[str, Any] | None = None,
    owner: str | None = None,
    assurance_depth: dict[str, str] | None = None,
) -> dict[str, Any]:
    if lens not in FULL_STACK_LENSES:
        raise ValueError(f"unknown full-stack lens: {lens}")
    if materiality not in LENS_MATERIALITY:
        raise ValueError(f"invalid lens materiality: {materiality}")
    if execution not in LENS_EXECUTION:
        raise ValueError(f"invalid lens execution: {execution}")
    if result not in LENS_RESULTS:
        raise ValueError(f"invalid lens result: {result}")
    if evidence_maturity not in EVIDENCE_MATURITY:
        raise ValueError(f"invalid lens evidence maturity: {evidence_maturity}")
    if not isinstance(reason, str) or not reason.strip():
        raise ValueError("lens disposition requires a non-empty reason")
    if materiality in {"not-applicable", "not-material"} and not provenance:
        raise ValueError("not-applicable/not-material lens disposition requires provenance")
    if execution == "executed" and not provenance:
        raise ValueError("executed lens disposition requires provenance")
    if result in {"PASS", "FAIL", "KNOWN_RESIDUAL"} and execution != "executed":
        raise ValueError(f"{result} requires an executed lens")
    if result == "N/A" and materiality not in {"not-applicable", "not-material"}:
        raise ValueError("N/A requires not-applicable or not-material lens")
    if assurance_depth is not None:
        if not isinstance(assurance_depth, dict) or not assurance_depth.get("achieved") or not assurance_depth.get("required"):
            raise ValueError("assurance_depth requires achieved and required")
    value = {
        "materiality": materiality,
        "execution": execution,
        "result": result,
        "evidence_maturity": evidence_maturity,
        "reason": reason.strip(),
        **({"provenance": provenance} if provenance else {}),
        **({"owner": owner} if owner else {}),
        **({"assurance_depth": assurance_depth} if assurance_depth else {}),
    }
    record.setdefault("lenses", {})[lens] = value
    return record


def full_stack_terminalization_errors(record: dict[str, Any]) -> list[str]:
    """Return fail-closed errors for a full-stack/composite terminal claim."""
    errors: list[str] = []
    if record.get("process_state") != "complete":
        errors.append("process_state must be complete")
    if record.get("assurance_state") not in ASSURANCE_STATES - {"pending"}:
        errors.append("assurance_state must be terminal and separate from process completion")
    if record.get("evidence_maturity") not in EVIDENCE_MATURITY - {"none"}:
        errors.append("evidence_maturity must state the achieved evidence depth")
    lenses = record.get("lenses")
    if not isinstance(lenses, dict):
        return errors + ["full-stack lens ledger missing"]
    for lens in FULL_STACK_LENSES:
        value = lenses.get(lens)
        if not isinstance(value, dict):
            errors.append(f"{lens}: lens disposition missing")
            continue
        materiality = value.get("materiality")
        execution = value.get("execution")
        result = value.get("result")
        if materiality == "uncertain":
            errors.append(f"{lens}: materiality remains uncertain")
        if materiality in {"not-applicable", "not-material"} and not value.get("provenance"):
            errors.append(f"{lens}: explicit non-applicability requires provenance")
        if result == "PENDING":
            errors.append(f"{lens}: result remains pending")
        if materiality == "applicable" and execution == "required-but-not-executed" and result != "INDETERMINATE":
            errors.append(f"{lens}: unexecuted applicable lens must remain INDETERMINATE")
        if result == "PASS" and execution != "executed":
            errors.append(f"{lens}: PASS requires attributable execution")
    if record.get("assurance_state") == "pass":
        for lens, value in lenses.items():
            if value.get("materiality") == "applicable" and value.get("result") != "PASS":
                errors.append(f"{lens}: full-stack PASS prohibited without lens PASS")
    return errors


def assert_full_stack_terminalizable(record: dict[str, Any]) -> None:
    errors = full_stack_terminalization_errors(record)
    if errors:
        raise ValueError("full-stack terminalization blocked: " + "; ".join(errors))


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
        "process_state": "in-progress",
        "assurance_state": "pending",
        "evidence_maturity": "none",
        "lenses": {lens: _default_lens_record(lens) for lens in FULL_STACK_LENSES},
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


def lifecycle_telemetry(record: dict[str, Any], duration_seconds: float = 0.0) -> dict[str, Any]:
    """Build an operational sidecar without mutating lifecycle state."""
    assessment_id = str(record.get("assessment_id") or "")
    if not assessment_id:
        raise ValueError("lifecycle telemetry requires assessment_id")
    return build_event(
        operation="assessment-lifecycle",
        run_id=assessment_id,
        duration_seconds=duration_seconds,
        context={"mode": str(record.get("mode") or "")},
        metrics=lifecycle_metrics(record),
    )


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
    p = sub.add_parser("telemetry")
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path)
    p.add_argument("--duration-seconds", type=float, default=0.0)
    args = ap.parse_args()
    if args.cmd == "clean-room-lineage":
        print(json.dumps(clean_room_lineage(args.instance, args.snapshot, args.nonce), indent=2))
    elif args.cmd == "telemetry":
        record = json.loads(args.input.read_text(encoding="utf-8"))
        event = lifecycle_telemetry(record, args.duration_seconds)
        if args.output:
            write_event(args.output, event)
        else:
            print(json.dumps(event, indent=2, sort_keys=True))
    else:
        print(json.dumps(new_lifecycle(args.assessment_id, args.mode), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
