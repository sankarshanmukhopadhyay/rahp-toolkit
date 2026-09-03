import unittest

from tools.evidence_topology_invariants import (
    evaluate_evidence_suppression,
    evaluate_relationship_evidence_semantics,
    evaluate_trust_view_isolation,
)


class RelationshipEvidenceSemanticsTests(unittest.TestCase):
    def test_valid_but_disputed_relationship_cannot_drive_consequential_decision(self):
        result = evaluate_relationship_evidence_semantics({
            "cryptographically_valid": True,
            "consequential_use": True,
            "semantic_status": "disputed",
            "publisher_provenance_verified": True,
            "contestability_available": True,
        })
        self.assertEqual(result["outcome"], "FAIL")

    def test_valid_signature_without_semantic_status_is_indeterminate(self):
        result = evaluate_relationship_evidence_semantics({
            "cryptographically_valid": True,
            "consequential_use": True,
        })
        self.assertEqual(result["outcome"], "INDETERMINATE")

    def test_governed_corroborated_negative_evidence_is_valid_counter_case(self):
        result = evaluate_relationship_evidence_semantics({
            "cryptographically_valid": True,
            "consequential_use": True,
            "semantic_status": "current",
            "publisher_provenance_verified": True,
            "contestability_available": True,
            "negative_effect": True,
            "governed_negative_evidence": True,
            "corroborated": True,
        })
        self.assertEqual(result["outcome"], "PASS")

    def test_corrected_assertion_cannot_continue_consequential_use(self):
        result = evaluate_relationship_evidence_semantics({
            "cryptographically_valid": True,
            "consequential_use": True,
            "semantic_status": "corrected",
        })
        self.assertEqual(result["outcome"], "FAIL")


class EvidenceSuppressionTests(unittest.TestCase):
    def test_withheld_evidence_presented_as_complete_fails(self):
        result = evaluate_evidence_suppression({
            "consequential_use": True,
            "known_material_evidence_withheld": True,
            "completeness_claim": "complete",
        })
        self.assertEqual(result["outcome"], "FAIL")

    def test_suppression_cannot_be_interpreted_as_no_entitlement(self):
        result = evaluate_evidence_suppression({
            "consequential_use": True,
            "known_material_evidence_withheld": True,
            "completeness_claim": "partial",
            "absence_interpretation": "no-entitlement",
        })
        self.assertEqual(result["outcome"], "FAIL")

    def test_unknown_completeness_remains_indeterminate(self):
        result = evaluate_evidence_suppression({
            "consequential_use": True,
            "known_material_evidence_withheld": False,
        })
        self.assertEqual(result["outcome"], "INDETERMINATE")

    def test_privacy_preserving_nondisclosure_is_valid_counter_case(self):
        result = evaluate_evidence_suppression({
            "consequential_use": True,
            "known_material_evidence_withheld": True,
            "privacy_preserving_nondisclosure": True,
            "completeness_claim": "partial",
            "absence_interpretation": "unknown",
        })
        self.assertEqual(result["outcome"], "PASS")


class TrustViewIsolationTests(unittest.TestCase):
    def test_attacker_controlled_coherent_view_treated_as_complete_fails(self):
        result = evaluate_trust_view_isolation({
            "consequential_use": True,
            "attacker_can_materially_constrain_view": True,
            "treated_as_complete": True,
            "source_diversity_known": True,
            "independent_sources": 1,
        })
        self.assertEqual(result["outcome"], "FAIL")

    def test_stale_partition_treated_as_complete_fails(self):
        result = evaluate_trust_view_isolation({
            "consequential_use": True,
            "stale_or_partitioned": True,
            "treated_as_complete": True,
        })
        self.assertEqual(result["outcome"], "FAIL")

    def test_unknown_diversity_is_indeterminate(self):
        result = evaluate_trust_view_isolation({
            "consequential_use": True,
            "treated_as_complete": True,
            "source_diversity_known": False,
        })
        self.assertEqual(result["outcome"], "INDETERMINATE")

    def test_resilient_multi_source_discovery_is_valid_counter_case(self):
        result = evaluate_trust_view_isolation({
            "consequential_use": True,
            "treated_as_complete": True,
            "source_diversity_known": True,
            "independent_sources": 3,
            "required_independent_sources": 2,
            "freshness_verified": True,
        })
        self.assertEqual(result["outcome"], "PASS")

    def test_legitimate_partial_view_is_valid_counter_case(self):
        result = evaluate_trust_view_isolation({
            "consequential_use": True,
            "partial_view_declared": True,
            "treated_as_complete": False,
        })
        self.assertEqual(result["outcome"], "PASS")


if __name__ == "__main__":
    unittest.main()
