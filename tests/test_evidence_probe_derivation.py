import json
import tempfile
import unittest
from pathlib import Path

import yaml

from tools.evidence_probe_orchestrator import execute


class EvidenceProbeDerivationTests(unittest.TestCase):
    def _run(self, classes):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            script = root / "producer.py"
            capture = root / "capture.yaml"
            script.write_text(
                "import yaml\nfrom pathlib import Path\n" +
                repr({"requirements": {"ER-X": {"surfaces": {f"s{i}": {"classification": c} for i, c in enumerate(classes)}}}}) +
                "\n",
                encoding="utf-8",
            )
            # Write producer data via a tiny JSON-safe Python command so the orchestrator really executes it.
            payload = {"requirements": {"ER-X": {"surfaces": {f"s{i}": {"classification": c} for i, c in enumerate(classes)}}}}
            command = ["python", "-c", f"import yaml; open('capture.yaml','w').write(yaml.safe_dump({payload!r}))"]
            plan = {
                "requirements": [
                    {"id": "ER-X", "producer": "p", "evidence_file": "capture.yaml"},
                    {"id": "ER-Y", "producer": "p", "success_result": "SATISFIED"},
                ],
                "producers": {"p": {"command": command}},
            }
            result = execute(plan, root)
            return result

    def test_not_evidenced_comes_from_executed_output(self):
        result = self._run(["not-evidenced", "not-evidenced"])
        self.assertTrue(result["complete"])
        self.assertEqual(result["requirements"][0]["result"], "NOT_EVIDENCED")
        self.assertEqual(result["requirements"][0]["attempt_state"], "EXECUTED")
        self.assertEqual(result["producer_execution_count"], 1)

    def test_absent_requires_all_absent(self):
        result = self._run(["absent", "absent"])
        self.assertEqual(result["requirements"][0]["result"], "ABSENT")

    def test_observed_surface_is_satisfied(self):
        result = self._run(["fresh", "absent"])
        self.assertEqual(result["requirements"][0]["result"], "SATISFIED")


if __name__ == "__main__":
    unittest.main()
