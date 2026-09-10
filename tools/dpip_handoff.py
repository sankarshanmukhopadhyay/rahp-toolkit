#!/usr/bin/env python3
"""Transport explicitly promoted RAHP privacy referrals to DPIP.

RAHP owns promotion of a privacy question. This transport separates durable
proposition identity, source-referral identity, and bounded DPIP examination
identity without making a privacy judgment.
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
SOURCE_LABEL = "source:rahp"
RUN_COMPLETE = "run:complete"
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
        "User-Agent": "rahp-dpip-handoff/2.0",
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


def _digest(material: Any, length: int = 20) -> str:
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()[:length]


def proposition_material(payload: dict[str, Any]) -> dict[str, Any]:
    canonical = {k: v for k, v in canonical_contract(payload).items() if k != "descriptors"}
    return {
        "affected_interactions": payload.get("affected_interactions", []),
        "affected_reference_flows": payload.get("affected_reference_flows", []),
        "affected_invariants": payload.get("affected_invariants", []),
        "affected_claims": payload.get("affected_claims", []),
        "suspected_surfaces": payload.get("suspected_surfaces", []),
        "canonical": canonical,
        "question": str(payload.get("question", "")).strip(),
    }


def proposition_id(payload: dict[str, Any]) -> str:
    return f"rahp-proposition:{_digest(proposition_material(payload))}"


def examination_material(payload: dict[str, Any]) -> dict[str, Any]:
    source = payload["source_change"]
    return {
        "proposition_id": proposition_id(payload),
        "changed_artifact": {
            "repository": str(source.get("repository") or "").strip(),
            "revision": str(source.get("revision") or "").strip(),
        },
        "source_pins": source_pins(payload),
        "provided_evidence": provided_evidence(payload),
        "requested_scope": proposition_material(payload),
    }


def examination_key(payload: dict[str, Any]) -> str:
    return _digest(examination_material(payload))


def referral_id(source_issue: int, payload: dict[str, Any]) -> str:
    source = payload["source_change"]
    return _digest({
        "source_issue": source_issue,
        "lineage": lineage_id(source),
        "revision": source.get("revision"),
        "examination_key": examination_key(payload),
    })


def identity(source_issue: int, payload: dict[str, Any]) -> tuple[str, str]:
    """Return the legacy source-specific marker plus semantic examination digest."""
    source = payload["source_change"]
    digest = examination_key(payload)[:16]
    marker = f"<!-- rahp-dpip-handoff:{source_issue}:{lineage_id(source)}:{source['revision']}:{digest} -->"
    return marker, digest


def proposition_marker(payload: dict[str, Any]) -> str:
    return f"<!-- rahp-dpip-proposition:{proposition_id(payload)} -->"


def examination_marker(payload: dict[str, Any]) -> str:
    return f"<!-- rahp-dpip-examination:{examination_key(payload)} -->"


def referral_marker(source_issue: int, payload: dict[str, Any]) -> str:
    return f"<!-- rahp-dpip-referral:{source_issue}:{referral_id(source_issue, payload)} -->"


def issue_has_label(issue: dict[str, Any], label: str) -> bool:
    return any(item.get("name") == label for item in issue.get("labels", []))


def list_requested(repo: str, token: str) -> list[dict[str, Any]]:
    label = urllib.parse.quote(REQUESTED, safe="")
    return api("GET", repo, f"issues?state=open&labels={label}&per_page=100", token) or []


def issue_comments(repo: str, number: int, token: str) -> list[dict[str, Any]]:
    return api("GET", repo, f"issues/{number}/comments?per_page=100", token) or []


def issue_text(issue: dict[str, Any], comments: list[dict[str, Any]]) -> str:
    return "\n".join([issue.get("body") or "", *[(c.get("body") or "") for c in comments]])


def find_existing(dpip_repo: str, token: str, source_marker: str, exam_marker: str, ref_marker: str) -> tuple[dict[str, Any] | None, str | None]:
    label = urllib.parse.quote(SOURCE_LABEL, safe="")
    issues = api("GET", dpip_repo, f"issues?state=all&labels={label}&per_page=100", token) or []

    # Exact source-referral retry takes precedence and remains backward compatible.
    for issue in issues:
        comments = issue_comments(dpip_repo, issue["number"], token)
        text = issue_text(issue, comments)
        if source_marker in text or ref_marker in text:
            return issue, "source-retry"

    # Cross-source semantic convergence is safe only for the same examination epoch.
    active: dict[str, Any] | None = None
    terminal: dict[str, Any] | None = None
    for issue in issues:
        comments = issue_comments(dpip_repo, issue["number"], token)
        if exam_marker not in issue_text(issue, comments):
            continue
        is_terminal = issue.get("state") == "closed" or issue_has_label(issue, RUN_COMPLETE)
        if is_terminal:
            terminal = terminal or issue
        else:
            active = active or issue
    if active is not None:
        return active, "active-equivalent"
    if terminal is not None:
        return terminal, "terminal-equivalent"
    return None, None


def source_data(rahp_repo: str, rahp_issue: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    source = payload["source_change"]
    data: dict[str, Any] = {
        "system": "RAHP",
        "repository": rahp_repo,
        "issue": rahp_issue["number"],
        "changed_artifact": {
            "repository": source["repository"],
            "revision": source["revision"],
            **({"pull_request": source["pull_request"]} if source.get("pull_request") else {}),
        },
        "source_pins": source_pins(payload),
        "identities": {
            "proposition_id": proposition_id(payload),
            "referral_id": f"rahp-referral:{referral_id(rahp_issue['number'], payload)}",
            "examination_key": examination_key(payload),
        },
    }
    if source.get("gatherer_run_id"):
        data["gatherer"] = {"run_id": source["gatherer_run_id"], **({"event_id": source["gatherer_event_id"]} if source.get("gatherer_event_id") else {})}
    if source.get("monitor_fingerprint"):
        data["portfolio_monitor"] = {"fingerprint": source["monitor_fingerprint"], **({"finding_id": source["monitor_finding_id"]} if source.get("monitor_finding_id") else {})}
    return data


def requested_data(payload: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in {
        "interactions": payload.get("affected_interactions", []),
        "reference_flows": payload.get("affected_reference_flows", []),
        "invariants": payload.get("affected_invariants", []),
        "claims": payload.get("affected_claims", []),
        "suspected_surfaces": payload.get("suspected_surfaces", []),
        "canonical": canonical_contract(payload),
        "provided_evidence": provided_evidence(payload),
        "question": payload.get("question", ""),
    }.items() if value}


def create_intake(rahp_repo: str, dpip_repo: str, rahp_issue: dict[str, Any], payload: dict[str, Any], source_marker: str, dpip_token: str) -> dict[str, Any]:
    source_block = {"source": source_data(rahp_repo, rahp_issue, payload)}
    requested = {"requested_examination": requested_data(payload)}
    body = (
        f"{source_marker}\n{proposition_marker(payload)}\n{examination_marker(payload)}\n{referral_marker(rahp_issue['number'], payload)}\n\n"
        f"## Examination identity\n\n`{proposition_id(payload)}` / `{examination_key(payload)}`\n\n"
        f"## Source\n\nAutomated handoff from `{rahp_repo}#{rahp_issue['number']}`.\n\n"
        f"```yaml\n{yaml.safe_dump(source_block, sort_keys=False).rstrip()}\n```\n\n"
        f"## Requested examination\n\n```yaml\n{yaml.safe_dump(requested, sort_keys=False).rstrip()}\n```\n\n"
        "## Boundary\n\nRAHP transports supplied evidence without deciding whether it is sufficient. DPIP owns applicability, evidence-class acceptance, evidence assessment, scoped conclusion, and return disposition. This issue is one bounded examination epoch; terminal results are historical and new material evidence/revision/scope creates a new epoch.\n"
    )
    title = f"[RAHP intake] {rahp_issue['title'].removeprefix('[DPIP candidate] ').removeprefix('[DPIP requested] ')}"
    return api("POST", dpip_repo, "issues", dpip_token, {"title": title[:256], "body": body, "assignees": ["sankarshanmukhopadhyay"], "labels": [SOURCE_LABEL, "run:requested"]})


def attach_referral(rahp_repo: str, dpip_repo: str, rahp_issue: dict[str, Any], payload: dict[str, Any], dpip_issue: dict[str, Any], dpip_token: str) -> None:
    marker = referral_marker(rahp_issue["number"], payload)
    comments = issue_comments(dpip_repo, dpip_issue["number"], dpip_token)
    if marker in issue_text(dpip_issue, comments):
        return
    record = {"source_referral": source_data(rahp_repo, rahp_issue, payload)}
    body = (
        f"{marker}\n## Additional RAHP referral lineage\n\n"
        f"This referral converges on examination `{examination_key(payload)}`; it does not create a new privacy judgment.\n\n"
        f"```yaml\n{yaml.safe_dump(record, sort_keys=False).rstrip()}\n```"
    )
    api("POST", dpip_repo, f"issues/{dpip_issue['number']}/comments", dpip_token, {"body": body})


def transition_source(rahp_repo: str, issue_number: int, dpip_issue: dict[str, Any], token: str, mode: str) -> None:
    comments = api("GET", rahp_repo, f"issues/{issue_number}/comments?per_page=100", token) or []
    backlink_marker = f"<!-- rahp-dpip-open:{dpip_issue['number']} -->"
    terminal = dpip_issue.get("state") == "closed" or issue_has_label(dpip_issue, RUN_COMPLETE)
    if not any(backlink_marker in (comment.get("body") or "") for comment in comments):
        if terminal:
            message = (
                f"{backlink_marker}\nEquivalent completed DPIP examination: {dpip_issue['html_url']}\n\n"
                "No historical examination is reopened. Return reconciliation will deliver the bounded terminal result to this referral; fresh material evidence/revision/scope requires a new examination epoch."
            )
        else:
            message = (
                f"{backlink_marker}\nDPIP examination opened: {dpip_issue['html_url']}\n\n"
                "The referral passed the RAHP promotion gate. DPIP now owns applicability and the scoped privacy conclusion."
            )
        api("POST", rahp_repo, f"issues/{issue_number}/comments", token, {"body": message})
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
            source_marker, _ = identity(issue["number"], payload)
            exam_marker = examination_marker(payload)
            ref_marker = referral_marker(issue["number"], payload)
            dpip_issue, mode = find_existing(dpip_repo, dpip_token, source_marker, exam_marker, ref_marker)
            if dpip_issue is None:
                dpip_issue = create_intake(rahp_repo, dpip_repo, issue, payload, source_marker, dpip_token)
                mode = "created"
                print(f"CREATED {dpip_repo}#{dpip_issue['number']} from {rahp_repo}#{issue['number']} examination={examination_key(payload)}")
            else:
                attach_referral(rahp_repo, dpip_repo, issue, payload, dpip_issue, dpip_token)
                print(f"REUSED {dpip_repo}#{dpip_issue['number']} for {rahp_repo}#{issue['number']} mode={mode}")
            transition_source(rahp_repo, issue["number"], dpip_issue, rahp_token, mode or "unknown")
        except Exception as exc:
            failures += 1
            print(f"FAIL {rahp_repo}#{issue.get('number')}: {exc}", file=sys.stderr)
    return 1 if failures else 0


def self_test() -> int:
    sha = "cb01d0a758863fb3a02f9f4eef2c4f15f56c4c3b"
    base = {
        "source_change": {"gatherer_run_id": "run-a", "repository": "OpenVTC/verifiable-trust-infrastructure", "revision": sha},
        "question": "Does the composition preserve correlation resistance?",
        "canonical": {
            "interaction_ids": ["C3", "C5"],
            "reference_flow_ids": ["RF-001", "RF-003"],
            "claim_ids": ["C3-PC-5", "C5-PC-2"],
            "evidence_requirement_ids": ["ER-REL-DID-AB"],
            "descriptors": [{"id": "C3", "title": "Human-readable metadata"}],
        },
    }
    assert not validate_payload(base)
    assert source_pins(base)[0]["revision"] == sha

    # Proposition identity survives referral/event and evidence changes.
    same_proposition = json.loads(json.dumps(base))
    same_proposition["source_change"]["gatherer_run_id"] = "run-b"
    assert proposition_id(base) == proposition_id(same_proposition)
    assert examination_key(base) == examination_key(same_proposition)
    assert referral_id(10, base) != referral_id(11, base)

    # Human-readable descriptors do not fork proposition identity.
    descriptor_change = json.loads(json.dumps(base))
    descriptor_change["canonical"]["descriptors"][0]["title"] = "Renamed presentation metadata"
    assert proposition_id(base) == proposition_id(descriptor_change)

    # Material semantic question change creates a new proposition.
    semantic_change = json.loads(json.dumps(base))
    semantic_change["question"] = "Does a different privacy proposition hold?"
    assert proposition_id(base) != proposition_id(semantic_change)

    # New evidence creates a new examination epoch but preserves proposition identity.
    evidence = {
        "requirement_id": "ER-REL-DID-AB",
        "evidence_class": "runtime-upstream-observation",
        "provenance": {
            "producer": "trust-protocol-interop-lab", "run_id": "run-001",
            "observed_at": "2026-09-10T00:00:00Z",
            "implementation_repository": "OpenVTC/verifiable-trust-infrastructure",
            "implementation_revision": sha, "context_a_run": "A", "context_b_run": "B",
        },
        "observation_summary": "Two-context observation.",
        "surfaces": {"identifier": {"context_a": "a", "context_b": "b"}},
    }
    supplied = json.loads(json.dumps(base)); supplied["provided_evidence"] = [evidence]
    assert not validate_payload(supplied)
    assert proposition_id(base) == proposition_id(supplied)
    assert examination_key(base) != examination_key(supplied)

    # Changed immutable source pin/revision creates a new examination epoch.
    revised = json.loads(json.dumps(base))
    revised["source_change"]["revision"] = "a" * 40
    assert proposition_id(base) == proposition_id(revised)
    assert examination_key(base) != examination_key(revised)

    # Legacy source marker remains source-specific and interpretable.
    assert identity(10, base)[0] != identity(11, base)[0]
    assert examination_marker(base) == examination_marker(same_proposition)

    malformed = json.loads(json.dumps(supplied))
    malformed["provided_evidence"][0]["provenance"]["implementation_revision"] = "main"
    assert any("implementation_revision" in item for item in validate_payload(malformed))

    legacy = {"affected_interactions": ["C3"], "source_change": {"monitor_fingerprint": "abc123", "repository": "example/source", "revision": "deadbeef"}, "question": "Does correlation widen?"}
    assert not validate_payload(legacy)
    print("PASS dpip_handoff self-test: proposition/referral/examination identity and epoch separation")
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