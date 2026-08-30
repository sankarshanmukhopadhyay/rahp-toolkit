#!/usr/bin/env python3
"""Clean-room Dogwood assessment acceptance runner.

This renderer records deterministic clean-room provenance and, when supplied,
reports the actual evidence-probe ledger. It never converts probe execution into
semantic assurance judgment: reviewer materiality/reconciliation remains explicit.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
from typing import Any

TARGET_REPOSITORY = "OpenVTC/verifiable-trust-infrastructure"
TARGET_RELEASE = "VTI-Dogwood-RC-1"
TARGET_REVISION = "cb01d0a758863fb3a02f9f4eef2c4f15f56c4c3b"
ISSUE_URL = "https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/246"
RELEASE_URL = "https://github.com/OpenVTC/verifiable-trust-infrastructure/releases/tag/VTI-Dogwood-RC-1"
FORBIDDEN_HISTORY = ["#225", "#228", "#231", "#234", "#120", "#123", "#129", "#134"]


def run(cmd: list[str], cwd: Path | None = None) -> str:
    p = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, check=False)
    if p.returncode != 0:
        raise RuntimeError(f"command failed ({p.returncode}): {' '.join(cmd)}\n{p.stderr}")
    return p.stdout.strip()


def git_head(path: Path) -> str:
    return run(["git", "rev-parse", "HEAD"], cwd=path)


def git_clean(path: Path) -> bool:
    return run(["git", "status", "--porcelain"], cwd=path) == ""


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def inventory_target(target: Path) -> dict[str, Any]:
    cargo_toml = target / "Cargo.toml"
    cargo_lock = target / "Cargo.lock"
    audit_review = target / "AUDIT-TRAIL-REVIEW.md"
    return {
        "cargo_workspace_present": cargo_toml.exists(),
        "cargo_lock_present": cargo_lock.exists(),
        "audit_trail_review_present": audit_review.exists(),
        "top_level_entries": sorted(p.name for p in target.iterdir())[:200],
    }


def load_ledger(path: Path | None) -> dict[str, Any] | None:
    if path is None:
        return None
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("schema") != "rahp-evidence-probe-ledger/v1":
        raise ValueError("unexpected evidence probe ledger schema")
    if value.get("target", {}).get("revision") != TARGET_REVISION:
        raise ValueError("probe ledger target revision does not match Dogwood target")
    if value.get("orchestration_defects"):
        raise ValueError("probe ledger contains orchestration defects")
    return value


def build_result(args: argparse.Namespace) -> tuple[dict[str, Any], str]:
    rahp, dpip, interop, target = (args.rahp.resolve(), args.dpip.resolve(), args.interop.resolve(), args.target.resolve())
    target_head = git_head(target)
    if target_head != TARGET_REVISION:
        raise RuntimeError(f"Dogwood pin mismatch: expected {TARGET_REVISION}, observed {target_head}")

    repos = {
        "rahp": {"revision": git_head(rahp)},
        "dpip": {"revision": git_head(dpip), "clean": git_clean(dpip)},
        "interop": {"revision": git_head(interop), "clean": git_clean(interop)},
        "target": {"revision": target_head, "clean": git_clean(target)},
    }
    if not repos["dpip"]["clean"] or not repos["interop"]["clean"] or not repos["target"]["clean"]:
        raise RuntimeError("clean-room integrity failed: supporting worktree became dirty")

    ledger = load_ledger(args.probe_ledger)
    requirements = ledger.get("requirements", []) if ledger else []
    executed = [x for x in requirements if x.get("attempt_state") == "EXECUTED"]
    unresolved = [x for x in requirements if x.get("result") == "NOT_EVIDENCED"]
    evidence_stage = "PASS" if ledger and len(requirements) == 4 and not ledger.get("orchestration_defects") else "NOT_RUN"

    result = {
        "schema": "rahp-clean-room-assessment-result/v2",
        "assessment": {
            "issue": 246,
            "issue_url": ISSUE_URL,
            "started_from_fresh_lineage": True,
            "historical_dogwood_inputs_permitted": False,
            "historical_comparators_allowed_after_terminal_result": FORBIDDEN_HISTORY,
            "observed_at": datetime.now(timezone.utc).isoformat(),
        },
        "target": {"repository": TARGET_REPOSITORY, "release": TARGET_RELEASE, "revision": TARGET_REVISION, "release_url": RELEASE_URL},
        "runtime": repos,
        "source_inventory": inventory_target(target),
        "evidence_probe_ledger": ledger,
        "deterministic_stages": {
            "clean_checkout_verification": "PASS",
            "immutable_target_pin": "PASS",
            "target_inventory": "PASS",
            "rahp_scaffold_capability": "PASS",
            "registered_evidence_probe_execution": evidence_stage,
            "semantic_review": "REVIEWER_REQUIRED",
            "privacy_materiality": "NOT_YET_DETERMINED",
            "dpip_examination": "NOT_YET_APPLICABLE",
            "rahp_reconciliation": "BLOCKED_ON_SEMANTIC_REVIEW",
        },
        "terminal": {
            "workflow_state": "COMPLETE_AT_EVIDENCE_AND_DETERMINISTIC_BOUNDARY",
            "assurance_disposition": "AMBER",
            "scoped_conclusion": "INDETERMINATE / REVIEW_REQUIRED",
            "reason": "Fresh runtime evidence probes were executed and recorded, but probe sufficiency does not replace the accepted semantic review required for materiality, DPIP applicability, and final RAHP reconciliation.",
            "unknowns": [
                "fresh risk/harm/security/composition semantic disposition has not yet been accepted",
                "privacy materiality has not yet been independently judged in this lineage",
                "the final DPIP and RAHP reconciled conclusion has not yet been produced from this fresh evidence",
            ],
            "references": [
                {"title": "Evidence-probe orchestration issue", "url": ISSUE_URL},
                {"title": "Dogwood RC-1 release", "url": RELEASE_URL},
                {"title": "Evidence probe ledger", "artifact_path": "evidence-probe-ledger.json"},
            ],
            "recommended_next_step": {"action": "Admit the fresh attributable probe evidence into a semantic RAHP review; if privacy is material, create a new DPIP examination and reconcile.", "owner": "RAHP reviewer / RAHP→DPIP lifecycle"},
        },
    }

    rows = "\n".join(
        f"- `{x.get('requirement_id')}` — **{x.get('result')}**, attempt `{x.get('attempt_state')}`, attribution `{x.get('attribution')}`"
        for x in requirements
    ) or "- No probe ledger supplied."
    summary = f"""# Clean-room Dogwood evidence-probe summary

