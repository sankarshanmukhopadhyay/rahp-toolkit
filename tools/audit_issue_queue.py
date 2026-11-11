#!/usr/bin/env python3
"""Read-only issue queue hygiene audit over GitHub REST issue-list JSON.

This tool never calls GitHub, mutates issues, or makes assurance determinations.
It can analyze a manually exported GitHub REST issue list (which may contain PRs).
Results are advisory, and a missing label is not proof of a missing obligation.
"""
import argparse
import json
from pathlib import Path
from typing import Any


def inspect(records: list[dict[str, Any]]) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    issues = [item for item in records if "pull_request" not in item]
    for item in issues:
        number = item.get("number")
        labels = {value.get("name") if isinstance(value, dict) else value
                  for value in item.get("labels", [])}
        labels.discard(None)
        state = item.get("state", "unknown")
        evidence = "evidence-required" in labels
        remediation = "remediation-required" in labels
        external = "state:waiting-external" in labels
        upstream = "dependency:upstream" in labels
        checks = [
            ("CLOSED_WITH_ACTIVE_EXTERNAL_WAIT", state == "closed" and external,
             "Confirm that a surviving obligation owns the externally waiting evidence."),
            ("CLOSED_WITH_REMEDIATION_REQUIRED", state == "closed" and remediation,
             "Confirm that remission or transfer of the remediation obligation is recorded."),
            ("OPEN_WITH_CONFLICTING_CLOSED_REASON", state == "open" and item.get("state_reason") in {"completed", "not_planned", "duplicate"},
             "Check the source state; an open record cannot be considered disposed."),
            ("EXTERNAL_DEPENDENCY_WITHOUT_WAIT_CLASS", state == "open" and upstream and (evidence or remediation) and not external,
             "Check whether work is externally blocked; do not infer waiting from a label alone."),
            ("WAIT_WITHOUT_EVIDENCE_OR_REMEDIATION_LABEL", state == "open" and external and not (evidence or remediation or "assessment-complete" in labels or "upstream-watch" in labels or "reassessment-pending-upstream" in labels),
             "Check whether the external wait is an explicit governance or coordination obligation."),
        ]
        for code, triggered, recommendation in checks:
            if triggered:
                findings.append({"number": number, "code": code, "recommendation": recommendation})
    return {
        "schema": "rahp-issue-queue-audit/v1",
        "authority": "derived-advisory",
        "issue_count": len(issues),
        "pull_requests_excluded": len(records) - len(issues),
        "findings": findings,
        "limitations": [
            "Labels are incomplete proxies for obligations and never establish readiness or assurance.",
            "This audit does not inspect issue bodies, PRs, upstream source state, acceptance, or runtime evidence.",
            "No finding authorizes issue closure, state mutation, or an assurance PASS.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="GitHub REST JSON array, exported manually")
    parser.add_argument("--report", type=Path, help="Optional local JSON report destination")
    args = parser.parse_args()
    records = json.loads(args.input.read_text(encoding="utf-8"))
    if not isinstance(records, list) or any(not isinstance(item, dict) for item in records):
        parser.error("--input must contain a JSON array of GitHub issue objects")
    report = inspect(records)
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.report:
        args.report.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
