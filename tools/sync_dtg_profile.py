#!/usr/bin/env python3
"""Synchronize the checked-in DTG RAHP profile with authoritative DTG discovery.

This is DTG deployment machinery, not generic RAHP core. Discovery authority remains
instances/dtg/instance.yaml -> DTG Portfolio Monitor registry + configured matching forks.
Assessment runs should pin immutable revisions after this perimeter is synchronized.
"""
from __future__ import annotations

import argparse
import copy
import pathlib
import sys
from typing import Any

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import dtg_portfolio  # noqa: E402

DEFAULT_INSTANCE = ROOT / "instances" / "dtg" / "instance.yaml"
DEFAULT_PROFILE = ROOT / "profiles" / "dtg" / "rahp.yaml"

DEFAULT_SCOPE = [
    "README.md",
    "docs/**",
    "specs/**",
    "schemas/**",
    "**/*spec*.md",
    ".github/workflows/**",
]


def portable_target(target: dict[str, Any]) -> dict[str, Any]:
    """Render one discovered DTG target into the portable profile shape."""
    return {
        "id": target["id"],
        "repository": target["repository"],
        "branch": target.get("branch", "main"),
        **({"upstream": target["upstream"]} if target.get("upstream") else {}),
        "context": {
            "title": target["repository"],
            "type": target.get("role") or "repository",
            "description": (
                f"DTG instance target discovered from {target['source']}; "
                f"workstream={target.get('workstream') or 'n/a'}; "
                f"lifecycle={target.get('lifecycle') or 'n/a'}; "
                f"reporting_weight={target.get('reporting_weight') or 'n/a'}."
            ),
        },
        "scope": {"include": target.get("material_paths") or DEFAULT_SCOPE},
        "reviews": ["rahp", "security", "combined"],
    }


def authoritative_repositories(cfg: dict[str, Any]) -> list[dict[str, Any]]:
    return [portable_target(t) for t in dtg_portfolio.discover(cfg)]


def normalized_repositories(profile: dict[str, Any]) -> list[dict[str, Any]]:
    """Normalize only fields governed by DTG portfolio discovery."""
    keep = []
    for item in profile.get("repositories", []):
        keep.append({
            "id": item.get("id"),
            "repository": item.get("repository"),
            "branch": item.get("branch", "main"),
            **({"upstream": item.get("upstream")} if item.get("upstream") else {}),
            "context": {
                "title": (item.get("context") or {}).get("title"),
                "type": (item.get("context") or {}).get("type"),
                "description": (item.get("context") or {}).get("description"),
            },
            "scope": {"include": ((item.get("scope") or {}).get("include") or [])},
            "reviews": item.get("reviews") or [],
        })
    return keep


def diff(profile: dict[str, Any], expected: list[dict[str, Any]]) -> list[str]:
    actual = normalized_repositories(profile)
    messages: list[str] = []

    a_by_repo = {x["repository"]: x for x in actual}
    e_by_repo = {x["repository"]: x for x in expected}

    for repo in sorted(e_by_repo.keys() - a_by_repo.keys()):
        messages.append(f"missing repository: {repo}")
    for repo in sorted(a_by_repo.keys() - e_by_repo.keys()):
        messages.append(f"unexpected repository: {repo}")

    for repo in sorted(e_by_repo.keys() & a_by_repo.keys()):
        if a_by_repo[repo] != e_by_repo[repo]:
            messages.append(f"metadata drift: {repo}")

    if [x["repository"] for x in actual] != [x["repository"] for x in expected]:
        messages.append("repository ordering drift")

    return messages


def synchronized_profile(existing: dict[str, Any], expected: list[dict[str, Any]], cfg: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(existing)
    result["repositories"] = expected
    result.setdefault("extensions", {})
    result["extensions"]["operational_profile"] = "instances/dtg/generated/repositories.yaml"
    result["extensions"]["portfolio_registry"] = cfg["portfolio"]["registry_repository"]
    result["extensions"]["portfolio_registry_path"] = cfg["portfolio"]["registry_path"]
    result["extensions"]["portfolio_authority"] = "dtg-instance-discovery"
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--instance", type=pathlib.Path, default=DEFAULT_INSTANCE)
    parser.add_argument("--profile", type=pathlib.Path, default=DEFAULT_PROFILE)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    args = parser.parse_args()

    cfg = dtg_portfolio.load_yaml(args.instance)
    existing = dtg_portfolio.load_yaml(args.profile)
    expected = authoritative_repositories(cfg)
    problems = diff(existing, expected)

    if args.check:
        if problems:
            print("DTG profile drift detected:", file=sys.stderr)
            for item in problems:
                print(f"  - {item}", file=sys.stderr)
            print("Run: python3 tools/sync_dtg_profile.py --write", file=sys.stderr)
            return 1
        print(f"PASS DTG profile synchronized with authoritative discovery ({len(expected)} targets)")
        return 0

    updated = synchronized_profile(existing, expected, cfg)
    args.profile.write_text(yaml.safe_dump(updated, sort_keys=False), encoding="utf-8")
    print(f"wrote {args.profile} from authoritative DTG discovery ({len(expected)} targets)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
