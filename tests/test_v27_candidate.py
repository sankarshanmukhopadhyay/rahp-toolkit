"""Regression tests for the non-publishing v2.7 candidate qualification boundary."""
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from validate_v27_candidate import validate, REQUIRED_GATES


class CandidateQualificationTests(unittest.TestCase):
    def test_manifest_is_structurally_valid_without_claiming_release(self):
        self.assertEqual(validate(ROOT), [])

    def test_all_mandatory_gates_are_declared(self):
        self.assertEqual(len(REQUIRED_GATES), 7)

    def test_unqualified_candidate_does_not_modify_current_release(self):
        import yaml
        manifest = yaml.safe_load((ROOT / "method/v2.7-release-candidate.yaml").read_text())
        release = yaml.safe_load((ROOT / "method/release.yaml").read_text())
        self.assertFalse(manifest["candidate"]["publication_authorized"])
        self.assertEqual(manifest["candidate"]["codename"], "Common Rose")
        self.assertEqual(release["release"]["tag"], "v2.7.0")\n        self.assertEqual(release["release"]["status"], "candidate")


if __name__ == "__main__":
    unittest.main()
