#!/usr/bin/env python3
"""Derive non-normative RAHP→DPIP lifecycle telemetry from attributable GitHub events."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

import yaml

DEFAULT_RAHP_REPO = "sankarshanmukhopadhyay/rahp-toolkit"
DEFAULT_DPIP_REPO = "sankarshanmukhopadhyay/dtg-privacy-implementation-profile"
OPEN = "assurance:dpip-open"


def api(method: str, repo: str, path: str, token: str, payload: Any | None = None) -> Any:
    url = f"https://api.github.com/repos/{repo}/{path.lstrip('/')}"
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "rahp-dpip-lifecycle/1.0",
            "X-GitHub-Api-Version": "2022-11-28",
            "Authorization": f"Bearer {token}",
            **({"Content-Type": "application/json"} if data is not None else {}),
        },
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        raw = response.read()
    return json.loads(raw) if raw else None


def parse_time(value: str | None) -> dt.datetime | None:
    if not value:
        return None
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))


def seconds_between(start: str | None, end: str | None) -> int | None:
    a, b = parse_time(start), parse_time(end)
    if not a or not b or b < a:
        return None
    return int((b - a).total_seconds())


def first_comment_time(comments: list[dict[str, Any]], predicate) -> str | None:
    matches = [c for c in comments if predicate(c.get("body") or "") and c.get("created_at")]
    if not matches:
        return None
    return min(matches, key=lambda c: c["created_at"])["created_at"]


def find_target_issue(source_comments: list[dict[str, Any]]) -> int | None:
    for comment in source_comments:
        match = re.search(r"<!--\s*rahp-dpip-open:(\d+)\s*-->", comment.get("body") or "")
        if match:
            return int(match.group(1))
    return None


def requested_label_time(events: list[dict[str, Any]]) -> str | None:
    for event in events:
        if event.get("event") == "labeled" and (event.get("label") or {}).get("name") == "assurance:dpip-requested":
            return event.get("created_at")
    return None


def derive(
    source_issue: dict[str, Any],
    source_comments: list[dict[str, Any]],
    source_events: list[dict[str, Any]],
    target_issue: dict[str, Any] | None,
    target_comments: list[dict[str, Any]],
    target_repo: str,
) -> dict[str, Any]:
    target_number = target_issue.get("number") if target_issue else find_target_issue(source_comments)
    referral_created_at = requested_label_time(source_events)
    requested_at = target_issue.get("created_at") if target_issue else None
    admitted_at = first_comment_time(target_comments, lambda b: "dpip-rahp-admission:" in b)
    examination_ready_at = first_comment_time(target_comments, lambda b: "dpip-examination-setup:" in b)
    acquisition_ready_at = first_comment_time(target_comments, lambda b: "dpip-evidence-acquisition:" in b)
    execution_ready_at = first_comment_time(target_comments, lambda b: "dpip-execution-evidence:" in b)
    judgment_recorded_at = first_comment_time(
        target_comments,
        lambda b: "dpip_examination:" in b and "Human acceptance decision" in b,
    )
    returned_at = first_comment_time(
        source_comments,
        lambda b: bool(target_number) and f"<!-- dpip-return:{target_repo}#{target_number} -->" in b,
    )

    ordered = [
        ("returned", returned_at, "RAHP human disposition / residual finding handling"),
        ("judgment-recorded", judgment_recorded_at, "DPIP→RAHP return transport"),
        ("execution-ready", execution_ready_at or acquisition_ready_at, "human DPIP judgment"),
        ("examination-ready", examination_ready_at, "evidence acquisition/execution"),
        ("admitted", admitted_at, "examination setup"),
        ("requested", requested_at, "DPIP admission"),
        ("referral-created", referral_created_at, "DPIP intake creation"),
    ]
    current_stage, waiting_on = "not-observed", "attributable lifecycle event"
    for stage, timestamp, waiting in ordered:
        if timestamp:
            current_stage, waiting_on = stage, waiting
            break

    timeline = {
        "referral_created_at": referral_created_at,
        "requested_at": requested_at,
        "admitted_at": admitted_at,
        "examination_ready_at": examination_ready_at,
        "acquisition_ready_at": acquisition_ready_at,
        "execution_ready_at": execution_ready_at,
        "judgment_recorded_at": judgment_recorded_at,
        "returned_at": returned_at,
    }
    metrics = {
        "referral_to_request_seconds": seconds_between(referral_created_at, requested_at),
        "request_to_admission_seconds": seconds_between(requested_at, admitted_at),
        "admission_to_examination_ready_seconds": seconds_between(admitted_at, examination_ready_at),
        "examination_to_acquisition_ready_seconds": seconds_between(examination_ready_at, acquisition_ready_at),
        "examination_to_execution_ready_seconds": seconds_between(examination_ready_at, execution_ready_at),
        "execution_to_judgment_seconds": seconds_between(execution_ready_at or acquisition_ready_at, judgment_recorded_at),
        "judgment_to_return_seconds": seconds_between(judgment_recorded_at, returned_at),
        "request_to_return_seconds": seconds_between(requested_at, returned_at),
    }
    return {
        "assurance_lifecycle": {
            "source_system": "RAHP",
            "source_repository": source_issue.get("repository_url", DEFAULT_RAHP_REPO),
            "source_issue": source_issue["number"],
            "target_repository": target_repo,
            "target_issue": target_number,
            **timeline,
            "current_stage": current_stage,
            "waiting_on": waiting_on,
            "operational_metrics": metrics,
            "metrics_are_normative": False,
            "assurance_effect": "none",
            "historical_gaps_policy": "leave-null; do-not-invent",
        }
    }


def marker(source_number: int, target_number: int | None) -> str:
    return f"<!-- rahp-dpip-lifecycle:{source_number}:{target_number or 'unknown'} -->"


def render(record: dict[str, Any]) -> str:
    lifecycle = record["assurance_lifecycle"]
    return (
        f"{marker(lifecycle['source_issue'], lifecycle.get('target_issue'))}\n"
        "## RAHP → DPIP lifecycle telemetry\n\n"
        "This record is derived from attributable GitHub issue events and machine-readable pipeline markers. "
        "Elapsed time is **operational telemetry only** and has no effect on assurance validity, severity, or disposition. "
        "Missing historical timestamps remain null rather than being reconstructed from prose.\n\n"
        f"```yaml\n{yaml.safe_dump(record, sort_keys=False).rstrip()}\n```"
    )


def reconcile_one(rahp_repo: str, dpip_repo: str, issue_number: int, rahp_token: str, dpip_token: str) -> None:
    source_issue = api("GET", rahp_repo, f"issues/{issue_number}", rahp_token)
    source_issue["repository_url"] = rahp_repo
    source_comments = api("GET", rahp_repo, f"issues/{issue_number}/comments?per_page=100", rahp_token) or []
    source_events = api("GET", rahp_repo, f"issues/{issue_number}/events?per_page=100", rahp_token) or []
    target_number = find_target_issue(source_comments)
    target_issue = None
    target_comments: list[dict[str, Any]] = []
    if target_number:
        target_issue = api("GET", dpip_repo, f"issues/{target_number}", dpip_token)
        target_comments = api("GET", dpip_repo, f"issues/{target_number}/comments?per_page=100", dpip_token) or []
    record = derive(source_issue, source_comments, source_events, target_issue, target_comments, dpip_repo)
    body = render(record)
    identity = marker(issue_number, target_number)
    existing = next((c for c in source_comments if identity in (c.get("body") or "")), None)
    if existing:
        if existing.get("body") != body:
            api("PATCH", rahp_repo, f"issues/comments/{existing['id']}", rahp_token, {"body": body})
    else:
        api("POST", rahp_repo, f"issues/{issue_number}/comments", rahp_token, {"body": body})


def list_open(repo: str, token: str) -> list[dict[str, Any]]:
    label = urllib.parse.quote(OPEN, safe="")
    return api("GET", repo, f"issues?state=open&labels={label}&per_page=100", token) or []


def self_test() -> int:
    source_issue = {"number": 91, "repository_url": DEFAULT_RAHP_REPO}
    source_comments = [
        {"body": "<!-- rahp-dpip-open:65 -->", "created_at": "2026-08-27T00:00:10Z"},
        {"body": f"<!-- dpip-return:{DEFAULT_DPIP_REPO}#65 -->", "created_at": "2026-08-27T00:10:00Z"},
    ]
    events = [
        {"event": "labeled", "label": {"name": "assurance:dpip-requested"}, "created_at": "2026-08-27T00:00:00Z"}
    ]
    target = {"number": 65, "created_at": "2026-08-27T00:00:10Z"}
    comments = [
        {"body": "<!-- dpip-rahp-admission:65:x -->", "created_at": "2026-08-27T00:01:00Z"},
        {"body": "<!-- dpip-examination-setup:65:x -->", "created_at": "2026-08-27T00:02:00Z"},
        {"body": "<!-- dpip-evidence-acquisition:65:x -->", "created_at": "2026-08-27T00:03:00Z"},
        {"body": "<!-- dpip-execution-evidence:65:x -->", "created_at": "2026-08-27T00:04:00Z"},
        {"body": "```yaml\ndpip_examination:\n  conclusion: INDETERMINATE\n```\n### Human acceptance decision", "created_at": "2026-08-27T00:08:00Z"},
    ]
    record = derive(source_issue, source_comments, events, target, comments, DEFAULT_DPIP_REPO)["assurance_lifecycle"]
    assert record["current_stage"] == "returned"
    assert record["operational_metrics"]["request_to_admission_seconds"] == 50
    assert record["operational_metrics"]["admission_to_examination_ready_seconds"] == 60
    assert record["operational_metrics"]["execution_to_judgment_seconds"] == 240
    assert record["operational_metrics"]["judgment_to_return_seconds"] == 120

    incomplete = derive(
        {"number": 92},
        [{"body": "<!-- rahp-dpip-open:66 -->", "created_at": "2026-08-27T00:00:00Z"}],
        [],
        {"number": 66, "created_at": "2026-08-27T00:00:00Z"},
        [],
        DEFAULT_DPIP_REPO,
    )["assurance_lifecycle"]
    assert incomplete["referral_created_at"] is None
    assert incomplete["current_stage"] == "requested"
    assert incomplete["operational_metrics"]["request_to_admission_seconds"] is None
    print("PASS dpip_lifecycle self-test")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--issue-number", type=int)
    parser.add_argument("--rahp-repository", default=os.getenv("RAHP_REPOSITORY", DEFAULT_RAHP_REPO))
    parser.add_argument("--dpip-repository", default=os.getenv("DPIP_REPOSITORY", DEFAULT_DPIP_REPO))
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    rahp_token = os.getenv("GITHUB_TOKEN", "")
    dpip_token = os.getenv("DPIP_HANDOFF_TOKEN", "") or rahp_token
    if not rahp_token:
        return 2
    issues = [{"number": args.issue_number}] if args.issue_number else list_open(args.rahp_repository, rahp_token)
    failures = 0
    for issue in issues:
        try:
            reconcile_one(args.rahp_repository, args.dpip_repository, int(issue["number"]), rahp_token, dpip_token)
        except Exception as exc:
            failures += 1
            print(f"FAIL {args.rahp_repository}#{issue['number']}: {exc}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
