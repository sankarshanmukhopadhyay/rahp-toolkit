#!/usr/bin/env python3
"""Advance routed combined RAHP reviews to deterministic evidence or an explicit judgment gate."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

REPO = "sankarshanmukhopadhyay/rahp-toolkit"
ASSESSMENT = "assessment-required"
JUDGMENT = "judgment-required"
EXECUTED = "assessment-evidence-complete"
MARKER = "<!-- rahp-combined-execution:v1 -->"
FINDING_RE = re.compile(r"([0-9a-f]{20})")


def api(method: str, path: str, token: str, payload: Any | None = None) -> Any:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"https://api.github.com/repos/{REPO}/{path}",
        data=data,
        method=method,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "User-Agent": "rahp-combined-review-worker/1.0",
            "X-GitHub-Api-Version": "2022-11-28",
            **({"Content-Type": "application/json"} if data is not None else {}),
        },
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        raw = response.read()
    return json.loads(raw) if raw else None


def label_names(issue: dict[str, Any]) -> set[str]:
    return {str(item.get("name")) for item in issue.get("labels", [])}


def is_combined(issue: dict[str, Any]) -> bool:
    body = issue.get("body") or ""
    return (
        issue.get("state") == "open"
        and ASSESSMENT in label_names(issue)
        and "dtg:portfolio:combined:" in body
    )


def finding_ids(body: str) -> list[str]:
    return list(dict.fromkeys(FINDING_RE.findall(body or "")))


def render_record(issue: dict[str, Any]) -> str:
    ids = finding_ids(issue.get("body") or "")
    if not ids:
        raise ValueError("combined review contains no reconstructable Portfolio Monitor finding IDs")
    lines = [
        MARKER,
        "## Automated bounded evidence execution",
        "",
        f"- Review issue: #{issue['number']}",
        f"- Routed finding IDs recovered: **{len(ids)}**",
        "- Execution result: **deterministic evidence complete; semantic judgment required**",
        "",
        "### Proposition tested",
        "",
        "Can the routed change set be disposed mechanically, or does RAHP require substantive interpretation of whether assurance propositions were preserved, strengthened, weakened, newly introduced, or left uncertain?",
        "",
        "### Mechanically established",
        "",
        "- The portfolio route is reproducible from durable finding identifiers.",
        "- The work item is explicitly scoped to combined RAHP + security assurance.",
        "- RAHP can establish routing, provenance, scope and deterministic validation boundaries without inventing semantic findings.",
        "- Successful tooling execution is **not** evidence that the underlying security/assurance proposition passed.",
        "",
        "### Falsification / boundary evidence",
        "",
        "- Treating command success as semantic assurance is rejected as a false positive.",
        "- Missing finding identifiers are an execution failure, not a judgment request.",
        "- Composed privacy questions remain outside this review and must use the canonical RAHP → DPIP path.",
        "",
        "### Judgment required",
        "",
        "Classify the material propositions as **preserved / strengthened / weakened / new / uncertain**, identify regressions or reversals of provisional no-action dispositions, and promote any new RAHP finding or composition only when supported by the routed evidence.",
        "",
        "### Routed finding IDs",
        "",
    ]
    lines.extend(f"- `{fid}`" for fid in ids)
    return "\n".join(lines) + "\n"


def ensure_label(name: str, token: str) -> None:
    encoded = urllib.parse.quote(name, safe="")
    try:
        api("GET", f"labels/{encoded}", token)
        return
    except urllib.error.HTTPError as exc:
        if exc.code != 404:
            raise
    api("POST", "labels", token, {"name": name, "color": "fbca04", "description": "RAHP explicit judgment/evidence state"})


def remove_label(issue_number: int, name: str, token: str) -> None:
    encoded = urllib.parse.quote(name, safe="")
    try:
        api("DELETE", f"issues/{issue_number}/labels/{encoded}", token)
    except urllib.error.HTTPError as exc:
        if exc.code != 404:
            raise


def already_recorded(issue_number: int, token: str) -> bool:
    comments = api("GET", f"issues/{issue_number}/comments?per_page=100", token) or []
    return any(MARKER in (comment.get("body") or "") for comment in comments)


def advance(issue: dict[str, Any], token: str) -> None:
    record = render_record(issue)
    if not already_recorded(issue["number"], token):
        api("POST", f"issues/{issue['number']}/comments", token, {"body": record})
    for label in (JUDGMENT, EXECUTED):
        ensure_label(label, token)
    api("POST", f"issues/{issue['number']}/labels", token, {"labels": [JUDGMENT, EXECUTED]})
    remove_label(issue["number"], ASSESSMENT, token)
    print(f"JUDGMENT_REQUIRED #{issue['number']}")


def run(token: str, issue_number: int | None = None) -> int:
    if issue_number:
        issues = [api("GET", f"issues/{issue_number}", token)]
    else:
        encoded = urllib.parse.quote(ASSESSMENT, safe="")
        issues = api("GET", f"issues?state=open&labels={encoded}&per_page=100", token) or []
    failures = 0
    for issue in issues:
        if not is_combined(issue):
            continue
        try:
            advance(issue, token)
        except Exception as exc:
            failures += 1
            print(f"FAIL #{issue.get('number')}: {exc}", file=sys.stderr)
    return 1 if failures else 0


def self_test() -> int:
    issue = {
        "state": "open",
        "number": 121,
        "labels": [{"name": ASSESSMENT}],
        "body": "<!-- rahp-assessment-key:dtg:portfolio:combined:test -->\n- 307e953d00cf9fb48ba7\n- 0bb1b102763cd38950c0\n",
    }
    assert is_combined(issue)
    assert finding_ids(issue["body"]) == ["307e953d00cf9fb48ba7", "0bb1b102763cd38950c0"]
    rendered = render_record(issue)
    assert "semantic judgment required" in rendered
    assert "false positive" in rendered
    print("PASS combined_review_worker self-test")
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
