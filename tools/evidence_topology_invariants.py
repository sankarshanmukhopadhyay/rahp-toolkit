#!/usr/bin/env python3
"""Portable RAHP evaluators for adversarial evidence semantics and trust views."""
from __future__ import annotations

from typing import Any


OUTCOMES = {"PASS", "FAIL", "INDETERMINATE"}


def _result(outcome: str, *reasons: str) -> dict[str, Any]:
    if outcome not in OUTCOMES:
        raise ValueError(f"invalid outcome: {outcome}")
    return {"outcome": outcome, "reasons": list(reasons)}


def evaluate_relationship_evidence_semantics(context: dict[str, Any]) -> dict[str, Any]:
    """Prevent cryptographic validity from being over-read as semantic truth.

    RAHP does not determine objective truth. It checks whether consequential use
    has governance evidence for provenance, contestability and semantic status.
    """
    if context.get("cryptographically_valid") is not True:
        if context.get("cryptographically_valid") is None:
            return _result("INDETERMINATE", "cryptographic-validity-unknown")
        return _result("FAIL", "relationship-evidence-cryptographically-invalid")

    if not context.get("consequential_use", False):
        return _result("PASS", "non-consequential-evidence-use")

    semantic_status = context.get("semantic_status")
    if semantic_status is None:
        return _result("INDETERMINATE", "semantic-status-unknown")

    if semantic_status in {"disputed", "corrected", "abusive", "malicious"}:
        return _result("FAIL", f"adversarial-relationship-evidence-used:{semantic_status}")

    if context.get("publisher_provenance_verified") is not True:
        return _result("INDETERMINATE", "publisher-provenance-unverified")

    if context.get("contestability_available") is not True:
        return _result("INDETERMINATE", "contestability-evidence-missing")

    if context.get("negative_effect", False):
        if context.get("governed_negative_evidence") is not True:
            return _result("INDETERMINATE", "negative-evidence-governance-unknown")
        if context.get("corroborated") is not True:
            return _result("INDETERMINATE", "negative-evidence-corroboration-missing")

    return _result("PASS", "relationship-evidence-consequential-use-bounded")


def evaluate_evidence_suppression(context: dict[str, Any]) -> dict[str, Any]:
    """Distinguish neutral absence from unavailable or selectively withheld evidence."""
    if not context.get("consequential_use", False):
        return _result("PASS", "non-consequential-result-set")

    withheld = context.get("known_material_evidence_withheld")
    completeness = context.get("completeness_claim")
    absence_interpretation = context.get("absence_interpretation")

    if withheld is True and completeness in {"complete", "neutral-absence"}:
        return _result("FAIL", "withheld-evidence-presented-as-complete")

    if withheld is True and absence_interpretation in {
        "no-entitlement",
        "no-standing",
        "no-contrary-evidence",
        "negative-trust",
    }:
        return _result("FAIL", "suppression-converted-to-adverse-absence")

    if context.get("privacy_preserving_nondisclosure") is True:
        if completeness == "partial" and absence_interpretation in {None, "unknown"}:
            return _result("PASS", "privacy-preserving-partial-view-declared")
        return _result("INDETERMINATE", "privacy-nondisclosure-boundary-unclear")

    if withheld is None:
        return _result("INDETERMINATE", "withholding-state-unknown")

    if completeness is None:
        return _result("INDETERMINATE", "result-completeness-unknown")

    if context.get("filtered_result_provenance_verified") is not True:
        return _result("INDETERMINATE", "filtered-result-provenance-unverified")

    if context.get("contestability_available") is not True:
        return _result("INDETERMINATE", "suppression-contestability-unknown")

    return _result("PASS", "absence-and-completeness-semantics-explicit")


def evaluate_trust_view_isolation(context: dict[str, Any]) -> dict[str, Any]:
    """Evaluate whether a coherent trust view is safely bounded against isolation."""
    if not context.get("consequential_use", False):
        return _result("PASS", "non-consequential-trust-view")

    if context.get("partial_view_declared") is True and context.get("treated_as_complete") is False:
        return _result("PASS", "partial-view-bounded")

    if context.get("stale_or_partitioned") is True and context.get("treated_as_complete") is True:
        return _result("FAIL", "stale-partition-treated-as-complete")

    attacker_control = context.get("attacker_can_materially_constrain_view")
    if attacker_control is True and context.get("treated_as_complete") is True:
        return _result("FAIL", "adversarially-constrained-view-treated-as-representative")

    diversity_known = context.get("source_diversity_known")
    if diversity_known is not True:
        return _result("INDETERMINATE", "source-diversity-unknown")

    independent_sources = context.get("independent_sources")
    if independent_sources is None:
        return _result("INDETERMINATE", "source-independence-unknown")

    minimum = context.get("required_independent_sources", 1)
    if independent_sources < minimum:
        return _result("INDETERMINATE", "discovery-diversity-below-required-evidence")

    if context.get("freshness_verified") is not True:
        return _result("INDETERMINATE", "trust-view-freshness-unverified")

    return _result("PASS", "trust-view-diversity-and-freshness-supported")
