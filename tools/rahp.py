#!/usr/bin/env python3
"""Configuration-driven RAHP v0.8 command line interface.

The YAML configuration is the portability boundary. A profile lists one or more
repositories, assessment context and permitted review modes. The engine does not
require DTG corpora, issues, governance records or portfolio-monitor metadata.

This command prepares/scaffolds assessment work. It does not invent substantive
findings: a human or AI-assisted reviewer must inspect the target material and
populate the canonical review records.
"""
from __future__ import annotations
import argparse
import json
import datetime as dt
import pathlib
import re
import shutil
import subprocess
import sys
from typing import Any

try:
    import yaml
    import jsonschema
except ImportError:
    sys.exit("rahp.py requires PyYAML and jsonschema: pip install -r requirements.txt")

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "method" / "schema" / "rahp-config.schema.json"


def load_yaml(path: pathlib.Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"configuration not found: {path}")
    with path.open(encoding="utf-8") as fh:
        value = yaml.safe_load(fh) or {}
    if not isinstance(value, dict):
        raise SystemExit("configuration root must be a YAML mapping")
    return value


def validate_config(path: pathlib.Path) -> dict[str, Any]:
    import json
    cfg = load_yaml(path)
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    try:
        jsonschema.Draft202012Validator(schema).validate(cfg)
    except jsonschema.ValidationError as exc:
        loc = ".".join(str(x) for x in exc.absolute_path) or "<root>"
        raise SystemExit(f"invalid RAHP configuration at {loc}: {exc.message}")
    ids = [r["id"] for r in cfg["repositories"]]
    duplicates = sorted({x for x in ids if ids.count(x) > 1})
    if duplicates:
        raise SystemExit("repository ids must be unique: " + ", ".join(duplicates))
    return cfg


def target(cfg: dict[str, Any], target_id: str) -> dict[str, Any]:
    for item in cfg["repositories"]:
        if item["id"] == target_id:
            return item
    known = ", ".join(r["id"] for r in cfg["repositories"])
    raise SystemExit(f"unknown target {target_id!r}; configured targets: {known}")


def title_for(item: dict[str, Any]) -> str:
    return (item.get("context") or {}).get("title") or item["id"].replace("-", " ").title()


def repo_url(repository: str) -> str:
    if re.match(r"^(?:https?|ssh|git)://", repository) or repository.startswith("git@"):
        return repository
    if repository.endswith(".git") and "/" in repository:
        return repository
    if re.fullmatch(r"[^/\s]+/[^/\s]+", repository):
        return f"https://github.com/{repository}.git"
    return repository


def resolve_commit(item: dict[str, Any], offline: bool = False) -> str | None:
    if item.get("commit"):
        return item["commit"]
    lp = item.get("local_path")
    if lp:
        p = pathlib.Path(lp)
        if not p.is_absolute():
            p = ROOT / p
        if (p / ".git").exists():
            run = subprocess.run(["git", "-C", str(p), "rev-parse", "HEAD"], text=True, capture_output=True)
            if run.returncode == 0:
                return run.stdout.strip()
    if offline:
        return None
    branch = item.get("branch", "main")
    run = subprocess.run(["git", "ls-remote", repo_url(item["repository"]), f"refs/heads/{branch}"], text=True, capture_output=True)
    if run.returncode == 0 and run.stdout.strip():
        return run.stdout.split()[0]
    raise SystemExit(f"cannot resolve {item['repository']} branch {branch}; pin commit or use --offline with a pinned/local target")


def cmd_config_validate(a: argparse.Namespace) -> None:
    cfg = validate_config(a.config)
    print(f"RAHP configuration valid: {a.config}")
    print(f"  profile: {cfg['profile']['id']} ({cfg['profile']['title']})")
    print(f"  repositories: {len(cfg['repositories'])}")


def cmd_targets(a: argparse.Namespace) -> None:
    cfg = validate_config(a.config)
    default = (cfg.get("assessment") or {}).get("default_mode", "combined")
    print(f"Profile: {cfg['profile']['title']} [{cfg['profile']['id']}]")
    print(f"Default mode: {default}")
    print("Targets:")
    for r in cfg["repositories"]:
        reviews = ",".join(r.get("reviews") or [default])
        print(f"  {r['id']}: {r['repository']} @ {r.get('branch','main')} [{reviews}]")


