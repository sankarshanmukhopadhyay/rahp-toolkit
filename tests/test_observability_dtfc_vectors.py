import json
import hashlib
import unittest
from pathlib import Path
from tools.observability_harm import evaluate_observability

class TestDTFCObservabilityVectors(unittest.TestCase):
    def test_pinned_synthetic_vectors(self):
        file = Path(__file__).resolve().parents[1] / "examples" / "observability-dtfc" / "synthetic-vectors-v1.json"
        raw = file.read_bytes()
        git_blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\\0" + raw).hexdigest()
        self.assertEqual(git_blob, "d5844a78206ea442a23a2bdc0e9fdc4140485cb5")
        payload = json.loads(raw)
        self.assertEqual(payload["contract"], "dtfc-observability-synthetic-vectors/v1")
        self.assertFalse(payload["provenance"]["deployment_evidence"])
        for vector in payload["vectors"]:
            with self.subTest(vector=vector["id"]):
                self.assertEqual(evaluate_observability(vector["events"]), vector["expected"])
