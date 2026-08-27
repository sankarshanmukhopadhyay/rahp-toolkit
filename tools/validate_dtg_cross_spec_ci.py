#!/usr/bin/env python3
"""Run DTG cross-spec validation for selected or all maintained compositions."""
from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys
import yaml

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "profiles" / "dtg" / "cross-spec-tests.yaml"


def run(*args: str) -> None:
    subprocess.run([sys.executable, *args], cwd=ROOT, check=True)


def load() -> dict:
    return yaml.safe_load(REGISTRY.read_text(encoding="utf-8")) or {}


def maintained(data: dict) -> dict[str, dict]:
    return {
        str(item["id"]): item
        for item in data.get("compositions", [])
        if item.get("runnable") and item.get("status") == "maintained"
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--all", action="store_true")
    group.add_argument("--compositions", help="Comma-separated DTG composition IDs")
    args = ap.parse_args()

    data = load()
    items = maintained(data)
    run("tools/validate_cross_spec_registry.py", "--registry", str(REGISTRY.relative_to(ROOT)))

    selected = sorted(items) if args.all else [x for x in (args.compositions or "").split(",") if x]
    if not selected:
        raise SystemExit("No DTG compositions selected")
    unknown = sorted(set(selected) - set(items))
    if unknown:
        raise SystemExit("Unknown/non-maintained DTG compositions: " + ", ".join(unknown))

    for cid in selected:
        assessment = str(items[cid]["assessment"])
        print(f"== DTG cross-spec: {cid} ==")
        run("tools/validate_scenario_corpora.py", "--registry", "profiles/dtg/cross-spec-tests.yaml", "--composition", cid)
        run("tools/validate_pressure_tests.py", "--file", assessment)

    print(f"PASS DTG cross-spec CI validation: {len(selected)} composition(s): {', '.join(selected)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
