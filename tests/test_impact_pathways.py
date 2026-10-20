"""Full pilot coverage and falsification tests for people-impact qualifications."""
import copy
import json
import unittest
from pathlib import Path
from tools.validate_impact_pathways import validate

ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/"method/impact-pathways/pilot.json").read_text())

class ImpactPilotTest(unittest.TestCase):
    def test_full_pilot(self):
        errors,states=validate(DATA)
        self.assertFalse(errors,errors)
        self.assertEqual(sum(states.values()),50)
        self.assertEqual(states["provisional"],2)
        self.assertEqual(states["not-established"],48)

    def assert_invalid(self,change):
        data=copy.deepcopy(DATA)
        change(data)
        self.assertTrue(validate(data)[0])

    def test_wrong_id(self):
        self.assert_invalid(lambda d:d["pilot_corpora"][0]["dispositions"][1].update(scenario_id="SEC-TT-002"))

    def test_source_drift(self):
        self.assert_invalid(lambda d:d["pilot_corpora"][0]["baseline"].update(source_commit="0"*40))

    def test_composition_drift(self):
        self.assert_invalid(lambda d:d["pilot_corpora"][1]["baseline"]["depends_on"][0].update(source_commit="0"*40))

    def test_invalid_harm(self):
        self.assert_invalid(lambda d:d["pilot_corpora"][0]["dispositions"][1]["pathway"].update(harm_patterns=["HRM-FAKE-99"]))

    def test_silent_omission(self):
        self.assert_invalid(lambda d:d["pilot_corpora"][1]["dispositions"].pop())

    def test_unsupported_qualification(self):
        self.assert_invalid(lambda d:d["pilot_corpora"][0]["dispositions"][1].update(status="qualified"))

    def test_fabricated_runtime(self):
        self.assert_invalid(lambda d:d["pilot_corpora"][0]["dispositions"][1].update(execution_status="PASS"))

    def test_fabricated_persona(self):
        self.assert_invalid(lambda d:d["pilot_corpora"][0]["dispositions"][1].update(persona_id="D1"))

    def test_missing_reason(self):
        self.assert_invalid(lambda d:d["pilot_corpora"][0]["dispositions"][0].update(reason=""))


    def test_unknown_role_rejected(self):
        self.assert_invalid(lambda d:d["pilot_corpora"][0]["dispositions"][1]["pathway"].update(role_id="fictional-persona"))

    def test_qualified_without_harm_and_adjudication_rejected(self):
        self.assert_invalid(lambda d:d["pilot_corpora"][1]["dispositions"][0].update(status="qualified"))

    def test_zero_positive_dispositions_valid(self):
        data=copy.deepcopy(DATA)
        for group in data["pilot_corpora"]:
            for row in group["dispositions"]:
                row.pop("pathway",None)
                row.pop("adjudication",None)
                row["status"]="not-established"
                row["reason"]="No direct source-qualified people-impact pathway has been established at this baseline."
        errors,counts=validate(data)
        self.assertFalse(errors,errors)
        self.assertEqual(counts["not-established"],50)

    def test_harm_membership_does_not_make_qualification(self):
        self.assert_invalid(lambda d:d["pilot_corpora"][1]["dispositions"][0].update(
            status="qualified",
            adjudication={"reviewer":"unverified","reviewed_on":"2026-10-20","decision_evidence":"not source-grounded"}))

if __name__=="__main__": unittest.main()
