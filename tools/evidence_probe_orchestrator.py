#!/usr/bin/env python3
"""Execute registered evidence producers and emit an attempt ledger.

The orchestration rule is deliberately conservative:
- SATISFIED/ABSENT require an executed producer result.
- NOT_EVIDENCED is allowed only when a producer was attempted but could not
  materially exercise the surface, or when no applicable producer is registered
  and that unavailability is recorded explicitly.
- Merely omitting a probe is an orchestration defect, not evidence.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

VALID_RESULTS = {"SATISFIED", "ABSENT", "NOT_EVIDENCED"}
VALID_ATTEMPTS = {"EXECUTED", "ATTEMPTED_UNAVAILABLE", "NO_APPLICABLE_PRODUCER"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _run(command: list[str], cwd: Path) -> tuple[int, str, str]:
    p = subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)
    return p.returncode, p.stdout, p.stderr


def execute(plan: dict[str, Any], workspace: Path) -> dict[str, Any]:
    requirements = plan.get("requirements") or []
    producers = plan.get("producers") or {}
    ledger: list[dict[str, Any]] = []
    defects: list[str] = []

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
        cwd = workspace / str(producer.get("cwd") or ".")
        code, stdout, stderr = _run(command, cwd)
        if code != 0:
            ledger.append({
                "requirement_id": rid,
                "attempt_state": "ATTEMPTED_UNAVAILABLE",
                "result": "NOT_EVIDENCED",
                "reason": f"producer exited {code}",
                "producer": producer_id,
                "stdout": stdout[-4000:],
                "stderr": stderr[-4000:],
            })
            continue
        result = str(requirement.get("success_result") or "SATISFIED")
        if result not in VALID_RESULTS:
            defects.append(f"{rid}: invalid success_result {result}")
            continue
        ledger.append({
            "requirement_id": rid,
            "attempt_state": "EXECUTED",
            "result": result,
            "reason": str(requirement.get("success_reason") or "registered producer executed successfully"),
            "producer": producer_id,
            "stdout": stdout[-4000:],
            "stderr": stderr[-4000:],
        })

    seen = {entry["requirement_id"] for entry in ledger}
    planned = {str(item.get("id") or "") for item in requirements}
    missing = sorted(x for x in planned - seen if x)
    defects.extend(f"{rid}: no attempt ledger entry produced" for rid in missing)

    for entry in ledger:
        if entry["result"] == "NOT_EVIDENCED" and entry["attempt_state"] not in {
            "ATTEMPTED_UNAVAILABLE", "NO_APPLICABLE_PRODUCER"
        }:
            defects.append(f"{entry['requirement_id']}: NOT_EVIDENCED without an explicit attempt/unavailability state")
        if entry["result"] in {"SATISFIED", "ABSENT"} and entry["attempt_state"] != "EXECUTED":
            defects.append(f"{entry['requirement_id']}: {entry['result']} without executed producer")

    return {
        "schema": "rahp-evidence-probe-ledger/v1",
        "lineage": plan.get("lineage"),
        "target": plan.get("target"),
        "requirements": ledger,
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
