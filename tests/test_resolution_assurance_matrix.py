from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "resolution-assurance-matrix.yaml"
DRARM = ROOT / "tools" / "resilience_assess.py"
DRARM_PROFILE = ROOT / "profiles" / "resilience" / "default.yaml"


def load_fixture():
    return yaml.safe_load(FIXTURE.read_text(encoding="utf-8"))


def case(case_id: str):
    return next(item for item in load_fixture()["cases"] if item["id"] == case_id)


def run_drarm(source_text: str) -> dict:
    with tempfile.TemporaryDirectory() as td:
        target = pathlib.Path(td) / "target"
        target.mkdir()
        (target / "resolver.py").write_text(source_text, encoding="utf-8")
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
                "example/resolution-fixture",
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
        return json.loads(result.read_text(encoding="utf-8"))


def test_authenticity_without_freshness_never_becomes_green():
    item = case("RES-AUTH-001")
    assert item["input"]["identifier_authenticity"] == "verified"
    assert item["input"]["freshness"] == "missing"
    assert item["expected"]["assurance_state"] == "indeterminate"
    assert "green" in item["expected"]["prohibited_states"]


def test_authentic_transport_without_recognition_never_becomes_green():
    item = case("RES-REC-001")
    assert item["input"]["transport_authenticity"] == "verified"
    assert item["input"]["recognition"] == "missing"
    assert item["expected"]["assurance_state"] == "indeterminate"


def test_version_binding_mismatch_is_rejected():
    item = case("RES-VER-001")
    assert item["input"]["requested_version"] != item["input"]["resolved_version"]
    assert item["expected"]["verification_result"] == "reject"


def test_positive_resolution_case_is_explicitly_bounded():
    item = case("RES-POS-001")
    for key in (
        "identifier_authenticity",
        "content_integrity",
        "freshness",
        "recognition",
        "version_applicability",
        "authorization_applicability",
    ):
        assert item["input"][key] == "verified"
    assert item["expected"]["assurance_state"] == "verified"
    assert item["expected"]["scope"] == "resolution-chain-only"


def test_recursive_resolution_without_bounds_surfaces_drarm_review():
    item = case("RES-DRARM-001")
    result = run_drarm(item["input"]["source_text"])
    by_risk = {finding["risk_id"]: finding for finding in result["findings"]}
    for risk_id in item["expected"]["risk_ids"]:
        assert risk_id in by_risk, result
        assert by_risk[risk_id]["status"] == item["expected"]["status"]


def test_bounded_recursive_resolution_supplies_static_control_evidence():
    item = case("RES-DRARM-002")
    result = run_drarm(item["input"]["source_text"])
    review_risks = {
        finding["risk_id"]
        for finding in result["findings"]
        if finding["status"] == "review-required"
    }
    for risk_id in item["expected"]["absent_review_for"]:
        assert risk_id not in review_risks, result
