#!/usr/bin/env python3
"""Monitor repository-head deltas for a normal RAHP deployment profile.

Operational contract:
- Generic deployment monitor used by non-DTG instances such as CAWG/C2PA.
- Reads a profile plus persisted repository state, compares repository heads/material
  paths, and emits assessment-required review events for qualifying changes.
- It is stateful and incremental: unchanged state correctly emits no new work.
- It does not perform the resulting assessment and does not equate monitor success with
  assurance success.
"""
from __future__ import annotations
import argparse, fnmatch, json, os, pathlib, urllib.error, urllib.request
from datetime import datetime, timezone
from typing import Any
import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent


def load_yaml(path: pathlib.Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def api_json(url: str) -> Any:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "rahp-instance-monitor/0.6"}
    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)


def head_sha(repo: str, branch: str) -> str | None:
    """Resolve a target branch head; return None for an empty GitHub repository."""
    try:
        return api_json(f"https://api.github.com/repos/{repo}/commits/{branch}")["sha"]
    except urllib.error.HTTPError as exc:
        if exc.code == 409:
            return None
        raise


def compare(repo: str, base: str, head: str) -> dict[str, Any]:
    return api_json(f"https://api.github.com/repos/{repo}/compare/{base}...{head}")


def target_role(target: dict[str, Any]) -> str | None:
    return (target.get("context") or {}).get("type") or target.get("role")


def material_paths(target: dict[str, Any], cfg: dict[str, Any]) -> list[str]:
    scoped = (target.get("scope") or {}).get("include") or []
    materiality = (cfg.get("assessment") or {}).get("materiality") or {}
    default = materiality.get("always_material_paths") or []
    profiles = materiality.get("role_profiles") or {}
    role = target_role(target)
    role_paths = profiles.get(role, []) if role else []
    return list(dict.fromkeys([*scoped, *default, *role_paths]))


def path_matches(name: str, pattern: str) -> bool:
    """Match repository paths with predictable root-file semantics.

    Python's fnmatch does not let ``**/SPEC.md`` match a root ``SPEC.md``.
    Git-style monitoring scopes normally expect that behaviour, so also try the
    pattern with a leading ``**/`` removed. Matching remains case-sensitive.
    """
    if fnmatch.fnmatch(name, pattern):
        return True
    if pattern.startswith("**/"):
        return fnmatch.fnmatch(name, pattern[3:])
    return False


def classify(target: dict[str, Any], files: list[dict[str, Any]], cfg: dict[str, Any]) -> tuple[str, list[str]]:
    patterns = material_paths(target, cfg)
    matched = []
    for f in files:
        name = f.get("filename", "")
        if any(path_matches(name, pat) for pat in patterns):
            matched.append(name)
    matched = sorted(set(matched))
    if not matched:
        return "ignore", matched
    materiality = (cfg.get("assessment") or {}).get("materiality") or {}
    documentation = materiality.get("documentation_paths") or []
    triage_roles = set(materiality.get("documentation_triage_roles") or [])
    role = target_role(target)
    docs_only = bool(documentation) and all(any(path_matches(name, pat) for pat in documentation) for name in matched)
    if role in triage_roles and docs_only:
        return "triage", matched
    return "assessment", matched


def state_key(target: dict[str, Any]) -> str:
    return f"{target['repository']}@{target.get('branch', 'main')}"


def assessment_key(instance_id: str, target: dict[str, Any]) -> str:
    """Return a stable assessment identity without collapsing branch targets.

    Main-branch repository keys retain the v0.7 key shape for compatibility.
    Non-main targets add ``@branch`` because they are independent assurance
    objects with separate revisions and dispositions.
    """
    repo = target["repository"]
    branch = target.get("branch", "main")
    suffix = "" if branch == "main" else f"@{branch}"
    return f"{instance_id}:repository:{repo}{suffix}"


