"""Regression coverage for DTG ZKP semantic requalification (#1147)."""
import copy
import pathlib
import sys
import unittest
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import validate_zkp_scenario_requalification as validator


class ZkpScenarioRequalificationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.corpus = yaml.safe_load((ROOT / "corpora" / "dtg-zkp.yaml").read_text())
        cls.review = yaml.safe_load(
            (ROOT / "corpora" / "reviews" / "dtg-zkp-semantic-requalification-2026-10-25.yaml").read_text()
        )

    def test_repository_record_is_complete(self):
        self.assertEqual(validator.validate(self.corpus, self.review), [])

    def test_missing_scenario_disposition_fails_closed(self):
        review = copy.deepcopy(self.review)
        review["dispositions"] = review["dispositions"][:-1]
        errors = validator.validate(self.corpus, review)
        self.assertTrue(any("exactly 30 dispositions" in e for e in errors))
        self.assertTrue(any("missing scenarios" in e for e in errors))

    def test_duplicate_scenario_disposition_is_rejected(self):
        review = copy.deepcopy(self.review)
        review["dispositions"][-1]["scenario_id"] = review["dispositions"][0]["scenario_id"]
        errors = validator.validate(self.corpus, review)
        self.assertTrue(any("duplicate scenario dispositions" in e for e in errors))

    def test_source_grounded_disposition_requires_evidence(self):
        review = copy.deepcopy(self.review)
        item = next(x for x in review["dispositions"] if x["disposition"] == "retain")
        item["source_evidence"] = []
        errors = validator.validate(self.corpus, review)
        self.assertTrue(any("requires source_evidence" in e for e in errors))

    def test_authority_pin_mismatch_is_rejected(self):
        review = copy.deepcopy(self.review)
        review["authority"]["commit"] = "b" * 40
        errors = validator.validate(self.corpus, review)
        self.assertTrue(any("authority commit does not match" in e for e in errors))

    def test_mixed_grounding_cannot_silently_claim_corpus_grade(self):
        corpus = copy.deepcopy(self.corpus)
        corpus["corpus"]["evidence_grade"] = "source-pinned"
        errors = validator.validate(corpus, self.review)
        self.assertTrue(any("must not declare a corpus-wide evidence_grade" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
