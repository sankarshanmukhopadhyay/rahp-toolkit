"""Falsification fixture and fail-closed regression checks."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "tools/upstream_evidence_boundary.py"
spec = importlib.util.spec_from_file_location("upstream_evidence_boundary", SCRIPT)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class EvidenceBoundaryTests(unittest.TestCase):
    def test_absent_upstream_fails_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(FileNotFoundError):
                m.evaluate(Path(temp))

    def test_trqp_assessment_mutation(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "evidence.json").write_text(json.dumps({"assessment_id": "SR-001"}))
            m.trqp_variant(root, "wrong_assessment")
            self.assertEqual(json.loads((root / "evidence.json").read_text())["assessment_id"], "SR-999")

    def test_missing_evidence_identifier_is_explicit(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "evidence.json").write_text(json.dumps({"findings": [{"evidence": ["E-001"]}]}))
            m.trqp_variant(root, "missing_finding_evidence")
            self.assertEqual(json.loads((root / "evidence.json").read_text())["findings"][0]["evidence"], ["E-999"])

    def test_incomplete_execution_cannot_be_success(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "evidence.json").write_text(json.dumps({"execution": {"state": "complete"}}))
            m.trqp_variant(root, "incomplete_execution")
            self.assertEqual(json.loads((root / "evidence.json").read_text())["execution"]["state"], "incomplete")

    def test_unknown_variant_is_error(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ValueError):
                m.trqp_variant(Path(temp), "unrecognized")


if __name__ == "__main__":
    unittest.main()
