"""Contract-level consumer-interaction evidence experiment for #1029.

Synthetic observations are NOT proof of a live OpenVTC deployment or terminal RAHP
assurance. This checks the portable producer-result validation boundary only.
"""
import copy
import unittest

from tools.validate_evidence_producer_result import validate_result

PIN = {"repository": "example/consumer-interface", "revision": "a" * 40, "role": "implementation"}
PRODUCER = "synthetic-interaction-harness"


def sample():
    return {
        "schema": "rahp-evidence-producer-result/v1",
        "producer": {
            "id": PRODUCER, "implementation": "synthetic-browser-runner",
            "repository": "example/interaction-harness", "revision": "b" * 40,
        },
        "obligation": {
            "proposition_key": "rahp-obligation:" + "c" * 20,
            "evidence_contract_key": "rahp-evidence-contract:" + "d" * 20,
            "evidence_requirement_ids": ["ER-INTERACTION-001"],
        },
        "source": {"pins": [PIN], "runtime_identity": {"scenario": "synthetic-wallet-trigger-link"}},
        "execution": {
            "id": "synthetic-run-001", "runner": "synthetic-harness",
            "timestamp": "2026-10-15T00:00:00Z", "determinism": "deterministic",
            "status": "succeeded",
        },
        "evidence": {
            "status": "observed", "evidence_class": "consumer-interaction-observation",
            "artifacts": [{
                "name": "synthetic-interaction-trace.json", "media_type": "application/json",
                "sha256": "e" * 64, "provenance": {"producer_id": PRODUCER},
            }],
            "observations": [{
                "requirement_id": "ER-INTERACTION-001",
                "interaction_id": "synthetic-interaction-001",
                "component": "wallet", "action": "approve-presentation",
                "consumer_visible_state": "approved",
                "ui_observed_outcome": "success",
                "protocol_trace_ref": None,
                "authority_decision_ref": None,
                "interpretation": "UI-only observation; authorization not established",
            }],
        },
        "claim_boundary": {
            "supports": ["synthetic UI approval was observed"],
            "does_not_support": [
                "underlying protocol validation", "authorization or enforcement",
                "terminal RAHP assurance PASS",
            ],
            "limitations": ["no live OpenVTC deployment; no runtime authority trace"],
            "residual_uncertainty": "Protocol and authority outcomes are not evidenced.",
        },
        "freshness": {
            "valid_against": [PIN],
            "invalidation_keys": ["source:example/consumer-interface@" + "a" * 40],
        },
    }


class ConsumerInteractionEvidenceContractTests(unittest.TestCase):
    def check(self, record, pins=None):
        return validate_result(
            record, expected_producer=PRODUCER,
            expected_source_pins=[PIN] if pins is None else pins,
        )

    def test_synthetic_ui_observation_is_structurally_accepted(self):
        self.assertEqual([], self.check(sample()))

    def test_observation_does_not_grant_terminal_assurance(self):
        record = sample()
        record["assurance_outcome"] = "PASS"
        self.assertTrue(any("terminal assurance" in x for x in self.check(record)))

    def test_observed_without_integrity_artifact_rejected(self):
        record = sample()
        record["evidence"]["artifacts"] = []
        self.assertTrue(any("integrity-bearing artifact" in x for x in self.check(record)))

    def test_misattributed_artifact_rejected(self):
        record = sample()
        record["evidence"]["artifacts"][0]["provenance"]["producer_id"] = "other"
        self.assertTrue(any("provenance mismatch" in x for x in self.check(record)))

    def test_stale_target_pin_rejected(self):
        expected = [{**PIN, "revision": "f" * 40}]
        self.assertTrue(any("source pin mismatch" in x for x in self.check(sample(), expected)))

    def test_freshness_mismatch_rejected(self):
        record = sample()
        record["freshness"]["valid_against"] = [{**PIN, "revision": "f" * 40}]
        self.assertTrue(any("freshness.valid_against" in x for x in self.check(record)))

    def test_incomplete_evidence_is_accepted_but_not_assurance(self):
        record = sample()
        record["evidence"].update(status="evidence-incomplete", artifacts=[], observations=[])
        record["claim_boundary"]["supports"] = []
        self.assertEqual([], self.check(record))
        self.assertEqual("evidence-incomplete", record["evidence"]["status"])

    def test_ui_success_with_contradictory_runtime_annotation_is_not_interpreted(self):
        record = sample()
        record["evidence"]["observations"][0]["authority_decision"] = "denied"
        self.assertEqual([], self.check(record))
        # Deliberately establishes a limitation: this contract validator validates
        # provenance/shape, not UI-versus-authority semantic consistency.


if __name__ == "__main__":
    unittest.main()
