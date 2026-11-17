from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from dtg_portfolio_routing import combined_event, combined_source_evidence

SHA = "a" * 40


def item(fid, repo="OpenVTC/verifiable-trust-infrastructure", urls=None):
    return {"finding": {"finding_id": fid, "repository": repo,
                        "title": fid, "evidence_urls": urls or []}}


class CombinedSourceEvidenceTests(unittest.TestCase):
    def test_exact_commit_source_is_pinned_and_release_tag_remains_unanchored(self):
        rows = [item("item-1", urls=[
            "https://github.com/OpenVTC/verifiable-trust-infrastructure/commit/" + SHA,
            "https://github.com/OpenVTC/verifiable-trust-infrastructure/pull/2439"]),
            item("item-2", urls=[
                "https://github.com/OpenVTC/verifiable-trust-infrastructure/releases/tag/v1.0.0"])]
        event = combined_event("source-scope", rows, "2026-11-16")
        self.assertEqual(event["assessment_key"], "dtg:portfolio:combined:source-scope")
        self.assertEqual(event["unanchored_finding_ids"], ["item-2"])
        self.assertEqual(event["source_pins"], [
            {"repository": "OpenVTC/verifiable-trust-infrastructure", "revision": SHA}])
        self.assertIn("item-1", event["body"])
        self.assertIn("item-2", event["body"])

    def test_cross_repository_commit_cannot_pin_changed_artifact(self):
        rows = [item("source-id", urls=[
            "https://github.com/other/other/commit/" + SHA])]
        data = combined_source_evidence(rows)
        self.assertEqual(data["source_pins"], [])
        self.assertEqual(data["unanchored_finding_ids"], ["source-id"])

    def test_source_order_does_not_change_machine_readable_identity(self):
        rows = [item("b"), item("a", urls=[
            "https://github.com/OpenVTC/verifiable-trust-infrastructure/commit/" + SHA])]
        self.assertEqual(combined_source_evidence(rows),
                         combined_source_evidence(list(reversed(rows))))

    def test_duplicate_findings_and_invalid_evidence_fail_closed(self):
        rows = [item("duplicate"), item("duplicate")]
        with self.assertRaisesRegex(ValueError, "duplicate"):
            combined_source_evidence(rows)
        invalid = item("invalid")
        invalid["finding"]["evidence_urls"] = "not-array"
        with self.assertRaisesRegex(ValueError, "array"):
            combined_source_evidence([invalid])
        invalid["finding"]["evidence_urls"] = [None]
        with self.assertRaisesRegex(ValueError, "string"):
            combined_source_evidence([invalid])

    def test_metadata_is_not_an_authority_transfer(self):
        event = combined_event("source-scope", [item("unresolved")], "2026-11-16")
        self.assertNotIn("responsible_owner", event)
        self.assertNotIn("transfer_authorized", event)
        self.assertEqual(event["source_observations"][0]["source_pin_status"],
                         "unresolved")


if __name__ == "__main__":
    unittest.main()
