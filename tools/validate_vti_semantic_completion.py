#!/usr/bin/env python3
"""Validate the VTI semantic-completion composition evidence for RAHP #185."""
from __future__ import annotations

from pathlib import Path
import sys
from typing import Any

import yaml

FIXTURE = Path("examples/cross-spec/vti-semantic-completion/evidence.yaml")
VALID_SEMANTIC = {"satisfied", "failed", "indeterminate"}
EXPECTED_CONVERGENCE_REQUIREMENTS = {"VTI-CMP-022", "VTI-CMP-023"}
EXPECTED_VTI_HEAD = "3cbd7300a4f46bb2518e2b4b485609e7b5432b58"


def evaluate(vector: dict[str, Any]) -> dict[str, str]:
    protocol = vector.get("protocol") or {}
    semantic = vector.get("semantic_preconditions") or {}

    technical_complete = bool(protocol.get("completed"))
    technical_outcome = "COMPLETE" if technical_complete else "INCOMPLETE"

    if not technical_complete:
        semantic_outcome = "NOT_EVALUATED"
    else:
        values = [str(value).strip().lower() for value in semantic.values()]
        if not values or any(value not in VALID_SEMANTIC for value in values):
            raise ValueError(f"{vector.get('id')}: invalid or missing semantic preconditions")
        if "failed" in values:
            semantic_outcome = "FAILED"
        elif "indeterminate" in values:
            semantic_outcome = "INDETERMINATE"
        else:
            semantic_outcome = "SATISFIED"

    return {
        "technical_outcome": technical_outcome,
        "semantic_outcome": semantic_outcome,
    }


def evaluate_completion_evidence(vector: dict[str, Any]) -> str:
    if vector.get("credential_valid") is not True:
        return "INDETERMINATE"
    binding = str(vector.get("citation_binding") or "unknown").lower()
    outcome = str(vector.get("outcome_evidence") or "missing").lower()
    if binding == "failed" or outcome == "mismatched":
        return "CONTRADICTED"
    if binding == "exact" and outcome == "matching":
        return "ESTABLISHED"
    return "INDETERMINATE"


def validate_convergence_extension(evidence: dict[str, Any]) -> list[str]:
    extension = evidence.get("convergence_extension") or {}
    source = extension.get("vti_source") or {}
    if source.get("commit") != EXPECTED_VTI_HEAD:
        raise AssertionError("WD02 semantic convergence evidence must be source-pinned")
    requirements = set(extension.get("requirements") or [])
    if requirements != EXPECTED_CONVERGENCE_REQUIREMENTS:
        raise AssertionError(f"WD02 semantic requirements mismatch: {sorted(requirements)}")
    vectors = extension.get("completion_evidence_vectors") or []
    if not vectors:
        raise AssertionError("WD02 completion-evidence vectors are missing")
    seen: set[str] = set()
    observed: dict[str, str] = {}
    for vector in vectors:
        vid = str(vector.get("id") or "").strip()
        if not vid or vid in seen:
            raise AssertionError(f"invalid or duplicate WD02 vector id: {vid!r}")
        seen.add(vid)
        actual = evaluate_completion_evidence(vector)
        expected = str(vector.get("expected") or "")
        if actual != expected:
            raise AssertionError(f"{vid}: expected {expected}, got {actual}")
        observed[vid] = actual
    if observed.get("valid-credential-missing-outcome-evidence") != "INDETERMINATE":
        raise AssertionError("valid credential without outcome evidence must not establish completion")
    if observed.get("valid-credential-mismatched-outcome-evidence") != "CONTRADICTED":
        raise AssertionError("mismatched outcome evidence must contradict completion evidence")
    if observed.get("valid-credential-matching-outcome-evidence") != "ESTABLISHED":
        raise AssertionError("matching outcome evidence positive control is missing")
    return [f"{vid}: {state}" for vid, state in observed.items()]


def validate(path: Path = FIXTURE) -> list[str]:
    doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    evidence = doc.get("evidence") or {}
    vectors = evidence.get("vectors") or []
    if not vectors:
        raise ValueError("semantic-completion evidence contains no vectors")

    ids: set[str] = set()
    results: list[str] = []
    witnessed_divergence = False
    witnessed_indeterminate = False
    witnessed_counter_case = False

    for vector in vectors:
        vid = str(vector.get("id") or "").strip()
        if not vid or vid in ids:
            raise ValueError(f"invalid or duplicate vector id: {vid!r}")
        ids.add(vid)
        expected = vector.get("expected") or {}
        actual = evaluate(vector)
        if actual != expected:
            raise AssertionError(f"{vid}: expected {expected}, got {actual}")

        if actual["technical_outcome"] == "COMPLETE" and actual["semantic_outcome"] == "FAILED":
            witnessed_divergence = True
        if actual["technical_outcome"] == "COMPLETE" and actual["semantic_outcome"] == "INDETERMINATE":
            witnessed_indeterminate = True
        if actual == {"technical_outcome": "COMPLETE", "semantic_outcome": "SATISFIED"}:
            witnessed_counter_case = True
        results.append(f"{vid}: {actual['technical_outcome']} / {actual['semantic_outcome']}")

    if not witnessed_divergence:
        raise AssertionError("no vector demonstrates technical COMPLETE with semantic FAILED")
    if not witnessed_indeterminate:
        raise AssertionError("no vector preserves technical COMPLETE with semantic INDETERMINATE")
    if not witnessed_counter_case:
        raise AssertionError("no legitimate COMPLETE / SATISFIED counter-case is preserved")
    results.extend(validate_convergence_extension(evidence))
    return results


def main() -> int:
    try:
        results = validate()
    except (OSError, ValueError, AssertionError, yaml.YAMLError) as exc:
        print(f"FAIL VTI semantic completion: {exc}", file=sys.stderr)
        return 1
    print("PASS VTI semantic completion evidence")
    for result in results:
        print(f"- {result}")
    print("Boundary: credential validity and citation binding do not establish Trust Task completion without matching outcome evidence.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
