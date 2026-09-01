#!/usr/bin/env python3
"""Schedule only RAHP obligations that a registered producer can legitimately advance.

`evidence-external` is deliberately excluded. That state means the substantive evidence
must come from the named target/operator/deployment authority; replaying a convenient
registered harness would collapse provenance boundaries and can create an acquisition
loop after a specialist has already rejected producer-local evidence.
"""
from __future__ import annotations

import argparse
import os
import sys
import tempfile
from pathlib import Path
from typing import Any

from dpip_lifecycle import api
from evidence_producer_controller import DEFAULT_REPO, drive_issue, list_active, load_registry, parse_obligation

EXECUTABLE_STATES = {"model-gap", "evidence-acquirable", "evidence-stale"}


def eligible(issue: dict[str, Any]) -> bool:
    obligation = parse_obligation(issue.get("body") or "")
    return bool(obligation and obligation.get("state") in EXECUTABLE_STATES)


def self_test() -> int:
    def body(state: str) -> str:
        return f"<!-- rahp-assurance-obligation:v1:k -->\n```yaml\nobligation:\n  proposition_key: k\n  state: {state}\n```\n"
    assert eligible({"body": body("evidence-acquirable")})
    assert eligible({"body": body("evidence-stale")})
    assert eligible({"body": body("model-gap")})
    assert not eligible({"body": body("evidence-external")})
    assert not eligible({"body": body("remediation-required")})
    assert not eligible({"body": body("evidence-produced")})
    print("PASS producer scheduler excludes external/remediation/assessment-owned obligations")
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
        obligation = parse_obligation(issue.get("body") or "")
        state = str((obligation or {}).get("state") or "not-obligation")
        if not eligible(issue):
            print(f"{args.repository}#{issue['number']}: {state}")
            continue
        try:
            print(f"{args.repository}#{issue['number']}: {drive_issue(args.repository, issue, token, registry, outbox_root, cache_root)}")
        except Exception as exc:
            failures += 1; print(f"FAIL {args.repository}#{issue.get('number')}: {exc}", file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
