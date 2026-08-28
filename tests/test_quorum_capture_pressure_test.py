from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "cross-spec" / "quorum-capture" / "pressure-test.yaml"


def load_review():
    return yaml.safe_load(FIXTURE.read_text(encoding="utf-8"))["review"]


def cases_by_name():
    return {case["name"]: case for case in load_review()["modeled_cases"]}


def test_fixture_preserves_threshold_arithmetic_vs_legitimacy_proposition():
    proposition = load_review()["proposition"].lower()
    assert "must not automatically establish" in proposition
    assert "independent" in proposition
    assert "representative" in proposition
    assert "legitimate approval" in proposition


def test_captured_three_of_five_is_not_independent_quorum():
    case = cases_by_name()["captured-three-of-five"]
    assert case["approvals_counted"] >= case["threshold_required"]
    assert case["threshold_satisfied"] is True
    assert case["effective_controller_count_for_approvals"] == 1
    assert case["expected_disposition"] == "reject-arithmetic-as-independence"


def test_duplicate_roles_do_not_automatically_multiply_independent_actors():
    case = cases_by_name()["duplicate-influence-across-roles"]
    assert case["nominal_roles_approving"] == case["approvals_counted"]
    assert case["distinct_actors_approving"] < case["nominal_roles_approving"]
    assert case["one_actor_multiple_roles"] is True
    assert case["policy_requires_distinct_actors"] is True
    assert case["expected_legitimacy_effect"] == "threshold-not-substantively-met"


def test_stale_quorum_semantics_do_not_silently_survive_lifecycle_change():
    case = cases_by_name()["lifecycle-denominator-change"]
    assert case["configured_membership_count"] != case["current_membership_count"]
    assert case["governance_rule_version_at_configuration"] != case["current_governance_rule_version"]
    assert case["rule_recomputed_for_current_membership"] is False
    assert case["threshold_satisfied_under_stale_rule"] is True
    assert case["expected_disposition"] == "require-current-rule-re-evaluation"


def test_coordinated_abstention_can_defeat_representativeness_without_banning_abstention():
    case = cases_by_name()["coordinated-abstention"]
    assert case["threshold_satisfied"] is True
    assert case["coordinated_abstainers"] > 0
    assert case["representativeness_assumption_defeated"] is True
    assert case["expected_disposition"] == "evaluate-attendance-semantics-and-control"


def test_hidden_weighting_prevents_count_from_proving_legitimacy():
    case = cases_by_name()["hidden-weighting"]
    assert case["threshold_satisfied_by_count"] is True
    assert case["weights_disclosed"] is False
    assert len(set(case["approval_weights"])) > 1
    assert case["expected_legitimacy_effect"] == "count-insufficient"


def test_genuinely_independent_current_quorum_may_be_recognized():
    case = cases_by_name()["genuinely-independent-threshold-approval"]
    assert case["threshold_satisfied"] is True
    assert case["effective_controller_count_for_approvals"] == case["approvals_counted"]
    assert case["independence_evidence"] == "established-independent"
    assert case["governance_rule_current"] is True
    assert case["expected_legitimacy_effect"] == "policy-may-recognize-approval"


def test_legitimate_versioned_recomputed_quorum_change_is_preserved():
    case = cases_by_name()["legitimate-versioned-recomputed-threshold"]
    assert case["configured_membership_count"] != case["current_membership_count"]
    assert case["rule_recomputed_for_current_membership"] is True
    assert case["approvals_counted"] >= case["current_threshold_required"]
    assert case["expected_disposition"] == "allow-versioned-governance-rule"


def test_legitimate_disclosed_weighted_vote_is_not_classified_as_capture():
    case = cases_by_name()["legitimate-disclosed-weighted-vote"]
    assert case["weights_disclosed"] is True
    assert case["weights_policy_authorized"] is True
    assert case["weighted_threshold_satisfied"] is True
    assert case["expected_disposition"] == "allow-transparent-weighted-rule"


def test_unknown_independence_or_eligibility_remains_bounded_uncertainty():
    case = cases_by_name()["unknown-independence-or-eligibility"]
    assert case["threshold_satisfied"] is True
    assert case["eligibility_evidence"] == "incomplete"
    assert case["effective_controller_count_for_approvals"] == "unknown"
    assert case["expected_legitimacy_effect"] == "no-silent-legitimacy-upgrade"
    assert case["expected_disposition"] == "indeterminate-or-reduced-weight"


def test_visible_judgment_rejects_both_arithmetic_legitimacy_and_anti_threshold_rule():
    judgment = load_review()["judgment"]
    alternatives = " ".join(judgment["alternatives_considered"]).lower()
    assert "syntactically satisfied n-of-m" in alternatives
    assert "reject threshold governance" in alternatives
    assert "threshold arithmetic as one input" in judgment["chosen"].lower()
    assert "universal voting constitution" in judgment["residual_uncertainty"].lower()
