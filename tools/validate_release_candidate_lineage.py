#!/usr/bin/env python3
"""Validate qualified-candidate to release-head lineage before publication (#1150).

Release evidence may be pinned to a qualified candidate that is an ancestor of the
published release commit. Any intervening changes must be limited to release/publication
metadata. This prevents unqualified implementation changes from riding after the evidence
SHA while preserving the repository's qualification-promotion pattern.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
SHA = re.compile(r"^[0-9a-f]{40}$")

BASE_ALLOWED = {
    "CHANGELOG.md",
    "PROJECT-STATUS.yaml",
    "README.md",
    "ROADMAP.md",
    "config/release-codename-history.json",
    "docs/engine-contract.md",
    "method/release.yaml",
    "method/versioning.yaml",
    "review/README.md",
}


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def allowed_paths(release_doc: dict, qualification: dict) -> set[str]:
    allowed = set(BASE_ALLOWED)
    notes = ((release_doc.get("release") or {}).get("notes") or {}).get("path")
    manifest = ((release_doc.get("release") or {}).get("qualification") or {}).get("manifest")
    if notes:
        allowed.add(str(notes))
    if manifest:
        allowed.add(str(manifest))
    release_evidence = (qualification.get("evidence") or {}).get("release_evidence")
    if release_evidence:
        allowed.add(str(release_evidence))
    return allowed


def classify_changed_paths(paths: list[str], allowed: set[str]) -> list[str]:
    return sorted(path for path in paths if path not in allowed)


def git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


def validate(head: str) -> list[str]:
    errors: list[str] = []
    release_doc = load_yaml(ROOT / "method/release.yaml")
    release = release_doc.get("release") or {}
    qualification_rel = ((release.get("qualification") or {}).get("manifest"))
    if not qualification_rel:
        return ["release declaration has no qualification manifest"]
    qualification = load_yaml(ROOT / str(qualification_rel))
    candidate = ((qualification.get("release_cut") or {}).get("candidate_sha"))

    if release.get("status") != "released" or release.get("qualification_status") != "qualified":
        return []

    if not isinstance(candidate, str) or not SHA.fullmatch(candidate):
        errors.append("qualified released state requires a full release_cut.candidate_sha")
        return errors
    if not SHA.fullmatch(str(head or "")):
        errors.append("release head must be a full 40-character commit SHA")
        return errors

    ancestor = git("merge-base", "--is-ancestor", candidate, head)
    if ancestor.returncode != 0:
        errors.append(f"qualified candidate {candidate} is not an ancestor of release head {head}")
        return errors

    if candidate == head:
        return errors

    diff = git("diff", "--name-only", candidate, head)
    if diff.returncode != 0:
        errors.append("cannot enumerate candidate-to-release changed paths: " + diff.stderr.strip())
        return errors

    changed = [line.strip() for line in diff.stdout.splitlines() if line.strip()]
    unexpected = classify_changed_paths(changed, allowed_paths(release_doc, qualification))
    if unexpected:
        errors.append(
            "post-candidate release head contains non-publication changes: "
            + ", ".join(unexpected)
        )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--head", default=os.environ.get("GITHUB_SHA", ""))
    args = parser.parse_args()
    head = args.head
    if not head:
        result = git("rev-parse", "HEAD")
        if result.returncode != 0:
            print("ERROR: cannot resolve release head")
            return 1
        head = result.stdout.strip()

    errors = validate(head)
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1

    release_doc = load_yaml(ROOT / "method/release.yaml")
    qualification = load_yaml(
        ROOT / str(((release_doc.get("release") or {}).get("qualification") or {}).get("manifest"))
    )
    candidate = (qualification.get("release_cut") or {}).get("candidate_sha")
    print(f"PASS release candidate lineage: {candidate} -> {head}; post-candidate changes are publication metadata only.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
