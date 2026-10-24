"""Boundary-focused tests: upstream review is not downstream assurance."""
import importlib.util
import unittest
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / "tools/upstream_review_boundary.py"
spec = importlib.util.spec_from_file_location("upstream_review_boundary", MODULE)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)

BASE = {
    "schema": "rahp-spec-review/v1",
    "target": {"repository": "example/spec", "revision": "a" * 40},
    "findings": [{"id": "F-001", "status": "open", "risks": ["RK-AU01"]}],
}


class ReviewBoundary(unittest.TestCase):
    def test_original_is_not_modified(self):
        import copy
        original = copy.deepcopy(BASE)
        for case in ("mutable_target", "unknown_risk", "duplicate_finding",
                     "invalid_status", "unsupported_evidence_extension"):
            probe.mutate(original, case)
        self.assertEqual(original, BASE)

    def test_mutable_revision_is_falsification(self):
        self.assertEqual(probe.mutate(BASE, "mutable_target")["target"]["revision"], "main")

    def test_duplicate_identifier_is_falsification(self):
        result = probe.mutate(BASE, "duplicate_finding")
        self.assertEqual(len(result["findings"]), 2)
        self.assertEqual(result["findings"][0]["id"], result["findings"][1]["id"])

    def test_assurance_status_must_not_be_an_upstream_review_status(self):
        result = probe.mutate(BASE, "invalid_status")
        self.assertEqual(result["findings"][0]["status"], "PASS")

    def test_evidence_extension_is_not_silently_made_normative(self):
        result = probe.mutate(BASE, "unsupported_evidence_extension")
        self.assertIn("evidence", result["findings"][0])

    def test_absent_upstream_contract_fails_closed(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(FileNotFoundError):
                probe.evaluate(Path(d))


if __name__ == "__main__":
    unittest.main()
