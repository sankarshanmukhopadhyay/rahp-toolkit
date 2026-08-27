#!/usr/bin/env python3
"""Advance RAHP DTG gatherer repository assessments to reviewer-ready judgment packets."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from typing import Any

REPO = "sankarshanmukhopadhyay/rahp-toolkit"
ASSESSMENT = "assessment-required"
JUDGMENT = "judgment-required"
EXECUTED = "assessment-evidence-complete"
MARKER = "<!-- rahp-dtg-repository-execution:v1 -->"
PACKET_MARKER = "<!-- rahp-dtg-repository-judgment-packet:v1 -->"
KEY_RE = re.compile(r"rahp-assessment-key:(dtg:repository:[^>\n]+)")
CHANGE_RE = re.compile(r"rahp-dtg-change:([^@>]+)@([0-9a-f]{7,40})")


def api(method: str, path: str, token: str, payload: Any | None = None) -> Any:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"https://api.github.com/repos/{REPO}/{path}", data=data, method=method,
        headers={"Accept": "application/vnd.github+json", "Authorization": f"Bearer {token}",
                 "User-Agent": "rahp-dtg-repository-review-worker/1.0",
                 "X-GitHub-Api-Version": "2022-11-28",
                 **({"Content-Type": "application/json"} if data is not None else {})},
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        raw = response.read()
    return json.loads(raw) if raw else None


def labels(issue: dict[str, Any]) -> set[str]:
    return {str(x.get("name")) for x in issue.get("labels", [])}


def is_repository_review(issue: dict[str, Any]) -> bool:
    body = issue.get("body") or ""
    return (
        issue.get("state") == "open"
        and KEY_RE.search(body) is not None
        and bool({ASSESSMENT, JUDGMENT} & labels(issue))
    )


def provenance(body: str) -> tuple[str, str, str]:
    key = KEY_RE.search(body or "")
    change = CHANGE_RE.search(body or "")
    if not key or not change:
        raise ValueError("repository review lacks gatherer assessment/change provenance")
    return key.group(1).strip(), change.group(1).strip(), change.group(2).strip()


def section(body: str, heading: str) -> str:
    match = re.search(rf"(?ms)^## {re.escape(heading)}\s*\n(.*?)(?=^## |\Z)", body or "")
    return (match.group(1).strip() if match else "")


def render_record(issue: dict[str, Any]) -> str:
    key, repo, sha = provenance(issue.get("body") or "")
    return "\n".join([
        MARKER,
        "## Automated gatherer-native evidence execution",
        "",
        f"- Review issue: #{issue['number']}",
        f"- Assessment key: `{key}`",
        f"- Repository: `{repo}`",
        f"- Gathered target revision: `{sha}`",
        "- Execution result: **gatherer provenance and bounded change evidence complete; semantic judgment required**",
        "",
        "### Proposition tested",
        "",
        "Can the gathered repository delta be reviewed from RAHP's own revision, changed-file, commit and materiality evidence without relying on an external portfolio monitor?",
        "",
        "### Mechanically established",
        "",
        "- The review is bound to a specific RAHP gatherer assessment key and target revision.",
        "- The issue already contains the gathered material-file scope, commit window and materiality rationale.",
        "- Successful worker execution is not a semantic PASS.",
        "- Any composed privacy question must use the canonical RAHP → DPIP referral path rather than being inferred here.",
        "",
        "### Falsification boundary",
        "",
        "If the issue lacks the gatherer assessment key or target revision marker, execution fails rather than manufacturing provenance.",
    ]) + "\n"


def render_packet(issue: dict[str, Any]) -> str:
    body = issue.get("body") or ""
    key, repo, sha = provenance(body)
    why = section(body, "Why review is required") or "No materiality rationale recovered."
    files = section(body, "Material files") or "No material-file table recovered."
    commits = section(body, "Commits in the change window") or "No commit list recovered."
    return "\n".join([
        PACKET_MARKER,
        "## Reviewer judgment packet — gatherer-native repository review",
        "",
        f"**Assessment:** `{key}`  ",
        f"**Repository:** `{repo}`  ",
        f"**Target revision:** `{sha}`",
        "",
        "### Materiality evidence",
        "",
        why,
        "",
        "### Gathered file boundary",
        "",
        files,
        "",
        "### Gathered commits",
        "",
        commits,
        "",
        "### Required judgment",
        "",
        "Record **preserved / strengthened / weakened / new / uncertain** for the affected assurance proposition(s).",
        "",
        "Also answer explicitly:",
        "1. Does this change alter an existing RAHP risk, harm, control, guardrail or security assumption?",
        "2. Does it create or alter a cross-specification composition proposition?",
        "3. Does it create a composed privacy/correlation question that warrants a DPIP referral?",
        "4. Is there evidence of regression relative to the previously observed revision?",
        "",
        "Close the assessment only after the judgment and any RAHP/DPIP follow-up are durably linked.",
    ]) + "\n"


def ensure_label(name: str, token: str) -> None:
    encoded = urllib.parse.quote(name, safe="")
    try:
        api("GET", f"labels/{encoded}", token)
    except Exception:
        api("POST", "labels", token, {"name": name, "color": "fbca04", "description": "RAHP explicit judgment/evidence state"})


def remove_label(number: int, name: str, token: str) -> None:
    encoded = urllib.parse.quote(name, safe="")
    try:
        api("DELETE", f"issues/{number}/labels/{encoded}", token)
    except Exception:
        pass


def comments(number: int, token: str) -> list[dict[str, Any]]:
    return api("GET", f"issues/{number}/comments?per_page=100", token) or []


def has_marker(items: list[dict[str, Any]], marker: str) -> bool:
    return any(marker in (x.get("body") or "") for x in items)


def advance(issue: dict[str, Any], token: str) -> None:
    existing = comments(issue["number"], token)
    states = labels(issue)
    if ASSESSMENT in states:
        if not has_marker(existing, MARKER):
            api("POST", f"issues/{issue['number']}/comments", token, {"body": render_record(issue)})
        for name in (JUDGMENT, EXECUTED):
            ensure_label(name, token)
        api("POST", f"issues/{issue['number']}/labels", token, {"labels": [JUDGMENT, EXECUTED]})
        remove_label(issue["number"], ASSESSMENT, token)
    if not has_marker(existing, PACKET_MARKER):
        api("POST", f"issues/{issue['number']}/comments", token, {"body": render_packet(issue)})
    print(f"JUDGMENT_READY #{issue['number']}")


def run(token: str, issue_number: int | None = None) -> int:
    if issue_number:
        issues = [api("GET", f"issues/{issue_number}", token)]
    else:
        encoded = urllib.parse.quote("dtg-instance", safe="")
        issues = api("GET", f"issues?state=open&labels={encoded}&per_page=100", token) or []
    failures = 0
    for issue in issues:
        if not is_repository_review(issue):
            continue
        try:
            advance(issue, token)
        except Exception as exc:
            failures += 1
            print(f"FAIL #{issue.get('number')}: {exc}", file=sys.stderr)
    return 1 if failures else 0


def self_test() -> int:
    issue = {
        "state": "open", "number": 2, "labels": [{"name": ASSESSMENT}],
        "body": """<!-- rahp-assessment-key:dtg:repository:OpenVTC/openvtc -->
<!-- rahp-dtg-change:OpenVTC/openvtc@1234567890abcdef -->
## Why review is required

- specification files changed

## Material files

| File | Status |
|---|---|
| `specs/x.md` | modified |

## Commits in the change window

- `1234567` feat: change semantics
""",
    }
    assert is_repository_review(issue)
    key, repo, sha = provenance(issue["body"])
    assert key == "dtg:repository:OpenVTC/openvtc"
    assert repo == "OpenVTC/openvtc" and sha.startswith("1234567")
    record = render_record(issue)
    packet = render_packet(issue)
    assert "external portfolio monitor" in record
    assert "composed privacy/correlation" in packet
    assert "specs/x.md" in packet
    print("PASS dtg_repository_review_worker self-test")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--issue", type=int)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    if not token:
        print("GITHUB_TOKEN or GH_TOKEN is required", file=sys.stderr)
        return 2
    return run(token, args.issue)


if __name__ == "__main__":
    raise SystemExit(main())
