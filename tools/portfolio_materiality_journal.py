#!/usr/bin/env python3
"""Reconcile routed DTG portfolio materiality into durable RAHP issue journals.

This is a conservative companion rail to publish_assessment_issues.py. It does not
create assessment owners. It updates an already-published durable owner with the
actual routed finding set and reopens a closed owner when the observed material set
has changed and evidence preservation has therefore not been established.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

KEY_RE = re.compile(r"<!--\s*rahp-assessment-key:([^>]+?)\s*-->")
CLUSTER_RE = re.compile(r"<!--\s*dtg-routing-cluster:([0-9a-f]+)\s*-->", re.I)
FINDING_ROW_RE = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*`([^`]+)`\s*\|\s*(.*?)\s*\|$", re.M)
CANONICAL_REPOSITORY = "sankarshanmukhopadhyay/rahp-toolkit"


def request(method: str, url: str, token: str, payload: Any | None = None) -> Any:
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "User-Agent": "rahp-materiality-journal/1.0",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            raw = response.read().decode()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        body = exc.read().decode(errors="replace")
        raise RuntimeError(f"GitHub API {method} {url} failed: {exc.code} {body}") from exc


def issue_key(body: str) -> str | None:
    match = KEY_RE.search(body or "")
    return match.group(1).strip() if match else None


def cluster_digest(body: str) -> str | None:
    match = CLUSTER_RE.search(body or "")
    return match.group(1).lower() if match else None


def routed_findings(body: str) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for finding_id, repository, title in FINDING_ROW_RE.findall(body or ""):
        findings.append(
            {
                "finding_id": finding_id.strip(),
                "repository": repository.strip(),
                "title": title.replace("\\|", "|").strip(),
            }
        )
    return findings


def observation_marker(key: str, day: str, digest: str) -> str:
    return f"<!-- rahp-materiality-journal:{key}@{day}:{digest} -->"


def evidence_impact(owner_body: str, event_body: str) -> tuple[str, str]:
    """Return conservative evidence impact and comparison basis.

    An identical routed-cluster digest is bounded evidence that the monitor is
    presenting the already-assessed material set. Anything else is uncertainty,
    not preservation. Explicit invalidation can still be carried by the event.
    """
    event_digest = cluster_digest(event_body)
    if not event_digest:
        return "uncertain", "routed event has no materiality digest"
    if f"<!-- dtg-routing-cluster:{event_digest} -->" in owner_body:
        return "preserved", "identical routed materiality digest already recorded by owner"
    if f"<!-- rahp-materiality-digest:{event_digest} -->" in owner_body:
        return "preserved", "identical routed materiality digest already recorded in journal"
    return "uncertain", "materiality digest differs from the evidence set recorded by owner"


def journal_appendix(event: dict[str, Any], owner_state: str, impact: str, basis: str) -> str:
    key = str(event.get("assessment_key") or "unkeyed")
    day = str(event.get("observed_at") or "unknown")
    body = str(event.get("body") or "")
    digest = cluster_digest(body) or "missing"
    findings = routed_findings(body)
    lines = [
        "",
        "---",
        "",
        "## Materiality journal",
        "",
        observation_marker(key, day, digest),
        f"<!-- rahp-materiality-digest:{digest} -->",
        f"- Portfolio snapshot: `{day}`",
        f"- Durable owner state when observed: `{owner_state}`",
        f"- Evidence impact: **{impact}**",
        f"- Comparison basis: {basis}",
    ]
    if event.get("affected_reviews"):
        lines.append(f"- Affected reviews: {', '.join(str(v) for v in event['affected_reviews'])}")
    if findings:
        lines.extend(["", "### Material findings", "", "| Finding | Repository | Change |", "|---|---|---|"])
        for finding in findings:
            title = finding["title"].replace("|", "\\|")
            lines.append(f"| `{finding['finding_id']}` | `{finding['repository']}` | {title} |")
    else:
        lines.extend(["", "No structured routed-finding rows were present in the event; evidence impact remains explicit."])
    if impact == "uncertain":
        lines.extend(
            [
                "",
                "### Reassessment consequence",
                "",
                "The new material observation is not proven to be covered by the prior evidence set. "
                "The durable owner must be reassessed before it can return to a terminal state.",
            ]
        )
    return "\n".join(lines) + "\n"


def index_issues(issues: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for issue in sorted(issues, key=lambda item: int(item.get("number") or 0)):
        key = issue_key(str(issue.get("body") or ""))
        if key and key not in result:
            result[key] = issue
    return result


def existing_issues(repository: str, token: str) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    for page in range(1, 6):
        items = request(
            "GET",
            f"https://api.github.com/repos/{repository}/issues?state=all&per_page=100&page={page}",
            token,
        )
        if not items:
            break
        issues.extend(item for item in items if "pull_request" not in item)
        if len(items) < 100:
            break
    return issues


def reconcile_event(repository: str, token: str, owner: dict[str, Any], event: dict[str, Any]) -> str:
    owner_body = str(owner.get("body") or "")
    event_body = str(event.get("body") or "")
    event_digest = cluster_digest(event_body) or "missing"
    key = str(event.get("assessment_key") or "unkeyed")
    day = str(event.get("observed_at") or "unknown")
    marker = observation_marker(key, day, event_digest)
    if marker in owner_body:
        return "deduped"

    explicit = str(event.get("evidence_impact") or "").strip().lower()
    if explicit in {"invalidated", "scope-expanded", "strengthened", "preserved", "uncertain"}:
        impact, basis = explicit, "explicit evidence-impact decision supplied by routed event"
    else:
        impact, basis = evidence_impact(owner_body, event_body)

    owner_state = str(owner.get("state") or "open")
    new_body = owner_body.rstrip() + "\n" + journal_appendix(event, owner_state, impact, basis)
    payload: dict[str, Any] = {"body": new_body}
    if owner_state == "closed" and impact in {"invalidated", "scope-expanded", "uncertain"}:
        payload["state"] = "open"
    request("PATCH", f"https://api.github.com/repos/{repository}/issues/{owner['number']}", token, payload)
    return "reopened" if payload.get("state") == "open" else "journaled"


def self_test() -> None:
    key = "dtg:portfolio:combined:key-custody-service-authority"
    old = """<!-- rahp-assessment-key:dtg:portfolio:combined:key-custody-service-authority -->
