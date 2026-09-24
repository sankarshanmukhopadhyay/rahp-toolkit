import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from policy_assessment import (  # noqa: E402
    evidence_work_queue,
    reconcile_evidence_obligations,
    render_markdown,
    review_subject,
    synthesize_assessment,
)
from policy_subject import ingest_policy, map_risk_hypotheses  # noqa: E402


class PolicyAssessmentResearchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = ROOT / "examples" / "policy-assurance" / "platform-terms-v1.md"
        cls.subject = ingest_policy(
            path.read_text(encoding="utf-8"),
            source_uri="fixture://platform-terms-v1.md",
            source_version="v1",
        )

    def test_ambiguous_machine_proposition_stays_at_review_boundary(self):
        review = review_subject(self.subject)
        records = {item["proposition_id"]: item for item in review["records"]}
        ambiguous = [p for p in self.subject["propositions"] if p["judgment_required"]]
        self.assertTrue(ambiguous)
        for proposition in ambiguous:
            record = records[proposition["id"]]
            self.assertEqual("judgment-required", record["review_state"])
            self.assertIsNone(record["reviewed_proposition"])
            self.assertEqual(proposition["normalized_proposition"], record["machine_proposal"])

    def test_human_amendment_preserves_machine_proposal_and_requires_rationale(self):
        proposition = self.subject["propositions"][0]
        review = review_subject(
            self.subject,
            [
                {
                    "proposition_id": proposition["id"],
                    "action": "amend",
                    "text": "The operator may suspend an account when it reasonably believes the terms were violated.",
                    "reviewer": "research-reviewer",
                    "rationale": "Make the actor explicit without changing the source span.",
                }
            ],
        )
        record = review["records"][0]
        self.assertEqual(proposition["normalized_proposition"], record["machine_proposal"])
        self.assertEqual("amended", record["review_state"])
        self.assertNotEqual(record["machine_proposal"], record["reviewed_proposition"])
        self.assertEqual("research-reviewer", record["reviewer"])

    def test_amend_without_rationale_is_rejected(self):
        proposition = self.subject["propositions"][0]
        with self.assertRaisesRegex(ValueError, "requires rationale"):
            review_subject(
                self.subject,
                [
                    {
                        "proposition_id": proposition["id"],
                        "action": "amend",
                        "text": "replacement",
                    }
                ],
            )

    def test_work_queue_routes_runtime_privacy_ux_and_human_judgment(self):
        mapping = map_risk_hypotheses(self.subject)
        queue = evidence_work_queue(self.subject, mapping)
        evidence_classes = {item["evidence_class"] for item in queue}
        routes = {item["route"] for item in queue}
        self.assertIn("runtime-observation", evidence_classes)
        self.assertIn("user-experience", evidence_classes)
        self.assertIn("human-judgment", evidence_classes)
        self.assertIn("DPIP-or-privacy-specialist", routes)
        self.assertIn("RAHP-assessment", routes)
        self.assertTrue(all(item.get("obligation_id") for item in queue))
        self.assertTrue(all(item.get("why_required") for item in queue))
        self.assertTrue(all(item.get("materiality") for item in queue))
        self.assertEqual(len(queue), len({item["obligation_id"] for item in queue}))

    def test_evidence_obligation_lifecycle_is_non_terminal_and_citable(self):
        mapping = map_risk_hypotheses(self.subject)
        queue = evidence_work_queue(self.subject, mapping)
        obligation = queue[0]
        lifecycle = reconcile_evidence_obligations(
            queue,
            [{
                "obligation_id": obligation["obligation_id"],
                "state": "CONTRADICTED",
                "evidence_refs": ["run://policy-obligation-001"],
                "rationale": "Observed behavior contradicts the reviewed policy proposition.",
            }],
        )
        reconciled = {item["obligation_id"]: item for item in lifecycle["obligations"]}[obligation["obligation_id"]]
        self.assertEqual("CONTRADICTED", reconciled["lifecycle_state"])
        self.assertEqual(["run://policy-obligation-001"], reconciled["evidence_refs"])
        self.assertFalse(lifecycle["terminal_assurance"])
        self.assertEqual("none-research-nonterminal", reconciled["terminal_effect"])

    def test_policy_change_supersedes_obligations_for_changed_source_proposition(self):
        old = ingest_policy("We retain records for seven years.", source_uri="fixture://retention", source_version="v1")
        new = ingest_policy("We retain records for ten years.", source_uri="fixture://retention", source_version="v2")
        mapping = map_risk_hypotheses(old)
        queue = evidence_work_queue(old, mapping)
        from policy_subject import diff_subjects
        lifecycle = reconcile_evidence_obligations(queue, policy_delta=diff_subjects(old, new))
        self.assertTrue(lifecycle["policy_reassessment_required"])
        self.assertTrue(any(item["lifecycle_state"] == "SUPERSEDED" for item in lifecycle["obligations"]))

    def test_evaluated_obligation_requires_rationale(self):
        mapping = map_risk_hypotheses(self.subject)
        queue = evidence_work_queue(self.subject, mapping)
        with self.assertRaisesRegex(ValueError, "requires rationale"):
            reconcile_evidence_obligations(
                queue,
                [{
                    "obligation_id": queue[0]["obligation_id"],
                    "state": "SATISFIED",
                    "evidence_refs": ["run://evidence"],
                }],
            )

    def test_synthesis_is_explicitly_non_terminal_and_cold_reader_friendly(self):
        assessment = synthesize_assessment(self.subject)
        self.assertFalse(assessment["terminal_assurance"])
        self.assertEqual("JUDGMENT_REQUIRED", assessment["current_disposition"]["state"])
        self.assertGreater(assessment["current_disposition"]["evidence_item_count"], 0)
        markdown = render_markdown(assessment)
        self.assertIn("What the policy text establishes", markdown)
        self.assertIn("What RAHP infers", markdown)
        self.assertIn("what to investigate next", markdown)
        self.assertIn("Why required:", markdown)
        self.assertIn("Research output only", markdown)
        self.assertNotIn("policy score", markdown.lower())

    def test_explicit_review_moves_disposition_to_evidence_required(self):
        decisions = [
            {
                "proposition_id": proposition["id"],
                "action": "accept",
                "reviewer": "research-reviewer",
            }
            for proposition in self.subject["propositions"]
            if proposition["judgment_required"]
        ]
        review = review_subject(self.subject, decisions)
        assessment = synthesize_assessment(self.subject, review=review)
        self.assertEqual("EVIDENCE_REQUIRED", assessment["current_disposition"]["state"])
        self.assertFalse(assessment["terminal_assurance"])


if __name__ == "__main__":
    unittest.main()
