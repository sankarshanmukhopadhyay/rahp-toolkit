#!/usr/bin/env python3
"""Typed semantic-review handoff and deterministic RAHP reconciliation.

Semantic judgment remains external. The acceptance fingerprint binds the immutable
target and accepted semantic judgment, while downstream DPIP state may advance and
the same lineage can be resumed without re-accepting unchanged judgment.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any

SHA40 = re.compile(r"^[0-9a-f]{40}$", re.I)
VALID_DIMENSION = {"PASS", "FAIL", "INDETERMINATE", "NOT_APPLICABLE"}
VALID_MATERIALITY = {"MATERIAL", "NOT_MATERIAL", "INDETERMINATE"}
VALID_DPIP = {"NOT_REQUIRED", "REQUIRED_PENDING", "COMPLETE"}
SEMANTIC_KEYS = (
    "schema", "lineage", "target", "reviewer", "propositions", "evidence",
    "dimensions", "privacy_materiality", "acceptance",
)


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("semantic review must be a JSON object")
    return value


def canonical_review(record: dict[str, Any]) -> dict[str, Any]:
    """Return only accepted semantic-judgment material.

    DPIP state, terminal residuals and presentation references are intentionally
    excluded because they are downstream/resumable lifecycle data.
    """
    value = {key: copy.deepcopy(record[key]) for key in SEMANTIC_KEYS if key in record}
    acceptance = value.get("acceptance")
    if isinstance(acceptance, dict):
        acceptance.pop("fingerprint", None)
    return value


def fingerprint(record: dict[str, Any]) -> str:
    payload = json.dumps(canonical_review(record), sort_keys=True, separators=(",", ":"))
    return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()


def validate(record: dict[str, Any], expected_revision: str | None = None) -> list[str]:
    errors: list[str] = []
    if record.get("schema") != "rahp-semantic-review/v1":
        errors.append("schema must be rahp-semantic-review/v1")
    lineage = record.get("lineage")
    if not isinstance(lineage, dict) or not str(lineage.get("id") or "").strip():
        errors.append("lineage.id is required")
    target = record.get("target")
    revision = ""
    if not isinstance(target, dict):
        errors.append("target is required")
    else:
        if not str(target.get("repository") or "").strip():
            errors.append("target.repository is required")
        revision = str(target.get("revision") or "")
        if not SHA40.fullmatch(revision):
            errors.append("target.revision must be an immutable 40-hex commit SHA")
        if expected_revision and revision.lower() != expected_revision.lower():
            errors.append("semantic review target revision does not match assessment target")
    reviewer = record.get("reviewer")
    if not isinstance(reviewer, dict):
        errors.append("reviewer is required")
    else:
        for key in ("actor", "role", "reviewed_at"):
            if not str(reviewer.get(key) or "").strip():
                errors.append(f"reviewer.{key} is required")
    acceptance = record.get("acceptance")
    if not isinstance(acceptance, dict) or acceptance.get("accepted") is not True:
        errors.append("acceptance.accepted must be true")
    else:
        supplied = str(acceptance.get("fingerprint") or "")
        if not supplied:
            errors.append("acceptance.fingerprint is required")
        elif supplied != fingerprint(record):
            errors.append("acceptance fingerprint does not bind this semantic review")
    evidence = record.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        errors.append("at least one evidence record is required")
    else:
        for i, item in enumerate(evidence):
            if not isinstance(item, dict):
                errors.append(f"evidence[{i}] must be an object")
                continue
            if item.get("status") not in {"SATISFIED", "ABSENT", "NOT_EVIDENCED"}:
                errors.append(f"evidence[{i}].status must be SATISFIED, ABSENT, or NOT_EVIDENCED")
            if not str(item.get("id") or "").strip():
                errors.append(f"evidence[{i}].id is required")
            if not str(item.get("provenance") or "").strip():
                errors.append(f"evidence[{i}].provenance is required")
    dimensions = record.get("dimensions")
    if not isinstance(dimensions, dict) or not dimensions:
        errors.append("dimensions are required")
    else:
        for key, value in dimensions.items():
            if value not in VALID_DIMENSION:
                errors.append(f"dimensions.{key} has invalid outcome {value}")
    materiality = record.get("privacy_materiality")
    if not isinstance(materiality, dict) or materiality.get("decision") not in VALID_MATERIALITY:
        errors.append("privacy_materiality.decision must be MATERIAL, NOT_MATERIAL, or INDETERMINATE")
    elif not str(materiality.get("rationale") or "").strip():
        errors.append("privacy_materiality.rationale is required")
    dpip = record.get("dpip")
    if not isinstance(dpip, dict) or dpip.get("state") not in VALID_DPIP:
        errors.append("dpip.state must be NOT_REQUIRED, REQUIRED_PENDING, or COMPLETE")
    elif dpip.get("state") == "COMPLETE" and dpip.get("conclusion") not in {"PASS", "FAIL", "INDETERMINATE"}:
        errors.append("completed DPIP requires PASS, FAIL, or INDETERMINATE conclusion")
    elif dpip.get("state") == "NOT_REQUIRED" and isinstance(materiality, dict) and materiality.get("decision") == "MATERIAL":
        errors.append("material privacy review cannot mark DPIP NOT_REQUIRED")
    return errors


def reconcile(record: dict[str, Any]) -> dict[str, Any]:
    errors = validate(record)
    if errors:
        return {
            "schema": "rahp-terminal-assurance/v1",
            "lineage": record.get("lineage"), "target": record.get("target"),
            "semantic_review_state": "REVIEW_REQUIRED",
            "terminal": {"colour": "AMBER", "conclusion": "INDETERMINATE", "reason": "; ".join(errors)},
            "recommended_next_step": "Supply and explicitly accept a valid semantic review bound to this immutable target.",
        }

    dimensions = record["dimensions"]
    materiality = record["privacy_materiality"]["decision"]
    dpip = record["dpip"]
    outcomes = set(dimensions.values())
    colour, conclusion = "GREEN", "PASS"
    reason = "Accepted semantic review and applicable privacy lifecycle are complete with no adverse or indeterminate outcomes."
    next_step = "Retain the terminal record and reassess on material change."

    if "FAIL" in outcomes:
        colour, conclusion = "RED", "FAIL"
        reason = "At least one accepted RAHP dimension has an adverse finding."
        next_step = "Address the adverse finding and create a new comparable assessment after remediation."
    elif "INDETERMINATE" in outcomes or materiality == "INDETERMINATE":
        colour, conclusion = "AMBER", "INDETERMINATE"
        reason = "Accepted judgment preserves unresolved RAHP or privacy-materiality uncertainty."
        next_step = "Produce the missing evidence or judgment required by the accepted review."
    elif materiality == "MATERIAL":
        if dpip["state"] == "REQUIRED_PENDING":
            colour, conclusion = "AMBER", "INDETERMINATE"
            reason = "Privacy is material and the required fresh DPIP examination has not returned."
            next_step = "Complete the fresh DPIP examination and resume this same lineage."
        elif dpip["state"] != "COMPLETE":
            colour, conclusion = "AMBER", "INDETERMINATE"
            reason = "Privacy is material but DPIP lifecycle state is incomplete."
            next_step = "Create or complete the required fresh DPIP examination."
        elif dpip["conclusion"] == "FAIL":
            colour, conclusion = "RED", "FAIL"
            reason = "The required DPIP examination returned an adverse privacy conclusion."
            next_step = "Remediate the privacy finding and reassess in a new comparable lineage."
        elif dpip["conclusion"] == "INDETERMINATE":
            colour, conclusion = "AMBER", "INDETERMINATE"
            reason = "The required DPIP examination completed but remains evidence-bounded and indeterminate."
            next_step = "Produce the DPIP evidence identified as missing, then create a new pinned examination."
    elif materiality == "NOT_MATERIAL" and dpip["state"] != "NOT_REQUIRED":
        colour, conclusion = "AMBER", "INDETERMINATE"
        reason = "Privacy was judged not material but DPIP lifecycle state is inconsistent."
        next_step = "Record DPIP_NOT_REQUIRED with the accepted materiality rationale."

    return {
        "schema": "rahp-terminal-assurance/v1",
        "lineage": record["lineage"], "target": record["target"],
        "semantic_review_state": "ACCEPTED",
        "semantic_review_fingerprint": record["acceptance"]["fingerprint"],
        "reviewer": record["reviewer"], "dimensions": dimensions,
        "privacy_materiality": record["privacy_materiality"], "dpip": dpip,
        "evidence": record["evidence"], "residuals": record.get("residuals", []),
        "references": record.get("references", []),
        "terminal": {"colour": colour, "conclusion": conclusion, "reason": reason},
        "recommended_next_step": next_step,
    }


def human_summary(terminal: dict[str, Any]) -> str:
    target = terminal.get("target") or {}
    result = terminal.get("terminal") or {}
    residuals = "\n".join("- " + str(x) for x in terminal.get("residuals", [])) or "- No residuals recorded."
    references = "\n".join("- " + str(x) for x in terminal.get("references", [])) or "- No references recorded."
    return f"""# RAHP terminal assurance summary

