#!/usr/bin/env python3
"""Execute registered evidence producers and emit an attributable attempt ledger.

An unmet evidence requirement is legitimate only when the lineage records an
attempt or an explicit no-producer determination. Producer success is not itself
evidence sufficiency: when an evidence file is declared, the result is derived
from the producer's per-requirement surface classifications.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

import yaml

VALID_RESULTS = {"SATISFIED", "ABSENT", "NOT_EVIDENCED"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_structured(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    return json.loads(text) if path.suffix.lower() == ".json" else yaml.safe_load(text)


def _run(command: list[str], cwd: Path) -> tuple[int, str, str]:
    p = subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)
    return p.returncode, p.stdout, p.stderr


def derive_requirement_result(evidence_path: Path, requirement_id: str) -> tuple[str, list[str]]:
    doc = load_structured(evidence_path)
    req = (doc.get("requirements") or {}).get(requirement_id) if isinstance(doc, dict) else None
    if not isinstance(req, dict):
        raise ValueError(f"{requirement_id}: producer output has no matching requirement")
    surfaces = req.get("surfaces")
    if not isinstance(surfaces, dict) or not surfaces:
        raise ValueError(f"{requirement_id}: producer output has no surface classifications")
    classes = sorted({str(item.get("classification") or "").lower() for item in surfaces.values() if isinstance(item, dict)})
    if not classes or "" in classes:
        raise ValueError(f"{requirement_id}: incomplete surface classification")
    if set(classes) == {"not-evidenced"}:
        return "NOT_EVIDENCED", classes
    if set(classes) == {"absent"}:
        return "ABSENT", classes
    return "SATISFIED", classes


def execute(plan: dict[str, Any], workspace: Path) -> dict[str, Any]:
    requirements = plan.get("requirements") or []
    producers = plan.get("producers") or {}
    ledger: list[dict[str, Any]] = []
    defects: list[str] = []
    producer_runs: dict[str, tuple[int, str, str]] = {}

    for requirement in requirements:
        rid = str(requirement.get("id") or "").strip()
        producer_id = str(requirement.get("producer") or "").strip()
        if not rid:
            defects.append("requirement without id")
            continue
        if not producer_id:
            ledger.append({
                "requirement_id": rid,
                "attempt_state": "NO_APPLICABLE_PRODUCER",
                "result": "NOT_EVIDENCED",
                "reason": str(requirement.get("unavailable_reason") or "no applicable producer registered"),
                "producer": None,
                "attribution": requirement.get("attribution"),
            })
            continue

        producer = producers.get(producer_id)
        if not isinstance(producer, dict):
            defects.append(f"{rid}: referenced producer {producer_id} is not registered")
            continue
        command = producer.get("command")
        if not isinstance(command, list) or not all(isinstance(x, str) for x in command):
            defects.append(f"{rid}: producer {producer_id} has invalid command")
            continue

        if producer_id not in producer_runs:
            cwd = workspace / str(producer.get("cwd") or ".")
            producer_runs[producer_id] = _run(command, cwd)
        code, stdout, stderr = producer_runs[producer_id]
        base = {
            "requirement_id": rid,
            "producer": producer_id,
            "producer_revision": producer.get("revision"),
            "attribution": producer.get("attribution") or requirement.get("attribution"),
            "stdout": stdout[-4000:],
            "stderr": stderr[-4000:],
        }
        if code != 0:
            ledger.append({**base, "attempt_state": "ATTEMPTED_UNAVAILABLE", "result": "NOT_EVIDENCED", "reason": f"producer exited {code}"})
            continue

        evidence_file = requirement.get("evidence_file")
        if evidence_file:
            evidence_path = workspace / str(evidence_file)
            try:
                result, classes = derive_requirement_result(evidence_path, str(requirement.get("evidence_requirement_id") or rid))
            except Exception as exc:
                defects.append(f"{rid}: executed producer output invalid: {exc}")
                continue
            ledger.append({
                **base,
                "attempt_state": "EXECUTED",
                "result": result,
                "reason": "derived from executed producer surface classifications",
                "surface_classifications": classes,
                "evidence_file": str(evidence_file),
            })
            continue

        result = str(requirement.get("success_result") or "SATISFIED")
        if result not in VALID_RESULTS:
            defects.append(f"{rid}: invalid success_result {result}")
            continue
        ledger.append({**base, "attempt_state": "EXECUTED", "result": result, "reason": str(requirement.get("success_reason") or "registered producer executed successfully")})

    seen = {entry["requirement_id"] for entry in ledger}
    planned = {str(item.get("id") or "") for item in requirements}
    defects.extend(f"{rid}: no attempt ledger entry produced" for rid in sorted(x for x in planned - seen if x))

    for entry in ledger:
        if entry["result"] == "NOT_EVIDENCED" and entry["attempt_state"] == "EXECUTED" and not entry.get("surface_classifications"):
            defects.append(f"{entry['requirement_id']}: executed NOT_EVIDENCED lacks producer classification evidence")
        if entry["result"] in {"SATISFIED", "ABSENT"} and entry["attempt_state"] != "EXECUTED":
            defects.append(f"{entry['requirement_id']}: {entry['result']} without executed producer")

    return {
        "schema": "rahp-evidence-probe-ledger/v1",
        "lineage": plan.get("lineage"),
        "target": plan.get("target"),
        "requirements": ledger,
        "producer_execution_count": len(producer_runs),
        "orchestration_defects": defects,
        "complete": not defects,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("plan", type=Path)
    ap.add_argument("--workspace", type=Path, default=Path("."))
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    plan = load_json(args.plan)
    result = execute(plan, args.workspace.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return 0 if result["complete"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
