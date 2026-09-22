#!/usr/bin/env python3
"""Validate VTI configuration-materiality evidence."""
from pathlib import Path
import sys
from typing import Any
import yaml

FIXTURE = Path("examples/cross-spec/vti-configuration-materiality/evidence.yaml")
SEMANTIC_CLASSES = {"trust", "privacy", "authority", "security"}


def evaluate(v: dict[str, Any]) -> tuple[str, str, str]:
    changes = set(v.get("semantic_changes") or [])
    unknown = changes - SEMANTIC_CLASSES
    if unknown:
        raise AssertionError(f"unknown semantic class(es): {sorted(unknown)}")

    classification = "MATERIAL" if changes else "NON_MATERIAL"
    expected_declared = classification == "MATERIAL"
    declaration = "MATCH" if bool(v.get("declared_material")) == expected_declared else "MISMATCH"

    version = v.get("decision_config_version")
    history = set(v.get("config_history") or [])
    reconstruction = "RECONSTRUCTABLE" if version and version in history else "NOT_RECONSTRUCTABLE"
    return classification, reconstruction, declaration


def validate() -> list[str]:
    doc = yaml.safe_load(FIXTURE.read_text(encoding="utf-8")) or {}
    vectors = (doc.get("evidence") or {}).get("vectors") or []
    if not vectors:
        raise AssertionError("configuration-materiality: no vectors")

    seen: set[str] = set()
    results: list[str] = []
    outcomes: set[str] = set()
    for vector in vectors:
        vid = str(vector.get("id") or "")
        if not vid or vid in seen:
            raise AssertionError(f"configuration-materiality: invalid or duplicate id {vid!r}")
        seen.add(vid)
        actual = evaluate(vector)
        expected = (
            vector.get("expected_classification"),
            vector.get("expected_reconstruction"),
            vector.get("expected_declaration"),
        )
        if actual != expected:
            raise AssertionError(f"{vid}: expected {expected}, got {actual}")
        outcomes.update(actual)
        results.append(f"{vid}: {' / '.join(actual)}")

    if "MATERIAL" not in outcomes or "NON_MATERIAL" not in outcomes:
        raise AssertionError("fixture must distinguish material and non-material configuration")
    if "NOT_RECONSTRUCTABLE" not in outcomes:
        raise AssertionError("fixture must expose missing historical configuration")
    if "MISMATCH" not in outcomes:
        raise AssertionError("fixture must expose misdeclared material configuration")
    return results


def main() -> int:
    try:
        results = validate()
    except (OSError, yaml.YAMLError, AssertionError, ValueError) as exc:
        print(f"FAIL VTI configuration materiality: {exc}", file=sys.stderr)
        return 1
    print("PASS VTI configuration materiality")
    for result in results:
        print(f"- {result}")
    print("Boundary: semantic configuration changes require review/audit; non-material changes remain distinguishable.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
