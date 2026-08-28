from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "cross-spec" / "trust-laundering" / "pressure-test.yaml"


def load_review():
    return yaml.safe_load(FIXTURE.read_text(encoding="utf-8"))["review"]


def cases_by_name():
    return {case["name"]: case for case in load_review()["modeled_cases"]}


def test_fixture_preserves_trust_laundering_proposition_and_countercase():
    proposition = load_review()["proposition"].lower()
    assert "must not increase" in proposition
    assert "re-issued" in proposition
    assert "genuinely new independent evidence" in proposition


def test_affiliated_reissuance_does_not_raise_assurance():
    case = cases_by_name()["affiliated-reissuance"]
    assert case["artifact_count"] > case["underlying_evidence_sources"]
    assert case["new_independent_evidence"] is False
    assert case["expected_assurance_effect"] == "no-increase"
    assert case["expected_disposition"] == "preserve-source-ceiling"


def test_circular_reattestation_is_not_independent_corroboration():
    case = cases_by_name()["circular-reattestation"]
    assert case["lineage_cycle"] is True
    assert case["lineage_depth"] > 1
    assert case["underlying_evidence_sources"] == 1
    assert case["expected_disposition"] == "reject-circular-corroboration"


def test_multiple_artifact_forms_do_not_multiply_one_source():
    case = cases_by_name()["multiple-artifact-forms-one-source"]
    assert case["artifact_count"] == len(case["artifact_forms"])
    assert case["underlying_evidence_sources"] == 1
    assert case["new_independent_evidence"] is False
    assert case["expected_assurance_effect"] == "no-increase"
    assert case["expected_disposition"] == "deduplicate-evidentiary-substance"


def test_legitimate_intermediary_wrapping_is_permitted_when_lineage_is_preserved():
    case = cases_by_name()["intermediary-wrapping-lineage-preserved"]
    assert case["lineage_preserved"] is True
    assert case["expected_disposition"] == "allow-derived-artifact-with-lineage"
    assert case["expected_assurance_effect"] == "preserve-or-reduce-per-policy"


def test_genuinely_new_independent_evidence_may_raise_assurance():
    case = cases_by_name()["genuinely-new-independent-corroboration"]
    assert case["underlying_evidence_sources"] == 2
    assert case["new_independent_evidence"] is True
    assert case["independence_evidence"] == "established-independent"
    assert case["expected_assurance_effect"] == "policy-may-recognize-uplift"


def test_unknown_lineage_remains_bounded_uncertainty():
    case = cases_by_name()["unknown-or-obscured-lineage"]
    assert case["lineage_depth"] == "unknown"
    assert case["underlying_evidence_sources"] == "unknown"
    assert case["expected_assurance_effect"] == "no-silent-increase"
    assert case["expected_disposition"] == "indeterminate-or-reduced-weight"


def test_fixture_separates_artifact_count_lineage_depth_and_evidentiary_substance():
    case = cases_by_name()["multiple-artifact-forms-one-source"]
    assert case["artifact_count"] > case["lineage_depth"]
    assert case["lineage_depth"] > case["underlying_evidence_sources"]


def test_visible_judgment_rejects_both_automatic_uplift_and_permanent_cap():
    judgment = load_review()["judgment"]
    alternatives = " ".join(judgment["alternatives_considered"]).lower()
    assert "fresh assurance" in alternatives
    assert "permanently" in alternatives
    assert "traceability rather than assurance depth" in judgment["chosen"].lower()
    assert "bounded uncertainty" in judgment["residual_uncertainty"].lower()
