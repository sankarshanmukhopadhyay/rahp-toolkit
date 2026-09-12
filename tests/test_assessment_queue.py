import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("publish_assessment_issues", ROOT / "tools" / "publish_assessment_issues.py")
MOD = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MOD
SPEC.loader.exec_module(MOD)


class AssessmentQueueTests(unittest.TestCase):
    def test_explicit_assessment_key_is_discovered(self):
        issue = {"body": "<!-- rahp-assessment-key:dtg:repository:example/repo -->\nbody"}
        self.assertEqual(MOD.infer_issue_keys(issue), {"dtg:repository:example/repo"})

    def test_legacy_dtg_marker_migrates_to_repository_key(self):
        issue = {"body": "<!-- rahp-dtg-change:example/repo@abc123 -->"}
        self.assertEqual(MOD.infer_issue_keys(issue), {"dtg:repository:example/repo"})

    def test_open_repository_assessment_can_absorb_issue_trigger(self):
        issues = [{
            "number": 1,
            "state": "open",
            "body": "<!-- rahp-dtg-change:example/repo@abc123 -->",
        }]
        index = MOD.issues_by_key(issues)
        owner, state = MOD.resolve_owner(index, "dtg:repository:example/repo")
        self.assertEqual(owner["number"], 1)
        self.assertEqual(state, "open")

    def test_trigger_marker_is_stable_for_same_observation(self):
        event = {"assessment_key": "dtg:issue:example/repo#7", "observed_at": "2026-08-16T00:00:00Z"}
        self.assertEqual(
            MOD.event_marker(event),
            "<!-- rahp-trigger:dtg:issue:example/repo#7@2026-08-16T00:00:00Z -->",
        )

    def test_canonical_rahp_repository_is_allowed(self):
        self.assertEqual(
            MOD.enforce_publication_repository(MOD.CANONICAL_RAHP_ISSUE_REPOSITORY),
            MOD.CANONICAL_RAHP_ISSUE_REPOSITORY,
        )

    def test_upstream_repository_is_rejected_as_publication_destination(self):
        with self.assertRaises(ValueError):
            MOD.enforce_publication_repository("OpenVTC/openvtc")


if __name__ == "__main__":
    unittest.main()
