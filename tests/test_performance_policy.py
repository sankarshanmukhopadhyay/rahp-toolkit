import tempfile
import unittest
from pathlib import Path

import yaml

from tools import compare_execution_benchmarks as benchmark_compare
from tools import validate as rahp_validate


class PerformancePolicyTests(unittest.TestCase):
    def sample(self, seconds=10.0, digest="a"):
        return {
            "contract": "rahp-execution-benchmark-v1",
            "profile": "core-validation",
            "profile_exit_code": 0,
            "wall_seconds": seconds,
            "semantic_reference_digests": {"x": digest},
        }

    def policy(self):
        return {
            "mode": "relative-baseline",
            "max_regression_percent": 20,
            "min_absolute_regression_seconds": 1.0,
            "require_same_contract": True,
            "require_same_profile": True,
            "require_semantic_reference_digest_match": True,
        }

    def test_small_noise_does_not_fail(self):
        result = benchmark_compare.compare(
            self.sample(10.0),
            self.sample(11.2),
            policy=self.policy(),
        )
        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["reason"], "within-policy")

    def test_meaningful_regression_fails(self):
        result = benchmark_compare.compare(
            self.sample(10.0),
            self.sample(13.0),
            policy=self.policy(),
        )
        self.assertEqual(result["status"], "fail")
        self.assertEqual(result["reason"], "meaningful-performance-regression")

    def test_semantic_digest_change_is_hard_failure(self):
        result = benchmark_compare.compare(
            self.sample(10.0, "a"),
            self.sample(9.0, "b"),
            policy=self.policy(),
        )
        self.assertEqual(result["status"], "fail")
        self.assertEqual(result["reason"], "semantic-reference-digest-mismatch")

    def test_profile_mismatch_is_incomparable(self):
        candidate = self.sample()
        candidate["profile"] = "full-validation"
        result = benchmark_compare.compare(
            self.sample(),
            candidate,
            policy=self.policy(),
        )
        self.assertEqual(result["status"], "incomparable")
        self.assertEqual(result["reason"], "profile-mismatch")

    def test_policy_loads_from_versioned_benchmark_contract(self):
        contract = {
            "regression_policy": {
                "mode": "relative-baseline",
                "max_regression_percent": 15,
                "min_absolute_regression_seconds": 0.5,
            }
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "benchmarks.yaml"
            path.write_text(yaml.safe_dump(contract), encoding="utf-8")
            policy = benchmark_compare.load_policy(path)
        self.assertEqual(policy["max_regression_percent"], 15)
        self.assertEqual(policy["min_absolute_regression_seconds"], 0.5)

    def test_validation_yaml_cache_eliminates_duplicate_parse(self):
        rahp_validate.load_yaml.cache_clear()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input.yaml"
            path.write_text("a: 1\n", encoding="utf-8")
            self.assertEqual(rahp_validate.load_yaml(path), {"a": 1})
            self.assertEqual(rahp_validate.load_yaml(path), {"a": 1})
            info = rahp_validate.load_yaml.cache_info()
        self.assertEqual(info.misses, 1)
        self.assertEqual(info.hits, 1)


if __name__ == "__main__":
    unittest.main()