<!-- dtg-routing-cluster:abc123 -->
"""
    same_event = {
        "assessment_key": key,
        "observed_at": "2026-09-16",
        "affected_reviews": ["rahp", "security", "combined"],
        "body": """<!-- dtg-routing-cluster:abc123 -->
## Routed findings
| Finding | Repository | Change |
|---|---|---|
| `f-1` | `example/repo` | same change |
""",
    }
    changed_event = {
        **same_event,
        "observed_at": "2026-09-17",
        "body": """<!-- dtg-routing-cluster:def456 -->
## Routed findings
| Finding | Repository | Change |
|---|---|---|
| `f-2` | `example/repo` | new material change |
""",
    }
    assert issue_key(old) == key
    assert cluster_digest(same_event["body"]) == "abc123"
    assert evidence_impact(old, same_event["body"])[0] == "preserved"
    assert evidence_impact(old, changed_event["body"])[0] == "uncertain"
    assert routed_findings(changed_event["body"])[0]["finding_id"] == "f-2"
    appendix = journal_appendix(changed_event, "closed", "uncertain", "changed digest")
    assert "f-2" in appendix and "Reassessment consequence" in appendix
    assert observation_marker(key, "2026-09-17", "def456") in appendix
    print("PASS portfolio materiality journal self-test")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events", type=Path, nargs="+", help="routed event JSON files")
    parser.add_argument("--repository", default=CANONICAL_REPOSITORY)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    if args.repository != CANONICAL_REPOSITORY:
        raise SystemExit(f"refused non-canonical repository: {args.repository}")
    if not args.events:
        raise SystemExit("--events is required")
    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    if not token:
        raise SystemExit("GITHUB_TOKEN or GH_TOKEN is required")

    events: list[dict[str, Any]] = []
    for path in args.events:
        if path.exists():
            value = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(value, list):
                events.extend(item for item in value if isinstance(item, dict))
    owners = index_issues(existing_issues(args.repository, token))
    counts = {"journaled": 0, "reopened": 0, "deduped": 0, "missing_owner": 0}
    for event in events:
        key = str(event.get("assessment_key") or "")
        owner = owners.get(key)
        if not owner:
            counts["missing_owner"] += 1
            continue
        action = reconcile_event(args.repository, token, owner, event)
        counts[action] += 1
    print(json.dumps(counts, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
