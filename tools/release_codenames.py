#!/usr/bin/env python3
"""Pinned-pool release codename governance for RAHP."""
from __future__ import annotations

import argparse
import json
import random
import secrets
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
POOL = ROOT / "config" / "release-codenames.txt"
POLICY = ROOT / "config" / "release-codename-policy.json"
HISTORY = ROOT / "config" / "release-codename-history.json"
DECLARATION = ROOT / "method" / "release.yaml"


class PolicyError(ValueError):
    pass


def load_pool() -> list[str]:
    names = [line.strip() for line in POOL.read_text(encoding="utf-8").splitlines() if line.strip() and not line.lstrip().startswith("#")]
    return names


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def aliases(policy: dict) -> dict[str, dict]:
    return {item["codename"].casefold(): item for item in policy.get("grandfatheredHistoryAliases", [])}


def validate_repository(release_doc: dict | None = None) -> list[str]:
    errors: list[str] = []
    try:
        names = load_pool()
        policy = load_json(POLICY)
        history = load_json(HISTORY)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"release codename governance could not be loaded: {exc}"]

    if policy.get("schemaVersion") != 1:
        errors.append("release codename policy schemaVersion must be 1")
    if history.get("schemaVersion") != 1:
        errors.append("release codename history schemaVersion must be 1")
    if policy.get("pool") != "config/release-codenames.txt":
        errors.append("release codename policy must reference config/release-codenames.txt")
    if len(names) < int(policy.get("minimumPoolSize", 20)):
        errors.append("release codename pool is below minimumPoolSize")
    folded = [name.casefold() for name in names]
    if len(folded) != len(set(folded)):
        errors.append("release codename pool contains case-insensitive duplicates")
    if not str(policy.get("source", {}).get("url", "")).startswith("https://"):
        errors.append("release codename source URL must use https")
    selection = policy.get("selection", {})
    if selection.get("liveSourceFetchAtRelease") is not False:
        errors.append("release-time source fetching must be disabled")
    if selection.get("persistBeforeAcceptance") is not True:
        errors.append("codename must be persisted before human release acceptance")

    allowed = {name.casefold() for name in names}
    grandfathered = aliases(policy)
    releases = history.get("releases", [])
    versions = [item.get("version") for item in releases]
    if len(versions) != len(set(versions)):
        errors.append("release codename history contains duplicate versions")
    used: list[str] = []
    for item in releases:
        codename = str(item.get("codename") or "")
        if codename.casefold() not in allowed and codename.casefold() not in grandfathered:
            errors.append(f"history codename is neither in the pinned pool nor grandfathered: {codename!r}")
        if item.get("status") not in {"candidate", "published"}:
            errors.append(f"invalid codename history status for {item.get('version')}")
        used.append(codename.casefold())
    if not selection.get("allowReuseAfterExhaustion", False) and len(used) != len(set(used)):
        errors.append("release codename history reuses a name while policy forbids reuse")

    if release_doc is None:
        try:
            release_doc = yaml.safe_load(DECLARATION.read_text(encoding="utf-8")) or {}
        except (OSError, yaml.YAMLError) as exc:
            errors.append(f"release declaration could not be loaded for codename validation: {exc}")
            release_doc = {}
    release = release_doc.get("release") or {}
    tag = str(release.get("tag") or "")
    common = str((release.get("name") or {}).get("common") or "")
    scientific = str((release.get("name") or {}).get("scientific") or "")
    binding = next((item for item in releases if item.get("version") == tag), None)
    if binding is None:
        errors.append(f"current release {tag!r} has no persisted codename history binding")
    elif binding.get("codename") != common:
        errors.append("current release common name differs from persisted codename history")
    alias = grandfathered.get(common.casefold())
    if alias and alias.get("scientific") and alias.get("scientific") != scientific:
        errors.append("grandfathered release alias scientific name differs from declaration")
    return errors


def select(version: str, seed: str | None = None) -> tuple[str, bool]:
    errors = validate_repository()
    # Future candidate selection is allowed even if current declaration is bound to current release.
    non_binding_errors = [e for e in errors if not e.startswith("current release")]
    if non_binding_errors:
        raise PolicyError("; ".join(non_binding_errors))
    names = load_pool()
    policy = load_json(POLICY)
    history = load_json(HISTORY)
    existing = next((item for item in history["releases"] if item.get("version") == version), None)
    if existing:
        return existing["codename"], True
    used = {str(item.get("codename") or "").casefold() for item in history["releases"]}
    available = [name for name in names if name.casefold() not in used]
    if not available:
        if policy["selection"].get("allowReuseAfterExhaustion", False):
            available = names
        else:
            raise PolicyError("release codename pool exhausted and reuse is forbidden")
    return (secrets.choice(available) if seed is None else random.Random(seed).choice(available)), False


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate")
    choose = sub.add_parser("select")
    choose.add_argument("--version", required=True)
    choose.add_argument("--seed")
    args = parser.parse_args()
    if args.command == "validate":
        errors = validate_repository()
        if errors:
            raise PolicyError("; ".join(errors))
        print("PASS RAHP release codename governance")
        return 0
    codename, existing = select(args.version, args.seed)
    print(json.dumps({"version": args.version, "codename": codename, "existing": existing}))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except PolicyError as exc:
        print(f"ERROR: {exc}")
        raise SystemExit(2)
