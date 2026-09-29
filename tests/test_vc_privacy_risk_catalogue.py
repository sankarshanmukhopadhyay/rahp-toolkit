from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def _records(path):
    return yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))["records"]


def test_vc_privacy_gap_risks_are_catalogued_without_new_harms():
    risks = {r["id"]: r for r in _records("method/catalogue/risk-patterns.yaml")}
    harms = {h["id"]: h for h in _records("method/catalogue/harm-patterns.yaml")}

    required = {
        "RKP-PRV-05",
        "RKP-PRV-06",
        "RKP-PRV-07",
        "RKP-PRV-08",
        "RKP-PRV-09",
    }
    assert required <= risks.keys()

    expected_harms = {
        "RKP-PRV-05": {"HRM-PRV-02", "HRM-PRV-04"},
        "RKP-PRV-06": {"HRM-PRV-02", "HRM-PRV-03", "HRM-PRV-04"},
        "RKP-PRV-07": {"HRM-PRV-05", "HRM-AUT-03"},
        "RKP-PRV-08": {"HRM-PRV-02", "HRM-PRV-04"},
        "RKP-PRV-09": {"HRM-PRV-01", "HRM-PRV-03", "HRM-PRV-04"},
    }
    for risk_id, harm_ids in expected_harms.items():
        assert harm_ids <= set(risks[risk_id]["harm_patterns"])
        assert harm_ids <= harms.keys()


def test_status_query_observability_is_not_failure_response_disclosure():
    risks = {r["id"]: r for r in _records("method/catalogue/risk-patterns.yaml")}
    status_query = risks["RKP-PRV-06"]["description"].lower()
    failure_channel = risks["RKP-PRV-03"]["description"].lower()

    assert "act and pattern of status resolution" in risks["RKP-PRV-06"]["guardrail_requirement"]["rationale"].lower()
    assert "status provider" in status_query
    assert "responses reveal" in failure_channel
    assert status_query != failure_channel


def test_proof_correlation_covers_securing_metadata_not_only_payload_identifiers():
    risks = {r["id"]: r for r in _records("method/catalogue/risk-patterns.yaml")}
    description = risks["RKP-PRV-05"]["description"].lower()

    for term in ("proof material", "verification-method", "securing metadata", "payload"):
        assert term in description


def test_post_disclosure_use_is_distinct_from_initial_audience_expansion():
    risks = {r["id"]: r for r in _records("method/catalogue/risk-patterns.yaml")}
    post_use = risks["RKP-PRV-07"]["description"].lower()
    audience = risks["RKP-CRD-04"]["description"].lower()

    assert "legitimately disclosed" in post_use
    assert "retained, transferred, profiled" in post_use
    assert "forwarded, reused or presented" in audience


def test_new_privacy_risks_have_guardrail_and_control_coverage():
    guards = _records("method/catalogue/guardrail-patterns.yaml")
    controls = _records("method/catalogue/control-patterns.yaml")

    guarded = {risk for guard in guards for risk in guard.get("risk_patterns", [])}
    controlled = {risk for control in controls for risk in control.get("risk_patterns", [])}

    required = {f"RKP-PRV-{n:02d}" for n in range(5, 10)}
    assert required <= guarded
    assert required <= controlled


def test_dedicated_controls_exist_for_status_purpose_retention_and_issuer_pressure():
    controls = {c["id"]: c for c in _records("method/catalogue/control-patterns.yaml")}

    assert controls["CTP-PRV-05"]["risk_patterns"] == ["RKP-PRV-06"]
    assert "RKP-PRV-07" in controls["CTP-PRV-06"]["risk_patterns"]
    assert "RKP-PRV-09" in controls["CTP-PRV-07"]["risk_patterns"]
    assert {"RKP-PRV-08", "RKP-PRV-05"} <= set(controls["CTP-PRV-08"]["risk_patterns"])
