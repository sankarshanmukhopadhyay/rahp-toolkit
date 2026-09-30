#!/usr/bin/env python3
"""Profile a RAHP benchmark profile and emit attributable performance evidence."""
from __future__ import annotations
import argparse, hashlib, io, json, math, os, pstats, resource, shlex, subprocess, sys, time
from pathlib import Path
from typing import Any
import yaml

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACT = ROOT / "method" / "execution-benchmarks.yaml"

def load_contract(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(value, dict):
        raise ValueError("benchmark contract must contain a mapping")
    return value

def classify_runtime(wall_seconds: float, cpu_seconds: float) -> str:
    if wall_seconds <= 0 or not math.isfinite(wall_seconds) or cpu_seconds < 0 or not math.isfinite(cpu_seconds):
        return "indeterminate"
    ratio = cpu_seconds / wall_seconds
    if ratio >= 0.80:
        return "cpu-dominant"
    if ratio <= 0.40:
        return "wait-or-process-dominant"
    return "mixed"

def _child_cpu_seconds() -> float:
    usage = resource.getrusage(resource.RUSAGE_CHILDREN)
    return usage.ru_utime + usage.ru_stime

def profile_command(command: str, index: int, profile_dir: Path) -> dict[str, Any]:
    argv = shlex.split(command)
    if not argv or argv[0] not in {"python", "python3"} or len(argv) < 2:
        raise ValueError(f"profiling requires a Python command: {command}")
    profile_dir.mkdir(parents=True, exist_ok=True)
    stats_path = profile_dir / f"command-{index:02d}.pstats"
    stdout_path = profile_dir / f"command-{index:02d}.stdout.txt"
    profile_argv = [sys.executable, "-m", "cProfile", "-o", str(stats_path), *argv[1:]]
    cpu_started = _child_cpu_seconds()
    started = time.perf_counter()
    proc = subprocess.run(profile_argv, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=os.environ.copy())
    wall = time.perf_counter() - started
    cpu = max(0.0, _child_cpu_seconds() - cpu_started)
    stdout_path.write_text(proc.stdout, encoding="utf-8")
    top = ""
    total_profile_seconds = 0.0
    if stats_path.is_file():
        stream = io.StringIO()
        stats = pstats.Stats(str(stats_path), stream=stream)
        total_profile_seconds = float(stats.total_tt)
        stats.strip_dirs().sort_stats("cumulative").print_stats(20)
        top = stream.getvalue()
    return {
        "index": index, "command": command, "wall_seconds": round(wall, 6),
        "cpu_seconds": round(cpu, 6),
        "cpu_wall_ratio": round(cpu / wall, 4) if wall > 0 else None,
        "classification": classify_runtime(wall, cpu),
        "profiled_python_seconds": round(total_profile_seconds, 6),
        "exit_code": proc.returncode,
        "stdout_sha256": hashlib.sha256(proc.stdout.encode("utf-8")).hexdigest(),
        "stats_file": str(stats_path.relative_to(ROOT)),
        "stdout_file": str(stdout_path.relative_to(ROOT)),
        "top_cumulative": top,
    }

def build_budget(results: list[dict[str, Any]]) -> dict[str, Any]:
    if not results:
        raise ValueError("profiling produced no command results")
    total_wall = sum(float(item["wall_seconds"]) for item in results)
    total_cpu = sum(float(item["cpu_seconds"]) for item in results)
    for item in results:
        item["wall_share_percent"] = round((float(item["wall_seconds"]) / total_wall * 100.0) if total_wall else 0.0, 3)
    dominant = sorted(results, key=lambda item: float(item["wall_seconds"]), reverse=True)
    return {
        "wall_seconds": round(total_wall, 6), "cpu_seconds": round(total_cpu, 6),
        "cpu_wall_ratio": round(total_cpu / total_wall, 4) if total_wall else None,
        "classification": classify_runtime(total_wall, total_cpu),
        "largest_wall_time_commands": [
            {"command": item["command"], "wall_seconds": item["wall_seconds"],
             "wall_share_percent": item["wall_share_percent"], "classification": item["classification"]}
            for item in dominant[:5]
        ],
    }

def render_markdown(payload: dict[str, Any]) -> str:
    budget = payload["runtime_budget"]
    lines = [
        f"# RAHP runtime profile: {payload['profile']}", "", "## Context", "",
        f"- Contract: `{payload.get('contract')}`",
        f"- Revision: `{payload.get('revision', 'unknown')}`",
        f"- Workload dimensions: `{json.dumps(payload.get('workload_dimensions') or {}, sort_keys=True)}`",
        "", "## Runtime budget", "",
        f"- Wall time: **{budget['wall_seconds']:.3f}s**",
        f"- Child CPU time: **{budget['cpu_seconds']:.3f}s**",
        f"- CPU/wall ratio: **{budget.get('cpu_wall_ratio')}**",
        f"- Classification: **{budget['classification']}**", "",
        "| Wall s | CPU s | Share | Classification | Command |",
        "|---:|---:|---:|---|---|",
    ]
    for item in payload["commands"]:
        lines.append(f"| {item['wall_seconds']:.3f} | {item['cpu_seconds']:.3f} | {item['wall_share_percent']:.1f}% | {item['classification']} | `{item['command']}` |")
    lines += ["", "## Interpretation boundary", "",
        "The classification is an observation derived from process wall and child CPU time. It does not by itself prove which semantic function should be optimized. Raw cProfile statistics are retained for command-level attribution.",
        "", "Performance evidence is non-authoritative for RAHP assurance outcomes."]
    return "\n".join(lines) + "\n"

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile")
    parser.add_argument("--contract", type=Path, default=Path("method/execution-benchmarks.yaml"))
    parser.add_argument("--output-dir", type=Path, default=Path("build/performance-profile"))
    args = parser.parse_args()
    contract = load_contract(ROOT / args.contract)
    profiles = contract.get("profiles") or {}
    if args.profile not in profiles:
        parser.error(f"unknown benchmark profile: {args.profile}")
    profile = profiles[args.profile]
    commands = profile.get("commands") or []
    if not commands:
        parser.error("selected profile has no commands")
    revision = os.environ.get("GITHUB_SHA") or subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True).stdout.strip()
    output_dir = ROOT / args.output_dir
    profile_dir = output_dir / "raw"
    results, exit_code = [], 0
    for index, command in enumerate(commands, 1):
        result = profile_command(str(command), index, profile_dir)
        results.append(result)
        if result["exit_code"] != 0:
            exit_code = result["exit_code"]
            break
    payload = {
        "schema": "rahp-runtime-profile/v1", "contract": contract.get("contract"),
        "profile": args.profile, "revision": revision,
        "workload_dimensions": profile.get("workload_dimensions") or {},
        "runtime_budget": build_budget(results), "commands": results,
        "authority_boundary": {"assurance_evidence": False, "may_set_assurance_outcome": False, "purpose": "performance-engineering"},
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "profile.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (output_dir / "report.md").write_text(render_markdown(payload), encoding="utf-8")
    print(render_markdown(payload))
    return exit_code

if __name__ == "__main__":
    raise SystemExit(main())
