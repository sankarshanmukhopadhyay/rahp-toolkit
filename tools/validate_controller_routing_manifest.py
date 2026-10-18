"""Fail-closed offline checks for exact snapshot controller routing ledgers.

This is not a GitHub issue closer or a semantic assurance engine. A valid
UNMAPPED ledger never proves that combined/covered/no-action/DPIP routing is
complete. Unknown ownership is allowed only when prominently declared.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUSES = {"review-open", "review-candidate", "already-assessed-trigger", "owner-unresolved"}


def validate_manifest(data: dict) -> list[str]:
    errors: list[str] = []
    if data.get("schema") != "rahp-controller-routing-manifest/v1":
        errors.append("unknown controller manifest schema")
    digest = data.get("snapshot_digest")
    if not isinstance(digest, str) or len(digest) != 64 or any(x not in "0123456789abcdef" for x in digest):
        errors.append("snapshot digest must be lowercase sha256")
    distribution = data.get("distribution")
    if not isinstance(distribution, dict) or set(distribution) != {"UNMAPPED", "combined", "covered", "no-action"}:
        errors.append("incomplete distribution")
        distribution = {}
    if sum(x for x in distribution.values() if isinstance(x, int) and x >= 0) != data.get("qualifying_findings"):
        errors.append("distribution does not equal qualifying findings")
    if data.get("scope") != "UNMAPPED-only" or data.get("closure_authorized") is not False:
        errors.append("partial routing cannot authorize controller closure")
    findings = data.get("findings")
    if not isinstance(findings, list):
        return errors + ["findings must be an array"]
    if len(findings) != distribution.get("UNMAPPED"):
        errors.append("unmapped finding count mismatch")
    seen: set[str] = set()
    for index, finding in enumerate(findings):
        if not isinstance(finding, dict):
            errors.append(f"finding {index}: object required")
            continue
        fid = finding.get("finding_id")
        if not isinstance(fid, str) or len(fid) != 20 or any(x not in "0123456789abcdef" for x in fid):
            errors.append(f"finding {index}: invalid identity")
        elif fid in seen:
            errors.append(f"finding {index}: duplicate identity {fid}")
        else:
            seen.add(fid)
        state = finding.get("status")
        owner = finding.get("owner_issue")
        if state not in STATUSES:
            errors.append(f"finding {index}: unknown disposition {state!r}")
        if state == "owner-unresolved":
            if owner is not None:
                errors.append(f"finding {index}: unresolved finding cannot declare owner")
        elif not isinstance(owner, int) or isinstance(owner, bool) or owner <= 0:
            errors.append(f"finding {index}: disposition requires durable owner issue")
    return errors


def main() -> int:
    path = ROOT / "data" / "assurance" / "controller-1054-routing.json"
    errors = validate_manifest(json.loads(path.read_text(encoding="utf-8")))
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: controller #1054 inventory validated; closure NOT authorized")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
