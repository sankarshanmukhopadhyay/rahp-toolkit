#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import argparse
import json
import sys
import yaml

ROOT = Path(__file__).resolve().parent.parent


def load_registry(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if data.get("deprecated") and data.get("canonical_registry"):
        return load_registry(ROOT / data["canonical_registry"])
    return data


def runnable_compositions(data: dict) -> list[dict]:
    return [
        item
        for item in data.get("compositions", [])
        if isinstance(item, dict) and item.get("runnable") is True
    ]


def plan_compositions(data: dict, plan: str, repositories: set[str]) -> list[dict]:
    runnable = runnable_compositions(data)
    if plan == "full":
        return runnable

    selected: list[dict] = []
    for item in runnable:
        execution_class = item.get("execution_class")
        component_repositories = {
            str(component.get("repository"))
            for component in item.get("components", [])
            if isinstance(component, dict) and component.get("repository")
        }
        if execution_class == "core":
            selected.append(item)
        elif execution_class == "conditional" and repositories.intersection(component_repositories):
            selected.append(item)
    return selected


def emit(values: dict[str, str], github_output: Path | None) -> None:
    for key, value in values.items():
        print(f"{key}={value}")
    if github_output:
        with github_output.open("a", encoding="utf-8") as handle:
            for key, value in values.items():
                handle.write(f"{key}={value}\n")


def self_test() -> int:
    fixture = {
        "profile": {"id": "test"},
        "compositions": [
            {
                "id": "core-a",
                "runnable": True,
                "execution_class": "core",
                "components": [{"repository": "o/a"}, {"repository": "o/b"}],
            },
            {
                "id": "conditional-b",
                "runnable": True,
                "execution_class": "conditional",
                "components": [{"repository": "o/b"}, {"repository": "o/c"}],
            },
            {
                "id": "reference-c",
                "runnable": False,
                "execution_class": "reference",
                "components": [{"repository": "o/c"}, {"repository": "o/d"}],
            },
        ],
    }
    routine = [item["id"] for item in plan_compositions(fixture, "routine", set())]
    affected = [item["id"] for item in plan_compositions(fixture, "routine", {"o/c"})]
    full = [item["id"] for item in plan_compositions(fixture, "full", set())]
    if routine != ["core-a"]:
        raise AssertionError(f"routine plan must select only core compositions: {routine}")
    if affected != ["core-a", "conditional-b"]:
        raise AssertionError(f"routine affected plan must add matching conditional compositions: {affected}")
    if full != ["core-a", "conditional-b"]:
        raise AssertionError(f"full plan must select every runnable composition: {full}")
    print("cross-spec selection self-test: PASS")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Resolve one cross-spec composition or plan a materiality-bounded execution set."
    )
    parser.add_argument("--registry", help="Cross-spec registry path")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--composition", help="Resolve one runnable composition")
    mode.add_argument("--plan", choices=("routine", "full"), help="Select runnable compositions by execution policy")
    parser.add_argument(
        "--repository",
        action="append",
        default=[],
        help="Materially changed component repository; repeat as needed for routine planning",
    )
    parser.add_argument("--github-output", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        return self_test()
    if not args.registry:
        parser.error("--registry is required unless --self-test is used")
    if not args.composition and not args.plan:
        parser.error("one of --composition or --plan is required")

    registry_path = Path(args.registry)
    registry_path = registry_path if registry_path.is_absolute() else ROOT / registry_path
    data = load_registry(registry_path)
    profile_id = (data.get("profile") or {}).get("id", "external")

    if args.composition:
        item = next(
            (candidate for candidate in runnable_compositions(data) if candidate.get("id") == args.composition),
            None,
        )
        if not item:
            raise SystemExit(f"Composition is unknown or not runnable: {args.composition}")
        values = {
            "assessment": str(item["assessment"]),
            "corpus_id": str(item["corpus_id"]),
            "profile_id": str(profile_id),
            "execution_class": str(item.get("execution_class", "")),
        }
        emit(values, args.github_output)
        return 0

    selected = plan_compositions(data, args.plan, set(args.repository))
    ids = [str(item["id"]) for item in selected]
    values = {
        "profile_id": str(profile_id),
        "plan": str(args.plan),
        "composition_ids": json.dumps(ids, separators=(",", ":")),
        "composition_count": str(len(ids)),
    }
    emit(values, args.github_output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
