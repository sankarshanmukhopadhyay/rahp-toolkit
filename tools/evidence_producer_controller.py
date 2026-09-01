#!/usr/bin/env python3
"""Drive registered assurance evidence producers for active RAHP obligations.

RAHP owns orchestration. Producers own observation. Specialists own interpretation.
The controller dispatches a configured producer, watches its durable GitHub Actions
artifact outbox, validates attribution/contract shape, and enqueues a comparable
specialist reassessment without converting observations into assurance judgments.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import sys
import urllib.request
import zipfile
from pathlib import Path
from typing import Any

import yaml

from assurance_obligation import transition_obligation
from dpip_lifecycle import api

DEFAULT_REPO = "sankarshanmukhopadhyay/rahp-toolkit"
REGISTRY_PATH = Path("config/evidence-producers.yaml")
OBLIGATION_RE = re.compile(r"```ya?ml\s*\n(?P<yaml>obligation:\s*.*?\n)```", re.DOTALL | re.IGNORECASE)
MARKER_RE = re.compile(r"<!--\s*rahp-assurance-obligation:v1:([^\s]+)\s*-->")
SHA40 = re.compile(r"^[0-9a-f]{40}$", re.I)
REQUESTED = "assurance:dpip-requested"


def load_registry(path: Path = REGISTRY_PATH) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or value.get("schema") != "rahp-evidence-producer-registry/v1":
        raise ValueError("invalid evidence producer registry")
    for producer in value.get("producers", []) or []:
        if producer.get("mode") == "registered-executable" and not producer.get("provenance_producer"):
            raise ValueError(f"registered producer {producer.get('id')} lacks provenance_producer")
    return value


def parse_obligation(body: str) -> dict[str, Any] | None:
    marker = MARKER_RE.search(body or "")
    if not marker:
        return None
    for match in OBLIGATION_RE.finditer(body or ""):
        value = yaml.safe_load(match.group("yaml"))
        obligation = value.get("obligation") if isinstance(value, dict) else None
        if isinstance(obligation, dict) and obligation.get("proposition_key") == marker.group(1):
            return obligation
    return None


def replace_obligation(body: str, obligation: dict[str, Any]) -> str:
    rendered = "```yaml\n" + yaml.safe_dump({"obligation": obligation}, sort_keys=False).rstrip() + "\n```"
    match = OBLIGATION_RE.search(body or "")
    if not match:
        raise ValueError("semantic obligation marker has no obligation YAML block")
    return body[:match.start()] + rendered + body[match.end():]


def resolve_producer(requirement_ids: list[str], registry: dict[str, Any]) -> tuple[dict[str, Any], str] | None:
    wanted = set(str(x) for x in requirement_ids if str(x))
    if not wanted:
        return None
    for producer in registry.get("producers", []) or []:
        if producer.get("mode") != "registered-executable" or not wanted.issubset(set(producer.get("requirements", []) or [])):
            continue
        for group_name, group in (producer.get("executable_groups") or {}).items():
            if wanted.issubset(set(group.get("requirements", []) or [])):
                resolved = dict(producer)
                resolved["workflow"] = group.get("workflow") or producer.get("workflow")
                return resolved, str(group_name)
    return None


def dispatch_key(obligation: dict[str, Any], producer_id: str) -> str:
    payload = {
        "proposition_key": obligation["proposition_key"],
        "evidence_contract_key": obligation.get("evidence_contract_key"),
        "producer": producer_id,
        "source_pins": sorted(obligation.get("source_pins", []), key=lambda x: (str(x.get("repository")), str(x.get("revision")))),
    }
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()[:24]
    return f"evidence-{digest}"


def validate_evidence_bundle(bundle: dict[str, Any], required_ids: list[str], producer: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if bundle.get("schema") != "interop-evidence-bundle/v1":
        errors.append("unsupported evidence bundle schema")
    records = bundle.get("provided_evidence")
    if not isinstance(records, list):
        return errors + ["provided_evidence must be a list"]
    by_id = {str(r.get("requirement_id")): r for r in records if isinstance(r, dict) and r.get("requirement_id")}
    expected_provenance = str(producer.get("provenance_producer") or "")
    for rid in required_ids:
        record = by_id.get(rid)
        if not record:
            errors.append(f"missing evidence for {rid}")
            continue
        if record.get("schema") != producer.get("output_schema"):
            errors.append(f"{rid}: unexpected evidence schema")
        if record.get("evidence_class") != producer.get("evidence_class"):
            errors.append(f"{rid}: evidence class mismatch")
        observer = record.get("observer")
        contexts = observer.get("contexts") if isinstance(observer, dict) else None
        if not isinstance(contexts, list) or len(contexts) < 2:
            errors.append(f"{rid}: observer A/B context missing")
        pins = record.get("source_pins")
        if not isinstance(pins, list) or not pins:
            errors.append(f"{rid}: source pins missing")
        else:
            for pin in pins:
                if not isinstance(pin, dict) or not str(pin.get("repository") or "") or not SHA40.fullmatch(str(pin.get("revision") or "")):
                    errors.append(f"{rid}: invalid immutable source pin")
        provenance = record.get("provenance")
        if not isinstance(provenance, dict) or provenance.get("producer") != expected_provenance:
            errors.append(f"{rid}: producer provenance mismatch")
        if not isinstance(record.get("surfaces"), dict) or not record.get("surfaces"):
            errors.append(f"{rid}: surfaces missing")
    return errors


def workflow_dispatch(producer: dict[str, Any], key: str, requirement_ids: list[str], token: str) -> None:
    api("POST", producer["repository"], f"actions/workflows/{producer['workflow']}/dispatches", token, {
        "ref": producer.get("ref") or "main",
        "inputs": {"correlation_key": key, "evidence_requirement_ids": json.dumps(requirement_ids, separators=(",", ":"))},
    })


def artifact_name(producer: dict[str, Any], key: str) -> str:
    return str(producer.get("artifact_prefix") or "assurance-evidence-") + key


def find_artifact(producer: dict[str, Any], key: str, token: str) -> dict[str, Any] | None:
    name = artifact_name(producer, key)
    result = api("GET", producer["repository"], f"actions/artifacts?name={name}&per_page=20", token) or {}
    artifacts = [a for a in result.get("artifacts", []) if not a.get("expired") and a.get("name") == name]
    return max(artifacts, key=lambda a: int(a.get("id", 0))) if artifacts else None


def download_artifact(repo: str, artifact_id: int, token: str) -> dict[str, Any]:
    req = urllib.request.Request(
        f"https://api.github.com/repos/{repo}/actions/artifacts/{artifact_id}/zip",
        headers={"Accept": "application/vnd.github+json", "Authorization": f"Bearer {token}", "User-Agent": "rahp-evidence-controller/1.0", "X-GitHub-Api-Version": "2022-11-28"},
    )
    with urllib.request.urlopen(req, timeout=60) as response:
        raw = response.read()
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        names = set(archive.namelist())
        target = next((n for n in names if n.endswith("unlinkability-pressure-provided-evidence.json")), None)
        if not target:
            raise ValueError("producer artifact lacks unlinkability pressure evidence bundle")
        return json.loads(archive.read(target).decode("utf-8"))


def append_reassessment(body: str, obligation: dict[str, Any], bundle: dict[str, Any], key: str) -> str:
    records = [r for r in bundle.get("provided_evidence", []) if r.get("requirement_id") in set(obligation.get("evidence_requirement_ids", []))]
    first_pin = next((p for r in records for p in r.get("source_pins", []) if isinstance(p, dict)), None)
    source_repo = str((first_pin or {}).get("repository") or "evidence-producer")
    source_revision = str((first_pin or {}).get("revision") or "")
    block = {
        "dpip": {
            "source_change": {"gatherer_run_id": key, "repository": source_repo, "revision": source_revision},
            "source_pins": list({(p["repository"], p["revision"]): p for r in records for p in r.get("source_pins", []) if isinstance(p, dict) and p.get("repository") and p.get("revision")}.values()),
            "canonical": {"evidence_requirement_ids": obligation.get("evidence_requirement_ids", [])},
            "provided_evidence": records,
            "question": f"Reassess assurance proposition {obligation['proposition_key']} using the attributable observer-bound evidence produced for this evidence contract.",
        }
    }
    marker = f"<!-- rahp-obligation-reassessment:{key} -->"
    rendered = marker + "\n```yaml\n" + yaml.safe_dump(block, sort_keys=False).rstrip() + "\n```\n"
    pattern = re.compile(r"<!--\s*rahp-obligation-reassessment:" + re.escape(key) + r"\s*-->\s*```ya?ml.*?```\s*", re.DOTALL | re.IGNORECASE)
    return pattern.sub(rendered, body) if pattern.search(body) else body.rstrip() + "\n\n" + rendered


def update_issue(repo: str, issue: dict[str, Any], obligation: dict[str, Any], body: str, token: str) -> None:
    api("PATCH", repo, f"issues/{issue['number']}", token, {"body": replace_obligation(body, obligation)})


def drive_issue(repo: str, issue: dict[str, Any], token: str, producer_token: str, registry: dict[str, Any]) -> str:
    body = issue.get("body") or ""
    obligation = parse_obligation(body)
    if not obligation:
        return "not-obligation"
    if obligation.get("state") not in {"model-gap", "evidence-external", "evidence-acquirable", "evidence-stale"}:
        return str(obligation.get("state") or "unknown")
    resolved = resolve_producer(obligation.get("evidence_requirement_ids", []), registry)
    if not resolved:
        return str(obligation.get("state") or "model-gap")
    producer, _group = resolved
    key = dispatch_key(obligation, producer["id"])
    artifact = find_artifact(producer, key, producer_token)
    comments = api("GET", repo, f"issues/{issue['number']}/comments?per_page=100", token) or []
    dispatch_marker = f"<!-- rahp-evidence-dispatch:{key} -->"
    if artifact is None:
        if not any(dispatch_marker in (c.get("body") or "") for c in comments):
            workflow_dispatch(producer, key, obligation.get("evidence_requirement_ids", []), producer_token)
            api("POST", repo, f"issues/{issue['number']}/comments", token, {"body": f"{dispatch_marker}\nRegistered evidence producer `{producer['id']}` dispatched. RAHP will poll durable artifact `{artifact_name(producer, key)}`; replay uses the same dispatch key."})
        next_obligation = transition_obligation(obligation, state="evidence-acquirable", producer={"mode": "registered-executable", "id": producer["id"], "repository": producer["repository"]})
        update_issue(repo, issue, next_obligation, body, token)
        return "evidence-acquirable"

    bundle = download_artifact(producer["repository"], int(artifact["id"]), producer_token)
    problems = validate_evidence_bundle(bundle, obligation.get("evidence_requirement_ids", []), producer)
    if problems:
        raise ValueError("; ".join(problems))
    evidence_pins = list({(p["repository"], p["revision"]): p for r in bundle["provided_evidence"] for p in r.get("source_pins", [])}.values())
    next_obligation = transition_obligation(obligation, state="evidence-produced", source_pins=evidence_pins, producer={"mode": "registered-executable", "id": producer["id"], "repository": producer["repository"]}, lineage={"kind": "evidence-production", "dispatch_key": key, "artifact_id": int(artifact["id"])})
    new_body = append_reassessment(replace_obligation(body, next_obligation), next_obligation, bundle, key)
    api("PATCH", repo, f"issues/{issue['number']}", token, {"body": new_body})
    api("POST", repo, f"issues/{issue['number']}/labels", token, {"labels": [REQUESTED]})
    return "evidence-produced"


def list_active(repo: str, token: str) -> list[dict[str, Any]]:
    issues = api("GET", repo, "issues?state=open&labels=assurance&per_page=100", token) or []
    return [i for i in issues if MARKER_RE.search(i.get("body") or "")]


def self_test() -> int:
    registry = load_registry()
    obligation = {
        "schema": "rahp-assurance-obligation/v1", "proposition_key": "rahp-obligation:abc",
        "evidence_contract_key": "rahp-evidence-contract:def", "state": "model-gap",
        "action_owner": {"surface": "specialist-profile"}, "artifact_to_produce": {"kind": "evidence-requirement", "description": "define"},
        "producer": {"mode": "not-yet-defined"}, "source_pins": [], "evidence_requirement_ids": ["ER-CREDENTIAL-ID-AB"], "lineage": [], "supersedes": [],
    }
    resolved = resolve_producer(obligation["evidence_requirement_ids"], registry)
    assert resolved and resolved[0]["id"] == "composed-unlinkability-v1" and resolved[1] == "relationship-and-credential"
    key = dispatch_key(obligation, resolved[0]["id"])
    assert key == dispatch_key(obligation, resolved[0]["id"])
    assert resolve_producer(["ER-UNKNOWN"], registry) is None
    record = {"schema": "interop-evidence-package/v1", "requirement_id": "ER-CREDENTIAL-ID-AB", "evidence_class": "runtime-upstream-observation", "experiment": {"kind": "unlinkability-pressure-case", "expected_join": "must-not-emerge", "observed_join": "not-detected"}, "observer": {"model": "distinct", "contexts": [{"id": "A"}, {"id": "B"}]}, "provenance": {"producer": resolved[0]["provenance_producer"]}, "source_pins": [{"repository": "example/runtime", "revision": "a" * 40}], "surfaces": {"credential_identifier": {"classification": "fresh"}}}
    bundle = {"schema": "interop-evidence-bundle/v1", "provided_evidence": [record]}
    assert validate_evidence_bundle(bundle, ["ER-CREDENTIAL-ID-AB"], resolved[0]) == []
    bad = json.loads(json.dumps(bundle)); bad["provided_evidence"][0]["provenance"]["producer"] = "different-producer"
    assert any("provenance" in x for x in validate_evidence_bundle(bad, ["ER-CREDENTIAL-ID-AB"], resolved[0]))
    bad_observer = json.loads(json.dumps(bundle)); bad_observer["provided_evidence"][0]["observer"]["contexts"] = [{"id": "A"}]
    assert any("observer" in x for x in validate_evidence_bundle(bad_observer, ["ER-CREDENTIAL-ID-AB"], resolved[0]))
    body = "<!-- rahp-assurance-obligation:v1:rahp-obligation:abc -->\n```yaml\n" + yaml.safe_dump({"obligation": obligation}, sort_keys=False) + "```\n"
    assert parse_obligation(body)["proposition_key"] == obligation["proposition_key"]
    produced = transition_obligation(obligation, state="evidence-produced", evidence_requirement_ids=["ER-CREDENTIAL-ID-AB"])
    assert produced["proposition_key"] == obligation["proposition_key"]
    print("PASS target-agnostic producer resolution, idempotent dispatch identity, configured provenance validation and stable obligation transition")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--self-test", action="store_true"); parser.add_argument("--issue-number", type=int); parser.add_argument("--repository", default=os.getenv("RAHP_REPOSITORY", DEFAULT_REPO)); args = parser.parse_args()
    if args.self_test:
        return self_test()
    token = os.getenv("GITHUB_TOKEN", "")
    producer_token = os.getenv("EVIDENCE_PRODUCER_TOKEN", "") or os.getenv("DPIP_HANDOFF_TOKEN", "")
    if not token or not producer_token:
        print("GITHUB_TOKEN and EVIDENCE_PRODUCER_TOKEN/DPIP_HANDOFF_TOKEN are required", file=sys.stderr); return 2
    registry = load_registry()
    issues = [api("GET", args.repository, f"issues/{args.issue_number}", token)] if args.issue_number else list_active(args.repository, token)
    failures = 0
    for issue in issues:
        try:
            print(f"{args.repository}#{issue['number']}: {drive_issue(args.repository, issue, token, producer_token, registry)}")
        except Exception as exc:
            failures += 1; print(f"FAIL {args.repository}#{issue.get('number')}: {exc}", file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
