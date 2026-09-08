#!/usr/bin/env python3
"""Portable capability-coverage validation and completeness helpers."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml

MATURITY = {"architectural", "specification", "implementation", "runtime", "deployment"}
JUDGMENTS = {"SATISFIED", "UNSATISFIED", "INDETERMINATE", "EVIDENCE_REQUIRED", "NOT_APPLICABLE"}
PROVIDERS = {"rahp", "dpip", "interop-lab", "external", "human-judgment"}
PATTERNS = {
    "context-isolation", "positive-disclosure", "provenance-preservation",
    "authority-non-composition", "capability-attenuation", "capability-chain-integrity",
    "lifecycle-current-authority-integrity", "confidentiality-boundary",
    "unlinkability-correlation", "rollback-freshness-integrity", "operator-independence",
    "untrusted-agent-input", "human-untrusted-content-handling",
    "cross-context-aggregation-non-inference",
}


def load(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    value = json.loads(text) if path.suffix.lower() == ".json" else yaml.safe_load(text)
    if not isinstance(value, dict):
        raise ValueError("coverage record must be an object")
    return value


def validate(doc: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    coverage = doc.get("coverage")
    if not isinstance(coverage, dict):
        return ["missing coverage object"]
    for field in ("id", "subject", "maturity", "propositions"):
        if not coverage.get(field):
            errors.append(f"missing coverage.{field}")
    maturity = coverage.get("maturity")
    if maturity and maturity not in MATURITY:
        errors.append(f"unknown maturity: {maturity}")
    propositions = coverage.get("propositions") or []
    if not isinstance(propositions, list):
        errors.append("coverage.propositions must be a list")
        return errors
    seen: set[str] = set()
    for index, proposition in enumerate(propositions):
        prefix = f"propositions[{index}]"
        if not isinstance(proposition, dict):
            errors.append(f"{prefix} must be an object")
            continue
        pid = proposition.get("id")
        if not pid:
            errors.append(f"{prefix} missing id")
        elif pid in seen:
            errors.append(f"duplicate proposition id: {pid}")
        else:
            seen.add(pid)
        pattern = proposition.get("pattern")
        if pattern not in PATTERNS:
            errors.append(f"{prefix} unknown pattern: {pattern}")
        provider = proposition.get("provider")
        if provider not in PROVIDERS:
            errors.append(f"{prefix} unknown provider: {provider}")
        judgment = proposition.get("judgment")
        if judgment not in JUDGMENTS:
            errors.append(f"{prefix} unknown judgment: {judgment}")
        evidence = proposition.get("evidence") or []
        required = proposition.get("evidence_required") or []
        if judgment == "SATISFIED" and required and not evidence:
            errors.append(f"{prefix} SATISFIED without required evidence")
        assessed_at = proposition.get("assessed_at_maturity", maturity)
        if assessed_at not in MATURITY:
            errors.append(f"{prefix} unknown assessed_at_maturity: {assessed_at}")
        if judgment == "SATISFIED" and assessed_at != maturity:
            errors.append(f"{prefix} satisfaction at {assessed_at} cannot promote to {maturity}")
    return errors


def completeness(doc: dict[str, Any]) -> dict[str, int]:
    propositions = (doc.get("coverage") or {}).get("propositions") or []
    result = {"defined": len(propositions), "assessed": 0, "satisfied": 0, "unsatisfied": 0,
              "indeterminate": 0, "evidence_required": 0, "not_applicable": 0}
    mapping = {"SATISFIED": "satisfied", "UNSATISFIED": "unsatisfied", "INDETERMINATE": "indeterminate",
               "EVIDENCE_REQUIRED": "evidence_required", "NOT_APPLICABLE": "not_applicable"}
    for proposition in propositions:
        judgment = proposition.get("judgment") if isinstance(proposition, dict) else None
        if judgment in mapping:
            result["assessed"] += 1
            result[mapping[judgment]] += 1
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate and summarize RAHP capability coverage")
    parser.add_argument("record", type=Path)
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    doc = load(args.record)
    errors = validate(doc)
    if errors:
        print(json.dumps({"valid": False, "errors": errors}, indent=2))
        return 1
    output: dict[str, Any] = {"valid": True}
    if args.summary:
        output["completeness"] = completeness(doc)
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
