#!/usr/bin/env python3
"""Validate the maintained newcomer adoption path.

The goal is deliberately small: prove that the canonical adoption entry points
exist, the RAHP-only onboarding configuration remains valid, and its dry-run can
resolve a source-pinned review without requiring DPIP or the Interop Lab.
"""
from __future__ import annotations

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

REQUIRED = [
    ROOT / "docs" / "adoption-guide.md",
    ROOT / "ADOPTION.md",
    ROOT / "examples" / "hello-rahp" / "README.md",
    ROOT / "examples" / "hello-rahp" / "rahp.yaml",
    ROOT / "examples" / "hello-rahp" / "subject" / "spec.md",
    ROOT / "examples" / "composed-assurance" / "README.md",
    ROOT / "schemas" / "rahp-assessor-result-v1.schema.json",
    ROOT / "schemas" / "rahp-assurance-obligation-v1.schema.json",
    ROOT / "schemas" / "rahp-evidence-producer-result-v1.schema.json",
]


def run(*args: str) -> None:
    proc = subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if proc.returncode:
        sys.stderr.write(proc.stdout)
        sys.stderr.write(proc.stderr)
        raise SystemExit(proc.returncode)


def main() -> int:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED if not path.exists()]
    if missing:
        for path in missing:
            print(f"ERROR missing adoption artifact: {path}")
        return 1

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    gateway = (ROOT / "docs" / "adoption-guide.md").read_text(encoding="utf-8")
    hello = (ROOT / "examples" / "hello-rahp" / "README.md").read_text(encoding="utf-8")

    checks = {
        "README routes to adoption gateway": "docs/adoption-guide.md" in readme,
        "gateway states RAHP-only start": "You can start with RAHP alone" in gateway,
        "gateway names orchestrator role": "Assurance orchestrator" in gateway,
        "gateway names specialist role": "Specialist assessor" in gateway,
        "gateway names evidence-producer role": "Evidence producer" in gateway,
        "gateway references assessor contract": "rahp-assessor-result/v1" in gateway,
        "gateway references obligation contract": "rahp-assurance-obligation/v1" in gateway,
        "gateway references evidence result": "rahp-evidence-producer-result/v1" in gateway,
        "hello declares no cross-repo prerequisite": "DPIP and the Trust Protocol Interop Lab are not required" in hello,
    }
    failed = [name for name, ok in checks.items() if not ok]
    if failed:
        for name in failed:
            print(f"ERROR adoption invariant failed: {name}")
        return 1

    cfg = "examples/hello-rahp/rahp.yaml"
    run("tools/rahp.py", "config-validate", "--config", cfg)
    run("tools/rahp.py", "targets", "--config", cfg)
    run(
        "tools/rahp.py",
        "review",
        "--config",
        cfg,
        "--target",
        "hello-spec",
        "--mode",
        "rahp",
        "--offline",
        "--dry-run",
    )

    print("PASS adoption path: gateway present; RAHP-only configuration and dry-run are executable")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
