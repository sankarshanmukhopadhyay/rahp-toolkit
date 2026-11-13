#!/usr/bin/env python3
"""Run bounded RAHP conformance fixtures against a trusted external executable.

A report describes tested operations only; it is not certification, assurance
acceptance, or evidence of runtime deployment behavior.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

import yaml

ROOT = Path(__file__).resolve().parent.parent
OPERATIONS = ("validate-result", "retention-plan", "correlate-trigger")
REPORT = "rahp-external-conformance-report/v1"


def invoke(adapter: Path, operation: str, fixture: Path, timeout: float):
    try:
        proc = subprocess.run(
            [str(adapter), operation, str(fixture), "--contract-root", str(ROOT)],
            cwd=ROOT, capture_output=True, text=True, timeout=timeout,
            check=False, stdin=subprocess.DEVNULL,
        )
    except subprocess.TimeoutExpired:
        return None, "adapter timeout"
    except OSError:
        return None, "adapter could not be executed"
    if proc.returncode != 0:
        return None, f"adapter exited nonzero ({proc.returncode})"
    try:
        return json.loads(proc.stdout), None
    except json.JSONDecodeError:
        return None, "adapter returned non-JSON output"


def required_retention(result: dict, policy: dict) -> dict:
    actions = []
    for evidence in result["evidence"]:
        cls = evidence["class"]
        spec = policy["classes"][cls]
        repository = spec["repository"]
        actions.append({
            "id": evidence["id"], "class": cls, "repository": repository,
            "retention_days": spec.get("default_retention_days"),
            "action": "commit" if repository == "allowed" else (
                "manifest-only" if repository == "manifest-only" else "do-not-commit"),
        })
    return {
        "policy": policy["id"], "assessment": result["assessment"]["id"],
        "actions": actions,
    }


def evaluate(adapter: Path, timeout: float) -> list[dict]:
    records = []
    policy = yaml.safe_load((ROOT / "method/evidence-retention.yaml").read_text(encoding="utf-8"))
    for folder in sorted((ROOT / "tests/conformance/engine").iterdir()):
        if not folder.is_dir():
            continue
        fixture = folder / "result.json"
        expected = folder / "expected.yaml"
        if not fixture.is_file() or not expected.is_file():
            continue
        declared = yaml.safe_load(expected.read_text(encoding="utf-8"))
        answer, error = invoke(adapter, "validate-result", fixture, timeout)
        valid = declared["valid"]
        passed = error is None and isinstance(answer, dict) and type(answer.get("valid")) is bool and answer["valid"] == valid
        records.append({
            "operation": "validate-result", "fixture": fixture.relative_to(ROOT).as_posix(),
            "status": "ERROR" if error else ("PASS" if passed else "FAIL"),
            "detail": error or (None if passed else "validation result disagrees with fixture expectation"),
        })
        if valid:
            output, err = invoke(adapter, "retention-plan", fixture, timeout)
            target = required_retention(json.loads(fixture.read_text(encoding="utf-8")), policy)
            ok = err is None and output == target
            records.append({
                "operation": "retention-plan", "fixture": fixture.relative_to(ROOT).as_posix(),
                "status": "ERROR" if err else ("PASS" if ok else "FAIL"),
                "detail": err or (None if ok else "retention decision disagrees with policy"),
            })
    for folder in sorted((ROOT / "tests/conformance/lifecycle").iterdir()):
        if not folder.is_dir():
            continue
        fixture = folder / "input.json"
        expected = folder / "expected.json"
        if not fixture.is_file() or not expected.is_file():
            continue
        answer, error = invoke(adapter, "correlate-trigger", fixture, timeout)
        target = json.loads(expected.read_text(encoding="utf-8"))
        passed = error is None and answer == target
        records.append({
            "operation": "correlate-trigger", "fixture": fixture.relative_to(ROOT).as_posix(),
            "status": "ERROR" if error else ("PASS" if passed else "FAIL"),
            "detail": error or (None if passed else "trigger correlation disagrees with fixture"),
        })
    return records


def run(adapter: Path, implementation: str, implementation_version: str,
        contract: str, revision: str, result_schema: int, timeout: float) -> tuple[dict, int]:
    version = yaml.safe_load((ROOT / "method/versioning.yaml").read_text(encoding="utf-8"))
    declared = version["contracts"]
    report = {
        "format": REPORT,
        "authority": "derived fixture evidence; not conformance certification or assurance PASS",
        "implementation": {"id": implementation, "version": implementation_version},
        "contract": {"family": contract, "revision": revision, "result_schema": result_schema},
        "operations": list(OPERATIONS),
        "results": [],
        "summary": {"PASS": 0, "FAIL": 0, "ERROR": 0, "NOT_TESTED": 0},
        "untested_operations": sorted(
            x["id"] for x in yaml.safe_load(
                (ROOT / "method/engine-contract.yaml").read_text(encoding="utf-8")
            )["operations"] if x["id"] not in OPERATIONS
        ),
        "limitations": [
            "No independent assessment of an implementation's claimed identity or provenance.",
            "Fixtures cover selected operations, not complete engine conformance.",
            "Running an adapter executes user-selected local code; only run trusted executables.",
        ],
    }
    reasons = []
    if not implementation.strip() or not implementation_version.strip():
        reasons.append("implementation identifier and version must be nonempty")
    if not (contract == declared["engine"] and revision == str(declared["engine_revision"])
            and result_schema == declared["result_schema"]):
        reasons.append("unsupported engine family/revision or result schema")
    if timeout <= 0 or timeout > 120:
        reasons.append("timeout must be between 0 and 120 seconds")
    if not adapter.is_file():
        reasons.append("adapter executable not found")
    elif not __import__("os").access(adapter, __import__("os").X_OK):
        reasons.append("adapter must be executable")
    if reasons:
        report["results"].append({"operation": "preflight", "fixture": None, "status": "ERROR",
                                  "detail": "; ".join(reasons)})
    else:
        report["results"] = evaluate(adapter, timeout)
    for result in report["results"]:
        report["summary"][result["status"]] += 1
    return report, (0 if report["results"] and all(x["status"] == "PASS" for x in report["results"]) else 1)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--adapter", type=Path, required=True, help="trusted executable; no shell invocation")
    parser.add_argument("--implementation", required=True)
    parser.add_argument("--implementation-version", required=True)
    parser.add_argument("--contract", default="rahp-engine-contract-v1")
    parser.add_argument("--revision", default="1.3")
    parser.add_argument("--result-schema", type=int, default=1)
    parser.add_argument("--timeout", type=float, default=10)
    args = parser.parse_args()
    report, status = run(
        args.adapter.resolve(), args.implementation, args.implementation_version,
        args.contract, args.revision, args.result_schema, args.timeout,
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return status


if __name__ == "__main__":
    raise SystemExit(main())
