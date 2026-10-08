"""Regression tests for the historical non-publishing v2.7 candidate boundary."""
import unittest
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from validate_v27_candidate import validate, REQUIRED_GATES


class CandidateQualificationTests(unittest.TestCase):
    def test_manifest_is_structurally_valid_without_claiming_release(self):
        self.assertEqual(validate(ROOT), [])

    def test_all_mandatory_gates_are_declared(self):
        self.assertEqual(len(REQUIRED_GATES), 7)

    def test_historical_candidate_remains_non_publishing_after_promotion(self):
        manifest = yaml.safe_load((ROOT / "method/v2.7-release-candidate.yaml").read_text())
        release = yaml.safe_load((ROOT / "method/release.yaml").read_text())
        self.assertEqual(manifest["candidate"]["status"], "prequalification")
        self.assertFalse(manifest["candidate"]["publication_authorized"])
        self.assertIsNone(manifest["candidate"]["release_sha"])
        self.assertEqual(manifest["candidate"]["codename"], "Common Rose")
        self.assertEqual(release["release"]["tag"], "v2.7.0")
        self.assertIn(release["release"]["status"], {"candidate", "released"})
        if release["release"]["status"] == "released":
            self.assertEqual(release["release"]["qualification_status"], "qualified")


if __name__ == "__main__":
    unittest.main()
