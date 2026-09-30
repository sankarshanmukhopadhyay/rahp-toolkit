#!/usr/bin/env python3
"""Portable producer-contract-consumer compatibility and version-skew helpers."""
from __future__ import annotations

from typing import Any

SIDES = ("old", "new")


def _semantic_key(value: dict[str, Any]) -> tuple[str, str]:
    role = str(value.get("semantic_role") or "").strip()
    meaning = str(value.get("meaning") or "").strip()
    if not role or not meaning:
        raise ValueError("semantic endpoint requires semantic_role and meaning")
    return role, meaning


def validate_descriptor(descriptor: dict[str, Any]) -> dict[str, Any]:
    if descriptor.get("schema") != "rahp-composition-compatibility/v1":
        raise ValueError("unsupported composition descriptor schema")
    for name in ("producer", "contract", "consumer"):
        part = descriptor.get(name)
        if not isinstance(part, dict):
            raise ValueError(f"{name} must be an object")
        for side in SIDES:
            item = part.get(side)
            if not isinstance(item, dict):
                raise ValueError(f"{name}.{side} must be an object")
            _semantic_key(item)
    mixed = descriptor.get("mixed_version_policy")
    if not isinstance(mixed, dict):
        raise ValueError("mixed_version_policy must be an object")
    for key in ("old-producer/new-consumer", "new-producer/old-consumer"):
        value = mixed.get(key)
        if value not in {"accept-compatible", "explicit-refusal", "unspecified"}:
            raise ValueError(f"invalid mixed-version policy for {key}: {value!r}")
    return descriptor


def derive_matrix(descriptor: dict[str, Any]) -> list[dict[str, Any]]:
    """Derive the four producer/consumer version combinations.

    This is a proposition generator, not a defect detector.  Semantic mismatch or
    unspecified mixed-version behavior produces review-required/model-gap.
    """
    validate_descriptor(descriptor)
    rows: list[dict[str, Any]] = []
    producer = descriptor["producer"]
    contract = descriptor["contract"]
    consumer = descriptor["consumer"]
    policy = descriptor["mixed_version_policy"]

    for p_side in SIDES:
        for c_side in SIDES:
            p_role, p_meaning = _semantic_key(producer[p_side])
            c_role, c_meaning = _semantic_key(consumer[c_side])
            contract_side = p_side if p_side == c_side else c_side
            k_role, k_meaning = _semantic_key(contract[contract_side])
            mixed = p_side != c_side
            policy_key = f"{p_side}-producer/{c_side}-consumer"
            expected = "same-generation"
            if mixed:
                expected = policy[policy_key]

            semantic_match = p_role == k_role == c_role and p_meaning == k_meaning == c_meaning
            if mixed and expected == "unspecified":
                state = "INDETERMINATE"
                reason = "mixed-version behavior is unspecified"
            elif mixed and expected == "explicit-refusal":
                state = "REVIEW_REQUIRED"
                reason = "mixed-version path must prove explicit refusal; component PASS is insufficient"
            elif semantic_match:
                state = "COMPATIBLE_PROPOSITION"
                reason = "producer, contract and consumer declare the same semantic role and meaning"
            else:
                state = "REVIEW_REQUIRED"
                reason = "producer/contract/consumer semantic roles or meanings differ"

            rows.append(
                {
                    "producer_version": p_side,
                    "consumer_version": c_side,
                    "contract_version": contract_side,
                    "expected": expected,
                    "semantic_match": semantic_match,
                    "state": state,
                    "reason": reason,
                    "proposition": (
                        f"{p_side} producer ({p_role}: {p_meaning}) through "
                        f"{contract_side} contract ({k_role}: {k_meaning}) to "
                        f"{c_side} consumer ({c_role}: {c_meaning})"
                    ),
                }
            )
    return rows


def review_propositions(descriptor: dict[str, Any]) -> list[dict[str, Any]]:
    return [row for row in derive_matrix(descriptor) if row["state"] in {"REVIEW_REQUIRED", "INDETERMINATE"}]
