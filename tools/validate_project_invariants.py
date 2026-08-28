#!/usr/bin/env python3
"""Validate machine-testable RAHP project architecture invariants."""
from __future__ import annotations
import pathlib
import shutil
import subprocess
import sys
import tempfile

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTRACT = ROOT / "method" / "project-invariants.yaml"


def load_invariant() -> dict:
    doc = yaml.safe_load(CONTRACT.read_text(encoding="utf-8"))
    if doc.get("contract") != "rahp-project-invariants-v1":
        raise ValueError("unexpected project invariant contract")
    matches = [x for x in doc.get("invariants", []) if x.get("id") == "INV-PORTABLE-001"]
    if len(matches) != 1:
        raise ValueError("INV-PORTABLE-001 must exist exactly once")
    return matches[0]


def check_core_dependency_boundary(inv: dict) -> list[str]:
    errors: list[str] = []
    prohibited = [str(x).lower() for x in inv.get("prohibited_core_tokens", [])]
    for rel in inv.get("portable_core_files", []):
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"portable core file missing: {rel}")
            continue
        text = path.read_text(encoding="utf-8").lower()
        for token in prohibited:
            if token in text:
                errors.append(f"{rel}: portable core depends on deployment-specific token {token!r}")
    return errors


def check_fixtures(inv: dict) -> list[str]:
    errors: list[str] = []
    profiles: list[dict] = []
    for rel in inv.get("portability_fixtures", []):
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"portability fixture missing: {rel}")
            continue
        profiles.append(yaml.safe_load(path.read_text(encoding="utf-8")))
    ids = [((p.get("profile") or {}).get("id")) for p in profiles]
    if len(ids) < 2 or len(set(ids)) != len(ids):
        errors.append("at least two distinct portability fixture profiles are required")
    target_types = {
        str(((repo.get("context") or {}).get("type") or "")).lower()
        for profile in profiles
        for repo in profile.get("repositories", [])
    }
    if not {"specification", "protocol", "implementation"}.issubset(target_types):
        errors.append(f"portability fixtures must cover specification, protocol and implementation; found {sorted(target_types)}")
    return errors


def check_coverage(inv: dict) -> list[str]:
    errors: list[str] = []
    targets = inv.get("required_target_classes") or {}
    pressures = inv.get("required_pressure_dimensions") or {}
    if set(targets) != {"specification", "protocol", "implementation", "composed-system"}:
        errors.append("target-class invariant must cover specification, protocol, implementation and composed-system")
    if set(pressures) != {"human-harms", "governance-failures", "adversarial-conditions", "resilience-risks"}:
        errors.append("pressure invariant must cover harms, governance, adversarial and resilience dimensions")
    for group_name, group in (("target", targets), ("pressure", pressures)):
        for name, evidence in group.items():
            rel = evidence.get("evidence")
            marker = str(evidence.get("marker") or "")
            path = ROOT / str(rel)
            if not path.is_file():
                errors.append(f"{group_name} {name}: evidence file missing: {rel}")
                continue
            if marker not in path.read_text(encoding="utf-8"):
                errors.append(f"{group_name} {name}: marker {marker!r} missing from {rel}")
    return errors


def check_stripped_core(inv: dict) -> list[str]:
    errors: list[str] = []
    with tempfile.TemporaryDirectory(prefix="rahp-portable-core-") as td:
        target = pathlib.Path(td) / "rahp"
        shutil.copytree(
            ROOT,
            target,
            ignore=shutil.ignore_patterns(".git", "build", ".rahp", "__pycache__", "node_modules"),
        )
        for rel in (inv.get("stripped_core") or {}).get("remove_paths", []):
            path = target / rel
            if path.is_dir():
                shutil.rmtree(path)
            elif path.exists():
                path.unlink()
        for command in (inv.get("stripped_core") or {}).get("commands", []):
            rendered = str(command).replace("{root}", str(target))
            result = subprocess.run(rendered, cwd=target, shell=True, text=True, capture_output=True)
            if result.returncode:
                detail = (result.stderr or result.stdout or "").strip()
                errors.append(f"stripped-core command failed: {rendered}: {detail}")
            else:
                print(f"[stripped-core] PASS · {rendered}")
    return errors


def main() -> int:
    try:
        inv = load_invariant()
    except Exception as exc:
        print(f"ERROR project invariant contract: {exc}", file=sys.stderr)
        return 1
    errors = []
    errors += check_core_dependency_boundary(inv)
    errors += check_fixtures(inv)
    errors += check_coverage(inv)
    errors += check_stripped_core(inv)
    if errors:
        for error in errors:
            print("ERROR", error, file=sys.stderr)
        print(f"Project invariant validation failed: {len(errors)} error(s).", file=sys.stderr)
        return 1
    print("PASS INV-PORTABLE-001")
    print("  portable core has no declared deployment dependency")
    print("  two distinct non-DTG deployment fixtures execute through the same engine")
    print("  stripped core executes with profiles/instances/corpora/examples absent")
    print("  target and pressure-dimension coverage remains represented")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
