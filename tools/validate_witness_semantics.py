"""Validate source-pinned witness role, identity and lifecycle assurance cases.

This is a downstream RAHP assurance harness. It does not define DTG witness
authority or privacy conclusions.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/assurance/witness-semantics-1081-1082.json"
STATES = {"PASS", "FAIL", "INDETERMINATE"}
PROPOSITIONS = {
    "WIT-ROLE-001", "WIT-ROLE-002", "WIT-ID-001", "WIT-ID-002",
    "WIT-TIME-001", "WIT-REV-001", "WIT-KEY-001", "WIT-AVAIL-001",
    "WIT-SUCC-001", "WIT-RET-001",
}


def evaluate(proposition: str, data: dict) -> str:
    if proposition == "WIT-ROLE-001":
        if data.get("witness_is_event_party") is True:
            return "FAIL"
        if data.get("witness_is_event_party") is not False:
            return "INDETERMINATE"
        if data.get("policy_requires_org_independence") is True:
            return "PASS" if data.get("external_independence_evidence") is True else "INDETERMINATE"
        return "PASS"

    if proposition == "WIT-ROLE-002":
        if data.get("policy_requires_org_independence") is not True:
            return "PASS"
        return "PASS" if data.get("external_independence_evidence") is True else "INDETERMINATE"

    if proposition == "WIT-ID-001":
        if data.get("continuity_required") is not True:
            return "PASS"
        values = [data.get("vwc_issuer"), data.get("session_recipient"), data.get("response_signer")]
        if any(not value for value in values):
            return "INDETERMINATE"
        return "PASS" if len(set(values)) == 1 else "FAIL"

    if proposition == "WIT-ID-002":
        if data.get("claims_org_independence_from_identifier") is True:
            return "FAIL"
        if data.get("ceremony_identity_continuous") is not True:
            return "INDETERMINATE"
        return "PASS"

    if proposition == "WIT-TIME-001":
        if data.get("cascade_applied") is True:
            return "FAIL"
        required = ("vrc_at_witnessing", "vrc_current", "vwc_current")
        if any(data.get(key) is None for key in required):
            return "INDETERMINATE"
        return "PASS"

    if proposition == "WIT-REV-001":
        if data.get("vwc_status") != "revoked":
            return "PASS"
        semantics = data.get("reason_semantics")
        interpretation = data.get("attempted_interpretation")
        if semantics in {"attestation-invalidation", "reliance-withdrawal"}:
            expected = {
                "attestation-invalidation": "historical-attestation-invalid",
                "reliance-withdrawal": "future-reliance-withdrawn",
            }[semantics]
            return "PASS" if interpretation in {None, expected} else "FAIL"
        return "INDETERMINATE"

    if proposition == "WIT-KEY-001":
        if data.get("key_authorized_at_issuance") is not True:
            return "INDETERMINATE"
        if data.get("compromise_discovered_later") is True and data.get("compromise_onset") in {None, "unknown"}:
            return "INDETERMINATE"
        return "PASS"

    if proposition == "WIT-AVAIL-001":
        evidence = data.get("status_evidence")
        if evidence in {None, "unavailable"}:
            return "INDETERMINATE"
        return "PASS" if evidence in {"valid", "revoked"} else "INDETERMINATE"

    if proposition == "WIT-SUCC-001":
        if data.get("successor_mutates_status") is not True:
            return "PASS" if data.get("successor_hosts_frozen_evidence") is True else "INDETERMINATE"
        authority = data.get("mutation_authority")
        if authority == "explicit":
            return "PASS"
        if authority in {None, "unknown"}:
            return "INDETERMINATE"
        return "FAIL"

    if proposition == "WIT-RET-001":
        if data.get("original_presentation_retained") is False and data.get("claims_original_reconstructible") is True:
            return "FAIL"
        if data.get("original_presentation_retained") is None:
            return "INDETERMINATE"
        return "PASS"

    raise ValueError(f"unsupported proposition: {proposition}")


def verify(data: dict) -> list[str]:
    errors: list[str] = []
    if data.get("schema") != "rahp-witness-assurance/v1":
        errors.append("unsupported witness assurance schema")

    if data.get("owners") != [1081, 1082]:
        errors.append("owners must preserve issue traceability [1081, 1082]")

    pins = data.get("source_pins")
    if not isinstance(pins, list) or len(pins) < 3:
        errors.append("expected at least three pinned authoritative source families")
    else:
        for pin in pins:
            if not re.fullmatch(r"[0-9a-f]{40}", str(pin.get("revision", ""))):
                errors.append(f"source revision must be full Git SHA: {pin.get('repository')}")
            if not pin.get("paths"):
                errors.append(f"source pin lacks paths: {pin.get('repository')}")

    proposition_ids = {item.get("id") for item in data.get("propositions", [])}
    if proposition_ids != PROPOSITIONS:
        errors.append("proposition set does not match the bounded #1081/#1082 contract")

    boundary = data.get("authority_boundary", {})
    if "privacy conclusions owned by issue #338/DPIP" not in boundary.get("does_not_define", []):
        errors.append("privacy authority boundary must route conclusions to #338/DPIP")

    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        return errors + ["witness assurance cases are required"]

    seen: set[str] = set()
    for case in cases:
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id or case_id in seen:
            errors.append(f"missing or duplicate case id: {case_id!r}")
            continue
        seen.add(case_id)
        proposition = case.get("proposition")
        if proposition not in PROPOSITIONS:
            errors.append(f"{case_id}: unknown proposition {proposition!r}")
            continue
        expected = case.get("expected")
        if expected not in STATES:
            errors.append(f"{case_id}: invalid expected state {expected!r}")
            continue
        observed = evaluate(proposition, case.get("input", {}))
        if observed != expected:
            errors.append(f"{case_id}: expected {expected}, evaluator produced {observed}")

    required_cases = {
        "ROLE-POS-COMMUNITY", "ROLE-NEG-PARTY", "ROLE-NEG-SELF-ASSERTED",
        "ID-NEG-DIVERGENCE", "TIME-N1-VRC-LATER-REVOKED", "TIME-N2-VWC-REVOKED",
        "AVAIL-N3-OUTAGE", "AVAIL-N4-RETIRED", "SUCC-N4-NEG-MUTATION",
        "KEY-N5-UNKNOWN-ONSET", "REV-N6-AMBIGUOUS", "RET-NEG-RECONSTRUCTION",
    }
    missing = sorted(required_cases - seen)
    if missing:
        errors.append(f"required falsification cases missing: {missing}")

    strategy = data.get("strategy_comparison", {})
    if strategy.get("assurance_equivalent") is not False:
        errors.append("short-validity and online-status strategies must not be declared assurance-equivalent")
    if strategy.get("short_validity_no_status", {}).get("immediate_withdrawal") is not False:
        errors.append("short-validity/no-status must preserve lack of immediate withdrawal")
    if strategy.get("online_status", {}).get("immediate_withdrawal") is not True:
        errors.append("online-status comparison must preserve immediate withdrawal capability")

    if data.get("evidence_state") != "mechanically-reviewable-source-pinned-cases":
        errors.append("evidence state must not overclaim runtime conformance")

    return errors


def main() -> int:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    errors = verify(data)
    for error in errors:
        print("ERROR:", error)
    if errors:
        return 1
    counts = {"PASS": 0, "FAIL": 0, "INDETERMINATE": 0}
    for case in data["cases"]:
        counts[evaluate(case["proposition"], case["input"])] += 1
    print(
        "PASS witness assurance contract; "
        f"{counts['PASS']} PASS / {counts['FAIL']} FAIL / "
        f"{counts['INDETERMINATE']} INDETERMINATE expected-case outcomes"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
