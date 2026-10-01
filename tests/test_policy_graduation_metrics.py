import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from policy_graduation_metrics import compare_pair, study_metrics, summarize_review  # noqa: E402


class PolicyGraduationMetricsTests(unittest.TestCase):
    def _review(self, reviewer_id, reviewer_class="human-independent", dispositions=None):
        dispositions = dispositions or [("p1", "accept", "high"), ("p2", "amend", "medium"), ("p3", "reject", "low")]
        return {
            "schema": "rahp-policy-graduation-review/v1",
            "reviewer_id": reviewer_id,
            "reviewer_class": reviewer_class,
            "corpus_item_id": "fixture",
            "effort_minutes": 15,
            "proposition_reviews": [
                {"proposition_id": pid, "disposition": disposition, "materiality": materiality}
                for pid, disposition, materiality in dispositions
            ],
            "hypothesis_reviews": [],
            "work_queue_reviews": [],
        }

    def test_useful_and_reject_metrics_remain_separate(self):
        summary = summarize_review(self._review("a"))
        self.assertEqual(3, summary["proposition_count"])
        self.assertEqual(2, summary["useful_count"])
        self.assertEqual(1, summary["reject_count"])
        self.assertEqual(66.67, summary["useful_percent"])
        self.assertEqual(33.33, summary["reject_percent"])

    def test_pair_reports_high_materiality_agreement(self):
        a = self._review("a")
        b = self._review("b", dispositions=[("p1", "accept", "high"), ("p2", "reject", "medium"), ("p3", "reject", "low")])
        pair = compare_pair(a, b)
        self.assertEqual(3, pair["common_propositions"])
        self.assertEqual(100.0, pair["high_materiality_agreement_percent"])
        self.assertEqual(66.67, pair["disposition_agreement_percent"])

    def test_ai_rehearsal_does_not_satisfy_human_gate(self):
        result = study_metrics([
            self._review("ai-a", "ai-assisted-rehearsal"),
            self._review("ai-b", "ai-assisted-rehearsal"),
        ])
        self.assertFalse(result["graduation_human_review_gate_satisfied"])
        self.assertEqual(0, result["independent_human_reviewer_count"])
        self.assertEqual(2, result["ai_rehearsal_reviewer_count"])

    def test_two_humans_enable_pair_comparison(self):
        result = study_metrics([self._review("human-a"), self._review("human-b")])
        self.assertTrue(result["graduation_human_review_gate_satisfied"])
        self.assertEqual(1, len(result["human_pair_comparisons"]))


if __name__ == "__main__":
    unittest.main()
