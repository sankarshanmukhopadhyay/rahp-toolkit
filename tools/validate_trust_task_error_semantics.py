#!/usr/bin/env python3
"""Validate assurance-relevant Trust Task error semantics.

Issue: #691

This validator checks whether an implementation preserves a specification-declared
extended error code and retryability value when those semantics are required by a
bounded assurance proposition.

The validator does not treat generated bindings as assurance evidence by itself.
Bindings are only one mechanism for carrying the declared vocabulary into an
implementation. The assurance question is whether the observed protocol outcome
preserves the declared meaning at the consuming boundary.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


FIXTURE = Path("examples/cross-spec/trust-task-error-semantics/evidence.yaml")

MATCH = "SEMANTIC_MATCH"
LOSS = "SEMANTIC_LOSS"
UNKNOWN_SPEC = "UNKNOWN_SPEC"
NOT_APPLICABLE = "NOT_APPLICABLE"


def evaluate(vector: dict[str, Any]) -> dict[str, str]:
    vector_id = str(vector.get("id") or "").strip()
    if not vector_id:
        raise ValueError("vector id is required")

    type_known = vector.get("type_known")
    if not isinstance(type_known, bool):
        raise ValueError(f"{vector_id}: type_known must be boolean")

    declared = vector.get("declared_error_codes")
    if not isinstance(declared, list):
        raise ValueError(f"{vector_id}: declared_error_codes must be a list")

    if not type_known:
        return {
            "semantic_outcome": UNKNOWN_SPEC,
            "reason": "task Type URI is unknown; absence of declared codes cannot be inferred",
        }

    observed_code = vector.get("observed_code")
    observed_retryable = vector.get("observed_retryable")

    if not declared:
        return {
            "semantic_outcome": NOT_APPLICABLE,
            "reason": "known task specification declares no extended error codes",
        }

    by_code: dict[str, dict[str, Any]] = {}
    for item in declared:
        if not isinstance(item, dict):
            raise ValueError(f"{vector_id}: declared error entry must be a mapping")
        code = str(item.get("code") or "").strip()
        retryable = item.get("retryable")
        if not code or not isinstance(retryable, bool):
            raise ValueError(f"{vector_id}: declared error requires code and boolean retryable")
        if code in by_code:
            raise ValueError(f"{vector_id}: duplicate declared error code {code}")
        by_code[code] = item

    if not isinstance(observed_code, str) or not observed_code:
        return {
            "semantic_outcome": LOSS,
            "reason": "declared extended error exists but no concrete observed code was captured",
        }

    if observed_code not in by_code:
        return {
            "semantic_outcome": LOSS,
            "reason": "observed code does not preserve any declared extended error",
        }

    if not isinstance(observed_retryable, bool):
        return {
            "semantic_outcome": LOSS,
            "reason": "declared retryability was not observed",
        }

    expected_retryable = bool(by_code[observed_code]["retryable"])
    if observed_retryable != expected_retryable:
        return {
            "semantic_outcome": LOSS,
            "reason": "observed retryability contradicts the governing declaration",
        }

    return {
        "semantic_outcome": MATCH,
        "reason": "observed extended error code and retryability match the declaration",
    }


def validate(path: Path = FIXTURE) -> list[str]:
    doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    evidence = doc.get("evidence") or {}
    vectors = evidence.get("vectors") or []
    if not vectors:
        raise ValueError("error-semantics evidence contains no vectors")

    seen: set[str] = set()
    results: list[str] = []
    witnessed_match = False
    witnessed_loss = False
    witnessed_unknown = False

    for vector in vectors:
        vector_id = str(vector.get("id") or "").strip()
        if not vector_id or vector_id in seen:
            raise ValueError(f"invalid or duplicate vector id: {vector_id!r}")
        seen.add(vector_id)

        actual = evaluate(vector)
        expected = vector.get("expected")
        if actual.get("semantic_outcome") != expected:
            raise AssertionError(
                f"{vector_id}: expected {expected}, got {actual.get('semantic_outcome')}"
            )

        witnessed_match |= actual["semantic_outcome"] == MATCH
        witnessed_loss |= actual["semantic_outcome"] == LOSS
        witnessed_unknown |= actual["semantic_outcome"] == UNKNOWN_SPEC
        results.append(f"{vector_id}: {actual['semantic_outcome']} — {actual['reason']}")

    if not witnessed_match:
        raise AssertionError("no vector demonstrates preserved declared error semantics")
    if not witnessed_loss:
        raise AssertionError("no vector demonstrates semantic loss")
    if not witnessed_unknown:
        raise AssertionError("no vector preserves unknown-spec distinction")

    return results


def main() -> int:
    try:
        results = validate()
    except (OSError, ValueError, AssertionError, yaml.YAMLError) as exc:
        print(f"FAIL Trust Task error semantics: {exc}")
        return 1

    print("PASS Trust Task error-semantic assurance evidence")
    for result in results:
        print(f"- {result}")
    print(
        "Boundary: generated bindings are implementation support; observed protocol semantics are the assurance evidence."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
