from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "examples/cross-spec/trust-tasks-credspec/issue-690-realization-conformance-2026-09-29.yaml"


class Issue690EvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = yaml.safe_load(EVIDENCE.read_text())["reconciliation"]

    def test_pins(self):
        self.assertEqual(
            "863dba154a2a907380e4f2447ee9eedba481d64f",
            self.r["target_implementation"]["revision"],
        )

    def test_states_remain_separate(self):
        p = self.r["proposition_results"]
        self.assertEqual("partially-established", p["citation_identity"]["state"])
        self.assertEqual("partially-established", p["citation_digest_binding"]["state"])
        self.assertEqual("established", p["completion_non_inference"]["state"])
        self.assertEqual("not-implemented", p["outcome_evidence_binding"]["state"])
        self.assertEqual("indeterminate", p["privacy_unlinkability"]["state"])

    def test_terminal_posture_is_amber(self):
        self.assertEqual("AMBER", self.r["terminal_disposition"]["assurance_posture"])


if __name__ == "__main__":
    unittest.main()
