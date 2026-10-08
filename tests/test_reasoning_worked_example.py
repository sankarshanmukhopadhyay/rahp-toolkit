"""Conformance checks for the end-to-end R1-R3 consumer example."""
import unittest
from tools.reasoning_worked_example import run_scenario


class WorkedReasoningTests(unittest.TestCase):
    def test_baseline(self):
        result = run_scenario()
        self.assertEqual(result["r1"]["outcome"], "PASS")
        self.assertEqual(result["r2"]["disposition"], "APPLICABLE")
        self.assertEqual(result["r3"]["disposition"], "DECLARED_MATCH")
        self.assertEqual(result, run_scenario())

    def test_missing_evidence_blocks_structural_pass(self):
        result = run_scenario("missing")
        self.assertEqual(result["r1"]["outcome"], "INDETERMINATE")
        self.assertIn("MISSING", {f["status"] for f in result["r1"]["findings"]})
        self.assertEqual(result["r2"]["disposition"], "APPLICABLE")
        self.assertEqual(result["r3"]["disposition"], "DECLARED_MATCH")

    def test_later_discovered_retroactive_claim(self):
        result = run_scenario("retroactive")
        self.assertEqual(result["r2"]["disposition"], "APPLICABLE")
        finding = next(f for f in result["r2"]["findings"] if f["evidence_id"] == "authority-assertion")
        self.assertEqual(finding["later_record_ids"], ["REC-LATER"])
        self.assertEqual(finding["known_record_ids"], ["REC-A"])

    def test_disagreement_and_challenge(self):
        result = run_scenario("disagreement")
        self.assertEqual(result["r3"]["disposition"], "OUTPUT_DISAGREEMENT")
        self.assertEqual(result["r3"]["challenges"][0]["status"], "OPEN")
        self.assertEqual(result["r1"]["outcome"], "PASS")
        self.assertEqual(result["r2"]["disposition"], "APPLICABLE")

    def test_invalid_scenario(self):
        with self.assertRaises(ValueError):
            run_scenario("unknown")

    def test_no_terminal_assurance_claim(self):
        for scenario in ("baseline", "missing", "retroactive", "disagreement"):
            result = run_scenario(scenario)
            self.assertNotIn("terminal_assurance", result)
            self.assertIn("no terminal RAHP assurance", result["assurance_note"])


if __name__ == "__main__":
    unittest.main()