def event_body(instance: dict[str, Any], target: dict[str, Any], old: str, new: str,
               comparison: dict[str, Any], matched: list[str]) -> str:
    repo = target["repository"]
    branch = target.get("branch", "main")
    commits = comparison.get("commits") or []
    lines = [
        "## RAHP assessment trigger", "",
        f"The **{instance.get('title', instance.get('id', 'RAHP'))}** change monitor detected a material change requiring review.", "",
        "| Field | Value |", "|---|---|",
        f"| Target | `{target.get('id')}` |",
        f"| Repository | `{repo}` |",
        f"| Branch | `{branch}` |",
        f"| Previous observed revision | `{old}` |",
        f"| Current observed revision | `{new}` |",
        f"| Commit count in comparison | {len(commits)} |", "",
        "### Material files changed", "",
    ]
    lines += [f"- `{p}`" for p in matched] or ["- Comparison could not identify a configured material path; conservative review requested."]
    lines += ["", "### Review action", "",
              "1. Inspect the upstream diff and determine whether semantics, assurance assumptions, security properties, governance dependencies, or interoperability behaviour changed.",
              "2. Re-run the target RAHP/security/combined review as appropriate.",
              "3. Update the relevant assessment artefact and close this issue only when the new revision has been dispositioned.",
              "", "### Governance boundary", "",
              "This issue records work for this RAHP deployment. It does **not** imply that RAHP owns, governs, or can change the upstream specification. Proposed remediation must be routed to the appropriate upstream specification, companion specification, governance body, implementation guidance, runtime control, or operational policy.", ""]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("command", choices=["sync", "check"])
    ap.add_argument("--config", type=pathlib.Path, required=True, help="instance configuration YAML")
    ap.add_argument("--initialize", action="store_true", help="record current heads without emitting review events")
    args = ap.parse_args()

    cfg = load_yaml(args.config)
    instance = cfg.get("instance") or {}
    profile_path = ROOT / instance["profile"]
    profile = load_yaml(profile_path)
    targets = profile.get("repositories") or []

    generated = ROOT / cfg["generated"]["manifest"]
    generated.parent.mkdir(parents=True, exist_ok=True)
    generated.write_text(yaml.safe_dump(profile, sort_keys=False), encoding="utf-8")
    print(f"loaded {len(targets)} target(s) for {instance.get('id')}")
    if args.command == "sync":
        return 0

    state_path = ROOT / cfg["state"]["file"]
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state = json.loads(state_path.read_text()) if state_path.exists() else {"version": 1, "targets": {}}
    state.setdefault("targets", {})
    events: list[dict[str, Any]] = []

    for target in targets:
        repo = target["repository"]
        branch = target.get("branch", "main")
        key = state_key(target)
        old_entry = state["targets"].get(key) or {}
        old = old_entry.get("sha")
        print(f"checking {key}")
        new = head_sha(repo, branch)
        if new is None:
            state["targets"][key] = {
                **({"sha": old} if old else {}),
                "status": "no-commits",
                "observed_at": datetime.now(timezone.utc).isoformat(),
            }
            print(f"warning: {key} has no commit history; skipped until a head revision exists")
            continue
        if not old or args.initialize:
            state["targets"][key] = {"sha": new, "status": "active", "observed_at": datetime.now(timezone.utc).isoformat()}
            continue
        if old == new:
            continue
        try:
            comp = compare(repo, old, new)
            classification, matched = classify(target, comp.get("files") or [], cfg)
        except Exception as exc:
            classification, matched = "assessment", []
            comp = {"commits": []}
            print(f"warning: comparison failed for {key}: {exc}")
        if classification == "assessment":
            instance_id = instance.get("id") or "external"
            events.append({
                "instance": instance_id,
                "target_id": target.get("id"),
                "assessment_key": assessment_key(instance_id, target),
                "source": "repository-change",
                "repository": repo,
                "branch": branch,
                "old": old,
                "new": new,
                "title": f"[RAHP review required] {target.get('id')}: {old[:7]} → {new[:7]}",
                "body": event_body(instance, target, old, new, comp, matched),
                "labels": ((cfg.get("assessment") or {}).get("issue") or {}).get("labels") or ["assessment-required"],
            })
        elif classification == "triage":
            instance_id = instance.get("id") or "external"
            events.append({
                "instance": instance_id,
                "target_id": target.get("id"),
                "assessment_key": f"{instance_id}:classification:{repo}{'' if branch == 'main' else '@' + branch}",
                "source": "repository-change",
                "repository": repo,
                "branch": branch,
                "old": old,
                "new": new,
                "event_class": "change-triage",
                "title": f"[Change triage] {target.get('id')}: {old[:7]} → {new[:7]}",
                "body": event_body(instance, target, old, new, comp, matched).replace(
                    "## RAHP assessment trigger", "## RAHP change-classification trigger"
                ).replace(
                    "detected a material change requiring review.",
                    "detected a documentation-only material change that requires classification before assessment."
                ).replace(
                    "2. Re-run the target RAHP/security/combined review as appropriate.",
                    "2. Classify the change as assessment-required, topology-change, or editorial/no-assurance-impact. Run RAHP/security review only when the first disposition applies."
                ),
                "labels": ["change-triage", f"{instance_id}-instance"],
            })
        state["targets"][key] = {"sha": new, "status": "active", "observed_at": datetime.now(timezone.utc).isoformat()}

    state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    events_path = ROOT / cfg["generated"]["events"]
    events_path.parent.mkdir(parents=True, exist_ok=True)
    events_path.write_text(json.dumps(events, indent=2) + "\n", encoding="utf-8")
    print(f"material review event(s): {len(events)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
