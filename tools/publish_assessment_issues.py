#!/usr/bin/env python3
"""Publish RAHP assessment events as stable, coalesced GitHub work items.

Operational contract:
- Consumes generated repository/architecture assessment events and confines automated
  issue creation to the canonical RAHP repository.
- Treats the assessment/proposition key as durable ownership across both open and closed
  issues. A new observation does not imply a new issue.
- Reuses/coalesces an existing open assessment key where possible instead of creating
  one issue per observation; the resulting issue is a durable work owner, not a finding.
- A closed owner remains terminal unless an event explicitly requests a retest/reopen and
  supplies a reason. Re-observation alone never manufactures a successor issue.
- Controller keys are epoch-scoped by their producer. Bounded child/repository keys may
  remain proposition-scoped where intentional; this publisher coalesces exact keys only.
- May create issues, append trigger metadata, or explicitly reopen a terminal owner through
  the GitHub API. Publication does not execute the assessment and issue creation does not
  imply that a target is unsafe or that DPIP is required.
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
LEGACY_DTG_RE = re.compile(r"<!--\s*rahp-dtg-change:([^@>]+)@[^>]+-->")

# Publication authority invariant for this RAHP distribution. Assessment targets and
# upstream remediation repositories are evidence metadata only; automated issue
# creation is confined to the RAHP review repository.
CANONICAL_RAHP_ISSUE_REPOSITORY = "sankarshanmukhopadhyay/rahp-toolkit"
CANONICAL_RAHP_ASSIGNEES = ["sankarshanmukhopadhyay"]


def enforce_publication_repository(repository: str) -> str:
    """Reject any attempt to publish RAHP work items outside the RAHP repository."""
    repo = (repository or "").strip()
    if repo != CANONICAL_RAHP_ISSUE_REPOSITORY:
        raise ValueError(
            "RAHP issue publication is confined to "
            f"{CANONICAL_RAHP_ISSUE_REPOSITORY}; refused destination {repo!r}. "
            "Target/upstream repositories may be recorded as evidence or remediation "
            "metadata but must never receive automated RAHP issues."
        )
    return repo


def request(method: str, url: str, token: str, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "User-Agent": "rahp-assessment-issue-publisher/0.8.0",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            raw = r.read().decode()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        raise RuntimeError(f"GitHub API {method} {url} failed: {e.code} {body}") from e


def ensure_label(repo: str, label: str, token: str):
    encoded = urllib.parse.quote(label, safe="")
    url = f"https://api.github.com/repos/{repo}/labels/{encoded}"
    try:
        request("GET", url, token)
        return
    except RuntimeError as exc:
        if " 404 " not in str(exc):
            raise
    palette = {"assessment-required": "d73a4a", "cawg-instance": "1d76db", "dtg-instance": "5319e7", "cross-specification": "8250df", "change-triage": "d4c5f9"}
    request("POST", f"https://api.github.com/repos/{repo}/labels", token,
            {"name": label, "color": palette.get(label, "6f42c1"), "description": "RAHP automated assessment workflow"})


def infer_issue_keys(issue: dict[str, Any]) -> set[str]:
    """Return explicit keys plus the v0.7 DTG repository key when inferable."""
    body = issue.get("body") or ""
    keys = {m.group(1).strip() for m in KEY_RE.finditer(body)}
    for match in LEGACY_DTG_RE.finditer(body):
        keys.add(f"dtg:repository:{match.group(1).strip()}")
    return keys


def existing_issues(repo: str, token: str) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    page = 1
    while page <= 10:
        items = request("GET", f"https://api.github.com/repos/{repo}/issues?state=all&per_page=100&page={page}", token)
        if not items:
            break
        issues.extend(i for i in items if "pull_request" not in i)
        if len(items) < 100:
            break
        page += 1
    return issues


def issue_owner_by_key(issues: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Index durable assessment owners, preferring an open owner over a closed owner.

    A closed issue does not stop owning its proposition. This is the core idempotency
    boundary: repeated observations must resolve to the terminal owner rather than create
    a new issue merely because that owner has been closed.
    """
    index: dict[str, dict[str, Any]] = {}
    for issue in sorted(issues, key=lambda value: int(value.get("number") or 0), reverse=True):
        for key in infer_issue_keys(issue):
            current = index.get(key)
            if current is None:
                index[key] = issue
                continue
            if current.get("state") != "open" and issue.get("state") == "open":
                index[key] = issue
    return index


def explicit_retest(event: dict[str, Any]) -> bool:
    """Return true only for an explicit, reasoned terminal-owner invalidation."""
    return event.get("reopen_closed") is True and bool(str(event.get("retest_reason") or "").strip())


def event_marker(event: dict[str, Any]) -> str:
    key = event.get("assessment_key") or "unkeyed"
    stamp = event.get("observed_at") or event.get("new") or "unknown"
    return f"<!-- rahp-trigger:{key}@{stamp} -->"


