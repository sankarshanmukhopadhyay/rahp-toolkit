"""Presentation contract tests for the retained TRQP replay."""
from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "standalone-trqp"
sys.path.insert(0, str(EXAMPLE))
spec = importlib.util.spec_from_file_location("trqp_demo", EXAMPLE / "demo.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class DemoTests(unittest.TestCase):
    def setUp(self):
        self.result = {
            "target_commit": "6863733878f3657e05f70764bb474a9fb918de9a",
            "source_integrity": "verified",
            "cases": [
                {"id": "minimal-required-fields", "schema_valid": True},
                {"id": "missing-authority-negative-control", "schema_valid": False},
                {"id": "historical-response-without-provenance", "schema_valid": True},
            ],
            "api_example": {"schema_valid": True, "requested_time_matches": False},
            "https_example": {"schema_valid": True, "requested_time_matches": True},
            "overall_assurance": "review-required",
            "runtime_authorization": "not-assessed",
            "authority_history": "not-assessed",
        }

    def test_expected_replay_is_explained_without_assurance_inflation(self):
        output = module.summarize(self.result)
        for term in ("F-001", "F-002", "REVIEW REQUIRED", "NOT ASSESSED", "schema INVALID"):
            self.assertIn(term, output)

    def test_missing_negative_control_is_rejected(self):
        self.result["cases"].pop(1)
        with self.assertRaises(ValueError):
            module.summarize(self.result)

    def test_changed_specification_example_is_rejected(self):
        self.result["api_example"]["requested_time_matches"] = True
        with self.assertRaises(ValueError):
            module.summarize(self.result)

    def test_assurance_upgrade_cannot_be_silently_presented(self):
        self.result["overall_assurance"] = "assured"
        with self.assertRaises(ValueError):
            module.summarize(self.result)


if __name__ == "__main__":
    unittest.main()
