"""Canonical combined worker must not invent findings from evidence digests."""
import sys
import unittest
from unittest.mock import patch
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import combined_review_worker as worker

IDS = [
    "0add1f4cc0f048ce6bfc", "29e39a0329123d8839a6",
    "a60eaffaf3cbc1394553", "acc9772126b1a3820240",
]


class CombinedReviewSourceTests(unittest.TestCase):
    def issue(self):
        return {
            "number": 272, "state": "open",
            "labels": [{"name": "judgment-required"}, {"name": "dtg-instance"}],
            "body": ("<!-- rahp-assessment-key:dtg:portfolio:combined:spec-dependency-alignment -->\n"
                     "Portfolio Monitor snapshot: `2026-11-16`\n"
                     + "\n".join("- `" + x + "`" for x in IDS)
                     + "\nSource commit: `" + "a"*40
                     + "`\nGroup digest: `" + "b"*64 + "`\n"),
        }

    def catalog(self):
        return {
            fid: {
                "finding_id": fid, "repository": "trustoverip/dtgwg-trust-tasks-tf",
                "title": "Trust Tasks dependency/specification delta",
                "severity": "high", "assurance_impact": "potentially-breaking",
                "kind": "material_change", "evidence_urls": [],
                "related_repositories": [],
            }
            for fid in IDS
        }

    def test_actual_four_member_packet_ignores_commit_and_group_digest(self):
        issue = self.issue()
        self.assertEqual(worker.finding_ids(issue["body"]), IDS)
        packet = worker.render_judgment_packet(issue, self.catalog())
        self.assertIn("Do any of the 4 changes jointly", packet)
        self.assertNotIn("nine changes", packet)
        for fid in IDS:
            self.assertIn(fid, packet)

    def test_synthetic_20_character_prefix_of_sha_is_not_a_finding(self):
        self.assertEqual(worker.finding_ids("commit:" + "a"*40), [])
        self.assertEqual(worker.finding_ids("digest:" + "f"*64), [])
        self.assertEqual(worker.finding_ids("prefix" + IDS[0] + "suffix"), [])
        self.assertEqual(worker.finding_ids("id=`" + IDS[0] + "`"), [IDS[0]])

    def test_missing_or_incomplete_source_never_mutates_issue(self):
        issue = self.issue()
        issue["labels"] = [{"name": worker.ASSESSMENT}]
        for body, catalog in (
            ("No qualified snapshot", self.catalog()),
            (issue["body"], {}),
        ):
            with self.subTest(body=body), patch.object(worker, "comments", return_value=[]), \
                    patch.object(worker, "fetch_monitor_findings", return_value=catalog), \
                    patch.object(worker, "api") as api:
                with self.assertRaises(ValueError):
                    worker.advance(dict(issue, body=body), "test")
                api.assert_not_called()

    def test_complete_source_allows_existing_transition(self):
        issue = self.issue()
        issue["labels"] = [{"name": worker.ASSESSMENT}]
        with patch.object(worker, "comments", return_value=[]), \
                patch.object(worker, "fetch_monitor_findings", return_value=self.catalog()), \
                patch.object(worker, "api") as api, \
                patch.object(worker, "ensure_label"), patch.object(worker, "remove_label"):
            worker.advance(issue, "test")
        self.assertEqual(api.call_count, 3)

    def test_forged_or_missing_source_member_fails_before_judgment(self):
        issue = self.issue()
        catalog = self.catalog()
        del catalog[IDS[2]]
        with self.assertRaisesRegex(ValueError, "missing routed finding"):
            worker.render_judgment_packet(issue, catalog)
        self.assertFalse(worker.is_combined({**issue, "labels": [{"name": "evidence-complete"}]}))


if __name__ == "__main__":
    unittest.main()
