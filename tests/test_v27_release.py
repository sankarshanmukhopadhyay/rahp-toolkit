"""Release v2.7 qualification must fail closed until gates authorize promotion."""
import unittest
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from validate_v27_release import validate, GATES, EXPERIMENTAL


class V27QualificationTests(unittest.TestCase):
    def test_qualification_is_structurally_valid(self):
        self.assertEqual(validate(ROOT), [])

    def test_manifest_enforces_release_lifecycle(self):
        q = yaml.safe_load((ROOT / "method/v2.7-release-qualification.yaml").read_text())
        release = yaml.safe_load((ROOT / "method/release.yaml").read_text())["release"]
        self.assertEqual(set(q["release_gates"]), GATES)
        self.assertEqual(set(q["experimental_profiles"]), EXPERIMENTAL)
        self.assertEqual(release["tag"], "v2.7.0")
        if release["status"] == "candidate":
            self.assertEqual(q["state"], "PREQUALIFICATION")
            self.assertFalse(q["release_cut"]["publication_authorized"])
            self.assertTrue(all(value == "PENDING" for value in q["release_gates"].values()))
        else:
            self.assertEqual(release["status"], "released")
            self.assertEqual(release["qualification_status"], "qualified")
            self.assertEqual(q["state"], "QUALIFIED")
            self.assertTrue(q["release_cut"]["publication_authorized"])
            self.assertTrue(all(value == "PASS" for value in q["release_gates"].values()))
            self.assertRegex(q["release_cut"]["candidate_sha"], r"^[0-9a-f]{40}$")


if __name__ == "__main__":
    unittest.main()
