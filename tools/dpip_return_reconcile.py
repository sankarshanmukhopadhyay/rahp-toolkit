#!/usr/bin/env python3
"""Terminally reconcile returned DPIP dispositions into RAHP-owned state.

A completed specialist handoff must not leave its RAHP referral container open
merely because the assurance proposition remains unresolved. This reconciler turns a
machine-readable DPIP return into one finite RAHP transition and distinguishes missing
evidence from an assurance-model/evidence-contract gap.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
import urllib.error
import urllib.parse
from typing import Any

import yaml

from assurance_fsm import terminal_from_specialist
from dpip_lifecycle import DEFAULT_DPIP_REPO, DEFAULT_RAHP_REPO, api

COMPLETE = "assurance:dpip-complete"
OPEN = "assurance:dpip-open"
RETURN_RE = re.compile(r"<!--\s*dpip-return:([^#\s]+)#(\d+)\s*-->")
YAML_RE = re.compile(r"```ya?ml\s*\n(.*?)```", re.DOTALL | re.IGNORECASE)
RECONCILIATION_VERSION = "v2"


def yaml_blocks(body: str) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for match in YAML_RE.finditer(body or ""):
        try:
            parsed = yaml.safe_load(match.group(1))
        except yaml.YAMLError:
            continue
        if isinstance(parsed, dict):
            out.append(parsed)
    return out


def parse_return(comments: list[dict[str, Any]]) -> dict[str, Any] | None:
    matches: list[tuple[dict[str, Any], re.Match[str]]] = []
    for comment in comments:
        body = comment.get("body") or ""
        match = RETURN_RE.search(body)
        if match:
            matches.append((comment, match))
    if not matches:
        return None
    comment, marker_match = matches[-1]
    body = comment.get("body") or ""
    disposition: dict[str, Any] = {}
    for block in yaml_blocks(body):
        value = block.get("dpip_disposition")
        if isinstance(value, dict):
            disposition = value
            break
    conclusion = str(disposition.get("conclusion") or "").strip()
    if not conclusion:
        fallback = re.search(r"(?:conclusion|outcome):\s*[*`\"']*([A-Z][A-Z_-]+)", body, re.IGNORECASE)
        if fallback:
            conclusion = fallback.group(1)
    human = disposition.get("human_summary") if isinstance(disposition.get("human_summary"), dict) else {}
    action = str(disposition.get("action") or human.get("action") or "").strip()
    residual = str(disposition.get("residual_correlation") or disposition.get("residual_risk") or "").strip()
    plan = disposition.get("evidence_remediation_plan") if isinstance(disposition.get("evidence_remediation_plan"), dict) else {}
    terminal_reason = str(disposition.get("terminal_reason") or plan.get("reason_code") or "").strip().lower()
    return {
        "target_repository": marker_match.group(1),
        "target_issue": int(marker_match.group(2)),
        "conclusion": conclusion or "UNKNOWN",
        "terminal_reason": terminal_reason,
        "action": action,
        "residual": residual,
        "remediation_plan": plan,
        "comment_url": comment.get("html_url"),
    }


def normalize_conclusion(value: str) -> str:
    return re.sub(r"[^A-Z0-9]+", "_", (value or "UNKNOWN").upper()).strip("_")


def reconciliation_state(conclusion: str, terminal_reason: str = "") -> str:
    value = normalize_conclusion(conclusion)
    if value in {"PASS", "PASSED", "NOT_APPLICABLE", "NOTAPPLICABLE"}:
        return "resolved"
    if value in {"FAIL", "FAILED"}:
        return "finding-open"
    if value == "INDETERMINATE":
        return "model-gap" if terminal_reason == "model-gap" else "evidence-required"
    return "controller-contract-error"


def fsm_terminal_state(conclusion: str, terminal_reason: str = "") -> str:
    return terminal_from_specialist(normalize_conclusion(conclusion), terminal_reason)


def is_referral_container(issue: dict[str, Any]) -> bool:
    title = str(issue.get("title") or "")
    body = str(issue.get("body") or "")
    if title.startswith("[DPIP candidate]") or title.startswith("[DPIP requested]"):
        return True
    return bool(re.search(r"```ya?ml\s*\n\s*dpip:\s*", body, re.IGNORECASE))


def reconciliation_marker(source: int, target: int) -> str:
    return f"<!-- rahp-dpip-reconciliation:{RECONCILIATION_VERSION}:{source}:{target} -->"


def residual_marker(source: int, target: int) -> str:
    return f"<!-- rahp-dpip-residual:{RECONCILIATION_VERSION}:{source}:{target} -->"


def list_candidates(repo: str, token: str) -> list[dict[str, Any]]:
    by_number: dict[int, dict[str, Any]] = {}
    for label_name in (OPEN, COMPLETE):
        label = urllib.parse.quote(label_name, safe="")
        issues = api("GET", repo, f"issues?state=open&labels={label}&per_page=100", token) or []
        for issue in issues:
            by_number[int(issue["number"])] = issue
    return [by_number[number] for number in sorted(by_number)]


def find_residual(repo: str, token: str, marker: str) -> dict[str, Any] | None:
    for page in range(1, 6):
        issues = api("GET", repo, f"issues?state=all&per_page=100&page={page}", token) or []
        if not issues:
            break
        for issue in issues:
            if "pull_request" not in issue and marker in (issue.get("body") or ""):
                return issue
        if len(issues) < 100:
            break
    return None


def residual_title(source_issue: dict[str, Any], state: str) -> str:
    title = str(source_issue.get("title") or "DPIP assurance proposition")
    for prefix in ("[DPIP candidate] ", "[DPIP requested] "):
        if title.startswith(prefix):
            title = title[len(prefix):]
    return f"[DPIP residual] {title} — {state}"[:256]


def ensure_residual(repo: str, source_issue: dict[str, Any], returned: dict[str, Any], state: str, token: str) -> dict[str, Any]:
    marker = residual_marker(source_issue["number"], returned["target_issue"])
    existing = find_residual(repo, token, marker)
    if existing:
        return existing
    source_url = source_issue.get("html_url") or f"https://github.com/{repo}/issues/{source_issue['number']}"
    dpip_url = f"https://github.com/{returned['target_repository']}/issues/{returned['target_issue']}"
    action = returned.get("action") or "Perform the explicit evidence/remediation action required by the returned DPIP disposition and execute a pinned retest."
    if state == "model-gap":
        boundary = "The privacy proposition is material, but the specialist evidence model lacks a canonical requirement/producer binding for it. Define that contract and run a new pinned examination; do not infer PASS or FAIL from the absence of a model binding."
    else:
        boundary = returned.get("residual") or "The returned specialist result is not sufficient to close the assurance proposition; only the explicitly required evidence/remediation can change this residual state."
    body = f"""{marker}

