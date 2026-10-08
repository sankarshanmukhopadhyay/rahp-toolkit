"""Conformance tests for optional evidence adequacy."""
import copy
import unittest
from tools.evidence_adequacy import evaluate

def sample():
    return {"schema":"rahp-evidence-adequacy/v1","proposition_id":"P-1","scope":"source snapshot","required_evidence":["E1","E2"],"observations":[
        {"id":"O1","evidence_id":"E1","scope":"source snapshot","state":"SATISFIED"},
        {"id":"O2","evidence_id":"E2","scope":"source snapshot","state":"SATISFIED"}]}

class EvidenceAdequacyTests(unittest.TestCase):
    def test_satisfied(self):
        self.assertEqual(evaluate(sample())["outcome"],"PASS")
    def test_negative(self):
        p=sample();p["observations"][0]["state"]="NOT_SATISFIED"
        self.assertEqual(evaluate(p)["outcome"],"FAIL")
    def test_missing(self):
        p=sample();p["observations"].pop()
        self.assertEqual(evaluate(p)["outcome"],"INDETERMINATE")
    def test_unavailable(self):
        p=sample();p["observations"][0]["state"]="UNAVAILABLE"
        self.assertEqual(evaluate(p)["outcome"],"INDETERMINATE")
    def test_mixed_missing_and_negative(self):
        p=sample();p["observations"][0]["state"]="NOT_SATISFIED";p["observations"].pop()
        self.assertEqual(evaluate(p)["outcome"],"INDETERMINATE")
    def test_conflicting(self):
        p=sample();p["observations"].append({"id":"O3","evidence_id":"E1","scope":p["scope"],"state":"NOT_SATISFIED"})
        self.assertEqual(evaluate(p)["findings"][0]["status"],"CONFLICT")
    def test_scope_mismatch(self):
        p=sample();p["observations"][0]["scope"]="another subject"
        self.assertEqual(evaluate(p)["outcome"],"INDETERMINATE")
    def test_order_invariance(self):
        p=sample();q=copy.deepcopy(p);q["observations"].reverse();q["required_evidence"].reverse()
        self.assertEqual(evaluate(p),evaluate(q))
    def test_malformed(self):
        for field,value in [("schema","other"),("required_evidence",["E1","E1"]),("observations","wrong")]:
            p=sample();p[field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):
                evaluate(p)
    def test_duplicate_ids_and_unknown_evidence(self):
        for field,value in [("id","O2"),("evidence_id","unknown"),("state","PASS"),("scope","")]:
            p=sample();p["observations"][0][field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):
                evaluate(p)
    def test_does_not_mutate_input(self):
        p=sample();before=copy.deepcopy(p);evaluate(p);self.assertEqual(p,before)

if __name__=="__main__":
    unittest.main()
