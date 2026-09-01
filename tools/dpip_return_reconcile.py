#!/usr/bin/env python3
"""Reconcile terminal DPIP dispositions into persistent semantic RAHP obligations."""
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
from assurance_obligation import new_obligation, transition_obligation
from dpip_lifecycle import DEFAULT_DPIP_REPO, DEFAULT_RAHP_REPO, api
from evidence_producer_controller import load_registry, parse_obligation, replace_obligation, resolve_producer

COMPLETE = "assurance:dpip-complete"
OPEN = "assurance:dpip-open"
MODEL_GAP = "assurance:model-gap"
REQUESTED = "assurance:dpip-requested"
RETURN_RE = re.compile(r"<!--\s*dpip-return:([^#\s]+)#(\d+)\s*-->")
YAML_RE = re.compile(r"```ya?ml\s*\n(.*?)```", re.DOTALL | re.IGNORECASE)
RECONCILIATION_VERSION = "v4"
SHA40 = re.compile(r"^[0-9a-f]{40}$", re.I)


def yaml_blocks(body: str) -> list[dict[str, Any]]:
    out = []
    for match in YAML_RE.finditer(body or ""):
        try:
            parsed = yaml.safe_load(match.group(1))
        except yaml.YAMLError:
            continue
        if isinstance(parsed, dict):
            out.append(parsed)
    return out


def parse_return(comments: list[dict[str, Any]]) -> dict[str, Any] | None:
    matches = []
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
    conclusion = str(disposition.get("conclusion") or "UNKNOWN").strip()
    human = disposition.get("human_summary") if isinstance(disposition.get("human_summary"), dict) else {}
    plan = disposition.get("evidence_remediation_plan") if isinstance(disposition.get("evidence_remediation_plan"), dict) else {}
    requirements = plan.get("requirements") if isinstance(plan.get("requirements"), list) else []
    requirement_ids = sorted({str(item.get("id")).strip() for item in requirements if isinstance(item, dict) and item.get("id")})
    supplied_ids = disposition.get("evidence_requirement_ids") if isinstance(disposition.get("evidence_requirement_ids"), list) else []
    requirement_ids = sorted(set(requirement_ids) | {str(v).strip() for v in supplied_ids if str(v).strip()})
    return {
        "target_repository": marker_match.group(1),
        "target_issue": int(marker_match.group(2)),
        "conclusion": conclusion,
        "terminal_reason": str(disposition.get("terminal_reason") or plan.get("reason_code") or "").strip().lower(),
        "action": str(disposition.get("action") or human.get("action") or "").strip(),
        "residual": str(disposition.get("residual_correlation") or disposition.get("residual_risk") or "").strip(),
        "remediation_plan": plan,
        "evidence_requirement_ids": requirement_ids,
        "comment_url": comment.get("html_url"),
    }


def normalize_conclusion(value: str) -> str:
    return re.sub(r"[^A-Z0-9]+", "_", (value or "UNKNOWN").upper()).strip("_")


def base_state(conclusion: str, terminal_reason: str = "") -> str:
    value = normalize_conclusion(conclusion)
    if value in {"PASS", "PASSED", "NOT_APPLICABLE", "NOTAPPLICABLE"}:
        return "resolved"
    if value in {"FAIL", "FAILED"}:
        return "remediation-required"
    if value == "INDETERMINATE":
        return "model-gap" if terminal_reason == "model-gap" else "evidence-external"
    return "controller-error"


def obligation_state(returned: dict[str, Any]) -> tuple[str, dict[str, Any] | None]:
    state = base_state(returned["conclusion"], returned.get("terminal_reason") or "")
    if state == "evidence-external" and returned.get("evidence_requirement_ids"):
        resolved = resolve_producer(returned["evidence_requirement_ids"], load_registry())
        if resolved:
            producer, _ = resolved
            return "evidence-acquirable", producer
    return state, None


def fsm_terminal_state(conclusion: str, terminal_reason: str = "") -> str:
    return terminal_from_specialist(normalize_conclusion(conclusion), terminal_reason)


def residual_labels(state: str) -> list[str]:
    return ["assurance", MODEL_GAP] if state == "model-gap" else ["assurance"]


def reconciliation_marker(source: int, target: int) -> str:
    return f"<!-- rahp-dpip-reconciliation:{RECONCILIATION_VERSION}:{source}:{target} -->"


def legacy_residual_marker(source: int, target: int) -> str:
    return f"<!-- rahp-dpip-residual:v2:{source}:{target} -->"


def semantic_marker(key: str) -> str:
    return f"<!-- rahp-assurance-obligation:v1:{key} -->"


