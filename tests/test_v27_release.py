"""Release v2.7 qualification fails closed on missing gates and premature promotion."""
import unittest
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from validate_v27_release import validate, GATES, EXPERIMENTAL


class V27QualificationTests(unittest.TestCase):
    def test_prequalification_is_structurally_valid(self):
        self.assertEqual(validate(ROOT), [])

    def test_unqualified_manifest_does_not_authorize_publication(self):
        q = yaml.safe_load((ROOT / "method/v2.7-release-qualification.yaml").read_text())
        self.assertEqual(q["state"], "PREQUALIFICATION")
        self.assertFalse(q["release_cut"]["publication_authorized"])
        self.assertEqual(set(q["release_gates"]), GATES)
        self.assertEqual(set(q["experimental_profiles"]), EXPERIMENTAL)
        self.assertTrue(all(value == "PENDING" for value in q["release_gates"].values()))

    def test_current_stable_release_remains_unchanged(self):
        release = yaml.safe_load((ROOT / "method/release.yaml").read_text())
        self.assertEqual(release["release"]["tag"], "v2.7.0")
        self.assertEqual(release["release"]["status"], "candidate")


if __name__ == "__main__":
    unittest.main()
