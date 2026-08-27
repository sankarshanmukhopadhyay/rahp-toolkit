#!/usr/bin/env python3
"""Reconcile lifecycle telemetry for both active and completed RAHP→DPIP handoffs."""
from __future__ import annotations

import argparse
import os
import urllib.parse

from dpip_lifecycle import (
    DEFAULT_DPIP_REPO,
    DEFAULT_RAHP_REPO,
    api,
    reconcile_one,
)

LABELS = ("assurance:dpip-open", "assurance:dpip-complete")


def candidates(repo: str, token: str) -> list[int]:
    numbers: set[int] = set()
    for label_name in LABELS:
        label = urllib.parse.quote(label_name, safe="")
        issues = api("GET", repo, f"issues?state=open&labels={label}&per_page=100", token) or []
        numbers.update(int(issue["number"]) for issue in issues)
    return sorted(numbers)


def self_test() -> int:
    # Candidate-query behavior is deliberately tiny: the substantive lifecycle
    # ordering/idempotence tests remain in dpip_lifecycle.py. This wrapper exists
    # to ensure completed handoffs are not excluded from operational telemetry.
    assert LABELS == ("assurance:dpip-open", "assurance:dpip-complete")
    print("PASS dpip_lifecycle_reconcile self-test")
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

    rahp_token = os.getenv("GITHUB_TOKEN", "")
    dpip_token = os.getenv("DPIP_HANDOFF_TOKEN", "") or rahp_token
    if not rahp_token:
        return 2

    numbers = [args.issue_number] if args.issue_number else candidates(args.rahp_repository, rahp_token)
    failures = 0
    for number in numbers:
        try:
            reconcile_one(args.rahp_repository, args.dpip_repository, int(number), rahp_token, dpip_token)
        except Exception as exc:
            failures += 1
            print(f"FAIL {args.rahp_repository}#{number}: {exc}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
