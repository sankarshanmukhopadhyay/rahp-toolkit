"""Bounded user-facing conformance tests for read-only result explanation."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from tools.explain_result import explain_file, render_markdown

ROOT = Path(__file__).resolve().parents[1]
VALID = ROOT / "tests/conformance/engine/valid-v12-assurance/result.json"
MINIMAL = ROOT / "tests/conformance/engine/valid-minimal/result.json"
CLI = ROOT / "tools/engine_contract.py"


class ExplanationTests(unittest.TestCase):
    def cli(self, *args):
        return subprocess.run([sys.executable, str(CLI), "explain", *map(str, args)],
                              cwd=ROOT, capture_output=True, text=True, check=False)

    def test_gap_cannot_become_assured(self):
        result = explain_file(VALID)
        self.assertEqual(result["evaluation"]["unresolved_count"], 1)
        self.assertEqual(result["evaluation"]["overall_assurance"], "not-derived")
        self.assertEqual(result["freshness"]["state"], "not-established")
        self.assertEqual(result["evaluation"]["residuals"][0]["missing"], ["lost-response-test"])
        self.assertEqual(result["decision"]["controller_terminal_outcome"], "not-established-by-normalized-result")

    def test_no_findings_does_not_prove_assurance(self):
        result = explain_file(MINIMAL)
        self.assertEqual(result["findings"], [])
        self.assertEqual(result["evaluation"]["state"], "not-recorded")
        self.assertEqual(result["evaluation"]["overall_assurance"], "not-derived")

    def test_cli_json_markdown_and_invalid(self):
        good = self.cli(VALID, "--format", "json")
        md = self.cli(VALID, "--format", "markdown")
        bad = self.cli(ROOT / "tests/conformance/engine/invalid-closure-revision/result.json")
        self.assertEqual(good.returncode, 0, good.stderr)
        self.assertEqual(md.returncode, 0, md.stderr)
        self.assertEqual(json.loads(good.stdout)["projection"], "rahp-result-explanation/v1")
        self.assertIn("assurance-gap", md.stdout)
        self.assertNotEqual(bad.returncode, 0)
        self.assertEqual(bad.stdout, "")

    def test_freshness_requires_correct_binding_and_basis(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "freshness.json"
            fixture = {"version": 1, "assessment_id": "TEST-V12-001",
                       "assessment_run_id": "RUN-1", "status": "retest-required",
                       "retest_required": True, "evaluated_at": "2026-11-12T00:00:00Z",
                       "basis": [{"kind": "evidence-change", "id": "EV-1", "effect": "requires-retest"}]}
            path.write_text(json.dumps(fixture), encoding="utf-8")
            valid = self.cli(VALID, "--freshness", path, "--run-id", "RUN-1")
            self.assertEqual(valid.returncode, 0, valid.stderr)
            self.assertEqual(json.loads(valid.stdout)["freshness"]["state"], "retest-required")
            self.assertNotEqual(self.cli(VALID, "--freshness", path).returncode, 0)
            self.assertNotEqual(self.cli(VALID, "--freshness", path, "--run-id", "WRONG").returncode, 0)
            fixture["status"] = "current"
            path.write_text(json.dumps(fixture), encoding="utf-8")
            self.assertNotEqual(self.cli(VALID, "--freshness", path, "--run-id", "RUN-1").returncode, 0)

    def test_documented_synthetic_freshness_walkthrough(self):
        fixture = ROOT / "examples/assurance-lineage/explanation-freshness-example.yaml"
        result = self.cli(VALID, "--freshness", fixture, "--run-id", "RUN-EXPLAIN-001")
        self.assertEqual(result.returncode, 0, result.stderr)
        view = json.loads(result.stdout)
        self.assertEqual(view["freshness"]["state"], "retest-required")
        self.assertEqual(view["freshness"]["verification"].split(";")[0], "caller-declared")
        self.assertEqual(view["evaluation"]["unresolved_count"], 1)

    def test_untrusted_markdown_escaped_and_inputs_unchanged(self):
        data = json.loads(MINIMAL.read_text(encoding="utf-8"))
        data["assessment"]["key"] = "<script>evil</script> **bold**"
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "result.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            content = path.read_bytes()
            rendered = render_markdown(explain_file(path))
            self.assertNotIn("<script>", rendered)
            self.assertNotIn("**bold**", rendered)
            self.assertEqual(path.read_bytes(), content)
            self.assertEqual(explain_file(path), explain_file(path))


if __name__ == "__main__":
    unittest.main()
