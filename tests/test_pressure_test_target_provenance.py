import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import validate_pressure_tests as pressure_validation


class PressureTestTargetProvenanceTests(unittest.TestCase):
    def test_pinned_multi_repository_target_is_accepted(self):
        target = {
            "version": "Pinned component revisions",
            "commit": "a" * 40,
            "repositories": {
                "a": "example/a",
                "b": "example/b",
            },
            "commits": {
                "a": "a" * 40,
                "b": "b" * 40,
            },
        }
        self.assertEqual(
            pressure_validation.validate_target_provenance(target, "source-pinned", "fixture"),
            [],
        )

    def test_component_keys_must_match(self):
        target = {
            "version": "Pinned component revisions",
            "commit": "a" * 40,
            "repositories": {"a": "example/a", "b": "example/b"},
            "commits": {"a": "a" * 40},
        }
        errors = pressure_validation.validate_target_provenance(target, "source-pinned", "fixture")
        self.assertTrue(any("identical component keys" in e for e in errors))

    def test_component_commits_must_be_full_shas(self):
        target = {
            "version": "Pinned component revisions",
            "commit": "a" * 40,
            "repositories": {"a": "example/a"},
            "commits": {"a": "main"},
        }
        errors = pressure_validation.validate_target_provenance(target, "source-pinned", "fixture")
        self.assertTrue(any("full 40-character" in e for e in errors))

    def test_pinned_component_target_cannot_claim_current_main(self):
        target = {
            "version": "Credential current main × ZKP current main",
            "commit": "a" * 40,
            "repositories": {"a": "example/a"},
            "commits": {"a": "a" * 40},
        }
        errors = pressure_validation.validate_target_provenance(target, "source-pinned", "fixture")
        self.assertTrue(any("must not claim 'current main'" in e for e in errors))

    def test_aggregate_commit_must_be_one_of_component_pins(self):
        target = {
            "version": "Pinned component revisions",
            "commit": "c" * 40,
            "repositories": {"a": "example/a", "b": "example/b"},
            "commits": {"a": "a" * 40, "b": "b" * 40},
        }
        errors = pressure_validation.validate_target_provenance(target, "source-pinned", "fixture")
        self.assertTrue(any("must correspond to one recorded component commit" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
