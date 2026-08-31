from __future__ import annotations

import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CORPUS_PATH = ROOT / "corpora/trust-tasks-credspec-composed.yaml"
PROFILE_PATH = ROOT / "examples/cross-spec/trust-tasks-credspec/authority-outcome-seam-candidate.yaml"


class AuthorityOutcomeSeamCandidateTests(unittest.TestCase):
    """Regression contract for the candidate seam derived from RAHP issue #337."""

    @staticmethod
    def load_yaml(path: Path) -> dict:
        return yaml.safe_load(path.read_text(encoding="utf-8"))

    def setUp(self) -> None:
        self.corpus = self.load_yaml(CORPUS_PATH)["corpus"]
        self.profile = self.load_yaml(PROFILE_PATH)["candidate_profile"]

    def test_candidate_covers_the_entire_xsp_corpus(self) -> None:
        corpus_ids = {scenario["id"] for scenario in self.corpus["scenarios"]}
        coverage_ids = set(self.profile["scenario_coverage"])
        self.assertEqual(corpus_ids, {f"XSP-{n:03d}" for n in range(1, 21)})
        self.assertEqual(coverage_ids, corpus_ids)

    def test_authority_and_outcome_are_bounded_tri_state_decisions(self) -> None:
        expected = {"confirmed", "contradicted", "unresolved"}
        self.assertEqual(set(self.profile["authority_decision"]["result_values"]), expected)
        self.assertEqual(set(self.profile["outcome_decision"]["result_values"]), expected)

        authority_invariants = " ".join(self.profile["authority_decision"]["invariants"]).lower()
        outcome_invariants = " ".join(self.profile["outcome_decision"]["invariants"]).lower()
        self.assertIn("must not imply execution", authority_invariants)
        self.assertIn("must remain distinct", outcome_invariants)
        self.assertIn("must not be treated as proof of completion", outcome_invariants)

    def test_missing_or_conflicting_evidence_cannot_silently_confirm_authority(self) -> None:
        semantics = self.profile["authority_decision"]["semantics"]
        self.assertIn("missing", semantics["unresolved"].lower())
        self.assertIn("conflicting", semantics["unresolved"].lower())
        invariants = " ".join(self.profile["authority_decision"]["invariants"]).lower()
        self.assertIn("missing evidence must not be treated as confirmed", invariants)
        self.assertIn("declared precedence rule", invariants)

    def test_privacy_and_redress_are_not_folded_into_authority(self) -> None:
        external = self.profile["external_obligations"]
        self.assertIn("privacy", external)
        self.assertIn("redress", external)
        self.assertIn("non_inference", external)

        coverage = self.profile["scenario_coverage"]
        for scenario_id in ("XSP-005", "XSP-006", "XSP-011", "XSP-018"):
            self.assertEqual(coverage[scenario_id]["primary_control"], "privacy")
            self.assertEqual(coverage[scenario_id]["authority_seam"], "out-of-scope")
        self.assertEqual(coverage["XSP-012"]["primary_control"], "redress")

    def test_f001_retest_gate_requires_action_time_lifecycle_closure(self) -> None:
        gate = self.profile["retest_gates"]["F-001"]
        self.assertEqual(gate["status"], "not-satisfied")
        requirements = " ".join(gate["close_only_if"]).lower()
        for concept in (
            "delegated-authority",
            "confirmed/contradicted/unresolved",
            "lifecycle",
            "precedence",
            "offline",
            "non-inference",
        ):
            self.assertIn(concept, requirements)

    def test_f002_retest_gate_requires_separate_outcome_and_evidence_closure(self) -> None:
        gate = self.profile["retest_gates"]["F-002"]
        self.assertEqual(gate["status"], "not-satisfied")
        requirements = " ".join(gate["close_only_if"]).lower()
        for concept in (
            "separate from action authority",
            "idempotent",
            "canonical decision",
            "unresolved",
            "side-effect",
            "input digests",
        ):
            self.assertIn(concept, requirements)

    def test_f003_is_deliberately_not_claimed_as_resolved(self) -> None:
        gate = self.profile["retest_gates"]["F-003"]
        self.assertEqual(gate["status"], "intentionally-not-resolved-by-this-candidate")


if __name__ == "__main__":
    unittest.main()
