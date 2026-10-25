"""Regression coverage for corpus claim-integrity invariants (#1144)."""
import copy
import pathlib
import sys
import unittest
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import corpus_claim_integrity as claim
import corpus_status


class CorpusClaimIntegrityTest(unittest.TestCase):
    def test_source_pinned_standalone_requires_immutable_pin(self):
        corpus = {"evidence_grade": "source-pinned", "source_commit": "archive-snapshot"}
        errors = claim.static_claim_errors(corpus, {"update_mode": "assisted"})
        self.assertTrue(any("immutable 40-character" in e for e in errors))

    def test_source_pinned_pending_review_is_rejected(self):
        corpus = {
            "evidence_grade": "source-pinned",
            "source_commit": "a" * 40,
            "provenance_status": "composition-review-pending",
        }
        errors = claim.static_claim_errors(corpus, {"update_mode": "assisted"})
        self.assertTrue(any("pending provenance" in e for e in errors))

    def test_source_pinned_mixed_grounding_is_rejected(self):
        corpus = {
            "evidence_grade": "source-pinned",
            "source_commit": "a" * 40,
            "provenance_status": "semantic-requalification-complete-mixed-grounding",
        }
        errors = claim.static_claim_errors(corpus, {"update_mode": "assisted"})
        self.assertTrue(any("mixed-grounding" in e for e in errors))

    def test_source_informed_pending_review_is_rejected(self):
        corpus = {
            "evidence_grade": "source-informed",
            "source_commit": "a" * 40,
            "provenance_status": "composition-review-pending",
        }
        errors = claim.static_claim_errors(corpus, {"update_mode": "derived"})
        self.assertTrue(any("pending provenance" in e for e in errors))

    def test_any_corpus_grade_is_rejected_for_mixed_grounding(self):
        corpus = {
            "evidence_grade": "source-informed",
            "source_commit": "a" * 40,
            "provenance_status": "semantic-requalification-complete-mixed-grounding",
        }
        errors = claim.static_claim_errors(corpus, {"update_mode": "assisted"})
        self.assertTrue(any("corpus-wide evidence grade" in e for e in errors))

    def test_source_informed_symbolic_baseline_is_not_promoted_or_blocked(self):
        corpus = {"evidence_grade": "source-informed", "source_commit": "interface-assumption-baseline"}
        self.assertEqual(claim.static_claim_errors(corpus, {"update_mode": "assisted"}), [])

    def test_valid_source_pinned_standalone_metadata_is_accepted(self):
        corpus = {"evidence_grade": "source-pinned", "source_commit": "a" * 40}
        self.assertEqual(claim.static_claim_errors(corpus, {"update_mode": "assisted"}), [])

    def test_derived_source_pinned_requires_immutable_dependency_pins(self):
        corpus = {
            "evidence_grade": "source-pinned",
            "depends_on": [{"corpus_id": "A", "source_commit": "archive-snapshot"}],
        }
        errors = claim.static_claim_errors(corpus, {"update_mode": "derived"})
        self.assertTrue(any("immutable dependency" in e for e in errors))

    def test_state_derivation_preserves_review_and_mixed_boundaries(self):
        self.assertEqual(
            claim.derive_claim_state({"provenance_status": "composition-review-pending"})["state"],
            "review-pending",
        )
        self.assertEqual(
            claim.derive_claim_state({"provenance_status": "semantic-requalification-complete-mixed-grounding"})["state"],
            "mixed-grounding",
        )
        self.assertEqual(
            claim.derive_claim_state({}, "CORPUS_REVIEW_REQUIRED")["state"],
            "reassessment-required",
        )

    def test_offline_declared_grade_does_not_claim_currentness(self):
        state = claim.derive_claim_state(
            {"evidence_grade": "source-informed"}, "PINNED_NOT_CHECKED"
        )
        self.assertEqual(state["state"], "declared-currentness-unchecked")

    def test_zkp_authority_and_portfolio_discovery_are_separate(self):
        import yaml
        sources = yaml.safe_load((ROOT / "corpora" / "sources.yaml").read_text())
        item = next(x for x in sources["sources"] if x["corpus_id"] == "CORPUS-DTG-ZKP")
        source = item["source"]
        corpus = yaml.safe_load((ROOT / "corpora" / "dtg-zkp.yaml").read_text())["corpus"]
        self.assertEqual(source["repository"], "trustoverip/dtgwg-zkp-spec")
        self.assertEqual(source["portfolio_repository"], "trustoverip/dtgwg-zkp-tf")
        self.assertEqual(source["relationship_to_portfolio"], "specification-authority-surface")
        self.assertEqual(source["authority_pin"], corpus["source_commit"])

    def test_corpus_status_marks_drift_as_reassessment_required(self):
        results = [{"corpus_id": "TEST", "status": "CORPUS_REVIEW_REQUIRED"}]
        byid = {"TEST": {"corpus_id": "TEST", "corpus_file": "corpora/test.yaml"}}
        corpus = {
            "id": "TEST",
            "evidence_grade": "source-informed",
            "source_commit": "a" * 40,
        }
        with patch.object(corpus_status, "corpus_record", return_value=corpus):
            out = corpus_status.annotate_claim_integrity(copy.deepcopy(results), byid)
        self.assertEqual(out[0]["claim_integrity"]["state"], "reassessment-required")


if __name__ == "__main__":
    unittest.main()
