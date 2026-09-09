import copy
import json
import unittest
from pathlib import Path

from tools.validate_evidence_producer_result import validate_result


FIXTURE = Path(__file__).parent / "fixtures/portable-producer/data-room-runtime-result.json"
EXPECTED_PIN = {
    "repository": "OpenVTC/verifiable-trust-infrastructure",
    "revision": "56cd6e5b7116777f1d9734e76c9a7b0569870e19",
    "role": "implementation",
}


class PortableProducerGenericIngestionTests(unittest.TestCase):
    def fixture(self):
        return json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_lab_result_is_accepted_without_domain_specific_interpretation(self):
        doc = self.fixture()
        self.assertEqual(
            [],
            validate_result(
                doc,
                expected_producer="interop-lab:data-room-runtime",
                expected_source_pins=[EXPECTED_PIN],
            ),
        )
        # Domain observations remain opaque to RAHP. A producer may add specialist-
        # specific fields without changing the generic validation outcome.
        extended = copy.deepcopy(doc)
        extended["evidence"]["observations"][0]["specialist_private_field"] = {
            "arbitrary": ["domain", "semantics"]
        }
        self.assertEqual(
            [],
            validate_result(
                extended,
                expected_producer="interop-lab:data-room-runtime",
                expected_source_pins=[EXPECTED_PIN],
            ),
        )

    def test_valid_local_execution_does_not_become_terminal_assurance(self):
        doc = self.fixture()
        self.assertEqual("succeeded", doc["execution"]["status"])
        self.assertEqual("observed", doc["evidence"]["status"])
        self.assertIn("terminal assurance PASS", doc["claim_boundary"]["does_not_support"])
        self.assertNotIn("assurance_outcome", doc)
        self.assertEqual([], validate_result(doc, expected_producer="interop-lab:data-room-runtime"))

    def test_terminal_assurance_injection_is_rejected_even_for_valid_lab_result(self):
        doc = self.fixture()
        doc["assurance_outcome"] = "PASS"
        errors = validate_result(doc, expected_producer="interop-lab:data-room-runtime")
        self.assertTrue(any("terminal assurance fields" in error for error in errors), errors)

    def test_source_revision_change_invalidates_the_result(self):
        doc = self.fixture()
        changed_pin = dict(EXPECTED_PIN)
        changed_pin["revision"] = "f" * 40
        errors = validate_result(
            doc,
            expected_producer="interop-lab:data-room-runtime",
            expected_source_pins=[changed_pin],
        )
        self.assertTrue(any("source pin mismatch" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
