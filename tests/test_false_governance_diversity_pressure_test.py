from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "cross-spec" / "false-governance-diversity" / "pressure-test.yaml"


def load_review():
    return yaml.safe_load(FIXTURE.read_text(encoding="utf-8"))["review"]


def cases_by_name():
    return {case["name"]: case for case in load_review()["modeled_cases"]}


def test_fixture_preserves_governance_independence_proposition():
    proposition = load_review()["proposition"].lower()
    assert "must not be treated as governance independence" in proposition
    assert "decisive control" in proposition
    assert "genuinely independent governance roots" in proposition


def test_nominal_issuer_diversity_under_common_control_gets_no_uplift():
    case = cases_by_name()["nominal-issuer-diversity-common-controller"]
    assert case["nominal_source_count"] > 1
    assert case["operator_count"] > 1
    assert case["effective_governance_domains"] == 1
    assert case["expected_assurance_effect"] == "no-diversity-uplift"
    assert case["expected_disposition"] == "reject-false-governance-diversity"


def test_common_policy_authority_defeats_nominal_community_diversity():
    case = cases_by_name()["branded-community-diversity-common-policy-authority"]
    assert case["nominal_source_count"] > 1
    assert case["decisive_authority"] == "common-mandatory-policy"
    assert case["effective_governance_domains"] == 1
    assert case["expected_assurance_effect"] == "no-governance-independence-uplift"


def test_operational_separation_is_not_governance_independence():
    case = cases_by_name()["operational-separation-common-decisive-root"]
    assert case["operator_count"] == 3
    assert case["shared_infrastructure"] is False
    assert case["effective_governance_domains"] == 1
    assert case["decisive_authority"] == "common-registry-decision"
    assert case["expected_disposition"] == "separate-operations-from-governance-independence"


def test_genuinely_independent_governance_roots_are_not_suppressed():
    case = cases_by_name()["genuinely-independent-governance-roots"]
    assert case["effective_governance_domains"] == case["nominal_source_count"]
    assert case["independence_evidence"] == "established-independent"
    assert case["expected_assurance_effect"] == "policy-may-recognize-diversity"


def test_unknown_governance_dependence_remains_bounded_uncertainty():
    case = cases_by_name()["unknown-governance-dependence"]
    assert case["effective_governance_domains"] == "unknown"
    assert case["independence_evidence"] == "unavailable"
    assert case["expected_assurance_effect"] == "no-silent-diversity-uplift"
    assert case["expected_disposition"] == "indeterminate-or-reduced-weight"


def test_fixture_does_not_equate_centralization_with_failure():
    excluded = " ".join(load_review()["scope"]["excluded"]).lower()
    assert "centralization is inherently a failure" in excluded
    assert "multiple governance roots" in excluded


def test_visible_judgment_records_both_false_diversity_and_false_capture_shortcuts():
    judgment = load_review()["judgment"]
    alternatives = " ".join(judgment["alternatives_considered"]).lower()
    assert "separately operated" in alternatives
    assert "shared infrastructure" in alternatives
    assert "bounded uncertainty" in judgment["residual_uncertainty"].lower()
