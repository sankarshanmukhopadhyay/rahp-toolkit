#!/usr/bin/env python3
"""Read-only external RAHP return diagnostics bound to an existing obligation.

Contract validation and evidence-obligation binding are not source authentication,
evidence admission, specialist authorization or a terminal RAHP determination.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

try:
    from tools import assessor_contract, validate_evidence_producer_result
except ImportError:
    import assessor_contract
    import validate_evidence_producer_result

ROOT = Path(__file__).resolve().parents[1]
OBLIGATION_SCHEMA = ROOT / "schemas/rahp-assurance-obligation-v1.schema.json"


def _load(path):
    doc = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(doc, dict):
        raise ValueError("expected a JSON object")
    return doc


def _pins(rows):
    if not isinstance(rows, list):
        return None
    if any(not isinstance(pin, dict) for pin in rows):
        return None
    # Preserve the full declared pin including roles and scoped extension claims.
    return [json.dumps(pin, sort_keys=True, separators=(",", ":")) for pin in rows]


def diagnose(kind, result, obligation=None, previous=None, expected_assessment_id=None):
    errors = []
    unknown = []
    expected_schema = {
        "producer": "rahp-evidence-producer-result/v1",
        "assessor": "rahp-assessor-result/v1",
    }[kind]
    if not isinstance(result, dict):
        return {"status": "INVALID_CONTRACT", "contract": expected_schema,
                "errors": ["result must be a JSON object"], "not_established": [],
                "authenticated": False, "assurance_determination": None}
    if kind == "producer":
        problems = validate_evidence_producer_result.validate_result(result)
    else:
        problems = assessor_contract.validate_result(result)
    if problems:
        # Avoid embedding sensitive arbitrary schema input in CLI diagnostics.
        return {"status": "INVALID_CONTRACT", "contract": expected_schema,
                "errors": ["result violates the authoritative v1 contract"],
                "not_established": [], "authenticated": False,
                "assurance_determination": None}
    if obligation is None:
        unknown.append("authoritative obligation context missing")
    elif not isinstance(obligation, dict):
        errors.append("obligation must be an object")
    else:
        schema = json.loads(OBLIGATION_SCHEMA.read_text(encoding="utf-8"))
        if not Draft202012Validator(schema).is_valid(obligation):
            errors.append("obligation violates authoritative v1 schema")
        else:
            if kind == "producer":
                bound = result["obligation"]
                for key in ("proposition_key", "evidence_contract_key"):
                    if bound.get(key) != obligation.get(key):
                        errors.append(key + " differs from obligation")
                ids = obligation.get("evidence_requirement_ids")
                if not isinstance(ids, list) or not ids:
                    unknown.append("obligation does not declare evidence requirement identifiers")
                elif set(ids) != set(bound.get("evidence_requirement_ids", [])):
                    errors.append("evidence requirement identities differ from obligation")
                observed = result["evidence"].get("observations", [])
                for item in observed:
                    if (isinstance(item, dict) and item.get("requirement_id")
                            and item["requirement_id"] not in bound["evidence_requirement_ids"]):
                        errors.append("observation references an unrelated evidence requirement")
                        break
            else:
                ids = obligation.get("evidence_requirement_ids")
                if ids is None:
                    unknown.append("obligation does not declare evidence requirement identifiers")
                elif any(ref not in ids for ref in result["evidence_used"]):
                    errors.append("assessor cites evidence outside addressed obligation")
            expected_pins = _pins(obligation.get("source_pins"))
            actual_pins = _pins(
                result.get("source", {}).get("pins") if kind == "producer"
                else result.get("source_pins"))
            if expected_pins is None or not expected_pins:
                unknown.append("obligation source pins unavailable")
            elif actual_pins is None:
                unknown.append("result source pins unavailable")
            elif sorted(expected_pins) != sorted(actual_pins):
                errors.append("source revision or scoped pin differs from obligation")

    if kind == "assessor":
        if expected_assessment_id is None:
            unknown.append("assessment identity not independently supplied")
        elif result["assessment_id"] != expected_assessment_id:
            errors.append("assessment identity differs from expected controller context")
    elif expected_assessment_id is not None:
        unknown.append("producer contract has no canonical assessor assessment identifier")

    if previous is not None:
        if not isinstance(previous, dict) or previous.get("schema") != expected_schema:
            errors.append("previous return has incompatible contract")
        else:
            if kind == "producer":
                same_identity = (previous.get("producer", {}).get("id") ==
                                 result["producer"]["id"] and
                                 previous.get("execution", {}).get("id") ==
                                 result["execution"]["id"])
            else:
                same_identity = (previous.get("assessor") == result["assessor"] and
                                 previous.get("assessment_id") == result["assessment_id"])
            if same_identity:
                errors.append("duplicate return identity" if previous == result
                              else "conflicting return under an existing identity")
            else:
                unknown.append("previous return is a distinct identity; no general replay registry")

    if kind == "producer":
        execution_state = result["execution"]["status"]
        evidence_state = result["evidence"]["status"]
        if execution_state != "succeeded":
            unknown.append("producer execution " + execution_state)
        if evidence_state != "observed":
            unknown.append("producer evidence " + evidence_state)
    # Never promote specialist PASS into controller assurance PASS.
    status = "REJECTED_BINDING" if errors else ("NOT_ESTABLISHED" if unknown else "VALID_BOUND_CONTRACT")
    return {"status": status, "contract": expected_schema, "errors": errors,
            "not_established": sorted(set(unknown)), "authenticated": False,
            "assurance_determination": None}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--kind", choices=("producer", "assessor"), required=True)
    p.add_argument("--result", type=Path, required=True)
    p.add_argument("--obligation", type=Path)
    p.add_argument("--previous-result", type=Path)
    p.add_argument("--expected-assessment-id")
    a = p.parse_args()
    try:
        result = _load(a.result)
        obligation = _load(a.obligation) if a.obligation else None
        previous = _load(a.previous_result) if a.previous_result else None
        report = diagnose(a.kind, result, obligation, previous, a.expected_assessment_id)
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        report = {"status": "INVALID_INPUT", "contract": None,
                  "errors": ["input is missing, unreadable or malformed"],
                  "not_established": [], "authenticated": False,
                  "assurance_determination": None}
    print(json.dumps(report, sort_keys=True))
    return 0 if report["status"] == "VALID_BOUND_CONTRACT" else 1


if __name__ == "__main__":
    sys.exit(main())
