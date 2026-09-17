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
