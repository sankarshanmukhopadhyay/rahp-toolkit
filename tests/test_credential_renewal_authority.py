from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "credential-renewal-authority" / "cases.yaml"


def _records(path):
    return yaml.safe_load((ROOT / path).read_text())["records"]


def _fixture():
    return yaml.safe_load(FIXTURE.read_text())


def test_renewal_assurance_reuses_existing_failure_mechanisms():
    risks = {r["id"] for r in _records("method/catalogue/risk-patterns.yaml")}
    mapped = set(_fixture()["portable_assurance"]["risk_patterns"])

    assert mapped == {"RKP-AUTH-02", "RKP-AUTH-05", "RKP-DEL-03"}
    assert mapped <= risks


def test_lifecycle_continuation_assurance_pattern_is_resolvable():
    assurance = {a["id"]: a for a in _records("method/catalogue/assurance-patterns.yaml")}
    controls = {c["id"] for c in _records("method/catalogue/control-patterns.yaml")}
    guardrails = {g["id"] for g in _records("method/catalogue/guardrail-patterns.yaml")}
    evidence = {e["id"] for e in _records("method/catalogue/evidence-patterns.yaml")}

    pattern = assurance["ATP-AUTH-03"]
    assert set(pattern["control_patterns"]) <= controls
    assert set(pattern["guardrail_patterns"]) <= guardrails
    assert set(pattern["evidence_patterns"]) <= evidence
    assert "unchanged claims" in pattern["failure_interpretation"].lower()
    assert "historical evidence" in pattern["expected_result"].lower()


def test_negative_renewal_vectors_never_allow_continuation():
    cases = {case["id"]: case for case in _fixture()["cases"]}
    required = {"CRA-001", "CRA-002", "CRA-003"}

    assert required <= cases.keys()
    for case_id in required:
        assert cases[case_id]["expected_decision"] in {"DENY", "INDETERMINATE"}

    assert cases["CRA-001"]["authority_evidence"] == "denied"
    assert cases["CRA-001"]["expected_decision"] == "DENY"
    assert cases["CRA-002"]["dependency_state"] == "unresolved"
    assert cases["CRA-003"]["dependency_state"] == "partial"


def test_positive_vector_requires_current_authority_and_satisfied_dependencies():
    positive = next(case for case in _fixture()["cases"] if case["id"] == "CRA-004")

    assert positive["expected_decision"] == "ALLOW"
    assert positive["authority_evidence"] == "established"
    assert positive["dependency_state"] == "satisfied"


def test_historical_evidence_is_not_destroyed_by_current_authority_decision():
    for case in _fixture()["cases"]:
        assert case["historical_evidence"] == "preserved"
