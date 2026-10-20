"""Executable regressions for witness role, identity and lifecycle assurance."""
import copy
import json
import unittest

from tools.validate_witness_semantics import MANIFEST, evaluate, verify

BASE = json.loads(MANIFEST.read_text())


class WitnessSemanticsTests(unittest.TestCase):
    def test_manifest_validates(self):
        self.assertEqual([], verify(BASE))

    def test_community_witness_is_not_rejected_for_affiliation_alone(self):
        case = {
            "witness_is_event_party": False,
            "witness_role": "community",
            "policy_requires_org_independence": False,
        }
        self.assertEqual("PASS", evaluate("WIT-ROLE-001", case))

    def test_party_witness_fails_and_missing_independence_evidence_is_indeterminate(self):
        self.assertEqual("FAIL", evaluate("WIT-ROLE-001", {"witness_is_event_party": True}))
        self.assertEqual(
            "INDETERMINATE",
            evaluate(
                "WIT-ROLE-002",
                {
                    "policy_requires_org_independence": True,
                    "self_asserted_independent": True,
                    "external_independence_evidence": False,
                },
            ),
        )

    def test_identity_continuity_requires_same_witness_when_required(self):
        self.assertEqual(
            "FAIL",
            evaluate(
                "WIT-ID-001",
                {
                    "continuity_required": True,
                    "vwc_issuer": "did:example:w1",
                    "session_recipient": "did:example:w1",
                    "response_signer": "did:example:w2",
                },
            ),
        )
        self.assertEqual(
            "INDETERMINATE",
            evaluate(
                "WIT-ID-001",
                {
                    "continuity_required": True,
                    "vwc_issuer": "did:example:w1",
                    "session_recipient": None,
                    "response_signer": "did:example:w1",
                },
            ),
        )

    def test_vrc_and_vwc_status_do_not_cascade(self):
        n1 = {
            "vrc_at_witnessing": "valid",
            "vrc_current": "revoked",
            "vwc_current": "valid",
            "cascade_applied": False,
        }
        n2 = {
            "vrc_at_witnessing": "valid",
            "vrc_current": "valid",
            "vwc_current": "revoked",
            "cascade_applied": False,
        }
        self.assertEqual("PASS", evaluate("WIT-TIME-001", n1))
        self.assertEqual("PASS", evaluate("WIT-TIME-001", n2))
        n1["cascade_applied"] = True
        self.assertEqual("FAIL", evaluate("WIT-TIME-001", n1))

    def test_unavailable_status_and_unknown_compromise_time_stay_indeterminate(self):
        self.assertEqual(
            "INDETERMINATE",
            evaluate("WIT-AVAIL-001", {"status_evidence": "unavailable", "witness_state": "temporary-outage"}),
        )
        self.assertEqual(
            "INDETERMINATE",
            evaluate(
                "WIT-KEY-001",
                {
                    "key_authorized_at_issuance": True,
                    "compromise_discovered_later": True,
                    "compromise_onset": "unknown",
                },
            ),
        )

    def test_successor_hosting_does_not_grant_mutation_authority(self):
        self.assertEqual(
            "PASS",
            evaluate(
                "WIT-SUCC-001",
                {
                    "successor_hosts_frozen_evidence": True,
                    "successor_mutates_status": False,
                    "mutation_authority": "none",
                },
            ),
        )
        self.assertEqual(
            "FAIL",
            evaluate(
                "WIT-SUCC-001",
                {
                    "successor_hosts_frozen_evidence": True,
                    "successor_mutates_status": True,
                    "mutation_authority": "none",
                },
            ),
        )

    def test_digest_does_not_reconstruct_discarded_presentation(self):
        self.assertEqual(
            "FAIL",
            evaluate(
                "WIT-RET-001",
                {
                    "original_presentation_retained": False,
                    "digest_retained": True,
                    "claims_original_reconstructible": True,
                },
            ),
        )

    def test_manifest_rejects_semantic_equivalence_and_overclaim(self):
        altered = copy.deepcopy(BASE)
        altered["strategy_comparison"]["assurance_equivalent"] = True
        self.assertTrue(any("assurance-equivalent" in item for item in verify(altered)))
        altered = copy.deepcopy(BASE)
        altered["evidence_state"] = "runtime-conformant"
        self.assertTrue(any("overclaim" in item for item in verify(altered)))


if __name__ == "__main__":
    unittest.main()
