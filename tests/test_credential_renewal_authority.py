from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "credential-renewal-authority" / "cases.yaml"


def _records(path):
    return yaml.safe_load((ROOT / path).read_text())["records"]


def _fixture():
    return yaml.safe_load(FIXTURE.read_text())


def _ids(path):
    return {record["id"] for record in _records(path)}


def test_renewal_assurance_reuses_existing_portable_patterns():
    fixture = _fixture()["portable_assurance"]
    catalogues = {
        "harm_patterns": "method/catalogue/harm-patterns.yaml",
        "risk_patterns": "method/catalogue/risk-patterns.yaml",
        "control_patterns": "method/catalogue/control-patterns.yaml",
        "guardrail_patterns": "method/catalogue/guardrail-patterns.yaml",
        "assurance_patterns": "method/catalogue/assurance-patterns.yaml",
        "evidence_patterns": "method/catalogue/evidence-patterns.yaml",
    }
    for field, path in catalogues.items():
        assert set(fixture[field]) <= _ids(path)

    assert {"RKP-AUTH-02", "RKP-PRV-06", "RKP-COMP-02", "RKP-EXC-02"} <= set(fixture["risk_patterns"])
    assert {"HRM-AUT-02", "HRM-AUT-05", "HRM-ACC-02", "HRM-PRV-02"} <= set(fixture["harm_patterns"])


def test_lifecycle_continuation_assurance_pattern_is_resolvable():
    assurance = {a["id"]: a for a in _records("method/catalogue/assurance-patterns.yaml")}
    controls = _ids("method/catalogue/control-patterns.yaml")
    guardrails = _ids("method/catalogue/guardrail-patterns.yaml")
    evidence = _ids("method/catalogue/evidence-patterns.yaml")

    pattern = assurance["ATP-AUTH-03"]
    assert set(pattern["control_patterns"]) <= controls
    assert set(pattern["guardrail_patterns"]) <= guardrails
    assert set(pattern["evidence_patterns"]) <= evidence
    assert "unchanged claims" in pattern["failure_interpretation"].lower()
    assert "historical evidence" in pattern["expected_result"].lower()


def test_original_negative_renewal_vectors_never_allow_continuation():
    cases = {case["id"]: case for case in _fixture()["cases"]}
    required = {"CRA-001", "CRA-002", "CRA-003"}
    assert required <= cases.keys()
    for case_id in required:
        assert cases[case_id]["expected_decision"] in {"DENY", "INDETERMINATE"}


def test_positive_vector_requires_current_authority_and_satisfied_dependencies():
    positive = next(case for case in _fixture()["cases"] if case["id"] == "CRA-004")
    assert positive["expected_decision"] == "ALLOW"
    assert positive["authority_evidence"] == "established"
    assert positive["dependency_state"] == "satisfied"


def test_lapse_is_not_silently_promoted_to_closure_withdrawal_or_continuation():
    case = next(case for case in _fixture()["cases"] if case["id"] == "CRA-005")
    assert case["lifecycle_event"] == "expired"
    assert case["holder_closure"] == "not_observed"
    assert case["issuer_withdrawal"] == "not_observed"
    assert case["expected_decision"] == "INDETERMINATE"


def test_coercion_and_supported_closure_are_distinguishable():
    cases = {case["id"]: case for case in _fixture()["cases"]}
    coerced, supported = cases["CRA-006"], cases["CRA-009"]
    assert coerced["expected_decision"] == "DENY"
    assert coerced["harm_disposition"] == "INDETERMINATE"
    assert coerced["voluntariness_evidence"] == "contradictory"
    assert supported["representative_authorization"] == "established"
    assert supported["accessible_participation"] == "established"
    assert supported["voluntariness_evidence"] == "established"
    assert supported["harm_disposition"] == "NO_ADDITIONAL_HARM_SIGNAL"


def test_demand_driven_renewal_with_missing_privacy_evidence_is_non_pass():
    case = next(case for case in _fixture()["cases"] if case["id"] == "CRA-007")
    assert case["renewal_trigger"] == "third_party_demand"
    assert case["privacy_evidence"] == "missing"
    assert case["expected_decision"] == "INDETERMINATE"
    assert {"timing", "relationship-or-credential-status-query"} <= set(case["observer_visible"])


def test_assurance_uplift_keeps_burden_transfer_visible_and_non_pass():
    case = next(case for case in _fixture()["cases"] if case["id"] == "CRA-008")
    assert case["renewal_trigger"] == "third_party_assurance_uplift"
    assert case["proportionality_evidence"] == "missing"
    assert case["alternative_path"] == "not_established"
    assert case["expected_decision"] == "INDETERMINATE"
    assert case["control_consequence"]["linked_method_issue"] == "#1089"
    assert "holder" in case["control_consequence"]["shifted_burden"].lower()


def test_historical_evidence_is_not_destroyed_or_promoted_to_current_state():
    for case in _fixture()["cases"]:
        assert case["historical_evidence"] == "preserved"
    assert all(case["expected_decision"] != "ALLOW" for case in _fixture()["cases"] if case["id"] != "CRA-004")
