#!/usr/bin/env python3
"""Watch an allow-listed set of GitHub issues for assessment-relevant change.

Operational contract:
- Deployment-neutral early-warning adapter; each registry owns the watched issues,
  affected reviews, labels, and state/output paths.
- Reads the persisted issue observation state, compares current GitHub issue metadata,
  and emits assessment-trigger events when selected observations change.
- Issue activity is non-normative evidence: a changed comment or state can trigger
  review, but cannot by itself rebaseline a specification or establish assurance.
- Writes observation/event state only; downstream publication owns GitHub work items.
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys
import urllib.error
import urllib.request

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]


def get_issue(repo: str, number: int, token: str | None = None):
    req = urllib.request.Request(
        f"https://api.github.com/repos/{repo}/issues/{number}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "rahp-toolkit",
        },
    )
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)


def _resolve_repo(registry: dict, item: dict) -> str:
    repo = item.get("repository") or registry.get("repository") or registry.get("default_repository")
    if not repo:
        raise ValueError(f"issue #{item.get('number')} has no repository and registry has no default repository")
    return repo


def _labels(registry: dict) -> list[str]:
    labels = registry.get("labels")
    if labels:
        return list(labels)
    instance = registry.get("instance", "external")
    return ["assessment-required", f"{instance}-instance"]


def watch(registry_path: pathlib.Path, state_path: pathlib.Path, events_path: pathlib.Path, *, check: bool = False, token: str | None = None) -> list[dict]:
    registry = yaml.safe_load(registry_path.read_text())
    if state_path.exists():
        raw_state = state_path.read_text()
        try:
            state = json.loads(raw_state)
        except json.JSONDecodeError:
            # v0.7 development snapshots briefly wrote YAML syntax to a .json
            # state path. Accept it as a one-time migration input; normal writes
            # below always serialize canonical JSON.
            state = yaml.safe_load(raw_state)
    else:
        state = {"version": 1, "observed": {}}
    if not isinstance(state, dict):
        raise ValueError(f"issue-watch state must be a mapping: {state_path}")
    state.setdefault("version", 1)
    state.setdefault("observed", {})
    events = []

    for item in registry.get("issues", []):
        repo = _resolve_repo(registry, item)
        number = int(item["number"])
        key = f"{repo}#{number}"
        try:
            issue = get_issue(repo, number, token)
        except urllib.error.HTTPError as exc:
            # Authentication/rate-limit/service failures invalidate the assurance
            # observation. A missing/retired selected issue is surfaced but does not
            # abort the rest of the curated watch list.
            if exc.code in (403, 429) or 500 <= exc.code < 600:
                raise
            print(f"warning: unable to resolve {key}: HTTP {exc.code}", file=sys.stderr)
            continue

        snap = {
            "updated_at": issue.get("updated_at"),
            "state": issue.get("state"),
            "title": issue.get("title"),
            "comments": issue.get("comments", 0),
        }
        old = state["observed"].get(key)
        if old and old != snap:
            revision = (snap.get("updated_at") or "unknown").replace(":", "-")
            instance_id = registry.get("instance", "external")
            event_title = f"[{instance_id.upper()} assessment] upstream issue {key} changed @ {revision}"
            assessment_key = f"{instance_id}:issue:{key}"
            related_assessment_key = f"{instance_id}:repository:{repo}"
            theme = item.get("theme", "unspecified")
            affected = item.get("affected_reviews", [])
            body = (
                "## Why this needs RAHP review\n\n"
                f"A selected upstream issue changed after the last observed state for the **{registry.get('instance', 'external')}** deployment. "
                "GitHub issue discussion is not normative input, but the change may alter assumptions used by affected RAHP reviews.\n\n"
                f"- Upstream: `{key}`\n"
                f"- Theme: `{theme}`\n"
                f"- Affected reviews: {', '.join(affected) or 'unspecified'}\n"
                f"- Previous observed state: `{old}`\n"
                f"- Current observed state: `{snap}`\n\n"
                "Review the discussion and any resulting branch/spec changes before re-baselining the affected assessment."
            )
            events.append(
                {
                    "title": event_title,
                    "body": body,
                    "labels": _labels(registry),
                    "source": "upstream-issue",
                    "upstream_repository": repo,
                    "upstream_issue": number,
                    "theme": theme,
                    "affected_reviews": affected,
                    "assessment_key": assessment_key,
                    "related_assessment_key": related_assessment_key,
                    "observed_at": snap.get("updated_at"),
                    "previous_observation": old,
                    "current_observation": snap,
                }
            )
        state["observed"][key] = snap

    if not check:
        state_path.parent.mkdir(parents=True, exist_ok=True)
        events_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")
        events_path.write_text(json.dumps(events, indent=2, sort_keys=True) + "\n")
    print(
        f"{registry.get('instance', 'RAHP')} issue watch: "
        f"{len(registry.get('issues', []))} selected issue(s), {len(events)} assessment event(s)."
    )
    return events


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", required=True)
    parser.add_argument("--state", required=True)
    parser.add_argument("--events", required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    watch(
        (ROOT / args.registry).resolve() if not pathlib.Path(args.registry).is_absolute() else pathlib.Path(args.registry),
        (ROOT / args.state).resolve() if not pathlib.Path(args.state).is_absolute() else pathlib.Path(args.state),
        (ROOT / args.events).resolve() if not pathlib.Path(args.events).is_absolute() else pathlib.Path(args.events),
        check=args.check,
        token=os.getenv("GITHUB_TOKEN"),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
