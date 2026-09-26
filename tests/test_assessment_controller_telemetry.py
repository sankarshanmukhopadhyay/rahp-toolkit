import unittest

from tools.assessment_controller import lifecycle_telemetry, new_lifecycle, transition


class AssessmentControllerTelemetryTests(unittest.TestCase):
    def test_lifecycle_telemetry_is_sidecar_and_does_not_mutate_record(self):
        record = new_lifecycle("assessment:test")
        transition(record, "QUALIFIED", "scope accepted")
        before = repr(record)
        event = lifecycle_telemetry(record, duration_seconds=0.25)
        self.assertEqual(repr(record), before)
        self.assertEqual(event["operation"], "assessment-lifecycle")
        self.assertEqual(event["run_id"], "assessment:test")
        self.assertEqual(event["metrics"]["transition_count"], 1)
        self.assertFalse(event["metrics"]["terminal"])
        self.assertFalse(event["authority_boundary"]["may_set_assurance_outcome"])

    def test_terminal_outcome_is_reported_only_after_terminal_transition(self):
        record = new_lifecycle("assessment:terminal")
        transition(record, "TERMINAL", "explicit fail", terminal_outcome="FAIL")
        event = lifecycle_telemetry(record)
        self.assertTrue(event["metrics"]["terminal"])
        self.assertEqual(event["metrics"]["terminal_outcome"], "FAIL")


if __name__ == "__main__":
    unittest.main()