## Bottom line

**{result.get('colour', 'AMBER')} — {result.get('conclusion', 'INDETERMINATE')}.** {result.get('reason', '')}

## What was assessed

`{target.get('repository', 'unknown')}` at immutable revision `{target.get('revision', 'unknown')}`.

## What remains unknown

{residuals}

## References

{references}

## Recommended next step

{terminal.get('recommended_next_step', 'No next step recorded.')}
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("bind"); p.add_argument("record", type=Path); p.add_argument("--output", type=Path)
    p = sub.add_parser("validate"); p.add_argument("record", type=Path); p.add_argument("--expected-revision")
    p = sub.add_parser("reconcile"); p.add_argument("record", type=Path); p.add_argument("--json-output", type=Path); p.add_argument("--summary-output", type=Path)
    args = parser.parse_args()
    record = load(args.record)
    if args.cmd == "bind":
        record.setdefault("acceptance", {})["fingerprint"] = fingerprint(record)
        (args.output or args.record).write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(record["acceptance"]["fingerprint"]); return 0
    if args.cmd == "validate":
        errors = validate(record, args.expected_revision)
        print(json.dumps({"valid": not errors, "errors": errors, "fingerprint": fingerprint(record)}, indent=2))
        return 1 if errors else 0
    terminal = reconcile(record)
    text = json.dumps(terminal, indent=2, sort_keys=True) + "\n"
    if args.json_output: args.json_output.write_text(text, encoding="utf-8")
    else: print(text, end="")
    if args.summary_output: args.summary_output.write_text(human_summary(terminal), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
