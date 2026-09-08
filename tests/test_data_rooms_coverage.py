from pathlib import Path

from tools.capability_coverage import completeness, load, validate


PACK = Path("profiles/dtg/coverage/data-rooms.yaml")


def room_pack():
    return load(PACK)


def proposition(doc, proposition_id):
    return next(p for p in doc["coverage"]["propositions"] if p["id"] == proposition_id)


def test_room_pack_is_valid_and_complete():
    doc = room_pack()
    assert validate(doc) == []
    assert completeness(doc) == {
        "defined": 16,
        "assessed": 16,
        "satisfied": 4,
        "unsatisfied": 0,
        "indeterminate": 0,
        "evidence_required": 12,
        "not_applicable": 0,
    }


def test_room_pack_is_architectural_not_implementation_assurance():
    doc = room_pack()
    assert doc["coverage"]["maturity"] == "architectural"
    assert doc["coverage"]["maturity_posture"]["implementation"] == "EVIDENCE_REQUIRED"
    assert doc["coverage"]["maturity_posture"]["runtime_privacy"] == "EVIDENCE_REQUIRED"
    assert doc["coverage"]["maturity_posture"]["composition"] == "EVIDENCE_REQUIRED"
    for item in doc["coverage"]["propositions"]:
        assert item["assessed_at_maturity"] == "architectural"


def test_all_required_scenario_families_are_present():
    ids = {scenario["id"] for scenario in room_pack()["coverage"]["scenarios"]}
    assert ids == {
        "SC-ROOM-COMMUNITY-MEMORY-001",
        "SC-ROOM-FAMILY-PRIVATE-001",
        "SC-ROOM-BUSINESS-COLLAB-001",
        "SC-ROOM-RESILIENT-COMMUNITY-001",
        "SC-ROOM-MULTICONTEXT-AGENT-001",
    }


def test_architectural_satisfaction_is_bounded_to_explicit_design_claims():
    doc = room_pack()
    satisfied = {p["id"] for p in doc["coverage"]["propositions"] if p["judgment"] == "SATISFIED"}
    assert satisfied == {"P-ROOM-001", "P-ROOM-003", "P-ROOM-004", "P-ROOM-006"}


def test_private_membership_and_invitation_privacy_route_to_dpip():
    doc = room_pack()
    for pid in ("P-ROOM-007", "P-ROOM-008"):
        item = proposition(doc, pid)
        assert item["provider"] == "dpip"
        assert item["judgment"] == "EVIDENCE_REQUIRED"
        assert any("runtime" in requirement.lower() or "dpip" in requirement.lower()
                   for requirement in item["evidence_required"])


def test_runtime_and_composition_obligations_route_to_interop_lab():
    doc = room_pack()
    for pid in (
        "P-ROOM-002", "P-ROOM-005", "P-ROOM-009", "P-ROOM-010",
        "P-ROOM-012", "P-ROOM-013", "P-ROOM-014", "P-ROOM-015", "P-ROOM-016",
    ):
        item = proposition(doc, pid)
        assert item["provider"] == "interop-lab"
        assert item["judgment"] == "EVIDENCE_REQUIRED"


def test_operator_independence_requires_governance_judgment():
    item = proposition(room_pack(), "P-ROOM-011")
    assert item["pattern"] == "operator-independence"
    assert item["provider"] == "human-judgment"
    assert item["judgment"] == "EVIDENCE_REQUIRED"


def test_host_confidentiality_is_not_upgraded_to_runtime_privacy():
    doc = room_pack()
    confidentiality = proposition(doc, "P-ROOM-006")
    membership_privacy = proposition(doc, "P-ROOM-007")
    assert confidentiality["judgment"] == "SATISFIED"
    assert confidentiality["assessed_at_maturity"] == "architectural"
    assert membership_privacy["judgment"] == "EVIDENCE_REQUIRED"


def test_source_pins_match_reviewed_delta():
    baseline = room_pack()["coverage"]["baseline"]
    assert baseline["normative_source"]["revision"] == "84a4329a5f797dec9d240c83ab5d564c120dde8f"
    assert baseline["design_source"]["revision"] == "0a5897f0acf9e16eec8ee88ccb74d7b1afb0bd87"
