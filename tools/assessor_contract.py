#!/usr/bin/env python3
"""RAHP-owned portable specialist-assessor contract validator."""
from __future__ import annotations
import argparse, json, pathlib
from typing import Any
import jsonschema

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "method" / "schema" / "assessor-result.schema.json"


def validate_result(value: dict[str, Any]) -> list[str]:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    errors = []
    for exc in jsonschema.Draft202012Validator(schema).iter_errors(value):
        loc = ".".join(str(x) for x in exc.absolute_path) or "<root>"
        errors.append(f"{loc}: {exc.message}")
    return errors


def normalize_external(
    *,
    assessor: str,
    assessment_id: str,
    outcome: str,
    reason_code: str,
    evidence_used: list[str],
    residual_risk: str,
    action_required: str,
    source_pins: list[dict[str, Any]] | None = None,
    provenance: dict[str, Any] | None = None,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    value = {
        "schema": "rahp-assessor-result/v1",
        "assessor": assessor,
        "assessment_id": assessment_id,
        "outcome": outcome,
        "reason_code": reason_code,
        "evidence_used": list(dict.fromkeys(evidence_used)),
        "residual_risk": residual_risk,
        "action_required": action_required,
        **({"source_pins": source_pins} if source_pins else {}),
        **({"provenance": provenance} if provenance else {}),
        **({"details": details} if details else {}),
    }
    problems = validate_result(value)
    if problems:
        raise ValueError("; ".join(problems))
    return value


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("result", type=pathlib.Path)
    args = ap.parse_args()
    value = json.loads(args.result.read_text(encoding="utf-8"))
    problems = validate_result(value)
    if problems:
        print("INVALID")
        for problem in problems:
            print(f"- {problem}")
        return 1
    print("VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
