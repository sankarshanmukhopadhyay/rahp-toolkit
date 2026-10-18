"""Release-workflow Action references must be immutable and source-traceable."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PINNED = {
    "actions/checkout": "3d3c42e5aac5ba805825da76410c181273ba90b1",
    "actions/setup-python": "5fda3b95a4ea91299a34e894583c3862153e4b97",
    "actions/setup-node": "949feb2413d6458794dcd2491c4babbbce0c15c1",
}
WORKFLOWS = (
    ROOT / ".github/workflows/release.yml",
    ROOT / ".github/workflows/release-codename-policy.yml",
)
ACTION_RE = re.compile(r"^\s*-?\s*uses:\s*([^\s#]+)", re.M)


def pin_errors(workflow_text):
    errors = []
    for ref in ACTION_RE.findall(workflow_text):
        if ref.startswith("./") or ref.startswith("docker://"):
            continue
        if "@" not in ref:
            errors.append("unversioned external action: " + ref)
            continue
        name, revision = ref.rsplit("@", 1)
        if not re.fullmatch(r"[0-9a-f]{40}", revision):
            errors.append("un-pinned external action: " + ref)
        elif name in PINNED and revision != PINNED[name]:
            errors.append("unexpected release action revision: " + ref)
    return errors


class ReleaseActionPinsTest(unittest.TestCase):
    def test_release_related_workflows_have_verified_immutable_refs(self):
        for path in WORKFLOWS:
            self.assertEqual([], pin_errors(path.read_text()), str(path))

    def test_tag_reference_fails(self):
        self.assertIn(
            "un-pinned external action: actions/checkout@v7",
            pin_errors("steps:\n  - uses: actions/checkout@v7\n"),
        )

    def test_lookalike_revision_and_unknown_ref_fail(self):
        self.assertTrue(pin_errors("- uses: actions/setup-python@deadbeef\n"))
        self.assertTrue(pin_errors("- uses: actions/setup-python\n"))

    def test_local_action_remains_allowed(self):
        self.assertEqual([], pin_errors("- uses: ./.github/actions/local\n"))


if __name__ == "__main__":
    unittest.main()
