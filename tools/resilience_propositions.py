#!/usr/bin/env python3
"""Normalize DRARM results into source-preserving RAHP assurance propositions."""
from __future__ import annotations

import argparse
import json
import pathlib
from typing import Any

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_MAPPING = ROOT / "method" / "mappings" / "resilience-to-assurance.yaml"
VALID_STATUSES = {"finding", "review-required"}


def load_mapping(path: pathlib.Path = DEFAULT_MAPPING) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(value, dict):
        raise ValueError("resilience assurance mapping root must be an object")
    mappings = value.get("mappings") or {}
    unmapped = value.get("unmapped") or {}
    if not isinstance(mappings, dict) or not isinstance(unmapped, dict):
        raise ValueError("resilience assurance mapping sections must be objects")
    overlap = set(mappings) & set(unmapped)
    if overlap:
        raise ValueError("DRARM rules cannot be both mapped and unmapped: " + ", ".join(sorted(overlap)))
    return value


def _target(result: dict[str, Any]) -> dict[str, Any]:
    target = result.get("target")
    if not isinstance(target, dict):
        raise ValueError("DRARM result requires a target object")
    return {
        "repository": target.get("repository"),
        "revision": target.get("revision"),
        "path": target.get("path"),
        "type": target.get("type"),
    }


def proposition_for_finding(
    finding: dict[str, Any],
    target: dict[str, Any],
    mapping: dict[str, Any],
) -> dict[str, Any]:
    risk_id = finding.get("risk_id")
    status = finding.get("status")
    if not isinstance(risk_id, str) or not risk_id.startswith("RLA-"):
        raise ValueError("DRARM finding requires an RLA-* risk_id")
    if status not in VALID_STATUSES:
        raise ValueError(f"unsupported DRARM finding status: {status}")

    mappings = mapping.get("mappings") or {}
    unmapped = mapping.get("unmapped") or {}
    mapped = mappings.get(risk_id)
    if mapped is not None and not isinstance(mapped, dict):
        raise ValueError(f"mapping for {risk_id} must be an object")

    if mapped is None:
        mapped_patterns: dict[str, Any] | list[Any] = []
        mapping_state = "explicitly-unmapped" if risk_id in unmapped else "unmapped"
    else:
        mapped_patterns = {k: v for k, v in mapped.items() if k in {"risk", "control", "guardrail", "assurance", "evidence"}}
        mapping_state = "mapped"

    evidence_required = finding.get("evidence_required") or []
    if not isinstance(evidence_required, list) or not all(isinstance(item, str) for item in evidence_required):
        raise ValueError(f"evidence_required for {risk_id} must be a list of strings")

    return {
        "schema": "rahp-resilience-proposition/v1",
        "type": "resilience",
        "source": {
            "model": "DRARM",
            "rule": risk_id,
            "finding_id": finding.get("id"),
            "status": status,
            "confidence": finding.get("confidence"),
        },
        "target": target,
        "mapped_patterns": mapped_patterns,
        "mapping_state": mapping_state,
        "state": "evidence-required",
        "required_evidence": evidence_required,
        "observed_evidence": finding.get("evidence") or [],
        "required_controls": finding.get("required_controls") or [],
        "title": finding.get("title"),
    }


def normalize_drarm_result(
    result: dict[str, Any],
    mapping: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    if not isinstance(result, dict):
        raise ValueError("DRARM result must be an object")
    model = result.get("model")
    if model not in {"distributed-resilience-amplification", "DRARM"}:
        raise ValueError(f"unsupported resilience model: {model}")
    target = _target(result)
    mapping = mapping or load_mapping()
    findings = result.get("findings") or []
    if not isinstance(findings, list):
        raise ValueError("DRARM findings must be an array")
    return [proposition_for_finding(item, target, mapping) for item in findings]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("result", type=pathlib.Path)
    ap.add_argument("--mapping", type=pathlib.Path, default=DEFAULT_MAPPING)
    ap.add_argument("--output", type=pathlib.Path)
    args = ap.parse_args()
    result = json.loads(args.result.read_text(encoding="utf-8"))
    propositions = normalize_drarm_result(result, load_mapping(args.mapping))
    rendered = json.dumps({"propositions": propositions}, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
