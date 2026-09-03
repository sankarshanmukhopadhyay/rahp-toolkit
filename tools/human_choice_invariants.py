#!/usr/bin/env python3
"""Portable RAHP evaluators for disclosure pressure, proxy use, and meaningful choice."""
from __future__ import annotations
from typing import Any

OUTCOMES = {"PASS", "FAIL", "INDETERMINATE"}


def _result(outcome: str, *reasons: str, dpip_handoff_required: bool = False) -> dict[str, Any]:
    if outcome not in OUTCOMES:
        raise ValueError(f"invalid outcome: {outcome}")
    return {"outcome": outcome, "reasons": list(reasons), "dpip_handoff_required": dpip_handoff_required}


def evaluate_disclosure_pressure(context: dict[str, Any]) -> dict[str, Any]:
    minimal = context.get("minimal_proof_available")
    expanded = context.get("expanded_disclosure_requested")
    necessary = context.get("expanded_disclosure_necessary")
    refusal = context.get("refusal_meaningfully_available")
    dependency = context.get("high_dependency_service", False)
    privacy_depth = context.get("correlation_or_minimization_depth_material", False)
    if minimal is None or expanded is None:
        return _result("INDETERMINATE", "disclosure-choice-evidence-incomplete", dpip_handoff_required=privacy_depth)
    if not expanded:
        return _result("PASS", "minimal-disclosure-path-preserved", dpip_handoff_required=privacy_depth)
    if necessary is None:
        return _result("INDETERMINATE", "expanded-disclosure-necessity-unknown", dpip_handoff_required=privacy_depth)
    if necessary and context.get("enhanced_assurance_justification_documented") is True:
        return _result("PASS", "enhanced-assurance-disclosure-justified", dpip_handoff_required=privacy_depth)
    if minimal and not necessary and (refusal is False or dependency or context.get("service_denied_on_refusal") is True):
        return _result("FAIL", "unnecessary-expanded-disclosure-compelled", dpip_handoff_required=privacy_depth)
    if minimal and not necessary:
        return _result("INDETERMINATE", "expanded-disclosure-requested-without-established-compulsion", dpip_handoff_required=privacy_depth)
    return _result("PASS", "no-disclosure-pressure-established", dpip_handoff_required=privacy_depth)


def evaluate_proxy_use(context: dict[str, Any]) -> dict[str, Any]:
    if context.get("consequential_use") is not True:
        return _result("PASS", "metadata-not-used-consequentially")
    if not context.get("feature"):
        return _result("INDETERMINATE", "consequential-feature-unknown")
    privacy_depth = context.get("privacy_or_correlation_analysis_material", False)
    proxy_risk = context.get("sensitive_or_social_proxy_risk")
    relevance = context.get("relevance_validated")
    necessity = context.get("necessity_supported")
    if proxy_risk is None:
        return _result("INDETERMINATE", "proxy-effect-unknown", dpip_handoff_required=privacy_depth)
    if proxy_risk and relevance is not True:
        return _result("FAIL", "consequential-proxy-relevance-unvalidated", dpip_handoff_required=privacy_depth)
    if proxy_risk and necessity is not True:
        return _result("FAIL", "consequential-proxy-not-necessary", dpip_handoff_required=privacy_depth)
    if proxy_risk and context.get("less_harmful_alternative_available") is True:
        return _result("FAIL", "less-harmful-decision-feature-available", dpip_handoff_required=privacy_depth)
    if proxy_risk and context.get("governance_approved") is not True:
        return _result("INDETERMINATE", "proxy-governance-approval-missing", dpip_handoff_required=privacy_depth)
    if relevance is False:
        return _result("FAIL", "feature-relevance-rejected", dpip_handoff_required=privacy_depth)
    if relevance is None or necessity is None:
        return _result("INDETERMINATE", "proxy-relevance-or-necessity-unknown", dpip_handoff_required=privacy_depth)
    return _result("PASS", "consequential-feature-governed-and-supported", dpip_handoff_required=privacy_depth)


def evaluate_meaningful_choice(context: dict[str, Any]) -> dict[str, Any]:
    recorded = context.get("authorization_recorded")
    if recorded is None:
        return _result("INDETERMINATE", "authorization-record-unknown")
    if recorded is not True:
        return _result("FAIL", "authorization-not-recorded")
    for field, reason in (
        ("bundled_unrelated_purposes", "unrelated-purposes-bundled"),
        ("deceptive_default", "deceptive-default-shapes-choice"),
        ("repeated_pressure_loop", "repeated-prompting-undermines-refusal"),
        ("refusal_consequence_disproportionate", "disproportionate-refusal-consequence"),
    ):
        if context.get(field) is True:
            return _result("FAIL", reason)
    required = ("purpose_specific", "scope_understandable", "refusal_meaningfully_available", "reversible_or_correctable")
    missing = [key for key in required if context.get(key) is None]
    if missing:
        return _result("INDETERMINATE", "choice-evidence-missing:" + ",".join(missing))
    failures = [key for key in required if context.get(key) is not True]
    if failures:
        return _result("FAIL", "choice-condition-failed:" + ",".join(failures))
    return _result("PASS", "authorization-meaningful-choice-supported")
