import importlib.util
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
SPEC = importlib.util.spec_from_file_location(
    "dtg_assurance_reconcile", ROOT / "tools" / "dtg_assurance_reconcile.py"
)
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


class DtgAssuranceReconcileTests(unittest.TestCase):
    EVENT = "a" * 20

    def run_record(self):
        return {"id": "gha-123-1", "fingerprint": "fp", "qualifying_events": [self.EVENT], "event_count": 1}

    def issue(self, state="closed", labels=None):
        return {
            "number": 9,
            "state": state,
            "labels": [{"name": name} for name in (labels or [])],
            "body": f"<!-- rahp-dtg-gatherer-run:gha-123-1 -->\n<!-- rahp-dtg-gatherer-event:{self.EVENT} -->",
        }

    def result(self, issue, comments=None):
        evidence = MOD.normalize(self.run_record(), [issue], {9: comments or []})
        return MOD.compute(evidence)["portfolio_assurance"]

    def test_closed_issue_without_explicit_dpip_decision_is_not_terminal(self):
        p = self.result(self.issue())
        self.assertEqual((p["pipeline_status"], p["disposition"]), ("AMBER", "WORK_OPEN"))

    def test_explicit_no_dpip_allows_green_when_closed(self):
        p = self.result(self.issue(labels=[MOD.DPIP_NOT_REQUIRED]))
        self.assertEqual((p["pipeline_status"], p["disposition"]), ("GREEN", "DPIP_NOT_REQUIRED"))

    def test_no_dpip_label_does_not_hide_open_issue(self):
        p = self.result(self.issue(state="open", labels=[MOD.DPIP_NOT_REQUIRED]))
        self.assertEqual((p["pipeline_status"], p["disposition"]), ("AMBER", "WORK_OPEN"))

    def test_completed_dpip_requires_returned_structured_disposition(self):
        p = self.result(self.issue(labels=["assurance:dpip-complete"]))
        self.assertEqual((p["pipeline_status"], p["disposition"]), ("RED", "PIPELINE_BROKEN"))

    def test_indeterminate_round_trip_remains_amber(self):
        comments = [{"body": "```yaml\ndpip_disposition:\n  conclusion: INDETERMINATE\n```"}]
        p = self.result(self.issue(labels=["assurance:dpip-complete"]), comments)
        self.assertEqual((p["pipeline_status"], p["disposition"]), ("AMBER", "INDETERMINATE"))

    def test_coalesced_trigger_recovers_event_lineage(self):
        issue = self.issue(labels=[MOD.DPIP_NOT_REQUIRED])
        issue["body"] = (
            "<!-- rahp-assessment-key:dtg:repository:OpenVTC/openvtc -->\n"
            f"<!-- rahp-trigger:dtg:repository:OpenVTC/openvtc@gatherer-gha-123-1-{self.EVENT} -->"
        )
        self.assertTrue(MOD.linked_to_run(issue, "gha-123-1"))
        self.assertEqual(MOD.event_ids(issue, "gha-123-1"), [self.EVENT])

    def test_aggregate_preserves_worst_outstanding_lineage(self):
        green = {"portfolio_assurance": {"run":"r-green","pipeline_status":"GREEN","disposition":"DPIP_NOT_REQUIRED"}}
        amber = {"portfolio_assurance": {"run":"r-amber","pipeline_status":"AMBER","disposition":"WORK_OPEN"}}
        summary = MOD.aggregate([green, amber])["dtg_assurance"]
        self.assertEqual((summary["pipeline_status"], summary["disposition"]), ("AMBER", "WORK_OPEN"))
        self.assertEqual(summary["open_or_blocked_runs"], 1)

    def test_broken_pipeline_with_existing_rahp_owner_does_not_require_incident(self):
        result = {
            "portfolio_assurance": {
                "run": "gha-123-1",
                "pipeline_status": "RED",
                "disposition": "PIPELINE_BROKEN",
                "blockers": {"orphaned_handoffs": ["rahp#305:dpip"], "provenance": []},
            }
        }
        incident = MOD.controller_incidents([result])[0]
        self.assertFalse(incident["incident_required"])
        self.assertEqual(incident["owner_issues"], [305])
        self.assertEqual(incident["unowned_blockers"], [])

    def test_broken_pipeline_without_owner_requires_deterministic_incident(self):
        result = {
            "portfolio_assurance": {
                "run": "gha-123-1",
                "pipeline_status": "RED",
                "disposition": "PIPELINE_BROKEN",
                "blockers": {"orphaned_handoffs": [], "provenance": ["missing-source-pin"]},
            }
        }
        first = MOD.controller_incidents([result])[0]
        second = MOD.controller_incidents([result])[0]
        self.assertTrue(first["incident_required"])
        self.assertEqual(first["incident_key"], second["incident_key"])
        self.assertEqual(first["unowned_blockers"], ["missing-source-pin"])


if __name__ == "__main__":
    unittest.main()
