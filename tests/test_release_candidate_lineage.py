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

    def test_review_and_adoption_publication_paths_are_exact(self):
        expected = {
            "ADOPTION.md",
            "docs/adoption-guide.md",
            "docs/releases/index.md",
            "docs/review/review-readiness-baseline.md",
            "docs/review/reproduction.md",
            "docs/review/known-limitations.md",
            "method/review/claim-evidence-ledger.yaml",
        }
        allowed = lineage.allowed_paths({}, {})
        self.assertTrue(expected <= allowed)
        self.assertEqual(lineage.classify_changed_paths(sorted(expected), allowed), [])
        unexpected = [
            "docs/review/threat-model.md",
            "docs/review/security-pre-review.md",
            "method/review/false-assurance-challenges.yaml",
            "docs/how-rahp-works.md",
            "tests/test_release_candidate_lineage.py",
            "tools/validate_release_candidate_lineage.py",
        ]
        self.assertEqual(lineage.classify_changed_paths(unexpected, allowed), sorted(unexpected))

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
