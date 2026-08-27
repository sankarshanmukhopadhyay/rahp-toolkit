#!/usr/bin/env python3
"""Stamp DTG gatherer events with a stable run lineage identifier.

This post-processes the existing dtg_portfolio.py event list so the gatherer remains
focused on discovery/materiality while orchestration owns run identity.
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
DEFAULT_RUN = pathlib.Path("instances/dtg/generated/gatherer-run.json")


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


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--events", type=pathlib.Path, default=DEFAULT_EVENTS)
    p.add_argument("--run-record", type=pathlib.Path, default=DEFAULT_RUN)
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
        print("PASS dtg_gatherer_lineage self-test")
        return 0
    events = json.loads(args.events.read_text(encoding="utf-8")) if args.events.exists() else []
    stamped, run = stamp(events, resolved_run_id(args.run_id))
    args.events.parent.mkdir(parents=True, exist_ok=True)
    args.events.write_text(json.dumps(stamped, indent=2) + "\n", encoding="utf-8")
    args.run_record.parent.mkdir(parents=True, exist_ok=True)
    args.run_record.write_text(json.dumps(run, indent=2) + "\n", encoding="utf-8")
    print(f"DTG gatherer run {run['id']}: {run['event_count']} qualifying event(s), fingerprint {run['fingerprint']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
