from pathlib import Path

from tools.capability_coverage import completeness, load, validate


PACK = Path("profiles/dtg/coverage/persona.yaml")


def persona_pack():
    return load(PACK)


def proposition(doc, proposition_id):
    return next(p for p in doc["coverage"]["propositions"] if p["id"] == proposition_id)


def test_persona_pack_is_valid_and_complete():
    doc = persona_pack()
    assert validate(doc) == []
    summary = completeness(doc)
    assert summary == {
        "defined": 9,
        "assessed": 9,
        "satisfied": 3,
        "unsatisfied": 0,
        "indeterminate": 0,
        "evidence_required": 6,
        "not_applicable": 0,
    }


def test_persona_pack_is_bounded_to_implementation_maturity():
    doc = persona_pack()
    assert doc["coverage"]["maturity"] == "implementation"
    for item in doc["coverage"]["propositions"]:
        assert item["assessed_at_maturity"] == "implementation"


def test_context_isolation_has_negative_executable_evidence():
    item = proposition(persona_pack(), "P-PER-001")
    assert item["judgment"] == "SATISFIED"
    paths = {e.get("path") for e in item["evidence"]}
    assert "vta-service/tests/persona_trust_task.rs" in paths
    assert any("cannot" in requirement for requirement in item["evidence_required"])


def test_positive_disclosure_requires_preview_boundary_evidence():
    item = proposition(persona_pack(), "P-PER-002")
    assert item["judgment"] == "SATISFIED"
    assert any("preview" in e.get("claim", "").lower() for e in item["evidence"])
    assert any("bypass" in requirement for requirement in item["evidence_required"])


def test_atomic_resolution_uses_generic_not_persona_specific_pattern():
    item = proposition(persona_pack(), "P-PER-004")
    assert item["pattern"] == "atomic-resolution-integrity"
    assert item["judgment"] == "EVIDENCE_REQUIRED"


def test_correlation_routes_to_dpip_without_static_pass():
    item = proposition(persona_pack(), "P-PER-008")
    assert item["provider"] == "dpip"
    assert item["judgment"] == "EVIDENCE_REQUIRED"
    assert any("runtime" in requirement.lower() or "dpip" in requirement.lower()
               for requirement in item["evidence_required"])


def test_composed_agent_and_aggregation_claims_route_to_interop_lab():
    doc = persona_pack()
    for proposition_id in ("P-PER-007", "P-PER-009"):
        item = proposition(doc, proposition_id)
        assert item["provider"] == "interop-lab"
        assert item["judgment"] == "EVIDENCE_REQUIRED"
        assert item["evidence"] == []


def test_pinned_sources_are_explicit():
    baseline = persona_pack()["coverage"]["baseline"]
    assert baseline["normative_source"]["revision"] == "84a4329a5f797dec9d240c83ab5d564c120dde8f"
    assert baseline["implementation_source"]["revision"] == "0a5897f0acf9e16eec8ee88ccb74d7b1afb0bd87"
