#!/usr/bin/env python3
"""Validate the preserved RAHP v1.5 qualification evidence on current or later v1 releases."""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "method" / "v1.5-release-qualification.yaml"


def semver_tuple(value: str) -> tuple[int, int, int]:
    major, minor, patch = value.lstrip("v").split(".")
    return int(major), int(minor), int(patch)


def main() -> int:
    q = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    status = yaml.safe_load((ROOT / "PROJECT-STATUS.yaml").read_text(encoding="utf-8"))
    errors: list[str] = []

    if q.get("release") != "v1.5.0":
        errors.append("preserved v1.5 qualification manifest no longer identifies v1.5.0")

    if semver_tuple(str(status.get("stable_release", "0.0.0"))) < semver_tuple("1.5.0"):
        errors.append("current stable release cannot precede the preserved v1.5.0 qualification")

    compat = status.get("compatibility") or {}
    for key, expected in (q.get("stable_compatibility") or {}).items():
        if compat.get(key) != expected:
            errors.append(f"stable compatibility mismatch for preserved v1.5 contract {key}: {compat.get(key)!r} != {expected!r}")

    for label, rel in (q.get("required_evidence") or {}).items():
        if not (ROOT / rel).exists():
            errors.append(f"preserved v1.5 required evidence missing ({label}): {rel}")

    for rel in q.get("portable_paths", []):
        if not (ROOT / rel).exists():
            errors.append(f"preserved v1.5 portable contract missing: {rel}")

    release_notes = ROOT / "docs" / "releases" / "v1.5.0.md"
    release_prep = ROOT / "docs" / "releases" / "v1.5.0-preparation.md"
    if not release_notes.exists():
        errors.append("preserved v1.5.0 release notes are missing")
    if not release_prep.exists():
        errors.append("preserved v1.5.0 release-preparation evidence is missing")

    notes = release_notes.read_text(encoding="utf-8") if release_notes.exists() else ""
    if "Purple Leaf Blue" not in notes or "Amblypodia anita" not in notes:
        errors.append("preserved v1.5.0 butterfly release metadata changed or is missing")

    cut = q.get("release_cut") or {}
    if cut.get("tag") != "v1.5.0":
        errors.append("preserved v1.5 release tag contract changed")
    if cut.get("butterfly_name_selection") != "random-at-release-time":
        errors.append("preserved v1.5 naming policy changed")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("PASS preserved v1.5 qualification evidence: historical release boundary remains intact under the current stable v1 release.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
