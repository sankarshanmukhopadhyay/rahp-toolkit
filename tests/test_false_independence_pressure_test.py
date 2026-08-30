from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "cross-spec" / "false-independence-sybil" / "pressure-test.yaml"


def load_review():
    return yaml.safe_load(FIXTURE.read_text(encoding="utf-8"))["review"]


def cases_by_name():
    return {case["name"]: case for case in load_review()["modeled_cases"]}


def test_fixture_preserves_core_false_independence_proposition():
    review = load_review()
    proposition = review["proposition"].lower()
    assert "must not increase assurance" in proposition
    assert "common effective control" in proposition
    assert "contextual identifier plurality" in proposition


def test_common_control_multiplicity_does_not_raise_assurance():
    case = cases_by_name()["common-control-multiplicity"]
    assert case["identity_count"] > 1
    assert case["evidence_source_count"] > 1
    assert case["effective_control_domains"] == 1
    assert case["expected_assurance_effect"] == "no-increase"
    assert case["expected_disposition"] == "reject-false-independence"


def test_genuinely_independent_evidence_is_not_suppressed():
    case = cases_by_name()["genuinely-independent-corroboration"]
    assert case["effective_control_domains"] == case["evidence_source_count"]
    assert case["independence_evidence"] == "established-independent"
    assert case["expected_assurance_effect"] == "policy-may-recognize-corroboration"


def test_legitimate_identifier_plurality_is_not_treated_as_attack_evidence():
    case = cases_by_name()["legitimate-contextual-identifiers"]
    assert case["identity_count"] > 1
    assert case["independence_evidence"] == "not-claimed"
    assert case["expected_assurance_effect"] == "no-increase-no-penalty"
    assert case["expected_disposition"] == "preserve-contextual-plurality"


def test_contextual_uniqueness_rejects_duplicate_without_universal_correlator():
    case = cases_by_name()["context-specific-uniqueness"]
    assert case["repeated_same_context"] is True
    assert case["expected_disposition"] == "reject-duplicate-contextual-exercise"
    assert case["prohibited_mechanism"] == "universal-cross-context-correlator"
    assert case["dpip_review"] == "warranted-if-nullifier-or-correlation-evidence-is-retained"


def test_unknown_independence_remains_bounded_uncertainty():
    case = cases_by_name()["unknown-independence"]
    assert case["effective_control_domains"] == "unknown"
    assert case["independence_evidence"] == "unavailable"
    assert case["expected_assurance_effect"] == "no-silent-increase"
    assert case["expected_disposition"] == "indeterminate-or-reduced-weight"


def test_fixture_separates_counts_from_effective_independence():
    cases = cases_by_name()
    common = cases["common-control-multiplicity"]
    independent = cases["genuinely-independent-corroboration"]

    assert common["evidence_source_count"] > independent["evidence_source_count"]
    assert common["expected_assurance_effect"] == "no-increase"
    assert independent["expected_assurance_effect"] == "policy-may-recognize-corroboration"


def test_visible_judgment_records_alternatives_and_residual_uncertainty():
    judgment = load_review()["judgment"]
    assert len(judgment["alternatives_considered"]) >= 2
    assert "issue 158" in judgment["chosen"].lower()
    assert "bounded uncertainty" in judgment["residual_uncertainty"].lower()


def test_control_routing_is_generic_and_non_normative():
    routing = load_review()["control_routing"]
    assert routing["assurance_owner"] == "rahp"
    capability = routing["required_capabilities"][0]
    assert capability["id"] == "privacy-preserving-contextual-uniqueness"
    assert capability["provider_binding"] == "non-normative"
    assert "zero-knowledge-proof-mechanism" in capability["candidate_provider_classes"]
    assert "issuer-independence" in capability["mechanism_success_does_not_establish"]
    assert "evidentiary-independence" in capability["mechanism_success_does_not_establish"]


def test_uniqueness_mechanism_pass_does_not_become_independence_pass():
    case = cases_by_name()["uniqueness-mechanism-success-with-residual-independence"]
    assert case["mechanism_result"] == "pass"
    assert case["mechanism_establishes"] == ["bounded-context-non-reuse"]
    assert case["independence_evidence"] == "unavailable"
    assert case["expected_assurance_effect"] == "bounded-sub-proposition-satisfied"
    assert case["expected_disposition"] == "retain-independence-uncertainty"
    assert case["overall_false_independence_result"] == "indeterminate"
    for claim in (
        "issuer-independence",
        "controller-independence",
        "governance-independence",
        "non-collusion",
        "evidentiary-independence",
    ):
        assert claim in case["mechanism_does_not_establish"]
