#!/usr/bin/env python3
"""Fail closed on unresolved monitor-state branches before issue publication.

A signed state branch can survive a failed Actions PR-creation call. Open-PR
checks alone cannot detect that stranded transaction. Historical branches with
one exact merged PR and an unchanged source commit are safe to retain.
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

REPOSITORY = "sankarshanmukhopadhyay/rahp-toolkit"
PREFIX = "refs/heads/automation/instance-monitor-"
SHA = re.compile(r"^[0-9a-f]{40}$")
API = "https://api.github.com/repos/" + REPOSITORY


class StateBranchError(ValueError):
    pass


def api_get(url: str):
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise StateBranchError("GITHUB_TOKEN is required for live branch qualification")
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "Authorization": "Bearer " + token,
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "rahp-monitor-state-branch-guard",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.load(response)
    except (urllib.error.URLError, ValueError) as exc:
        raise StateBranchError("monitor-state branch authority unavailable") from exc


def qualify(refs, get):
    if not isinstance(refs, list):
        raise StateBranchError("malformed monitor-state branch listing")
    seen = set()
    for item in refs:
        if not isinstance(item, dict):
            raise StateBranchError("malformed monitor-state branch")
        ref = item.get("ref")
        sha = (item.get("object") or {}).get("sha")
        if (not isinstance(ref, str) or not ref.startswith(PREFIX)
                or ref in seen or not isinstance(sha, str) or not SHA.fullmatch(sha)):
            raise StateBranchError("ambiguous monitor-state ref or commit")
        seen.add(ref)
        branch = ref.removeprefix("refs/heads/")
        query = urllib.parse.urlencode({
            "state": "all", "head": "sankarshanmukhopadhyay:" + branch,
            "per_page": "100",
        })
        pulls = get(API + "/pulls?" + query)
        if not isinstance(pulls, list) or len(pulls) != 1:
            raise StateBranchError("orphaned or ambiguous monitored-state branch: " + branch)
        pr = pulls[0]
        head = pr.get("head") if isinstance(pr, dict) else None
        if (not isinstance(head, dict)
                or (head.get("repo") or {}).get("full_name") != REPOSITORY
                or head.get("ref") != branch or head.get("sha") != sha
                or pr.get("state") != "closed" or not pr.get("merged_at")):
            raise StateBranchError("unaccepted monitored-state branch: " + branch)
    return len(seen)


def main() -> int:
    try:
        refs = api_get(API + "/git/matching-refs/heads/automation/instance-monitor-")
        count = qualify(refs, api_get)
    except StateBranchError as exc:
        print("BLOCKED before new external issue publication: " + str(exc), file=sys.stderr)
        return 1
    print(f"PASS: {count} retained monitor-state branches have exact merged PRs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
