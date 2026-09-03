#!/usr/bin/env python3
"""Portable evaluators for bounded RAHP assurance invariants.

These helpers evaluate generic assurance propositions. They deliberately do not
infer entitlement, authority, or trustworthiness from missing evidence and do
not encode DTG-specific protocol semantics.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Iterable


OUTCOMES = {"PASS", "FAIL", "INDETERMINATE"}


def _result(outcome: str, *reasons: str) -> dict[str, Any]:
    if outcome not in OUTCOMES:
        raise ValueError(f"invalid outcome: {outcome}")
    return {"outcome": outcome, "reasons": list(reasons)}


def evaluate_evidence_asymmetry(context: dict[str, Any]) -> dict[str, Any]:
    """Ensure missing preferred evidence is not converted into adverse inference.

    The evaluator does not require insufficient evidence to be accepted. A
    policy may deny or defer because required evidence is absent, provided it
    does not reinterpret absence as fraud, ineligibility, low trustworthiness,
    or another unsupported negative fact.
    """
    preferred_available = context.get("preferred_evidence_available")
    adverse_inference = context.get("adverse_inference")
    independent_negative_evidence = context.get("independent_negative_evidence", False)
    decision = context.get("decision")

    if preferred_available is None:
        return _result("INDETERMINATE", "preferred-evidence-availability-unknown")

    if not preferred_available and adverse_inference and not independent_negative_evidence:
        return _result("FAIL", "evidence-absence-converted-to-adverse-inference")

    if not preferred_available:
        if decision in {"INDETERMINATE", "DEFER", "ESCALATE"}:
            return _result("PASS", "uncertainty-preserved")
        if decision == "DENY" and context.get("denial_reason") == "insufficient-evidence":
            return _result("PASS", "insufficient-evidence-not-adverse-inference")
        return _result("INDETERMINATE", "missing-evidence-disposition-unclear")

    return _result("PASS", "preferred-evidence-present")


def evaluate_assurance_floor(
    declared_floor: dict[str, int],
    effective_assurance: dict[str, int],
    *,
    fallback_occurred: bool = False,
    fallback_visible: bool | None = None,
    authorized_floor_override: dict[str, int] | None = None,
) -> dict[str, Any]:
    """Check that negotiated/fallback semantics do not cross a policy floor.

    Assurance levels are intentionally represented as caller-defined integers;
    RAHP compares order, not protocol-specific labels. An explicit policy
    override may authorize a lower floor for a known fallback mode.
    """
    floor = authorized_floor_override if authorized_floor_override is not None else declared_floor
    missing = sorted(set(floor) - set(effective_assurance))
    if missing:
        return _result("INDETERMINATE", "assurance-dimension-missing:" + ",".join(missing))

    below = sorted(key for key, minimum in floor.items() if effective_assurance[key] < minimum)
    if below:
        return _result("FAIL", "assurance-floor-violated:" + ",".join(below))

    if fallback_occurred and fallback_visible is not True:
        if fallback_visible is None:
            return _result("INDETERMINATE", "fallback-visibility-unknown")
        return _result("FAIL", "fallback-not-visible")

    reason = "authorized-lower-floor-preserved" if authorized_floor_override is not None else "declared-floor-preserved"
    return _result("PASS", reason)


def _binding_matches(declared: Any, requested: Any) -> bool:
    if declared == "*":
        return True
    if isinstance(declared, (list, tuple, set, frozenset)):
        return requested in declared
    return declared == requested


def evaluate_authority_context_binding(
    authority_context: dict[str, Any], requested_context: dict[str, Any]
) -> dict[str, Any]:
    """Check confused-deputy bindings for a consequential action context."""
    dimensions = ("principal", "resource", "purpose", "beneficiary", "action")
    missing = [key for key in dimensions if key not in authority_context or key not in requested_context]
    if missing:
        return _result("INDETERMINATE", "context-binding-missing:" + ",".join(missing))

    mismatches = [
        key for key in dimensions
        if not _binding_matches(authority_context[key], requested_context[key])
    ]
    if mismatches:
        return _result("FAIL", "authority-context-mismatch:" + ",".join(mismatches))

    return _result("PASS", "authority-context-bound")


def evaluate_historical_evidence_use(
    evidence: dict[str, Any],
    *,
    consequential_use: bool,
    decision_context: str | None = None,
    at: datetime | None = None,
) -> dict[str, Any]:
    """Bound consequential reliance on retained historical trust evidence.

    Retention for audit/accountability is permitted. The proposition fails only
    when stale, corrected, superseded, restored, or context-inapplicable
    evidence is still given consequential decision authority.
    """
    if not consequential_use:
        return _result("PASS", "retention-separated-from-consequential-use")

    state = evidence.get("state")
    if state in {"corrected", "superseded", "restored", "revoked", "expired"}:
        return _result("FAIL", f"historical-state-used-consequentially:{state}")

    applicable_contexts: Iterable[str] | None = evidence.get("applicable_contexts")
    if applicable_contexts is not None and decision_context not in applicable_contexts:
        return _result("FAIL", "historical-evidence-used-outside-context")

    use_until = evidence.get("decision_use_until")
    if use_until is not None:
        if at is None:
            return _result("INDETERMINATE", "decision-time-unknown")
        if isinstance(use_until, str):
            use_until = datetime.fromisoformat(use_until.replace("Z", "+00:00"))
        if at > use_until:
            return _result("FAIL", "historical-evidence-use-window-expired")

    if state is None and use_until is None and applicable_contexts is None:
        return _result("INDETERMINATE", "historical-relevance-unbounded")

    return _result("PASS", "historical-relevance-bounded")
