#!/usr/bin/env python3
"""Validate accepted-main assurance publication after protected state PR review."""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"
MONITOR = WORKFLOWS / "instance-monitor-main.yml"
RECONCILE = WORKFLOWS / "dtg-assurance-reconcile.yml"


def fail(message: str) -> None:
    print("ERROR: " + message)
    raise SystemExit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def main() -> int:
    monitor = MONITOR.read_text(encoding="utf-8")
    reconciler = RECONCILE.read_text(encoding="utf-8")
    config = yaml.load(monitor, Loader=yaml.BaseLoader)
    jobs = config.get("jobs", {})
    require(set(jobs) == {"monitor", "publish_external", "persist", "local_incidents"},
            "instance monitor jobs are not the accepted four-step chain")
    require(jobs["persist"].get("needs") == "publish_external",
            "state review may precede external issue publication")
    require(jobs["local_incidents"].get("needs") == "persist"
            and "needs.persist.outputs.disposition == 'unchanged'" in jobs["local_incidents"].get("if", ""),
            "unmerged changed state may trigger local controller incidents")
    required_monitor = (
        "git ls-remote origin refs/heads/main",
        "git commit -s",
        'git push -u origin "$branch"',
        "gh pr create --base main",
        "disposition=staged_pending_review",
        "Unmerged monitored-state PR exists",
        "Pending protected-main instance state PR blocks re-publication",
        "if: steps.persist.outputs.disposition == 'unchanged'",
    )
    for marker in required_monitor:
        require(marker in monitor, "missing protected-main marker: " + marker)
    require("git push\n" not in monitor and "git push origin main" not in monitor,
            "instance monitor still has direct protected-main push")
    require("pull-requests: write" in monitor,
            "persist cannot stage reviewable state PR")
    for name in ("validate.yml", "pages.yml"):
        target = (WORKFLOWS / name).read_text(encoding="utf-8")
        require("push:" in target and "branches: [main]" in target,
                "accepted-main post-merge validation/publication missing: " + name)
    require("push:" in reconciler and "branches: [main]" in reconciler
            and "'instances/dtg/state/**'" in reconciler
            and "'instances/cawg/state/**'" in reconciler,
            "canonical reconciliation does not observe accepted main state")
    require("needs: reconcile" in reconciler
            and "publish_dtg_controller_incidents.py" in reconciler
            and "issues: write" in reconciler,
            "accepted-state local incidents lack bounded reconciliation dependency")
    print("PASS instance-watch protected-main state acceptance and assurance dispatch contract")
    print("  source observation and publication are separate")
    print("  changed state requires signed PR and accepted main before reconciliation")
    print("  validate/pages and canonical DTG assurance run on accepted main")
    return 0


if __name__ == "__main__":
    sys.exit(main())
