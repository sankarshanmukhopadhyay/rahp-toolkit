"""Optional deterministic agent authority evaluator.

Evaluates a bounded action against one delegation-scope document. This module
does not authenticate identities, fetch revocation state, or grant permission.
Unknown external status remains INDETERMINATE.
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

SCHEMA = "rahp-agent-authority/v1"
VALID_STATUS = {"ACTIVE", "REVOKED", "SUSPENDED", "UNAVAILABLE"}


def _time(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timestamps must include timezone")
    return parsed.astimezone(timezone.utc)


def evaluate(case: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(case, dict) or case.get("schema") != SCHEMA:
        raise ValueError("unsupported agent authority schema")
    delegation = case.get("delegation")
    action = case.get("action")
    if not isinstance(delegation, dict) or not isinstance(action, dict):
        raise ValueError("delegation and action must be objects")
    for field in ("principal", "delegate"):
        if not isinstance(delegation.get(field), str) or not delegation[field]:
            raise ValueError(f"delegation.{field} must be nonempty")
    for field in ("capability", "resource", "evaluated_at"):
        if not isinstance(action.get(field), str) or not action[field]:
            raise ValueError(f"action.{field} must be nonempty")

    findings: list[dict[str, str]] = []
    def finding(control: str, status: str, reason: str) -> None:
        findings.append({"control": control, "status": status, "reason": reason})

    capabilities = delegation.get("capabilities")
    if not isinstance(capabilities, list) or not capabilities:
        raise ValueError("delegation.capabilities must be a nonempty array")
    finding("capability", "SATISFIED" if action["capability"] in capabilities else "NOT_SATISFIED",
            "requested capability is delegated" if action["capability"] in capabilities else "requested capability exceeds delegation")

    resources = delegation.get("resource_scope")
    if resources is None:
        finding("resource", "UNAVAILABLE", "delegation does not declare resource scope")
    elif not isinstance(resources, list):
        raise ValueError("delegation.resource_scope must be an array")
    else:
        finding("resource", "SATISFIED" if action["resource"] in resources else "NOT_SATISFIED",
                "resource is within delegated scope" if action["resource"] in resources else "resource exceeds delegated scope")

    validity = delegation.get("validity")
    if not isinstance(validity, dict):
        raise ValueError("delegation.validity must be an object")
    now = _time(action["evaluated_at"])
    start = _time(validity.get("valid_from", ""))
    end = _time(validity.get("valid_until", ""))
    finding("validity", "SATISFIED" if start <= now <= end else "NOT_SATISFIED",
            "delegation is current" if start <= now <= end else "delegation is not current")

    status = action.get("revocation_status")
    if status not in VALID_STATUS:
        raise ValueError("action.revocation_status must be ACTIVE, REVOKED, SUSPENDED, or UNAVAILABLE")
    if status == "ACTIVE":
        finding("revocation", "SATISFIED", "authoritative status is active")
    elif status == "UNAVAILABLE":
        finding("revocation", "UNAVAILABLE", "authoritative status is unavailable")
    else:
        finding("revocation", "NOT_SATISFIED", f"authoritative status is {status.lower()}")

    constraints = delegation.get("constraints") or {}
    if not isinstance(constraints, dict):
        raise ValueError("delegation.constraints must be an object")
    if constraints.get("human_confirmation_required") is True:
        confirmed = action.get("human_confirmed")
        if confirmed is True:
            finding("human-confirmation", "SATISFIED", "required human confirmation is evidenced")
        elif confirmed is False:
            finding("human-confirmation", "NOT_SATISFIED", "required human confirmation was denied or absent")
        else:
            finding("human-confirmation", "UNAVAILABLE", "required human confirmation evidence is unavailable")

    max_depth = constraints.get("max_delegation_depth")
    if max_depth is not None:
        depth = action.get("delegation_depth")
        if not isinstance(depth, int) or isinstance(depth, bool) or depth < 0:
            finding("delegation-depth", "UNAVAILABLE", "delegation depth evidence is unavailable")
        else:
            finding("delegation-depth", "SATISFIED" if depth <= max_depth else "NOT_SATISFIED",
                    "delegation depth is within bound" if depth <= max_depth else "delegation depth exceeds bound")

    statuses = {x["status"] for x in findings}
    if "UNAVAILABLE" in statuses:
        outcome, reason = "INDETERMINATE", "required-authority-evidence-unavailable"
    elif "NOT_SATISFIED" in statuses:
        outcome, reason = "FAIL", "agent-authority-constraint-not-satisfied"
    else:
        outcome, reason = "PASS", "all-agent-authority-constraints-satisfied"
    return {"schema": SCHEMA, "outcome": outcome, "reason_code": reason, "findings": findings,
            "authority_note": "Bounded assessment only; not a runtime permission grant."}
