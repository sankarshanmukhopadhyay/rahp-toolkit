#!/usr/bin/env python3
"""Validate the independent-review working surface and false-assurance challenge contract."""
from __future__ import annotations
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "review/README.md",
    "docs/review/external-review-charter.md",
    "docs/review/architecture-and-trust-boundaries.md",
    "docs/review/threat-model.md",
    "docs/review/known-limitations.md",
    "docs/review/reproduction.md",
    "docs/review/security-pre-review.md",
    "docs/review/semantic-coverage.md",
    "docs/review/software-quality-sweep.md",
    "method/review/claim-evidence-ledger.yaml",
    "method/review/false-assurance-challenges.yaml",
]
POSITIVE = {"PASS", "GREEN", "pass", "green", "verified", "permit"}

def load_yaml(path: str):
    value = yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: top-level value must be a mapping")
    return value

def main() -> int:
    errors = []
    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            errors.append(f"missing review surface: {rel}")

    if errors:
        for e in errors: print("ERROR", e)
        return 1

    versioning = load_yaml("method/versioning.yaml")
    ledger = load_yaml("method/review/claim-evidence-ledger.yaml")
    challenges = load_yaml("method/review/false-assurance-challenges.yaml")

    target = ledger.get("review_target") or {}
    contracts = versioning.get("contracts") or {}
    expected = {
        "toolkit_release": versioning.get("stable_release"),
        "engine_contract": contracts.get("engine"),
        "engine_revision": str(contracts.get("engine_revision")),
        "normalized_result_schema": contracts.get("result_schema"),
    }
    actual = {
        "toolkit_release": target.get("toolkit_release"),
        "engine_contract": target.get("engine_contract"),
        "engine_revision": str(target.get("engine_revision")),
        "normalized_result_schema": target.get("normalized_result_schema"),
    }
    if actual != expected:
        errors.append(f"claim ledger review_target {actual} != stable versioning {expected}")

    claims = ledger.get("claims")
    if not isinstance(claims, list) or not claims:
        errors.append("claim ledger must contain claims")
    else:
        seen = set()
        required = {"id","claim","scope","normative_evidence","executable_evidence","falsification","expected_if_falsified","limitations"}
        for claim in claims:
            missing = sorted(k for k in required if not claim.get(k))
            cid = str(claim.get("id") or "<missing>")
            if cid in seen: errors.append(f"duplicate claim id: {cid}")
            seen.add(cid)
            if missing: errors.append(f"{cid}: missing {missing}")
            for field in ("normative_evidence","executable_evidence"):
                for rel in claim.get(field) or []:
                    if not (ROOT / rel).exists():
                        errors.append(f"{cid}: {field} path does not exist: {rel}")

    cases = challenges.get("challenges")
    if not isinstance(cases, list) or not cases:
        errors.append("false-assurance challenge matrix must contain challenges")
    else:
        seen = set()
        for case in cases:
            cid = str(case.get("id") or "<missing>")
            if cid in seen: errors.append(f"duplicate challenge id: {cid}")
            seen.add(cid)
            prohibited = set(case.get("prohibited") or [])
            if not {"PASS","GREEN"} <= prohibited:
                errors.append(f"{cid}: must prohibit PASS and GREEN")
            expected_state = str(case.get("expected") or "")
            if expected_state in POSITIVE:
                errors.append(f"{cid}: deficient-evidence challenge has positive expected state {expected_state!r}")
            if not case.get("attack"):
                errors.append(f"{cid}: attack required")
            evidence_ref = str(case.get("evidence_ref") or "")
            if not evidence_ref:
                errors.append(f"{cid}: evidence_ref required")
            else:
                rel, _, marker = evidence_ref.partition("#")
                evidence_path = ROOT / rel
                if not evidence_path.is_file():
                    errors.append(f"{cid}: evidence_ref path does not exist: {rel}")
                elif marker and marker not in evidence_path.read_text(encoding="utf-8"):
                    errors.append(f"{cid}: evidence_ref fragment not found: {evidence_ref}")

    stable_release = str(expected["toolkit_release"] or "")
    engine_revision = str(expected["engine_revision"] or "")
    result_schema = str(expected["normalized_result_schema"] or "")

    engine_doc = (ROOT / "docs/engine-contract.md").read_text(encoding="utf-8")
    engine_tokens = (
        stable_release,
        f"revision `{engine_revision}`",
        f"schema version `{result_schema}`",
    )
    for token in engine_tokens:
        if token not in engine_doc:
            errors.append(
                f"docs/engine-contract.md missing current compatibility token: {token}"
            )

    review_readme = (ROOT / "review/README.md").read_text(encoding="utf-8")
    review_phrases = (
        "workflow success",
        "not an assurance conclusion",
        stable_release,
        f"revision `{engine_revision}`",
    )
    for phrase in review_phrases:
        if phrase not in review_readme:
            errors.append(
                f"review/README.md missing required review boundary phrase: {phrase}"
            )

    if errors:
        for e in errors: print("ERROR", e)
        print(f"Review-readiness validation failed: {len(errors)} error(s)")
        return 1
    print(f"Review-readiness validation clean: {len(claims)} material claims; {len(cases)} false-assurance challenges; stable boundary synchronized.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
