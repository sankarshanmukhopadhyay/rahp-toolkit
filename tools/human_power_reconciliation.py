#!/usr/bin/env python3
"""Reconcile RAHP human-choice model results with DPIP specialist returns.

The reconciler preserves authority: DPIP supplies privacy-depth judgment; RAHP owns
human-power/harm judgment and the terminal bounded disposition. A specialist outcome
is evidence, not a mechanical replacement for the RAHP model result.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("human_choice_invariants", HERE / "human_choice_invariants.py")
_hci = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_hci)

SCHEMA = "rahp-human-power-reconciliation/v1"
DPIP_SCHEMA = "dpip-human-power-privacy-result/v1"
OUTCOMES = {"PASS", "FAIL", "INDETERMINATE"}


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate_dpip_result(result: dict[str, Any]) -> None:
    _require(isinstance(result, dict), "DPIP result must be an object")
    _require(result.get("schema") == DPIP_SCHEMA, f"DPIP result schema must be {DPIP_SCHEMA}")
    _require(result.get("outcome") in {"PASS", "FAIL", "INDETERMINATE", "NOT_APPLICABLE"}, "invalid DPIP outcome")
    evidence = result.get("evidence")
    _require(isinstance(evidence, dict), "DPIP evidence metadata is required")
    _require(isinstance(evidence.get("source_revision"), str) and evidence["source_revision"], "Interop source revision is required")
    _require(isinstance(result.get("deployment_claim_supported"), bool), "deployment_claim_supported must be boolean")


def _terminal(rahp: dict[str, Any], dpip: dict[str, Any]) -> tuple[str, list[str]]:
    """Compose results without allowing specialist status to replace RAHP authority."""
    rahp_outcome = rahp["outcome"]
    dpip_outcome = dpip["outcome"]
    handoff_material = bool(rahp.get("dpip_handoff_required"))

    if rahp_outcome == "FAIL":
        reasons = ["rahp-human-power-invariant-failed"]
        if dpip_outcome == "FAIL":
            reasons.append("dpip-privacy-depth-negative")
        elif dpip_outcome == "INDETERMINATE":
            reasons.append("dpip-privacy-depth-remains-indeterminate")
        return "FAIL", reasons

    if rahp_outcome == "INDETERMINATE":
        return "INDETERMINATE", ["rahp-human-power-evidence-incomplete", f"dpip:{dpip_outcome.lower()}"]

    # RAHP model is PASS. If privacy depth was material, DPIP must be sufficiently
    # resolved before the bounded composite proposition may pass.
    if handoff_material:
        if dpip_outcome == "PASS" or dpip_outcome == "NOT_APPLICABLE":
            return "PASS", ["rahp-human-power-invariant-passed", "dpip-specialist-obligation-resolved"]
        if dpip_outcome == "INDETERMINATE":
            return "INDETERMINATE", ["dpip-material-privacy-depth-indeterminate"]
        if dpip_outcome == "FAIL":
            return "INDETERMINATE", ["dpip-privacy-negative-but-human-power-attribution-not-established"]

    return "PASS", ["rahp-human-power-invariant-passed", "no-material-unresolved-specialist-obligation"]


def reconcile(
    proposition: str,
    rahp_result: dict[str, Any],
    dpip_result: dict[str, Any],
    *,
    rahp_issue: int,
    dpip_revision: str,
    interop_revision: str,
) -> dict[str, Any]:
    _require(rahp_result.get("outcome") in OUTCOMES, "invalid RAHP outcome")
    validate_dpip_result(dpip_result)
    _require(dpip_result["evidence"]["source_revision"] == interop_revision, "Interop revision mismatch")
    outcome, reasons = _terminal(rahp_result, dpip_result)

    deployment_claim_supported = bool(dpip_result["deployment_claim_supported"])
    residual: list[str] = []
    if not deployment_claim_supported:
        residual.append("target-deployment-behavior-not-established-by-synthetic-evidence")
    if dpip_result["outcome"] == "INDETERMINATE":
        dpip_residual = dpip_result.get("residual", {}).get("evidence_required", [])
        residual.extend(str(item) for item in dpip_residual)

    return {
        "schema": SCHEMA,
        "proposition": proposition,
        "rahp_issue": rahp_issue,
        "outcome": outcome,
        "reasons": reasons,
        "inputs": {"rahp": rahp_result, "dpip": dpip_result},
        "provenance": {
            "interop_revision": interop_revision,
            "dpip_revision": dpip_revision,
            "dpip_issue": dpip_result.get("dpip_issue"),
        },
        "deployment_claim_supported": deployment_claim_supported,
        "residual_evidence_requirements": residual,
        "authority": {
            "interop_lab": "execution observations",
            "dpip": "privacy-depth judgment",
            "rahp": "human-power/harm judgment and terminal bounded disposition",
        },
    }


def reconcile_bundle(bundle: dict[str, Any]) -> dict[str, Any]:
    _require(bundle.get("schema") == "rahp-human-power-reconciliation-input/v1", "invalid input bundle schema")
    dpip_results = {item["dpip_issue"]: item for item in bundle.get("dpip_results", [])}
    _require(190 in dpip_results and 191 in dpip_results, "DPIP #190 and #191 results are required")

    disclosure_context = bundle["rahp_contexts"]["compelled_disclosure"]
    proxy_context = bundle["rahp_contexts"]["proxy_inference"]
    disclosure_rahp = _hci.evaluate_disclosure_pressure(disclosure_context)
    proxy_rahp = _hci.evaluate_proxy_use(proxy_context)

    common = bundle["provenance"]
    results = [
        reconcile(
            "compelled-expanded-disclosure",
            disclosure_rahp,
            dpip_results[190],
            rahp_issue=161,
            dpip_revision=common["dpip_revision"],
            interop_revision=common["interop_revision"],
        ),
        reconcile(
            "consequential-proxy-inference",
            proxy_rahp,
            dpip_results[191],
            rahp_issue=179,
            dpip_revision=common["dpip_revision"],
            interop_revision=common["interop_revision"],
        ),
    ]
    return {
        "schema": "rahp-human-power-reconciliation-bundle/v1",
        "controller_issue": 670,
        "results": results,
        "portfolio_outcome": "FAIL" if any(r["outcome"] == "FAIL" for r in results) else (
            "INDETERMINATE" if any(r["outcome"] == "INDETERMINATE" for r in results) else "PASS"
        ),
        "portfolio_boundary": "bounded human-power tranche only; not a whole-portfolio assurance result",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    bundle = json.loads(args.input.read_text(encoding="utf-8"))
    result = reconcile_bundle(bundle)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    if args.check:
        _require(all(item["outcome"] in OUTCOMES for item in result["results"]), "non-terminal reconciliation")
        _require(result["portfolio_outcome"] in OUTCOMES, "invalid bounded portfolio outcome")
        print("PASS: human-power DPIP reconciliation is terminal and provenance-bound")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
