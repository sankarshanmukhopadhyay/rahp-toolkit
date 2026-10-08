"""R3: deterministic comparison of declared assessment records and open challenges.

Equality of records is not proof of independent execution, source authenticity,
evaluator correctness, or authoritative assurance.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any

SCHEMA = "rahp-reproducibility-challenge/v1"
OUTCOMES = {"PASS", "FAIL", "INDETERMINATE"}
REASONS = {"EVIDENCE", "METHOD", "SCOPE", "TEMPORAL", "OTHER"}


def _nonempty(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a nonempty string")
    return value


def _digest(value: Any) -> str:
    try:
        serialized = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    except (TypeError, ValueError) as exc:
        raise ValueError("record must be canonical JSON-compatible data") from exc
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def compare(profile: dict[str, Any]) -> dict[str, Any]:
    """Compare exactly two declared runs and return inspectable open challenges.

    Run records: id, evaluator_id, evaluator_version, input_pin
    (algorithm=sha256, digest=64 lowercase hex), outcome.
    A pin is a declaration, not a verified input fetch or independent execution.
    """
    if not isinstance(profile, dict) or profile.get("schema") != SCHEMA:
        raise ValueError("unsupported reproducibility schema")
    proposition = _nonempty(profile.get("proposition_id"), "proposition_id")
    runs = profile.get("runs")
    if not isinstance(runs, list) or len(runs) != 2:
        raise ValueError("exactly two runs required")
    normalized = []
    seen = set()
    for run in runs:
        if not isinstance(run, dict):
            raise ValueError("run must be an object")
        rid = _nonempty(run.get("id"), "run id")
        if rid in seen:
            raise ValueError("run IDs must be distinct")
        seen.add(rid)
        eid = _nonempty(run.get("evaluator_id"), "evaluator_id")
        version = _nonempty(run.get("evaluator_version"), "evaluator_version")
        pin = run.get("input_pin")
        if not isinstance(pin, dict) or set(pin) != {"algorithm", "digest"} or pin.get("algorithm") != "sha256":
            raise ValueError("input_pin requires sha256 algorithm and digest")
        digest = pin.get("digest")
        if not isinstance(digest, str) or len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
            raise ValueError("input digest must be lowercase sha256 hex")
        outcome = run.get("outcome")
        if not isinstance(outcome, str) or outcome not in OUTCOMES:
            raise ValueError("unsupported run outcome")
        if set(run) != {"id", "evaluator_id", "evaluator_version", "input_pin", "outcome"}:
            raise ValueError("run has missing or undeclared fields")
        normalized.append({"id": rid, "evaluator_id": eid, "evaluator_version": version,
                           "input_pin": dict(pin), "outcome": outcome})
    normalized.sort(key=lambda r: r["id"])
    a, b = normalized
    same_input = a["input_pin"] == b["input_pin"]
    same_evaluator = (a["evaluator_id"], a["evaluator_version"]) == (b["evaluator_id"], b["evaluator_version"])
    if not same_input:
        disposition = "DIFFERENT_INPUT"
    elif not same_evaluator:
        disposition = "DIFFERENT_EVALUATOR"
    elif a["outcome"] != b["outcome"]:
        disposition = "OUTPUT_DISAGREEMENT"
    else:
        disposition = "DECLARED_MATCH"

    challenges = profile.get("challenges")
    if not isinstance(challenges, list):
        raise ValueError("challenges must be an array")
    ids = set()
    normalized_challenges = []
    for item in challenges:
        if not isinstance(item, dict) or set(item) != {"id", "run_id", "reason", "evidence_refs"}:
            raise ValueError("challenge must have exactly id, run_id, reason, evidence_refs")
        cid = _nonempty(item["id"], "challenge id")
        if cid in ids:
            raise ValueError("duplicate challenge ID")
        ids.add(cid)
        run_id = item["run_id"]
        if not isinstance(run_id, str) or run_id not in seen:
            raise ValueError("challenge must reference a declared run")
        reason = item["reason"]
        if not isinstance(reason, str) or reason not in REASONS:
            raise ValueError("unsupported challenge reason")
        refs = item["evidence_refs"]
        if not isinstance(refs, list) or not refs or any(
            not isinstance(x, str) or not x.strip() for x in refs
        ) or len(set(refs)) != len(refs):
            raise ValueError("challenge requires unique nonempty evidence references")
        normalized_challenges.append({"id": cid, "run_id": run_id, "reason": reason,
                                      "evidence_refs": sorted(refs), "status": "OPEN"})
    normalized_challenges.sort(key=lambda x: x["id"])
    return {"schema": SCHEMA, "proposition_id": proposition, "disposition": disposition,
            "same_input": same_input, "same_evaluator": same_evaluator,
            "runs": [{"id": r["id"], "outcome": r["outcome"],
                      "record_digest": _digest(r)} for r in normalized],
            "challenges": normalized_challenges,
            "authority_note": "Declared comparison only; challenges remain open and no assurance decision is changed."}
