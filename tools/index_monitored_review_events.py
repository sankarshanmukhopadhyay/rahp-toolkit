#!/usr/bin/env python3
"""Validate and index source-observed external review events without admitting cases.

The canonical event bytes are deterministic and the source/pin is a concrete
upstream commit. Neither classification nor this index decides whether a new
Registry case is eligible, unique, or accepted by its external owner.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

HEX40 = re.compile(r"^[0-9a-f]{40}$")
REPOSITORY = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
KEY = re.compile(r"^(?:dtg|cawg):[a-z0-9][a-z0-9:._/-]{7,170}$")
SCHEMA = "rahp-monitored-source-review-index/v1"


def canonical(event):
    return json.dumps(event, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def qualify(events, instance):
    if instance not in ("dtg", "cawg"):
        raise ValueError("unknown source instance")
    if not isinstance(events, list):
        raise ValueError("monitored review batch must be JSON array")
    items = []
    seen = set()
    for event in events:
        if not isinstance(event, dict):
            raise ValueError("monitored source event is not object")
        key = event.get("assessment_key")
        repo = event.get("repository")
        revision = event.get("new")
        kind = event.get("event_class")
        if (not isinstance(key, str) or not KEY.fullmatch(key)
                or not key.startswith(instance + ":") or key in seen):
            raise ValueError("invalid or duplicate monitored assessment key")
        seen.add(key)
        if (not isinstance(repo, str) or not REPOSITORY.fullmatch(repo)
                or any(segment in (".", "..") for segment in repo.split("/"))
                or not isinstance(revision, str) or not HEX40.fullmatch(revision)):
            raise ValueError("missing immutable repository source pin")
        if not isinstance(event.get("title"), str) or not event["title"].strip():
            raise ValueError("monitored event has no title")
        if not isinstance(event.get("body"), str) or not event["body"].strip():
            raise ValueError("monitored event has no source body")
        if not isinstance(event.get("labels"), list) or not all(
                isinstance(x, str) and x.strip() for x in event["labels"]):
            raise ValueError("monitored event labels invalid")
        if kind not in (None, "assessment-required", "change-triage"):
            raise ValueError("unknown monitored event classification")
        encoded = canonical(event)
        full = hashlib.sha256(encoded).hexdigest()
        items.append({
            "assessment_key": key,
            "source_repository": repo,
            "source_revision": revision,
            "source_evidence_sha256": full,
            "finding_id": full[:20],
            "classification": (
                "assessment_required" if "assessment-required" in event["labels"]
                and kind in (None, "assessment-required")
                else "triage_only"
            ),
        })
    return {"schema": SCHEMA, "instance": instance, "events": items,
            "candidate_count": sum(x["classification"] == "assessment_required"
                                   for x in items),
            "admission_authorized": False,
            "assurance_determination": None}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dtg", type=Path, required=True)
    parser.add_argument("--cawg", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    results = []
    for instance, path in (("dtg", args.dtg), ("cawg", args.cawg)):
        results.append(qualify(json.loads(path.read_text(encoding="utf-8")),
                               instance))
    report = {"schema": SCHEMA,
              "sources": results,
              "admission_authorized": False,
              "assurance_determination": None}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8")
    print("Validated reviewed monitor source batches; no Registry admission or PASS")


if __name__ == "__main__":
    main()
