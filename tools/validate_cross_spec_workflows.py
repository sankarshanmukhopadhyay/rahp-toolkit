#!/usr/bin/env python3
"""Validate the generic cross-specification executor and profile registries.

The generic workflow is the sole cross-specification execution surface. Profile
selection is declarative through registry_path + composition_id; portfolio-
specific dispatch wrappers are intentionally forbidden.
"""
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
GENERIC = ROOT / ".github/workflows/cross-spec-pressure-test.yml"
REGISTRIES = [
    ("dtg", ROOT / "profiles/dtg/cross-spec-tests.yaml"),
    ("cawg-c2pa", ROOT / "profiles/cawg/cross-spec-tests.yaml"),
]
REMOVED_WRAPPERS = [
    ROOT / ".github/workflows/dtg-cross-spec-pressure-test.yml",
    ROOT / ".github/workflows/cawg-cross-spec-pressure-test.yml",
]
REQUIRED_INPUTS = {
    "registry_path",
    "composition_id",
    "composition_scoped_registry_validation",
    "assessment_lineage",
}


def load_base(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.load(handle, Loader=yaml.BaseLoader)


def load_safe(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def validate_trigger_inputs(trigger_name: str, trigger: dict, errors: list[str]) -> None:
    inputs = (trigger or {}).get("inputs") or {}
    missing = sorted(REQUIRED_INPUTS - set(inputs))
    if missing:
        errors.append(f"generic {trigger_name} missing inputs: {missing}")
    scoped = inputs.get("composition_scoped_registry_validation") or {}
    if scoped.get("type") != "boolean" or scoped.get("default") not in ("false", False):
        errors.append(
            f"generic {trigger_name} must expose "
            "composition_scoped_registry_validation boolean default false"
        )


def main() -> int:
    errors: list[str] = []
    generic = load_base(GENERIC) or {}
    triggers = generic.get("on", {})
    for trigger_name in ("workflow_call", "workflow_dispatch"):
        trigger = triggers.get(trigger_name)
        if not isinstance(trigger, dict):
            errors.append(f"generic cross-spec workflow must expose {trigger_name}")
        else:
            validate_trigger_inputs(trigger_name, trigger, errors)

    for path in REMOVED_WRAPPERS:
        if path.exists():
            errors.append(
                f"{path.name}: profile-specific cross-spec wrapper must not be reintroduced; "
                "use cross-spec-pressure-test.yml with declarative inputs"
            )

    for profile_id, registry_path in REGISTRIES:
        registry = load_safe(registry_path) or {}
        profile = registry.get("profile") or {}
        if profile.get("id") != profile_id:
            errors.append(
                f"{registry_path.relative_to(ROOT)}: expected profile.id={profile_id!r}, "
                f"got {profile.get('id')!r}"
            )
        compositions = registry.get("compositions") or []
        if not isinstance(compositions, list):
            errors.append(f"{registry_path.relative_to(ROOT)}: compositions must be a list")
            continue
        ids = [str(item.get("id") or "") for item in compositions if isinstance(item, dict)]
        if any(not item for item in ids):
            errors.append(f"{registry_path.relative_to(ROOT)}: every composition requires an id")
        if len(ids) != len(set(ids)):
            errors.append(f"{registry_path.relative_to(ROOT)}: composition ids must be unique")
        runnable = [
            item.get("id") for item in compositions
            if isinstance(item, dict) and item.get("runnable") is True
        ]
        if not runnable:
            errors.append(f"{registry_path.relative_to(ROOT)}: at least one runnable composition is required")

    if errors:
        print("Cross-spec workflow validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Cross-spec workflow validation: PASS")
    for profile_id, registry_path in REGISTRIES:
        registry = load_safe(registry_path) or {}
        runnable = sum(1 for item in registry.get("compositions", []) if item.get("runnable") is True)
        print(f"- {profile_id}: {runnable} runnable composition(s) via generic executor")
    print("- generic workflow: workflow_dispatch + workflow_call")
    print("- profile-specific workflow wrappers: absent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
