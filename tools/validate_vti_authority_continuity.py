#!/usr/bin/env python3
"""Validate bounded VTI authority-continuity evidence."""
from pathlib import Path
import sys
from typing import Any
import yaml

FIXTURE = Path("examples/cross-spec/vti-authority-continuity/evidence.yaml")


def evaluate(v: dict[str, Any]) -> str:
    if not v.get("identity_established") or not v.get("authenticated"):
        return "INDETERMINATE"
    if not v.get("credential_verified"):
        return "INDETERMINATE"
    if v.get("authority_source_entitled") is not True:
        return "INDETERMINATE"

    authority = v.get("authority_state")
    if authority == "unknown":
        return "INDETERMINATE"
    if authority != "current":
        return "DENIED"

    authorization = v.get("authorization")
    if authorization == "unknown":
        return "INDETERMINATE"
    if authorization != "granted":
        return "DENIED"
    return "AUTHORIZED"


def validate() -> list[str]:
    doc = yaml.safe_load(FIXTURE.read_text(encoding="utf-8")) or {}
    evidence = doc.get("evidence") or {}
    vectors = evidence.get("vectors") or []
    if not vectors:
        raise AssertionError("authority-continuity: no vectors")

    results: list[str] = []
    seen: set[str] = set()
    outcomes: set[str] = set()
    for vector in vectors:
        vid = str(vector.get("id") or "")
        if not vid or vid in seen:
            raise AssertionError(f"authority-continuity: invalid or duplicate id {vid!r}")
        seen.add(vid)

        required = {
            "identity_established",
            "authenticated",
            "credential_verified",
            "authority_source_entitled",
            "authority_state",
            "authorization",
            "expected",
        }
        missing = required - set(vector)
        if missing:
            raise AssertionError(f"{vid}: missing fields {sorted(missing)}")

        actual = evaluate(vector)
        expected = vector.get("expected")
        if actual != expected:
            raise AssertionError(f"{vid}: expected {expected}, got {actual}")
        outcomes.add(actual)
        results.append(f"{vid}: {actual}")

    if not {"AUTHORIZED", "DENIED", "INDETERMINATE"}.issubset(outcomes):
        raise AssertionError("authority-continuity must preserve positive, negative and indeterminate outcomes")

    by_id = {v["id"]: v for v in vectors}
    if evaluate(by_id["valid-proof-revoked-authority"]) == "AUTHORIZED":
        raise AssertionError("valid proof must not override revoked authority")
    if evaluate(by_id["valid-proof-unentitled-authority-source"]) != "INDETERMINATE":
        raise AssertionError("unentitled authority source must not establish authority")
    if evaluate(by_id["current-authority-no-authorization"]) == "AUTHORIZED":
        raise AssertionError("current authority must remain distinct from action authorization")

    return results


def main() -> int:
    try:
        results = validate()
    except (OSError, yaml.YAMLError, AssertionError, ValueError) as exc:
        print(f"FAIL VTI authority continuity: {exc}", file=sys.stderr)
        return 1

    print("PASS VTI authority continuity")
    for result in results:
        print(f"- {result}")
    print("Boundary: verification != authority; authority != authorization; missing decision-time authority remains indeterminate.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
