#!/usr/bin/env python3
"""Evaluate v2.7 release readiness from pinned GitHub Actions evidence.

This is an evidence verifier, not a publisher or a substitute for human approval.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ("full_regression", "typescript_conformance", "stable_compatibility",
            "docs_rendering", "publication_metadata", "security_review", "owner_approval")
SHA = re.compile(r"^[0-9a-f]{40}$")


def assess(record: dict) -> list[str]:
    errors: list[str] = []
    if record.get("contract") != "rahp-release-evidence/v1":
        errors.append("unsupported release evidence contract")
    if record.get("candidate_version") != "v2.7.0":
        errors.append("candidate version mismatch")
    sha = record.get("candidate_sha")
    if not isinstance(sha, str) or not SHA.fullmatch(sha):
        errors.append("candidate_sha must be a full 40-character commit SHA")
    gates = record.get("gates")
    if not isinstance(gates, dict) or set(gates) != set(REQUIRED):
        return errors + ["release gate inventory must be exact"]
    for gate in REQUIRED:
        item = gates[gate]
        if not isinstance(item, dict):
            errors.append(f"{gate}: evidence must be a mapping")
            continue
        if item.get("result") != "PASS":
            errors.append(f"{gate}: not PASS ({item.get('result')})")
        if item.get("candidate_sha") != sha:
            errors.append(f"{gate}: evidence SHA differs from candidate SHA")
        source = item.get("source")
        if not isinstance(source, str) or not source.startswith("https://github.com/sankarshanmukhopadhyay/rahp-toolkit/"):
            errors.append(f"{gate}: missing repository evidence URL")
        if gate == "owner_approval" and item.get("decision") != "GO":
            errors.append("owner_approval: explicit GO decision required")
    if record.get("publication_authorized") is not True:
        errors.append("publication is not authorized")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("evidence", type=Path, help="JSON evidence record, external to repository until completed")
    args = parser.parse_args()
    try:
        record = json.loads(args.evidence.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read evidence: {exc}")
        return 1
    errors = assess(record)
    if errors:
        for error in errors:
            print("NO-GO:", error)
        return 1
    print("GO: evidence record passes structural checks; verify linked run provenance independently before publication")
    return 0


if __name__ == "__main__":
    sys.exit(main())
