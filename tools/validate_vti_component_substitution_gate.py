#!/usr/bin/env python3
"""Validate the VTI component-substitution evidence gate."""
from pathlib import Path
import sys
import yaml

GATE = Path("examples/cross-spec/vti-component-substitution/evidence-gate.yaml")
EXPECTED = {"VTI-CMP-100", "VTI-CMP-101"}


def validate() -> list[str]:
    doc = yaml.safe_load(GATE.read_text(encoding="utf-8")) or {}
    gate = doc.get("evidence_gate") or {}
    if set(gate.get("vti_requirements") or []) != EXPECTED:
        raise AssertionError("component-substitution requirement set drifted")
    if gate.get("state") != "EVIDENCE_REQUIRED":
        raise AssertionError("component substitution must remain EVIDENCE_REQUIRED")
    inventory = gate.get("current_inventory") or {}
    if inventory.get("genuine_ab_pair_available") is not False:
        raise AssertionError("gate must not claim a genuine A/B pair")
    if inventory.get("dogwood_ab_satisfies_gate") is not False:
        raise AssertionError("Dogwood multi-context A/B must not be relabelled as substitution")
    shortcuts = set(gate.get("prohibited_shortcuts") or [])
    required_shortcuts = {
        "synthetic implementations created solely to satisfy the evidence gate",
        "component-local conformance used as a proxy for composition preservation",
        "one-implementation multi-context A/B evidence relabelled as substitution evidence",
    }
    if not required_shortcuts.issubset(shortcuts):
        raise AssertionError("component-substitution anti-shortcut boundaries incomplete")
    if len(gate.get("reentry_conditions") or []) < 2:
        raise AssertionError("component-substitution re-entry conditions missing")
    if gate.get("terminal_tranche_outcome") != "evidence-required":
        raise AssertionError("T10 terminal outcome must remain evidence-required")
    return [
        "VTI-CMP-100..101 mapped",
        "genuine A/B implementation pair absent",
        "synthetic substitution forbidden",
        "re-entry trigger explicit",
        "terminal tranche outcome: evidence-required",
    ]


def main() -> int:
    try:
        results = validate()
    except (OSError, yaml.YAMLError, AssertionError, ValueError) as exc:
        print(f"FAIL VTI component-substitution evidence gate: {exc}", file=sys.stderr)
        return 1
    print("PASS VTI component-substitution evidence gate")
    for result in results:
        print(f"- {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
