"""Reproduce a bounded consumer-demand decision using accepted upstream VRC reviews.

This is NOT a schema adapter. It demonstrates what a real downstream consumer
would have to supply before upstream findings could become an operational result.
"""
from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path

import yaml

UPSTREAM_FILES = {
    "baseline": "review/examples/vrc-v03/baseline-review.yaml",
    "reassessed": "review/examples/vrc-v03/reassessed-review.yaml",
}
DOWNSTREAM_CONSUMERS = {
    "review_scaffold": "tools/review.py",
    "specialist_result": "tools/assessor_contract.py",
    "provenance_routing": "tools/evidence_provenance_router.py",
}
UPSTREAM_SCHEMA = "rahp-spec-review/v1"


def review(path: Path) -> dict:
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(doc, dict) or doc.get("schema") != UPSTREAM_SCHEMA:
        raise ValueError(f"Not an authoritative upstream review: {path}")
    if not isinstance(doc.get("target"), dict) or len(str(doc["target"].get("revision", ""))) != 40:
        raise ValueError("Missing immutable upstream target revision")
    return doc


def inspect_consumer(path: Path) -> dict:
    """Inspect declared Python interfaces; don't guess at dynamic GitHub workflows."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    functions = sorted(node.name for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)))
    imports = sorted(
        node.module for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    )
    text = path.read_text(encoding="utf-8")
    return {
        "functions": functions,
        "direct_spec_review_schema_reference": UPSTREAM_SCHEMA in text,
        "direct_upstream_review_validator_reference": "validate_spec_review" in text,
        "imported_modules": imports,
    }


def decide(upstream: Path, downstream: Path) -> dict:
    base = review(upstream / UPSTREAM_FILES["baseline"])
    new = review(upstream / UPSTREAM_FILES["reassessed"])
    if base["target"]["repository"] != new["target"]["repository"]:
        raise ValueError("VRC pair targets different repositories")
    if base["target"]["revision"] == new["target"]["revision"]:
        raise ValueError("VRC pair reuses the same source revision")
    old = {f["id"]: f for f in base["findings"]}
    current = {f["id"]: f for f in new["findings"]}
    if set(old) != set(current):
        raise ValueError("VRC finding continuity requires explicit analysis")
    transitions = {fid: {"baseline": old[fid]["status"], "reassessed": current[fid]["status"]}
                   for fid in sorted(old)}
    if transitions != {
        "F-001": {"baseline": "open", "reassessed": "resolved"},
        "F-002": {"baseline": "open", "reassessed": "open"},
    }:
        raise ValueError("Unexpected authoritative VRC reassessment")
    consumers = {}
    for name, relative in DOWNSTREAM_CONSUMERS.items():
        path = downstream / relative
        if not path.is_file():
            raise FileNotFoundError(f"Named downstream consumer unavailable: {relative}")
        consumers[name] = {"source": relative, **inspect_consumer(path)}
    review_functions = consumers["review_scaffold"]["functions"]
    assessor_functions = consumers["specialist_result"]["functions"]
    if "init_rahp" not in review_functions or "init_security" not in review_functions:
        raise ValueError("Downstream review contract changed; re-assessment required")
    if "normalize_external" not in assessor_functions or "validate_result" not in assessor_functions:
        raise ValueError("Specialist result contract changed; re-assessment required")
    if any(v["direct_spec_review_schema_reference"] or v["direct_upstream_review_validator_reference"]
           for v in consumers.values()):
        raise ValueError("Direct upstream consumer candidate found; inspect before deciding no adapter")
    return {
        "scope": "source-inspected named downstream Python consumer entry points and retained VRC transition",
        "upstream_records": UPSTREAM_FILES,
        "source_revisions": {
            "baseline": base["target"]["revision"],
            "reassessed": new["target"]["revision"],
        },
        "transitions": transitions,
        "consumer_interfaces": consumers,
        "decision": "no_adapter_for_inspected_consumers",
        "basis": ("No direct upstream schema/validator reference found in the three named Python "
                  "entry points; each owns a different representation and has no demonstrated "
                  "operational call requiring review conversion."),
        "not_claimed": [
            "exhaustive repository-wide absence of dynamic consumers",
            "upstream review to downstream controller semantic equivalence",
            "assurance PASS or automatic risk acceptance",
        ],
        "reopen_if": ("A named consumer provides a real upstream record and a reproducible "
                      "failing downstream use case with a justified non-authority-elevating mapping."),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--upstream", type=Path, required=True)
    parser.add_argument("--downstream", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = decide(args.upstream.resolve(), args.downstream.resolve())
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
