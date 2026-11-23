"""Verify the teaching replay fails closed and preserves source-only boundaries."""
import importlib.util
import json
import subprocess
import sys
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples/standalone-trqp"
spec = importlib.util.spec_from_file_location("standalone_trqp_replay", EXAMPLE / "replay.py")
replay = importlib.util.module_from_spec(spec)
spec.loader.exec_module(replay)


class StandaloneTRQPTests(unittest.TestCase):
    def test_retained_result_and_semantic_counterexample(self):
        result = replay.replay()
        self.assertEqual(result, json.loads((EXAMPLE / "expected-replay.json").read_text()))
        self.assertTrue(result["api_example"]["schema_valid"])
        self.assertFalse(result["api_example"]["requested_time_matches"])
        self.assertEqual(result["runtime_authorization"], "not-assessed")
        self.assertEqual(result["overall_assurance"], "review-required")

    def run_cli(self, root):
        return subprocess.run(
            [sys.executable, str(EXAMPLE / "replay.py"), "--root", str(root), "--check"],
            cwd=ROOT, capture_output=True, text=True, timeout=30,
        )

    def test_clean_checkout_cli_replay(self):
        run = self.run_cli(EXAMPLE)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(json.loads(run.stdout)["overall_assurance"], "review-required")

    def test_cli_missing_source_and_tampered_source_fail_closed(self):
        for operation in ("remove", "tamper"):
            with self.subTest(operation=operation), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp) / "example"
                shutil.copytree(EXAMPLE, root)
                source = root / "source/api.md.txt"
                if operation == "remove":
                    source.unlink()
                else:
                    source.write_text("tampered source", encoding="utf-8")
                run = self.run_cli(root)
                self.assertNotEqual(run.returncode, 0)
                self.assertRegex(run.stderr, "Missing or unsafe retained file|Git blob mismatch")

    def test_cli_expected_output_and_historical_revision_divergence(self):
        for mutation in ("output", "revision"):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp) / "example"
                shutil.copytree(EXAMPLE, root)
                if mutation == "output":
                    expected = root / "expected-replay.json"
                    data = json.loads(expected.read_text(encoding="utf-8"))
                    data["overall_assurance"] = "PASS"
                    expected.write_text(json.dumps(data), encoding="utf-8")
                    diagnostic = "Replay differs from retained expected result"
                else:
                    manifest = root / "source-manifest.json"
                    data = json.loads(manifest.read_text(encoding="utf-8"))
                    data["commit"] = "b" * 40
                    manifest.write_text(json.dumps(data), encoding="utf-8")
                    diagnostic = "Source URL disagrees with identity"
                run = self.run_cli(root)
                self.assertNotEqual(run.returncode, 0)
                self.assertIn(diagnostic, run.stderr)

    def test_cli_rejects_symlinked_local_retained_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "example"
            shutil.copytree(EXAMPLE, root)
            original = root / "source/api.md.txt"
            source_bytes = original.read_bytes()
            original.unlink()
            outside = Path(tmp) / "outside.txt"
            outside.write_bytes(source_bytes)
            original.symlink_to(outside)
            run = self.run_cli(root)
            self.assertNotEqual(run.returncode, 0)
            self.assertIn("Symlink retained path", run.stderr)

    def test_source_tampering_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "example"
            shutil.copytree(EXAMPLE, root)
            (root / "source/api.md.txt").write_text("changed source")
            with self.assertRaisesRegex(ValueError, "Git blob mismatch"):
                replay.replay(root)

    def test_negative_control_cannot_silently_become_valid(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "example"
            shutil.copytree(EXAMPLE, root)
            cases = json.loads((root / "cases.json").read_text())
            cases[1]["response"]["authority_id"] = "did:example:authority"
            (root / "cases.json").write_text(json.dumps(cases))
            with self.assertRaisesRegex(ValueError, "Unexpected schema result"):
                replay.replay(root)


if __name__ == "__main__":
    unittest.main()
