"""Optional R2 temporal/provenance applicability profile.

This module evaluates declared time and source-pin metadata, not the truth,
authority, revocation status, or substantive correctness of evidence.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

SCHEMA = "rahp-temporal-provenance/v1"


def _instant(value: Any, label: str) -> datetime:
    if not isinstance(value, str) or not value or ("T" not in value):
        raise ValueError(f"{label} must be an offset-aware ISO-8601 timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{label} must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(f"{label} must have an explicit UTC offset")
    return parsed.astimezone(timezone.utc)


def evaluate_temporal(profile: dict[str, Any]) -> dict[str, Any]:
    """Evaluate declared applicability at target_time as known by knowledge_cutoff.

    Multiple known records for the same evidence ID are unresolved, even when
    apparently consistent. A future-discovered record is disclosed but cannot
    affect the as-known-at determination. No internal persistence is assumed.
    """
    if not isinstance(profile, dict) or profile.get("schema") != SCHEMA:
        raise ValueError("unsupported temporal provenance schema")
    if not isinstance(profile.get("proposition_id"), str) or not profile["proposition_id"].strip():
        raise ValueError("proposition_id required")
    target = _instant(profile.get("target_time"), "target_time")
    cutoff = _instant(profile.get("knowledge_cutoff"), "knowledge_cutoff")
    evaluated = _instant(profile.get("evaluated_at"), "evaluated_at")
    if cutoff > evaluated:
        raise ValueError("knowledge_cutoff cannot exceed evaluated_at")
    required = profile.get("required_evidence")
    if not isinstance(required, list) or not required or any(
        not isinstance(x, str) or not x.strip() for x in required
    ) or len(set(required)) != len(required):
        raise ValueError("required_evidence must contain unique nonempty IDs")
    max_age = profile.get("max_observation_age_seconds")
    if max_age is not None and (type(max_age) is not int or max_age < 0):
        raise ValueError("max_observation_age_seconds must be a nonnegative integer")
    records = profile.get("records")
    if not isinstance(records, list):
        raise ValueError("records must be an array")
    by_id: dict[str, list[dict[str, Any]]] = {x: [] for x in required}
    seen: set[str] = set()
    for rec in records:
        if not isinstance(rec, dict):
            raise ValueError("record must be an object")
        rid, eid = rec.get("id"), rec.get("evidence_id")
        if not isinstance(rid, str) or not rid.strip() or rid in seen:
            raise ValueError("record IDs must be unique nonempty strings")
        seen.add(rid)
        if not isinstance(eid, str) or eid not in by_id:
            raise ValueError("record references undeclared evidence")
        pin = rec.get("source_pin")
        if not isinstance(pin, dict) or not isinstance(pin.get("repository"), str) or not pin["repository"].strip() or not isinstance(pin.get("revision"), str) or not pin["revision"].strip():
            raise ValueError("record requires a nonempty repository and immutable revision declaration")
        observed = _instant(rec.get("observed_at"), "observed_at")
        recorded = _instant(rec.get("recorded_at"), "recorded_at")
        start = _instant(rec.get("effective_from"), "effective_from")
        end = _instant(rec["effective_until"], "effective_until") if rec.get("effective_until") is not None else None
        if end is not None and end <= start:
            raise ValueError("effective_until must be after effective_from")
        if observed > recorded:
            raise ValueError("observed_at cannot exceed recorded_at")
        if recorded > evaluated:
            raise ValueError("recorded_at cannot exceed evaluated_at")
        by_id[eid].append({"id": rid, "observed": observed, "recorded": recorded, "start": start, "end": end})

    findings: list[dict[str, Any]] = []
    for eid in sorted(required):
        items = by_id[eid]
        known = [r for r in items if r["recorded"] <= cutoff]
        future = sorted(r["id"] for r in items if r["recorded"] > cutoff)
        if not known:
            status = "NOT_KNOWN_AT_CUTOFF"
        elif len(known) > 1:
            status = "CONFLICT"
        else:
            r = known[0]
            if target < r["start"] or (r["end"] is not None and target >= r["end"]):
                status = "OUTSIDE_EFFECTIVE_INTERVAL"
            elif max_age is not None and (r["observed"] > evaluated or evaluated - r["observed"] > timedelta(seconds=max_age)):
                status = "STALE_OR_FUTURE_OBSERVATION"
            else:
                status = "APPLICABLE"
        findings.append({
            "evidence_id": eid,
            "status": status,
            "known_record_ids": sorted(r["id"] for r in known),
            "later_record_ids": future,
        })
    outcome = "APPLICABLE" if all(f["status"] == "APPLICABLE" for f in findings) else "INDETERMINATE"
    return {
        "schema": SCHEMA,
        "proposition_id": profile["proposition_id"],
        "disposition": outcome,
        "findings": findings,
        "authority_note": "Declared temporal applicability only; no authenticity, truth, revocation or assurance PASS.",
    }
