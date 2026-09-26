import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PROOF = ROOT / "examples/cawg-c2pa/post-v2.4-portability-proof.yaml"


class PostV24NonDtgPortabilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = yaml.safe_load(PROOF.read_text(encoding="utf-8"))

    def test_proof_uses_stable_generic_contracts(self):
        contracts = self.doc["stable_contracts"]
        self.assertEqual(contracts["engine"], "rahp-engine-contract-v1@1.3")
        self.assertEqual(contracts["normalized_result_schema"], 1)
        self.assertEqual(contracts["evidence_retention"], "rahp-evidence-retention-v1")
        self.assertEqual(self.doc["consumer"]["kind"], "non-dtg")

    def test_first_assessment_is_source_pinned_and_keeps_residuals(self):
        first = self.doc["first_assessment"]
        self.assertEqual(len(first["source"]["revision"]), 40)
        self.assertGreaterEqual(len(first["propositions"]), 2)
        self.assertTrue(first["residuals"])
        self.assertIn("not upstream conformance certification", first["claim_boundary"].lower())

    def test_material_change_reassessment_is_bounded(self):
        change = self.doc["material_change_reassessment"]
        self.assertEqual(len(change["previous_revision"]), 40)
        self.assertEqual(len(change["current_revision"]), 40)
        self.assertNotEqual(change["previous_revision"], change["current_revision"])
        self.assertEqual(change["disposition"], "no-material-assurance-impact")
        self.assertTrue(change["baseline_advanced"])
        selected = set(change["retest_scope"]["selected"])
        skipped = set(change["retest_scope"]["not_selected"])
        self.assertTrue(selected)
        self.assertTrue(skipped)
        self.assertTrue(selected.isdisjoint(skipped))

    def test_no_material_impact_is_not_universal_pass(self):
        serialized = yaml.safe_dump(self.doc["material_change_reassessment"]).upper()
        self.assertNotIn("UNIVERSAL PASS", serialized)
        self.assertNotEqual(
            self.doc["material_change_reassessment"]["disposition"].upper(),
            "PASS",
        )
        self.assertEqual(self.doc["current_posture"]["release_inference"], "none")

    def test_consumer_specific_material_stays_out_of_generic_core_contract(self):
        assertions = "\n".join(self.doc["portability_assertions"]).lower()
        self.assertIn("outside the portable core", assertions)
        # The portability proof itself is consumer-specific; stable contracts must not be.
        stable = yaml.safe_dump(self.doc["stable_contracts"]).lower()
        for token in ("cawg", "c2pa", "dtg", "openvtc"):
            self.assertNotIn(token, stable)


if __name__ == "__main__":
    unittest.main()
