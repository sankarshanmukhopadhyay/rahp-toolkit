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


def load_contract(root: pathlib.Path = ROOT) -> dict:
    path = root / "method" / "project-invariants.yaml"
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    if doc.get("contract") != "rahp-project-invariants-v1":
        raise ValueError("unexpected project invariant contract")
    return doc


def load_invariant(invariant_id: str, root: pathlib.Path = ROOT) -> dict:
    doc = load_contract(root)
    matches = [x for x in doc.get("invariants", []) if x.get("id") == invariant_id]
    if len(matches) != 1:
        raise ValueError(f"{invariant_id} must exist exactly once")
    return matches[0]


def check_core_dependency_boundary(inv: dict, root: pathlib.Path = ROOT) -> list[str]:
    errors: list[str] = []
    prohibited = [str(x).lower() for x in inv.get("prohibited_core_tokens", [])]
    for rel in inv.get("portable_core_files", []):
        path = root / rel
        if not path.is_file():
            errors.append(f"portable core file missing: {rel}")
            continue
        text = path.read_text(encoding="utf-8").lower()
        for token in prohibited:
            if token in text:
                errors.append(f"{rel}: portable core depends on deployment-specific token {token!r}")
    return errors


def check_fixtures(inv: dict, root: pathlib.Path = ROOT) -> list[str]:
    errors: list[str] = []
    profiles: list[dict] = []
    for rel in inv.get("portability_fixtures", []):
        path = root / rel
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
        errors.append(
            "portability fixtures must cover specification, protocol and implementation; "
            f"found {sorted(target_types)}"
        )
    return errors


def check_coverage(inv: dict, root: pathlib.Path = ROOT) -> list[str]:
    errors: list[str] = []
    targets = inv.get("required_target_classes") or {}
    pressures = inv.get("required_pressure_dimensions") or {}
    if set(targets) != {"specification", "protocol", "implementation", "composed-system"}:
        errors.append(
            "target-class invariant must cover specification, protocol, implementation and composed-system"
        )
    if set(pressures) != {
        "human-harms",
        "governance-failures",
        "adversarial-conditions",
        "resilience-risks",
    }:
        errors.append("pressure invariant must cover harms, governance, adversarial and resilience dimensions")
    for group_name, group in (("target", targets), ("pressure", pressures)):
        for name, evidence in group.items():
            rel = evidence.get("evidence")
            marker = str(evidence.get("marker") or "")
            path = root / str(rel)
            if not path.is_file():
                errors.append(f"{group_name} {name}: evidence file missing: {rel}")
                continue
            if marker not in path.read_text(encoding="utf-8"):
                errors.append(f"{group_name} {name}: marker {marker!r} missing from {rel}")
    return errors


def check_stripped_core(inv: dict, root: pathlib.Path = ROOT) -> list[str]:
    errors: list[str] = []
    with tempfile.TemporaryDirectory(prefix="rahp-portable-core-") as td:
        target = pathlib.Path(td) / "rahp"
        shutil.copytree(
            root,
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


def _consumer_independence_scan_paths(
    inv: dict, root: pathlib.Path = ROOT
) -> tuple[list[pathlib.Path], list[str]]:
    errors: list[str] = []
    extensions = {str(x).lower() for x in inv.get("scan_extensions", [])}
    excluded = {pathlib.PurePosixPath(str(x)).as_posix() for x in inv.get("excluded_paths", [])}
    paths: list[pathlib.Path] = []

    for rel in inv.get("portable_core_roots", []):
        base = root / rel
        if not base.is_dir():
            errors.append(f"consumer-independence core root missing: {rel}")
            continue
        for path in sorted(p for p in base.rglob("*") if p.is_file()):
            rel_path = path.relative_to(root).as_posix()
            if rel_path in excluded:
                continue
            if extensions and path.suffix.lower() not in extensions:
                continue
            paths.append(path)

    for rel in inv.get("portable_core_files", []):
        path = root / rel
        if not path.is_file():
            errors.append(f"consumer-independence core file missing: {rel}")
            continue
        if path.relative_to(root).as_posix() not in excluded:
            paths.append(path)

    return list(dict.fromkeys(paths)), errors


def check_consumer_independence(inv: dict, root: pathlib.Path = ROOT) -> list[str]:
    errors: list[str] = []
    prohibited = [str(x).lower() for x in inv.get("prohibited_consumer_tokens", [])]
    if not prohibited:
        return ["consumer-independence invariant declares no prohibited consumer tokens"]

    paths, path_errors = _consumer_independence_scan_paths(inv, root)
    errors.extend(path_errors)
    for path in paths:
        rel = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8").lower()
        except UnicodeDecodeError:
            errors.append(f"{rel}: declared consumer-independence surface is not UTF-8 text")
            continue
        for token in prohibited:
            if token in text:
                errors.append(f"{rel}: portable core contains consumer-specific token {token!r}")
    return errors


def check_consumer_independence_negative_fixture(
    inv: dict, root: pathlib.Path = ROOT
) -> list[str]:
    fixture = inv.get("negative_fixture") or {}
    source_rel = str(fixture.get("source") or "")
    inject_rel = str(fixture.get("inject_as") or "")
    expected_token = str(fixture.get("expected_token") or "").lower()
    if not source_rel or not inject_rel or not expected_token:
        return ["consumer-independence negative fixture is incomplete"]

    source = root / source_rel
    if not source.is_file():
        return [f"consumer-independence negative fixture missing: {source_rel}"]

    with tempfile.TemporaryDirectory(prefix="rahp-consumer-independence-negative-") as td:
        test_root = pathlib.Path(td) / "rahp"
        target = test_root / inject_rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

        synthetic_inv = dict(inv)
        synthetic_inv["portable_core_roots"] = [str(pathlib.PurePosixPath(inject_rel).parent)]
        synthetic_inv["portable_core_files"] = []
        synthetic_inv["excluded_paths"] = []

        detected = check_consumer_independence(synthetic_inv, test_root)
        expected_fragment = f"consumer-specific token {expected_token!r}"
        if not any(expected_fragment in error for error in detected):
            return [
                "consumer-independence negative fixture was not rejected; "
                f"expected detection of {expected_token!r}"
            ]
    return []


def main() -> int:
    try:
        portable = load_invariant("INV-PORTABLE-001")
        consumer_independence = load_invariant("INV-CONSUMER-INDEPENDENCE-001")
    except Exception as exc:
        print(f"ERROR project invariant contract: {exc}", file=sys.stderr)
        return 1

    errors: list[str] = []
    errors += check_core_dependency_boundary(portable)
    errors += check_fixtures(portable)
    errors += check_coverage(portable)
    errors += check_stripped_core(portable)
    errors += check_consumer_independence(consumer_independence)
    errors += check_consumer_independence_negative_fixture(consumer_independence)

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
    print("PASS INV-CONSUMER-INDEPENDENCE-001")
    print("  authoritative portable core surfaces contain no declared consumer dependency")
    print("  consumer-specific dependency injection is rejected by executable negative evidence")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
