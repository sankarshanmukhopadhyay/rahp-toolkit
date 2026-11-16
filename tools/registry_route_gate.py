#!/usr/bin/env python3
"""Read-only readiness audit of actual DTG-generated issue events."""
import argparse
import json
import re
from pathlib import Path

SHA = re.compile(r"^[0-9a-f]{40}$")
KEY = re.compile(r"^[a-z0-9][a-z0-9:._/-]{7,180}$")


def evaluate(kind, event):
    if not isinstance(event, dict):
        raise ValueError("event must be an object")
    key = event.get("assessment_key")
    blockers = []
    if not isinstance(key, str) or not KEY.fullmatch(key):
        blockers.append("invalid_assessment_key")
    if not isinstance(event.get("body"), str) or not event["body"].strip():
        blockers.append("missing_body")
    if kind == "controller":
        blockers.append("controller_requires_non_issue_execution_state")
    elif kind == "dpip":
        blockers.append("dpip_return_requires_controller_compatible_transport")
    elif kind == "combined":
        blockers.append("combined_worker_requires_registry_aware_consumer")
        pins = event.get("source_pins")
        if not isinstance(pins, list) or not pins:
            blockers.append("missing_source_pins")
        elif any(not isinstance(p, dict) or not SHA.fullmatch(str(p.get("revision", "")))
                 or not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+",
                                     str(p.get("repository", ""))) for p in pins):
            blockers.append("invalid_source_pins")
        if not event.get("responsible_owner"):
            blockers.append("missing_accepted_external_owner")
    else:
        raise ValueError("unknown event kind")
    return {"kind": kind, "assessment_key": key,
            "ready": not blockers, "blockers": blockers}


def audit(groups):
    result = []
    seen = set()
    for kind in ("controller", "combined", "dpip"):
        events = groups.get(kind)
        if not isinstance(events, list):
            raise ValueError(f"{kind} must be a JSON array")
        for event in events:
            item = evaluate(kind, event)
            key = item["assessment_key"]
            if key and key in seen:
                item["ready"] = False
                item["blockers"].append("duplicate_assessment_key")
            seen.add(key)
            result.append(item)
    return {"schema": "rahp-registry-route-preflight/v1",
            "live_cutover_authorized": False,
            "blocked": sum(not item["ready"] for item in result),
            "events": result}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for kind in ("controller", "combined", "dpip"):
        p.add_argument("--" + kind, type=Path, required=True)
    p.add_argument("--out", type=Path)
    p.add_argument("--require-ready", action="store_true")
    args = p.parse_args()
    report = audit({kind: json.loads(getattr(args, kind).read_text(encoding="utf-8"))
                    for kind in ("controller", "combined", "dpip")})
    output = json.dumps(report, indent=2) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    if args.require_ready and report["blocked"]:
        raise SystemExit("registry cutover blocked by unsatisfied controller/producer contracts")


if __name__ == "__main__":
    main()
