#!/usr/bin/env python3
"""Reconstruct retained DTG gatherer runs from RAHP issues and compute assurance state."""
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
DEFAULT_RUN_DIR = pathlib.Path("instances/dtg/generated/gatherer-runs")
RUN_RE_TEMPLATE = r"(?:rahp-dtg-gatherer-run:{run}|@gatherer-{run}-)"
EVENT_RE = re.compile(r"rahp-dtg-gatherer-event:([0-9a-f]{20})")
DPIP_DISPOSITION_RE = re.compile(r"dpip_disposition:\s*\n(?:.*\n)*?\s*conclusion:\s*([A-Z_]+)")
DPIP_NOT_REQUIRED = "assurance:dpip-not-required"
DPIP_STATES = {"assurance:dpip-candidate", "assurance:dpip-requested", "assurance:dpip-open", "assurance:dpip-complete"}
STATUS_RANK = {"GREEN": 0, "AMBER": 1, "RED": 2}


def api(path: str, token: str) -> Any:
    req = urllib.request.Request(
        f"https://api.github.com/repos/{REPO}/{path}",
        headers={"Accept":"application/vnd.github+json", "Authorization":f"Bearer {token}",
                 "User-Agent":"rahp-dtg-assurance-reconcile/1.1", "X-GitHub-Api-Version":"2022-11-28"},
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
    coalesced = re.findall(rf"@gatherer-{re.escape(run_id)}-([0-9a-f]{{20}})", text)
    return list(dict.fromkeys(explicit + coalesced))


def dpip_conclusion(comments: list[dict[str, Any]]) -> str | None:
    for comment in reversed(comments):
        m = DPIP_DISPOSITION_RE.search(comment.get("body") or "")
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
        ids = [eid for eid in event_ids(issue, str(run["id"]), comments) if eid in events]
        if not ids:
            continue
        for eid in ids:
            events[eid]["accounted_for"] = True
            events[eid].setdefault("assessment_ids", []).append(f"rahp#{number}")
        states = label_names(issue)
        has_dpip = bool(states & DPIP_STATES)
        explicit_no_dpip = DPIP_NOT_REQUIRED in states
        dpip_complete = "assurance:dpip-complete" in states
        conclusion = dpip_conclusion(comments)
        semantic_terminal = issue.get("state") == "closed" and (explicit_no_dpip or dpip_complete)
        assessments.append({
            "id": f"rahp#{number}", "required": True, "complete": semantic_terminal,
            "adverse": "assessment-adverse" in states or "finding-raised" in states,
            "provenance_valid": bool(ids),
        })
        if has_dpip:
            dpip.append({
                "id": f"rahp#{number}:dpip", "required": True, "complete": dpip_complete,
                "return_received": conclusion is not None, "disposition": conclusion,
                "provenance_valid": bool(ids),
            })
    return {"run": run, "events": list(events.values()), "assessments": assessments, "dpip": dpip}


def list_dtg_issues(token: str) -> list[dict[str, Any]]:
    label = urllib.parse.quote("dtg-instance", safe="")
    all_issues: list[dict[str, Any]] = []
    for page in range(1, 6):
        batch = api(f"issues?state=all&labels={label}&per_page=100&page={page}", token) or []
        all_issues.extend(x for x in batch if "pull_request" not in x)
        if len(batch) < 100:
            break
    return all_issues


def collect_comments(issues: list[dict[str, Any]], run_ids: list[str], token: str) -> dict[int, list[dict[str, Any]]]:
    comments: dict[int, list[dict[str, Any]]] = {}
    for issue in issues:
        body = issue.get("body") or ""
        if any(run_id in body for run_id in run_ids):
            number = int(issue["number"])
            comments[number] = api(f"issues/{number}/comments?per_page=100", token) or []
    return comments


def aggregate(results: list[dict[str, Any]]) -> dict[str, Any]:
    if not results:
        return {"dtg_assurance": {"pipeline_status": "GREEN", "disposition": "NO_PENDING_GATHERER_RUNS", "runs": []}}
    rows = [r["portfolio_assurance"] for r in results]
    worst = max(rows, key=lambda r: STATUS_RANK[r["pipeline_status"]])
    if all(row["pipeline_status"] == "GREEN" for row in rows):
        status, disposition = "GREEN", "ASSURED"
    else:
        status, disposition = worst["pipeline_status"], worst["disposition"]
    return {
        "dtg_assurance": {
            "pipeline_status": status,
            "disposition": disposition,
            "run_count": len(rows),
            "open_or_blocked_runs": sum(1 for row in rows if row["pipeline_status"] != "GREEN"),
            "runs": [{"id": row["run"], "status": row["pipeline_status"], "disposition": row["disposition"]} for row in rows],
        }
    }


def render_aggregate(summary: dict[str, Any]) -> str:
    p = summary["dtg_assurance"]
    lines = ["# DTG End-to-End Assurance", "", f"**{p['pipeline_status']} — {p['disposition']}**", ""]
    if not p.get("runs"):
        lines.append("No retained non-empty gatherer runs require reconciliation.")
    else:
        lines.append(f"{p['run_count']} retained gatherer run(s) · {p['open_or_blocked_runs']} open or blocked")
        lines.extend(["", "## Run lineage"])
        for row in p["runs"]:
            lines.append(f"- `{row['id']}` — **{row['status']} / {row['disposition']}**")
    return "\n".join(lines) + "\n"


def load_runs(run_dir: pathlib.Path) -> list[dict[str, Any]]:
    if not run_dir.exists():
        return []
    runs = [json.loads(path.read_text(encoding="utf-8")) for path in sorted(run_dir.glob("*.json"))]
    return [run for run in runs if run.get("event_count", len(run.get("qualifying_events") or []))]


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--run-dir", type=pathlib.Path, default=DEFAULT_RUN_DIR)
    p.add_argument("--evidence-output", type=pathlib.Path)
    p.add_argument("--result-output", type=pathlib.Path)
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args()
    if args.self_test:
        run = {"id":"r1","fingerprint":"f1","qualifying_events":["a"*20],"event_count":1}
        issue = {"number":7,"state":"closed","labels":[{"name":DPIP_NOT_REQUIRED}],"body":f"<!-- rahp-dtg-gatherer-run:r1 -->\n<!-- rahp-dtg-gatherer-event:{'a'*20} -->"}
        green = compute(normalize(run,[issue],{7:[]}))
        assert green["portfolio_assurance"]["pipeline_status"] == "GREEN"
        issue["state"]="open"
        amber = compute(normalize(run,[issue],{7:[]}))
        assert amber["portfolio_assurance"]["pipeline_status"] == "AMBER"
        overall = aggregate([green, amber])
        assert overall["dtg_assurance"]["pipeline_status"] == "AMBER"
        dpip_issue = {"number":8,"state":"closed","labels":[{"name":"assurance:dpip-complete"}],"body":f"<!-- rahp-dtg-gatherer-run:r1 -->\n<!-- rahp-dtg-gatherer-event:{'a'*20} -->"}
        comments={8:[{"body":"```yaml\ndpip_disposition:\n  conclusion: INDETERMINATE\n```"}]}
        assert compute(normalize(run,[dpip_issue],comments))["portfolio_assurance"]["disposition"] == "INDETERMINATE"
        print("PASS dtg_assurance_reconcile self-test")
        return 0
    runs = load_runs(args.run_dir)
    if not runs:
        summary = aggregate([])
        print(render_aggregate(summary), end="")
        return 0
    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    if not token:
        raise SystemExit("GITHUB_TOKEN or GH_TOKEN is required")
    issues = list_dtg_issues(token)
    comments = collect_comments(issues, [str(run["id"]) for run in runs], token)
    evidence_rows = [normalize(run, issues, comments) for run in runs]
    results = [compute(row) for row in evidence_rows]
    summary = aggregate(results)
    if args.evidence_output:
        args.evidence_output.parent.mkdir(parents=True, exist_ok=True)
        args.evidence_output.write_text(yaml.safe_dump({"runs": evidence_rows}, sort_keys=False), encoding="utf-8")
    if args.result_output:
        args.result_output.parent.mkdir(parents=True, exist_ok=True)
        args.result_output.write_text(yaml.safe_dump({"summary": summary, "runs": results}, sort_keys=False), encoding="utf-8")
    print(render_aggregate(summary), end="")
    for result in results:
        print("\n" + render_markdown(result), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
