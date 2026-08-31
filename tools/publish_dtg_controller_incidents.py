#!/usr/bin/env python3
"""Publish durable controller incidents for unowned DTG broken-pipeline conditions.

Operational contract:
- Consumes the machine-readable incident records emitted by dtg_assurance_reconcile.py.
- Does nothing for RED blockers already owned by a referenced RAHP issue.
- For an unowned blocker, creates one deterministic dtg-instance issue and reuses the
  same issue on subsequent runs by its embedded incident key.
- This owns controller/provenance remediation only; it must not duplicate assessment or
  DPIP work already owned by another issue.
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import urllib.request
from typing import Any

DEFAULT_REPO = "sankarshanmukhopadhyay/rahp-toolkit"


def api(repo: str, path: str, token: str, method: str = "GET", payload: dict[str, Any] | None = None) -> Any:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(
        f"https://api.github.com/repos/{repo}/{path}",
        data=data,
        method=method,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "rahp-dtg-controller-incidents/1.0",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        raw = response.read()
    return json.loads(raw) if raw else None


def marker(key: str) -> str:
    return f"<!-- rahp-controller-incident:{key} -->"


def find_existing(repo: str, key: str, token: str) -> dict[str, Any] | None:
    needle = marker(key)
    for page in range(1, 6):
        batch = api(repo, f"issues?state=all&labels=dtg-instance&per_page=100&page={page}", token) or []
        for issue in batch:
            if "pull_request" in issue:
                continue
            if needle in (issue.get("body") or ""):
                return issue
        if len(batch) < 100:
            break
    return None


def issue_body(record: dict[str, Any]) -> str:
    blockers = "\n".join(f"- `{item}`" for item in record.get("unowned_blockers") or []) or "- unknown"
    owners = ", ".join(f"#{n}" for n in record.get("owner_issues") or []) or "none"
    return (
        f"{marker(str(record['incident_key']))}\n\n"
        "## RAHP DTG controller incident\n\n"
        "The end-to-end assurance reconciler computed **RED / PIPELINE_BROKEN** and found at least "
        "one blocker without a durable RAHP issue owner. This issue owns the controller-level "
        "remediation only; it does not duplicate assessment work already owned elsewhere.\n\n"
        f"- Gatherer run: `{record.get('run')}`\n"
        f"- Existing owning issue(s): {owners}\n"
        f"- Deterministic incident key: `{record.get('incident_key')}`\n\n"
        "### Unowned broken-pipeline evidence\n\n"
        f"{blockers}\n\n"
        "### Closure condition\n\n"
        "Close only after each unowned blocker has either acquired a durable assessment/DPIP owner "
        "or the provenance/handoff defect has been repaired and reconciliation no longer reports it "
        "as an unowned broken-pipeline condition.\n"
    )


def publish(records: list[dict[str, Any]], repo: str, token: str) -> list[dict[str, Any]]:
    outcomes: list[dict[str, Any]] = []
    for record in records:
        if not record.get("incident_required"):
            outcomes.append({
                "incident_key": record.get("incident_key"),
                "action": "owned",
                "owner_issues": record.get("owner_issues") or [],
            })
            continue
        key = str(record["incident_key"])
        existing = find_existing(repo, key, token)
        if existing:
            outcomes.append({"incident_key": key, "action": "reused", "number": existing.get("number")})
            continue
        created = api(
            repo,
            "issues",
            token,
            method="POST",
            payload={
                "title": f"[RAHP controller incident] DTG pipeline broken for {record.get('run')}",
                "body": issue_body(record),
                "labels": ["dtg-instance"],
                "assignees": ["sankarshanmukhopadhyay"],
            },
        )
        outcomes.append({"incident_key": key, "action": "created", "number": created.get("number")})
    return outcomes


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("incident_json", type=pathlib.Path)
    parser.add_argument("--repository", default=DEFAULT_REPO)
    parser.add_argument("--result-json", type=pathlib.Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        sample = {
            "incident_key": "abc123",
            "run": "gha-1-1",
            "owner_issues": [9],
            "unowned_blockers": ["missing-provenance"],
            "incident_required": True,
        }
        body = issue_body(sample)
        assert marker("abc123") in body
        assert "missing-provenance" in body
        print("PASS publish_dtg_controller_incidents self-test")
        return 0

    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    if not token:
        raise SystemExit("GITHUB_TOKEN or GH_TOKEN is required")
    payload = json.loads(args.incident_json.read_text(encoding="utf-8"))
    outcomes = publish(list(payload.get("incidents") or []), args.repository, token)
    if args.result_json:
        args.result_json.parent.mkdir(parents=True, exist_ok=True)
        args.result_json.write_text(json.dumps({"outcomes": outcomes}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    for outcome in outcomes:
        print(json.dumps(outcome, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
