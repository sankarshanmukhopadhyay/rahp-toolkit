import unittest

from tools.actor_dependency_invariants import (
    evaluate_delegation_accountability,
    evaluate_effective_actor_continuity,
    evaluate_external_trust_sources,
)


class DelegationAccountabilityTests(unittest.TestCase):
    def test_hidden_principal_fails_even_with_complete_roles(self):
        result = evaluate_delegation_accountability({
            "acting_agent": "agent-a",
            "represented_principal": "principal-a",
            "beneficiary": "principal-a",
            "accountable_decision_maker": "principal-a",
            "hidden_principal": True,
            "accountability_lineage_complete": True,
        })
        self.assertEqual(result["outcome"], "FAIL")

    def test_beneficiary_substitution_fails(self):
        result = evaluate_delegation_accountability({
            "acting_agent": "agent-a",
            "represented_principal": "principal-a",
            "beneficiary": "agent-a",
            "authorized_beneficiary": "principal-a",
            "accountable_decision_maker": "principal-a",
            "accountability_lineage_complete": True,
        })
        self.assertEqual(result["outcome"], "FAIL")

    def test_explicit_role_separation_is_valid_counter_case(self):
        result = evaluate_delegation_accountability({
            "acting_agent": "agent-a",
            "represented_principal": "principal-a",
            "beneficiary": "beneficiary-b",
            "authorized_beneficiary": "beneficiary-b",
            "accountable_decision_maker": "officer-c",
            "accountability_lineage_complete": True,
        })
        self.assertEqual(result["outcome"], "PASS")

    def test_missing_accountable_role_is_indeterminate(self):
        result = evaluate_delegation_accountability({
            "acting_agent": "agent-a",
            "represented_principal": "principal-a",
            "beneficiary": "principal-a",
        })
        self.assertEqual(result["outcome"], "INDETERMINATE")


class EffectiveActorContinuityTests(unittest.TestCase):
    def test_valid_artifact_with_wrong_effective_controller_fails(self):
        result = evaluate_effective_actor_continuity({
            "credential_valid": True,
            "intended_controller": "alice",
            "effective_controller": "mallory",
            "control_state": "current",
        })
        self.assertEqual(result["outcome"], "FAIL")

    def test_old_control_after_recovery_fails(self):
        result = evaluate_effective_actor_continuity({
            "intended_controller": "alice",
            "effective_controller": "alice-old-device",
            "control_state": "recovered",
            "old_control_used": True,
        })
        self.assertEqual(result["outcome"], "FAIL")

    def test_legitimate_device_migration_is_valid_counter_case(self):
        result = evaluate_effective_actor_continuity({
            "intended_controller": "alice-old-device",
            "effective_controller": "alice-new-device",
            "authorized_migration": True,
            "migration_evidence_verified": True,
            "current_control_state_verified": True,
        })
        self.assertEqual(result["outcome"], "PASS")

    def test_valid_evidence_without_effective_controller_is_indeterminate(self):
        result = evaluate_effective_actor_continuity({
            "credential_valid": True,
            "intended_controller": "alice",
        })
        self.assertEqual(result["outcome"], "INDETERMINATE")


class ExternalTrustSourceTests(unittest.TestCase):
    def test_compromised_status_source_fails(self):
        result = evaluate_external_trust_sources([{
            "id": "status-a",
            "accepted": True,
            "integrity": "compromised",
            "freshness": "current",
            "provenance_verified": True,
            "value": "valid",
        }])
        self.assertEqual(result["outcome"], "FAIL")

    def test_stale_but_syntactically_valid_source_fails(self):
        result = evaluate_external_trust_sources([{
            "id": "registry-a",
            "accepted": True,
            "integrity": "verified",
            "freshness": "stale",
            "provenance_verified": True,
            "value": "issuer-authorized",
        }])
        self.assertEqual(result["outcome"], "FAIL")

    def test_source_disagreement_is_indeterminate(self):
        sources = [
            {"id": "policy-a", "integrity": "verified", "freshness": "current", "provenance_verified": True, "value": "allow"},
            {"id": "policy-b", "integrity": "verified", "freshness": "current", "provenance_verified": True, "value": "deny"},
        ]
        self.assertEqual(evaluate_external_trust_sources(sources)["outcome"], "INDETERMINATE")

    def test_independently_corroborated_sources_are_valid_counter_case(self):
        sources = [
            {"id": "registry-a", "integrity": "verified", "freshness": "current", "provenance_verified": True, "value": "issuer-authorized"},
            {"id": "registry-b", "integrity": "verified", "freshness": "current", "provenance_verified": True, "value": "issuer-authorized"},
        ]
        result = evaluate_external_trust_sources(sources, corroboration_required=True)
        self.assertEqual(result["outcome"], "PASS")

    def test_single_source_when_corroboration_required_is_indeterminate(self):
        source = {"id": "registry-a", "integrity": "verified", "freshness": "current", "provenance_verified": True, "value": "issuer-authorized"}
        self.assertEqual(
            evaluate_external_trust_sources([source], corroboration_required=True)["outcome"],
            "INDETERMINATE",
        )


if __name__ == "__main__":
    unittest.main()
