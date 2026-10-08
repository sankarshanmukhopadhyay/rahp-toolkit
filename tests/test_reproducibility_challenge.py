"""R3 comparison and challenge conformance tests."""
import copy
import unittest
from tools.reproducibility_challenge import compare


def fixture():
    return {"schema": "rahp-reproducibility-challenge/v1",
            "proposition_id": "P-1",
            "runs": [
                {"id": rid, "evaluator_id": "ra", "evaluator_version": "1",
                 "input_pin": {"algorithm": "sha256", "digest": "a" * 64},
                 "outcome": "PASS"} for rid in ("A", "B")],
            "challenges": []}


class R3Tests(unittest.TestCase):
    def test_matching_declared_runs(self):
        p = fixture()
        self.assertEqual(compare(p)["disposition"], "DECLARED_MATCH")
        self.assertEqual(len(compare(p)["runs"][0]["record_digest"]), 64)

    def test_output_disagreement(self):
        p = fixture()
        p["runs"][1]["outcome"] = "FAIL"
        self.assertEqual(compare(p)["disposition"], "OUTPUT_DISAGREEMENT")

    def test_input_difference_takes_precedence(self):
        p = fixture()
        p["runs"][1]["input_pin"]["digest"] = "b" * 64
        p["runs"][1]["outcome"] = "FAIL"
        self.assertEqual(compare(p)["disposition"], "DIFFERENT_INPUT")

    def test_evaluator_difference(self):
        p = fixture()
        p["runs"][1]["evaluator_version"] = "2"
        self.assertEqual(compare(p)["disposition"], "DIFFERENT_EVALUATOR")

    def test_challenge_does_not_reverse(self):
        p = fixture()
        p["challenges"] = [{"id": "C", "run_id": "A", "reason": "EVIDENCE",
                            "evidence_refs": ["E-2", "E-1"]}]
        result = compare(p)
        self.assertEqual(result["disposition"], "DECLARED_MATCH")
        self.assertEqual(result["challenges"][0]["status"], "OPEN")
        self.assertEqual(result["challenges"][0]["evidence_refs"], ["E-1", "E-2"])

    def test_order_invariant_and_no_mutation(self):
        p = fixture()
        p["challenges"] = [{"id": "C", "run_id": "A", "reason": "METHOD",
                            "evidence_refs": ["E-2", "E-1"]}]
        q = copy.deepcopy(p)
        q["runs"].reverse()
        q["challenges"][0]["evidence_refs"].reverse()
        self.assertEqual(compare(p), compare(q))
        self.assertEqual(p["challenges"][0]["evidence_refs"], ["E-2", "E-1"])

    def test_malformed_fail_closed(self):
        changes = [
            lambda p: p["runs"].pop(),
            lambda p: p["runs"][1].update(id="A"),
            lambda p: p["runs"][1]["input_pin"].update(digest="invalid"),
            lambda p: p["runs"][1].update(outcome=[]),
            lambda p: p["runs"][1].update(evaluator_version=""),
            lambda p: p["runs"][1].update(unexpected=True),
            lambda p: p["challenges"].append({"id": "C", "run_id": "unknown", "reason": "METHOD", "evidence_refs": ["E"]}),
            lambda p: p["challenges"].append({"id": "C", "run_id": "A", "reason": "METHOD", "evidence_refs": []}),
            lambda p: p["challenges"].append({"id": "C", "run_id": "A", "reason": "METHOD", "evidence_refs": ["E", "E"]}),
        ]
        for change in changes:
            p = fixture()
            change(p)
            with self.subTest(p=p), self.assertRaises(ValueError):
                compare(p)


if __name__ == "__main__":
    unittest.main()
