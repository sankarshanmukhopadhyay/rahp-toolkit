from pathlib import Path

import yaml


FIXTURE = Path("examples/cross-spec/collusion/pressure-test.yaml")


def load_review():
    return yaml.safe_load(FIXTURE.read_text())["review"]


def case(review, name):
    return next(item for item in review["modeled_cases"] if item["name"] == name)


def test_proposition_separates_actor_distinctness_from_independence():
    review = load_review()
    proposition = review["proposition"]
    assert "distinct actors" in proposition
    assert "independent corroboration" in proposition
    assert "coordinated behaviour" in proposition


def test_coordinated_distinct_actors_do_not_gain_independence_credit():
    review = load_review()
    item = case(review, "coordinated-cross-endorsement")
    assert item["distinct_actor_count"] == 3
    assert item["effective_controller_count"] == 3
    assert item["coordination_state"] == "established"
    assert item["evidence_paths_independent"] is False
    assert item["expected_assurance_effect"] == "no-independent-uplift"


def test_cartelized_cross_community_exclusion_is_not_independent_adverse_evidence():
    review = load_review()
    item = case(review, "cartelized-exclusion")
    assert item["communities_involved"] == 3
    assert item["coordination_state"] == "established"
    assert item["expected_assurance_effect"] == "no-cross-community-independence-credit"


def test_prearranged_threshold_keeps_arithmetic_distinct_from_decision_independence():
    review = load_review()
    item = case(review, "pre-arranged-threshold-approval")
    assert item["threshold_satisfied"] is True
    assert item["prearranged_vote"] is True
    assert item["policy_expects_independent_judgment"] is True
    assert item["expected_assurance_effect"] == "no-independent-decision-credit"


def test_separately_signed_negative_attestations_can_still_be_coordinated():
    review = load_review()
    item = case(review, "collusive-negative-attestations")
    assert item["separately_signed_attestations"] is True
    assert item["coordination_state"] == "established"
    assert item["evidence_paths_independent"] is False


def test_shared_interest_alone_does_not_prove_collusion():
    review = load_review()
    item = case(review, "aligned-interest-without-observed-coordination")
    assert item["strategic_interest_alignment"] == "high"
    assert item["coordination_state"] == "not-established"
    assert item["expected_assurance_effect"] == "no-collusion-finding-from-interest-alone"


def test_genuine_independent_agreement_remains_valid_countercase():
    review = load_review()
    item = case(review, "genuinely-independent-agreement")
    assert item["distinct_actor_count"] == 3
    assert item["effective_controller_count"] == 3
    assert item["evidence_paths_independent"] is True
    assert item["expected_assurance_effect"] == "policy-may-recognize-corroboration"


def test_disclosed_coalition_is_not_misrepresented_as_false_independence():
    review = load_review()
    item = case(review, "legitimate-disclosed-coalition")
    assert item["coordination_state"] == "explicit-and-disclosed"
    assert item["coalition_modeled_as_single_decision_unit"] is True
    assert item["claims_independent_corroboration"] is False
    assert item["expected_assurance_effect"] == "no-false-independence-defect"


def test_unknown_coordination_remains_bounded_uncertainty():
    review = load_review()
    item = case(review, "unknown-coordination")
    assert item["coordination_state"] == "unknown"
    assert item["evidence_paths_independent"] == "unknown"
    assert item["expected_assurance_effect"] == "no-silent-independence-upgrade"
    assert item["expected_disposition"] == "indeterminate-or-reduced-weight"


def test_fixture_explicitly_rejects_common_false_positive_rules():
    review = load_review()
    excluded = " ".join(review["scope"]["excluded"])
    assert "agreement" in excluded
    assert "shared strategic interest alone proves collusion" in excluded
    chosen = review["judgment"]["chosen"]
    assert "shared interest" in chosen
    assert "coalition" in chosen


def test_residual_uncertainty_rejects_universal_surveillance():
    review = load_review()
    residual = review["judgment"]["residual_uncertainty"]
    assert "should not fabricate intent" in residual
    assert "aligned incentives alone" in residual
    assert "universal surveillance" in residual
