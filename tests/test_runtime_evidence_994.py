"""Negative controls ensure fixture or schema checks never become runtime PASS."""
import copy
import json
import unittest
from tools.validate_runtime_evidence_994 import DEFAULT, validate

DATA = json.loads(DEFAULT.read_text())

class RuntimeEvidenceGateTests(unittest.TestCase):
    def test_all_three_scopes_are_explicitly_indeterminate(self):
        self.assertEqual([], validate(DATA))
        self.assertEqual({"INDETERMINATE"}, {x["state"] for x in DATA["scopes"]})

    def test_no_false_pass(self):
        x = copy.deepcopy(DATA)
        x["scopes"][0]["state"] = "PASS"
        self.assertTrue(any("PASS cannot" in y for y in validate(x)))

    def test_no_unattributed_fail_or_transfer(self):
        x = copy.deepcopy(DATA)
        x["scopes"][1]["state"] = "FAIL"
        self.assertTrue(validate(x))
        x = copy.deepcopy(DATA)
        x["scopes"][2]["state"] = "TRANSFERRED"
        self.assertTrue(validate(x))

    def test_no_false_privacy_disposition(self):
        x = copy.deepcopy(DATA)
        x["scopes"][0]["dpip"] = "OUT_OF_SCOPE_WITH_RATIONALE"
        self.assertTrue(validate(x))
        x = copy.deepcopy(DATA)
        x["scopes"][0]["dpip"] = "REFERRED"
        self.assertTrue(validate(x))

    def test_bad_runtime_evidence_attribution_fails(self):
        x = copy.deepcopy(DATA)
        x["scopes"][0]["runtime_evidence"] = {"sha256": "a" * 64}
        self.assertTrue(any("provenance incomplete" in y for y in validate(x)))
if __name__ == "__main__":
    unittest.main()