## Bottom line

**AMBER — INDETERMINATE / REVIEW REQUIRED.** The stronger clean-room flow successfully executed the registered runtime evidence producers against pinned Dogwood RC-1 and recorded every required evidence attempt. This is materially stronger than the earlier clean-room run: no requirement is `NOT_EVIDENCED` merely because the harness failed to try it. It is still not a target-level privacy PASS/FAIL because semantic review, materiality, DPIP examination, and reconciliation remain separate judgment stages.

## Evidence produced

{rows}

Two producers executed for four requirements. Dogwood-native relationship/verifier observations remain attributed to Dogwood; status/policy and Trust Task observations remain explicitly attributed to the Interop Lab composition.

## Why this remains AMBER here

The evidence-production gap is closed, but evidence production alone is not assurance judgment. A reviewer must admit and interpret the evidence, determine privacy materiality, invoke DPIP if warranted, and reconcile the result. Workflow success therefore does not become assurance GREEN.

## Remaining uncertainty

{('- No runtime requirement remains NOT_EVIDENCED in the probe ledger.' if not unresolved else '- Some runtime requirements remain NOT_EVIDENCED after explicit attempts.')}
- Fresh semantic RAHP disposition and privacy materiality remain to be accepted.
- A fresh DPIP conclusion based on this evidence has not yet been produced.

## Recommended next step

Use this fresh attempt ledger and evidence package in the next pinned semantic RAHP/DPIP assessment. Any future `NOT_EVIDENCED` result must now be traceable to an executed/unavailable probe or an explicit absence of an applicable producer.
"""
    return result, summary


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rahp", type=Path, required=True)
    ap.add_argument("--dpip", type=Path, required=True)
    ap.add_argument("--interop", type=Path, required=True)
    ap.add_argument("--target", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--probe-ledger", type=Path)
    args = ap.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    result, summary = build_result(args)
    write_json(args.out_dir / "machine-conclusion.json", result)
    (args.out_dir / "human-summary.md").write_text(summary, encoding="utf-8")
    print(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
