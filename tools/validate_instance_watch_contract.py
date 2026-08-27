#!/usr/bin/env python3
"""Validate the monitored-instance → current-head assurance dispatch contract."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WATCH = ROOT / ".github" / "workflows" / "instance-watch.yml"
WORKFLOWS = ROOT / ".github" / "workflows"


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


def main() -> int:
    text = WATCH.read_text(encoding="utf-8")

    required_markers = (
        "actions: write",
        "EXPECTED_HEAD_SHA",
        "git ls-remote origin refs/heads/main",
        "Default-branch HEAD moved before assurance dispatch",
        "if: steps.persist.outputs.changed == 'true'",
    )
    for marker in required_markers:
        if marker not in text:
            fail(f"instance-watch missing safety/dispatch marker: {marker}")

    invoked = re.findall(r"gh workflow run\s+([^\s]+\.ya?ml)\s+--ref\s+main", text)
    if not invoked:
        fail("instance-watch does not dispatch any current-head assurance workflows")

    expected = {"validate.yml", "pages.yml"}
    if set(invoked) != expected:
        fail(f"unexpected instance-watch dispatch set: {sorted(set(invoked))}; expected {sorted(expected)}")

    for name in sorted(expected):
        path = WORKFLOWS / name
        if not path.is_file():
            fail(f"dispatched workflow does not exist: {name}")
        target = path.read_text(encoding="utf-8")
        if "workflow_dispatch:" not in target:
            fail(f"dispatched workflow lacks workflow_dispatch trigger: {name}")

    print("PASS instance-watch current-head assurance dispatch contract")
    print(f"  dispatched workflows: {', '.join(sorted(expected))}")
    print("  stale-head protection: required")
    return 0


if __name__ == "__main__":
    sys.exit(main())
