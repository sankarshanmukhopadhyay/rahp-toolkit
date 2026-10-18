"""Cross-process deterministic replay qualification for synthetic R1/R2/R3 consumer.

This exercises a fresh interpreter for each process. It does not authenticate
source material, prove evaluator independence or establish terminal assurance.
"""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def invoke(scenario: str) -> dict:
    output = subprocess.check_output(
        [sys.executable, "-m", "tools.reasoning_worked_example", "--scenario", scenario],
        cwd=ROOT,
        text=True,
        timeout=30,
    )
    return json.loads(output)


class CrossProcessReasoningReplayTests(unittest.TestCase):
    def test_fresh_process_baseline_is_deterministic(self):
        first = invoke("baseline")
        second = invoke("baseline")
        self.assertEqual(first, second)
        self.assertEqual("PASS", first["r1"]["outcome"])
        self.assertEqual("APPLICABLE", first["r2"]["disposition"])
        self.assertEqual("DECLARED_MATCH", first["r3"]["disposition"])
        self.assertNotIn("terminal_assurance", first)

    def test_missing_required_evidence_does_not_become_positive(self):
        first = invoke("missing")
        second = invoke("missing")
        self.assertEqual(first, second)
        self.assertEqual("INDETERMINATE", first["r1"]["outcome"])
        self.assertEqual("DECLARED_MATCH", first["r3"]["disposition"])
        self.assertNotIn("terminal_assurance", first)

    def test_later_discovered_record_does_not_rewrite_as_known_at(self):
        first = invoke("retroactive")
        second = invoke("retroactive")
        self.assertEqual(first, second)
        findings = first["r2"]["findings"]
        authority = next(f for f in findings if f["evidence_id"] == "authority-assertion")
        self.assertEqual(["REC-A"], authority["known_record_ids"])
        self.assertEqual(["REC-LATER"], authority["later_record_ids"])

    def test_declared_output_disagreement_remains_open_challenge(self):
        first = invoke("disagreement")
        second = invoke("disagreement")
        self.assertEqual(first, second)
        self.assertEqual("OUTPUT_DISAGREEMENT", first["r3"]["disposition"])
        self.assertEqual("OPEN", first["r3"]["challenges"][0]["status"])
        self.assertNotIn("terminal_assurance", first)

    def test_changed_declared_fixture_is_not_the_same_input_pin(self):
        baseline = invoke("baseline")
        missing = invoke("missing")
        bpin = baseline["r3"]["runs"][0]["input_pin"]["digest"]
        mpin = missing["r3"]["runs"][0]["input_pin"]["digest"]
        self.assertNotEqual(bpin, mpin)


if __name__ == "__main__":
    unittest.main()
