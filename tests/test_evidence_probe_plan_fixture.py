import json
import tempfile
import unittest
from pathlib import Path

from tools.evidence_probe_orchestrator import execute


class EvidenceProbePlanFixtureTests(unittest.TestCase):
    def test_fixture_produces_complete_attempt_ledger(self):
        plan = json.loads(Path("tests/fixtures/evidence-probe-plan.json").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            result = execute(plan, Path(tmp))
        self.assertTrue(result["complete"])
        by_id = {x["requirement_id"]: x for x in result["requirements"]}
        self.assertEqual(by_id["ER-EXECUTED"]["attempt_state"], "EXECUTED")
        self.assertEqual(by_id["ER-UNAVAILABLE"]["attempt_state"], "NO_APPLICABLE_PRODUCER")


if __name__ == "__main__":
    unittest.main()
