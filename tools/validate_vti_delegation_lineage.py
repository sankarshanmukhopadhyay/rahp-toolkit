#!/usr/bin/env python3
"""Validate executable VTI delegation-lineage pressure vectors."""
from datetime import datetime, timezone
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "examples" / "cross-spec" / "vti-delegation-lineage" / "evidence.yaml"


def parse_time(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def evaluate(vector):
    if not vector.get("lineage_complete"):
        return "INDETERMINATE"
    lineage = vector.get("lineage") or []
    if not lineage:
        return "INDETERMINATE"
    acting = vector.get("acting_delegate")
    decision_actor = vector.get("decision_actor")
    if not acting or not decision_actor:
        return "INDETERMINATE"
    if acting != decision_actor:
        return "DENIED"

    action = vector.get("action")
    action_time = parse_time(vector["action_time"])
    for idx, hop in enumerate(lineage):
        if hop.get("scope") != action:
            return "DENIED"
        if hop.get("revoked"):
            return "DENIED"
        if not hop.get("delegator_current"):
            return "DENIED"
        if parse_time(hop["expires_at"]) < action_time:
            return "DENIED"
        if idx < len(lineage) - 1 and not hop.get("redelegation"):
            return "DENIED"

    if lineage[-1].get("to") != acting:
        return "INDETERMINATE"
    return "AUTHORIZED"


def main():
    try:
        doc = yaml.safe_load(PATH.read_text(encoding="utf-8"))
        vectors = doc["evidence"]["vectors"]
        outcomes = set()
        ids = set()
        for vector in vectors:
            vid = vector["id"]
            if vid in ids:
                raise AssertionError(f"duplicate vector id: {vid}")
            ids.add(vid)
            actual = evaluate(vector)
            expected = vector["expected"]
            if actual != expected:
                raise AssertionError(f"{vid}: expected {expected}, got {actual}")
            outcomes.add(actual)

        if not {"AUTHORIZED", "DENIED", "INDETERMINATE"}.issubset(outcomes):
            raise AssertionError("delegation vectors must preserve positive, negative and indeterminate outcomes")

        identity_case = next(v for v in vectors if v["id"] == "delegate-identity-substituted-by-principal")
        if evaluate(identity_case) != "DENIED":
            raise AssertionError("delegate identity substitution must not be accepted")
    except (OSError, KeyError, TypeError, ValueError, yaml.YAMLError, AssertionError) as exc:
        print(f"FAIL VTI delegation lineage: {exc}", file=sys.stderr)
        return 1

    print("PASS VTI delegation lineage")
    print(f"- vectors: {len(vectors)}")
    print("- preserves scope, lineage, expiry, revocation, re-delegation and current delegator authority")
    print("- acting delegate identity reaches the decision point")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
