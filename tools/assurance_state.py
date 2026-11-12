#!/usr/bin/env python3
"""Portable evidence freshness and assurance-delta helpers."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml

RESIDUAL_RANK = {
    "not-assessed": 0,
    "review-required": 1,
    "assurance-gap": 2,
    "finding": 2,
    "controlled": 3,
    "assured": 4,
    "not-applicable": 4,
}


def load(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    value = json.loads(text) if path.suffix.lower() == ".json" else yaml.safe_load(text)
    if not isinstance(value, dict):
        raise ValueError(f"expected object: {path}")
    return value


def conclusion_transition(previous: str, current: str) -> str:
    if previous == current:
        return "unchanged"
    if previous in {"finding", "assurance-gap", "review-required"} and current in {"controlled", "assured", "not-applicable"}:
        return "resolved"
    if previous in {"controlled", "assured", "not-applicable"} and current in {"finding", "assurance-gap", "review-required"}:
        return "regressed"
    p = RESIDUAL_RANK.get(previous)
    c = RESIDUAL_RANK.get(current)
    if p is None or c is None:
        return "indeterminate"
    if c > p:
        return "improved"
    if c < p:
        return "degraded"
    return "indeterminate"


def freshness_from_basis(basis: list[dict[str, Any]]) -> tuple[str, bool]:
    # The freshness record schema requires a nonempty basis. Do not let a
    # missing or unrecognized effect become a claim of current evidence.
    allowed = {"none", "potential", "invalidating", "requires-retest", "supersedes", "unknown"}
    if not isinstance(basis, list) or not basis:
        raise ValueError("freshness basis must be a nonempty list")
    if any(not isinstance(item, dict) or item.get("effect") not in allowed for item in basis):
        raise ValueError("freshness basis contains an unsupported or missing effect")
    effects = {item["effect"] for item in basis}
    if "supersedes" in effects:
        return "superseded", False
    if "requires-retest" in effects:
        return "retest-required", True
    if "invalidating" in effects:
        return "stale", True
    if "unknown" in effects:
        return "indeterminate", True
    if "potential" in effects:
        return "potentially-stale", False
    return "current", False


def main() -> int:
    parser = argparse.ArgumentParser(description="RAHP portable assurance freshness and delta helpers")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("freshness")
    p.add_argument("record", type=Path)

    p = sub.add_parser("transition")
    p.add_argument("--previous", required=True)
    p.add_argument("--current", required=True)

    args = parser.parse_args()
    if args.cmd == "freshness":
        doc = load(args.record)
        try:
            status, retest = freshness_from_basis(doc.get("basis"))
        except ValueError as exc:
            parser.error(str(exc))
        print(json.dumps({"status": status, "retest_required": retest}, sort_keys=True))
        return 0

    print(conclusion_transition(args.previous, args.current))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
