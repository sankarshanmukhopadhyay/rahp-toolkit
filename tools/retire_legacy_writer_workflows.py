#!/usr/bin/env python3
"""Disable only approved legacy RAHP workflow registrations after replacement.

Requires a main-branch push from the repository owner and Actions:write.
No Registry case authority, GitHub Issues permission or cutover acceptance
is conferred by retiring these exact workflow IDs.
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import subprocess

REPOSITORY = "sankarshanmukhopadhyay/rahp-toolkit"
REPLACEMENTS = frozenset({
    ".github/workflows/dtg-materiality-main.yml",
    ".github/workflows/instance-monitor-main.yml",
})
LEGACY = (
    (343470013, ".github/workflows/dtg-portfolio-materiality-handoff.yml"),
    (334033746, ".github/workflows/instance-watch.yml"),
)
TERMINAL = frozenset({"disabled_manually", "deleted"})


class RetirementError(ValueError):
    pass


def require_operator_context(env: dict[str, str]) -> str:
    if (env.get("GITHUB_ACTIONS") != "true"
            or env.get("GITHUB_REPOSITORY") != REPOSITORY
            or env.get("GITHUB_REF") != "refs/heads/main"
            or env.get("GITHUB_EVENT_NAME") != "push"
            or env.get("GITHUB_ACTOR") != "sankarshanmukhopadhyay"
            or not re.fullmatch("[0-9a-f]{40}", env.get("GITHUB_SHA", ""))):
        raise RetirementError("workflow retirement requires owner-initiated Toolkit main push")
    return env["GITHUB_SHA"]


def retire(registrations, get, put, commit: str) -> dict:
    if (not isinstance(registrations, dict)
            or not isinstance(registrations.get("workflows"), list)):
        raise RetirementError("workflow registration inventory unavailable")
    seen = {}
    for row in registrations["workflows"]:
        if not isinstance(row, dict) or not isinstance(row.get("path"), str):
            raise RetirementError("malformed workflow inventory")
        seen.setdefault(row["path"], []).append(row)
    for path in REPLACEMENTS:
        matches = seen.get(path, [])
        if (len(matches) != 1 or matches[0].get("state") != "active"
                or type(matches[0].get("id")) is not int):
            raise RetirementError("replacement workflow not uniquely active: " + path)
    # Evaluate every candidate before mutating *any* registration.
    planned = []
    for workflow_id, path in LEGACY:
        item = get(workflow_id)
        if (not isinstance(item, dict) or item.get("id") != workflow_id
                or item.get("path") != path
                or item.get("state") not in ({"active"} | TERMINAL)):
            raise RetirementError("unverified legacy workflow registration " + path)
        planned.append((workflow_id, path, item["state"]))
    rows = []
    for workflow_id, path, initial in planned:
        if initial == "active":
            put(workflow_id)
        current = get(workflow_id)
        if (not isinstance(current, dict) or current.get("id") != workflow_id
                or current.get("path") != path
                or current.get("state") not in TERMINAL):
            raise RetirementError("legacy workflow not verifiably retired " + path)
        rows.append({"id": workflow_id, "path": path,
                     "state_before": initial, "state_after": current["state"]})
    return {
        "schema": "rahp-legacy-workflow-registration-retirement/v1",
        "toolkit_commit": commit,
        "replacements_active": sorted(REPLACEMENTS),
        "legacy_registrations": rows,
        "historical_ref_dispatch_denial_tested": False,
        "global_issues_api_exclusivity_verified": False,
        "registry_cutover_authorized": False,
    }


def gh_api(*args: str):
    process = subprocess.run(["gh", "api", *args],
                             capture_output=True, text=True, check=True)
    return json.loads(process.stdout) if process.stdout.strip() else None


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", type=pathlib.Path, required=True)
    args = p.parse_args()
    commit = require_operator_context(os.environ)
    repository = REPOSITORY
    receipt = retire(
        gh_api(f"repos/{repository}/actions/workflows?per_page=100"),
        lambda workflow_id: gh_api(f"repos/{repository}/actions/workflows/{workflow_id}"),
        lambda workflow_id: gh_api("--method", "PUT",
                                  f"repos/{repository}/actions/workflows/{workflow_id}/disable"),
        commit)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print("PASS exact legacy workflow registrations retired;")
    print("historical ref denial and universal external writer exclusivity remain unverified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
