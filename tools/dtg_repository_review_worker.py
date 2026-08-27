#!/usr/bin/env python3
"""Advance RAHP DTG gatherer repository assessments with bounded auto-disposition."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from typing import Any

import dtg_automated_disposition as auto

REPO = "sankarshanmukhopadhyay/rahp-toolkit"
ASSESSMENT = "assessment-required"
JUDGMENT = "judgment-required"
EXECUTED = "assessment-evidence-complete"
AUTO_DISPOSED = "assessment:auto-disposed"
DPIP_NOT_REQUIRED = "assurance:dpip-not-required"
DPIP_REQUESTED = "assurance:dpip-requested"
MARKER = "<!-- rahp-dtg-repository-execution:v1 -->"
PACKET_MARKER = "<!-- rahp-dtg-repository-judgment-packet:v1 -->"
AUTO_MARKER = "<!-- rahp-dtg-auto-disposition:v1 -->"
KEY_RE = re.compile(r"rahp-assessment-key:(dtg:repository:[^>\n]+)")
CHANGE_RE = re.compile(r"rahp-dtg-change:([^@>]+)@([0-9a-f]{7,40})")
BASE_RE = re.compile(r"Previous assessed/observed SHA\s*\|\s*`([0-9a-f]{7,40})`")
RUN_RE = re.compile(r"rahp-dtg-gatherer-run:([^>\n]+)")
EVENT_RE = re.compile(r"rahp-dtg-gatherer-event:([0-9a-f]{20})")


def api(method: str, path: str, token: str, payload: Any | None = None) -> Any:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"https://api.github.com/repos/{REPO}/{path}", data=data, method=method,
        headers={"Accept": "application/vnd.github+json", "Authorization": f"Bearer {token}",
                 "User-Agent": "rahp-dtg-repository-review-worker/1.2",
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
    return issue.get("state") == "open" and KEY_RE.search(body) is not None and bool({ASSESSMENT, JUDGMENT} & labels(issue))


def provenance(body: str) -> tuple[str, str, str, str]:
    key = KEY_RE.search(body or "")
    change = CHANGE_RE.search(body or "")
    base = BASE_RE.search(body or "")
    if not key or not change or not base:
        raise ValueError("repository review lacks gatherer assessment/base/change provenance")
    return key.group(1).strip(), change.group(1).strip(), base.group(1).strip(), change.group(2).strip()


def lineage(body: str) -> tuple[str | None, str | None]:
    run = RUN_RE.search(body or "")
    event = EVENT_RE.search(body or "")
    return (run.group(1).strip() if run else None, event.group(1) if event else None)


def section(body: str, heading: str) -> str:
    match = re.search(rf"(?ms)^## {re.escape(heading)}\s*\n(.*?)(?=^## |\Z)", body or "")
    return match.group(1).strip() if match else ""


def render_record(issue: dict[str, Any]) -> str:
    body = issue.get("body") or ""
    key, repo, base, sha = provenance(body)
    run_id, event_id = lineage(body)
    lines = [
        MARKER, "## Automated gatherer-native evidence execution", "",
        f"- Review issue: #{issue['number']}", f"- Assessment key: `{key}`", f"- Repository: `{repo}`",
        f"- Gathered revision window: `{base}` → `{sha}`",
    ]
    if run_id:
        lines.append(f"- Gatherer run: `{run_id}`" + (f" / event `{event_id}`" if event_id else ""))
    lines.extend([
        "- Execution result: **gatherer provenance and bounded change evidence complete; automated disposition attempted before human judgment**", "",
        "### Proposition tested", "",
        "Can the gathered repository delta be disposed by explicit evidence-sufficiency rules before requiring human semantic judgment?", "",
        "### Mechanically established", "",
        "- The review is bound to a specific RAHP gatherer assessment key and immutable revision window.",
        "- The issue contains the gathered material-file scope, commit window and materiality rationale.",
        "- Successful worker execution is not a semantic PASS.",
        "- Auto-disposition is permitted only where all required assurance lenses are terminal under an explicit evidence rule.",
        "- Any unresolved composed privacy question must use the canonical RAHP → DPIP referral path.", "",
        "### Falsification boundary", "",
        "Missing provenance or insufficient/contradictory evidence yields uncertainty rather than a manufactured PASS.",
    ])
    return "\n".join(lines) + "\n"


def render_packet(issue: dict[str, Any]) -> str:
    body = issue.get("body") or ""
    key, repo, base, sha = provenance(body)
    run_id, event_id = lineage(body)
    why = section(body, "Why review is required") or "No materiality rationale recovered."
    files = section(body, "Material files") or "No material-file table recovered."
    commits = section(body, "Commits in the change window") or "No commit list recovered."
    lineage_line = f"**Gatherer lineage:** `{run_id}`" + (f" / `{event_id}`" if event_id else "") if run_id else "**Gatherer lineage:** legacy/un-stamped assessment"
    return "\n".join([
        PACKET_MARKER, "## Reviewer judgment packet — gatherer-native repository review", "",
        f"**Assessment:** `{key}`  ", f"**Repository:** `{repo}`  ", f"**Revision window:** `{base}` → `{sha}`  ", lineage_line, "",
        "The automated disposition attempt did not establish every required lens. Human judgment is therefore the exception path for the unresolved dimensions below.", "",
        "### Materiality evidence", "", why, "", "### Gathered file boundary", "", files, "",
        "### Gathered commits", "", commits, "", "### Required judgment", "",
        "Record **preserved / strengthened / weakened / new / uncertain** for the affected assurance proposition(s).", "",
        "Also answer explicitly:",
        "1. Does this change alter an existing RAHP risk, harm, control, guardrail or security assumption?",
        "2. Does it create or alter a cross-specification composition proposition?",
        "3. Does it create a composed privacy/correlation question that warrants a DPIP referral?",
        "4. Is there evidence of regression relative to the previously observed revision?", "",
        "### Required DPIP applicability disposition", "",
        f"Before closing this assessment, record exactly one path: apply `{DPIP_NOT_REQUIRED}` when the judgment finds no DPIP examination is warranted; or add a valid gatherer-native `dpip:` referral block and apply `{DPIP_REQUESTED}` when examination is warranted.",
        "A missing applicability decision is deliberately non-terminal and will keep the end-to-end controller amber.", "",
        "Close the assessment only after the semantic judgment and selected RAHP/DPIP path are durably linked.",
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


def attempt_auto(issue: dict[str, Any], token: str, existing: list[dict[str, Any]]) -> bool:
    _, repo, base, head = provenance(issue.get("body") or "")
    compare = auto.fetch_compare(repo, base, head, token)
    result = auto.assess(compare)
    if not has_marker(existing, AUTO_MARKER):
        api("POST", f"issues/{issue['number']}/comments", token, {"body": auto.render(result, repo, base, head)})
    if not result["terminal"]:
        return False

    for name in (EXECUTED, AUTO_DISPOSED, DPIP_NOT_REQUIRED):
        ensure_label(name, token)
    api("POST", f"issues/{issue['number']}/labels", token, {"labels": [EXECUTED, AUTO_DISPOSED, DPIP_NOT_REQUIRED]})
    remove_label(issue["number"], ASSESSMENT, token)
    remove_label(issue["number"], JUDGMENT, token)
    api("PATCH", f"issues/{issue['number']}", token, {"state": "closed", "state_reason": "completed"})
    print(f"AUTO_DISPOSED #{issue['number']} security={result['security']} risk={result['risk']} harm={result['harm']}")
    return True


def advance(issue: dict[str, Any], token: str) -> None:
    existing = comments(issue["number"], token)
    states = labels(issue)
    if ASSESSMENT in states:
        if not has_marker(existing, MARKER):
            api("POST", f"issues/{issue['number']}/comments", token, {"body": render_record(issue)})
        if attempt_auto(issue, token, existing):
            return
        for name in (JUDGMENT, EXECUTED, DPIP_NOT_REQUIRED):
            ensure_label(name, token)
        api("POST", f"issues/{issue['number']}/labels", token, {"labels": [JUDGMENT, EXECUTED]})
        remove_label(issue["number"], ASSESSMENT, token)
    elif JUDGMENT in states and not has_marker(existing, AUTO_MARKER):
        # Existing judgment-era issues (e.g. live acceptance cases) get one
        # retrospective bounded auto-disposition attempt after this upgrade.
        if attempt_auto(issue, token, existing):
            return
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
    issue = {"state":"open","number":2,"labels":[{"name":ASSESSMENT}],"body":"""<!-- rahp-dtg-gatherer-run:gha-1-1 -->
