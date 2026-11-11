"""Regression tests for the advisory issue queue audit."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from audit_issue_queue import inspect


def issue(number, labels=(), state="open", **extra):
    return {"number": number, "labels": [{"name": label} for label in labels], "state": state, **extra}


class IssueQueueAuditTest(unittest.TestCase):
    def test_never_promotes_open_unlabelled_issue_to_ready(self):
        result = inspect([issue(1)])
        self.assertEqual(result["authority"], "derived-advisory")
        self.assertEqual(result["findings"], [])
        self.assertNotIn("ready", result)

    def test_completed_assessment_can_remain_waiting(self):
        result = inspect([issue(2, ["assessment-complete", "state:waiting-external", "reassessment-pending-upstream"])])
        self.assertEqual(result["findings"], [])

    def test_closed_external_obligation_is_advisory_not_auto_closed(self):
        result = inspect([issue(3, ["state:waiting-external", "remediation-required"], state="closed")])
        self.assertEqual({f["code"] for f in result["findings"]},
                         {"CLOSED_WITH_ACTIVE_EXTERNAL_WAIT", "CLOSED_WITH_REMEDIATION_REQUIRED"})

    def test_upstream_evidence_without_wait_label_is_review_only(self):
        result = inspect([issue(4, ["dependency:upstream", "evidence-required"])])
        self.assertEqual(result["findings"][0]["code"], "EXTERNAL_DEPENDENCY_WITHOUT_WAIT_CLASS")

    def test_excludes_pull_requests(self):
        result = inspect([issue(5), issue(6, pull_request={"url": "https://example.invalid"})])
        self.assertEqual(result["issue_count"], 1)
        self.assertEqual(result["pull_requests_excluded"], 1)

    def test_open_state_with_closed_reason_is_flagged(self):
        result = inspect([issue(7, state_reason="completed")])
        self.assertEqual(result["findings"][0]["code"], "OPEN_WITH_CONFLICTING_CLOSED_REASON")


if __name__ == "__main__":
    unittest.main()
