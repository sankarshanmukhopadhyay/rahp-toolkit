"""Conformance checks for optional reasoning trace, independent of v1 assessor contract."""
import copy
import unittest

from tools.reasoning_trace import validate_trace


def fixture():
    trace = {
        "schema": "rahp-reasoning-trace/v1",
        "proposition_id": "TRQP-AUTH-001",
        "method": "bounded-schema-check",
        "method_version": "1",
        "scope": "retained TRQP source only; not runtime authority",
        "evidence_refs": ["ER-1"],
        "observations": [{"id": "OBS-1", "result": "SATISFIED", "evidence_refs": ["ER-1"]}],
        "judgment": {"outcome": "PASS", "reason_codes": ["schema-predicate-satisfied"]},
    }
    result = {"outcome": "PASS", "evidence_used": ["ER-1"]}
    return trace, result


class ReasoningTraceTests(unittest.TestCase):
    def test_valid_bounded_trace(self):
        trace, result = fixture()
        self.assertEqual(validate_trace(trace, result), [])

    def test_missing_evidence_reference(self):
        trace, result = fixture()
        trace["observations"][0]["evidence_refs"] = ["ER-MISSING"]
        self.assertTrue(validate_trace(trace, result))

    def test_indeterminate_does_not_pass(self):
        trace, result = fixture()
        trace["observations"][0]["result"] = "INDETERMINATE"
        self.assertIn("PASS cannot silently bypass indeterminate observations", validate_trace(trace, result))

    def test_contradiction_does_not_pass(self):
        trace, result = fixture()
        trace["observations"][0]["result"] = "NOT_SATISFIED"
        self.assertIn("PASS cannot silently bypass contradictory observations", validate_trace(trace, result))

    def test_assessor_outcome_mismatch(self):
        trace, result = fixture()
        result["outcome"] = "FAIL"
        self.assertIn("trace judgment and assessor outcome disagree", validate_trace(trace, result))

    def test_assessor_evidence_mismatch(self):
        trace, result = fixture()
        result["evidence_used"] = ["ER-2"]
        self.assertIn("trace evidence and assessor evidence_used disagree", validate_trace(trace, result))

    def test_duplicate_observations(self):
        trace, result = fixture()
        trace["observations"].append(copy.deepcopy(trace["observations"][0]))
        self.assertTrue(any("duplicate observation" in e for e in validate_trace(trace, result)))


if __name__ == "__main__":
    unittest.main()
