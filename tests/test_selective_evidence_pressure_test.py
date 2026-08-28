from pathlib import Path

import yaml


FIXTURE = Path("examples/cross-spec/selective-evidence/pressure-test.yaml")


def load_fixture():
    return yaml.safe_load(FIXTURE.read_text())


def cases_by_name(review):
    return {case["name"]: case for case in review["modeled_cases"]}


def test_review_identity_and_proposition():
    review = load_fixture()["review"]
    assert review["id"] == "SR-XSP-FI-007"
    assert "valid subset of evidence" in review["proposition"].lower()
    assert "materially change the relying decision" in review["proposition"].lower()


def test_valid_artifact_does_not_prove_current_completeness():
    case = cases_by_name(load_fixture()["review"])["valid-but-stale-credential"]
    assert case["artifact_valid"] is True
    assert case["later_state_material"] is True
    assert case["later_state_disclosed"] is False
    assert case["evidence_completeness"] is False


def test_material_contradiction_blocks_silent_completeness():
    case = cases_by_name(load_fixture()["review"])["contradictory-attestations-cherry-picked"]
    assert case["favorable_attestation_valid"] is True
    assert case["contradiction_material"] is True
    assert case["contradiction_disclosed"] is False
    assert case["expected_disposition"] == "represent-material-contradiction"


def test_derived_claim_preserves_material_source_limitations():
    case = cases_by_name(load_fixture()["review"])["derived-claim-with-omitted-source-limitation"]
    assert case["derived_artifact_valid"] is True
    assert case["source_limitation_material"] is True
    assert case["source_limitation_preserved"] is False
    assert case["evidence_completeness"] is False


def test_partial_relationship_history_is_not_automatically_complete():
    case = cases_by_name(load_fixture()["review"])["selective-relationship-history"]
    assert case["omitted_entries_material"] is True
    assert case["superseding_or_adverse_event_omitted"] is True
    assert case["expected_assurance_effect"] == "partial-history-not-complete-history"


def test_legitimate_selective_disclosure_is_preserved():
    case = cases_by_name(load_fixture()["review"])["legitimate-selective-disclosure"]
    assert case["disclosure_is_partial"] is True
    assert case["omitted_attributes_material"] is False
    assert case["omitted_history_material"] is False
    assert case["evidence_completeness_for_proposition"] is True
    assert case["privacy_minimization_preserved"] is True


def test_privacy_sensitive_completeness_does_not_force_full_disclosure():
    case = cases_by_name(load_fixture()["review"])["privacy-sensitive-contradiction-handling"]
    assert case["contradiction_material"] is True
    assert case["direct_full_disclosure_creates_privacy_or_linkability_risk"] is True
    assert case["expected_disposition"] == "indeterminate-and-consider-dpip"


def test_unknown_completeness_remains_bounded_uncertainty():
    review = load_fixture()["review"]
    case = cases_by_name(review)["unknown-completeness"]
    assert case["evidence_completeness"] == "unknown"
    assert case["expected_disposition"] == "indeterminate-or-reduced-weight"
    assert review["assurance"]["policy_gate"] == "AMBER"


def test_complete_relevant_disclosure_does_not_require_irrelevant_data():
    case = cases_by_name(load_fixture()["review"])["complete-relevant-disclosure"]
    assert case["material_source_limitations_preserved"] is True
    assert case["material_lifecycle_context_represented"] is True
    assert case["irrelevant_data_disclosed"] is False
    assert case["evidence_completeness_for_proposition"] is True


def test_fixture_separates_validity_completeness_and_materiality():
    review = load_fixture()["review"]
    controls = " ".join(review["assurance"]["positive_controls"]).lower()
    assert "artifact validity and evidence completeness" in controls
    assert "materiality" in controls
    assert "selective disclosure" in controls


def test_visible_judgment_rejects_both_extremes():
    review = load_fixture()["review"]
    alternatives = " ".join(review["judgment"]["alternatives_considered"]).lower()
    chosen = review["judgment"]["chosen"].lower()
    residual = review["judgment"]["residual_uncertainty"].lower()
    assert "valid presented artifact as complete evidence" in alternatives
    assert "maximal disclosure" in alternatives
    assert "validity and completeness as distinct" in chosen
    assert "dpip" in residual
