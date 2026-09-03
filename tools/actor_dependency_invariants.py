#!/usr/bin/env python3
"""Portable RAHP evaluators for actor/accountability and trust-source integrity."""
from __future__ import annotations

from typing import Any


OUTCOMES = {"PASS", "FAIL", "INDETERMINATE"}


def _result(outcome: str, *reasons: str) -> dict[str, Any]:
    if outcome not in OUTCOMES:
        raise ValueError(f"invalid outcome: {outcome}")
    return {"outcome": outcome, "reasons": list(reasons)}


def evaluate_delegation_accountability(context: dict[str, Any]) -> dict[str, Any]:
    """Detect semantic laundering of principal, benefit and accountability roles.

    This evaluates role transparency and beneficiary/accountability continuity;
    it intentionally does not re-evaluate delegation scope or re-delegation.
    """
    roles = ("acting_agent", "represented_principal", "beneficiary", "accountable_decision_maker")
    missing = [role for role in roles if not context.get(role)]
    if missing:
        return _result("INDETERMINATE", "delegation-role-missing:" + ",".join(missing))

    if context.get("hidden_principal"):
        return _result("FAIL", "represented-principal-hidden")

    expected_beneficiary = context.get("authorized_beneficiary")
    if expected_beneficiary is not None and context["beneficiary"] != expected_beneficiary:
        return _result("FAIL", "beneficiary-substitution")

    if context.get("agent_self_dealing") and not context.get("self_dealing_explicitly_authorized", False):
        return _result("FAIL", "undisclosed-agent-self-dealing")

    if context.get("accountability_lineage_complete") is not True:
        if context.get("accountability_lineage_complete") is None:
            return _result("INDETERMINATE", "accountability-lineage-unknown")
        return _result("FAIL", "accountability-lineage-broken")

    return _result("PASS", "delegation-roles-explicit-and-accountable")


def evaluate_effective_actor_continuity(context: dict[str, Any]) -> dict[str, Any]:
    """Separate validity of presented evidence from current effective control."""
    intended = context.get("intended_controller")
    effective = context.get("effective_controller")
    if intended is None:
        return _result("INDETERMINATE", "intended-controller-unknown")
    if effective is None:
        return _result("INDETERMINATE", "effective-controller-unknown")

    if context.get("control_state") in {"retired", "revoked", "recovered"} and context.get("old_control_used"):
        return _result("FAIL", "superseded-control-used")

    if intended == effective:
        return _result("PASS", "effective-controller-continuity-proven")

    if context.get("authorized_migration"):
        if context.get("migration_evidence_verified") is True and context.get("current_control_state_verified") is True:
            return _result("PASS", "authorized-controller-migration")
        return _result("INDETERMINATE", "controller-migration-evidence-incomplete")

    return _result("FAIL", "effective-controller-substitution")


def evaluate_external_trust_sources(
    sources: list[dict[str, Any]], *, corroboration_required: bool = False
) -> dict[str, Any]:
    """Evaluate integrity/freshness/provenance of accepted external trust inputs.

    Correct downstream parsing is outside this proposition. The evaluator asks
    whether the accepted source material itself has sufficient independent
    integrity evidence and whether multiple authoritative sources disagree.
    """
    accepted = [source for source in sources if source.get("accepted", True)]
    if not accepted:
        return _result("INDETERMINATE", "no-accepted-trust-source")

    compromised = [source.get("id", "unknown") for source in accepted if source.get("integrity") == "compromised"]
    if compromised:
        return _result("FAIL", "compromised-source-accepted:" + ",".join(sorted(compromised)))

    stale = [source.get("id", "unknown") for source in accepted if source.get("freshness") == "stale"]
    if stale:
        return _result("FAIL", "stale-source-accepted:" + ",".join(sorted(stale)))

    unknown_checks = []
    for source in accepted:
        source_id = source.get("id", "unknown")
        if source.get("integrity") != "verified":
            unknown_checks.append(f"{source_id}:integrity")
        if source.get("freshness") != "current":
            unknown_checks.append(f"{source_id}:freshness")
        if source.get("provenance_verified") is not True:
            unknown_checks.append(f"{source_id}:provenance")
    if unknown_checks:
        return _result("INDETERMINATE", "source-check-incomplete:" + ",".join(sorted(unknown_checks)))

    values = {source.get("value") for source in accepted if "value" in source}
    if len(values) > 1:
        return _result("INDETERMINATE", "authoritative-sources-disagree")

    if corroboration_required and len(accepted) < 2:
        return _result("INDETERMINATE", "independent-corroboration-missing")

    return _result("PASS", "external-source-integrity-supported")
