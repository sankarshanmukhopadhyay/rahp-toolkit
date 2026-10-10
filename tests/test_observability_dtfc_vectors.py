import json
import unittest
from pathlib import Path
from tools.observability_harm import evaluate_observability

class TestDTFCObservabilityVectors(unittest.TestCase):
    def test_pinned_synthetic_vectors(self):
        file = Path(__file__).resolve().parents[1] / "examples" / "observability-dtfc" / "synthetic-vectors-v1.json"
        payload = json.loads(file.read_text(encoding="utf-8"))
        self.assertEqual(payload["contract"], "dtfc-observability-synthetic-vectors/v1")
        self.assertEqual(payload["provenance"]["imported_blob_sha"], "d5844a78206ea442a23a2bdc0e9fdc4140485cb5")
        self.assertFalse(payload["provenance"]["deployment_evidence"])
        for vector in payload["vectors"]:
            with self.subTest(vector=vector["id"]):
                self.assertEqual(evaluate_observability(vector["events"]), vector["expected"])
