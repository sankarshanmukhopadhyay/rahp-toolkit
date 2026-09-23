#!/usr/bin/env python3
"""Reconcile DPIP evidence-obligation state into bounded RAHP assurance constraints."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

SCHEMA = "dpip-evidence-obligation/v1"
OUTPUT_SCHEMA = "rahp-dpip-evidence-obligation-reconciliation/v1"
UNRESOLVED = {"IDENTIFIED", "QUALIFIED", "EXPERIMENT_DESIGNED", "EVIDENCE_ACQUIRED", "REEVALUATED", "INDETERMINATE", "BLOCKED"}
RESOLVED = {"SATISFIED", "FALSIFIED", "SUPERSEDED"}


def require(ok: bool, msg: str) -> None:
    if not ok:
        raise ValueError(msg)


def reconcile(ob: dict[str, Any], *, dependent_rahp_outcome: str) -> dict[str, Any]:
    require(ob.get("schema") == SCHEMA, f"schema must be {SCHEMA}")
    require(dependent_rahp_outcome in {"PASS", "FAIL", "INDETERMINATE"}, "invalid RAHP outcome")
    require(ob.get("materiality") in {"material", "non-material"}, "invalid materiality")
    access = ob.get("access") or {}
    state = ob.get("state")
    blocker = access.get("blocker")
    acceptance = ob.get("residual_risk_acceptance")
    if state == "ACCEPTED_RESIDUAL_RISK":
        require(isinstance(acceptance, dict) and acceptance.get("authority") and acceptance.get("scope"), "accepted residual risk requires named authority and scope")

    assurability = "ASSURABILITY_GAP" if blocker in {"NO_OBSERVATION_SURFACE", "NO_INSTRUMENTATION", "NON_REPRODUCIBLE"} else ("EVIDENCE_BLOCKED" if access.get("status") == "BLOCKED" else "EVIDENTIABLE")
    material_unresolved = ob["materiality"] == "material" and state in UNRESOLVED

    if dependent_rahp_outcome == "FAIL":
        outcome = "FAIL"
        reason = "rahp-dependent-proposition-failed"
    elif dependent_rahp_outcome == "INDETERMINATE":
        outcome = "INDETERMINATE"
        reason = "rahp-dependent-proposition-indeterminate"
    elif material_unresolved:
        outcome = "INDETERMINATE"
        reason = "material-dpip-evidence-obligation-unresolved"
    else:
        outcome = "PASS"
        reason = "no-material-unresolved-dpip-evidence-obligation"

    deployment_claim_supported = not (blocker == "NO_TARGET" or (ob.get("evidence_maturity") or {}).get("minimum_required") in {"E3", "E4", "E5"} and state not in {"SATISFIED", "FALSIFIED"})
    return {
        "schema": OUTPUT_SCHEMA,
        "obligation_id": ob.get("id"),
        "dependent_rahp_outcome": dependent_rahp_outcome,
        "outcome": outcome,
        "reason": reason,
        "obligation_state": state,
        "materiality": ob["materiality"],
        "blocker": blocker,
        "assurability": assurability,
        "deployment_claim_supported": deployment_claim_supported,
        "authority_boundary": {
            "dpip": "privacy evidence sufficiency and obligation state",
            "rahp": "broader harm/power judgment and terminal bounded assurance",
            "rule": "DPIP privacy status does not mechanically establish broader harm"
        }
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", required=True, type=Path)
    p.add_argument("--rahp-outcome", default="PASS", choices=["PASS", "FAIL", "INDETERMINATE"])
    p.add_argument("--output", type=Path)
    p.add_argument("--check", action="store_true")
    args = p.parse_args()
    doc = json.loads(args.input.read_text(encoding="utf-8"))
    items = doc if isinstance(doc, list) else doc.get("obligations", [doc])
    require(isinstance(items, list) and items, "input must contain obligations")
    results = [reconcile(item, dependent_rahp_outcome=args.rahp_outcome) for item in items]
    bundle = {"schema": "rahp-dpip-evidence-obligation-reconciliation-bundle/v1", "results": results}
    text = json.dumps(bundle, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    if args.check:
        require(all(x["outcome"] in {"PASS", "FAIL", "INDETERMINATE"} for x in results), "invalid reconciliation outcome")
        print(f"PASS: {len(results)} DPIP obligation(s) reconciled under RAHP authority")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
