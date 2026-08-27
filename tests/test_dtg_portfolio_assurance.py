import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "dtg_portfolio_assurance", ROOT / "tools" / "dtg_portfolio_assurance.py"
)
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


class DtgPortfolioAssuranceTests(unittest.TestCase):
    def evidence(self):
        return {
            "run": {"id": "run-1", "fingerprint": "fp-1", "qualifying_events": ["e1"]},
            "events": [{"id": "e1", "accounted_for": True}],
            "assessments": [{"id": "a1", "required": True, "complete": True, "provenance_valid": True}],
            "dpip": [],
        }

    def result(self, evidence):
        return MOD.compute(evidence)["portfolio_assurance"]

    def test_green_when_all_work_complete_and_dpip_not_required(self):
        p = self.result(self.evidence())
        self.assertEqual((p["pipeline_status"], p["disposition"]), ("GREEN", "DPIP_NOT_REQUIRED"))
        self.assertEqual(p["events_accounted_for"], 1)

    def test_green_when_required_dpip_returns_pass(self):
        evidence = self.evidence()
        evidence["dpip"] = [{
            "id": "d1", "required": True, "complete": True,
            "return_received": True, "disposition": "PASS", "provenance_valid": True,
        }]
        p = self.result(evidence)
        self.assertEqual((p["pipeline_status"], p["disposition"]), ("GREEN", "DPIP_COMPLETE"))

    def test_indeterminate_is_amber_not_green(self):
        evidence = self.evidence()
        evidence["dpip"] = [{
            "id": "d1", "required": True, "complete": True,
            "return_received": True, "disposition": "INDETERMINATE", "provenance_valid": True,
        }]
        p = self.result(evidence)
        self.assertEqual((p["pipeline_status"], p["disposition"]), ("AMBER", "INDETERMINATE"))

    def test_open_assessment_overrides_green_ci_assumption(self):
        evidence = self.evidence()
        evidence["assessments"][0]["complete"] = False
        p = self.result(evidence)
        self.assertEqual((p["pipeline_status"], p["disposition"]), ("AMBER", "WORK_OPEN"))

    def test_unaccounted_gatherer_event_is_amber(self):
        evidence = self.evidence()
        evidence["run"]["qualifying_events"].append("e2")
        p = self.result(evidence)
        self.assertEqual((p["pipeline_status"], p["disposition"]), ("AMBER", "WORK_OPEN"))
        self.assertIn("e2", p["blockers"]["coverage"])

    def test_missing_dpip_return_is_pipeline_broken(self):
        evidence = self.evidence()
        evidence["dpip"] = [{
            "id": "d1", "required": True, "complete": True,
            "return_received": False, "disposition": "PASS", "provenance_valid": True,
        }]
        p = self.result(evidence)
        self.assertEqual((p["pipeline_status"], p["disposition"]), ("RED", "PIPELINE_BROKEN"))

    def test_invalid_provenance_is_pipeline_broken(self):
        evidence = self.evidence()
        evidence["assessments"][0]["provenance_valid"] = False
        p = self.result(evidence)
        self.assertEqual((p["pipeline_status"], p["disposition"]), ("RED", "PIPELINE_BROKEN"))

    def test_adverse_assessment_is_red(self):
        evidence = self.evidence()
        evidence["assessments"][0]["adverse"] = True
        p = self.result(evidence)
        self.assertEqual((p["pipeline_status"], p["disposition"]), ("RED", "ADVERSE_FINDING"))

    def test_zero_events_is_valid_green_no_dpip(self):
        evidence = {"run": {"id": "run-empty", "fingerprint": "fp-empty", "qualifying_events": []}}
        p = self.result(evidence)
        self.assertEqual((p["pipeline_status"], p["disposition"]), ("GREEN", "DPIP_NOT_REQUIRED"))
        self.assertEqual(p["gatherer_events"], 0)

    def test_deterministic_for_same_evidence(self):
        evidence = self.evidence()
        self.assertEqual(MOD.compute(evidence), MOD.compute(evidence))


if __name__ == "__main__":
    unittest.main()
