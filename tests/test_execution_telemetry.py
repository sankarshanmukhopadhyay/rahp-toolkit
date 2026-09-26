import json
import tempfile
import unittest
from pathlib import Path

from tools.execution_telemetry import (
    SCHEMA,
    build_event,
    lifecycle_metrics,
    sanitize_context,
    sanitize_metrics,
    selection_metrics,
    write_event,
)


class ExecutionTelemetryTests(unittest.TestCase):
    def test_event_is_operational_not_assurance_evidence(self):
        event = build_event(
            operation="reassessment-selection",
            run_id="run-1",
            duration_seconds=0.125,
            context={"profile_id": "example", "plan": "routine"},
            metrics={"available_count": 8, "selected_count": 3},
        )
        self.assertEqual(event["schema"], SCHEMA)
        self.assertFalse(event["authority_boundary"]["assurance_evidence"])
        self.assertFalse(event["authority_boundary"]["may_set_assurance_outcome"])

    def test_context_is_whitelisted_and_drops_sensitive_arbitrary_fields(self):
        context = sanitize_context(
            {
                "profile_id": "example",
                "source_revision": "a" * 40,
                "token": "secret",
                "credential": "do-not-record",
                "evidence_body": "do-not-record",
            }
        )
        self.assertEqual(set(context), {"profile_id", "source_revision"})
        self.assertNotIn("secret", json.dumps(context))

    def test_metrics_reject_nested_payloads(self):
        with self.assertRaises(ValueError):
            sanitize_metrics({"evidence": {"raw": "payload"}})
        with self.assertRaises(ValueError):
            sanitize_metrics({"values": ["one", "two"]})

    def test_lifecycle_summary_does_not_infer_terminal_outcome(self):
        record = {
            "state": "EVIDENCE_REQUIRED",
            "history": [
                {"from": None, "to": "DISCOVERED"},
                {"from": "DISCOVERED", "to": "QUALIFIED"},
                {"from": "QUALIFIED", "to": "ROUTED"},
                {"from": "ROUTED", "to": "EVIDENCE_REQUIRED"},
            ],
            "blocking_reason": {"code": "missing-runtime-evidence", "message": "not available"},
            "capabilities": {
                "resilience": {"disposition": "required-but-not-executed"}
            },
        }
        metrics = lifecycle_metrics(record)
        self.assertFalse(metrics["terminal"])
        self.assertIsNone(metrics["terminal_outcome"])
        self.assertEqual(metrics["blocking_reason_code"], "missing-runtime-evidence")
        self.assertEqual(metrics["transition_count"], 3)

    def test_selection_metrics_are_exact(self):
        self.assertEqual(
            selection_metrics(available_count=8, selected_count=3),
            {"available_count": 8, "selected_count": 3, "skipped_count": 5},
        )
        with self.assertRaises(ValueError):
            selection_metrics(available_count=2, selected_count=3)

    def test_serialization_is_deterministic(self):
        event = build_event(
            operation="benchmark",
            run_id="full-validation",
            duration_seconds=1.0,
            metrics={"z": 2, "a": 1},
        )
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "event.json"
            write_event(path, event)
            first = path.read_text()
            write_event(path, event)
            self.assertEqual(first, path.read_text())
            self.assertIn('"schema": "rahp-execution-telemetry/v1"', first)


if __name__ == "__main__":
    unittest.main()
