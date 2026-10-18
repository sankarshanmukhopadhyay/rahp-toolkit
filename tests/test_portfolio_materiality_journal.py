from __future__ import annotations

import importlib.util
import pathlib
import unittest


MODULE_PATH = pathlib.Path(__file__).resolve().parents[1] / "tools" / "materiality_journal_gate.py"
SPEC = importlib.util.spec_from_file_location("materiality_journal_gate", MODULE_PATH)
assert SPEC and SPEC.loader
gate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gate)


class MaterialityJournalGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.key = "dtg:portfolio:combined:credential-status-lifecycle"
        self.owner = {
            "state": "closed",
            "number": 636,
            "body": (
                f"<!-- rahp-assessment-key:{self.key} -->\n"
                "| Finding | Repository | Change |\n"
                "|---|---|---|\n"
                "| `f-1` | `example/repo` | original material change |\n"
            ),
        }

    def event(self, rows: list[tuple[str, str, str]]) -> dict:
        table = ["| Finding | Repository | Change |", "|---|---|---|"]
        for finding_id, repository, title in rows:
            table.append(f"| `{finding_id}` | `{repository}` | {title} |")
        return {
            "assessment_key": self.key,
            "observed_at": "2026-09-17",
            "affected_reviews": ["rahp", "security", "combined"],
            "body": "\n".join(table) + "\n",
        }

    def test_repeated_material_finding_is_preserved_and_does_not_reopen(self) -> None:
        enriched = gate.enrich_event(self.event([("f-1", "example/repo", "original material change")]), self.owner)
        self.assertEqual("preserved", enriched["evidence_impact"])
        self.assertNotIn("retest_reason", enriched)
        self.assertNotIn("reopen_closed_owner", enriched)
        self.assertIn("finding=f-1 @ example/repo", enriched["theme"])

    def test_new_material_finding_on_closed_owner_fails_closed(self) -> None:
        enriched = gate.enrich_event(
            self.event(
                [
                    ("f-1", "example/repo", "original material change"),
                    ("f-2", "example/repo", "new material change"),
                ]
            ),
            self.owner,
        )
        self.assertEqual("uncertain", enriched["evidence_impact"])
        self.assertTrue(enriched["reopen_closed_owner"])
        self.assertIn("finding=f-2 @ example/repo", enriched["retest_reason"])
        self.assertEqual(["f-1", "f-2"], [row["finding_id"] for row in enriched["journal_findings"]])

    def test_journaled_finding_is_not_reopened_again_after_reassessment_and_reclosure(self) -> None:
        journaled_owner = dict(self.owner)
        journaled_owner["body"] = self.owner["body"] + (
            "\n- Theme: `materiality-journal impact=uncertain; "
            "findings=finding=f-2 @ example/repo: new material change`\n"
        )
        enriched = gate.enrich_event(
            self.event(
                [
                    ("f-1", "example/repo", "original material change"),
                    ("f-2", "example/repo", "new material change"),
                ]
            ),
            journaled_owner,
        )
        self.assertEqual("preserved", enriched["evidence_impact"])
        self.assertNotIn("retest_reason", enriched)
        self.assertNotIn("reopen_closed_owner", enriched)

    def test_transferred_closed_wrapper_produces_bounded_idempotent_successor(self) -> None:
        owner = dict(self.owner)
        owner["body"] += "\n<!-- rahp-terminal-wrapper:transferred -->\n"
        event = self.event([
            ("f-1", "example/repo", "old claim"),
            ("f-2", "example/repo", "new material change"),
        ])
        event["related_assessment_key"] = self.key
        first = gate.enrich_event(dict(event), owner)
        second = gate.enrich_event(dict(event), owner)
        self.assertEqual(first["assessment_key"], second["assessment_key"])
        self.assertIn(f"{self.key}:successor:", first["assessment_key"])
        self.assertEqual(636, first["successor_of_terminal_issue"])
        self.assertNotIn("reopen_closed_owner", first)
        self.assertNotIn("retest_reason", first)
        self.assertNotIn("related_assessment_key", first)
        self.assertIn("finding", first["body"])
        self.assertIn("f-2", first["body"])
        self.assertNotIn("f-1", first["body"])
        self.assertIn("terminal dispositions or explicit durable transfers", first["body"])

    def test_transferred_wrapper_new_finding_set_gets_distinct_successor(self) -> None:
        owner = dict(self.owner)
        owner["body"] += "\n<!-- rahp-terminal-wrapper:transferred -->\n"
        a = gate.enrich_event(self.event([("f-2", "example/repo", "new a")]), owner)
        b = gate.enrich_event(self.event([("f-3", "example/repo", "new b")]), owner)
        self.assertNotEqual(a["assessment_key"], b["assessment_key"])

    def test_real_explicit_invalidation_still_reopens_terminal_wrapper(self) -> None:
        owner = dict(self.owner)
        owner["body"] += "\n<!-- rahp-terminal-wrapper:transferred -->\n"
        event = self.event([("f-2", "example/repo", "new material")])
        event["invalidation_reason"] = "direct negative evidence invalidates original terminal claim"
        enriched = gate.enrich_event(event, owner)
        self.assertTrue(enriched["reopen_closed_owner"])
        self.assertEqual(self.key, enriched["assessment_key"])

    def test_frozen_openvtc_wrapper_never_reopens_when_marker_missing(self):
        key = "dtg:portfolio:combined:openvtc-security-combined"
        event = self.event([("fresh", "example/repo", "breaking new sign-in")])
        event["assessment_key"] = key
        owner = {
            "state": "closed", "number": 121,
            "body": f"<!-- rahp-assessment-key:{key} -->",
        }
        enriched = gate.enrich_event(event, owner)
        self.assertEqual(121, enriched["successor_of_terminal_issue"])
        self.assertIn(":successor:", enriched["assessment_key"])
        self.assertNotIn("reopen_closed_owner", enriched)
        self.assertNotIn("retest_reason", enriched)

    def test_closed_data_room_wrapper_missing_from_index_still_gets_successor(self):
        key = "dtg:portfolio:combined:data-room-custody-lifecycle"
        event = self.event([("room-new", "OpenVTC/verifiable-trust-infrastructure", "new room revocation")])
        event["assessment_key"] = key
        enriched = gate.enrich_event(event, None)
        self.assertEqual(527, enriched["successor_of_terminal_issue"])
        self.assertIn("room-new", enriched["body"])
        self.assertNotIn("reopen_closed_owner", enriched)
        self.assertNotEqual(key, enriched["assessment_key"])

    def test_known_transferred_id_does_not_create_duplicate_successor(self):
        key = "dtg:portfolio:combined:openvtc-security-combined"
        event = self.event([
            ("aa28149c7babc678e9e7", "OpenVTC/verifiable-trust-infrastructure",
             "breaking wallet sign-in already transferred to #994")
        ])
        event["assessment_key"] = key
        enriched = gate.enrich_event(event, None)
        self.assertEqual(key, enriched["assessment_key"])
        self.assertEqual("preserved", enriched["evidence_impact"])
        self.assertNotIn("reopen_closed_owner", enriched)
        self.assertNotIn("successor_of_terminal_issue", enriched)

    def test_frozen_wrapper_explicit_invalidation_remains_fail_closed(self):
        key = "dtg:portfolio:combined:openvtc-security-combined"
        event = self.event([("fresh", "example/repo", "new contrary evidence")])
        event["assessment_key"] = key
        event["invalidation_reason"] = "negative evidence overturns original terminal conclusion"
        owner = {"state": "closed", "number": 121, "body": f"<!-- rahp-assessment-key:{key} -->"}
        enriched = gate.enrich_event(event, owner)
        self.assertTrue(enriched["reopen_closed_owner"])
        self.assertEqual(key, enriched["assessment_key"])

    def test_new_proposition_is_not_treated_as_reassessment(self) -> None:
        enriched = gate.enrich_event(self.event([("f-2", "example/repo", "first observation")]), None)
        self.assertEqual("new-proposition", enriched["evidence_impact"])
        self.assertNotIn("retest_reason", enriched)
        self.assertNotIn("reopen_closed_owner", enriched)

    def test_journal_summary_retains_finding_identity_repository_and_change(self) -> None:
        summary = gate.journal_summary(
            [{"finding_id": "f-2", "repository": "example/repo", "title": "new material change"}],
            "uncertain",
        )
        self.assertIn("impact=uncertain", summary)
        self.assertIn("finding=f-2 @ example/repo: new material change", summary)
        self.assertEqual({"f-2"}, gate.journaled_finding_ids(summary))


if __name__ == "__main__":
    unittest.main()
