from __future__ import annotations

import importlib.util
from io import BytesIO
from pathlib import Path
import unittest
from unittest.mock import patch
import urllib.error

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

    def test_api_errors_never_expose_response_body(self) -> None:
        secret_body = b'{"message":"private request detail"}'
        error = urllib.error.HTTPError(
            "https://api.github.com/repos/example/private",
            422,
            "Unprocessable Entity",
            {"X-GitHub-Request-Id": "request-123"},
            BytesIO(secret_body),
        )
        with patch.object(publisher.urllib.request, "urlopen", side_effect=error):
            with self.assertRaises(publisher.GitHubAPIError) as caught:
                publisher.request("POST", "https://api.github.com/repos/example/private", "token")
        self.assertNotIn("private request detail", str(caught.exception))
        self.assertNotIn(secret_body.decode(), str(caught.exception))
        self.assertIn("HTTP 422", str(caught.exception))
        self.assertEqual(caught.exception.request_id, "request-123")

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


    def test_existing_issue_scan_does_not_drop_owner_beyond_five_pages(self) -> None:
        calls: list[int] = []
        canonical = {
            "state": "closed",
            "number": 410,
            "body": "<!-- rahp-assessment-key:cawg:issue:decentralized-identity/cawg-identity-assertion#275 -->",
        }

        def fake_request(method, url, token, payload=None):
            page = int(url.rsplit("page=", 1)[1])
            calls.append(page)
            if page <= 5:
                return [{"number": page * 100 + i, "state": "closed", "body": ""} for i in range(100)]
            if page == 6:
                filler = [{"number": 600 + i, "state": "closed", "body": ""} for i in range(99)]
                return filler + [canonical]
            return []

        original = publisher.request
        publisher.request = fake_request
        try:
            issues = publisher.existing_issues("sankarshanmukhopadhyay/rahp-toolkit", "token")
        finally:
            publisher.request = original

        self.assertIn(canonical, issues)
        self.assertEqual(calls, [1, 2, 3, 4, 5, 6, 7])

        index = publisher.issues_by_key(issues)
        owner, state = publisher.resolve_owner(
            index,
            "cawg:issue:decentralized-identity/cawg-identity-assertion#275",
        )
        self.assertIsNotNone(owner)
        self.assertEqual(owner["number"], 410)
        self.assertEqual(state, "closed")

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
