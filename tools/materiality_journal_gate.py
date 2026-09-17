#!/usr/bin/env python3
"""Enrich portfolio assessment events with durable materiality journal evidence.

For proposition-scoped DTG portfolio events, this gate compares routed finding identities
with the current durable owner before publication. Repeated finding sets are journaled as
preserved observations. A closed owner that receives a previously unseen material finding
is fail-closed to `uncertain` and receives an explicit retest reason, causing the existing
publisher to reopen it.

The gate is deliberately conservative: it does not claim semantic preservation for a new
finding merely because it maps to the same proposition. Journal entries also retain a
machine-readable finding identity so that, after reassessment and re-closure, an already
journaled finding is not incorrectly treated as new again.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import urllib.request
from pathlib import Path
from typing import Any

KEY_RE = re.compile(r"<!--\s*rahp-assessment-key:([^>]+?)\s*-->")
TABLE_RE = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*`([^`]+)`\s*\|\s*(.*?)\s*\|\s*$", re.M)
JOURNAL_FINDING_RE = re.compile(r"\bfinding=([^\s;]+)\s+@")


def request_json(url: str, token: str) -> Any:
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "User-Agent": "rahp-materiality-journal-gate/1.0",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode())


def finding_rows(body: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for finding_id, repository, title in TABLE_RE.findall(body or ""):
        if finding_id.lower() == "finding":
            continue
        rows.append({
            "finding_id": finding_id.strip(),
            "repository": repository.strip(),
            "title": title.replace("\\|", "|").strip(),
        })
    return rows


def journaled_finding_ids(body: str) -> set[str]:
    """Recover finding identities retained in prior materiality journal summaries."""
    return {match.group(1).strip() for match in JOURNAL_FINDING_RE.finditer(body or "")}


def issue_key(body: str) -> str | None:
    match = KEY_RE.search(body or "")
    return match.group(1).strip() if match else None


def load_issue_index(repository: str, token: str) -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    page = 1
    while page <= 5:
        issues = request_json(
            f"https://api.github.com/repos/{repository}/issues?state=all&per_page=100&page={page}",
            token,
        )
        if not issues:
            break
        for issue in sorted((i for i in issues if "pull_request" not in i), key=lambda i: int(i.get("number") or 0)):
            key = issue_key(issue.get("body") or "")
            if key and key not in index:
                index[key] = issue
        if len(issues) < 100:
            break
        page += 1
    return index


def journal_summary(rows: list[dict[str, str]], impact: str) -> str:
    compact = []
    for row in rows:
        title = " ".join(row["title"].split())
        if len(title) > 120:
            title = title[:117] + "..."
        compact.append(f"finding={row['finding_id']} @ {row['repository']}: {title}")
    findings = "; ".join(compact) if compact else "no routed finding rows"
    return f"materiality-journal impact={impact}; findings={findings}"


def enrich_event(event: dict[str, Any], owner: dict[str, Any] | None) -> dict[str, Any]:
    body = event.get("body") or ""
    rows = finding_rows(body)
    if not rows:
        return event

    owner_body = (owner or {}).get("body") or ""
    known_rows = finding_rows(owner_body)
    known_ids = {row["finding_id"] for row in known_rows} | journaled_finding_ids(owner_body)
    new_rows = [row for row in rows if row["finding_id"] not in known_ids]

    if owner is None:
        impact = "new-proposition"
    elif not new_rows:
        impact = "preserved"
    else:
        # Same proposition identity does not prove that prior evidence covers new material.
        impact = "uncertain"

    event["evidence_impact"] = impact
    event["journal_findings"] = rows
    event["theme"] = journal_summary(rows, impact)

    if owner and owner.get("state") == "closed" and new_rows:
        detail = journal_summary(new_rows, "uncertain")
        event["retest_reason"] = (
            "New material finding(s) mapped to this closed durable proposition without "
            f"evidence-backed preservation: {detail}"
        )
        event["reopen_closed_owner"] = True
    return event


def self_test() -> None:
    old = """<!-- rahp-assessment-key:dtg:portfolio:combined:x -->
| Finding | Repository | Change |
|---|---|---|
| `a` | `example/repo` | old change |
"""
    owner = {"state": "closed", "number": 1, "body": old}
    same = {
        "assessment_key": "dtg:portfolio:combined:x",
        "body": old,
    }
    enriched = enrich_event(dict(same), owner)
    assert enriched["evidence_impact"] == "preserved"
    assert "retest_reason" not in enriched

    changed = {
        "assessment_key": "dtg:portfolio:combined:x",
        "body": """| Finding | Repository | Change |
|---|---|---|
| `a` | `example/repo` | old change |
| `b` | `example/repo` | materially new change |
""",
    }
    enriched = enrich_event(dict(changed), owner)
    assert enriched["evidence_impact"] == "uncertain"
    assert enriched["reopen_closed_owner"] is True
    assert "finding=b @ example/repo" in enriched["retest_reason"]

    # After the publisher records the journal summary and the issue is reassessed/closed,
    # the same material finding must not be treated as new again.
    journaled_owner = {
        "state": "closed",
        "number": 1,
        "body": old + "\n- Theme: `materiality-journal impact=uncertain; findings=finding=b @ example/repo: materially new change`\n",
    }
    enriched_again = enrich_event(dict(changed), journaled_owner)
    assert enriched_again["evidence_impact"] == "preserved"
    assert "retest_reason" not in enriched_again

    fresh = enrich_event(dict(changed), None)
    assert fresh["evidence_impact"] == "new-proposition"
    assert "retest_reason" not in fresh
    print("PASS materiality journal gate self-test")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--events", type=Path)
    ap.add_argument("--repository", default="sankarshanmukhopadhyay/rahp-toolkit")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        self_test()
        return 0
    if args.events is None:
        raise SystemExit("--events is required unless --self-test is used")

    events = json.loads(args.events.read_text()) if args.events.exists() else []
    if not events:
        return 0
    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    if not token:
        raise SystemExit("GITHUB_TOKEN or GH_TOKEN is required")

    index = load_issue_index(args.repository, token)
    enriched = []
    for event in events:
        key = event.get("related_assessment_key") or event.get("assessment_key")
        enriched.append(enrich_event(event, index.get(key)))
    args.events.write_text(json.dumps(enriched, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