## RAHP post-DPIP residual

This issue is the durable RAHP owner created by terminal reconciliation of a completed specialist handoff.

- Source RAHP referral: {source_url}
- DPIP examination: {dpip_url}
- DPIP conclusion: **{returned['conclusion']}**
- Specialist terminal reason: **`{returned.get('terminal_reason') or 'n/a'}`**
- Normalized RAHP reconciliation state: **`{state}`**
- Canonical FSM terminal target: **`{fsm_terminal_state(returned['conclusion'], returned.get('terminal_reason') or '')}`**

## Required action

{action}

## Residual boundary

{boundary}

## Closure rule

Close only after attributable remediation/evidence plus a comparable pinned reassessment supports a terminal RAHP disposition. The completed referral container being closed is **not** evidence of privacy PASS.
"""
    return api("POST", repo, "issues", token, {"title": residual_title(source_issue, state), "body": body, "labels": ["assurance"], "assignees": ["sankarshanmukhopadhyay"]})


def remove_label(repo: str, number: int, label: str, token: str) -> None:
    try:
        api("DELETE", repo, f"issues/{number}/labels/{urllib.parse.quote(label, safe='')}", token)
    except urllib.error.HTTPError as exc:
        if exc.code != 404:
            raise


def reconcile_one(repo: str, number: int, token: str) -> str:
    issue = api("GET", repo, f"issues/{number}", token)
    comments = api("GET", repo, f"issues/{number}/comments?per_page=100", token) or []
    returned = parse_return(comments)
    if returned is None:
        return "no-return"
    identity = reconciliation_marker(number, returned["target_issue"])
    if any(identity in (comment.get("body") or "") for comment in comments):
        return "already-reconciled"

    state = reconciliation_state(returned["conclusion"], returned.get("terminal_reason") or "")
    referral = is_referral_container(issue)
    residual = None
    if state != "resolved" and referral:
        residual = ensure_residual(repo, issue, returned, state, token)

    lines = [identity, "## RAHP post-DPIP reconciliation", "", f"- DPIP: `{returned['target_repository']}#{returned['target_issue']}`", f"- DPIP conclusion: **{returned['conclusion']}**", f"- Specialist terminal reason: **`{returned.get('terminal_reason') or 'n/a'}`**", f"- RAHP reconciliation state: **`{state}`**"]
    if residual:
        lines.append(f"- Durable RAHP residual owner: {residual.get('html_url')}")
    lines += ["", "The specialist handoff is complete. Closing this referral container does **not** convert FAIL or INDETERMINATE to PASS; unresolved work is carried by the durable residual above."]
    if not referral:
        lines += ["", "This issue is not recognizably a referral-only container, so it is left open for explicit RAHP review rather than being auto-closed."]
    api("POST", repo, f"issues/{number}/comments", token, {"body": "\n".join(lines)})
    remove_label(repo, number, OPEN, token)
    if referral:
        api("PATCH", repo, f"issues/{number}", token, {"state": "closed", "state_reason": "completed"})
    return state


def self_test() -> int:
    sample = [{"body": """<!-- dpip-return:sankarshanmukhopadhyay/dtg-privacy-implementation-profile#147 -->
