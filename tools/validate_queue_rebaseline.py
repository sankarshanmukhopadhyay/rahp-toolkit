"""Validate a point-in-time RAHP issue-queue rebaseline without implying closure."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUSES = {
    "controller-reconciliation", "publication-verification",
    "implementation-evidence", "upstream-normative-dependency",
    "external-privacy-evidence", "bounded-research",
    "independent-human-judgment", "intentional-dormancy",
}


def validate_queue(data: dict) -> list[str]:
    errors: list[str] = []
    if data.get("schema") != "rahp-queue-rebaseline/v1":
        errors.append("unrecognized rebaseline schema")
    if data.get("scope") != "open-issues":
        errors.append("only open issue inventories may use this schema")
    issues = data.get("issues")
    if not isinstance(issues, list):
        return errors + ["issue inventory must be list"]
    if data.get("open_issue_count") != len(issues):
        errors.append("declared count does not match inventory")
    ids: set[int] = set()
    for row in issues:
        if not isinstance(row, dict):
            errors.append("issue entry must be object")
            continue
        number = row.get("number")
        if not isinstance(number, int) or isinstance(number, bool) or number <= 0:
            errors.append(f"invalid issue number {number!r}")
        elif number in ids:
            errors.append(f"duplicate issue number #{number}")
        else:
            ids.add(number)
        if not isinstance(row.get("title"), str) or not row["title"].strip():
            errors.append(f"#{number}: title missing")
        if row.get("classification") not in STATUSES:
            errors.append(f"#{number}: unclassified or invalid disposition")
        if "assurance_outcome" in row or "closure_authorized" in row:
            errors.append(f"#{number}: routing metadata cannot assert substantive PASS or closure")
    return errors


def main() -> int:
    path = ROOT / "data" / "assurance" / "queue-rebaseline-2026-10-18.json"
    errors = validate_queue(json.loads(path.read_text(encoding="utf-8")))
    for e in errors:
        print("ERROR:", e)
    if not errors:
        print("PASS: point-in-time queue is classified; no closure or assurance claims")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
