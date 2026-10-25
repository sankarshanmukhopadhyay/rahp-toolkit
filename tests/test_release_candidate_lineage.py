import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import validate_release_candidate_lineage as lineage


class ReleaseCandidateLineageTests(unittest.TestCase):
    def test_release_metadata_changes_are_allowed(self):
        allowed = {
            "README.md",
            "method/release.yaml",
            "docs/releases/v2.9.0.md",
            "method/v2.9-release-qualification.yaml",
            "method/v2.9-release-evidence.json",
        }
        changed = [
            "README.md",
            "method/release.yaml",
            "docs/releases/v2.9.0.md",
        ]
        self.assertEqual(lineage.classify_changed_paths(changed, allowed), [])

    def test_post_candidate_code_change_is_rejected(self):
        allowed = {"README.md", "method/release.yaml"}
        changed = ["README.md", "tools/assurance.py"]
        self.assertEqual(
            lineage.classify_changed_paths(changed, allowed),
            ["tools/assurance.py"],
        )

    def test_post_candidate_test_change_is_rejected(self):
        allowed = {"README.md", "method/release.yaml"}
        changed = ["tests/test_release_workflow.py"]
        self.assertEqual(
            lineage.classify_changed_paths(changed, allowed),
            ["tests/test_release_workflow.py"],
        )

    def test_current_release_declares_expected_publication_metadata_paths(self):
        import yaml
        release_doc = yaml.safe_load((ROOT / "method/release.yaml").read_text())
        qualification_path = release_doc["release"]["qualification"]["manifest"]
        qualification = yaml.safe_load((ROOT / qualification_path).read_text())
        allowed = lineage.allowed_paths(release_doc, qualification)
        self.assertIn("method/release.yaml", allowed)
        self.assertIn(release_doc["release"]["notes"]["path"], allowed)
        self.assertIn(qualification_path, allowed)
        self.assertIn(qualification["evidence"]["release_evidence"], allowed)


if __name__ == "__main__":
    unittest.main()