def list_candidates(repo: str, token: str) -> list[dict[str, Any]]:
    by_number: dict[int, dict[str, Any]] = {}
    for label_name in (OPEN, COMPLETE):
        label = urllib.parse.quote(label_name, safe="")
        for issue in api("GET", repo, f"issues?state=open&labels={label}&per_page=100", token) or []:
            by_number[int(issue["number"])] = issue
    return [by_number[n] for n in sorted(by_number)]


def find_residual(repo: str, token: str, marker: str) -> dict[str, Any] | None:
    for page in range(1, 6):
        issues = api("GET", repo, f"issues?state=all&per_page=100&page={page}", token) or []
        for issue in issues:
            if "pull_request" not in issue and marker in (issue.get("body") or ""):
                return issue
        if len(issues) < 100:
            break
    return None


def semantic_scope(issue: dict[str, Any]) -> tuple[str, list[str], str, list[dict[str, str]]]:
    body = str(issue.get("body") or "")
    proposition_ids: list[str] = []
    surfaces: list[str] = []
    flows: list[str] = []
    profile = "generic"
    pins: list[dict[str, str]] = []
    for block in yaml_blocks(body):
        for name in ("dpip", "requested_examination"):
            value = block.get(name) if isinstance(block.get(name), dict) else {}
            canonical = value.get("canonical") if isinstance(value.get("canonical"), dict) else {}
            for key in ("interaction_ids", "invariant_ids", "claim_ids", "profile_ids"):
                proposition_ids.extend(str(x) for x in canonical.get(key, []) or [])
            for key in ("interactions", "invariants", "claims"):
                proposition_ids.extend(str(x) for x in value.get(key, []) or [])
            flows.extend(str(x) for x in (canonical.get("reference_flow_ids", []) or value.get("reference_flows", []) or []))
            surfaces.extend(str(x) for x in value.get("suspected_surfaces", []) or [])
        source = block.get("source") if isinstance(block.get("source"), dict) else {}
        source_change = block.get("dpip", {}).get("source_change") if isinstance(block.get("dpip"), dict) and isinstance(block.get("dpip", {}).get("source_change"), dict) else {}
        for raw in (source.get("source_pins", []) or []) + (block.get("dpip", {}).get("source_pins", []) if isinstance(block.get("dpip"), dict) else []):
            if isinstance(raw, dict) and raw.get("repository") and SHA40.fullmatch(str(raw.get("revision") or "")):
                pins.append({"repository": str(raw["repository"]), "revision": str(raw["revision"])})
        for changed in (source.get("changed_artifact"), source_change):
            if isinstance(changed, dict) and changed.get("repository") and SHA40.fullmatch(str(changed.get("revision") or "")):
                pins.append({"repository": str(changed["repository"]), "revision": str(changed["revision"])})
    canonical_ids = sorted(set(proposition_ids))
    if canonical_ids:
        subject_id = "dpip:" + "+".join(canonical_ids[:8])
    else:
        question = next((str((b.get("requested_examination") or {}).get("question") or (b.get("dpip") or {}).get("question") or "") for b in yaml_blocks(body) if isinstance(b, dict)), "")
        subject_id = "dpip:" + re.sub(r"[^a-z0-9]+", "-", question.lower()).strip("-")[:96]
    boundary = json_key({"flows": sorted(set(flows)), "surfaces": sorted(set(surfaces))})
    unique_pins = list({(p["repository"], p["revision"]): p for p in pins}.values())
    return profile, canonical_ids, subject_id + "|" + boundary, unique_pins


