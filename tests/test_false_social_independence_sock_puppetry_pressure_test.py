from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "cross-spec" / "false-social-independence-sock-puppetry" / "pressure-test.yaml"


def load_review():
    return yaml.safe_load(FIXTURE.read_text(encoding="utf-8"))["review"]


def cases_by_name():
    return {case["name"]: case for case in load_review()["modeled_cases"]}


def test_fixture_preserves_false_social_independence_proposition_and_countercase():
    proposition = load_review()["proposition"].lower()
    assert "must not be interpreted as independent social evidence" in proposition
    assert "genuine independent support may be recognized" in proposition


def test_manufactured_endorsements_do_not_multiply_one_controller():
    case = cases_by_name()["manufactured-endorsement-cluster"]
    assert case["persona_count"] == case["social_evidence_count"]
    assert case["effective_controller_count"] == 1
    assert case["expected_corroboration_effect"] == "no-independent-uplift"
    assert case["expected_disposition"] == "collapse-to-effective-controller"


def test_persona_count_does_not_establish_community_consensus():
    case = cases_by_name()["apparent-community-consensus"]
    assert case["persona_count"] > case["effective_controller_count"]
    assert case["expected_consensus_effect"] == "no-legitimate-consensus-credit"
    assert case["expected_disposition"] == "reject-persona-count-as-consensus"


def test_separately_signed_negative_attestations_are_not_automatically_independent():
    case = cases_by_name()["coordinated-negative-attestations"]
    assert case["independently_signed"] is True
    assert case["effective_controller_count"] == 1
    assert case["social_evidence_count"] > case["effective_controller_count"]
    assert case["expected_disposition"] == "collapse-adverse-signals-to-effective-source"


def test_cross_community_spread_does_not_prove_independence():
    case = cases_by_name()["cross-community-sock-puppetry"]
    assert case["community_count"] > 1
    assert case["effective_controller_count"] == 1
    assert case["expected_disposition"] == "do-not-credit-community-spread-alone"


def test_genuinely_independent_social_support_may_receive_policy_weight():
    case = cases_by_name()["genuinely-independent-social-support"]
    assert case["effective_controller_count"] == case["persona_count"]
    assert case["independence_evidence"] == "established-independent"
    assert case["expected_corroboration_effect"] == "policy-may-recognize-uplift"


def test_legitimate_multi_persona_use_is_not_penalized():
    case = cases_by_name()["legitimate-multi-persona-use"]
    assert case["persona_count"] > 1
    assert case["claims_independent_social_support"] is False
    assert case["social_evidence_count"] == 0
    assert case["expected_disposition"] == "permit-contextual-personas-without-penalty"


def test_unknown_controller_independence_remains_bounded_uncertainty():
    case = cases_by_name()["unknown-controller-independence"]
    assert case["effective_controller_count"] == "unknown"
    assert case["independence_evidence"] == "unknown"
    assert case["expected_corroboration_effect"] == "no-silent-independent-uplift"
    assert case["expected_disposition"] == "indeterminate-or-reduced-weight"


def test_fixture_separates_personas_social_evidence_and_effective_control():
    case = cases_by_name()["manufactured-endorsement-cluster"]
    assert case["persona_count"] == 5
    assert case["social_evidence_count"] == 5
    assert case["effective_controller_count"] == 1


def test_visible_judgment_rejects_universal_correlation_and_identity_plurality_penalty():
    judgment = load_review()["judgment"]
    alternatives = " ".join(judgment["alternatives_considered"]).lower()
    assert "universal cross-context identity correlation" in alternatives
    assert "disallow multiple personas" in alternatives
    assert "effective-controller independence" in judgment["chosen"].lower()
    assert "dpip" in judgment["residual_uncertainty"].lower()
