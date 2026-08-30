import importlib.util
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from assessor_contract import normalize_external, validate_result
from assessment_controller import (
    apply_assessor_result, clean_room_lineage, may_coalesce,
    new_lifecycle, plugin_error, transition,
)


class PortableLifecycleContractTests(unittest.TestCase):
    def result(self, outcome):
        return normalize_external(
            assessor="example-specialist",
            assessment_id="A-1",
            outcome=outcome,
            reason_code="example",
            evidence_used=["E-1"],
            residual_risk="bounded",
            action_required="none" if outcome == "PASS" else "review",
        )

    def evidence_ready(self, mode="steady-state"):
        r = new_lifecycle("A-1", mode)
        transition(r, "QUALIFIED", "qualified")
        transition(r, "ROUTED", "routed")
        transition(r, "ASSESSMENT_REQUIRED", "assessment required")
        transition(r, "EVIDENCE_READY", "evidence supplied")
        return r

    def test_all_specialist_outcomes_terminate(self):
        for outcome in ("PASS", "FAIL", "INDETERMINATE", "NOT_APPLICABLE"):
            record = self.evidence_ready()
            apply_assessor_result(record, self.result(outcome))
            self.assertEqual(record["state"], "TERMINAL")
            self.assertEqual(record["terminal_outcome"], outcome)

    def test_evidence_ready_cannot_silently_accept_invalid_result(self):
        record = self.evidence_ready()
        with self.assertRaises(ValueError):
            apply_assessor_result(record, {"outcome": "MAYBE"})
        self.assertEqual(record["state"], "EVIDENCE_READY")

    def test_plugin_error_is_indeterminate_never_pass(self):
        record = self.evidence_ready()
        plugin_error(record, "plugin-error", "boom")
        self.assertEqual(record["terminal_outcome"], "INDETERMINATE")
        self.assertEqual(record["blocking_reason"]["code"], "plugin-error")

    def test_unmapped_is_explicit_terminal(self):
        record = new_lifecycle("A-2")
        transition(record, "QUALIFIED", "qualified")
        transition(record, "TERMINAL", "no semantic mapping", terminal_outcome="UNMAPPED", blocking_reason={"code": "unmapped"})
        self.assertEqual(record["terminal_outcome"], "UNMAPPED")

    def test_clean_room_never_coalesces(self):
        lineage_a = clean_room_lineage("example", "2026-08-30", "A")
        lineage_b = clean_room_lineage("example", "2026-08-30", "B")
        a = new_lifecycle("same-key", "clean-room", lineage_a)
        b = new_lifecycle("same-key", "clean-room", lineage_b)
        self.assertFalse(may_coalesce(a, b))
        self.assertNotEqual(lineage_a["run_id"], lineage_b["run_id"])
        self.assertFalse(lineage_a["isolation"]["historical_evidence_allowed"])

    def test_steady_state_can_coalesce_open_same_assessment(self):
        a = new_lifecycle("same-key")
        b = new_lifecycle("same-key")
        self.assertTrue(may_coalesce(a, b))

    def test_assessor_schema_rejects_workflow_success_as_outcome(self):
        invalid = {
            "schema": "rahp-assessor-result/v1",
            "assessor": "x",
            "assessment_id": "A",
            "outcome": "GREEN",
            "reason_code": "workflow-success",
            "evidence_used": [],
            "residual_risk": "unknown",
            "action_required": "none",
        }
        self.assertTrue(validate_result(invalid))


if __name__ == "__main__":
    unittest.main()