def json_key(value: Any) -> str:
    import json
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def ensure_residual(repo: str, source_issue: dict[str, Any], returned: dict[str, Any], state: str, producer: dict[str, Any] | None, token: str) -> dict[str, Any]:
    profile, proposition_ids, subject_boundary, pins = semantic_scope(source_issue)
    subject_id, boundary = subject_boundary.split("|", 1)
    producer_data = {"mode": "registered-executable", "id": producer["id"], "repository": producer["repository"]} if producer else None
    obligation = new_obligation(
        target_profile=profile, subject_id=subject_id, state=state, proposition_ids=proposition_ids,
        evidence_requirement_ids=returned.get("evidence_requirement_ids") or [], material_boundary=boundary,
        source_pins=pins, lineage=[{"source_issue": int(source_issue["number"]), "specialist_repository": returned["target_repository"], "specialist_issue": returned["target_issue"]}],
        producer=producer_data,
    )
    marker = semantic_marker(obligation["proposition_key"])
    existing = find_residual(repo, token, marker)
    lineage_marker = legacy_residual_marker(source_issue["number"], returned["target_issue"])
    if existing:
        current = parse_obligation(existing.get("body") or "")
        if current:
            updated = transition_obligation(current, state=state, evidence_requirement_ids=returned.get("evidence_requirement_ids") or current.get("evidence_requirement_ids"), source_pins=pins or current.get("source_pins"), lineage=obligation["lineage"][0], producer=producer_data)
            body = replace_obligation(existing.get("body") or "", updated)
            if lineage_marker not in body:
                body += "\n\n" + lineage_marker + "\n"
            api("PATCH", repo, f"issues/{existing['number']}", token, {"body": body, "title": residual_title(source_issue, state)})
        return existing

    source_url = source_issue.get("html_url") or f"https://github.com/{repo}/issues/{source_issue['number']}"
    dpip_url = f"https://github.com/{returned['target_repository']}/issues/{returned['target_issue']}"
    action = returned.get("action") or obligation["artifact_to_produce"]["description"]
    boundary_text = returned.get("residual") or ("The specialist privacy model lacks a complete evidence contract." if state == "model-gap" else "A stronger pinned reassessment is required to supersede this obligation.")
    obligation_yaml = yaml.safe_dump({"obligation": obligation}, sort_keys=False).strip()
    body = f"""{marker}\n{lineage_marker}\n\n## RAHP post-DPIP residual\n\n- Source RAHP referral: {source_url}\n- DPIP examination: {dpip_url}\n- DPIP conclusion: **{returned['conclusion']}**\n- Normalized RAHP obligation state: **`{state}`**\n- Canonical FSM terminal target: **`{fsm_terminal_state(returned['conclusion'], returned.get('terminal_reason') or '')}`**\n\n## Assurance obligation\n\n```yaml\n{obligation_yaml}\n```\n\n## Required action\n\n{action}\n\n## Residual boundary\n\n{boundary_text}\n\n## Closure rule\n\nClose only after a comparable pinned reassessment resolves the proposition. Historical assessment attempts remain immutable.\n"""
    return api("POST", repo, "issues", token, {"title": residual_title(source_issue, state), "body": body, "labels": residual_labels(state), "assignees": ["sankarshanmukhopadhyay"]})


def residual_title(source_issue: dict[str, Any], state: str) -> str:
    title = str(source_issue.get("title") or "DPIP assurance proposition")
    for prefix in ("[DPIP candidate] ", "[DPIP requested] ", "[DPIP residual] "):
        title = title.removeprefix(prefix)
    title = re.sub(r"\s+—\s+(model-gap|evidence-acquirable|evidence-external|evidence-produced|remediation-required|upstream-action|controller-error)$", "", title)
    return f"[DPIP residual] {title} — {state}"[:256]


def remove_label(repo: str, number: int, label: str, token: str) -> None:
    try:
        api("DELETE", repo, f"issues/{number}/labels/{urllib.parse.quote(label, safe='')}", token)
    except urllib.error.HTTPError as exc:
        if exc.code != 404:
            raise


def reconcile_existing_obligation(repo: str, issue: dict[str, Any], returned: dict[str, Any], state: str, producer: dict[str, Any] | None, token: str) -> None:
    current = parse_obligation(issue.get("body") or "")
    if not current:
        raise ValueError("semantic marker present but obligation block is invalid")
    lineage = {"kind": "specialist-reassessment", "specialist_repository": returned["target_repository"], "specialist_issue": returned["target_issue"], "conclusion": returned["conclusion"]}
    if state == "resolved":
        api("POST", repo, f"issues/{issue['number']}/comments", token, {"body": "The comparable specialist reassessment resolved this semantic assurance obligation. Historical attempts and evidence lineage remain preserved in this issue."})
        remove_label(repo, issue["number"], OPEN, token); remove_label(repo, issue["number"], REQUESTED, token)
        api("PATCH", repo, f"issues/{issue['number']}", token, {"state": "closed", "state_reason": "completed"})
        return
    producer_data = {"mode": "registered-executable", "id": producer["id"], "repository": producer["repository"]} if producer else None
    updated = transition_obligation(current, state=state, evidence_requirement_ids=returned.get("evidence_requirement_ids") or current.get("evidence_requirement_ids"), lineage=lineage, producer=producer_data)
    body = replace_obligation(issue.get("body") or "", updated)
    api("PATCH", repo, f"issues/{issue['number']}", token, {"body": body, "title": residual_title(issue, state), "state": "open"})
    remove_label(repo, issue["number"], OPEN, token); remove_label(repo, issue["number"], REQUESTED, token)
    if state == "model-gap":
        api("POST", repo, f"issues/{issue['number']}/labels", token, {"labels": [MODEL_GAP]})
    else:
        remove_label(repo, issue["number"], MODEL_GAP, token)


