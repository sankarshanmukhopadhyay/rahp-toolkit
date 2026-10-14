"""Bounded adversarial boundary tests for RAHP #1023.

These are controlled counterexamples to over-reading optional structural profiles.
Some evaluations legitimately produce structurally positive declarations despite
unverified scope or provenance. Those are explicit consumer-governance residuals,
not evaluator bugs or terminal RAHP assurance outcomes.
"""
import copy
import unittest

from tools.evidence_adequacy import evaluate
from tools.temporal_provenance import evaluate_temporal
from tools.reproducibility_challenge import compare


def r1():
    return {
        "schema": "rahp-evidence-adequacy/v1",
        "proposition_id": "AA-01", "scope": "synthetic bounded scope",
        "required_evidence": ["E-A", "E-B"],
        "observations": [
            {"id": "O-A", "evidence_id": "E-A", "scope": "synthetic bounded scope", "state": "SATISFIED"},
            {"id": "O-B", "evidence_id": "E-B", "scope": "synthetic bounded scope", "state": "SATISFIED"},
        ],
    }


def r2():
    return {
        "schema": "rahp-temporal-provenance/v1", "proposition_id": "AA-03",
        "target_time": "2026-04-15T00:00:00Z",
        "knowledge_cutoff": "2026-05-01T00:00:00Z",
        "evaluated_at": "2026-08-20T00:00:00Z",
        "required_evidence": ["E-A"],
        "records": [{
            "id": "R-A", "evidence_id": "E-A",
            "source_pin": {"repository": "synthetic/unverified-source", "revision": "a" * 40},
            "observed_at": "2026-04-15T00:00:00Z",
            "recorded_at": "2026-04-16T00:00:00Z",
            "effective_from": "2026-04-10T00:00:00Z",
            "effective_until": "2026-05-01T00:00:00Z",
        }],
    }


def r3():
    return {
        "schema": "rahp-reproducibility-challenge/v1", "proposition_id": "AA-05",
        "runs": [
            {"id": rid, "evaluator_id": "synthetic-evaluator", "evaluator_version": "1",
             "input_pin": {"algorithm": "sha256", "digest": "a" * 64}, "outcome": "PASS"}
            for rid in ("A", "B")
        ],
        "challenges": [],
    }


class CrossBoundaryAdversarialQualification(unittest.TestCase):
    def test_AA01_removed_requirement_preserves_only_bounded_structural_pass(self):
        complete = evaluate(r1())
        self.assertEqual(complete["outcome"], "PASS")
        withheld = r1()
        withheld["required_evidence"].remove("E-B")
        withheld["observations"].pop()
        result = evaluate(withheld)
        # Demonstrates caller-controlled coverage, *not* a toolkit terminal PASS.
        self.assertEqual(result["outcome"], "PASS")
        self.assertEqual(len(result["findings"]), 1)
        self.assertIn("not terminal RAHP assurance", result["authority_note"])

    def test_AA02_contradictory_observation_fails_conservative_adequacy(self):
        item = r1()
        item["observations"].append({
            "id": "O-ADVERSARIAL", "evidence_id": "E-A",
            "scope": item["scope"], "state": "NOT_SATISFIED",
        })
        result = evaluate(item)
        self.assertEqual(result["outcome"], "INDETERMINATE")
        self.assertEqual(next(f for f in result["findings"] if f["evidence_id"] == "E-A")["status"], "CONFLICT")

    def test_AA03_unverified_declared_source_is_not_authoritative(self):
        result = evaluate_temporal(r2())
        self.assertEqual(result["disposition"], "APPLICABLE")
        self.assertIn("no authenticity", result["authority_note"])
        self.assertNotIn("outcome", result)

    def test_AA04_later_record_changes_known_at_answer_not_historical_record(self):
        item = r2()
        later = copy.deepcopy(item["records"][0])
        later.update(id="R-LATER", recorded_at="2026-08-10T00:00:00Z",
                     effective_from="2026-04-01T00:00:00Z")
        item["records"].append(later)
        earlier = evaluate_temporal(item)
        self.assertEqual(earlier["disposition"], "APPLICABLE")
        self.assertEqual(earlier["findings"][0]["later_record_ids"], ["R-LATER"])
        item["knowledge_cutoff"] = "2026-08-20T00:00:00Z"
        later_known = evaluate_temporal(item)
        self.assertEqual(later_known["disposition"], "INDETERMINATE")
        self.assertEqual(later_known["findings"][0]["status"], "CONFLICT")

    def test_AA05_identical_claimed_digest_is_not_verified_replay(self):
        item = r3()
        result = compare(item)
        self.assertEqual(result["disposition"], "DECLARED_MATCH")
        self.assertTrue(result["same_input"])
        self.assertIn("Declared comparison only", result["authority_note"])
        # The arbitrary synthetic digest is accepted *as a claim*; this
        # test does not assert that source bytes were read or authenticated.
        self.assertNotIn("terminal_outcome", result)

    def test_AA06_declared_digest_divergence_is_detected(self):
        item = r3()
        item["runs"][1]["input_pin"]["digest"] = "b" * 64
        result = compare(item)
        self.assertEqual(result["disposition"], "DIFFERENT_INPUT")
        self.assertFalse(result["same_input"])

    def test_AA11_reporting_boundary_cannot_be_inferred_from_profile_pass(self):
        structural = evaluate(r1())
        temporal = evaluate_temporal(r2())
        self.assertEqual(structural["outcome"], "PASS")
        self.assertEqual(temporal["disposition"], "APPLICABLE")
        self.assertIn("not terminal RAHP assurance", structural["authority_note"])
        self.assertIn("no authenticity", temporal["authority_note"])
        self.assertNotIn("terminal_outcome", structural)
        self.assertNotIn("terminal_outcome", temporal)

    def test_AA12_open_challenge_survives_declared_match(self):
        item = r3()
        item["challenges"].append({
            "id": "C-A", "run_id": "A", "reason": "SCOPE",
            "evidence_refs": ["E-UNVERIFIED"],
        })
        result = compare(item)
        self.assertEqual(result["disposition"], "DECLARED_MATCH")
        self.assertEqual(result["challenges"][0]["status"], "OPEN")
        self.assertIn("challenges remain open", result["authority_note"])


if __name__ == "__main__":
    unittest.main()
