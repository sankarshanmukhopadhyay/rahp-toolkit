import unittest
from datetime import datetime, timezone

from tools.assurance_invariants import (
    evaluate_assurance_floor,
    evaluate_authority_context_binding,
    evaluate_evidence_asymmetry,
    evaluate_historical_evidence_use,
)


class EvidenceAsymmetryTests(unittest.TestCase):
    def test_missing_preferred_evidence_does_not_support_adverse_inference(self):
        result = evaluate_evidence_asymmetry({
            "preferred_evidence_available": False,
            "adverse_inference": "fraud",
            "independent_negative_evidence": False,
            "decision": "DENY",
        })
        self.assertEqual(result["outcome"], "FAIL")

    def test_unavailable_essential_service_evidence_needs_recovery_route(self):
        result = evaluate_evidence_asymmetry({
            "preferred_evidence_available": False,
            "essential_service": True,
            "decision": "DENY",
            "denial_reason": "insufficient-evidence",
        })
        self.assertEqual(result["outcome"], "FAIL")

    def test_missing_evidence_can_preserve_uncertainty_and_escalate(self):
        result = evaluate_evidence_asymmetry({
            "preferred_evidence_available": False,
            "essential_service": True,
            "decision": "ESCALATE",
            "alternative_evidence_route": True,
        })
        self.assertEqual(result["outcome"], "PASS")

    def test_genuinely_insufficient_evidence_may_be_denied_without_negative_inference(self):
        result = evaluate_evidence_asymmetry({
            "preferred_evidence_available": False,
            "decision": "DENY",
            "denial_reason": "insufficient-evidence",
        })
        self.assertEqual(result["outcome"], "PASS")


class AssuranceFloorTests(unittest.TestCase):
    def test_silent_fallback_below_declared_floor_fails(self):
        result = evaluate_assurance_floor(
            {"privacy": 3, "freshness": 2},
            {"privacy": 1, "freshness": 2},
            fallback_occurred=True,
            fallback_visible=False,
        )
        self.assertEqual(result["outcome"], "FAIL")

    def test_peer_forced_weaker_semantics_cannot_cross_floor(self):
        result = evaluate_assurance_floor(
            {"authentication": 3},
            {"authentication": 2},
            fallback_occurred=True,
            fallback_visible=True,
        )
        self.assertEqual(result["outcome"], "FAIL")

    def test_explicitly_authorized_lower_mode_is_valid_counter_case(self):
        result = evaluate_assurance_floor(
            {"privacy": 3},
            {"privacy": 2},
            fallback_occurred=True,
            fallback_visible=True,
            authorized_floor_override={"privacy": 2},
        )
        self.assertEqual(result["outcome"], "PASS")

    def test_missing_assurance_dimension_is_indeterminate(self):
        result = evaluate_assurance_floor({"freshness": 2}, {})
        self.assertEqual(result["outcome"], "INDETERMINATE")


class AuthorityContextBindingTests(unittest.TestCase):
    def setUp(self):
        self.authority = {
            "principal": "alice",
            "resource": "account-1",
            "purpose": "benefit-payment",
            "beneficiary": "alice",
            "action": "disburse",
        }

    def test_valid_authority_reused_for_wrong_beneficiary_fails(self):
        requested = dict(self.authority, beneficiary="bob")
        self.assertEqual(
            evaluate_authority_context_binding(self.authority, requested)["outcome"],
            "FAIL",
        )

    def test_context_drift_in_purpose_fails(self):
        requested = dict(self.authority, purpose="debt-collection")
        self.assertEqual(
            evaluate_authority_context_binding(self.authority, requested)["outcome"],
            "FAIL",
        )

    def test_explicit_reusable_binding_is_valid_counter_case(self):
        reusable = dict(self.authority, resource=["account-1", "account-2"])
        requested = dict(self.authority, resource="account-2")
        self.assertEqual(
            evaluate_authority_context_binding(reusable, requested)["outcome"],
            "PASS",
        )

    def test_missing_context_binding_is_indeterminate(self):
        incomplete = dict(self.authority)
        del incomplete["beneficiary"]
        self.assertEqual(
            evaluate_authority_context_binding(incomplete, self.authority)["outcome"],
            "INDETERMINATE",
        )


class HistoricalEvidenceUseTests(unittest.TestCase):
    def test_corrected_evidence_cannot_continue_consequential_use(self):
        result = evaluate_historical_evidence_use(
            {"state": "corrected", "retained_for": ["audit"]},
            consequential_use=True,
            decision_context="eligibility",
        )
        self.assertEqual(result["outcome"], "FAIL")

    def test_old_context_specific_event_cannot_be_generalized(self):
        result = evaluate_historical_evidence_use(
            {"state": "current", "applicable_contexts": ["service-a"]},
            consequential_use=True,
            decision_context="service-b",
        )
        self.assertEqual(result["outcome"], "FAIL")

    def test_immutable_audit_retention_without_decision_use_is_valid(self):
        result = evaluate_historical_evidence_use(
            {"state": "superseded", "retained_for": ["audit"]},
            consequential_use=False,
            decision_context="eligibility",
        )
        self.assertEqual(result["outcome"], "PASS")

    def test_unbounded_historical_relevance_is_indeterminate(self):
        result = evaluate_historical_evidence_use(
            {"artifact_id": "old-assertion"},
            consequential_use=True,
            decision_context="eligibility",
        )
        self.assertEqual(result["outcome"], "INDETERMINATE")

    def test_expired_decision_use_window_fails(self):
        result = evaluate_historical_evidence_use(
            {"state": "current", "decision_use_until": "2026-08-01T00:00:00Z"},
            consequential_use=True,
            decision_context="eligibility",
            at=datetime(2026, 9, 3, tzinfo=timezone.utc),
        )
        self.assertEqual(result["outcome"], "FAIL")


if __name__ == "__main__":
    unittest.main()
