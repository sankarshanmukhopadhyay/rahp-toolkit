"""Source-pinned standalone TRQP replay negative and process-independence tests."""
from __future__ import annotations

import json
import importlib.util
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "standalone-trqp"
SPEC = importlib.util.spec_from_file_location("standalone_trqp_replay_qualification", EXAMPLE / "replay.py")
assert SPEC and SPEC.loader
trqp_replay = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(trqp_replay)


class TRQPSourcePinnedChallengeTests(unittest.TestCase):
    def test_independent_process_runs_agree_with_expected_fixture(self):
        outputs = [
            subprocess.check_output([sys.executable, str(EXAMPLE / "replay.py"), "--check"], cwd=ROOT, text=True, timeout=30)
            for _ in range(2)
        ]
        self.assertEqual(outputs[0], outputs[1])
        result = json.loads(outputs[0])
        self.assertEqual("verified", result["source_integrity"])
        self.assertEqual("review-required", result["overall_assurance"])
        self.assertEqual("not-assessed", result["runtime_authorization"])
        self.assertFalse(result["api_example"]["requested_time_matches"])

    def test_modified_retained_source_fails_integrity(self):
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp) / "standalone"
            shutil.copytree(EXAMPLE, root)
            source = root / "source" / "api.md.txt"
            source.write_bytes(source.read_bytes() + b"\\n# deliberately tampered fixture\\n")
            with self.assertRaisesRegex(ValueError, "mismatch"):
                trqp_replay.source_integrity(root)

    def test_expected_case_mutation_fails_replay_check(self):
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp) / "standalone"
            shutil.copytree(EXAMPLE, root)
            cases = root / "cases.json"
            rows = json.loads(cases.read_text())
            rows[0]["schema_valid"] = not rows[0]["schema_valid"]
            cases.write_text(json.dumps(rows))
            with self.assertRaisesRegex(ValueError, "Unexpected schema result"):
                trqp_replay.replay(root)

    def test_retained_source_pin_is_not_runtime_proof(self):
        result = trqp_replay.replay()
        expected = json.loads((EXAMPLE / "expected-replay.json").read_text())
        self.assertEqual(expected, result)
        self.assertNotEqual("PASS", result["overall_assurance"])
        self.assertEqual("not-assessed", result["authority_history"])


if __name__ == "__main__":
    unittest.main()