def trigger_appendix(event: dict[str, Any]) -> str:
    marker = event_marker(event)
    source = event.get("source", "assessment-event")
    lines = [
        "",
        "---",
        "",
        "## Additional assessment trigger",
        "",
        marker,
        f"- Source: `{source}`",
    ]
    if event.get("upstream_repository") and event.get("upstream_issue"):
        lines.append(f"- Upstream issue: `{event['upstream_repository']}#{event['upstream_issue']}`")
    if event.get("repository"):
        lines.append(f"- Repository: `{event['repository']}`")
    if event.get("old") and event.get("new"):
        lines.append(f"- Additional revision window: `{event['old']}` → `{event['new']}`")
    if event.get("theme"):
        lines.append(f"- Theme: `{event['theme']}`")
    if event.get("affected_reviews"):
        lines.append(f"- Affected reviews: {', '.join(event['affected_reviews'])}")
    if event.get("retest_reason"):
        lines.append(f"- Retest reason: {event['retest_reason']}")
    lines.extend([
        "",
        "This observation has been coalesced into the durable assessment owner. Review the new delta or discussion before dispositioning the work item.",
    ])
    return "\n".join(lines)


def coalesce_issue(repo: str, issue: dict[str, Any], event: dict[str, Any], token: str) -> bool:
    body = issue.get("body") or ""
    marker = event_marker(event)
    if marker in body:
        print(f"[dedupe-trigger] #{issue.get('number')} {marker}")
        return False
    new_body = body.rstrip() + "\n" + trigger_appendix(event) + "\n"
    payload: dict[str, Any] = {"body": new_body}
    # Repository-change events advance the visible work-item revision window.
    if event.get("source") == "repository-change" and event.get("title"):
        payload["title"] = event["title"]
    request("PATCH", f"https://api.github.com/repos/{repo}/issues/{issue['number']}", token, payload)
    print(f"[coalesced] #{issue.get('number')} <- {event.get('assessment_key')}")
    return True


def reopen_owner(repo: str, issue: dict[str, Any], event: dict[str, Any], token: str) -> dict[str, Any]:
    """Reopen a terminal proposition owner only after an explicit invalidation signal."""
    if not explicit_retest(event):
        raise ValueError("closed assessment owner may only reopen with reopen_closed=true and retest_reason")
    body = issue.get("body") or ""
    marker = event_marker(event)
    new_body = body if marker in body else body.rstrip() + "\n" + trigger_appendix(event) + "\n"
    payload: dict[str, Any] = {"state": "open", "body": new_body}
    if event.get("source") == "repository-change" and event.get("title"):
        payload["title"] = event["title"]
    reopened = request("PATCH", f"https://api.github.com/repos/{repo}/issues/{issue['number']}", token, payload)
    print(f"[reopened] #{issue.get('number')} <- {event.get('assessment_key')}: {event.get('retest_reason')}")
    return reopened


