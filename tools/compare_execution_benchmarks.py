#!/usr/bin/env python3
"""Compare like-for-like RAHP benchmark artefacts conservatively."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import yaml

DEFAULT_POLICY_PATH = Path("method/execution-benchmarks.yaml")


def load_benchmark(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("benchmark must be an object")
    return value


def load_policy(path: Path = DEFAULT_POLICY_PATH) -> dict[str, Any]:
    document = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(document, dict):
        raise ValueError("benchmark contract must be an object")
    policy = document.get("regression_policy")
    if not isinstance(policy, dict):
        raise ValueError("benchmark contract is missing regression_policy")
    return policy


def _finite_non_negative(value: Any, *, field: str) -> float:
    number = float(value)
    if not math.isfinite(number) or number < 0:
        raise ValueError(f"{field} must be finite and non-negative")
    return number


def compare(
    baseline: dict[str, Any],
    candidate: dict[str, Any],
    *,
    policy: dict[str, Any] | None = None,
) -> dict[str, Any]:
    policy = dict(policy or {})
    max_regression_percent = _finite_non_negative(
        policy.get("max_regression_percent", 20.0),
        field="max_regression_percent",
    )
    min_absolute_seconds = _finite_non_negative(
        policy.get("min_absolute_regression_seconds", 1.0),
        field="min_absolute_regression_seconds",
    )

    if policy.get("require_same_contract", True) and baseline.get("contract") != candidate.get("contract"):
        return {"status": "incomparable", "reason": "contract-mismatch"}

    if policy.get("require_same_profile", True) and baseline.get("profile") != candidate.get("profile"):
        return {"status": "incomparable", "reason": "profile-mismatch"}

    if baseline.get("profile_exit_code") != 0 or candidate.get("profile_exit_code") != 0:
        return {"status": "invalid", "reason": "benchmark-command-failure"}

    if (
        policy.get("require_semantic_reference_digest_match", True)
        and baseline.get("semantic_reference_digests")
        != candidate.get("semantic_reference_digests")
    ):
        return {"status": "fail", "reason": "semantic-reference-digest-mismatch"}

    baseline_seconds = _finite_non_negative(
        baseline.get("wall_seconds"),
        field="baseline.wall_seconds",
    )
    candidate_seconds = _finite_non_negative(
        candidate.get("wall_seconds"),
        field="candidate.wall_seconds",
    )

    delta_seconds = candidate_seconds - baseline_seconds
    if baseline_seconds == 0:
        delta_percent = 0.0 if candidate_seconds == 0 else math.inf
    else:
        delta_percent = delta_seconds / baseline_seconds * 100.0

    meaningful = (
        delta_seconds > min_absolute_seconds
        and delta_percent > max_regression_percent
    )

    return {
        "status": "fail" if meaningful else "pass",
        "reason": "meaningful-performance-regression" if meaningful else "within-policy",
        "baseline_seconds": round(baseline_seconds, 6),
        "candidate_seconds": round(candidate_seconds, 6),
        "delta_seconds": round(delta_seconds, 6),
        "delta_percent": round(delta_percent, 3) if math.isfinite(delta_percent) else None,
        "policy": {
            "mode": policy.get("mode", "relative-baseline"),
            "max_regression_percent": max_regression_percent,
            "min_absolute_regression_seconds": min_absolute_seconds,
            "require_same_contract": bool(policy.get("require_same_contract", True)),
            "require_same_profile": bool(policy.get("require_same_profile", True)),
            "require_semantic_reference_digest_match": bool(
                policy.get("require_semantic_reference_digest_match", True)
            ),
        },
        "authority_boundary": {
            "assurance_evidence": False,
            "may_set_assurance_outcome": False,
            "purpose": "performance-engineering",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("baseline", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--policy", type=Path, default=DEFAULT_POLICY_PATH)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = compare(
        load_benchmark(args.baseline),
        load_benchmark(args.candidate),
        policy=load_policy(args.policy),
    )
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")

    if result["status"] == "fail":
        return 1
    if result["status"] in {"invalid", "incomparable"}:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
