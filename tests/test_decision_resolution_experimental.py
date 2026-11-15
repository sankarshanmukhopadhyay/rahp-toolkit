from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]

def test_decision_resolution_experimental_profile_is_evidence_conservative():
    p=yaml.safe_load((ROOT/"examples/assurance/decision-resolution-experimental.yaml").read_text())
    assert p["status"]=="experimental"
    assert p["stable_release_boundary"] is False
    props={x["id"]:x for x in p["propositions"]}
    assert props["RAHP-DR-02"]["missing_basis_outcome"]=="INDETERMINATE"
    assert props["RAHP-DR-03"]["missing_resolution_evidence_outcome"]=="INDETERMINATE"
    forbidden=set(props["RAHP-DR-03"]["non_resolution_events"])
    assert {"peer_pressure","repetition","reputation","workflow_progression"} <= forbidden

def test_non_authority_resolution_cannot_masquerade_as_authority_change():
    p=yaml.safe_load((ROOT/"examples/assurance/decision-resolution-experimental.yaml").read_text())
    props={x["id"]:x for x in p["propositions"]}
    assert props["RAHP-DR-02"]["non_authority_categories_must_not_imply_authority_change"] is True

def test_branch_note_preserves_upstream_provenance_and_non_adoption():
    text=(ROOT/"method/decision-resolution-assurance-experimental.md").read_text()
    assert "SIMULATION_01_RUNBOOK.md" in text
    assert "does not adopt" in text
    assert "MUST NOT be treated as part of the stable RAHP release boundary" in text
