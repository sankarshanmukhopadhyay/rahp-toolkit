"""Regression tests for a one-invocation, fail-closed release workflow."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from verify_published_release import preflight, postflight


TITLE = "RAHP Toolkit v2.7.0 — Common Rose"
TAG = "v2.7.0"
NOTES = "# RAHP Toolkit v2.7.0 — Common Rose\n\n**Status:** PUBLISHED / QUALIFIED\n"
OK = {"tagName": TAG, "name": TITLE, "body": NOTES, "isDraft": False, "isPrerelease": False}


class PublicationTests(unittest.TestCase):
    def test_published_notes_are_accepted(self):
        self.assertEqual(preflight(NOTES), [])

    def test_stale_candidate_notes_are_rejected(self):
        for value in (
            "# RAHP Toolkit v2.7.0 — Common Rose (candidate)\n",
            "# RAHP\n**Status: UNPUBLISHED / NOT QUALIFIED**\n",
            "# RAHP\n**Release date:** Pending qualification and publication\n",
        ):
            with self.subTest(value=value):
                self.assertTrue(preflight(value))

    def test_verified_published_release(self):
        self.assertEqual(postflight(OK, NOTES, TAG, TITLE, TAG), [])

    def test_reject_inconsistent_publication(self):
        for field, replacement in (
            ("tagName", "v2.6.0"),
            ("name", "Candidate"),
            ("body", "outdated candidate notes"),
            ("isDraft", True),
            ("isPrerelease", True),
        ):
            with self.subTest(field=field):
                broken = {**OK, field: replacement}
                self.assertTrue(postflight(broken, NOTES, TAG, TITLE, TAG))

    def test_reject_nonlatest(self):
        self.assertTrue(postflight(OK, NOTES, TAG, TITLE, "v2.6.0"))

    def test_reject_empty_notes(self):
        self.assertTrue(preflight(""))

    def test_workflow_preserves_auto_and_manual_paths(self):
        workflow = (ROOT / ".github/workflows/release.yml").read_text()
        self.assertIn("  push:\n    branches: [main]", workflow)
        self.assertIn("  workflow_dispatch:", workflow)
        self.assertIn("github.event_name == 'push'", workflow)
        self.assertIn("concurrency:", workflow)
        self.assertIn("verify_published_release.py preflight", workflow)
        self.assertIn("verify_published_release.py postflight", workflow)


if __name__ == "__main__":
    unittest.main()
