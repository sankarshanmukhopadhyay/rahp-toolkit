"""Fail-closed attribution gate for RAHP #994 runtime evidence.

This validates evidence metadata, not a signature, credential, protocol exchange,
or deployed authorization. PASS requires a qualified external verifier; unreviewed
runtime records must remain INDETERMINATE regardless of schema validity.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "data/assurance/runtime-evidence-994.json"
REQUIRED_SCOPES = {"A", "B", "C"}
STATES = {"INDETERMINATE", "FAIL", "TRANSFERRED"}
EVIDENCE_RE = re.compile(r"^[0-9a-f]{64}$")


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    if data.get("schema") != "rahp-runtime-evidence-packet/v1" or data.get("issue") != 994:
        errors.append("wrong packet schema or issue ownership")
    scopes = data.get("scopes")
    if not isinstance(scopes, list) or {x.get("scope") for x in scopes if isinstance(x, dict)} != REQUIRED_SCOPES or len(scopes) != 3:
        return errors + ["exact scopes A/B/C are required"]
    for row in scopes:
        name = row.get("scope", "?")
        if row.get("state") not in STATES:
            errors.append(f"{name}: unsupported disposition; PASS cannot be certified by a routing manifest")
        findings = row.get("source_findings")
        cases = row.get("negative_cases")
        if not isinstance(findings, list) or not findings or len(set(findings)) != len(findings):
            errors.append(f"{name}: missing or duplicate source finding")
        if not isinstance(cases, list) or not cases or len(set(cases)) != len(cases):
            errors.append(f"{name}: missing or duplicate negative cases")
        if row.get("state") == "TRANSFERRED" and not isinstance(row.get("successor_issue"), int):
            errors.append(f"{name}: transfer needs durable owner")
        artifact = row.get("runtime_evidence")
        if artifact is not None:
            if not isinstance(artifact, dict) or not EVIDENCE_RE.fullmatch(str(artifact.get("sha256", ""))):
                errors.append(f"{name}: evidence must carry SHA-256")
            elif any(not isinstance(artifact.get(k), str) or not artifact[k] for k in ("source", "actor", "observed_at", "environment", "replay_command")):
                errors.append(f"{name}: evidence provenance incomplete")
        if row.get("state") == "FAIL" and artifact is None:
            errors.append(f"{name}: observed FAIL needs attributable evidence")
        if row.get("dpip") not in {"NOT_ASSESSED", "REFERRED", "OUT_OF_SCOPE_WITH_RATIONALE"}:
            errors.append(f"{name}: invalid DPIP status")
        if row.get("dpip") == "REFERRED" and not isinstance(row.get("dpip_issue"), int):
            errors.append(f"{name}: DPIP referral needs issue")
        if row.get("dpip") == "OUT_OF_SCOPE_WITH_RATIONALE" and not row.get("privacy_rationale"):
            errors.append(f"{name}: privacy exclusion needs rationale")
    return errors


def main() -> int:
    data = json.loads(DEFAULT.read_text(encoding="utf-8"))
    errors = validate(data)
    for error in errors:
        print("ERROR:", error)
    if not errors:
        print("PASS manifest integrity. Runtime assurance: INDETERMINATE; no deployment proof inferred.")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
