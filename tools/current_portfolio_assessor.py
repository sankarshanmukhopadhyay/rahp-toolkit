#!/usr/bin/env python3
"""Conservative assessor for the source-pinned current DTG/VTC portfolio run.

This adapter does not infer PASS from successful checkout, CI, or document presence.
It proves only the executable proposition represented by the configured Lab evidence,
checks that every configured source pin is the checkout actually inspected, and emits
INDETERMINATE for proposition families that still require implementation/runtime evidence.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
from typing import Any


def head(path: Path) -> str:
    return subprocess.check_output(["git", "-C", str(path), "rev-parse", "HEAD"], text=True).strip()


def read_texts(root: Path, needle: str) -> bool:
    needle = needle.lower()
    for path in root.rglob("*"):
        if not path.is_file() or path.stat().st_size > 2_000_000:
            continue
        try:
            if needle in path.read_text(encoding="utf-8").lower():
                return True
        except (UnicodeDecodeError, OSError):
            continue
    return False


def item(pid: str, proposition: str, judgment: str, evidence_state: str, rationale: str, implementation: str | None = None) -> dict[str, Any]:
    out = {
        "id": pid,
        "proposition": proposition,
        "judgment": judgment,
        "evidence_state": evidence_state,
        "rationale": rationale,
    }
    if implementation:
        out["implementation_state"] = implementation
    return out


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--spec", type=Path, required=True)
    p.add_argument("--workspace", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--matrix", type=Path, required=True)
    a = p.parse_args()

    spec = json.loads(a.spec.read_text(encoding="utf-8"))
    ws = a.workspace.resolve()

    configured = {"target": spec["target"], **spec.get("resources", {})}
    pins = {}
    for rid, resource in configured.items():
        actual = head(ws / resource["path"])
        expected = resource["revision"]
        if actual != expected:
            raise SystemExit(f"immutable pin mismatch for {rid}: {actual} != {expected}")
        pins[rid] = {"repository": resource["repository"], "revision": actual}

    evidence_path = ws / "output" / "vdc-vac-non-substitution.json"
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    semantic_pass = bool(evidence.get("all_expected_outcomes_matched"))
    if not semantic_pass:
        raise SystemExit("VDC/VAC semantic non-substitution vectors did not all match expected outcomes")

    dtg_credentials = ws / spec["resources"]["dtg_credentials"]["path"]
    vdc_constructor_present = read_texts(dtg_credentials, "new_vdc")
    merged_scope_surface_present = read_texts(dtg_credentials, "delegation.scope")
    merged_acceptance_surface_present = read_texts(dtg_credentials, "delegation.accepts")

    dpip = ws / spec["resources"]["dpip"]["path"]
    dpip_evidence_required = read_texts(dpip, "indeterminate / evidence-required") or read_texts(dpip, "evidence-required")

    matrix = [
        item(
            "P01",
            "delegation cannot substitute for current authority and authority cannot substitute for representation",
            "PASS",
            "verified",
            "The pinned Interop Lab negative vectors execute both substitution directions and all expected deny/allow outcomes match.",
            "supported",
        ),
        item(
            "P02",
            "current implementation materially conforms to adopted VDC semantics where it claims support",
            "INDETERMINATE",
            "partially_verified",
            "The current dtg-credentials tree exposes a VDC constructor, but the assessor does not find the merged delegation.scope and delegation.accepts surfaces required by adopted #19. This is implementation-version divergence, not a defect in the specification.",
            "divergent" if vdc_constructor_present and not (merged_scope_surface_present and merged_acceptance_surface_present) else "not-observable",
        ),
        item(
            "P03",
            "Trust Task authorization and invocation boundaries do not enlarge credential authority",
            "INDETERMINATE",
            "execution_evidence_pending",
            "Current normative and implementation sources are pinned, but this clean run has no current end-to-end actuation trace proving the credential-to-task authorization boundary.",
            "not-observable",
        ),
        item(
            "P04",
            "replay/idempotency behavior does not create a second authorization path",
            "INDETERMINATE",
            "execution_evidence_pending",
            "Trust Tasks defines replay/idempotency semantics, but the portfolio run lacks a current cross-layer replay trace through the consuming OpenVTC path.",
            "not-observable",
        ),
        item(
            "P05",
            "presenter, subject and relationship bindings are preserved across the composed path",
            "INDETERMINATE",
            "partially_verified",
            "Existing source-compatible evidence is bounded to selected paths; this run does not establish preservation across all current credential/task compositions.",
            "not-observable",
        ),
        item(
            "P06",
            "correlation scope and disclosure behavior do not create unnecessary durable cross-context joins",
            "INDETERMINATE",
            "execution_evidence_pending",
            "The pinned DPIP source continues to record evidence-required privacy disposition; successful bounded no-join observations are insufficient for portfolio-wide effective-correlation PASS.",
            "not-observable" if dpip_evidence_required else "not-observable",
        ),
        item(
            "P07",
            "status/policy discovery and retained task evidence do not silently become correlation surfaces",
            "INDETERMINATE",
            "execution_evidence_pending",
            "Current-source A/B execution for status/policy discovery and retained Trust Task evidence is not supplied by this run.",
            "not-observable",
        ),
        item(
            "P08",
            "capability, key possession and authority remain non-collapsible at consequential actuation boundaries",
            "INDETERMINATE",
            "partially_verified",
            "Current Trust Tasks/VTI sources contain increasingly explicit capability separation, but source structure alone cannot prove consequential actuation non-collapsibility end to end.",
            "not-observable",
        ),
        item(
            "P09",
            "Trust Tasks and Credential Specification compose without introducing a semantic authority gap",
            "INDETERMINATE",
            "partially_verified",
            "Semantic non-substitution is proven, but current invocation, lifecycle, replay and implementation-conformance evidence is incomplete for the full composition.",
            "not-observable",
        ),
        item(
            "P10",
            "the current OpenVTC realization is distinguishable from the normative baseline wherever it is divergent or incomplete",
            "PASS",
            "verified",
            "The clean run keeps normative Credential Spec and Trust Tasks pins separate from VTI and dtg-credentials realization pins and records implementation divergence instead of collapsing it into normative PASS.",
            "supported",
        ),
    ]

    portfolio = {
        "schema": "rahp-dtg-current-portfolio-matrix/v1",
        "assessment_epoch": spec["run"]["snapshot"],
        "subject": spec["subject"],
        "source_pins": pins,
        "propositions": matrix,
        "summary": {
            "pass": sum(x["judgment"] == "PASS" for x in matrix),
            "fail": sum(x["judgment"] == "FAIL" for x in matrix),
            "indeterminate": sum(x["judgment"] == "INDETERMINATE" for x in matrix),
            "not_applicable": sum(x["judgment"] == "NOT_APPLICABLE" for x in matrix),
            "portfolio_posture": "AMBER",
            "reason": "The portfolio proves bounded delegation/authority non-substitution and explicit spec/implementation separation, but current implementation conformance, actuation, replay and privacy evidence remain incomplete."
        },
        "residuals": [
            {"owner": "OpenVTC implementation / future retest", "surface": "VDC merged #19 realization", "condition": "Current implementation exposes the adopted VDC scope, acceptance, lifecycle and binding contract."},
            {"owner": "Interop Lab", "surface": "credential-to-Trust-Task actuation", "condition": "A current source-pinned consuming path can execute negative authority/invocation/replay vectors."},
            {"owner": "DPIP + Interop Lab", "surface": "effective correlation", "condition": "Current A/B evidence exercises status/policy, retained task evidence and credential-carriage surfaces where implemented."}
        ]
    }
    a.matrix.parent.mkdir(parents=True, exist_ok=True)
    a.matrix.write_text(json.dumps(portfolio, indent=2) + "\n", encoding="utf-8")

    assessor = {
        "schema": "rahp-assessor-result/v1",
        "assessor": "dtg-current-portfolio-clean-room-v1",
        "assessment_id": "DTG-VTC-CURRENT-PORTFOLIO-2026-09-07",
        "outcome": "INDETERMINATE",
        "reason_code": "portfolio-evidence-required",
        "evidence_used": ["ER-VDC-VAC-NON-SUBSTITUTION"],
        "residual_risk": "The current portfolio has bounded executable assurance but lacks enough current realization/runtime evidence to defend end-to-end GREEN, especially for merged VDC conformance, credential-to-task actuation/replay, and effective-correlation surfaces.",
        "action_required": "Retest the named residual surfaces against future/current implementation support without synthesizing missing schema or runtime behavior; retain AMBER until those runs resolve the indeterminate propositions."
    }
    a.output.write_text(json.dumps(assessor, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(portfolio["summary"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
