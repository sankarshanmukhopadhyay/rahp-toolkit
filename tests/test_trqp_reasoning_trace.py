"""Connect the optional trace to the existing TRQP source replay."""
import importlib.util
import json
import unittest
from pathlib import Path

from tools.reasoning_trace import validate_trace

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples/standalone-trqp"
spec = importlib.util.spec_from_file_location("standalone_trqp_replay_trace", EXAMPLE / "replay.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class TRQPReasoningTraceTests(unittest.TestCase):
    def test_source_replay_supports_bounded_trace(self):
        replay = module.replay()
        trace = json.loads((EXAMPLE / "reasoning-trace-f002.json").read_text())
        self.assertTrue(replay["api_example"]["schema_valid"])
        self.assertFalse(replay["api_example"]["requested_time_matches"])
        self.assertEqual(replay["overall_assurance"], "review-required")
        self.assertEqual(trace["observations"][0]["result"], "NOT_SATISFIED")
        result = {"outcome": "INDETERMINATE", "evidence_used": ["ER-API-EXAMPLE"]}
        self.assertEqual(validate_trace(trace, result), [])


if __name__ == "__main__":
    unittest.main()
