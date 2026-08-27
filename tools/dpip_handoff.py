#!/usr/bin/env python3
"""Transport explicitly promoted RAHP privacy referrals to DPIP.

This tool intentionally does *not* decide which RAHP findings are privacy relevant.
It only transports open RAHP issues already labelled ``assurance:dpip-requested``
after validating the documented promotion-gate payload.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

import yaml

DEFAULT_RAHP_REPO = "sankarshanmukhopadhyay/rahp-toolkit"
DEFAULT_DPIP_REPO = "sankarshanmukhopadhyay/dtg-privacy-implementation-profile"
REQUESTED = "assurance:dpip-requested"
OPEN = "assurance:dpip-open"
COMPLETE = "assurance:dpip-complete"


def api(method: str, repo: str, path: str, token: str, payload: Any | None = None) -> Any:
    url = f"https://api.github.com/repos/{repo}/{path.lstrip('/')}"
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "rahp-dpip-handoff/1.1",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {token}",
        **({"Content-Type": "application/json"} if data is not None else {}),
    })
    with urllib.request.urlopen(req, timeout=30) as response:
        raw = response.read()
    return json.loads(raw) if raw else None


def yaml_blocks(body: str) -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = []
    for match in re.finditer(r"```ya?ml\s*\n(.*?)```", body or "", re.DOTALL | re.IGNORECASE):
        try:
            parsed = yaml.safe_load(match.group(1))
        except yaml.YAMLError:
            continue
        if isinstance(parsed, dict):
            blocks.append(parsed)
    return blocks


def handoff_payload(body: str) -> dict[str, Any]:
    for block in yaml_blocks(body):
        value = block.get("dpip")
        if isinstance(value, dict):
            return value
    raise ValueError("no machine-readable `dpip:` YAML block found")


def validate_payload(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    source = payload.get("source_change")
    if not isinstance(source, dict):
        return ["source_change must be a mapping"]
    for key in ("monitor_fingerprint", "repository", "revision"):
        if not str(source.get(key, "")).strip():
            errors.append(f"source_change.{key} is required for automated promotion")
    targets = []
    for key in ("affected_interactions", "affected_reference_flows", "affected_invariants", "affected_claims"):
        value = payload.get(key, [])
        if isinstance(value, list):
            targets.extend(str(item) for item in value if str(item).strip())
    if not targets:
        errors.append("at least one DPIP target is required")
    if not str(payload.get("question", "")).strip():
        errors.append("an actionable DPIP examination question is required")
    return errors


def identity(source_issue: int, payload: dict[str, Any]) -> tuple[str, str]:
    source = payload["source_change"]
    target_material = {key: payload.get(key, []) for key in (
        "affected_interactions", "affected_reference_flows", "affected_invariants",
        "affected_claims", "suspected_surfaces")}
    target_material["question"] = payload.get("question", "")
    digest = hashlib.sha256(json.dumps(target_material, sort_keys=True, separators=(",", ":")).encode()).hexdigest()[:16]
    marker = f"<!-- rahp-dpip-handoff:{source_issue}:{source['monitor_fingerprint']}:{source['revision']}:{digest} -->"
    return marker, digest


def issue_has_label(issue: dict[str, Any], label: str) -> bool:
    return any(item.get("name") == label for item in issue.get("labels", []))


def list_requested(repo: str, token: str) -> list[dict[str, Any]]:
    label = urllib.parse.quote(REQUESTED, safe="")
    return api("GET", repo, f"issues?state=open&labels={label}&per_page=100", token) or []


def find_existing(dpip_repo: str, token: str, marker: str) -> dict[str, Any] | None:
    label = urllib.parse.quote("source:rahp", safe="")
    issues = api("GET", dpip_repo, f"issues?state=all&labels={label}&per_page=100", token) or []
    for issue in issues:
        if marker in (issue.get("body") or ""):
            return issue
    return None


def create_intake(rahp_repo: str, dpip_repo: str, rahp_issue: dict[str, Any], payload: dict[str, Any], marker: str, dpip_token: str) -> dict[str, Any]:
    source = payload["source_change"]
    source_block = {"source": {
        "system": "RAHP", "repository": rahp_repo, "issue": rahp_issue["number"],
        "portfolio_monitor": {"fingerprint": source["monitor_fingerprint"], **({"finding_id": source["monitor_finding_id"]} if source.get("monitor_finding_id") else {})},
        "changed_artifact": {"repository": source["repository"], "revision": source["revision"], **({"pull_request": source["pull_request"]} if source.get("pull_request") else {})},
    }}
    requested = {"requested_examination": {key: value for key, value in {
        "interactions": payload.get("affected_interactions", []),
        "reference_flows": payload.get("affected_reference_flows", []),
        "invariants": payload.get("affected_invariants", []),
        "claims": payload.get("affected_claims", []),
        "suspected_surfaces": payload.get("suspected_surfaces", []),
        "question": payload.get("question", ""),
    }.items() if value}}
    body = (
        f"{marker}\n\n## Source\n\nAutomated handoff from `{rahp_repo}#{rahp_issue['number']}`.\n\n"
        f"```yaml\n{yaml.safe_dump(source_block, sort_keys=False).rstrip()}\n```\n\n"
        f"## Requested examination\n\n```yaml\n{yaml.safe_dump(requested, sort_keys=False).rstrip()}\n```\n\n"
        "## Boundary\n\nRAHP does not prejudge the DPIP result. DPIP owns applicability, evidence assessment, scoped conclusion, and return disposition.\n"
    )
    title = f"[RAHP intake] {rahp_issue['title'].removeprefix('[DPIP candidate] ').removeprefix('[DPIP requested] ')}"
    return api("POST", dpip_repo, "issues", dpip_token, {
        "title": title[:256], "body": body, "assignees": ["sankarshanmukhopadhyay"],
        "labels": ["source:rahp", "run:requested"],
    })


def transition_source(rahp_repo: str, issue_number: int, dpip_issue: dict[str, Any], token: str) -> None:
    comments = api("GET", rahp_repo, f"issues/{issue_number}/comments?per_page=100", token) or []
    backlink_marker = f"<!-- rahp-dpip-open:{dpip_issue['number']} -->"
    if not any(backlink_marker in (comment.get("body") or "") for comment in comments):
        api("POST", rahp_repo, f"issues/{issue_number}/comments", token, {"body": (
            f"{backlink_marker}\nDPIP examination opened: {dpip_issue['html_url']}\n\n"
            "The referral passed the RAHP promotion gate. DPIP now owns applicability and the scoped privacy conclusion."
        )})
    api("POST", rahp_repo, f"issues/{issue_number}/labels", token, {"labels": [OPEN]})
    try:
        api("DELETE", rahp_repo, f"issues/{issue_number}/labels/{urllib.parse.quote(REQUESTED, safe='')}", token)
    except urllib.error.HTTPError as exc:
        if exc.code != 404:
            raise


def run(rahp_repo: str, dpip_repo: str, rahp_token: str, dpip_token: str) -> int:
    failures = 0
    for issue in list_requested(rahp_repo, rahp_token):
        if issue_has_label(issue, COMPLETE):
            continue
        try:
            payload = handoff_payload(issue.get("body") or "")
            problems = validate_payload(payload)
            if problems:
                raise ValueError("; ".join(problems))
            marker, _ = identity(issue["number"], payload)
            dpip_issue = find_existing(dpip_repo, dpip_token, marker)
            if dpip_issue is None:
                dpip_issue = create_intake(rahp_repo, dpip_repo, issue, payload, marker, dpip_token)
                print(f"CREATED {dpip_repo}#{dpip_issue['number']} from {rahp_repo}#{issue['number']}")
            else:
                print(f"EXISTS {dpip_repo}#{dpip_issue['number']} for {rahp_repo}#{issue['number']}")
            transition_source(rahp_repo, issue["number"], dpip_issue, rahp_token)
        except Exception as exc:
            failures += 1
            print(f"FAIL {rahp_repo}#{issue.get('number')}: {exc}", file=sys.stderr)
    return 1 if failures else 0


def self_test() -> int:
    body = """```yaml
dpip:
  recommendation: examine
  affected_interactions: [C3]
  affected_reference_flows: [RF-001]
  affected_invariants: [P2, P4]
  source_change:
    monitor_fingerprint: abc123
    repository: example/source
    revision: deadbeef
  question: Does the changed envelope widen correlation scope?
```"""
    payload = handoff_payload(body)
    assert not validate_payload(payload)
    marker1, digest1 = identity(12, payload)
    marker2, digest2 = identity(12, payload)
    assert marker1 == marker2 and digest1 == digest2
    assert "abc123" in marker1 and "deadbeef" in marker1
    bad = dict(payload); bad["question"] = ""
    assert any("question" in error for error in validate_payload(bad))
    print("PASS dpip_handoff self-test")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--rahp-repository", default=os.getenv("RAHP_REPOSITORY", DEFAULT_RAHP_REPO))
    parser.add_argument("--dpip-repository", default=os.getenv("DPIP_REPOSITORY", DEFAULT_DPIP_REPO))
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    rahp_token = os.getenv("GITHUB_TOKEN", "")
    dpip_token = os.getenv("DPIP_HANDOFF_TOKEN", "")
    if not rahp_token:
        print("GITHUB_TOKEN is required", file=sys.stderr)
        return 2
    if not dpip_token:
        print("DPIP_HANDOFF_TOKEN is not configured; refusing to leave qualified referrals stranded.", file=sys.stderr)
        return 2
    return run(args.rahp_repository, args.dpip_repository, rahp_token, dpip_token)


if __name__ == "__main__":
    raise SystemExit(main())
