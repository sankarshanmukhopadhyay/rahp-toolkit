import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from policy_assessment import review_subject, synthesize_assessment  # noqa: E402
from policy_structure import ingest_structured_policy  # noqa: E402


class PolicyReviewLineageTests(unittest.TestCase):
    def _subject(self, text):
        return ingest_structured_policy(
            text,
            source_uri="fixture://review-lineage.md",
            source_version="v1",
        )

    def test_rejected_proposition_does_not_enter_risk_analysis(self):
        subject = self._subject("We reserve the right to modify these terms at any time.")
        pid = subject["propositions"][0]["id"]
        review = review_subject(
            subject,
            [{"proposition_id": pid, "action": "reject", "reviewer": "human", "rationale": "Not an operative proposition in this context."}],
        )
        assessment = synthesize_assessment(subject, review=review)
        self.assertEqual([], assessment["reviewed_analysis"])
        self.assertEqual([], assessment["rahp_infers"]["hypotheses"])
        self.assertFalse(assessment["authority_boundary"]["rejected_propositions_enter_analysis"])

    def test_amended_text_is_the_text_consumed_by_risk_analysis(self):
        subject = self._subject("The service has a governance process.")
        pid = subject["propositions"][0]["id"]
        review = review_subject(
            subject,
            [{
                "proposition_id": pid,
                "action": "amend",
                "text": "We reserve the right to modify these terms at any time.",
                "reviewer": "human",
                "rationale": "Reviewer determined the operative proposition after examining surrounding policy context.",
            }],
        )
        assessment = synthesize_assessment(subject, review=review)
        self.assertEqual("amended", assessment["reviewed_analysis"][0]["review_state"])
        patterns = {item["risk_pattern"] for item in assessment["rahp_infers"]["hypotheses"]}
        self.assertIn("RKP-GOV-01", patterns)
        self.assertIn("RKP-GOV-03", patterns)

    def test_split_creates_independent_reviewed_children_with_source_lineage(self):
        subject = self._subject("We may suspend your account and share account information with service providers.")
        pid = subject["propositions"][0]["id"]
        review = review_subject(
            subject,
            [{
                "proposition_id": pid,
                "action": "split",
                "parts": [
                    "We may suspend your account.",
                    "We may share account information with service providers.",
                ],
                "reviewer": "human",
                "rationale": "The source contains two independently reviewable propositions.",
            }],
        )
        assessment = synthesize_assessment(subject, review=review)
        self.assertEqual(2, len(assessment["reviewed_analysis"]))
        self.assertTrue(all(item["source_proposition_ids"] == [pid] for item in assessment["reviewed_analysis"]))
        types = {item["type"] for item in assessment["reviewed_analysis"]}
        self.assertIn("termination", types)
        self.assertIn("disclosure", types)

    def test_merge_preserves_all_parent_propositions(self):
        subject = self._subject("We may use service providers.\n\nThose providers may act on our behalf.")
        ids = [item["id"] for item in subject["propositions"]]
        review = review_subject(
            subject,
            [{
                "action": "merge",
                "proposition_ids": ids,
                "text": "We may delegate activity to service providers acting on our behalf.",
                "reviewer": "human",
                "rationale": "The two clauses form one delegation proposition when read together.",
            }],
        )
        merged = [item for item in review["records"] if item["review_state"] == "merged"]
        self.assertEqual(1, len(merged))
        assessment = synthesize_assessment(subject, review=review)
        self.assertEqual(1, len(assessment["reviewed_analysis"]))
        self.assertEqual(ids, assessment["reviewed_analysis"][0]["source_proposition_ids"])
        self.assertEqual("merged", assessment["reviewed_analysis"][0]["review_state"])

    def test_split_and_merge_require_rationale(self):
        subject = self._subject("We may suspend accounts.\n\nYou may appeal.")
        ids = [item["id"] for item in subject["propositions"]]
        with self.assertRaisesRegex(ValueError, "split requires rationale"):
            review_subject(subject, [{"proposition_id": ids[0], "action": "split", "parts": ["A", "B"]}])
        with self.assertRaisesRegex(ValueError, "merge requires rationale"):
            review_subject(subject, [{"action": "merge", "proposition_ids": ids, "text": "Merged"}])


if __name__ == "__main__":
    unittest.main()
