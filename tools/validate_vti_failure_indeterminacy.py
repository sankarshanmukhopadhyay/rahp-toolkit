#!/usr/bin/env python3
"""Validate VTI failure/indeterminacy evidence."""
from pathlib import Path
import sys
from typing import Any
import yaml

FIXTURE = Path("examples/cross-spec/vti-failure-indeterminacy/evidence.yaml")


def evaluate(v: dict[str, Any]) -> tuple[str, str]:
    outcome = v.get("evaluation_outcome")
    if outcome not in {"supported", "refuted", "indeterminate"}:
        raise AssertionError(f"invalid evaluation outcome: {outcome!r}")

    action = v.get("policy_action")
    if outcome == "indeterminate":
        if action == "silent":
            decision = "REFUSE"
        elif action == "allow":
            decision = "ALLOW_BY_POLICY"
        elif action == "refuse":
            decision = "REFUSE"
        elif action == "escalate":
            decision = "ESCALATE"
        else:
            raise AssertionError(f"indeterminate evaluation has unsupported policy action: {action!r}")
        return "indeterminate", decision

    if outcome == "supported":
        return "supported", "ALLOW" if action == "allow" else "REFUSE"
    return "refuted", "REFUSE"


def validate() -> list[str]:
    doc = yaml.safe_load(FIXTURE.read_text(encoding="utf-8")) or {}
    evidence = doc.get("evidence") or {}
    vectors = evidence.get("vectors") or []
    if not vectors:
        raise AssertionError("failure-indeterminacy: no vectors")

    seen: set[str] = set()
    results: list[str] = []
    indeterminate_seen = False
    for vector in vectors:
        vid = str(vector.get("id") or "")
        if not vid or vid in seen:
            raise AssertionError(f"failure-indeterminacy: invalid or duplicate id {vid!r}")
        seen.add(vid)
        actual_eval, actual_decision = evaluate(vector)
        if actual_eval != vector.get("expected_evaluation"):
            raise AssertionError(
                f"{vid}: expected evaluation {vector.get('expected_evaluation')}, got {actual_eval}"
            )
        if actual_decision != vector.get("expected_decision"):
            raise AssertionError(
                f"{vid}: expected decision {vector.get('expected_decision')}, got {actual_decision}"
            )
        if vector.get("evaluation_outcome") == "indeterminate":
            indeterminate_seen = True
            if actual_eval != "indeterminate":
                raise AssertionError(f"{vid}: indeterminate was silently converted")
        results.append(f"{vid}: {actual_eval} / {actual_decision}")

    if not indeterminate_seen:
        raise AssertionError("fixture must exercise indeterminate")
    by_id = {v["id"]: v for v in vectors}
    silent = evaluate(by_id["indeterminate-policy-silent"])
    if silent != ("indeterminate", "REFUSE"):
        raise AssertionError("silent policy must refuse while preserving indeterminate")
    explicit_allow = evaluate(by_id["indeterminate-explicit-allow"])
    if explicit_allow != ("indeterminate", "ALLOW_BY_POLICY"):
        raise AssertionError("explicit policy action must not rewrite indeterminate as support")

    return results


def main() -> int:
    try:
        results = validate()
    except (OSError, yaml.YAMLError, AssertionError, ValueError) as exc:
        print(f"FAIL VTI failure/indeterminacy: {exc}", file=sys.stderr)
        return 1
    print("PASS VTI failure/indeterminacy")
    for result in results:
        print(f"- {result}")
    print("Boundary: decision policy may act on indeterminate, but may not rewrite it as support or refutation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
