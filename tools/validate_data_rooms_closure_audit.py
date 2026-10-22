#!/usr/bin/env python3
"""Fail-closed cross-check of Data Rooms closure audit and monitor inventory."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FINDINGS = ROOT / "docs/review/data-rooms/reconciliation-2026-10-22.json"
AUDIT = ROOT / "docs/review/data-rooms/closure-audit-2026-10-22.json"

def validate(findings, audit):
    errors = []
    rows = findings.get("findings", [])
    attributed = sum(bool(row.get("source_revision")) for row in rows)
    terminal = sum(row.get("disposition") not in ("triage_required", "requires_target_retest") for row in rows)
    expected = {"observations": len(rows), "source_attributed": attributed,
                "unattributed": len(rows) - attributed, "terminally_dispositioned": terminal}
    if audit.get("schema") != "rahp-data-rooms-closure-audit/v1":
        errors.append("invalid audit schema")
    if audit.get("monitor") != expected:
        errors.append("audit monitor counts differ from source inventory")
    props = audit.get("propositions", [])
    ids = [row.get("proposition_id") for row in props]
    required = [f"P-ROOM-{i:03}" for i in range(1, 17)]
    if sorted(ids) != required:
        errors.append("proposition set is not exactly P-ROOM-001..016")
    for row in props:
        name = row.get("proposition_id")
        if row.get("current_target_retest") == "not_established" and row.get("transfer_accepted"):
            errors.append(f"{name}: cannot accept transfer based on absent retest alone")
        if row.get("owner_status") == "not_accepted" and row.get("owner_ref"):
            errors.append(f"{name}: unaccepted owner cannot be a canonical handoff")
    gates = audit.get("closure_gates", {})
    if not all(gates.get(k) is True for k in (
        "all_monitor_findings_terminal", "all_propositions_adjudicated_current_target",
        "all_unresolved_residuals_accepted_by_owner",
        "applicable_dpip_returns_accounted_for")):
        if audit.get("close_481") or audit.get("close_1074"):
            errors.append("closure asserted with incomplete substantive gates")
    if terminal != len(rows) and audit.get("close_1074"):
        errors.append("1074 cannot close while monitor dispositions remain non-terminal")
    return errors

def main():
    findings = json.loads(FINDINGS.read_text(encoding="utf-8"))
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    errors = validate(findings, audit)
    if errors:
        for error in errors:
            print("FAIL:", error, file=sys.stderr)
        return 1
    print("PASS: 16 proposition records and fail-closed closure gates; no unsupported closure")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
