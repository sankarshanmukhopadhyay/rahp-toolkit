#!/usr/bin/env python3
"""Validate bounded VTI composition evidence for RAHP #235."""
from pathlib import Path
import sys
from typing import Any
import yaml

FIXTURE = Path("examples/cross-spec/vti-composition-wave/evidence.yaml")


def delegation(v: dict[str, Any]) -> str:
    if v.get("missing_hop"):
        return "INDETERMINATE"
    chain = v.get("lineage") or []
    if len(chain) < 2:
        return "INDETERMINATE"
    action = v.get("action")
    for i, hop in enumerate(chain):
        if not hop.get("current") or hop.get("scope") != action:
            return "DENIED"
        if i < len(chain) - 1 and not hop.get("redelegation"):
            return "DENIED"
    return "AUTHORIZED"


def lifecycle(v: dict[str, Any]) -> str:
    if not v.get("authoritative_state_known"):
        return "INDETERMINATE"
    state = v.get("authoritative_state")
    return "ACTIONABLE" if state in {"active", "restored"} else "NOT_ACTIONABLE"


def human_control(v: dict[str, Any]) -> str:
    if not v.get("protocol_complete"):
        return "INDETERMINATE"
    if not v.get("required_authorization"):
        return "NOT_REQUIRED"
    evidence = v.get("authorization_evidence")
    if evidence != "present":
        return "INDETERMINATE"
    return "AUTHORIZED" if v.get("authorized_scope") == v.get("action_scope") else "DENIED"


def discovery(v: dict[str, Any]) -> str:
    if v.get("resolution") != "success":
        return "NOT_RESOLVED"
    authority = v.get("authority")
    if authority == "valid":
        return "AUTHORIZED"
    if authority == "invalid":
        return "DENIED"
    return "INDETERMINATE"


def validate() -> list[str]:
    doc = yaml.safe_load(FIXTURE.read_text(encoding="utf-8")) or {}
    evidence = doc.get("evidence") or {}
    evaluators = {
        "delegation": delegation,
        "lifecycle": lifecycle,
        "human_control": human_control,
        "discovery": discovery,
    }
    results: list[str] = []
    for family, evaluator in evaluators.items():
        vectors = evidence.get(family) or []
        if not vectors:
            raise AssertionError(f"{family}: no vectors")
        seen: set[str] = set()
        outcomes: set[str] = set()
        for vector in vectors:
            vid = str(vector.get("id") or "")
            if not vid or vid in seen:
                raise AssertionError(f"{family}: invalid or duplicate id {vid!r}")
            seen.add(vid)
            actual = evaluator(vector)
            expected = vector.get("expected")
            if actual != expected:
                raise AssertionError(f"{vid}: expected {expected}, got {actual}")
            outcomes.add(actual)
            results.append(f"{vid}: {actual}")
        if "INDETERMINATE" not in outcomes:
            raise AssertionError(f"{family}: missing INDETERMINATE boundary")

    delegation_outcomes = {delegation(v) for v in evidence["delegation"]}
    if not {"AUTHORIZED", "DENIED", "INDETERMINATE"}.issubset(delegation_outcomes):
        raise AssertionError("delegation must preserve positive, negative and indeterminate cases")
    lifecycle_outcomes = {lifecycle(v) for v in evidence["lifecycle"]}
    if not {"ACTIONABLE", "NOT_ACTIONABLE", "INDETERMINATE"}.issubset(lifecycle_outcomes):
        raise AssertionError("lifecycle must preserve current, stale and unknown cases")
    human_outcomes = {human_control(v) for v in evidence["human_control"]}
    if not {"AUTHORIZED", "DENIED", "INDETERMINATE", "NOT_REQUIRED"}.issubset(human_outcomes):
        raise AssertionError("human-control counter-boundaries incomplete")
    discovery_outcomes = {discovery(v) for v in evidence["discovery"]}
    if not {"AUTHORIZED", "DENIED", "INDETERMINATE", "NOT_RESOLVED"}.issubset(discovery_outcomes):
        raise AssertionError("discovery/authority boundaries incomplete")

    residuals = evidence.get("unresolved_implementation_evidence") or []
    by_issue = {int(r.get("issue")): r for r in residuals}
    for issue in (188, 190):
        r = by_issue.get(issue)
        if not r or r.get("status") != "EVIDENCE_REQUIRED" or r.get("synthetic_substitution_permitted") is not False:
            raise AssertionError(f"#{issue}: unresolved implementation evidence boundary not preserved")
    return results


def main() -> int:
    try:
        results = validate()
    except (OSError, yaml.YAMLError, AssertionError, ValueError) as exc:
        print(f"FAIL VTI composition wave: {exc}", file=sys.stderr)
        return 1
    print("PASS VTI composition wave")
    for result in results:
        print(f"- {result}")
    print("Boundary: #188/#190 remain EVIDENCE_REQUIRED until concrete implementation pairs exist.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
