from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "negative-assurance-matrix.yaml"
DRARM = ROOT / "tools" / "resilience_assess.py"
DRARM_PROFILE = ROOT / "profiles" / "resilience" / "default.yaml"


def load_fixture():
    return yaml.safe_load(FIXTURE.read_text(encoding="utf-8"))


def case(case_id: str):
    return next(item for item in load_fixture()["cases"] if item["id"] == case_id)


def test_matrix_covers_all_major_negative_assessment_lenses():
    lenses = {item["lens"] for item in load_fixture()["cases"]}
    assert {"rahp", "security", "composition", "drarm"} <= lenses


def test_existing_false_independence_and_quorum_capture_evidence_is_reused():
    refs = load_fixture()["authoritative_existing_fixtures"]
    for ref in refs:
        assert (ROOT / ref).is_file(), ref


def test_member_validity_does_not_become_collective_authority_green():
    item = case("CA-RAHP-001")
    given, expected = item["given"], item["expected"]
    assert given["individually_valid_member_evidence"] >= given["threshold_required"]
    assert given["collective_authority_evidence"] == "missing"
    assert expected["assurance_state"] == "indeterminate"
    assert expected["terminal_colour"] == "amber"
    assert "green" in expected["prohibited_states"]


def test_insufficient_subset_is_rejected_by_security_fixture():
    item = case("CA-SEC-001")
    assert item["given"]["valid_member_signatures_present"] < item["given"]["threshold_required"]
    assert item["expected"]["authorization_result"] == "reject"


def test_component_pass_never_synthesizes_missing_composition_rule():
    item = case("CA-CMP-001")
    assert set(item["given"]["component_results"]) == {"pass"}
    assert item["given"]["threshold_rule_evidence"] == "missing"
    assert item["expected"]["component_to_composition_upgrade"] is False
    assert item["expected"]["composition_state"] == "indeterminate"


def test_bounded_unknown_audience_is_not_bearer_permission():
    item = case("AUD-RAHP-001")
    assert item["given"]["enumerable_at_emit_time"] is False
    assert item["given"]["membership_predicate_required"] is True
    assert item["expected"]["authorization_result"] == "reject-widening"
    assert item["expected"]["assurance_state"] == "indeterminate"


def test_resolution_authenticity_does_not_imply_freshness_recognition_or_authorization():
    item = case("RES-RAHP-001")
    assert item["given"]["content_authenticity"] == "verified"
    assert item["given"]["freshness_evidence"] == "missing"
    assert item["given"]["recognition_evidence"] == "missing"
    assert item["given"]["authorization_evidence"] == "missing"
    prohibited = set(item["expected"]["prohibited_inferences"])
    assert "authentic-identifier-means-current" in prohibited
    assert "resolvable-means-recognized" in prohibited
    assert "recognized-means-authorized" in prohibited
    assert item["expected"]["assurance_state"] == "indeterminate"


def test_drarm_fixture_executes_and_surfaces_broadcast_amplification():
    item = case("CA-DRARM-001")
    with tempfile.TemporaryDirectory() as td:
        target = pathlib.Path(td) / "target"
        target.mkdir()
        source = target / item["given"]["source_file"]
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text(item["given"]["source_text"], encoding="utf-8")
        result = pathlib.Path(td) / "result.json"
        report = pathlib.Path(td) / "report.md"
        events = pathlib.Path(td) / "events.json"
        proc = subprocess.run(
            [
                sys.executable,
                str(DRARM),
                "--target",
                str(target),
                "--profile",
                str(DRARM_PROFILE),
                "--repository",
                "example/collective-authority-fixture",
                "--revision",
                "fixture",
                "--json",
                str(result),
                "--markdown",
                str(report),
                "--events",
                str(events),
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        assert proc.returncode == 0, proc.stdout
        data = json.loads(result.read_text(encoding="utf-8"))
        rows = [row for row in data["findings"] if row["risk_id"] == item["expected"]["risk_id"]]
        assert rows, data
        assert rows[0]["status"] == item["expected"]["status"]


def test_drarm_case_does_not_claim_authority_semantics():
    reason = case("CA-DRARM-001")["expected"]["reason"].lower()
    assert "does not decide" in reason
    assert "authority" in reason