def self_test() -> None:
    """Regression coverage for proposition ownership, terminal suppression and epochs."""
    issues = [
        {
            "state": "open",
            "number": 343,
            "body": "<!-- rahp-assessment-key:dtg:portfolio:material-change-set:2026-08-31 -->",
        },
        {
            "state": "open",
            "number": 420,
            "body": "<!-- rahp-assessment-key:dtg:repository:sankarshanmukhopadhyay/dtgwg-zkp-tf -->",
        },
        {
            "state": "closed",
            "number": 589,
            "body": "<!-- rahp-assessment-key:dtg:portfolio:combined:backup-evidence-integrity -->",
        },
        # Regression fixture for the Sep 11 duplicate episode: the later closed duplicate
        # must not steal ownership from an earlier still-open durable owner.
        {
            "state": "open",
            "number": 590,
            "body": "<!-- rahp-assessment-key:dtg:portfolio:combined:spec-dependency-alignment -->",
        },
        {
            "state": "closed",
            "number": 615,
            "body": "<!-- rahp-assessment-key:dtg:portfolio:combined:spec-dependency-alignment -->",
        },
    ]
    index = issue_owner_by_key(issues)
    assert index["dtg:portfolio:material-change-set:2026-08-31"]["number"] == 343
    assert "dtg:portfolio:material-change-set:2026-09-01" not in index
    assert "dtg:portfolio:material-change-set:2026-08-31:lineage:clean-a" not in index
    assert index["dtg:repository:sankarshanmukhopadhyay/dtgwg-zkp-tf"]["number"] == 420
    assert index["dtg:portfolio:combined:backup-evidence-integrity"]["number"] == 589
    assert index["dtg:portfolio:combined:backup-evidence-integrity"]["state"] == "closed"
    assert index["dtg:portfolio:combined:spec-dependency-alignment"]["number"] == 590

    same_epoch = {"assessment_key": "dtg:portfolio:material-change-set:2026-08-31", "observed_at": "2026-08-31"}
    later_epoch = {"assessment_key": "dtg:portfolio:material-change-set:2026-09-01", "observed_at": "2026-09-01"}
    lineage_epoch = {"assessment_key": "dtg:portfolio:material-change-set:2026-08-31:lineage:clean-a", "observed_at": "2026-08-31"}
    repeated_closed = {"assessment_key": "dtg:portfolio:combined:backup-evidence-integrity", "observed_at": "2026-09-12"}
    invalidating_retest = {
        **repeated_closed,
        "reopen_closed": True,
        "retest_reason": "authoritative source changed a proposition premise",
    }
    malformed_retest = {**repeated_closed, "reopen_closed": True}

    assert index.get(same_epoch["assessment_key"], {}).get("number") == 343
    assert index.get(later_epoch["assessment_key"]) is None
    assert index.get(lineage_epoch["assessment_key"]) is None
    assert explicit_retest(repeated_closed) is False
    assert explicit_retest(malformed_retest) is False
    assert explicit_retest(invalidating_retest) is True
    assert event_marker(same_epoch) == "<!-- rahp-trigger:dtg:portfolio:material-change-set:2026-08-31@2026-08-31 -->"
    print("self-test: proposition owners survive closure; repeated observations do not create successors")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--events", type=Path)
    ap.add_argument(
        "--repository",
        default=CANONICAL_RAHP_ISSUE_REPOSITORY,
        help="RAHP issue repository; non-canonical destinations are rejected",
    )
    ap.add_argument("--result-json", type=Path, help="write created/coalesced issue references")
    ap.add_argument("--self-test", action="store_true", help="run publisher regression tests and exit")
    args = ap.parse_args()
    if args.self_test:
        self_test()
        return 0
    if args.events is None:
        raise SystemExit("--events is required unless --self-test is used")
    try:
        args.repository = enforce_publication_repository(args.repository)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    if not token:
        raise SystemExit("GITHUB_TOKEN or GH_TOKEN is required")
    events = json.loads(args.events.read_text()) if args.events.exists() else []
    if not events:
        if args.result_json:
            args.result_json.parent.mkdir(parents=True, exist_ok=True)
            args.result_json.write_text(json.dumps({"issues": []}, indent=2) + "\n", encoding="utf-8")
        print("no assessment issues to publish")
        return 0

    issues = existing_issues(args.repository, token)
    owner_by_key = issue_owner_by_key(issues)
    known_titles = {i.get("title", "") for i in issues}
    created = coalesced = reopened = suppressed = 0
    published: list[dict[str, Any]] = []

    for event in events:
        key = event.get("assessment_key")
        related = event.get("related_assessment_key")
        target = owner_by_key.get(related) if related else None
        target = target or (owner_by_key.get(key) if key else None)
        if target:
            owner_key = related or key
            if target.get("state") == "open":
                if coalesce_issue(args.repository, target, event, token):
                    coalesced += 1
                published.append({"action": "coalesced", "number": target.get("number"), "url": target.get("html_url"), "assessment_key": owner_key})
                continue
            if explicit_retest(event):
                target = reopen_owner(args.repository, target, event, token)
                reopened += 1
                if owner_key:
                    owner_by_key[owner_key] = target
                published.append({"action": "reopened", "number": target.get("number"), "url": target.get("html_url"), "assessment_key": owner_key, "retest_reason": event.get("retest_reason")})
                continue
            suppressed += 1
            print(f"[terminal-owner] #{target.get('number')} retains {owner_key}; observation recorded without successor issue")
            published.append({"action": "terminal-owner", "number": target.get("number"), "url": target.get("html_url"), "assessment_key": owner_key, "observation": event_marker(event)})
            continue

        title = event["title"]
        # Backward compatibility for unkeyed events generated by older tooling.
        if not key and title in known_titles:
            print(f"[dedupe-title] {title}")
            continue
        labels = event.get("labels") or ["assessment-required"]
        for label in labels:
            ensure_label(args.repository, label, token)
        body = event["body"]
        if key and f"rahp-assessment-key:{key}" not in body:
            body = f"<!-- rahp-assessment-key:{key} -->\n\n" + body
        assignees = event.get("assignees") or CANONICAL_RAHP_ASSIGNEES
        issue = request(
            "POST",
            f"https://api.github.com/repos/{args.repository}/issues",
            token,
            {"title": title, "body": body, "labels": labels, "assignees": assignees},
        )
        print(f"[created] #{issue.get('number')} {title}")
        known_titles.add(title)
        if key:
            owner_by_key[key] = issue
        published.append({"action": "created", "number": issue.get("number"), "url": issue.get("html_url"), "assessment_key": key})
        created += 1

    if args.result_json:
        args.result_json.parent.mkdir(parents=True, exist_ok=True)
        args.result_json.write_text(json.dumps({"issues": published}, indent=2) + "\n", encoding="utf-8")
    print(f"created {created} issue(s); coalesced {coalesced} event(s); reopened {reopened}; terminal-owner suppressions {suppressed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
