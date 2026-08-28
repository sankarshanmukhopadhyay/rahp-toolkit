#!/usr/bin/env python3
"""Validate configuration-driven portability without bundled deployment state."""
from __future__ import annotations
import argparse
import pathlib
import subprocess
import sys

DEFAULT_ROOT = pathlib.Path(__file__).resolve().parent.parent
FORBIDDEN = ["trustoverip", "portfolio-monitor", "corpus-dtg", "rp-001", "dtgwg-", "profiles/dtg", "instances/dtg"]


def run(root: pathlib.Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(root / "tools" / "rahp.py"), *args], cwd=root, text=True, capture_output=True)


def validate_fixture(root: pathlib.Path, rel: str, target: str, modes: tuple[str, ...]) -> list[str]:
    errors: list[str] = []
    config = root / rel
    if not config.exists():
        return [f"missing portability fixture: {rel}"]
    text = config.read_text(encoding="utf-8").lower()
    leaked = [x for x in FORBIDDEN if x in text]
    if leaked:
        errors.append(f"{rel}: deployment-specific coupling: {', '.join(leaked)}")
        return errors
    checks = [
        ("configuration schema", run(root, "config-validate", "--config", str(config))),
        ("target discovery", run(root, "targets", "--config", str(config))),
    ]
    checks.extend(
        (f"{mode} mode", run(root, "review", "--config", str(config), "--target", target, "--mode", mode, "--offline", "--dry-run"))
        for mode in modes
    )
    for label, result in checks:
        if result.returncode:
            detail = (result.stderr or result.stdout or "").strip()
            errors.append(f"{rel} [{label}] failed: {detail}")
        else:
            print(f"[{rel} · {label}] PASS")
    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=pathlib.Path, default=DEFAULT_ROOT, help="repository root to qualify")
    args = ap.parse_args()
    root = args.root.resolve()
    required = [root / "method" / "schema" / "rahp-config.schema.json", root / "tools" / "rahp.py"]
    errors = [f"missing portable core asset: {p.relative_to(root)}" for p in required if not p.exists()]
    errors += validate_fixture(root, "tests/fixtures/portable-project/rahp.yaml", "alpha-spec", ("rahp", "security", "combined"))
    errors += validate_fixture(root, "tests/fixtures/portable-implementation/rahp.yaml", "gamma-runtime", ("rahp", "security", "combined"))
    if errors:
        for error in errors:
            print("ERROR", error, file=sys.stderr)
        print(f"Portability validation: FAIL ({len(errors)} error(s))", file=sys.stderr)
        return 1
    print("Portability validation: PASS")
    print("  standards/protocol and implementation deployments use the same portable engine")
    print("  no bundled profile, corpus, instance or portfolio-governance state is required")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
