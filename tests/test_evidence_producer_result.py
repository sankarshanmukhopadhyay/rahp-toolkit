import copy
import unittest

from tools.validate_evidence_producer_result import validate_result


PIN = {"repository": "example/target", "revision": "a" * 40, "role": "implementation"}


def valid_result():
    return {
        "schema": "rahp-evidence-producer-result/v1",
        "producer": {
            "id": "example-producer-v1",
            "implementation": "example-producer",
            "repository": "example/evidence-producer",
            "revision": "b" * 40,
        },
        "obligation": {
            "proposition_key": "rahp-obligation:" + "c" * 20,
            "evidence_contract_key": "rahp-evidence-contract:" + "d" * 20,
            "evidence_requirement_ids": ["ER-EXAMPLE-AB"],
        },
        "source": {"pins": [PIN]},
        "execution": {
            "id": "run-001",
            "runner": "python example_runner.py",
            "timestamp": "2026-09-09T00:00:00Z",
            "determinism": "deterministic",
            "status": "succeeded",
        },
        "evidence": {
            "status": "observed",
            "evidence_class": "runtime-upstream-observation",
            "artifacts": [
                {
                    "name": "observation.json",
                    "media_type": "application/json",
                    "sha256": "e" * 64,
                    "provenance": {"producer_id": "example-producer-v1"},
                }
            ],
            "observations": [{"requirement_id": "ER-EXAMPLE-AB", "finding": "bounded-observation"}],
        },
        "claim_boundary": {
            "supports": ["ER-EXAMPLE-AB bounded runtime observation"],
            "does_not_support": ["terminal assurance PASS", "deployment-wide inference"],
            "limitations": ["single immutable implementation revision"],
            "residual_uncertainty": "Other deployments and revisions were not tested.",
        },
        "freshness": {
            "valid_against": [PIN],
            "invalidation_keys": ["source:example/target@" + "a" * 40],
        },
    }


class EvidenceProducerResultContractTests(unittest.TestCase):
    def test_valid_result_is_accepted(self):
        self.assertEqual([], validate_result(valid_result(), expected_producer="example-producer-v1", expected_source_pins=[PIN]))

    def test_evidence_incomplete_is_a_valid_fail_closed_result(self):
        doc = valid_result()
        doc["execution"]["status"] = "unavailable"
        doc["evidence"] = {
            "status": "evidence-incomplete",
            "evidence_class": "runtime-upstream-observation",
            "artifacts": [],
            "observations": [],
        }
        doc["claim_boundary"]["supports"] = []
        self.assertEqual([], validate_result(doc, expected_producer="example-producer-v1", expected_source_pins=[PIN]))

    def test_misattributed_artifact_fails_closed(self):
        doc = valid_result()
        doc["evidence"]["artifacts"][0]["provenance"]["producer_id"] = "different-producer"
        errors = validate_result(doc, expected_producer="example-producer-v1", expected_source_pins=[PIN])
        self.assertTrue(any("artifact producer provenance mismatch" in error for error in errors), errors)

    def test_source_pin_mismatch_marks_result_stale_for_requested_target(self):
        doc = valid_result()
        expected = [{"repository": "example/target", "revision": "f" * 40, "role": "implementation"}]
        errors = validate_result(doc, expected_producer="example-producer-v1", expected_source_pins=expected)
        self.assertTrue(any("source pin mismatch" in error for error in errors), errors)

    def test_local_success_cannot_encode_terminal_assurance(self):
        doc = valid_result()
        doc["assurance_outcome"] = "PASS"
        errors = validate_result(doc, expected_producer="example-producer-v1", expected_source_pins=[PIN])
        self.assertTrue(any("assurance_outcome" in error for error in errors), errors)

    def test_observed_evidence_requires_artifact_integrity(self):
        doc = valid_result()
        del doc["evidence"]["artifacts"][0]["sha256"]
        errors = validate_result(doc, expected_producer="example-producer-v1", expected_source_pins=[PIN])
        self.assertTrue(any("sha256" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
