import unittest
from tools.observability_harm import evaluate_observability

class TestObservabilityHarm(unittest.TestCase):
    def test_reused_trace(self):
        observations = [
            dict(context="alpha", trace_id="same", evidence_state="verified"),
            dict(context="beta", trace_id="same", evidence_state="verified"),
        ]
        self.assertEqual(evaluate_observability(observations)["state"], "FAIL")

    def test_absent_evidence(self):
        result = evaluate_observability([dict(context="alpha", trace_id="one", evidence_state="missing")])
        self.assertEqual(result["state"], "INDETERMINATE")

    def test_decision_boundary(self):
        event = dict(context="alpha", trace_id="one", evidence_state="verified",
                     decision_source="telemetry", consequential_action="suspend")
        self.assertEqual(evaluate_observability([event])["state"], "FAIL")

    def test_no_false_pass(self):
        event = dict(context="alpha", trace_id="one", evidence_state="verified")
        self.assertEqual(evaluate_observability([event])["state"], "INDETERMINATE")
