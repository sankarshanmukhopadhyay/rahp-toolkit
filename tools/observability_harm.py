"""Synthetic observability-harm propositions; no live telemetry or personal data."""
from collections import defaultdict

def evaluate_observability(events, *, prohibited_cross_context=True):
    """Return findings without interpreting telemetry as authoritative policy evidence.

    Events are synthetic dictionaries with context, trace_id, evidence_state and
    optional decision_source. Missing fields cannot establish safety.
    """
    if not isinstance(events, list):
        raise ValueError("events must be a list")
    traces = defaultdict(set)
    unknown = False
    for event in events:
        if not isinstance(event, dict):
            raise ValueError("event must be an object")
        context, trace = event.get("context"), event.get("trace_id")
        if not isinstance(context, str) or not context or not isinstance(trace, str) or not trace:
            unknown = True
        else:
            traces[trace].add(context)
        if event.get("evidence_state") not in ("verified", "missing", "unavailable", "contradictory"):
            unknown = True
        if event.get("evidence_state") != "verified":
            unknown = True
        if event.get("decision_source") == "telemetry" and event.get("consequential_action"):
            return {"state": "FAIL", "reason": "telemetry-promoted-to-authority"}
    if prohibited_cross_context and any(len(contexts) > 1 for contexts in traces.values()):
        return {"state": "FAIL", "reason": "cross-context-trace-correlation"}
    if unknown or not events:
        return {"state": "INDETERMINATE", "reason": "insufficient-observation-evidence"}
    return {"state": "INDETERMINATE", "reason": "no-failure-observed-not-proof-of-safety"}
