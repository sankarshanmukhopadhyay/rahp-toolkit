from __future__ import annotations

import importlib.util
import pathlib
import unittest


MODULE_PATH = pathlib.Path(__file__).resolve().parents[1] / "tools" / "portfolio_materiality_journal.py"
SPEC = importlib.util.spec_from_file_location("portfolio_materiality_journal", MODULE_PATH)
assert SPEC and SPEC.loader
journal = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(journal)


class PortfolioMaterialityJournalTests(unittest.TestCase):
    def setUp(self) -> None:
        self.key = "dtg:portfolio:combined:credential-status-lifecycle"
        self.owner = (
            "<!-- rahp-assessment-key:dtg:portfolio:combined:credential-status-lifecycle -->\n"
            "<!-- dtg-routing-cluster:aaa111 -->\n"
        )

    def event(self, digest: str, finding: str = "f-1", day: str = "2026-09-17") -> dict:
        return {
            "assessment_key": self.key,
            "observed_at": day,
            "affected_reviews": ["rahp", "security", "combined"],
            "body": (
                f"<!-- dtg-routing-cluster:{digest} -->\n"
                "## Routed findings\n\n"
                "| Finding | Repository | Change |\n"
                "|---|---|---|\n"
                f"| `{finding}` | `example/repo` | material change |\n"
            ),
        }

    def test_identical_material_set_is_preserved(self) -> None:
        impact, basis = journal.evidence_impact(self.owner, self.event("aaa111")["body"])
        self.assertEqual("preserved", impact)
        self.assertIn("identical", basis)

    def test_changed_material_set_fails_closed(self) -> None:
        impact, basis = journal.evidence_impact(self.owner, self.event("bbb222", "f-2")["body"])
        self.assertEqual("uncertain", impact)
        self.assertIn("differs", basis)

    def test_journal_contains_actual_finding(self) -> None:
        event = self.event("bbb222", "f-2")
        appendix = journal.journal_appendix(event, "closed", "uncertain", "changed material set")
        self.assertIn("`f-2`", appendix)
        self.assertIn("`example/repo`", appendix)
        self.assertIn("Evidence impact: **uncertain**", appendix)
        self.assertIn("Reassessment consequence", appendix)

    def test_marker_is_snapshot_and_digest_scoped(self) -> None:
        marker = journal.observation_marker(self.key, "2026-09-17", "bbb222")
        self.assertEqual(
            "<!-- rahp-materiality-journal:dtg:portfolio:combined:credential-status-lifecycle@2026-09-17:bbb222 -->",
            marker,
        )

    def test_prior_journal_digest_counts_as_preservation_evidence(self) -> None:
        owner = self.owner + "<!-- rahp-materiality-digest:bbb222 -->\n"
        impact, _ = journal.evidence_impact(owner, self.event("bbb222", "f-2")["body"])
        self.assertEqual("preserved", impact)


if __name__ == "__main__":
    unittest.main()
