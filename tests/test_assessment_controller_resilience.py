import importlib.util
import json
import pathlib
import unittest

import jsonschema

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "assessment_controller", ROOT / "tools" / "assessment_controller.py"
)
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)
SCHEMA = json.loads((ROOT / "method/schema/assessment-lifecycle.schema.json").read_text())


class AssessmentControllerResilienceTests(unittest.TestCase):
    def test_new_lifecycle_is_fail_closed_for_resilience(self):
        record = MOD.new_lifecycle("A-1")
        value = MOD.resilience_disposition(record)
        self.assertEqual(value["disposition"], "required-but-not-executed")
        self.assertEqual(value["provenance"]["decision"], "fail-closed")
        jsonschema.Draft202012Validator(SCHEMA).validate(record)

    def test_all_three_dispositions_are_distinct(self):
        for disposition in MOD.RESILIENCE_DISPOSITIONS:
            record = MOD.new_lifecycle(f"A-{disposition}")
            provenance = {"source": "test"} if disposition == "not-applicable" else None
            MOD.set_resilience_disposition(record, disposition, "test decision", provenance)
            self.assertEqual(MOD.resilience_disposition(record)["disposition"], disposition)
            jsonschema.Draft202012Validator(SCHEMA).validate(record)

    def test_not_applicable_requires_provenance(self):
        record = MOD.new_lifecycle("A-2")
        with self.assertRaises(ValueError):
            MOD.set_resilience_disposition(record, "not-applicable", "governance-only target")

    def test_unknown_or_empty_disposition_is_rejected(self):
        record = MOD.new_lifecycle("A-3")
        with self.assertRaises(ValueError):
            MOD.set_resilience_disposition(record, "skipped", "test")
        with self.assertRaises(ValueError):
            MOD.set_resilience_disposition(record, "executed", "")

    def test_legacy_record_without_capability_is_readable_but_unresolved(self):
        record = {
            "schema": "rahp-assessment-lifecycle/v1",
            "assessment_id": "legacy",
            "mode": "steady-state",
            "state": "DISCOVERED",
            "history": [{"from": None, "to": "DISCOVERED", "reason": "legacy"}],
            "blocking_reason": None,
        }
        jsonschema.Draft202012Validator(SCHEMA).validate(record)
        value = MOD.resilience_disposition(record)
        self.assertEqual(value["disposition"], "required-but-not-executed")
        self.assertEqual(value["provenance"]["source"], "compatibility-default")

    def test_legacy_terminal_pass_does_not_imply_resilience_pass(self):
        record = {
            "schema": "rahp-assessment-lifecycle/v1",
            "assessment_id": "legacy-pass",
            "mode": "steady-state",
            "state": "TERMINAL",
            "terminal_outcome": "PASS",
            "history": [{"from": "ASSESSED", "to": "TERMINAL", "reason": "legacy pass"}],
            "blocking_reason": None,
        }
        jsonschema.Draft202012Validator(SCHEMA).validate(record)
        self.assertEqual(
            MOD.resilience_disposition(record)["disposition"],
            "required-but-not-executed",
        )

    def test_malformed_stored_disposition_is_rejected(self):
        record = MOD.new_lifecycle("A-4")
        record["capabilities"]["resilience"] = {
            "disposition": "unknown",
            "reason": "bad persisted value",
        }
        with self.assertRaises(ValueError):
            MOD.resilience_disposition(record)
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.Draft202012Validator(SCHEMA).validate(record)


if __name__ == "__main__":
    unittest.main()
