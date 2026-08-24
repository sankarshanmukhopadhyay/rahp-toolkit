import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


class GenericReleaseWorkflowTests(unittest.TestCase):
    def test_current_declaration_points_to_permanent_workflow(self):
        doc = yaml.safe_load((ROOT / "method/release.yaml").read_text())
        self.assertEqual(doc["publication"]["workflow"], ".github/workflows/release.yml")
        self.assertTrue((ROOT / doc["publication"]["workflow"]).is_file())

    def test_workflow_contains_no_release_specific_identity(self):
        text = (ROOT / ".github/workflows/release.yml").read_text()
        for forbidden in ("v1.6.0", "Common Earl", "Tanaecia julii", "validate_v16_release.py"):
            self.assertNotIn(forbidden, text)
        self.assertIn("tools/release.py metadata", text)
        self.assertIn("tools/release.py qualify", text)
        self.assertIn("steps.release.outputs.tag", text)
        self.assertIn("steps.release.outputs.title", text)
        self.assertIn("steps.release.outputs.notes_path", text)

    def test_release_specific_publisher_is_retired(self):
        self.assertFalse((ROOT / ".github/workflows/publish-qualified-release.yml").exists())

    def test_v16_manifest_preserves_at_cut_publication_provenance(self):
        doc = yaml.safe_load((ROOT / "method/v1.6-release-qualification.yaml").read_text())
        cut = doc["release_cut"]
        self.assertEqual(cut["publication_workflow_at_cut"], ".github/workflows/publish-qualified-release.yml")
        self.assertEqual(cut["publication_workflow"], ".github/workflows/release.yml")


if __name__ == "__main__":
    unittest.main()
