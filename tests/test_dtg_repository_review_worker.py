import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "dtg_repository_review_worker", ROOT / "tools" / "dtg_repository_review_worker.py"
)
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


class DtgRepositoryReviewWorkerTests(unittest.TestCase):
    def issue(self):
        return {
            "state": "open",
            "number": 9,
            "labels": [{"name": "assessment-required"}],
            "body": """<!-- rahp-dtg-gatherer-run:gha-123-1 -->
<!-- rahp-dtg-gatherer-event:aaaaaaaaaaaaaaaaaaaa -->
<!-- rahp-assessment-key:dtg:repository:OpenVTC/openvtc -->
<!-- rahp-dtg-change:OpenVTC/openvtc@1234567890abcdef -->
## Why review is required

- specification files changed

## Material files

| File | Status |
|---|---|
| `specs/x.md` | modified |

## Commits in the change window

- `1234567` feat: change semantics
""",
        }

    def test_accepts_gatherer_repository_assessment(self):
        self.assertTrue(MOD.is_repository_review(self.issue()))

    def test_rejects_old_portfolio_combined_shape(self):
        issue = self.issue()
        issue["body"] = "<!-- rahp-assessment-key:dtg:portfolio:combined:test -->"
        self.assertFalse(MOD.is_repository_review(issue))

    def test_requires_revision_provenance(self):
        issue = self.issue()
        issue["body"] = "<!-- rahp-assessment-key:dtg:repository:OpenVTC/openvtc -->"
        with self.assertRaises(ValueError):
            MOD.provenance(issue["body"])

    def test_packet_asks_explicit_dpip_question_and_terminal_path(self):
        packet = MOD.render_packet(self.issue())
        self.assertIn("warrants a DPIP referral", packet)
        self.assertIn("specs/x.md", packet)
        self.assertIn("assurance:dpip-not-required", packet)
        self.assertIn("assurance:dpip-requested", packet)
        self.assertIn("missing applicability decision", packet)

    def test_lineage_is_visible_in_judgment_packet(self):
        packet = MOD.render_packet(self.issue())
        self.assertIn("gha-123-1", packet)
        self.assertIn("aaaaaaaaaaaaaaaaaaaa", packet)


if __name__ == "__main__":
    unittest.main()
