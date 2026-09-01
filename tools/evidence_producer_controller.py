#!/usr/bin/env python3
"""Drive registered assurance evidence producers for active RAHP obligations.

RAHP owns orchestration. Producers own observation. Specialists own interpretation.
For public registered producers RAHP checks out the configured immutable producer
revision locally, executes its declared entrypoint, validates the resulting evidence,
persists a durable workflow outbox copy, and enqueues a comparable specialist
reassessment. No cross-repository Actions write credential is required.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
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
        if producer.get("mode") != "registered-executable":
            continue
        for required in ("id", "repository", "revision", "provenance_producer", "execution_mode", "output_schema", "evidence_class"):
            if not producer.get(required):
                raise ValueError(f"registered producer {producer.get('id')} lacks {required}")
        if producer.get("execution_mode") != "local-public-checkout":
            raise ValueError(f"registered producer {producer.get('id')} has unsupported execution_mode")
        if not SHA40.fullmatch(str(producer.get("revision"))):
            raise ValueError(f"registered producer {producer.get('id')} revision must be immutable 40-hex")
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
            if wanted.issubset(set(group.get("requirements", []) or [])) and group.get("entrypoint") and group.get("output_bundle"):
                resolved = dict(producer)
                resolved["execution_group"] = dict(group)
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


def _checkout_producer(producer: dict[str, Any], cache_root: Path) -> Path:
    cache_root.mkdir(parents=True, exist_ok=True)
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "-", producer["repository"])
    target = cache_root / f"{safe}-{producer['revision']}"
    if target.exists():
        return target
    tmp = Path(tempfile.mkdtemp(prefix="rahp-producer-", dir=cache_root))
    try:
        subprocess.run(["git", "init", "-q", str(tmp)], check=True)
        subprocess.run(["git", "-C", str(tmp), "remote", "add", "origin", f"https://github.com/{producer['repository']}.git"], check=True)
        subprocess.run(["git", "-C", str(tmp), "fetch", "-q", "--depth", "1", "origin", producer["revision"]], check=True)
        subprocess.run(["git", "-C", str(tmp), "checkout", "-q", "--detach", "FETCH_HEAD"], check=True)
        actual = subprocess.check_output(["git", "-C", str(tmp), "rev-parse", "HEAD"], text=True).strip()
        if actual.lower() != str(producer["revision"]).lower():
            raise ValueError("producer checkout revision mismatch")
        tmp.rename(target)
        return target
    except Exception:
        shutil.rmtree(tmp, ignore_errors=True)
        raise


def execute_producer(producer: dict[str, Any], key: str, outbox_root: Path, cache_root: Path) -> dict[str, Any]:
    checkout = _checkout_producer(producer, cache_root)
    group = producer["execution_group"]
    entrypoint = checkout / str(group["entrypoint"])
    if not entrypoint.is_file():
        raise ValueError(f"registered producer entrypoint missing: {group['entrypoint']}")
    run_dir = outbox_root / key
    run_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run([
        sys.executable, str(entrypoint),
        "--revision", str(producer["revision"]),
        "--output-dir", str(run_dir),
    ], cwd=checkout, check=True)
    bundle_path = run_dir / str(group["output_bundle"])
    if not bundle_path.is_file():
        raise ValueError(f"registered producer did not emit {group['output_bundle']}")
    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
    (run_dir / "rahp-dispatch.json").write_text(json.dumps({
        "schema": "rahp-evidence-dispatch/v1",
        "dispatch_key": key,
        "producer": producer["id"],
        "producer_repository": producer["repository"],
        "producer_revision": producer["revision"],
    }, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return bundle


def append_reassessment(body: str, obligation: dict[str, Any], bundle: dict[str, Any], key: str) -> str:
    wanted = set(obligation.get("evidence_requirement_ids", []))
    records = [r for r in bundle.get("provided_evidence", []) if r.get("requirement_id") in wanted]
    evidence_pins = [p for r in records for p in r.get("source_pins", []) if isinstance(p, dict) and p.get("repository") and p.get("revision")]
    all_pins = list({(p["repository"], p["revision"]): p for p in [*(obligation.get("source_pins", []) or []), *evidence_pins]}.values())
    source_pin = next(iter(obligation.get("source_pins", []) or []), None) or next(iter(evidence_pins), None) or {}
    block = {
        "dpip": {
            "source_change": {"gatherer_run_id": key, "repository": source_pin.get("repository", "evidence-producer"), "revision": source_pin.get("revision", "")},
            "source_pins": all_pins,
            "canonical": {"evidence_requirement_ids": obligation.get("evidence_requirement_ids", [])},
            "provided_evidence": records,
            "question": f"Reassess assurance proposition {obligation['proposition_key']} using the attributable observer-bound evidence produced for this evidence contract. Preserve the distinction between producer/composition evidence and evidence attributable to the original target implementation.",
        }
    }
    marker = f"<!-- rahp-obligation-reassessment:{key} -->"
    rendered = marker + "\n```yaml\n" + yaml.safe_dump(block, sort_keys=False).rstrip() + "\n```\n"
    pattern = re.compile(r"<!--\s*rahp-obligation-reassessment:" + re.escape(key) + r"\s*-->\s*```ya?ml.*?```\s*", re.DOTALL | re.IGNORECASE)
    return pattern.sub(rendered, body) if pattern.search(body) else body.rstrip() + "\n\n" + rendered


def drive_issue(repo: str, issue: dict[str, Any], token: str, registry: dict[str, Any], outbox_root: Path, cache_root: Path) -> str:
    body = issue.get("body") or ""
    obligation = parse_obligation(body)
    if not obligation:
        return "not-obligation"
    if obligation.get("state") not in {"model-gap", "evidence-external", "evidence-acquirable", "evidence-stale"}:
        return str(obligation.get("state") or "unknown")
    resolved = resolve_producer(obligation.get("evidence_requirement_ids", []), registry)
    if not resolved:
        return str(obligation.get("state") or "model-gap")
    producer, group_name = resolved
    key = dispatch_key(obligation, producer["id"])
    reassessment_marker = f"<!-- rahp-obligation-reassessment:{key} -->"
    if reassessment_marker in body:
        return "evidence-produced"

    bundle = execute_producer(producer, key, outbox_root, cache_root)
    problems = validate_evidence_bundle(bundle, obligation.get("evidence_requirement_ids", []), producer)
    if problems:
        raise ValueError("; ".join(problems))
    evidence_pins = list({(p["repository"], p["revision"]): p for r in bundle["provided_evidence"] for p in r.get("source_pins", []) if isinstance(p, dict) and p.get("repository") and p.get("revision")}.values())
    combined_pins = list({(p["repository"], p["revision"]): p for p in [*(obligation.get("source_pins", []) or []), *evidence_pins]}.values())
    next_obligation = transition_obligation(
        obligation,
        state="evidence-produced",
        source_pins=combined_pins,
        producer={"mode": "registered-executable", "id": producer["id"], "repository": producer["repository"], "revision": producer["revision"]},
        lineage={"kind": "evidence-production", "dispatch_key": key, "execution_group": group_name, "producer_revision": producer["revision"]},
    )
    new_body = append_reassessment(replace_obligation(body, next_obligation), next_obligation, bundle, key)
    api("PATCH", repo, f"issues/{issue['number']}", token, {"body": new_body})
    api("POST", repo, f"issues/{issue['number']}/labels", token, {"labels": [REQUESTED]})
    api("POST", repo, f"issues/{issue['number']}/comments", token, {"body": f"<!-- rahp-evidence-dispatch:{key} -->\nRegistered producer `{producer['id']}` executed locally by RAHP at immutable revision `{producer['revision']}`. Evidence outbox key: `{key}`. The same semantic obligation has advanced to `evidence-produced` and is queued for comparable DPIP reassessment."})
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
        "producer": {"mode": "not-yet-defined"}, "source_pins": [{"repository": "target/runtime", "revision": "b" * 40}], "evidence_requirement_ids": ["ER-CREDENTIAL-ID-AB"], "lineage": [], "supersedes": [],
    }
    resolved = resolve_producer(obligation["evidence_requirement_ids"], registry)
    assert resolved and resolved[0]["id"] == "composed-unlinkability-v1" and resolved[1] == "relationship-and-credential"
    key = dispatch_key(obligation, resolved[0]["id"])
    assert key == dispatch_key(obligation, resolved[0]["id"])
    changed = json.loads(json.dumps(obligation)); changed["source_pins"][0]["revision"] = "c" * 40
    assert dispatch_key(changed, resolved[0]["id"]) != key
    assert changed["proposition_key"] == obligation["proposition_key"]
    assert resolve_producer(["ER-DEVICE-METADATA-AB"], registry) is None
    record = {"schema": "interop-evidence-package/v1", "requirement_id": "ER-CREDENTIAL-ID-AB", "evidence_class": "runtime-upstream-observation", "experiment": {"kind": "unlinkability-pressure-case", "expected_join": "must-not-emerge", "observed_join": "not-detected"}, "observer": {"model": "distinct", "contexts": [{"id": "A"}, {"id": "B"}]}, "provenance": {"producer": resolved[0]["provenance_producer"]}, "source_pins": [{"repository": resolved[0]["repository"], "revision": resolved[0]["revision"]}], "surfaces": {"credential_identifier": {"classification": "fresh"}}}
    bundle = {"schema": "interop-evidence-bundle/v1", "provided_evidence": [record]}
    assert validate_evidence_bundle(bundle, ["ER-CREDENTIAL-ID-AB"], resolved[0]) == []
    bad = json.loads(json.dumps(bundle)); bad["provided_evidence"][0]["provenance"]["producer"] = "different-producer"
    assert any("provenance" in x for x in validate_evidence_bundle(bad, ["ER-CREDENTIAL-ID-AB"], resolved[0]))
    produced = transition_obligation(obligation, state="evidence-produced", evidence_requirement_ids=["ER-CREDENTIAL-ID-AB"])
    assert produced["proposition_key"] == obligation["proposition_key"]
    print("PASS local registered-producer resolution, source-pin dispatch freshness, configured provenance validation and stable obligation transition")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--self-test", action="store_true"); parser.add_argument("--issue-number", type=int); parser.add_argument("--repository", default=os.getenv("RAHP_REPOSITORY", DEFAULT_REPO)); args = parser.parse_args()
    if args.self_test:
        return self_test()
    token = os.getenv("GITHUB_TOKEN", "")
    if not token:
        print("GITHUB_TOKEN is required", file=sys.stderr); return 2
    registry = load_registry()
    outbox_root = Path(os.getenv("RAHP_EVIDENCE_OUTBOX", ".rahp/evidence-outbox"))
    cache_root = Path(os.getenv("RAHP_PRODUCER_CACHE", tempfile.gettempdir())) / "rahp-producer-cache"
    issues = [api("GET", args.repository, f"issues/{args.issue_number}", token)] if args.issue_number else list_active(args.repository, token)
    failures = 0
    for issue in issues:
        try:
            print(f"{args.repository}#{issue['number']}: {drive_issue(args.repository, issue, token, registry, outbox_root, cache_root)}")
        except Exception as exc:
            failures += 1; print(f"FAIL {args.repository}#{issue.get('number')}: {exc}", file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
