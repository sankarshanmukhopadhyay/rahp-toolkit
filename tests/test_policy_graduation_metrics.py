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
            "study": "rahp-policy-graduation-668",
            "reviewer_id": reviewer_id,
            "reviewer_class": reviewer_class,
            "candidate_implementation_sha": "0c29f9226a44bc3c0efbd0213a46d2c4b6fb66ce",
            "attestation": {"independent_of_other_reviewer": True,
                            "saw_other_review_before_completion": False,
                            "ai_assistance_used": False},
            "corpus_item_id": "fixture",
            "effort_minutes": 15,
            "proposition_reviews": [
                {"proposition_id": pid, "source_span_sha256": "b" * 64, "disposition": disposition, "materiality": materiality}
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

    def test_duplicate_reviewer_cannot_count_as_independent_pair(self):
        r = study_metrics([self._review("a"), self._review("a")])
        self.assertFalse(r["graduation_human_review_gate_satisfied"])
        self.assertEqual([], r["human_pair_comparisons"])

    def test_no_review_attestation_must_not_claim_human_gate(self):
        a, b = self._review("a"), self._review("b")
        del b["attestation"]
        r = study_metrics([a, b])
        self.assertFalse(r["graduation_human_review_gate_satisfied"])
        self.assertEqual(1, r["ineligible_declared_human_review_count"])

    def test_ai_assisted_or_previously_exposed_record_fails_gate(self):
        for field, value in (("ai_assistance_used", True),
                             ("saw_other_review_before_completion", True),
                             ("independent_of_other_reviewer", False)):
            with self.subTest(field=field):
                a, b = self._review("a"), self._review("b")
                b["attestation"][field] = value
                self.assertFalse(study_metrics([a, b])["graduation_human_review_gate_satisfied"])

    def test_different_frozen_candidate_cannot_count_as_pair(self):
        a, b = self._review("a"), self._review("b")
        b["candidate_implementation_sha"] = "a" * 40
        self.assertFalse(study_metrics([a, b])["graduation_human_review_gate_satisfied"])

    def test_no_shared_proposition_cannot_establish_agreement(self):
        a, b = self._review("a"), self._review("b", dispositions=[("other", "accept", "high")])
        self.assertFalse(study_metrics([a, b])["graduation_human_review_gate_satisfied"])

    def test_placeholder_or_empty_records_do_not_graduate(self):
        a, b = self._review("a"), self._review("b")
        for change in (lambda r: r.update(reviewer_id="REPLACE"),
                       lambda r: r.update(proposition_reviews=[]),
                       lambda r: r["proposition_reviews"].append(r["proposition_reviews"][0].copy())):
            with self.subTest(change=str(change)):
                v = dict(b)
                v["proposition_reviews"] = [dict(x) for x in b["proposition_reviews"]]
                change(v)
                self.assertFalse(study_metrics([a, v])["graduation_human_review_gate_satisfied"])

    def test_unpinned_source_span_or_wrong_study_is_not_accepted(self):
        a, b = self._review("a"), self._review("b")
        b["proposition_reviews"][0]["source_span_sha256"] = "REPLACE"
        self.assertFalse(study_metrics([a, b])["graduation_human_review_gate_satisfied"])
        b = self._review("b")
        b["study"] = "another-study"
        self.assertFalse(study_metrics([a, b])["graduation_human_review_gate_satisfied"])

    def test_two_wrong_but_matching_candidate_pins_do_not_pass(self):
        a, b = self._review("a"), self._review("b")
        a["candidate_implementation_sha"] = "a" * 40
        b["candidate_implementation_sha"] = "a" * 40
        self.assertFalse(study_metrics([a, b])["graduation_human_review_gate_satisfied"])

    def test_documentary_gate_is_not_authenticated_independence(self):
        result = study_metrics([self._review("a"), self._review("b")])
        self.assertTrue(result["graduation_human_review_gate_satisfied"])
        self.assertFalse(result["human_identity_and_independence_verified"])


if __name__ == "__main__":
    unittest.main()
