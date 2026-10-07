"""Optional, bounded reasoning-trace profile; not an assessor or proof engine."""
from __future__ import annotations

from typing import Any

TRACE_SCHEMA = "rahp-reasoning-trace/v1"
RESULTS = {"SATISFIED", "NOT_SATISFIED", "INDETERMINATE"}
OUTCOMES = {"PASS", "FAIL", "INDETERMINATE", "NOT_APPLICABLE"}


def validate_trace(trace: dict[str, Any], assessor_result: dict[str, Any] | None = None) -> list[str]:
    errors: list[str] = []
    if not isinstance(trace, dict):
        return ["trace must be an object"]
    if trace.get("schema") != TRACE_SCHEMA:
        errors.append("unsupported trace schema")
    for key in ("proposition_id", "method", "method_version", "scope"):
        if not isinstance(trace.get(key), str) or not trace[key].strip():
            errors.append(f"{key} must be a non-empty string")
    evidence = trace.get("evidence_refs")
    if not isinstance(evidence, list) or not all(isinstance(x, str) and x for x in evidence):
        errors.append("evidence_refs must be an array of non-empty strings")
        evidence = []
    elif len(evidence) != len(set(evidence)):
        errors.append("evidence_refs must be unique")
    observations = trace.get("observations")
    if not isinstance(observations, list) or not observations:
        errors.append("observations must be a non-empty array")
        observations = []
    seen: set[str] = set()
    for i, obs in enumerate(observations):
        if not isinstance(obs, dict):
            errors.append(f"observations[{i}] must be an object")
            continue
        oid = obs.get("id")
        if not isinstance(oid, str) or not oid:
            errors.append(f"observations[{i}].id is required")
        elif oid in seen:
            errors.append(f"duplicate observation id: {oid}")
        else:
            seen.add(oid)
        if obs.get("result") not in RESULTS:
            errors.append(f"observations[{i}].result invalid")
        refs = obs.get("evidence_refs")
        if not isinstance(refs, list) or not refs or any(ref not in evidence for ref in refs):
            errors.append(f"observations[{i}] must reference declared evidence")
    judgment = trace.get("judgment")
    if not isinstance(judgment, dict):
        errors.append("judgment must be an object")
        judgment = {}
    outcome = judgment.get("outcome")
    if outcome not in OUTCOMES:
        errors.append("judgment.outcome invalid")
    if not isinstance(judgment.get("reason_codes"), list) or not judgment["reason_codes"] or any(not isinstance(x, str) or not x for x in judgment["reason_codes"]):
        errors.append("judgment.reason_codes required")
    if any(isinstance(o, dict) and o.get("result") == "INDETERMINATE" for o in observations) and outcome == "PASS":
        errors.append("PASS cannot silently bypass indeterminate observations")
    if any(isinstance(o, dict) and o.get("result") == "NOT_SATISFIED" for o in observations) and outcome == "PASS":
        errors.append("PASS cannot silently bypass contradictory observations")
    if assessor_result is not None:
        if outcome != assessor_result.get("outcome"):
            errors.append("trace judgment and assessor outcome disagree")
        used = assessor_result.get("evidence_used", [])
        if not isinstance(used, list) or set(evidence) != set(used):
            errors.append("trace evidence and assessor evidence_used disagree")
    return errors
