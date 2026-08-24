#!/usr/bin/env python3
"""Measure stable RAHP execution profiles without publishing external work items."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import resource
import shlex
import subprocess
import sys
import time
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACT = ROOT / "method" / "execution-benchmarks.yaml"


def digest_file(path: Path) -> str | None:
    if not path.is_file():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_command(command: str) -> dict:
    started = time.perf_counter()
    proc = subprocess.run(
        shlex.split(command),
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=os.environ.copy(),
    )
    elapsed = time.perf_counter() - started
    return {
        "command": command,
        "seconds": round(elapsed, 6),
        "exit_code": proc.returncode,
        "output_sha256": hashlib.sha256(proc.stdout.encode("utf-8")).hexdigest(),
        "output_tail": proc.stdout[-4000:],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("profile", nargs="?", default="full-validation")
    parser.add_argument("--contract", default=str(DEFAULT_CONTRACT.relative_to(ROOT)))
    parser.add_argument("--output", default="build/execution-benchmark.json")
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args()

    contract_path = ROOT / args.contract
    contract = yaml.safe_load(contract_path.read_text(encoding="utf-8"))
    profiles = contract.get("profiles") or {}

    if args.list:
        for name, profile in profiles.items():
            print(f"{name}\t{profile.get('description', '')}")
        return 0

    if args.profile not in profiles:
        print(f"ERROR: unknown benchmark profile: {args.profile}", file=sys.stderr)
        return 2

    profile = profiles[args.profile]
    commands = profile.get("commands") or []
    started = time.perf_counter()
    results = []
    exit_code = 0
    for command in commands:
        result = run_command(command)
        results.append(result)
        print(f"{result['seconds']:9.3f}s  [{result['exit_code']}] {command}")
        if result["exit_code"] != 0:
            exit_code = result["exit_code"]
            break

    wall = time.perf_counter() - started
    peak_rss = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    output_path = ROOT / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "contract": contract.get("contract"),
        "profile": args.profile,
        "description": profile.get("description"),
        "wall_seconds": round(wall, 6),
        "profile_exit_code": exit_code,
        "peak_rss_kb": peak_rss,
        "commands": results,
        "semantic_reference_digests": {
            "current_baselines": digest_file(ROOT / "examples/current-baselines.yaml"),
            "tt_credspec_pressure_test": digest_file(ROOT / "examples/cross-spec/trust-tasks-credspec/pressure-test.yaml"),
            "scenario_corpus_registry": digest_file(ROOT / "corpora/sources.yaml"),
        },
    }
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"TOTAL {wall:.3f}s -> {output_path.relative_to(ROOT)}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
