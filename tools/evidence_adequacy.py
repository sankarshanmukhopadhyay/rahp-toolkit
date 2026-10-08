"""Optional deterministic evidence adequacy profile; not an authority or terminal assurance engine.

All declared requirements are mandatory. Each requirement must have exactly one
in-scope observation. Unavailable, conflicting, or out-of-scope evidence blocks PASS.
This module does not validate the authenticity or truth of source evidence.
"""
from __future__ import annotations

from typing import Any

SCHEMA = "rahp-evidence-adequacy/v1"
STATES = {"SATISFIED", "NOT_SATISFIED", "UNAVAILABLE"}


def evaluate(profile: dict[str, Any]) -> dict[str, Any]:
    """Return a stable, inspectable bounded disposition; raise ValueError on bad contracts.

    Input:
      schema: rahp-evidence-adequacy/v1
      proposition_id: nonempty string
      scope: nonempty string (caller-defined, not independently authenticated)
      required_evidence: unique, nonempty string identifiers
      observations: {id, evidence_id, scope, state} records

    Scope must exactly equal the declared profile scope. Multiple observations for
    one required ID are conservatively conflicting, even when their states agree:
    deduplication and supersession require an explicit upstream decision.
    """
    if not isinstance(profile, dict) or profile.get("schema") != SCHEMA:
        raise ValueError("unsupported evidence adequacy schema")
    for field in ("proposition_id", "scope"):
        if not isinstance(profile.get(field), str) or not profile[field].strip():
            raise ValueError(f"{field} must be a nonempty string")
    required = profile.get("required_evidence")
    if not isinstance(required, list) or not required or any(
        not isinstance(x, str) or not x.strip() for x in required
    ) or len(required) != len(set(required)):
        raise ValueError("required_evidence must contain unique nonempty IDs")
    observations = profile.get("observations")
    if not isinstance(observations, list):
        raise ValueError("observations must be an array")
    seen_ids: set[str] = set()
    grouped: dict[str, list[dict[str, str]]] = {key: [] for key in required}
    for obs in observations:
        if not isinstance(obs, dict):
            raise ValueError("observation must be an object")
        oid, eid, scope, state = (obs.get(k) for k in ("id", "evidence_id", "scope", "state"))
        if not isinstance(oid, str) or not oid.strip() or oid in seen_ids:
            raise ValueError("observation IDs must be unique nonempty strings")
        seen_ids.add(oid)
        if not isinstance(eid, str) or eid not in grouped:
            raise ValueError("observation references undeclared evidence")
        if not isinstance(scope, str) or not scope.strip():
            raise ValueError("observation scope must be a nonempty string")
        if state not in STATES:
            raise ValueError("unsupported observation state")
        grouped[eid].append({"id": oid, "scope": scope, "state": state})

    findings: list[dict[str, Any]] = []
    for eid in sorted(required):
        items = sorted(grouped[eid], key=lambda item: item["id"])
        if not items:
            status = "MISSING"
        elif len(items) > 1:
            status = "CONFLICT"
        elif items[0]["scope"] != profile["scope"]:
            status = "OUT_OF_SCOPE"
        else:
            status = items[0]["state"]
        findings.append({
            "evidence_id": eid,
            "status": status,
            "observation_ids": [item["id"] for item in items],
        })

    statuses = {f["status"] for f in findings}
    if statuses == {"SATISFIED"}:
        outcome, reason = "PASS", "all-required-evidence-satisfied"
    elif statuses & {"MISSING", "UNAVAILABLE", "CONFLICT", "OUT_OF_SCOPE"}:
        outcome, reason = "INDETERMINATE", "evidence-adequacy-unresolved"
    else:
        outcome, reason = "FAIL", "required-evidence-not-satisfied"
    return {
        "schema": SCHEMA,
        "proposition_id": profile["proposition_id"],
        "scope": profile["scope"],
        "outcome": outcome,
        "reason_code": reason,
        "findings": findings,
        "authority_note": "Bounded structural evaluation only; not terminal RAHP assurance.",
    }
