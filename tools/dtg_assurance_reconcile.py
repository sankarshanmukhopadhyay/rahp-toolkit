#!/usr/bin/env python3
"""Reconstruct a DTG gatherer run from RAHP issues and compute its assurance state."""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import urllib.parse
import urllib.request
from typing import Any

import yaml

from dtg_portfolio_assurance import compute, render_markdown

REPO = "sankarshanmukhopadhyay/rahp-toolkit"
RUN_RE_TEMPLATE = r"(?:rahp-dtg-gatherer-run:{run}|@gatherer-{run}-)"
EVENT_RE = re.compile(r"rahp-dtg-gatherer-event:([0-9a-f]{20})")
DPIP_DISPOSITION_RE = re.compile(r"dpip_disposition:\s*\n(?:.*\n)*?\s*conclusion:\s*([A-Z_]+)")
DPIP_NOT_REQUIRED = "assurance:dpip-not-required"
DPIP_STATES = {"assurance:dpip-candidate", "assurance:dpip-requested", "assurance:dpip-open", "assurance:dpip-complete"}


def api(path: str, token: str) -> Any:
    req = urllib.request.Request(
        f"https://api.github.com/repos/{REPO}/{path}",
        headers={"Accept":"application/vnd.github+json", "Authorization":f"Bearer {token}",
                 "User-Agent":"rahp-dtg-assurance-reconcile/1.0", "X-GitHub-Api-Version":"2022-11-28"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        raw = r.read()
    return json.loads(raw) if raw else None


def label_names(issue: dict[str, Any]) -> set[str]:
    return {str(x.get("name")) for x in issue.get("labels", [])}


def linked_to_run(issue: dict[str, Any], run_id: str, comments: list[dict[str, Any]] | None = None) -> bool:
    text = (issue.get("body") or "") + "\n" + "\n".join((c.get("body") or "") for c in (comments or []))
    return re.search(RUN_RE_TEMPLATE.format(run=re.escape(run_id)), text) is not None


def event_ids(issue: dict[str, Any], run_id: str, comments: list[dict[str, Any]] | None = None) -> list[str]:
    text = (issue.get("body") or "") + "\n" + "\n".join((c.get("body") or "") for c in (comments or []))
    explicit = EVENT_RE.findall(text)
    if explicit:
        return list(dict.fromkeys(explicit))
    # Coalesced trigger markers retain the event id in observed_at.
    return list(dict.fromkeys(re.findall(rf"@gatherer-{re.escape(run_id)}-([0-9a-f]{{20}})", text)))


def dpip_conclusion(comments: list[dict[str, Any]]) -> str | None:
    for comment in reversed(comments):
        body = comment.get("body") or ""
        m = DPIP_DISPOSITION_RE.search(body)
        if m:
            return m.group(1)
    return None


def normalize(run: dict[str, Any], issues: list[dict[str, Any]], comments_by_issue: dict[int, list[dict[str, Any]]]) -> dict[str, Any]:
    expected = list(run.get("qualifying_events") or [])
    events = {eid: {"id": eid, "accounted_for": False} for eid in expected}
    assessments: list[dict[str, Any]] = []
    dpip: list[dict[str, Any]] = []

    for issue in issues:
        number = int(issue["number"])
        comments = comments_by_issue.get(number, [])
        if not linked_to_run(issue, str(run["id"]), comments):
            continue
        ids = event_ids(issue, str(run["id"]), comments)
        for eid in ids:
            if eid in events:
                events[eid]["accounted_for"] = True
                events[eid].setdefault("assessment_ids", []).append(f"rahp#{number}")
        states = label_names(issue)
        has_dpip = bool(states & DPIP_STATES)
        explicit_no_dpip = DPIP_NOT_REQUIRED in states
        dpip_complete = "assurance:dpip-complete" in states
        conclusion = dpip_conclusion(comments)
        semantic_terminal = issue.get("state") == "closed" and (explicit_no_dpip or dpip_complete)
        assessments.append({
            "id": f"rahp#{number}",
            "required": True,
            "complete": semantic_terminal,
            "adverse": "assessment-adverse" in states or "finding-raised" in states,
            "provenance_valid": bool(ids),
        })
        if has_dpip:
            dpip.append({
                "id": f"rahp#{number}:dpip",
                "required": True,
                "complete": dpip_complete,
                "return_received": conclusion is not None,
                "disposition": conclusion,
                "provenance_valid": bool(ids),
            })
    return {
        "run": run,
        "events": list(events.values()),
        "assessments": assessments,
        "dpip": dpip,
    }


def fetch_lineage(run_id: str, token: str) -> tuple[list[dict[str, Any]], dict[int, list[dict[str, Any]]]]:
    label = urllib.parse.quote("dtg-instance", safe="")
    issues = api(f"issues?state=all&labels={label}&per_page=100", token) or []
    comments: dict[int, list[dict[str, Any]]] = {}
    linked: list[dict[str, Any]] = []
    for issue in issues:
        number = int(issue["number"])
        body = issue.get("body") or ""
        if run_id in body:
            comments[number] = api(f"issues/{number}/comments?per_page=100", token) or []
            linked.append(issue)
            continue
        # Coalesced lineage may live in the issue body trigger appendix; no comment fetch is needed
        # unless the body already suggests this run.
    return linked, comments


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--run-record", type=pathlib.Path, default=pathlib.Path("instances/dtg/generated/gatherer-run.json"))
    p.add_argument("--evidence-output", type=pathlib.Path)
    p.add_argument("--result-output", type=pathlib.Path)
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args()
    if args.self_test:
        run = {"id":"r1","fingerprint":"f1","qualifying_events":["a"*20]}
        issue = {"number":7,"state":"closed","labels":[{"name":DPIP_NOT_REQUIRED}],"body":f"<!-- rahp-dtg-gatherer-run:r1 -->\n<!-- rahp-dtg-gatherer-event:{'a'*20} -->"}
        ev = normalize(run,[issue],{7:[]})
        result = compute(ev)["portfolio_assurance"]
        assert result["pipeline_status"] == "GREEN" and result["disposition"] == "DPIP_NOT_REQUIRED"
        issue["state"]="open"
        assert compute(normalize(run,[issue],{7:[]}))["portfolio_assurance"]["pipeline_status"] == "AMBER"
        dpip_issue = {"number":8,"state":"closed","labels":[{"name":"assurance:dpip-complete"}],"body":f"<!-- rahp-dtg-gatherer-run:r1 -->\n<!-- rahp-dtg-gatherer-event:{'a'*20} -->"}
        comments={8:[{"body":"```yaml\ndpip_disposition:\n  conclusion: INDETERMINATE\n```"}]}
        assert compute(normalize(run,[dpip_issue],comments))["portfolio_assurance"]["disposition"] == "INDETERMINATE"
        print("PASS dtg_assurance_reconcile self-test")
        return 0
    if not args.run_record.exists():
        print("No DTG gatherer run record exists yet; nothing to reconcile.")
        return 0
    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    if not token:
        raise SystemExit("GITHUB_TOKEN or GH_TOKEN is required")
    run = json.loads(args.run_record.read_text(encoding="utf-8"))
    issues, comments = fetch_lineage(str(run["id"]), token)
    evidence = normalize(run, issues, comments)
    result = compute(evidence)
    if args.evidence_output:
        args.evidence_output.parent.mkdir(parents=True, exist_ok=True)
        args.evidence_output.write_text(yaml.safe_dump(evidence, sort_keys=False), encoding="utf-8")
    if args.result_output:
        args.result_output.parent.mkdir(parents=True, exist_ok=True)
        args.result_output.write_text(yaml.safe_dump(result, sort_keys=False), encoding="utf-8")
    print(render_markdown(result), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
