#!/usr/bin/env python3
"""Generic RAHP release metadata, verification and qualification CLI."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DECLARATION = ROOT / "method" / "release.yaml"


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def declaration() -> dict:
    doc = load_yaml(DECLARATION)
    if doc.get("contract") != "rahp-release-declaration-v1":
        raise ValueError("method/release.yaml must use rahp-release-declaration-v1")
    release = doc.get("release")
    if not isinstance(release, dict):
        raise ValueError("method/release.yaml must define release mapping")
    return doc


def resolve_repo_path(value: str, label: str) -> Path:
    path = (ROOT / value).resolve()
    try:
        path.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise ValueError(f"{label} must remain within repository: {value}") from exc
    return path


def metadata(doc: dict) -> dict:
    r = doc["release"]
    q = r.get("qualification") or {}
    notes = r.get("notes") or {}
    name = r.get("name") or {}
    return {
        "version": str(r.get("version") or ""),
        "tag": str(r.get("tag") or ""),
        "status": str(r.get("status") or ""),
        "qualification_status": str(r.get("qualification_status") or ""),
        "title": str(r.get("title") or ""),
        "theme": str(r.get("theme") or ""),
        "common_name": str(name.get("common") or ""),
        "scientific_name": str(name.get("scientific") or ""),
        "qualification_manifest": str(q.get("manifest") or ""),
        "qualification_validator": str(q.get("validator") or ""),
        "notes_path": str(notes.get("path") or ""),
        "target_branch": str((doc.get("publication") or {}).get("target_branch") or "main"),
    }


def verify(doc: dict) -> list[str]:
    r = doc["release"]
    meta = metadata(doc)
    errors: list[str] = []
    version = meta["version"]
    tag = meta["tag"]

    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        errors.append(f"release.version must be semantic x.y.z, got {version!r}")
    if tag != f"v{version}":
        errors.append(f"release.tag must be v{version}, got {tag!r}")
    if meta["status"] not in {"candidate", "released"}:
        errors.append("release.status must be candidate or released")
    if meta["qualification_status"] not in {"candidate", "cut-ready", "qualified"}:
        errors.append("release.qualification_status is not permitted")
    for key in ("title", "qualification_manifest", "qualification_validator", "notes_path"):
        if not meta[key]:
            errors.append(f"release metadata requires {key}")

    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    if package.get("version") != version:
        errors.append(f"package.json version {package.get('version')!r} != {version!r}")
    lock = json.loads((ROOT / "package-lock.json").read_text(encoding="utf-8"))
    if lock.get("version") != version or (lock.get("packages") or {}).get("", {}).get("version") != version:
        errors.append("package-lock.json root version is not synchronized")
    for pkg in sorted((ROOT / "packages").glob("*/package.json")):
        pdoc = json.loads(pkg.read_text(encoding="utf-8"))
        if pdoc.get("version") != version:
            errors.append(f"{pkg.relative_to(ROOT)} version is not {version}")
        for dep, dep_version in (pdoc.get("dependencies") or {}).items():
            if dep.startswith("@rahp/") and dep_version != version:
                errors.append(f"{pkg.relative_to(ROOT)} dependency {dep} is not {version}")

    status = load_yaml(ROOT / "PROJECT-STATUS.yaml")
    if str(status.get("stable_release")) != version:
        errors.append("PROJECT-STATUS stable_release differs from release declaration")
    if status.get("release_status") != meta["status"]:
        errors.append("PROJECT-STATUS release_status differs from release declaration")
    if status.get("qualification_status") != meta["qualification_status"]:
        errors.append("PROJECT-STATUS qualification_status differs from release declaration")
    if status.get("qualification_contract") != meta["qualification_manifest"]:
        errors.append("PROJECT-STATUS qualification_contract differs from release declaration")

    status_name = status.get("release_name") or {}
    declared_name = r.get("name") or {}
    if status_name.get("common_name") != declared_name.get("common"):
        errors.append("PROJECT-STATUS common release name differs from declaration")
    if status_name.get("scientific_name") != declared_name.get("scientific"):
        errors.append("PROJECT-STATUS scientific release name differs from declaration")

    compat = status.get("compatibility") or {}
    for key, expected in (r.get("compatibility") or {}).items():
        if compat.get(key) != expected:
            errors.append(f"compatibility mismatch for {key}")

    for key, label in (
        ("qualification_manifest", "qualification manifest"),
        ("qualification_validator", "qualification validator"),
        ("notes_path", "release notes"),
    ):
        try:
            path = resolve_repo_path(meta[key], label)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if not path.is_file():
            errors.append(f"{label} does not exist: {meta[key]}")

    versioning = load_yaml(ROOT / "method" / "versioning.yaml")
    if versioning.get("stable_release") != tag:
        errors.append("method/versioning.yaml stable_release differs from release declaration")

    return errors


def run_qualification(doc: dict) -> int:
    errors = verify(doc)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    meta = metadata(doc)
    validator = resolve_repo_path(meta["qualification_validator"], "qualification validator")
    proc = subprocess.run([sys.executable, str(validator)], cwd=ROOT)
    if proc.returncode != 0:
        return proc.returncode
    print(f"PASS qualification: {meta['tag']} via {meta['qualification_validator']}")
    return 0


def write_github_output(meta: dict, path: Path) -> None:
    with path.open("a", encoding="utf-8") as fh:
        for key, value in meta.items():
            if "\n" in value or "\r" in value:
                raise ValueError(f"GitHub output value for {key} must be single-line")
            fh.write(f"{key}={value}\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    meta_parser = sub.add_parser("metadata", help="Print normalized current-release metadata")
    meta_parser.add_argument("--json", action="store_true")
    meta_parser.add_argument("--github-output", type=Path)
    sub.add_parser("verify", help="Verify generic release declaration and synchronized surfaces")
    sub.add_parser("qualify", help="Verify declaration then invoke its declared qualification validator")

    args = parser.parse_args()
    try:
        doc = declaration()
    except (ValueError, OSError, yaml.YAMLError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.command == "metadata":
        meta = metadata(doc)
        if args.github_output:
            write_github_output(meta, args.github_output)
        if args.json or not args.github_output:
            print(json.dumps(meta, indent=2, sort_keys=True))
        return 0

    if args.command == "verify":
        errors = verify(doc)
        if errors:
            for error in errors:
                print(f"ERROR: {error}")
            return 1
        meta = metadata(doc)
        print(f"PASS release declaration: {meta['tag']} ({meta['title']})")
        return 0

    return run_qualification(doc)


if __name__ == "__main__":
    raise SystemExit(main())
