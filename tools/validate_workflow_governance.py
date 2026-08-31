#!/usr/bin/env python3
"""Enforce the governed GitHub Actions surface and anti-bloat invariants."""
from __future__ import annotations

from pathlib import Path
import re
import sys
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_ROOT = ROOT / ".github/workflows"
POLICY = ROOT / "config/workflow-governance.yaml"


def load_base(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.load(handle, Loader=yaml.BaseLoader)


def main() -> int:
    errors: list[str] = []
    policy = yaml.safe_load(POLICY.read_text(encoding="utf-8")) or {}
    if policy.get("schema") != "rahp-workflow-governance/v1":
        errors.append("workflow governance schema must be rahp-workflow-governance/v1")

    inventory = policy.get("workflows") or {}
    if not isinstance(inventory, dict) or not inventory:
        errors.append("workflow governance inventory must be a non-empty mapping")
        inventory = {}

    actual = sorted(path.name for path in WORKFLOW_ROOT.glob("*.yml"))
    declared = sorted(inventory)
    maximum = int(policy.get("max_workflows") or 0)
    if not maximum:
        errors.append("max_workflows must be a positive integer")
    elif len(actual) > maximum:
        errors.append(f"workflow budget exceeded: {len(actual)} > {maximum}")

    missing = sorted(set(declared) - set(actual))
    undeclared = sorted(set(actual) - set(declared))
    if missing:
        errors.append("declared workflows missing from repository: " + ", ".join(missing))
    if undeclared:
        errors.append("undeclared workflows are forbidden: " + ", ".join(undeclared))

    responsibilities: dict[str, str] = {}
    for name, metadata in inventory.items():
        if not isinstance(metadata, dict):
            errors.append(f"{name}: inventory metadata must be a mapping")
            continue
        responsibility = str(metadata.get("responsibility") or "").strip()
        workflow_class = str(metadata.get("class") or "").strip()
        if not responsibility:
            errors.append(f"{name}: responsibility is required")
        elif responsibility in responsibilities:
            errors.append(
                f"duplicate workflow responsibility {responsibility!r}: "
                f"{responsibilities[responsibility]} and {name}"
            )
        else:
            responsibilities[responsibility] = name
        if not workflow_class:
            errors.append(f"{name}: class is required")

    canonical = "clean-room-assessment.yml"
    if canonical not in actual:
        errors.append(f"missing canonical clean-room executor: {canonical}")
    forbidden_clean_room = [
        name for name in actual
        if name != canonical and (
            name.startswith("clean-room-") or
            name.startswith("true-clean-room-") or
            re.search(r"clean-room.*\d+", name)
        )
    ]
    if forbidden_clean_room:
        errors.append(
            "target/issue-specific clean-room workflows are forbidden: "
            + ", ".join(forbidden_clean_room)
        )
    if (WORKFLOW_ROOT / canonical).exists():
        text = (WORKFLOW_ROOT / canonical).read_text(encoding="utf-8").lower()
        leaked = [
            token for token in ("dogwood", "openvtc", "vti-dogwood", "true-clean-room-dogwood")
            if token in text
        ]
        if leaked:
            errors.append("canonical clean-room executor contains target-specific literals: " + ", ".join(leaked))

    if policy.get("forbid_dispatch_only_wrappers") is True:
        for name in actual:
            data = load_base(WORKFLOW_ROOT / name) or {}
            jobs = data.get("jobs") or {}
            if not isinstance(jobs, dict) or len(jobs) != 1:
                continue
            job = next(iter(jobs.values()))
            if isinstance(job, dict) and "uses" in job and "steps" not in job:
                errors.append(
                    f"{name}: dispatch-only local workflow wrapper is forbidden; "
                    "dispatch/call the reusable workflow directly with declarative inputs"
                )

    removed_wrappers = {
        "cawg-cross-spec-pressure-test.yml",
        "dtg-cross-spec-pressure-test.yml",
    }
    resurrected = sorted(removed_wrappers & set(actual))
    if resurrected:
        errors.append("removed cross-spec wrappers must not be reintroduced: " + ", ".join(resurrected))

    if errors:
        print("Workflow governance: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Workflow governance: PASS")
    print(f"- workflow files: {len(actual)} / budget {maximum}")
    print("- exact inventory synchronized")
    print("- responsibilities unique")
    print("- dispatch-only wrappers absent")
    print("- canonical clean-room boundary preserved")
    return 0


if __name__ == "__main__":
    sys.exit(main())
