#!/usr/bin/env python3
"""Measure stable RAHP execution profiles without publishing external work items."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import resource
import shlex
import statistics
import subprocess
import sys
import time
from pathlib import Path

import yaml

try:
    from .execution_telemetry import build_event
except ImportError:  # script execution
    from execution_telemetry import build_event

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACT = ROOT / "method" / "execution-benchmarks.yaml"


def digest_file(path: Path) -> str | None:
    if not path.is_file():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _child_cpu_seconds() -> float:
    usage = resource.getrusage(resource.RUSAGE_CHILDREN)
    return usage.ru_utime + usage.ru_stime


def run_command(command: str) -> dict:
    cpu_started = _child_cpu_seconds()
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
    cpu_elapsed = max(0.0, _child_cpu_seconds() - cpu_started)
    return {
        "command": command,
        "seconds": round(elapsed, 6),
        "cpu_seconds": round(cpu_elapsed, 6),
        "exit_code": proc.returncode,
        "output_sha256": hashlib.sha256(proc.stdout.encode("utf-8")).hexdigest(),
        "output_tail": proc.stdout[-4000:],
    }


def run_sample(commands: list[str]) -> dict:
    started = time.perf_counter()
    results = []
    exit_code = 0
    for command in commands:
        result = run_command(command)
        results.append(result)
        print(
            f"{result['seconds']:9.3f}s wall "
            f"{result['cpu_seconds']:9.3f}s cpu "
            f"[{result['exit_code']}] {command}"
        )
        if result["exit_code"] != 0:
            exit_code = result["exit_code"]
            break
    wall = time.perf_counter() - started
    return {
        "wall_seconds": round(wall, 6),
        "cpu_seconds": round(sum(item["cpu_seconds"] for item in results), 6),
        "profile_exit_code": exit_code,
        "commands": results,
    }


def validate_sample_count(value: int) -> int:
    if value < 1:
        raise ValueError("samples must be at least 1")
    return value


def summarize_samples(samples: list[dict]) -> dict:
    if not samples:
        raise ValueError("at least one benchmark sample is required")

    wall_values = [float(sample["wall_seconds"]) for sample in samples]
    cpu_values = [float(sample["cpu_seconds"]) for sample in samples]
    if any(not math.isfinite(value) or value < 0 for value in wall_values + cpu_values):
        raise ValueError("benchmark sample timings must be finite and non-negative")

    return {
        "sample_count": len(samples),
        "wall_seconds": {
            "min": round(min(wall_values), 6),
            "median": round(statistics.median(wall_values), 6),
            "mean": round(statistics.fmean(wall_values), 6),
            "max": round(max(wall_values), 6),
        },
        "cpu_seconds": {
            "min": round(min(cpu_values), 6),
            "median": round(statistics.median(cpu_values), 6),
            "mean": round(statistics.fmean(cpu_values), 6),
            "max": round(max(cpu_values), 6),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("profile", nargs="?", default="full-validation")
    parser.add_argument("--contract", default=str(DEFAULT_CONTRACT.relative_to(ROOT)))
    parser.add_argument("--output", default="build/execution-benchmark.json")
    parser.add_argument(
        "--samples",
        type=int,
        default=1,
        help="number of repeated profile executions; defaults to 1 for compatibility",
    )
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args()

    try:
        sample_count = validate_sample_count(args.samples)
    except ValueError as exc:
        parser.error(str(exc))

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
    samples = []
    exit_code = 0

    for sample_index in range(sample_count):
        if sample_count > 1:
            print(f"SAMPLE {sample_index + 1}/{sample_count}")
        sample = run_sample(commands)
        samples.append(sample)
        if sample["profile_exit_code"] != 0:
            exit_code = sample["profile_exit_code"]
            break

    summary = summarize_samples(samples)
    peak_rss = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    output_path = ROOT / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)

    representative = samples[0]
    payload = {
        "contract": contract.get("contract"),
        "profile": args.profile,
        "description": profile.get("description"),
        # Keep these established top-level fields for existing consumers. For
        # repeated runs wall_seconds is the median, while commands remains the
        # first complete sample for backwards-compatible command detail.
        "wall_seconds": summary["wall_seconds"]["median"],
        "cpu_seconds": summary["cpu_seconds"]["median"],
        "profile_exit_code": exit_code,
        "peak_rss_kb": peak_rss,
        "commands": representative["commands"],
        "sample_count": len(samples),
        "samples": samples,
        "summary": summary,
        "telemetry": build_event(
            operation="execution-benchmark",
            run_id=args.profile,
            duration_seconds=summary["wall_seconds"]["median"],
            context={"profile_id": args.profile, "mode": "benchmark"},
            metrics={
                "command_count": len(representative["commands"]),
                "failed_command_count": sum(
                    1
                    for sample in samples
                    for item in sample["commands"]
                    if item["exit_code"] != 0
                ),
                "peak_rss_kb": int(peak_rss),
                "sample_count": len(samples),
                "median_cpu_seconds": summary["cpu_seconds"]["median"],
            },
        ),
        "semantic_reference_digests": {
            "current_baselines": digest_file(ROOT / "examples/current-baselines.yaml"),
            "tt_credspec_pressure_test": digest_file(ROOT / "examples/cross-spec/trust-tasks-credspec/pressure-test.yaml"),
            "scenario_corpus_registry": digest_file(ROOT / "corpora/sources.yaml"),
        },
    }
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        f"TOTAL median={summary['wall_seconds']['median']:.3f}s "
        f"cpu={summary['cpu_seconds']['median']:.3f}s "
        f"samples={len(samples)} -> {output_path.relative_to(ROOT)}"
    )
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
