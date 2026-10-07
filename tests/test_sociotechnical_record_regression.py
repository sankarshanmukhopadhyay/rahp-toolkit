"""Regression: canonical projection must preserve current assurance dimensions."""
import unittest

from tools.assurance_record import canonical_record


class CanonicalDimensionsRegression(unittest.TestCase):
    def test_current_dimensions_survive_canonical_projection(self):
        record = {
            "assessment_id": "rahp:projection", "subject": {"type": "deployment", "id": "synthetic"},
            "source_pins": [{"repository": "synthetic/service", "revision": "a" * 40}],
            "state": "TERMINAL_PASS", "terminal": True, "outcome": "PASS", "reason_code": "bounded-pass",
            "process_state": "complete", "assurance_state": "pass", "evidence_maturity": "modeled",
            "lenses": {"rahp": {"result": "PASS"}}, "required_evidence": ["runtime-required"],
            "evidence_probe_ledger": {"runtime-required": "attempted-unavailable"},
        }
        projected = canonical_record(record)
        for key in ("process_state", "assurance_state", "evidence_maturity", "lenses", "required_evidence", "evidence_probe_ledger"):
            with self.subTest(key=key):
                self.assertEqual(projected.get(key), record[key])
