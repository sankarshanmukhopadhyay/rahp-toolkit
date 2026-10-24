"""Falsification tests for a demand-gated upstream review adapter decision."""
import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

SCRIPT = Path(__file__).resolve().parents[1] / "tools/upstream_review_consumer_decision.py"
spec = importlib.util.spec_from_file_location("review_consumer_decision", SCRIPT)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)


class ConsumerDecisionTests(unittest.TestCase):
    def test_missing_consumer_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(FileNotFoundError):
                probe.inspect_consumer(Path(tmp) / "missing.py")

    def test_direct_upstream_reference_is_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "consumer.py"
            path.write_text("def consume(record):\n    return 'rahp-spec-review/v1'\n")
            self.assertTrue(probe.inspect_consumer(path)["direct_spec_review_schema_reference"])

    def test_mutable_target_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "record.yaml"
            path.write_text(yaml.safe_dump({"schema": "rahp-spec-review/v1",
                                            "target": {"repository": "example/spec", "revision": "main"}}))
            with self.assertRaisesRegex(ValueError, "immutable"):
                probe.review(path)

    def test_foreign_record_family_is_not_upstream(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "record.yaml"
            path.write_text(yaml.safe_dump({"schema": "rahp-assessor-result/v1",
                                            "target": {"repository": "example/spec",
                                                       "revision": "a" * 40}}))
            with self.assertRaisesRegex(ValueError, "Not an authoritative"):
                probe.review(path)

    def test_no_automatic_assurance_is_inferred(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            upstream = base / "upstream"
            downstream = base / "downstream"
            for relative in probe.UPSTREAM_FILES.values():
                (upstream / relative).parent.mkdir(parents=True, exist_ok=True)
            initial = {"schema": "rahp-spec-review/v1", "target": {
                "repository": "example/vrc", "revision": "a" * 40},
                "findings": [{"id": "F-001", "status": "open"}, {"id": "F-002", "status": "open"}]}
            later = {"schema": "rahp-spec-review/v1", "target": {
                "repository": "example/vrc", "revision": "b" * 40},
                "findings": [{"id": "F-001", "status": "resolved"}, {"id": "F-002", "status": "open"}]}
            for name, data in [("baseline", initial), ("reassessed", later)]:
                (upstream / probe.UPSTREAM_FILES[name]).write_text(yaml.safe_dump(data))
            for rel in probe.DOWNSTREAM_CONSUMERS.values():
                path = downstream / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("def init_rahp(): pass\ndef init_security(): pass\n"
                                "def normalize_external(): pass\ndef validate_result(): pass\n")
            result = probe.decide(upstream, downstream)
            self.assertEqual(result["decision"], "no_adapter_for_inspected_consumers")
            self.assertIn("assurance PASS or automatic risk acceptance", result["not_claimed"])


if __name__ == "__main__":
    unittest.main()
