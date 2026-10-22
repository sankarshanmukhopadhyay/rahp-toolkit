from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "control-consequence-assurance" / "cases.yaml"


def _records(path):
    return yaml.safe_load((ROOT / path).read_text())["records"]


def _fixture():
    return yaml.safe_load(FIXTURE.read_text())


def test_existing_method_chain_is_resolvable():
    controls = {r["id"]: r for r in _records("method/catalogue/control-patterns.yaml")}
    assurance = {r["id"]: r for r in _records("method/catalogue/assurance-patterns.yaml")}
    evidence = {r["id"]: r for r in _records("method/catalogue/evidence-patterns.yaml")}

    assert "CTP-RISK-01" in controls
    assert "ATP-RISK-01" in assurance
    assert "EVP-RISK-01" in evidence
    assert "CTP-RISK-01" in assurance["ATP-RISK-01"]["control_patterns"]
    assert "EVP-RISK-01" in assurance["ATP-RISK-01"]["evidence_patterns"]


def test_fixture_reuses_existing_controls_and_risks():
    controls = {r["id"] for r in _records("method/catalogue/control-patterns.yaml")}
    risks = {r["id"] for r in _records("method/catalogue/risk-patterns.yaml")}
    cases = _fixture()["cases"]

    assert len({case["target_control"] for case in cases}) >= 5
    for case in cases:
        assert case["target_control"] in controls
        assert set(case["introduced_or_amplified_risks"]) <= risks


def test_uniqueness_control_has_machine_readable_side_effects():
    control = next(r for r in _records("method/catalogue/control-patterns.yaml") if r["id"] == "CTP-ID-03")
    assert set(control["introduces_or_amplifies_risks"]) == {"RKP-EXC-02", "RKP-PRV-01"}


def test_renewal_case_carries_1106_actor_redistribution_evidence():
    case = next(c for c in _fixture()["cases"] if c["id"] == "CCA-001")
    assert case["source_context"] == "#1106 CRA-008"
    changes = {actor["actor"]: actor["exposure_change"] for actor in case["affected_actors"]}
    assert changes["holder"] == "increased"
    assert changes["relying-party"] == "reduced"
    assert case["disposition"] == "context_dependent_residual"


def test_materially_different_controls_are_pressure_tested():
    cases = {c["id"]: c for c in _fixture()["cases"]}
    assert cases["CCA-002"]["target_control"] == "CTP-ID-03"
    assert cases["CCA-003"]["target_control"] == "CTP-RED-01"
    assert cases["CCA-004"]["target_control"] == "CTP-DEL-02"
    assert cases["CCA-005"]["target_control"] == "CTP-AGT-01"


def test_unassessed_material_consequence_cannot_silently_pass():
    case = next(c for c in _fixture()["cases"] if c["id"] == "CCA-005")
    assert case["evidence_state"] == "insufficient"
    assert case["disposition"] == "insufficient_evidence"
    assert case["control_credit"] == "withheld"
    assert case["expected_assurance"] == "INDETERMINATE"


def test_no_case_requires_catalogue_proliferation():
    assert all(c["disposition"] != "candidate_distinct_reusable_risk" for c in _fixture()["cases"])
