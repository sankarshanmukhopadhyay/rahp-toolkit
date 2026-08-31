#!/usr/bin/env python3
"""Stamp DTG material-review events with stable gatherer run/event lineage.

Operational contract:
- Post-processes dtg_portfolio.py output; discovery/materiality remain owned upstream.
- Adds deterministic event identifiers and a run identifier, then retains each non-empty
  gatherer run as immutable JSON under instances/dtg/generated/gatherer-runs/.
- This retention prevents a later empty incremental run from hiding unresolved RAHP or
  DPIP work from an earlier run.
- It creates provenance only; it does not assess or disposition the events.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
from datetime import datetime, timezone
from typing import Any

DEFAULT_EVENTS = pathlib.Path("instances/dtg/generated/review-events.json")
DEFAULT_RUN_DIR = pathlib.Path("instances/dtg/generated/gatherer-runs")


def event_id(event: dict[str, Any]) -> str:
    material = "|".join(str(event.get(k) or "") for k in ("assessment_key", "repository", "old", "new", "event_class"))
    return hashlib.sha256(material.encode("utf-8")).hexdigest()[:20]


def stamp(events: list[dict[str, Any]], run_id: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    ids: list[str] = []
    stamped: list[dict[str, Any]] = []
    marker = f"<!-- rahp-dtg-gatherer-run:{run_id} -->"
    for raw in events:
        event = dict(raw)
        eid = event_id(event)
        ids.append(eid)
        event["gatherer_run_id"] = run_id
        event["gatherer_event_id"] = eid
        # publish_assessment_issues uses observed_at in the coalesced trigger marker;
        # this preserves the run identity even when a repository's work is coalesced.
        event["observed_at"] = f"gatherer-{run_id}-{eid}"
        body = str(event.get("body") or "")
        if marker not in body:
            event["body"] = marker + f"\n<!-- rahp-dtg-gatherer-event:{eid} -->\n\n" + body
        stamped.append(event)
    fingerprint = hashlib.sha256("\n".join(sorted(ids)).encode("utf-8")).hexdigest()[:24]
    run = {
        "version": 1,
        "id": run_id,
        "fingerprint": fingerprint,
        "qualifying_events": ids,
        "event_count": len(ids),
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "source": "rahp-dtg-gatherer",
    }
    return stamped, run


def resolved_run_id(explicit: str | None = None) -> str:
    if explicit:
        return explicit
    github_run = os.getenv("GITHUB_RUN_ID")
    attempt = os.getenv("GITHUB_RUN_ATTEMPT", "1")
    if github_run:
        return f"gha-{github_run}-{attempt}"
    return datetime.now(timezone.utc).strftime("local-%Y%m%dT%H%M%SZ")


def run_record_path(run_dir: pathlib.Path, run_id: str) -> pathlib.Path:
    return run_dir / f"{run_id}.json"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--events", type=pathlib.Path, default=DEFAULT_EVENTS)
    p.add_argument("--run-dir", type=pathlib.Path, default=DEFAULT_RUN_DIR)
    p.add_argument("--run-id")
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args()
    if args.self_test:
        events = [{"assessment_key":"dtg:repository:a/b","repository":"a/b","old":"a","new":"b","event_class":"assessment-required","body":"x"}]
        first, run1 = stamp(events, "test-1")
        second, run2 = stamp(events, "test-1")
        assert run1["fingerprint"] == run2["fingerprint"]
        assert first[0]["gatherer_event_id"] == second[0]["gatherer_event_id"]
        assert "rahp-dtg-gatherer-run:test-1" in first[0]["body"]
        assert run_record_path(pathlib.Path("runs"), "test-1") == pathlib.Path("runs/test-1.json")
        print("PASS dtg_gatherer_lineage self-test")
        return 0
    events = json.loads(args.events.read_text(encoding="utf-8")) if args.events.exists() else []
    run_id = resolved_run_id(args.run_id)
    stamped, run = stamp(events, run_id)
    args.events.parent.mkdir(parents=True, exist_ok=True)
    args.events.write_text(json.dumps(stamped, indent=2) + "\n", encoding="utf-8")
    if run["event_count"]:
        args.run_dir.mkdir(parents=True, exist_ok=True)
        path = run_record_path(args.run_dir, run_id)
        if path.exists():
            existing = json.loads(path.read_text(encoding="utf-8"))
            # A rerun/attempt with the same identity must be deterministic rather than
            # mutating the evidence set beneath an existing assurance lineage.
            if existing.get("fingerprint") != run["fingerprint"]:
                raise SystemExit(f"gatherer run identity collision for {run_id}: evidence fingerprint changed")
        else:
            path.write_text(json.dumps(run, indent=2) + "\n", encoding="utf-8")
    print(f"DTG gatherer run {run['id']}: {run['event_count']} qualifying event(s), fingerprint {run['fingerprint']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
