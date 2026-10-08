"""Fail closed if release publishing loses its explicit dispatch authorization."""
import unittest
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]


class PublicationGuardTests(unittest.TestCase):
    def test_publication_is_manual_only(self):
        workflow = yaml.safe_load((ROOT / ".github/workflows/release.yml").read_text())
        # PyYAML 1.1 interprets the key 'on' as boolean True.
        triggers = workflow.get("on", workflow.get(True))
        self.assertIn("workflow_dispatch", triggers)
        self.assertNotIn("push", triggers)

    def test_explicit_confirmation_and_qualification(self):
        source = (ROOT / ".github/workflows/release.yml").read_text()
        for required in (
            "github.event_name == 'workflow_dispatch'",
            'test "$CONFIRMATION" = PUBLISH',
            'test "$REQUESTED_TAG" = "$DECLARED_TAG"',
            'test "$RELEASE_STATUS" = released',
            'test "$QUALIFICATION_STATUS" = qualified',
            "python3 tools/release.py qualify",
        ):
            with self.subTest(required=required):
                self.assertIn(required, source)


if __name__ == "__main__":
    unittest.main()
