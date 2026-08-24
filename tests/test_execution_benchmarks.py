import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


class ExecutionBenchmarkContractTests(unittest.TestCase):
    def setUp(self):
        self.doc = yaml.safe_load((ROOT / "method/execution-benchmarks.yaml").read_text())

    def test_contract_and_profiles_are_declared(self):
        self.assertEqual(self.doc["contract"], "rahp-execution-benchmark-v1")
        profiles = self.doc["profiles"]
        for required in [
            "core-validation",
            "corpus-validation",
            "cross-spec-dtg-tt-credspec",
            "full-validation",
        ]:
            self.assertIn(required, profiles)
            self.assertTrue(profiles[required]["commands"])

    def test_benchmark_profiles_do_not_publish_issues(self):
        forbidden = ["publish_assessment_issues.py", "gh issue", "create_issue"]
        for name, profile in self.doc["profiles"].items():
            joined = "\n".join(profile.get("commands") or []).lower()
            for token in forbidden:
                self.assertNotIn(token.lower(), joined, f"{name} must remain non-publishing")

    def test_semantic_invariant_is_explicit(self):
        comparison = self.doc["comparison"]
        self.assertIn("normalized outputs", comparison["semantic_invariant"])
        self.assertGreaterEqual(comparison["target_reduction_percent"]["full-validation"], 50)


if __name__ == "__main__":
    unittest.main()
