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


def _load_yaml(path):
    return yaml.safe_load((ROOT/path).read_text())


def test_experimental_risk_overlay_is_branch_scoped_and_non_promoting():
    overlay=_load_yaml("method/catalogue/experimental/decision-resolution-patterns.yaml")
    assert overlay["status"]=="experimental"
    assert overlay["stable_catalogue_boundary"] is False
    assert overlay["branch_constraint"]=="research/decision-resolution-assurance"
    ids={x["id"] for x in overlay["failure_patterns"]}
    assert {
        "EXP-DR-AUTH-LAUNDERING",
        "EXP-DR-DECISION-BASIS-CONFLATION",
        "EXP-DR-SILENT-RESOLUTION",
        "EXP-DR-FALSE-PERSISTENCE",
    } <= ids


def test_authority_laundering_reuses_existing_stable_rahp_patterns():
    overlay=_load_yaml("method/catalogue/experimental/decision-resolution-patterns.yaml")
    laundering=next(x for x in overlay["failure_patterns"] if x["id"]=="EXP-DR-AUTH-LAUNDERING")

    stable_files={
        "risk": _load_yaml("method/catalogue/risk-patterns.yaml"),
        "harm": _load_yaml("method/catalogue/harm-patterns.yaml"),
        "control": _load_yaml("method/catalogue/control-patterns.yaml"),
        "guardrail": _load_yaml("method/catalogue/guardrail-patterns.yaml"),
        "evidence": _load_yaml("method/catalogue/evidence-patterns.yaml"),
    }
    stable_ids={k:{x["id"] for x in v["records"]} for k,v in stable_files.items()}

    assert set(laundering["existing_risk_patterns"]) <= stable_ids["risk"]
    assert set(laundering["harm_patterns"]) <= stable_ids["harm"]
    assert set(laundering["control_patterns"]) <= stable_ids["control"]
    assert set(laundering["guardrail_patterns"]) <= stable_ids["guardrail"]
    assert set(laundering["evidence_patterns"]) <= stable_ids["evidence"]


def test_authority_laundering_cannot_be_satisfied_by_non_authority_signals():
    p=_load_yaml("examples/assurance/decision-resolution-experimental.yaml")
    props={x["id"]:x for x in p["propositions"]}
    forbidden=set(props["RAHP-DR-01"]["prohibited_substitutes"])
    assert {
        "peer-influence",
        "repetition",
        "consensus",
        "reputation",
        "capability",
        "discovery",
        "endorsement",
        "projection",
        "aggregation",
        "unrelated-authority",
    } <= forbidden
    assert props["RAHP-DR-01"]["failure_pattern"]=="EXP-DR-AUTH-LAUNDERING"


def test_decision_basis_conflation_and_silent_resolution_are_explicit_failures():
    p=_load_yaml("examples/assurance/decision-resolution-experimental.yaml")
    props={x["id"]:x for x in p["propositions"]}
    assert props["RAHP-DR-02"]["failure_pattern"]=="EXP-DR-DECISION-BASIS-CONFLATION"
    assert {
        "EXP-DR-SILENT-RESOLUTION",
        "EXP-DR-FALSE-PERSISTENCE",
    } <= set(props["RAHP-DR-03"]["failure_patterns"])


def test_experimental_candidates_do_not_collide_with_stable_catalogue_ids():
    overlay=_load_yaml("method/catalogue/experimental/decision-resolution-patterns.yaml")
    stable_paths=[
        "method/catalogue/risk-patterns.yaml",
        "method/catalogue/guardrail-patterns.yaml",
        "method/catalogue/evidence-patterns.yaml",
    ]
    stable_ids=set()
    for path in stable_paths:
        stable_ids |= {x["id"] for x in _load_yaml(path)["records"]}

    provisional=set()
    for record in overlay["failure_patterns"]:
        if record.get("provisional_catalogue_id"):
            provisional.add(record["provisional_catalogue_id"])
    for section in ("guardrail_candidates","evidence_candidates"):
        provisional |= {x["provisional_catalogue_id"] for x in overlay[section]}

    assert provisional
    assert provisional.isdisjoint(stable_ids)


def test_false_persistence_is_not_treated_as_safe_by_default():
    overlay=_load_yaml("method/catalogue/experimental/decision-resolution-patterns.yaml")
    false_persistence=next(x for x in overlay["failure_patterns"] if x["id"]=="EXP-DR-FALSE-PERSISTENCE")
    assert "HRM-ACC-01" in false_persistence["harm_patterns"]
    guardrails={x["id"]:x for x in overlay["guardrail_candidates"]}
    assert guardrails["EXP-GRP-DR-02"]["fail_behavior"]=="require-reassessment"


def test_experimental_overlay_preserves_upstream_provenance_without_dependency():
    overlay=_load_yaml("method/catalogue/experimental/decision-resolution-patterns.yaml")
    provenance=overlay["research_provenance"]
    assert provenance["normative_dependency"] is False
    assert any("SIMULATION_01_RUNBOOK.md" in x for x in provenance["sources"])
