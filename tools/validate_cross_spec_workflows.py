#!/usr/bin/env python3
"""Validate cross-specification workflow wrappers against profile registries.

The generic workflow is the only execution implementation. Portfolio-specific
workflows may expose curated workflow_dispatch choices, but every choice must
correspond exactly to a runnable composition in the referenced profile.
"""
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]

WRAPPERS = [
    (
        ROOT / ".github/workflows/dtg-cross-spec-pressure-test.yml",
        ROOT / "profiles/dtg/cross-spec-tests.yaml",
        "profiles/dtg/cross-spec-tests.yaml",
        True,
    ),
    (
        ROOT / ".github/workflows/cawg-cross-spec-pressure-test.yml",
        ROOT / "profiles/cawg/cross-spec-tests.yaml",
        "profiles/cawg/cross-spec-tests.yaml",
        False,
    ),
]
GENERIC = ROOT / ".github/workflows/cross-spec-pressure-test.yml"


def load_base(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.load(handle, Loader=yaml.BaseLoader)


def load_safe(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def main() -> int:
    errors = []
    generic = load_base(GENERIC)
    triggers = generic.get("on", {})
    if "workflow_call" not in triggers:
        errors.append("generic cross-spec workflow must expose workflow_call")
    if "workflow_dispatch" not in triggers:
        errors.append("generic cross-spec workflow must retain workflow_dispatch")
    call_inputs = ((triggers.get("workflow_call") or {}).get("inputs") or {})
    scoped_input = call_inputs.get("composition_scoped_registry_validation") or {}
    if scoped_input.get("type") != "boolean" or scoped_input.get("default") not in ("false", False):
        errors.append("generic cross-spec workflow must expose composition_scoped_registry_validation boolean default false")

    for wrapper_path, registry_path, expected_registry, expect_scoped in WRAPPERS:
        wrapper = load_base(wrapper_path)
        registry = load_safe(registry_path)
        runnable = {
            item["id"]
            for item in registry.get("compositions", [])
            if item.get("runnable") is True
        }
        try:
            dispatch = wrapper["on"]["workflow_dispatch"]
            input_cfg = dispatch["inputs"]["composition_id"]
            options = set(input_cfg["options"])
            default = input_cfg.get("default")
        except (KeyError, TypeError):
            errors.append(f"{wrapper_path.name}: missing workflow_dispatch composition_id choice")
            continue

        if options != runnable:
            missing = sorted(runnable - options)
            extra = sorted(options - runnable)
            errors.append(
                f"{wrapper_path.name}: choices drift from runnable registry entries; "
                f"missing={missing}, extra={extra}"
            )
        if default not in runnable:
            errors.append(f"{wrapper_path.name}: default {default!r} is not runnable")

        try:
            job = wrapper["jobs"]["assess"]
            target = job["uses"]
            wired_registry = job["with"]["registry_path"]
            wired_composition = job["with"]["composition_id"]
            scoped = job.get("with", {}).get("composition_scoped_registry_validation", "false")
        except (KeyError, TypeError):
            errors.append(f"{wrapper_path.name}: assess job is not wired to reusable generic workflow")
            continue

        if target != "./.github/workflows/cross-spec-pressure-test.yml":
            errors.append(f"{wrapper_path.name}: must call the generic cross-spec workflow")
        if wired_registry != expected_registry:
            errors.append(
                f"{wrapper_path.name}: expected registry {expected_registry}, got {wired_registry}"
            )
        if "inputs.composition_id" not in wired_composition:
            errors.append(f"{wrapper_path.name}: selected composition is not forwarded")
        actual_scoped = str(scoped).lower() == "true"
        if actual_scoped != expect_scoped:
            errors.append(
                f"{wrapper_path.name}: composition_scoped_registry_validation={actual_scoped}, expected {expect_scoped}"
            )

    if errors:
        print("Cross-spec workflow validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Cross-spec workflow validation: PASS")
    for wrapper_path, registry_path, _, expect_scoped in WRAPPERS:
        registry = load_safe(registry_path)
        count = sum(1 for item in registry.get("compositions", []) if item.get("runnable") is True)
        mode = "composition-scoped" if expect_scoped else "full-registry"
        print(f"- {wrapper_path.name}: {count} runnable choices synchronized; registry validation={mode}")
    print("- generic workflow: workflow_dispatch + workflow_call")
    return 0


if __name__ == "__main__":
    sys.exit(main())
