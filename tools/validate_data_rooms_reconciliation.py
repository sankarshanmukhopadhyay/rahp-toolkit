#!/usr/bin/env python3
"""Validate the bounded Data Rooms monitor reconciliation inventory."""
import json
import re
import sys
from pathlib import Path

DEFAULT = Path(__file__).resolve().parents[1] / "docs/review/data-rooms/reconciliation-2026-10-22.json"
SHA = re.compile(r"^[a-f0-9]{40}$")
FINDING = re.compile(r"^[a-f0-9]{20}$")

def validate(doc):
    errors = []
    if doc.get("schema") != "rahp-data-rooms-reconciliation/v1":
        errors.append("unsupported schema")
    baseline = doc.get("baseline", {})
    for key in ("rahp_main", "openvtc_main", "trust_tasks_main",
                "historical_executable_openvtc", "historical_trust_tasks",
                "historical_design_openvtc"):
        if not SHA.fullmatch(str(baseline.get(key, ""))):
            errors.append(f"missing or invalid baseline SHA: {key}")
    entries = doc.get("findings", [])
    if len(entries) != 21:
        errors.append(f"expected exactly 21 distinct monitor findings, got {len(entries)}")
    seen = set()
    kinds = {"release_marker": 0, "change_description": 0}
    for row in entries:
        fid = row.get("finding_id", "")
        if not FINDING.fullmatch(str(fid)):
            errors.append(f"invalid monitor key: {fid}")
        if fid in seen:
            errors.append(f"duplicate monitor key: {fid}")
        seen.add(fid)
        kind = row.get("observation_kind")
        if kind not in kinds:
            errors.append(f"invalid observation kind: {fid}")
        else:
            kinds[kind] += 1
        if not row.get("source_repository") or not row.get("observed_change"):
            errors.append(f"missing provenance description: {fid}")
        if row.get("classification") == "pending_source_verification":
            if row.get("source_revision") is not None:
                errors.append(f"pending item improperly carries source revision: {fid}")
            if row.get("evidence_state") != "not_established" or row.get("disposition") != "triage_required":
                errors.append(f"pending item asserted a terminal result: {fid}")
        elif not SHA.fullmatch(str(row.get("source_revision", ""))):
            errors.append(f"classified item lacks an attributable source SHA: {fid}")
    if kinds != {"release_marker": 3, "change_description": 18}:
        errors.append(f"unexpected monitor kind counts: {kinds}")
    return errors

def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
    errors = validate(json.loads(path.read_text(encoding="utf-8")))
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print("PASS: 21 distinct observed IDs (18 changes, 3 release markers); no unverified PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
