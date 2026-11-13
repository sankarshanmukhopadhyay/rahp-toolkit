#!/usr/bin/env python3
"""Fixture-only external-style adapter. Never imports RAHP reference code.

Demonstrates a runnable subprocess protocol, not comprehensive independent
implementation of every engine revision 1.3 operation.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import yaml
from jsonschema import Draft202012Validator


def validated(data: dict, root: Path) -> bool:
    schema = json.loads((root / "method/schema/rahp-result.schema.json").read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not Draft202012Validator(schema).is_valid(data):
        return False
    if data["status"] == "dispositioned" and data["disposition"]["outcome"] == "pending":
        return False
    if data["status"] == "dispositioned" and any(x["class"] == "ephemeral" for x in data["evidence"]):
        return False
    if any(x["class"] == "referenced" and not all(x.get(k) for k in
           ("uri", "sha256", "collected_at", "sensitivity")) for x in data["evidence"]):
        return False
    if "closure" in data and (
        data["status"] != "dispositioned"
        or data["closure"]["reviewed_revision"] != data["target"]["reviewed_revision"]
    ):
        return False
    counts = {}
    for item in data.get("evaluations") or []:
        state = (item.get("residual") or {}).get("status")
        counts[state] = counts.get(state, 0) + 1
    if any(counts.get(k, 0) != v for k, v in (data.get("assurance_summary") or {}).items()):
        return False
    if not data["findings"] and any(
        (data.get("assurance_summary") or {}).get(x, 0)
        for x in ("assurance-gap", "review-required", "not-assessed")
    ) and data["disposition"]["outcome"] == "no-material-assurance-impact":
        return False
    return True


def execute(operation: str, file: Path, root: Path) -> dict:
    data = json.loads(file.read_text(encoding="utf-8"))
    if operation == "validate-result":
        return {"valid": validated(data, root)}
    if operation == "retention-plan":
        if not validated(data, root):
            raise ValueError("result invalid")
        policy = yaml.safe_load((root / "method/evidence-retention.yaml").read_text(encoding="utf-8"))
        actions = []
        for item in data["evidence"]:
            cls = item["class"]
            spec = policy["classes"][cls]
            repository = spec["repository"]
            actions.append({
                "id": item["id"], "class": cls, "repository": repository,
                "retention_days": spec.get("default_retention_days"),
                "action": "commit" if repository == "allowed" else (
                    "manifest-only" if repository == "manifest-only" else "do-not-commit"),
            })
        return {"policy": policy["id"], "assessment": data["assessment"]["id"], "actions": actions}
    if operation == "correlate-trigger":
        observation = data["observation"]
        key = observation.get("assessment_key")
        for item in data.get("open_assessments") or []:
            if item.get("key") == key and item.get("status") in ("in-progress", "open"):
                return {"action": "coalesce", "assessment_key": key, "assessment_id": item.get("id")}
        return {"action": "create", "assessment_key": key}
    raise ValueError("unsupported operation")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("operation", choices=("validate-result", "retention-plan", "correlate-trigger"))
    p.add_argument("fixture", type=Path)
    p.add_argument("--contract-root", type=Path, required=True)
    a = p.parse_args()
    try:
        result = execute(a.operation, a.fixture, a.contract_root)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"adapter error: {type(exc).__name__}", file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
