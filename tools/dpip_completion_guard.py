#!/usr/bin/env python3
"""Prevent specialist DPIP completion telemetry from masking live RAHP obligations."""
from __future__ import annotations

import argparse
import os
import urllib.error
import urllib.parse

from dpip_lifecycle import DEFAULT_RAHP_REPO, api
from evidence_producer_controller import parse_obligation

COMPLETE = "assurance:dpip-complete"
SEMANTIC_MARKER = "<!-- rahp-assurance-obligation:v1:"


def is_live_semantic_obligation(issue: dict) -> bool:
    body = str(issue.get("body") or "")
    if SEMANTIC_MARKER not in body:
        return False
    obligation = parse_obligation(body)
    if not obligation:
        return False
    return str(obligation.get("state") or "").strip() != "resolved"


def candidates(repo: str, token: str) -> list[dict]:
    label = urllib.parse.quote(COMPLETE, safe="")
    return api("GET", repo, f"issues?state=open&labels={label}&per_page=100", token) or []


def remove_completion_label(repo: str, number: int, token: str) -> None:
    try:
        api("DELETE", repo, f"issues/{number}/labels/{urllib.parse.quote(COMPLETE, safe='')}", token)
    except urllib.error.HTTPError as exc:
        if exc.code != 404:
            raise


def reconcile(repo: str, token: str) -> int:
    changed = 0
    for issue in candidates(repo, token):
        if not is_live_semantic_obligation(issue):
            continue
        remove_completion_label(repo, int(issue["number"]), token)
        changed += 1
        print(f"REMOVED {COMPLETE} from live semantic obligation {repo}#{issue['number']}")
    return changed


def self_test() -> int:
    live = {
        "body": """<!-- rahp-assurance-obligation:v1:rahp-obligation:test -->
```yaml
obligation:
  schema: rahp-assurance-obligation/v1
  proposition_key: rahp-obligation:test
  evidence_contract_key: rahp-evidence-contract:test
  state: evidence-external
  action_owner:
    surface: external
    repository: example/target
  artifact_to_produce:
    kind: runtime-evidence
    description: Supply attributable target evidence.
  producer:
    mode: external
  source_pins: []
  evidence_requirement_ids: []
  lineage: []
  supersedes: []
```
"""
    }
    resolved = {
        "body": live["body"].replace("state: evidence-external", "state: resolved")
    }
    historical_referral = {"body": "DPIP specialist leg completed; no semantic obligation owner here."}

    assert is_live_semantic_obligation(live)
    assert not is_live_semantic_obligation(resolved)
    assert not is_live_semantic_obligation(historical_referral)
    print("PASS DPIP completion guard: completion telemetry cannot mask live semantic obligations")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--rahp-repository", default=os.getenv("RAHP_REPOSITORY", DEFAULT_RAHP_REPO))
    args = parser.parse_args()
    if args.self_test:
        return self_test()

    token = os.getenv("GITHUB_TOKEN", "")
    if not token:
        print("GITHUB_TOKEN is required")
        return 2
    reconcile(args.rahp_repository, token)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
