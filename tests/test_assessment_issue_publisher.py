from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "publish_assessment_issues.py"
SPEC = importlib.util.spec_from_file_location("publish_assessment_issues", MODULE_PATH)
assert SPEC and SPEC.loader
publisher = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(publisher)


class AssessmentIssuePublisherTests(unittest.TestCase):
    def setUp(self) -> None:
        self.key = "dtg:portfolio:combined:delegation-credential-composition"
        self.issues = [
            {
                "state": "closed",
                "number": 584,
                "body": f"<!-- rahp-assessment-key:{self.key} -->",
            },
            {
                "state": "closed",
                "number": 611,
                "body": f"<!-- rahp-assessment-key:{self.key} -->",
            },
        ]

    def test_earliest_closed_owner_survives_duplicate_history(self) -> None:
        index = publisher.issues_by_key(self.issues)
        self.assertEqual(index["closed"][self.key]["number"], 584)

    def test_repeated_observation_resolves_to_closed_owner(self) -> None:
        index = publisher.issues_by_key(self.issues)
        owner, state = publisher.resolve_owner(index, self.key)
        self.assertIsNotNone(owner)
        self.assertEqual(owner["number"], 584)
        self.assertEqual(state, "closed")

    def test_closed_owner_does_not_reopen_without_explicit_trigger(self) -> None:
        event = {"assessment_key": self.key, "observed_at": "2026-09-11"}
        self.assertFalse(publisher.should_reopen_closed_owner(event))

    def test_closed_owner_reopens_only_on_governed_trigger(self) -> None:
        base = {"assessment_key": self.key, "observed_at": "2026-09-12"}
        self.assertTrue(
            publisher.should_reopen_closed_owner(
                {**base, "invalidation_reason": "authoritative semantic delta invalidates prior proposition evidence"}
            )
        )
        self.assertTrue(
            publisher.should_reopen_closed_owner(
                {**base, "retest_reason": "new negative evidence intersects prior terminal conclusion"}
            )
        )
        self.assertTrue(publisher.should_reopen_closed_owner({**base, "reopen_closed_owner": True}))

    def test_open_owner_is_preferred_when_both_states_exist(self) -> None:
        issues = self.issues + [
            {
                "state": "open",
                "number": 622,
                "body": f"<!-- rahp-assessment-key:{self.key} -->",
            }
        ]
        index = publisher.issues_by_key(issues)
        owner, state = publisher.resolve_owner(index, self.key)
        self.assertEqual(owner["number"], 622)
        self.assertEqual(state, "open")


if __name__ == "__main__":
    unittest.main()