def reconcile_one(repo: str, number: int, token: str) -> str:
    issue = api("GET", repo, f"issues/{number}", token)
    comments = api("GET", repo, f"issues/{number}/comments?per_page=100", token) or []
    returned = parse_return(comments)
    if returned is None:
        return "no-return"
    identity = reconciliation_marker(number, returned["target_issue"])
    if any(identity in (comment.get("body") or "") for comment in comments):
        return "already-reconciled"
    state, producer = obligation_state(returned)
    existing_obligation = parse_obligation(issue.get("body") or "")
    residual = None
    if existing_obligation:
        reconcile_existing_obligation(repo, issue, returned, state, producer, token)
    elif state != "resolved":
        residual = ensure_residual(repo, issue, returned, state, producer, token)
        remove_label(repo, number, OPEN, token)
        api("PATCH", repo, f"issues/{number}", token, {"state": "closed", "state_reason": "completed"})
    else:
        remove_label(repo, number, OPEN, token)
        api("PATCH", repo, f"issues/{number}", token, {"state": "closed", "state_reason": "completed"})

    lines = [identity, "## RAHP post-DPIP reconciliation", "", f"- DPIP: `{returned['target_repository']}#{returned['target_issue']}`", f"- DPIP conclusion: **{returned['conclusion']}**", f"- RAHP obligation state: **`{state}`**"]
    if residual:
        lines.append(f"- Durable semantic obligation: {residual.get('html_url')}")
    lines += ["", "The specialist attempt is immutable. Any unresolved assurance work remains on one semantic obligation whose state may advance without changing proposition identity."]
    api("POST", repo, f"issues/{number}/comments", token, {"body": "\n".join(lines)})
    return state


def self_test() -> int:
    sample = [{"body": """<!-- dpip-return:sankarshanmukhopadhyay/dtg-privacy-implementation-profile#147 -->\n```yaml\ndpip_disposition:\n  conclusion: INDETERMINATE\n  evidence_remediation_plan:\n    requirements:\n      - id: ER-REL-DID-AB\n      - id: ER-STATUS-AB\n      - id: ER-TASK-AB\n      - id: ER-VERIFIER-AB\n```\n"""}]
    returned = parse_return(sample); assert returned
    state, producer = obligation_state(returned)
    assert state == "evidence-acquirable" and producer and producer["id"] == "composed-unlinkability-v1"
    assert base_state("INDETERMINATE", "model-gap") == "model-gap"
    assert base_state("FAIL") == "remediation-required"
    assert base_state("PASS") == "resolved"
    assert base_state("unexpected") == "controller-error"
    obligation = new_obligation(target_profile="generic", subject_id="dpip:test", state="model-gap", proposition_ids=["P2"], material_boundary="{}")
    body = semantic_marker(obligation["proposition_key"]) + "\n```yaml\n" + yaml.safe_dump({"obligation": obligation}, sort_keys=False) + "```\n"
    current = parse_obligation(body); assert current
    updated = transition_obligation(current, state="evidence-acquirable", evidence_requirement_ids=["ER-CREDENTIAL-ID-AB"], producer={"mode": "registered-executable", "id": "composed-unlinkability-v1"})
    assert updated["proposition_key"] == current["proposition_key"]
    assert parse_obligation(replace_obligation(body, updated))["state"] == "evidence-acquirable"
    print("PASS DPIP return reconciliation: producer-aware routing and in-place semantic obligation transitions")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--self-test", action="store_true"); parser.add_argument("--issue-number", type=int); parser.add_argument("--rahp-repository", default=os.getenv("RAHP_REPOSITORY", DEFAULT_RAHP_REPO)); parser.add_argument("--dpip-repository", default=os.getenv("DPIP_REPOSITORY", DEFAULT_DPIP_REPO)); args = parser.parse_args()
    if args.self_test:
        return self_test()
    token = os.getenv("GITHUB_TOKEN", "")
    if not token:
        print("GITHUB_TOKEN is required", file=sys.stderr); return 2
    issues = [api("GET", args.rahp_repository, f"issues/{args.issue_number}", token)] if args.issue_number else list_candidates(args.rahp_repository, token)
    failures = 0
    for issue in issues:
        try:
            print(f"{args.rahp_repository}#{issue['number']}: {reconcile_one(args.rahp_repository, int(issue['number']), token)}")
        except Exception as exc:
            failures += 1; print(f"FAIL {args.rahp_repository}#{issue.get('number')}: {exc}", file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
