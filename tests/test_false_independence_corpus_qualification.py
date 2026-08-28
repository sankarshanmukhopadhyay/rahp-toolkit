from __future__ import annotations

import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]

CORPUS = {
    "SR-XSP-FI-001": "examples/cross-spec/false-independence-sybil/pressure-test.yaml",
    "SR-XSP-FI-002": "examples/cross-spec/false-governance-diversity/pressure-test.yaml",
    "SR-XSP-FI-003": "examples/cross-spec/trust-laundering/pressure-test.yaml",
    "SR-XSP-FI-004": "examples/cross-spec/false-social-independence-sock-puppetry/pressure-test.yaml",
    "SR-XSP-FI-005": "examples/cross-spec/quorum-capture/pressure-test.yaml",
    "SR-XSP-FI-006": "examples/cross-spec/collusion/pressure-test.yaml",
    "SR-XSP-FI-007": "examples/cross-spec/selective-evidence/pressure-test.yaml",
}

POSITIVE_CASE_MARKERS = (
    "legitimate",
    "genuine",
    "independent",
    "complete-relevant",
    "disclosed",
)

ADVERSARIAL_EFFECT_MARKERS = (
    "no-",
    "reject",
    "qualify",
    "preserve-source-ceiling",
    "deduplicate",
)


class FalseIndependenceCorpusQualificationTests(unittest.TestCase):
    """Corpus-level regression contract for the seven rows closed by issue #193."""

    @staticmethod
    def load(path: str) -> dict:
        return yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))["review"]

    def test_all_seven_reviews_exist_with_stable_identity(self) -> None:
        self.assertEqual(set(CORPUS), {f"SR-XSP-FI-{n:03d}" for n in range(1, 8)})
        seen_paths: set[str] = set()
        for expected_id, path in CORPUS.items():
            self.assertTrue((ROOT / path).is_file(), path)
            review = self.load(path)
            self.assertEqual(review["id"], expected_id)
            self.assertEqual(review["status"], "complete")
            self.assertEqual(review["target"]["source_paths"], [path])
            self.assertNotIn(path, seen_paths)
            seen_paths.add(path)

    def test_every_row_preserves_visible_judgment_and_amber_boundary(self) -> None:
        for review_id, path in CORPUS.items():
            with self.subTest(review=review_id):
                review = self.load(path)
                self.assertEqual(review["assurance"]["policy_gate"], "AMBER")
                self.assertEqual(review["assurance"]["residual_state"], "finding")
                judgment = review["judgment"]
                self.assertGreaterEqual(len(judgment["alternatives_considered"]), 2)
                self.assertTrue(judgment["chosen"].strip())
                self.assertTrue(judgment["residual_uncertainty"].strip())
                self.assertTrue(review["method"]["falsification_bias"].strip())

    def test_every_row_contains_adversarial_and_legitimate_counter_cases(self) -> None:
        for review_id, path in CORPUS.items():
            with self.subTest(review=review_id):
                cases = self.load(path)["modeled_cases"]
                self.assertGreaterEqual(len(cases), 5)
                names = [str(case.get("name", "")).lower() for case in cases]
                self.assertTrue(
                    any(any(marker in name for marker in POSITIVE_CASE_MARKERS) for name in names),
                    f"{review_id} must preserve a legitimate/genuine counter-case",
                )
                expected = [
                    " ".join(
                        str(case.get(key, "")).lower()
                        for key in ("expected_assurance_effect", "expected_disposition")
                    )
                    for case in cases
                ]
                self.assertTrue(
                    any(any(marker in outcome for marker in ADVERSARIAL_EFFECT_MARKERS) for outcome in expected),
                    f"{review_id} must preserve an adversarial no-uplift/rejection case",
                )

    def test_unknown_independence_or_completeness_never_silently_passes(self) -> None:
        for review_id, path in CORPUS.items():
            with self.subTest(review=review_id):
                cases = self.load(path)["modeled_cases"]
                unknown_cases = [
                    case
                    for case in cases
                    if "unknown" in str(case.get("name", "")).lower()
                    or any(str(value).lower() == "unknown" for value in case.values())
                ]
                self.assertTrue(unknown_cases, f"{review_id} needs an explicit uncertainty case")
                for case in unknown_cases:
                    outcome = " ".join(
                        str(case.get(key, "")).lower()
                        for key in ("expected_assurance_effect", "expected_disposition")
                    )
                    self.assertNotIn("pass", outcome)
                    self.assertNotIn("assured", outcome)
                    self.assertTrue(
                        any(marker in outcome for marker in ("indeterminate", "reduced-weight", "no-silent", "no-increase")),
                        f"{review_id} uncertainty must remain bounded rather than become assurance sufficiency",
                    )

    def test_corpus_level_rule_remains_evidence_conservative(self) -> None:
        propositions = " ".join(self.load(path)["proposition"].lower() for path in CORPUS.values())
        methods = " ".join(self.load(path)["method"]["rule"].lower() for path in CORPUS.values())
        combined = propositions + " " + methods
        for concept in ("multiplicity", "independence", "assurance", "evidence"):
            self.assertIn(concept, combined)
        self.assertIn("completeness", combined)
        self.assertIn("not", combined)


if __name__ == "__main__":
    unittest.main()
