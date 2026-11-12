import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tools.assurance_state import conclusion_transition, freshness_from_basis


class EvidenceFreshnessDeltaTests(unittest.TestCase):
    def test_requires_retest_dominates_potential(self):
        status, retest = freshness_from_basis([
            {"effect": "potential"},
            {"effect": "requires-retest"},
        ])
        self.assertEqual(status, "retest-required")
        self.assertTrue(retest)

    def test_invalidating_is_stale(self):
        status, retest = freshness_from_basis([{"effect": "invalidating"}])
        self.assertEqual(status, "stale")
        self.assertTrue(retest)

    def test_unknown_preserves_uncertainty(self):
        status, retest = freshness_from_basis([{"effect": "unknown"}])
        self.assertEqual(status, "indeterminate")
        self.assertTrue(retest)

    def test_no_material_change_is_current_only_with_explicit_basis(self):
        self.assertEqual(freshness_from_basis([{"effect": "none"}]), ("current", False))

    def test_empty_or_unsupported_freshness_basis_fails_closed(self):
        for basis in ([], None, [{"effect": "unsupported"}], [{}], ["none"]):
            with self.subTest(basis=basis), self.assertRaises(ValueError):
                freshness_from_basis(basis)

    def test_cli_cannot_report_current_for_invalid_basis(self):
        script = Path(__file__).resolve().parents[1] / "tools" / "assurance_state.py"
        with tempfile.TemporaryDirectory() as directory:
            record = Path(directory) / "freshness.json"
            for payload in ({}, {"basis": []}, {"basis": [{"effect": "unsupported"}]}):
                with self.subTest(payload=payload):
                    record.write_text(json.dumps(payload), encoding="utf-8")
                    result = subprocess.run(
                        [sys.executable, str(script), "freshness", str(record)],
                        capture_output=True, text=True, check=False,
                    )
                    self.assertNotEqual(result.returncode, 0)
                    self.assertNotIn('"status": "current"', result.stdout)
                    self.assertIn("freshness basis", result.stderr)

    def test_resolution_transition(self):
        self.assertEqual(conclusion_transition("finding", "controlled"), "resolved")

    def test_regression_transition(self):
        self.assertEqual(conclusion_transition("assured", "finding"), "regressed")

    def test_unchanged_transition(self):
        self.assertEqual(conclusion_transition("controlled", "controlled"), "unchanged")


if __name__ == "__main__":
    unittest.main()