<!-- rahp-dtg-gatherer-event:aaaaaaaaaaaaaaaaaaaa -->
<!-- rahp-assessment-key:dtg:repository:OpenVTC/openvtc -->
<!-- rahp-dtg-change:OpenVTC/openvtc@1234567890abcdef -->
| Previous assessed/observed SHA | `abcdef0123456789` |
## Why review is required

- specification files changed

## Material files

| File | Status |
|---|---|
| `specs/x.md` | modified |

## Commits in the change window

- `1234567` feat: change semantics
"""}
    assert is_repository_review(issue)
    key, repo, base, sha = provenance(issue["body"])
    assert key == "dtg:repository:OpenVTC/openvtc" and repo == "OpenVTC/openvtc"
    assert base.startswith("abcdef") and sha.startswith("1234567")
    assert lineage(issue["body"]) == ("gha-1-1", "a"*20)
    record, packet = render_record(issue), render_packet(issue)
    assert "automated disposition" in record and "exception path" in packet
    assert DPIP_NOT_REQUIRED in packet and DPIP_REQUESTED in packet
    print("PASS dtg_repository_review_worker self-test")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--issue", type=int); parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    if not token:
        print("GITHUB_TOKEN or GH_TOKEN is required", file=sys.stderr); return 2
    return run(token, args.issue)


if __name__ == "__main__":
    raise SystemExit(main())