def cmd_prepare(a: argparse.Namespace) -> None:
    cfg = validate_config(a.config)
    chosen = cfg["repositories"] if a.all else [target(cfg, a.target)]
    base = pathlib.Path(a.directory or (cfg.get("output") or {}).get("directory") or "build/targets")
    if not base.is_absolute():
        base = ROOT / base
    base.mkdir(parents=True, exist_ok=True)
    for item in chosen:
        dst = base / item["id"]
        lp = item.get("local_path")
        if lp:
            src = pathlib.Path(lp)
            if not src.is_absolute(): src = ROOT / src
            if not src.exists(): raise SystemExit(f"local target path not found: {src}")
            print(f"[prepare] {item['id']}: using local path {src}")
            continue
        if a.offline:
            print(f"[prepare] {item['id']}: offline; remote checkout skipped")
            continue
        if dst.exists():
            if a.force: shutil.rmtree(dst)
            else: raise SystemExit(f"target checkout exists: {dst.relative_to(ROOT)} (use --force)")
        branch = item.get("branch", "main")
        subprocess.run(["git", "clone", "--depth", "1", "--branch", branch, repo_url(item["repository"]), str(dst)], check=True)
        if item.get("commit"):
            subprocess.run(["git", "-C", str(dst), "fetch", "--depth", "1", "origin", item["commit"]], check=True)
            subprocess.run(["git", "-C", str(dst), "checkout", item["commit"]], check=True)
        print(f"[prepare] {item['id']}: {dst.relative_to(ROOT)}")


def scaffold_one(cfg: dict[str, Any], item: dict[str, Any], mode: str, a: argparse.Namespace) -> None:
    allowed = item.get("reviews") or [(cfg.get("assessment") or {}).get("default_mode", "combined")]
    if mode not in allowed:
        raise SystemExit(f"target {item['id']} does not permit {mode!r}; configured modes: {', '.join(allowed)}")
    commit = resolve_commit(item, offline=a.offline)
    if not commit:
        raise SystemExit(f"target {item['id']} has no resolvable commit; pin `commit`, provide a git `local_path`, or run online")
    assessment = cfg.get("assessment") or {}
    version = item.get("version") or item.get("branch") or "configured"
    cmd = [sys.executable, str(ROOT / "tools" / "review.py"), "init",
           "--mode", mode, "--slug", item["id"], "--title", title_for(item),
           "--repository", item["repository"], "--version", version, "--commit", commit,
           "--reviewed-on", a.reviewed_on,
           "--rahp-repository", assessment.get("rahp_repository", "sankarshanmukhopadhyay/rahp-toolkit"),
           "--rahp-version", assessment.get("rahp_version", "v0.9.0"), "--storage", "working"]
    if item.get("document"): cmd += ["--document", item["document"]]
    for path in (item.get("scope") or {}).get("include", []): cmd += ["--source-path", path]
    if a.force: cmd.append("--force")
    if a.dry_run:
        print("[dry-run] " + " ".join(cmd))
        return
    subprocess.run(cmd, cwd=ROOT, check=True)


def cmd_review(a: argparse.Namespace) -> None:
    cfg = validate_config(a.config)
    mode = a.mode or (cfg.get("assessment") or {}).get("default_mode", "combined")
    chosen = cfg["repositories"] if a.all else [target(cfg, a.target)]
    for item in chosen:
        scaffold_one(cfg, item, mode, a)
    print("\nConfigured review scaffold(s) created. Inspect target material and populate findings before rendering/validation.")