```yaml
dpip_disposition:
  conclusion: INDETERMINATE
  action: Produce attributable A/B evidence and rerun.
  residual_correlation: Correlation cannot be ruled in or out.
```
"""}]
    parsed = parse_return(sample)
    assert parsed and parsed["target_issue"] == 147
    assert parsed["conclusion"] == "INDETERMINATE"
    assert reconciliation_state(parsed["conclusion"]) == "evidence-required"
    assert fsm_terminal_state("INDETERMINATE") == "TERMINAL_INDETERMINATE_EVIDENCE_REQUIRED"

    model_gap = [{"body": """<!-- dpip-return:sankarshanmukhopadhyay/dtg-privacy-implementation-profile#149 -->
```yaml
dpip_disposition:
  conclusion: INDETERMINATE
  terminal_reason: model-gap
  action: Define the evidence contract and rerun.
  evidence_remediation_plan:
    reason_code: model-gap
    requirements:
      - id: MODEL-GAP-abc
        routing_target: dpip-model-gap
```
"""}]
    parsed_gap = parse_return(model_gap)
    assert parsed_gap and parsed_gap["target_issue"] == 149 and parsed_gap["terminal_reason"] == "model-gap"
    assert reconciliation_state(parsed_gap["conclusion"], parsed_gap["terminal_reason"]) == "model-gap"
    assert fsm_terminal_state(parsed_gap["conclusion"], parsed_gap["terminal_reason"]) == "TERMINAL_INDETERMINATE_MODEL_GAP"

    assert reconciliation_state("FAIL") == "finding-open"
    assert reconciliation_state("PASS") == "resolved"
    assert reconciliation_state("NOT_APPLICABLE") == "resolved"
    assert reconciliation_state("unexpected") == "controller-contract-error"
    assert is_referral_container({"title": "[DPIP requested] test", "body": ""})
    assert not is_referral_container({"title": "Composite assessment", "body": ""})
    assert reconciliation_marker(309, 149) == "<!-- rahp-dpip-reconciliation:v2:309:149 -->"
    assert set((OPEN, COMPLETE)) == {"assurance:dpip-open", "assurance:dpip-complete"}
    print("PASS dpip_return_reconcile self-test including #309/#149 model-gap")
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
    token = os.getenv("GITHUB_TOKEN", "")
    if not token:
        print("GITHUB_TOKEN is required", file=sys.stderr)
        return 2
    issues = [api("GET", args.rahp_repository, f"issues/{args.issue_number}", token)] if args.issue_number else list_candidates(args.rahp_repository, token)
    failures = 0
    for issue in issues:
        try:
            result = reconcile_one(args.rahp_repository, int(issue["number"]), token)
            print(f"{args.rahp_repository}#{issue['number']}: {result}")
        except Exception as exc:
            failures += 1
            print(f"FAIL {args.rahp_repository}#{issue.get('number')}: {exc}", file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
