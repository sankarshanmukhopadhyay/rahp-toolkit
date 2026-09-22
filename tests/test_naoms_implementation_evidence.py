from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "data" / "naoms-trust-tasks-evidence.yaml"


def load_record() -> dict:
    value = yaml.safe_load(RECORD.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_naoms_evidence_never_promotes_independence_to_conformance() -> None:
    record = load_record()
    classification = record["evidence_classification"]
    assert classification["implementation_independence"] == "plausible"
    assert classification["conformance"] == "not_established"
    assert classification["interoperability"] == "not_established"
    assert classification["endorsement_or_certification"] is False


def test_missing_public_source_pin_is_explicit() -> None:
    pin = load_record()["observation"]["public_source_pin"]
    assert pin["state"] == "unavailable"
    assert "must not invent" in pin["reason"].lower()


def test_threshold_and_cryptosuite_observations_have_durable_owners() -> None:
    observations = load_record()["observations"]
    assert observations["threshold_composition"]["durable_owner"].endswith("/issues/65")
    assert observations["cryptosuite_interoperability"]["evidence_owner"].endswith("/issues/238")


def test_registry_observations_remain_historical_and_bounded() -> None:
    registry = load_record()["observations"]["registry_maturity"]
    assert registry["reported_count_difference"]["disposition"] == "counting-method-difference-unresolved"
    assert registry["zero_candidate_or_standard_entries"]["disposition"] == "historical-informational-only"
    assert registry["durable_registry_epoch"]["source_pin"] == "bbe1ddc77ac31d6e09c5dd655a86976d80afd8fd"


def test_non_inference_rules_are_explicit() -> None:
    rules = set(load_record()["non_inference"])
    assert "implementation_independence_does_not_imply_conformance" in rules
    assert "local_conformance_does_not_imply_interoperability" in rules
    assert "historical_registry_observation_does_not_imply_current_registry_state" in rules
