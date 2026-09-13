#!/usr/bin/env python3
"""Route a RAHP lifecycle through the existing DRARM assessor when applicable."""
from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any, Callable

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from assessment_controller import (  # noqa: E402
    apply_resilience_applicability,
    new_lifecycle,
    resilience_applicability,
    set_resilience_disposition,
)

Runner = Callable[..., subprocess.CompletedProcess[str]]


def load_policy(profile: pathlib.Path) -> dict[str, Any]:
    value = yaml.safe_load(profile.read_text(encoding="utf-8")) or {}
    if not isinstance(value, dict):
        raise ValueError("resilience profile root must be a mapping")
    policy = value.get("applicability") or {}
    if not isinstance(policy, dict):
        raise ValueError("resilience profile applicability must be a mapping")
    return policy


def route_resilience(
    record: dict[str, Any],
    *,
    target_class: str,
    target_path: pathlib.Path | None,
    profile: pathlib.Path,
    repository: str | None = None,
    revision: str | None = None,
    runner: Runner = subprocess.run,
) -> tuple[dict[str, Any], dict[str, Any] | None]:
    policy = load_policy(profile)
    apply_resilience_applicability(
        record,
        target_class,
        policy,
        policy_source=str(profile),
    )
    decision = resilience_applicability(target_class, policy)["decision"]
    if decision != "required":
        return record, None
    if target_path is None:
        return record, None
    if not target_path.exists():
        raise ValueError(f"resilience target path does not exist: {target_path}")

    with tempfile.TemporaryDirectory(prefix="rahp-drarm-") as tmp:
        result_path = pathlib.Path(tmp) / "resilience.json"
        cmd = [
            sys.executable,
            str(ROOT / "tools" / "resilience_assess.py"),
            "--target",
            str(target_path),
            "--profile",
            str(profile),
            "--json",
            str(result_path),
        ]
        if repository:
            cmd += ["--repository", repository]
        if revision:
            cmd += ["--revision", revision]
        completed = runner(cmd, cwd=ROOT, text=True, capture_output=True)
        if completed.returncode != 0:
            return record, {
                "error": "drarm-execution-failed",
                "returncode": completed.returncode,
                "stderr": completed.stderr,
            }
        if not result_path.exists():
            return record, {"error": "drarm-result-missing"}
        result = json.loads(result_path.read_text(encoding="utf-8"))

    set_resilience_disposition(
        record,
        "executed",
        f"DRARM executed for required target class {target_class!r}",
        {
            "source": str(profile),
            "target_class": target_class,
            "decision": "required",
            "repository": repository,
            "revision": revision,
        },
    )
    return record, result


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--assessment-id", required=True)
    ap.add_argument("--target-class", required=True)
    ap.add_argument("--path", type=pathlib.Path)
    ap.add_argument(
        "--profile",
        type=pathlib.Path,
        default=ROOT / "profiles" / "resilience" / "default.yaml",
    )
    ap.add_argument("--repository")
    ap.add_argument("--revision")
    args = ap.parse_args()
    record = new_lifecycle(args.assessment_id)
    record, result = route_resilience(
        record,
        target_class=args.target_class,
        target_path=args.path,
        profile=args.profile,
        repository=args.repository,
        revision=args.revision,
    )
    print(json.dumps({"lifecycle": record, "drarm": result}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
