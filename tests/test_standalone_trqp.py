"""Verify the teaching replay fails closed and preserves source-only boundaries."""
import importlib.util
import json
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
