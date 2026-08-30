import tempfile
import unittest
from pathlib import Path

from tools.evidence_probe_orchestrator import execute


class EvidenceProbeOrchestratorTests(unittest.TestCase):
    def test_no_producer_is_explicit_not_evidenced(self):
        plan = {"requirements": [{"id": "ER-X", "unavailable_reason": "target has no registered probe"}]}
        result = execute(plan, Path("."))
        self.assertTrue(result["complete"])
        entry = result["requirements"][0]
        self.assertEqual(entry["result"], "NOT_EVIDENCED")
        self.assertEqual(entry["attempt_state"], "NO_APPLICABLE_PRODUCER")

    def test_success_requires_executed_probe(self):
        with tempfile.TemporaryDirectory() as tmp:
            plan = {
                "requirements": [{"id": "ER-X", "producer": "p"}],
                "producers": {"p": {"command": ["python", "-c", "print('ok')"]}},
            }
            result = execute(plan, Path(tmp))
        self.assertTrue(result["complete"])
        self.assertEqual(result["requirements"][0]["attempt_state"], "EXECUTED")
        self.assertEqual(result["requirements"][0]["result"], "SATISFIED")

    def test_failed_probe_is_not_evidenced_but_attempted(self):
        with tempfile.TemporaryDirectory() as tmp:
            plan = {
                "requirements": [{"id": "ER-X", "producer": "p"}],
                "producers": {"p": {"command": ["python", "-c", "raise SystemExit(7)"]}},
            }
            result = execute(plan, Path(tmp))
        self.assertTrue(result["complete"])
        entry = result["requirements"][0]
        self.assertEqual(entry["attempt_state"], "ATTEMPTED_UNAVAILABLE")
        self.assertEqual(entry["result"], "NOT_EVIDENCED")

    def test_bad_registration_is_orchestration_defect(self):
        plan = {"requirements": [{"id": "ER-X", "producer": "missing"}], "producers": {}}
        result = execute(plan, Path("."))
        self.assertFalse(result["complete"])
        self.assertTrue(result["orchestration_defects"])

    def test_absent_requires_executed_probe(self):
        with tempfile.TemporaryDirectory() as tmp:
            plan = {
                "requirements": [{"id": "ER-X", "producer": "p", "success_result": "ABSENT"}],
                "producers": {"p": {"command": ["python", "-c", "print('none')"]}},
            }
            result = execute(plan, Path(tmp))
        self.assertEqual(result["requirements"][0]["attempt_state"], "EXECUTED")
        self.assertEqual(result["requirements"][0]["result"], "ABSENT")


if __name__ == "__main__":
    unittest.main()
