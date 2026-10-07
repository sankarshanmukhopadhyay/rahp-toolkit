"""Counterexamples for the opt-in evidence-bound sociotechnical profile."""
from copy import deepcopy
import json
from pathlib import Path
import unittest

import yaml

from tools.assurance_record import canonical_record, markdown
from tools.sociotechnical_assurance import build_record, digest, evaluate, replay, validate_input

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "examples/sociotechnical-assurance"


def case(prefix):
    return json.loads(next(CORPUS.glob(prefix + "-*.json")).read_text(encoding="utf-8"))


class SociotechnicalAssuranceTests(unittest.TestCase):
    def test_frozen_corpus_expected_outcomes(self):
        report = replay(CORPUS / "corpus.json")
        self.assertEqual(len(report["cases"]), 8)
        self.assertEqual(report["independent_human_review"], "pending")

    def test_correct_technical_control_cannot_hide_compelled_disclosure(self):
        result = evaluate(case("A"))
        self.assertEqual([r["outcome"] for r in result["results"]], ["PASS", "FAIL"])
        self.assertFalse(result["deployment_approval"])

    def test_policy_assertion_does_not_establish_runtime_choice(self):
        value = case("B")
        self.assertEqual(evaluate(value)["outcome"], "INDETERMINATE")
        self.assertIn("wrong-evidence-class", evaluate(value)["results"][1]["rejected_evidence"][0]["reasons"])

    def test_correlated_positive_sources_cannot_outvote_refutation(self):
        result = evaluate(case("C"))
        self.assertEqual(result["outcome"], "FAIL")
        row = result["results"][0]
        self.assertEqual(row["dependence_groups"], [["review-a", "review-b"]])
        self.assertIn("C-contradiction", row["admitted_evidence"])

    def test_duplicate_support_without_refutation_still_not_independent(self):
        value = case("C")
        value["propositions"][0]["evidence_ids"].remove("C-contradiction")
        value["evidence"] = value["evidence"][:2]
        value["disagreements"] = []
        result = evaluate(value)
        self.assertEqual(result["outcome"], "INDETERMINATE")
        self.assertIn("independent-corroboration-not-established", result["results"][0]["reasons"])

    def test_reviewed_disjoint_positive_sources_are_bounded_countercase(self):
        value = case("C")
        value["evidence"][2]["status"] = "supported"
        value["disagreements"] = []
        self.assertEqual(evaluate(value)["outcome"], "PASS")

    def test_unknown_independence_is_not_positive_independence(self):
        value = case("C")
        value["evidence"][2]["status"] = "supported"
        value["assessors"][2]["independence_review"]["state"] = "unknown"
        value["disagreements"] = []
        result = evaluate(value)
        self.assertEqual(result["outcome"], "INDETERMINATE")
        self.assertEqual(result["results"][0]["independence_unknown"], ["review-c"])

    def test_shared_material_basis_in_any_dimension_blocks_independence(self):
        for dimension in ("control", "maintainers", "corpus", "model_prompt", "fixtures"):
            with self.subTest(dimension=dimension):
                value = case("C")
                value["evidence"][2]["status"] = "supported"
                value["disagreements"] = []
                value["assessors"][2]["dependence"][dimension] = value["assessors"][0]["dependence"][dimension]
                self.assertEqual(evaluate(value)["outcome"], "INDETERMINATE")

    def test_each_context_change_invalidates_old_evidence_and_identity(self):
        baseline = case("P")
        for field in baseline["context"]:
            with self.subTest(field=field):
                value = deepcopy(baseline)
                value["lineage"] = {"previous_context": deepcopy(baseline["context"]), "previous_assessment": build_record(baseline)["assessment_id"]}
                value["context"][field] += "-changed"
                record = build_record(value)
                self.assertEqual(record["outcome"], "INDETERMINATE")
                self.assertEqual(record["sociotechnical"]["changed_context"], [field])
                self.assertNotEqual(record["assessment_id"], build_record(baseline)["assessment_id"])
                # Explicit, reviewed evidence for the new snapshot can re-establish support.
                value["evidence"][0]["context_digest"] = digest(value["context"])
                self.assertEqual(evaluate(value)["outcome"], "PASS")

    def test_stale_insufficient_unknown_and_wrong_pin_never_pass(self):
        for change in ({"freshness": "stale"}, {"sufficient": False}, {"status": "unknown"},
                       {"source_pin": {"repository": "other/source", "revision": "b" * 40}},
                       {"provenance": {"source": "assertion", "revision": "b" * 40, "description": "wrong epoch"}}):
            with self.subTest(change=change):
                value = case("P")
                value["evidence"][0].update(change)
                self.assertEqual(evaluate(value)["outcome"], "INDETERMINATE")

    def test_no_evidence_does_not_become_pass(self):
        value = case("P")
        value["propositions"][0]["evidence_ids"] = []
        value["evidence"] = []
        self.assertEqual(evaluate(value)["outcome"], "INDETERMINATE")

    def test_repair_and_operator_closure_do_not_resolve_human_remedy(self):
        value = case("E")
        record = canonical_record(build_record(value))
        self.assertEqual(record["outcome"], "FAIL")
        self.assertIn("O-E", record["sociotechnical"]["unresolved"])
        self.assertEqual(record["sociotechnical"]["input"]["disposition"]["affected_party_agreement"], "objected")
        value["obligations"][0]["state"] = "resolved"
        self.assertIn("O-E", evaluate(value)["unresolved"])

    def test_open_remedy_blocks_aggregate_pass_even_after_supported_repair(self):
        value = case("E")
        value["evidence"][1]["status"] = "supported"
        self.assertEqual(evaluate(value)["outcome"], "INDETERMINATE")
        value["obligations"][0]["state"] = "resolved"
        self.assertEqual(evaluate(value)["outcome"], "PASS")
        # A resolved label without attributable evidence is still unresolved.
        value["obligations"][0]["evidence_ids"] = []
        self.assertEqual(evaluate(value)["outcome"], "INDETERMINATE")

    def test_unresolved_disagreement_blocks_bounded_aggregate_pass(self):
        value = case("F")
        self.assertEqual(evaluate(value)["outcome"], "INDETERMINATE")
        value["disagreements"][0]["state"] = "resolved"
        self.assertEqual(evaluate(value)["outcome"], "PASS")

    def test_unjustified_non_applicability_is_indeterminate(self):
        value = case("N")
        value["propositions"][0]["not_applicable_reason"] = ""
        self.assertEqual(evaluate(value)["outcome"], "INDETERMINATE")
        value = case("N")
        value["propositions"][0]["evidence_ids"] = []
        value["evidence"] = []
        self.assertEqual(evaluate(value)["outcome"], "INDETERMINATE")

    def test_record_tampering_cannot_omit_material_qualifications(self):
        record = build_record(case("F"))
        mutations = [lambda r: r.pop("sociotechnical"), lambda r: r.pop("scope"),
                     lambda r: r["sociotechnical"].update(unresolved=[]),
                     lambda r: r.update(outcome="PASS", state="TERMINAL_PASS"),
                     lambda r: r["sociotechnical"]["input"].update(disagreements=[])]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                changed = deepcopy(record)
                mutate(changed)
                with self.assertRaises(ValueError):
                    canonical_record(changed)
                with self.assertRaises(ValueError):
                    markdown(changed)

    def test_supplied_contradiction_cannot_be_hidden_from_proposition(self):
        value = case("C")
        value["propositions"][0]["evidence_ids"].remove("C-contradiction")
        with self.assertRaises(ValueError):
            evaluate(value)

    def test_material_specialist_referral_cannot_become_pass(self):
        value = case("P")
        value["propositions"][0]["evaluator"] = "disclosure-pressure"
        value["propositions"][0]["facts"] = {"minimal_proof_available": True, "expanded_disclosure_requested": False, "correlation_or_minimization_depth_material": True}
        self.assertEqual(evaluate(value)["outcome"], "INDETERMINATE")

    def test_false_challenge_demonstration_is_not_positive_support(self):
        value = case("P")
        value["challenge_route"].update(state="demonstrated", account_independent=False, evidence=["P-choice"])
        self.assertEqual(evaluate(value)["outcome"], "INDETERMINATE")

    def test_human_record_embeds_exact_machine_record_and_visible_obligations(self):
        record = canonical_record(build_record(case("E")))
        human = markdown(record)
        embedded = yaml.safe_load(human.split("```yaml\n")[1].split("```", 1)[0])
        self.assertEqual(embedded, record)
        for fragment in ("Organizational risk acceptor", "objected", "human-remedy", "account independent: False", "No affected-party participation"):
            self.assertIn(fragment, human)

    def test_replay_is_deterministic_and_does_not_mutate_input(self):
        value = case("C")
        original = deepcopy(value)
        self.assertEqual(build_record(value), build_record(value))
        self.assertEqual(value, original)

    def test_invalid_boolean_and_reference_are_rejected(self):
        value = case("P")
        value["propositions"][0]["facts"]["refusal_meaningfully_available"] = "yes"
        with self.assertRaises(ValueError):
            validate_input(value)
        value = case("P")
        value["propositions"][0]["evidence_ids"] = ["missing"]
        with self.assertRaises(ValueError):
            validate_input(value)

    def test_duplicate_evidence_and_unknown_assessor_rejected(self):
        value = case("P")
        value["evidence"].append(deepcopy(value["evidence"][0]))
        with self.assertRaises(ValueError):
            validate_input(value)
        value = case("P")
        value["evidence"][0]["assessor"] = "unrecorded-reviewer"
        with self.assertRaises(ValueError):
            validate_input(value)

    def test_synthetic_review_cannot_be_flagged_independent_human(self):
        value = case("P")
        value["review"]["independent_human"] = "completed"
        with self.assertRaises(ValueError):
            validate_input(value)


if __name__ == "__main__":
    unittest.main()
