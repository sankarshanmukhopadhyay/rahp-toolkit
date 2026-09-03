import unittest

from tools.human_choice_invariants import (
    evaluate_disclosure_pressure,
    evaluate_meaningful_choice,
    evaluate_proxy_use,
)


class DisclosurePressureTests(unittest.TestCase):
    def test_unnecessary_expanded_disclosure_under_dependency_fails(self):
        result = evaluate_disclosure_pressure({
            "minimal_proof_available": True,
            "expanded_disclosure_requested": True,
            "expanded_disclosure_necessary": False,
            "high_dependency_service": True,
            "refusal_meaningfully_available": False,
            "correlation_or_minimization_depth_material": True,
        })
        self.assertEqual(result["outcome"], "FAIL")
        self.assertTrue(result["dpip_handoff_required"])

    def test_stable_identifier_demand_with_service_denial_fails(self):
        result = evaluate_disclosure_pressure({
            "minimal_proof_available": True,
            "expanded_disclosure_requested": True,
            "expanded_disclosure_necessary": False,
            "service_denied_on_refusal": True,
        })
        self.assertEqual(result["outcome"], "FAIL")

    def test_enhanced_assurance_request_is_valid_counter_case(self):
        result = evaluate_disclosure_pressure({
            "minimal_proof_available": True,
            "expanded_disclosure_requested": True,
            "expanded_disclosure_necessary": True,
            "enhanced_assurance_justification_documented": True,
            "refusal_meaningfully_available": True,
        })
        self.assertEqual(result["outcome"], "PASS")

    def test_extra_request_without_power_evidence_is_indeterminate(self):
        result = evaluate_disclosure_pressure({
            "minimal_proof_available": True,
            "expanded_disclosure_requested": True,
            "expanded_disclosure_necessary": False,
            "refusal_meaningfully_available": True,
        })
        self.assertEqual(result["outcome"], "INDETERMINATE")


class ProxyUseTests(unittest.TestCase):
    def test_sparse_graph_as_unvalidated_risk_proxy_fails(self):
        result = evaluate_proxy_use({
            "consequential_use": True,
            "feature": "graph-density",
            "sensitive_or_social_proxy_risk": True,
            "relevance_validated": False,
            "necessity_supported": False,
            "privacy_or_correlation_analysis_material": True,
        })
        self.assertEqual(result["outcome"], "FAIL")
        self.assertTrue(result["dpip_handoff_required"])

    def test_issuer_choice_proxy_with_less_harmful_alternative_fails(self):
        result = evaluate_proxy_use({
            "consequential_use": True,
            "feature": "issuer-choice",
            "sensitive_or_social_proxy_risk": True,
            "relevance_validated": True,
            "necessity_supported": True,
            "less_harmful_alternative_available": True,
            "governance_approved": True,
        })
        self.assertEqual(result["outcome"], "FAIL")

    def test_unknown_proxy_effect_is_indeterminate(self):
        result = evaluate_proxy_use({
            "consequential_use": True,
            "feature": "community-membership",
        })
        self.assertEqual(result["outcome"], "INDETERMINATE")

    def test_governed_relevant_feature_is_valid_counter_case(self):
        result = evaluate_proxy_use({
            "consequential_use": True,
            "feature": "recent-verified-fraud-event",
            "sensitive_or_social_proxy_risk": True,
            "relevance_validated": True,
            "necessity_supported": True,
            "less_harmful_alternative_available": False,
            "governance_approved": True,
        })
        self.assertEqual(result["outcome"], "PASS")


class MeaningfulChoiceTests(unittest.TestCase):
    def test_bundled_unrelated_purposes_fail(self):
        result = evaluate_meaningful_choice({
            "authorization_recorded": True,
            "bundled_unrelated_purposes": True,
        })
        self.assertEqual(result["outcome"], "FAIL")

    def test_deceptive_default_fails(self):
        result = evaluate_meaningful_choice({
            "authorization_recorded": True,
            "deceptive_default": True,
        })
        self.assertEqual(result["outcome"], "FAIL")

    def test_repeated_pressure_loop_fails(self):
        result = evaluate_meaningful_choice({
            "authorization_recorded": True,
            "repeated_pressure_loop": True,
        })
        self.assertEqual(result["outcome"], "FAIL")

    def test_missing_choice_evidence_is_indeterminate(self):
        result = evaluate_meaningful_choice({
            "authorization_recorded": True,
            "purpose_specific": True,
        })
        self.assertEqual(result["outcome"], "INDETERMINATE")

    def test_informed_reversible_purpose_specific_choice_is_valid_counter_case(self):
        result = evaluate_meaningful_choice({
            "authorization_recorded": True,
            "purpose_specific": True,
            "scope_understandable": True,
            "refusal_meaningfully_available": True,
            "reversible_or_correctable": True,
        })
        self.assertEqual(result["outcome"], "PASS")


if __name__ == "__main__":
    unittest.main()
