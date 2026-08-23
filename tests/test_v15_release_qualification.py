import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def semver_tuple(value: str):
    major, minor, patch = value.lstrip("v").split(".")
    return int(major), int(minor), int(patch)


class V15ReleaseQualificationTests(unittest.TestCase):
    def test_preserved_v15_manifest_identifies_release(self):
        manifest = yaml.safe_load((ROOT / "method/v1.5-release-qualification.yaml").read_text())
        self.assertEqual(manifest["release"], "v1.5.0")
        self.assertEqual(manifest["release_cut"]["tag"], "v1.5.0")

    def test_stable_compatibility_contracts_are_unchanged(self):
        status = yaml.safe_load((ROOT / "PROJECT-STATUS.yaml").read_text())
        self.assertEqual(status["compatibility"]["engine_contract"], "rahp-engine-contract-v1")
        self.assertEqual(status["compatibility"]["normalized_result_schema"], 1)
        self.assertEqual(status["compatibility"]["evidence_retention_contract"], "rahp-evidence-retention-v1")
        self.assertGreaterEqual(semver_tuple(status["stable_release"]), semver_tuple("1.5.0"))

    def test_purple_leaf_blue_release_record_is_preserved(self):
        notes = (ROOT / "docs/releases/v1.5.0.md").read_text()
        self.assertIn("Purple Leaf Blue", notes)
        self.assertIn("Amblypodia anita", notes)
        self.assertTrue((ROOT / "docs/releases/v1.5.0-preparation.md").is_file())

    def test_v15_portable_qualification_paths_still_exist(self):
        manifest = yaml.safe_load((ROOT / "method/v1.5-release-qualification.yaml").read_text())
        for rel in manifest["portable_paths"]:
            self.assertTrue((ROOT / rel).exists(), rel)


if __name__ == "__main__":
    unittest.main()