def cmd_assess(a: argparse.Namespace) -> None:
    """Initialize an engine-owned assessment mode contract.

    This command does not perform substantive semantic judgment. It resolves the
    portable lifecycle/isolation boundary that execution workflows must obey.
    """
    if a.mode == "clean-room":
        if not a.run_spec:
            raise SystemExit("--run-spec is required for clean-room mode")
        cmd = [
            sys.executable, str(ROOT / "tools" / "clean_room.py"),
            "--spec", str(a.run_spec),
            "--nonce", a.nonce,
        ]
        if a.instance:
            cmd += ["--instance", a.instance]
        if a.snapshot:
            cmd += ["--snapshot", a.snapshot]
        subprocess.run(cmd, cwd=ROOT, check=True)
        return

    from assessment_controller import new_lifecycle
    assessment_id = a.assessment_id or f"{a.instance or 'portable'}:{a.snapshot or 'current'}"
    print(json.dumps(new_lifecycle(assessment_id, "steady-state"), indent=2))


def cmd_resilience(a: argparse.Namespace) -> None:
    profile = a.profile or (ROOT / "profiles" / "resilience" / "default.yaml")
    cmd = [sys.executable, str(ROOT / "tools" / "resilience_assess.py"),
           "--target", str(a.path), "--profile", str(profile)]
    if a.repository: cmd += ["--repository", a.repository]
    if a.revision: cmd += ["--revision", a.revision]
    if a.json: cmd += ["--json", str(a.json)]
    if a.markdown: cmd += ["--markdown", str(a.markdown)]
    if a.events: cmd += ["--events", str(a.events)]
    subprocess.run(cmd, cwd=ROOT, check=True)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="command", required=True)
    cv = sub.add_parser("config-validate", help="validate a RAHP YAML configuration")
    cv.add_argument("--config", type=pathlib.Path, required=True); cv.set_defaults(func=cmd_config_validate)
    ts = sub.add_parser("targets", help="list configured repository targets")
    ts.add_argument("--config", type=pathlib.Path, required=True); ts.set_defaults(func=cmd_targets)
    pp = sub.add_parser("prepare", help="checkout or resolve configured target repositories")
    pp.add_argument("--config", type=pathlib.Path, required=True); pp.add_argument("--target"); pp.add_argument("--all", action="store_true")
    pp.add_argument("--directory"); pp.add_argument("--offline", action="store_true"); pp.add_argument("--force", action="store_true"); pp.set_defaults(func=cmd_prepare)
    rv = sub.add_parser("review", help="scaffold configured RAHP/security/combined reviews")
    rv.add_argument("--config", type=pathlib.Path, required=True); rv.add_argument("--target"); rv.add_argument("--all", action="store_true")
    rv.add_argument("--mode", choices=["rahp","security","combined"]); rv.add_argument("--offline", action="store_true"); rv.add_argument("--force", action="store_true")
    rv.add_argument("--reviewed-on", default=dt.date.today().isoformat()); rv.add_argument("--dry-run", action="store_true", help="resolve configuration and show review scaffolding commands without writing files"); rv.set_defaults(func=cmd_review)
    ass = sub.add_parser("assess", help="initialize portable steady-state or clean-room assessment semantics")
    ass.add_argument("--mode", choices=["steady-state", "clean-room"], required=True)
    ass.add_argument("--instance")
    ass.add_argument("--snapshot")
    ass.add_argument("--assessment-id")
    ass.add_argument("--run-spec", type=pathlib.Path)
    ass.add_argument("--nonce", default="local")
    ass.set_defaults(func=cmd_assess)
    dr = sub.add_parser("resilience", help="run the portable Distributed Resilience and Amplification Risk Model")
    dr.add_argument("--path", type=pathlib.Path, required=True, help="checked-out repository or extracted target directory")
    dr.add_argument("--profile", type=pathlib.Path, help="DRARM profile; defaults to profiles/resilience/default.yaml")
    dr.add_argument("--repository"); dr.add_argument("--revision")
    dr.add_argument("--json", type=pathlib.Path); dr.add_argument("--markdown", type=pathlib.Path); dr.add_argument("--events", type=pathlib.Path)
    dr.set_defaults(func=cmd_resilience)
    a = ap.parse_args()
    if hasattr(a, "all") and not a.all and not a.target:
        ap.error("specify --target ID or --all")
    a.func(a)

if __name__ == "__main__":
    main()
