#!/usr/bin/env python3
"""Validate executable VTI human-control pressure vectors."""
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "examples" / "cross-spec" / "vti-human-control" / "evidence.yaml"


def evaluate(vector):
    if not vector.get("principal_authorization_required"):
        return "NOT_REQUIRED"

    evidence = vector.get("authorization_evidence")
    authorizer = vector.get("authorizer")
    required = vector.get("required_principal")
    if evidence != "present" or authorizer is None:
        return "INDETERMINATE"
    if authorizer != required:
        return "DENIED"
    if not vector.get("information_sufficient"):
        return "DENIED"
    if vector.get("authorized_action") != vector.get("requested_action"):
        return "DENIED"
    return "AUTHORIZED"


def main():
    try:
        doc = yaml.safe_load(PATH.read_text(encoding="utf-8"))
        vectors = doc["evidence"]["vectors"]
        ids = set()
        outcomes = set()
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

        if not {"AUTHORIZED", "DENIED", "INDETERMINATE", "NOT_REQUIRED"}.issubset(outcomes):
            raise AssertionError("human-control counter-boundaries incomplete")

        delegate_case = next(v for v in vectors if v["id"] == "delegate-cannot-authorize-for-principal")
        if evaluate(delegate_case) != "DENIED":
            raise AssertionError("delegate must not satisfy principal authorization requirement")

        missing_case = next(v for v in vectors if v["id"] == "required-authorization-missing")
        if evaluate(missing_case) != "INDETERMINATE":
            raise AssertionError("missing required authorization must remain indeterminate")
    except (OSError, KeyError, TypeError, yaml.YAMLError, AssertionError) as exc:
        print(f"FAIL VTI human control: {exc}", file=sys.stderr)
        return 1

    print("PASS VTI human control")
    print(f"- vectors: {len(vectors)}")
    print("- exact-action binding and sufficient-information boundaries preserved")
    print("- delegate cannot substitute for required principal authorization")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
