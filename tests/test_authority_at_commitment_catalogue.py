from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]


def _records(path):
    return yaml.safe_load((ROOT / path).read_text())["records"]


def test_authority_at_commitment_risks_are_catalogued_and_guarded():
    risks = {r["id"]: r for r in _records("method/catalogue/risk-patterns.yaml")}
    guards = {g["id"]: g for g in _records("method/catalogue/guardrail-patterns.yaml")}

    required = {"RKP-AUTH-04", "RKP-AUTH-05", "RKP-AUTH-06", "RKP-AUTH-07"}
    assert required <= risks.keys()

    no_inference = set(guards["GRP-AUTH-01"]["risk_patterns"])
    current_authority = set(guards["GRP-AUTH-02"]["risk_patterns"])
    assert {"RKP-AUTH-04", "RKP-AUTH-06"} <= no_inference
    assert {"RKP-AUTH-04", "RKP-AUTH-05", "RKP-AUTH-07"} <= current_authority


def test_authority_at_commitment_requires_positive_evidence():
    text = (ROOT / "method/authority-at-commitment.md").read_text()
    assert "Positive authority evidence must establish the required propositions" in text
    assert "MUST NOT become PASS" in text
