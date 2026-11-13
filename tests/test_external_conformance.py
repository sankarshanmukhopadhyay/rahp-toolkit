"""External adapter consumer-path and false-success conformance tests."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "tools/run_external_conformance.py"
ADAPTER = ROOT / "examples/external-conformance/adapter.py"


class ExternalConformanceTests(unittest.TestCase):
    def run_kit(self, adapter=ADAPTER, *args):
        p = subprocess.run([
            sys.executable, str(RUNNER), "--adapter", str(adapter),
            "--implementation", "external-fixture-adapter",
            "--implementation-version", "0.1", *args,
        ], cwd=ROOT, capture_output=True, text=True, check=False)
        return p, json.loads(p.stdout)

    def fake_adapter(self, directory, body):
        file = Path(directory) / "adapter.py"
        file.write_text("#!/usr/bin/env python3\n" + body, encoding="utf-8")
        file.chmod(0o755)
        return file

    def test_clean_external_adapter_passes_only_tested_surfaces(self):
        p, result = self.run_kit()
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertGreater(result["summary"]["PASS"], 10)
        self.assertEqual(result["summary"]["FAIL"], 0)
        self.assertEqual(result["summary"]["ERROR"], 0)
        self.assertIn("observe-source", result["untested_operations"])
        self.assertNotIn("validate-result", result["untested_operations"])
        self.assertTrue(all(x["status"] == "PASS" for x in result["results"]))

    def test_false_success_claim_is_detected(self):
        with tempfile.TemporaryDirectory() as td:
            fake = self.fake_adapter(td, 'import json\nprint(json.dumps({"valid": True}))\n')
            p, result = self.run_kit(fake)
            self.assertNotEqual(p.returncode, 0)
            self.assertGreater(result["summary"]["FAIL"], 0)
            self.assertEqual(result["summary"]["ERROR"], 0)
            self.assertTrue(any(item["operation"] == "validate-result" and item["status"] == "FAIL" for item in result["results"]))

    def test_missing_adapter_explicit(self):
        p, result = self.run_kit("/nonexistent/rahp-fixture-adapter")
        self.assertNotEqual(p.returncode, 0)
        self.assertEqual(result["results"][0]["operation"], "preflight")
        self.assertEqual(result["results"][0]["status"], "ERROR")

    def test_unsupported_contract_version_rejected_without_execution(self):
        p, result = self.run_kit(ADAPTER, "--revision", "9.9")
        self.assertNotEqual(p.returncode, 0)
        self.assertEqual(len(result["results"]), 1)
        self.assertIn("unsupported", result["results"][0]["detail"])

    def test_timeout_detected_without_false_pass(self):
        with tempfile.TemporaryDirectory() as td:
            fake = self.fake_adapter(td, "import time\ntime.sleep(1)\n")
            p, result = self.run_kit(fake, "--timeout", "0.01")
            self.assertNotEqual(p.returncode, 0)
            self.assertGreater(result["summary"]["ERROR"], 0)
            self.assertTrue(any("timeout" in (x["detail"] or "") for x in result["results"]))

    def test_report_is_deterministic(self):
        a, x = self.run_kit()
        b, y = self.run_kit()
        self.assertEqual(a.returncode, b.returncode)
        self.assertEqual(x, y)


if __name__ == "__main__":
    unittest.main()
