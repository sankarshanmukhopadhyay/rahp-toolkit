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

if __name__=="__main__": unittest.main()
