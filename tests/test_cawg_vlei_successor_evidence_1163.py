"""Contract checks for the source-level CAWG vLEI successor assessment.

The file explicitly does not claim executable CAWG/KERI conformance.
"""
import json
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
RECORD = ROOT / "instances/cawg/reviews/2026-10-identity-vlei-reassessment.result.json"


class CawgVleiSuccessorEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record = json.loads(RECORD.read_text(encoding="utf-8"))

    def test_revision_pins_and_divergence_are_explicit(self):
        source = self.record["source"]
        for key in ("previous_sha", "current_sha", "merge_base_sha"):
            self.assertRegex(source[key], r"^[0-9a-f]{40}$")
        self.assertEqual(source["comparison"], "diverged")
        self.assertNotEqual(source["previous_sha"], source["current_sha"])
        self.assertNotEqual(source["merge_base_sha"], source["current_sha"])

    def test_three_lenses_have_citable_outstanding_findings(self):
        modes = self.record["review_modes"]
        self.assertEqual(set(modes), {"rahp", "security", "combined"})
        self.assertEqual({x["id"] for x in modes["rahp"]["findings"]}, {"F-001", "F-002", "F-003"})
        self.assertTrue(modes["security"]["findings"])
        for name in ("rahp", "security"):
            for finding in modes[name]["findings"]:
                self.assertEqual(finding["disposition"], "retained-open")
                self.assertTrue(finding["basis"])
                self.assertTrue(finding["retest"])
        ids = {x["id"] for name in ("rahp", "security") for x in modes[name]["findings"]}
        self.assertLessEqual(set(modes["combined"]["links"]), ids)

    def test_scenarios_reused_without_fake_execution(self):
        self.assertEqual({x["id"] for x in self.record["scenarios"]}, {"CAWG-006", "CAWG-028", "CAWG-033", "CAWG-034"})
        self.assertTrue(all(x["status"] == "mapped-not-implemented" for x in self.record["scenarios"]))

    def test_closure_requires_actual_runtime_evidence(self):
        evidence = self.record["evidence"]
        for name in ("runtime_verification", "full_rahp_security_combined_engine_runs", "historical_signature_validation"):
            self.assertEqual(evidence[name], "not-executed")
        self.assertFalse(self.record["issue_1163_closure_eligible"])
        self.assertIn("runtime", self.record["status"])


if __name__ == "__main__":
    unittest.main()
