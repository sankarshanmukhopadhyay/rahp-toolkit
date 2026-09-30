#!/usr/bin/env python3
"""Execute a bounded number of real DTG cross-specification RAHP workloads."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = Path("profiles/dtg/cross-spec-tests.yaml")


def load_registry(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError("cross-spec registry must contain a mapping")
    return data


def runnable_compositions(registry: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        item
        for item in registry.get("compositions", [])
        if item.get("runnable") and item.get("assessment")
    ]


def select_compositions(registry: dict[str, Any], limit: int) -> list[dict[str, Any]]:
    items = runnable_compositions(registry)
    if limit < 1:
        raise ValueError("limit must be at least 1")
    if limit > len(items):
        raise ValueError(f"limit {limit} exceeds {len(items)} runnable compositions")
    return items[:limit]


def run(command: list[str]) -> None:
    proc = subprocess.run(command, cwd=ROOT, text=True)
    if proc.returncode != 0:
        raise SystemExit(proc.returncode)


def execute(registry_path: Path, limit: int, output: Path) -> dict[str, Any]:
    registry = load_registry(ROOT / registry_path)
    selected = select_compositions(registry, limit)

    run([
        sys.executable,
        "tools/validate_cross_spec_registry.py",
        "--registry",
        str(registry_path),
    ])

    for item in selected:
        composition_id = str(item["id"])
        run([
            sys.executable,
            "tools/validate_scenario_corpora.py",
            "--registry",
            str(registry_path),
            "--composition",
            composition_id,
        ])

    pressure_command = [sys.executable, "tools/validate_pressure_tests.py"]
    for item in selected:
        pressure_command.extend(["--file", str(item["assessment"])])
    run(pressure_command)

    for item in selected:
        composition_id = str(item["id"])
        safe_id = composition_id.replace("/", "-")
        run([
            sys.executable,
            "tools/cross_spec_review.py",
            composition_id,
            "--registry",
            str(registry_path),
            "--output",
            f"build/benchmark-scale-{safe_id}-review.md",
            "--events",
            f"build/benchmark-scale-{safe_id}-events.json",
        ])

    result = {
        "registry": str(registry_path),
        "runnable_composition_count": len(runnable_compositions(registry)),
        "selected_composition_count": len(selected),
        "selected_compositions": [str(item["id"]) for item in selected],
        "assessment_paths": [str(item["assessment"]) for item in selected],
    }
    target = ROOT / output
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--limit", type=int, required=True)
    parser.add_argument("--output", type=Path, default=Path("build/cross-spec-scale-workload.json"))
    args = parser.parse_args()
    try:
        execute(args.registry, args.limit, args.output)
    except ValueError as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
