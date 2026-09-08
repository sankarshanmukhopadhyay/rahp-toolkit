#!/usr/bin/env python3
"""Validate target-neutral RAHP executable-evidence producer results.

This module validates producer/execution/provenance/freshness/claim-boundary
semantics only. It deliberately does not interpret domain-specific observations
or translate local execution success into terminal assurance outcomes.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schemas" / "rahp-evidence-producer-result-v1.schema.json"
FORBIDDEN_TERMINAL_KEYS = {"assurance_outcome", "portfolio_outcome", "terminal_assurance", "terminal_state"}


def _pin_key(pin: dict[str, Any]) -> tuple[str, str, str]:
    return (
        str(pin.get("repository") or ""),
        str(pin.get("revision") or "").lower(),
        str(pin.get("role") or ""),
    )


def validate_result(
    doc: dict[str, Any],
    *,
    expected_producer: str | None = None,
    expected_source_pins: list[dict[str, Any]] | None = None,
) -> list[str]:
    errors: list[str] = []
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for error in sorted(validator.iter_errors(doc), key=lambda e: list(e.absolute_path)):
        path = ".".join(str(part) for part in error.absolute_path) or "$"
        errors.append(f"schema {path}: {error.message}")

    forbidden = sorted(FORBIDDEN_TERMINAL_KEYS.intersection(doc.keys()))
    if forbidden:
        errors.append(
            "producer result must not encode terminal assurance fields: " + ", ".join(forbidden)
        )

    producer = doc.get("producer") if isinstance(doc.get("producer"), dict) else {}
    producer_id = str(producer.get("id") or "")
    if expected_producer and producer_id != expected_producer:
        errors.append(f"producer identity mismatch: expected {expected_producer}, got {producer_id or '<missing>'}")

    evidence = doc.get("evidence") if isinstance(doc.get("evidence"), dict) else {}
    for artifact in evidence.get("artifacts", []) if isinstance(evidence.get("artifacts"), list) else []:
        if not isinstance(artifact, dict):
            continue
        provenance = artifact.get("provenance") if isinstance(artifact.get("provenance"), dict) else {}
        if producer_id and provenance.get("producer_id") != producer_id:
            errors.append(f"artifact producer provenance mismatch for {artifact.get('name', '<unnamed>')}")

    if evidence.get("status") == "observed" and not evidence.get("artifacts"):
        errors.append("observed evidence requires at least one integrity-bearing artifact")

    if expected_source_pins is not None:
        source = doc.get("source") if isinstance(doc.get("source"), dict) else {}
        actual = {_pin_key(pin) for pin in source.get("pins", []) if isinstance(pin, dict)}
        expected = {_pin_key(pin) for pin in expected_source_pins if isinstance(pin, dict)}
        if actual != expected:
            errors.append("source pin mismatch: producer result is stale or attributable to a different target revision")

    freshness = doc.get("freshness") if isinstance(doc.get("freshness"), dict) else {}
    source = doc.get("source") if isinstance(doc.get("source"), dict) else {}
    source_keys = {_pin_key(pin) for pin in source.get("pins", []) if isinstance(pin, dict)}
    freshness_keys = {_pin_key(pin) for pin in freshness.get("valid_against", []) if isinstance(pin, dict)}
    if source_keys and freshness_keys and source_keys != freshness_keys:
        errors.append("freshness.valid_against must identify the same source pins as source.pins")

    execution = doc.get("execution") if isinstance(doc.get("execution"), dict) else {}
    if execution.get("status") == "succeeded" and evidence.get("status") in {"not-tested", "evidence-incomplete"}:
        # Valid by design: process success may still produce no admissible observation.
        pass

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", help="JSON producer result to validate")
    parser.add_argument("--expected-producer")
    args = parser.parse_args()
    if not args.path:
        parser.error("path is required")
    doc = json.loads(Path(args.path).read_text(encoding="utf-8"))
    errors = validate_result(doc, expected_producer=args.expected_producer)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("portable evidence producer result: valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
