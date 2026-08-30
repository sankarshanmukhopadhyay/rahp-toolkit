#!/usr/bin/env python3
"""Transport explicitly promoted RAHP privacy referrals to DPIP.

RAHP owns promotion of a privacy question. Once promoted, this transport preserves
canonical examination identifiers, immutable source pins, evidence requirements,
supplied evidence bindings and human-readable presentation metadata without making
the DPIP privacy judgment.
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
CANONICAL_KEYS = (
    "interaction_ids", "reference_flow_ids", "invariant_ids", "claim_ids",
    "profile_ids", "evidence_requirement_ids",
)
EVIDENCE_PROVENANCE_KEYS = (
    "producer", "run_id", "observed_at", "implementation_repository",
    "implementation_revision", "context_a_run", "context_b_run",
)
SHA40 = re.compile(r"^[0-9a-f]{40}$", re.I)


def api(method: str, repo: str, path: str, token: str, payload: Any | None = None) -> Any:
    url = f"https://api.github.com/repos/{repo}/{path.lstrip('/')}"
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "rahp-dpip-handoff/1.4",
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


def lineage_id(source: dict[str, Any]) -> str:
    return str(source.get("gatherer_run_id") or source.get("monitor_fingerprint") or "").strip()


def _strings(value: Any) -> list[str]:
    return [str(item).strip() for item in value] if isinstance(value, list) else []


def canonical_contract(payload: dict[str, Any]) -> dict[str, Any]:
    canonical = payload.get("canonical") if isinstance(payload.get("canonical"), dict) else {}
    out: dict[str, Any] = {}
    for key in CANONICAL_KEYS:
        values = _strings(canonical.get(key, payload.get(key, [])))
        if values:
            out[key] = values
    descriptors = canonical.get("descriptors", payload.get("descriptors", []))
    if isinstance(descriptors, list) and descriptors:
        out["descriptors"] = descriptors
    return out


def source_pins(payload: dict[str, Any]) -> list[dict[str, str]]:
    pins: list[dict[str, str]] = []
    for raw in payload.get("source_pins", []) or []:
        if not isinstance(raw, dict):
            continue
        repository = str(raw.get("repository") or "").strip()
        revision = str(raw.get("revision") or "").strip()
        if repository and SHA40.fullmatch(revision):
            pins.append({
                "label": str(raw.get("label") or repository).strip(),
                "repository": repository,
                "revision": revision,
            })
    source = payload.get("source_change") or {}
    repository = str(source.get("repository") or "").strip()
    revision = str(source.get("revision") or "").strip()
    if repository and SHA40.fullmatch(revision):
        implicit = {"label": "Changed artifact", "repository": repository, "revision": revision}
        if not any(p["repository"] == repository and p["revision"].lower() == revision.lower() for p in pins):
            pins.insert(0, implicit)
    return pins


def provided_evidence(payload: dict[str, Any]) -> list[dict[str, Any]]:
    raw = payload.get("provided_evidence", [])
    if raw is None:
        return []
    if not isinstance(raw, list):
        raise ValueError("provided_evidence must be a list")
    return raw


def validate_evidence(records: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    for index, record in enumerate(records):
        prefix = f"provided_evidence[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{prefix} must be a mapping")
            continue
        requirement_id = str(record.get("requirement_id") or "").strip()
        if not requirement_id:
            errors.append(f"{prefix}.requirement_id is required")
        elif requirement_id in seen:
            errors.append(f"duplicate supplied evidence for requirement {requirement_id}")
        else:
            seen.add(requirement_id)
        if not str(record.get("evidence_class") or "").strip():
            errors.append(f"{prefix}.evidence_class is required")
        provenance = record.get("provenance")
        if not isinstance(provenance, dict):
            errors.append(f"{prefix}.provenance must be a mapping")
        else:
            for key in EVIDENCE_PROVENANCE_KEYS:
                if not str(provenance.get(key) or "").strip():
                    errors.append(f"{prefix}.provenance.{key} is required")
            revision = str(provenance.get("implementation_revision") or "")
            if revision and not SHA40.fullmatch(revision):
                errors.append(f"{prefix}.provenance.implementation_revision must be an immutable 40-hex commit SHA")
        if not isinstance(record.get("surfaces"), dict):
            errors.append(f"{prefix}.surfaces must be a mapping")
        if not str(record.get("observation_summary") or "").strip():
            errors.append(f"{prefix}.observation_summary is required")
    return errors


def validate_payload(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    source = payload.get("source_change")
    if not isinstance(source, dict):
        return ["source_change must be a mapping"]
    if not lineage_id(source):
        errors.append("source_change.gatherer_run_id or source_change.monitor_fingerprint is required for automated promotion")
    for key in ("repository", "revision"):
        if not str(source.get(key, "")).strip():
            errors.append(f"source_change.{key} is required for automated promotion")
    legacy_targets: list[str] = []
    for key in ("affected_interactions", "affected_reference_flows", "affected_invariants", "affected_claims"):
        legacy_targets.extend(_strings(payload.get(key, [])))
    typed_targets = [item for key, values in canonical_contract(payload).items() if key != "descriptors" for item in (values if isinstance(values, list) else [])]
    if not legacy_targets and not typed_targets:
        errors.append("at least one legacy or canonical DPIP target is required")
    if not str(payload.get("question", "")).strip():
        errors.append("an actionable DPIP examination question is required")
    try:
        errors.extend(validate_evidence(provided_evidence(payload)))
    except ValueError as exc:
        errors.append(str(exc))
    return errors


def identity(source_issue: int, payload: dict[str, Any]) -> tuple[str, str]:
    source = payload["source_change"]
    target_material = {key: payload.get(key, []) for key in (
        "affected_interactions", "affected_reference_flows", "affected_invariants",
        "affected_claims", "suspected_surfaces")}
    target_material["canonical"] = canonical_contract(payload)
    target_material["source_pins"] = source_pins(payload)
    target_material["provided_evidence"] = provided_evidence(payload)
    target_material["question"] = payload.get("question", "")
    digest = hashlib.sha256(json.dumps(target_material, sort_keys=True, separators=(",", ":")).encode()).hexdigest()[:16]
    marker = f"<!-- rahp-dpip-handoff:{source_issue}:{lineage_id(source)}:{source['revision']}:{digest} -->"
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
    source_data: dict[str, Any] = {
        "system": "RAHP", "repository": rahp_repo, "issue": rahp_issue["number"],
        "changed_artifact": {"repository": source["repository"], "revision": source["revision"], **({"pull_request": source["pull_request"]} if source.get("pull_request") else {})},
        "source_pins": source_pins(payload),
    }
    if source.get("gatherer_run_id"):
        source_data["gatherer"] = {"run_id": source["gatherer_run_id"], **({"event_id": source["gatherer_event_id"]} if source.get("gatherer_event_id") else {})}
    if source.get("monitor_fingerprint"):
        source_data["portfolio_monitor"] = {"fingerprint": source["monitor_fingerprint"], **({"finding_id": source["monitor_finding_id"]} if source.get("monitor_finding_id") else {})}
    source_block = {"source": source_data}
    requested_data = {key: value for key, value in {
        "interactions": payload.get("affected_interactions", []),
        "reference_flows": payload.get("affected_reference_flows", []),
        "invariants": payload.get("affected_invariants", []),
        "claims": payload.get("affected_claims", []),
        "suspected_surfaces": payload.get("suspected_surfaces", []),
        "canonical": canonical_contract(payload),
        "provided_evidence": provided_evidence(payload),
        "question": payload.get("question", ""),
    }.items() if value}
    requested = {"requested_examination": requested_data}
    body = (
        f"{marker}\n\n## Source\n\nAutomated handoff from `{rahp_repo}#{rahp_issue['number']}`.\n\n"
        f"```yaml\n{yaml.safe_dump(source_block, sort_keys=False).rstrip()}\n```\n\n"
        f"## Requested examination\n\n```yaml\n{yaml.safe_dump(requested, sort_keys=False).rstrip()}\n```\n\n"
        "## Boundary\n\nRAHP transports supplied evidence without deciding whether it is sufficient. DPIP owns applicability, evidence-class acceptance, evidence assessment, scoped conclusion, and return disposition. Canonical identifiers are machine keys; DPIP must resolve them to human-readable titles and explanations in reviewer-facing output.\n"
    )
    title = f"[RAHP intake] {rahp_issue['title'].removeprefix('[DPIP candidate] ').removeprefix('[DPIP requested] ')}"
    return api("POST", dpip_repo, "issues", dpip_token, {"title": title[:256], "body": body, "assignees": ["sankarshanmukhopadhyay"], "labels": ["source:rahp", "run:requested"]})


def transition_source(rahp_repo: str, issue_number: int, dpip_issue: dict[str, Any], token: str) -> None:
    comments = api("GET", rahp_repo, f"issues/{issue_number}/comments?per_page=100", token) or []
    backlink_marker = f"<!-- rahp-dpip-open:{dpip_issue['number']} -->"
    if not any(backlink_marker in (comment.get("body") or "") for comment in comments):
        api("POST", rahp_repo, f"issues/{issue_number}/comments", token, {"body": f"{backlink_marker}\nDPIP examination opened: {dpip_issue['html_url']}\n\nThe referral passed the RAHP promotion gate. DPIP now owns applicability and the scoped privacy conclusion."})
    api("POST", rahp_repo, f"issues/{issue_number}/labels", token, {"labels": [OPEN]})
    try:
        api("DELETE", rahp_repo, f"issues/{issue_number}/labels/{urllib.parse.quote(REQUESTED, safe='')}", token)
    except urllib.error.HTTPError as exc:
        if exc.code != 404:
            raise


def run(rahp_repo: str, dpip_repo: str, rahp_token: str, dpip_token: str, issue_numbers: list[int] | None = None) -> int:
    failures = 0
    issues = [api("GET", rahp_repo, f"issues/{number}", rahp_token) for number in issue_numbers] if issue_numbers else list_requested(rahp_repo, rahp_token)
    for issue in issues:
        if not issue_has_label(issue, REQUESTED) or issue_has_label(issue, COMPLETE):
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
    dogwood_sha = "cb01d0a758863fb3a02f9f4eef2c4f15f56c4c3b"
    dogwood = {
        "source_change": {"gatherer_run_id": "dogwood-rc1", "repository": "OpenVTC/verifiable-trust-infrastructure", "revision": dogwood_sha},
        "question": "Does Dogwood RC-1 preserve correlation resistance across composed interactions?",
        "canonical": {
            "interaction_ids": ["C3", "C5"],
            "reference_flow_ids": ["RF-001", "RF-003"],
            "claim_ids": ["C3-PC-5", "C5-PC-2"],
            "evidence_requirement_ids": ["ER-REL-DID-AB", "ER-STATUS-AB", "ER-TASK-AB", "ER-VERIFIER-AB"],
            "descriptors": [
                {"id": "C3", "title": "Asymmetric cross-community relationship privacy"},
                {"id": "C5", "title": "Privacy-preserving lifecycle evaluation and precedence"},
            ],
        },
    }
    assert not validate_payload(dogwood)
    assert source_pins(dogwood)[0]["revision"] == dogwood_sha
    assert canonical_contract(dogwood)["interaction_ids"] == ["C3", "C5"]
    digest1 = identity(225, dogwood)[1]
    changed = json.loads(json.dumps(dogwood)); changed["canonical"]["evidence_requirement_ids"].append("ER-NEW")
    assert identity(225, changed)[1] != digest1

    evidence = {
        "requirement_id": "ER-REL-DID-AB",
        "evidence_class": "runtime-upstream-observation",
        "provenance": {
            "producer": "trust-protocol-interop-lab",
            "run_id": "run-001",
            "observed_at": "2026-08-30T00:00:00Z",
            "implementation_repository": "OpenVTC/verifiable-trust-infrastructure",
            "implementation_revision": dogwood_sha,
            "context_a_run": "A-001",
            "context_b_run": "B-001",
        },
        "observation_summary": "Two-context runtime relationship observations.",
        "surfaces": {"relationship_did": {"classification": "fresh", "context_a": "did:example:a", "context_b": "did:example:b"}},
    }
    supplied = json.loads(json.dumps(dogwood)); supplied["provided_evidence"] = [evidence]
    assert not validate_payload(supplied)
    assert identity(225, supplied)[1] != digest1
    changed_evidence = json.loads(json.dumps(supplied)); changed_evidence["provided_evidence"][0]["provenance"]["run_id"] = "run-002"
    assert identity(225, changed_evidence)[1] != identity(225, supplied)[1]
    malformed = json.loads(json.dumps(supplied)); malformed["provided_evidence"][0]["provenance"]["implementation_revision"] = "main"
    assert any("implementation_revision" in item for item in validate_payload(malformed))

    legacy = {"affected_interactions": ["C3"], "source_change": {"monitor_fingerprint": "abc123", "repository": "example/source", "revision": "deadbeef"}, "question": "Does correlation widen?"}
    assert not validate_payload(legacy)
    print("PASS dpip_handoff self-test")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--rahp-repository", default=os.getenv("RAHP_REPOSITORY", DEFAULT_RAHP_REPO))
    parser.add_argument("--dpip-repository", default=os.getenv("DPIP_REPOSITORY", DEFAULT_DPIP_REPO))
    parser.add_argument("--issue-number", type=int, action="append", default=[], help="process a freshly published RAHP referral directly")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    rahp_token = os.getenv("GITHUB_TOKEN", "")
    dpip_token = os.getenv("DPIP_HANDOFF_TOKEN", "")
    if not rahp_token:
        print("GITHUB_TOKEN is required", file=sys.stderr); return 2
    if not dpip_token:
        print("DPIP_HANDOFF_TOKEN is not configured; refusing to leave qualified referrals stranded.", file=sys.stderr); return 2
    return run(args.rahp_repository, args.dpip_repository, rahp_token, dpip_token, args.issue_number or None)


if __name__ == "__main__":
    raise SystemExit(main())
