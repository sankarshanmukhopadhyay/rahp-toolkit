#!/usr/bin/env python3
"""Escalate provenance-insufficient specialist returns without reacquisition loops.

A registered producer may produce valid evidence for its own composition/runtime while
DPIP correctly rejects that evidence as insufficiently attributable to the original
target implementation. Once that has happened, re-running the same producer cannot
satisfy the missing provenance class. The same semantic obligation therefore advances
to `evidence-external`; RAHP must not manufacture target attribution by replaying the
registered producer.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from typing import Any

import yaml

from assurance_obligation import transition_obligation
from dpip_lifecycle import api
from evidence_producer_controller import MARKER_RE, parse_obligation, replace_obligation

DEFAULT_REPO = "sankarshanmukhopadhyay/rahp-toolkit"
RETURN_RE = re.compile(r"<!--\s*dpip-return:[^#\s]+#\d+\s*-->", re.I)
TITLE_STATE_RE = re.compile(r"\s+—\s+(model-gap|evidence-acquirable|evidence-external|evidence-stale|evidence-produced|remediation-required|upstream-action|controller-error)$")


def latest_return_body(comments: list[dict[str, Any]]) -> str:
    bodies = [str(c.get("body") or "") for c in comments if RETURN_RE.search(str(c.get("body") or ""))]
    return bodies[-1] if bodies else ""


def latest_specialist_lineage(obligation: dict[str, Any]) -> dict[str, Any] | None:
    items = [x for x in obligation.get("lineage", []) or [] if isinstance(x, dict) and x.get("kind") == "specialist-reassessment"]
    return items[-1] if items else None


def has_prior_evidence_production(obligation: dict[str, Any]) -> bool:
    return any(isinstance(x, dict) and x.get("kind") == "evidence-production" for x in obligation.get("lineage", []) or [])


def provenance_insufficient(obligation: dict[str, Any], return_body: str) -> bool:
    """True only after a real producer attempt followed by an INDETERMINATE return.

    The textual check is deliberately narrow and mirrors DPIP's current machine/human
    disposition wording. It is not used to infer privacy outcome; it only distinguishes
    `same producer can acquire missing evidence` from `target authority must supply it`.
    """
    latest = latest_specialist_lineage(obligation)
    if not latest or str(latest.get("conclusion") or "").upper() != "INDETERMINATE":
        return False
    if not has_prior_evidence_production(obligation):
        return False
    body = return_body.lower()
    return (
        "provenance-insufficient" in body
        or "do not prove upstream runtime behaviour" in body
        or "accepted provenance class" in body and "evidence_used: []" in body
    )


def external_owner(obligation: dict[str, Any]) -> dict[str, Any]:
    producer_repo = str((obligation.get("producer") or {}).get("repository") or "")
    for pin in obligation.get("source_pins", []) or []:
        if not isinstance(pin, dict):
            continue
        repo = str(pin.get("repository") or "")
        if repo and repo != producer_repo:
            return {"surface": "external", "repository": repo}
    return {"surface": "external"}


def route_issue(repo: str, issue: dict[str, Any], token: str) -> str:
    obligation = parse_obligation(issue.get("body") or "")
    if not obligation:
        return "not-obligation"
    if obligation.get("state") not in {"evidence-acquirable", "evidence-produced"}:
        return str(obligation.get("state") or "unknown")
    comments = api("GET", repo, f"issues/{issue['number']}/comments?per_page=100", token) or []
    returned = latest_return_body(comments)
    if not provenance_insufficient(obligation, returned):
        return str(obligation.get("state"))

    updated = transition_obligation(
        obligation,
        state="evidence-external",
        action_owner=external_owner(obligation),
        artifact_to_produce={
            "kind": "runtime-evidence",
            "description": "Supply attributable runtime evidence from the original target implementation/deployment in the accepted evidence class. Interop/composition evidence already produced for this contract was judged provenance-insufficient and must not be relabelled as target evidence.",
        },
        producer={"mode": "external"},
        lineage={
            "kind": "provenance-escalation",
            "reason": "registered-producer-evidence-insufficient-for-target-attribution",
        },
    )
    body = replace_obligation(issue.get("body") or "", updated)
    title = TITLE_STATE_RE.sub("", str(issue.get("title") or "DPIP assurance obligation")) + " — evidence-external"
    api("PATCH", repo, f"issues/{issue['number']}", token, {"body": body, "title": title[:256]})
    marker = "<!-- rahp-provenance-escalation:v1 -->"
    if not any(marker in str(c.get("body") or "") for c in comments):
        api("POST", repo, f"issues/{issue['number']}/comments", token, {"body": marker + "\nThe registered producer completed a real evidence attempt, but DPIP rejected that evidence as insufficiently attributable to the original target runtime. This same semantic obligation is now `evidence-external`; the target/deployment authority must supply the attributable package. RAHP will not replay the same producer or synthesize target provenance."})
    return "evidence-external"


def list_active(repo: str, token: str) -> list[dict[str, Any]]:
    issues = api("GET", repo, "issues?state=open&labels=assurance&per_page=100", token) or []
    return [i for i in issues if MARKER_RE.search(str(i.get("body") or ""))]


def self_test() -> int:
    obligation = {
        "state": "evidence-acquirable",
        "producer": {"mode": "registered-executable", "repository": "example/producer"},
        "source_pins": [
            {"repository": "example/target", "revision": "a" * 40},
            {"repository": "example/producer", "revision": "b" * 40},
        ],
        "lineage": [
            {"kind": "evidence-production", "dispatch_key": "evidence-1"},
            {"kind": "specialist-reassessment", "conclusion": "INDETERMINATE"},
        ],
    }
    assert provenance_insufficient(obligation, "Missing or provenance-insufficient evidence. Repository-native fixtures do not prove upstream runtime behaviour.")
    assert external_owner(obligation) == {"surface": "external", "repository": "example/target"}
    no_attempt = dict(obligation); no_attempt["lineage"] = [{"kind": "specialist-reassessment", "conclusion": "INDETERMINATE"}]
    assert not provenance_insufficient(no_attempt, "provenance-insufficient")
    failed = dict(obligation); failed["lineage"] = [{"kind": "evidence-production"}, {"kind": "specialist-reassessment", "conclusion": "FAIL"}]
    assert not provenance_insufficient(failed, "provenance-insufficient")
    print("PASS provenance-insufficient producer evidence escalates to external target authority without changing assurance outcome")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--self-test", action="store_true"); parser.add_argument("--issue-number", type=int); parser.add_argument("--repository", default=os.getenv("RAHP_REPOSITORY", DEFAULT_REPO)); args = parser.parse_args()
    if args.self_test:
        return self_test()
    token = os.getenv("GITHUB_TOKEN", "")
    if not token:
        print("GITHUB_TOKEN is required", file=sys.stderr); return 2
    issues = [api("GET", args.repository, f"issues/{args.issue_number}", token)] if args.issue_number else list_active(args.repository, token)
    failures = 0
    for issue in issues:
        try:
            print(f"{args.repository}#{issue['number']}: {route_issue(args.repository, issue, token)}")
        except Exception as exc:
            failures += 1; print(f"FAIL {args.repository}#{issue.get('number')}: {exc}", file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
