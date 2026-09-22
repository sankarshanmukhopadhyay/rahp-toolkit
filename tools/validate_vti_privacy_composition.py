#!/usr/bin/env python3
"""Validate bounded VTI privacy-composition specialist evidence reconciliation."""
from pathlib import Path
import sys
import yaml

FIXTURE = Path("examples/cross-spec/vti-privacy-composition/evidence.yaml")
EXPECTED_REQUIREMENTS = {"VTI-CMP-060", "VTI-CMP-061", "VTI-CMP-062", "VTI-CMP-063"}
EXPECTED_CONVERGENCE_REQUIREMENTS = {"VTI-CMP-064"}
EXPECTED_VTI_HEAD = "3cbd7300a4f46bb2518e2b4b485609e7b5432b58"


def validate() -> list[str]:
    doc = yaml.safe_load(FIXTURE.read_text(encoding="utf-8")) or {}
    evidence = doc.get("evidence") or {}
    requirements = set(evidence.get("vti_requirements") or [])
    if requirements != EXPECTED_REQUIREMENTS:
        raise AssertionError(f"privacy requirements mismatch: {sorted(requirements)}")

    inventory = evidence.get("evidence_inventory") or []
    by_id = {item.get("id"): item for item in inventory}
    if set(by_id) != {"DPIP-163", "RAHP-339", "RAHP-690", "RAHP-184"}:
        raise AssertionError("privacy evidence inventory is incomplete")

    dpip = by_id["DPIP-163"]
    if dpip.get("evidence_state") != "attributable-runtime-fail":
        raise AssertionError("DPIP-163 attributable runtime failure must remain visible")
    if dpip.get("observed_join") != "detected":
        raise AssertionError("DPIP-163 observed join must remain recorded")
    if "heartbeat-transport-correlation" not in (dpip.get("does_not_establish") or []):
        raise AssertionError("heartbeat transport must remain explicitly not established")

    coordination = by_id["RAHP-690"]
    if coordination.get("evidence_state") != "waiting-external":
        raise AssertionError("task-citation correlation dependency must remain waiting-external")

    req = evidence.get("requirement_evidence") or {}
    if set(req) != EXPECTED_REQUIREMENTS:
        raise AssertionError("requirement-level evidence states incomplete")
    if req["VTI-CMP-063"].get("state") != "specialist-evidence-required":
        raise AssertionError("minimisation evidence gap must remain explicit")

    if evidence.get("family_disposition") != "INDETERMINATE":
        raise AssertionError("privacy family must remain INDETERMINATE at this evidence state")
    if not evidence.get("blockers"):
        raise AssertionError("privacy blockers must remain explicit")
    rules = set(evidence.get("non_inference_rules") or [])
    if "valid proof != privacy PASS" not in rules:
        raise AssertionError("valid-proof/privacy boundary missing")
    if "not-evidenced != preserved" not in rules:
        raise AssertionError("not-evidenced boundary missing")

    extension = evidence.get("convergence_extension") or {}
    source = extension.get("vti_source") or {}
    if source.get("commit") != EXPECTED_VTI_HEAD:
        raise AssertionError("CMP-064 convergence evidence must be source-pinned to WD02")
    if set(extension.get("requirements") or []) != EXPECTED_CONVERGENCE_REQUIREMENTS:
        raise AssertionError("CMP-064 convergence requirement is missing")
    specialist = {item.get("id"): item for item in extension.get("specialist_evidence") or []}
    if set(specialist) != {"DPIP-271", "INTEROP-233"}:
        raise AssertionError("CMP-064 specialist evidence must include DPIP-271 and Interop-233")
    if specialist["DPIP-271"].get("state") != "terminal-indeterminate-evidence-required":
        raise AssertionError("DPIP-271 terminal INDETERMINATE must remain explicit")
    if specialist["INTEROP-233"].get("state") != "target-runtime-not-implemented":
        raise AssertionError("Interop-233 target-runtime boundary must remain not-implemented")
    if extension.get("disposition") != "INDETERMINATE":
        raise AssertionError("CMP-064 must remain INDETERMINATE for the current epoch")
    if extension.get("reconciliation_state") != "terminal-current-epoch":
        raise AssertionError("CMP-064 current epoch must have a terminal reconciliation state")
    extension_rules = set(extension.get("non_inference_rules") or [])
    if "not-implemented != privacy preserved" not in extension_rules:
        raise AssertionError("CMP-064 missing not-implemented/privacy non-inference rule")

    return [
        "DPIP-163 attributable correlation failure preserved",
        "heartbeat transport remains not-evidenced",
        "RAHP-690 remains waiting-external",
        "VTI-CMP-063 specialist evidence gap preserved",
        "family disposition remains INDETERMINATE",
        "VTI-CMP-064 current epoch reconciled as terminal INDETERMINATE",
    ]


def main() -> int:
    try:
        results = validate()
    except (OSError, yaml.YAMLError, AssertionError, ValueError) as exc:
        print(f"FAIL VTI privacy composition: {exc}", file=sys.stderr)
        return 1
    print("PASS VTI privacy composition evidence reconciliation")
    for result in results:
        print(f"- {result}")
    print("Boundary: scoped privacy failures and pending evidence do not become a family-level privacy PASS.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
