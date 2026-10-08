"""Release publication guards for automatic qualified merges and manual recovery."""
import unittest
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]


class PublicationGuardTests(unittest.TestCase):
    def test_publication_is_scoped_to_main_release_changes(self):
        workflow = yaml.safe_load((ROOT / ".github/workflows/release.yml").read_text())
        # PyYAML 1.1 interprets the key 'on' as boolean True.
        triggers = workflow.get("on", workflow.get(True))
        self.assertIn("workflow_dispatch", triggers)
        self.assertIn("push", triggers)
        self.assertEqual(triggers["push"]["branches"], ["main"])
        paths = triggers["push"]["paths"]
        self.assertIn("method/release.yaml", paths)
        self.assertIn("PROJECT-STATUS.yaml", paths)
        self.assertIn("docs/releases/**", paths)
        self.assertNotIn("**", paths)

    def test_manual_confirmation_and_qualification_remain_mandatory(self):
        source = (ROOT / ".github/workflows/release.yml").read_text()
        for required in (
            "github.event_name == 'workflow_dispatch'",
            "github.event_name == 'push'",
            'if [ "$GITHUB_EVENT_NAME" = "workflow_dispatch" ]; then',
            'test "$CONFIRMATION" = PUBLISH',
            'test "$REQUESTED_TAG" = "$DECLARED_TAG"',
            'test "$RELEASE_STATUS" = released',
            'test "$QUALIFICATION_STATUS" = qualified',
            "python3 tools/release.py qualify",
            "python3 tools/verify_published_release.py preflight",
            "python3 tools/verify_published_release.py postflight",
        ):
            with self.subTest(required=required):
                self.assertIn(required, source)

    def test_publication_is_serialized_and_fail_closed(self):
        workflow = yaml.safe_load((ROOT / ".github/workflows/release.yml").read_text())
        self.assertFalse(workflow["concurrency"]["cancel-in-progress"])
        self.assertEqual(workflow["permissions"]["contents"], "write")
        self.assertEqual(workflow["jobs"]["publish"]["runs-on"], "ubuntu-latest")


if __name__ == "__main__":
    unittest.main()
