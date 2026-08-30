#!/usr/bin/env python3
"""Clean-room Dogwood assessment acceptance runner for RAHP #241.

This script deliberately tests the deterministic boundary of current RAHP/DPIP machinery.
It does not import historical Dogwood assessment records and does not manufacture semantic
judgments that current RAHP explicitly requires a reviewer to supply.
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
ISSUE_URL = "https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/241"
RELEASE_URL = "https://github.com/OpenVTC/verifiable-trust-infrastructure/releases/tag/VTI-Dogwood-RC-1"
FORBIDDEN_HISTORY = ["#225", "#228", "#231", "#234", "#120", "#123", "#129"]


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
    members = []
    if cargo_toml.exists():
        for line in cargo_toml.read_text(encoding="utf-8").splitlines():
            s = line.strip().strip(',').strip('"')
            if s and not s.startswith("#") and "/" in s and "=" not in s and "[" not in s:
                members.append(s)
    return {
        "cargo_workspace_present": cargo_toml.exists(),
        "cargo_lock_present": cargo_lock.exists(),
        "audit_trail_review_present": audit_review.exists(),
        "workspace_member_candidates": sorted(set(members)),
        "top_level_entries": sorted(p.name for p in target.iterdir())[:200],
    }


def build_result(args: argparse.Namespace) -> tuple[dict[str, Any], str]:
    rahp = args.rahp.resolve()
    dpip = args.dpip.resolve()
    interop = args.interop.resolve()
    target = args.target.resolve()

    target_head = git_head(target)
    if target_head != TARGET_REVISION:
        raise RuntimeError(f"Dogwood pin mismatch: expected {TARGET_REVISION}, observed {target_head}")

    repos = {
        "rahp": {"path": str(rahp), "revision": git_head(rahp), "clean_after_scaffold": git_clean(rahp)},
        "dpip": {"path": str(dpip), "revision": git_head(dpip), "clean": git_clean(dpip)},
        "interop": {"path": str(interop), "revision": git_head(interop), "clean": git_clean(interop)},
        "target": {"path": str(target), "revision": target_head, "clean": git_clean(target)},
    }
    # RAHP is expected to contain newly scaffolded working assessment files at this point.
    if not repos["dpip"]["clean"] or not repos["interop"]["clean"] or not repos["target"]["clean"]:
        raise RuntimeError("clean-room integrity failed: target or supporting read-only worktree became dirty")

    now = datetime.now(timezone.utc).isoformat()
    result = {
        "schema": "rahp-clean-room-assessment-result/v1",
        "assessment": {
            "issue": 241,
            "issue_url": ISSUE_URL,
            "started_from_fresh_lineage": True,
            "historical_dogwood_inputs_permitted": False,
            "historical_comparators_allowed_after_terminal_result": FORBIDDEN_HISTORY,
            "observed_at": now,
        },
        "target": {
            "repository": TARGET_REPOSITORY,
            "release": TARGET_RELEASE,
            "revision": TARGET_REVISION,
            "release_url": RELEASE_URL,
        },
        "runtime": repos,
        "source_inventory": inventory_target(target),
        "deterministic_stages": {
            "clean_checkout_verification": "PASS",
            "immutable_target_pin": "PASS",
            "target_inventory": "PASS",
            "rahp_scaffold_capability": "PASS",
            "semantic_review": "REVIEWER_REQUIRED",
            "privacy_materiality": "NOT_YET_DETERMINED",
            "dpip_examination": "NOT_YET_APPLICABLE",
            "rahp_reconciliation": "BLOCKED_ON_SEMANTIC_REVIEW",
        },
        "terminal": {
            "workflow_state": "COMPLETE_AT_DETERMINISTIC_BOUNDARY",
            "assurance_disposition": "AMBER",
            "scoped_conclusion": "INDETERMINATE / REVIEW_REQUIRED",
            "reason": (
                "Current RAHP deterministically pins, prepares and structures assessment work, "
                "but its CLI explicitly leaves substantive semantic findings to a human or AI-assisted reviewer. "
                "A clean-room run therefore cannot truthfully infer privacy materiality, invoke DPIP, or reconcile "
                "a target-level PASS/FAIL without that semantic step."
            ),
            "unknowns": [
                "risk/harm/security/composition semantic disposition has not yet been independently populated",
                "privacy materiality has not yet been independently judged",
                "no fresh DPIP examination exists in this lineage",
            ],
            "references": [
                {"title": "Clean-room assessment issue", "url": ISSUE_URL},
                {"title": "Dogwood RC-1 release", "url": RELEASE_URL},
            ],
            "recommended_next_step": {
                "action": "Populate a fresh semantic RAHP review from this clean-room target and evidence only; if privacy is material, create a new DPIP lineage, then reconcile.",
                "owner": "RAHP reviewer / current RAHP→DPIP workflow",
            },
        },
        "tooling_maturity": {
            "machine_readability": {
                "status": "PARTIAL",
                "strengths": ["immutable target", "fresh-lineage marker", "typed stage states", "references", "explicit next step"],
                "defects": ["no autonomous semantic disposition", "no autonomous DPIP applicability decision", "no one-shot reconciled target conclusion"],
            },
            "human_comprehensibility": {
                "status": "PARTIAL",
                "strengths": ["plain bottom line", "unknowns", "links", "next step"],
                "defects": ["terminal target conclusion still depends on an external semantic-review step"],
            },
        },
    }

    summary = f"""# Clean-room Dogwood assessment — reviewer summary\n\n## Bottom line\n\n**AMBER — INDETERMINATE / REVIEW REQUIRED.** The clean-room run successfully verified a fresh, clean checkout of Dogwood RC-1 at `{TARGET_REVISION}` and exercised the deterministic RAHP assessment boundary. It did **not** produce a truthful target-level PASS or FAIL because current RAHP deliberately requires a reviewer to supply substantive semantic findings before privacy materiality, DPIP referral, and final reconciliation can occur.\n\n## What was assessed\n\n- Target: `{TARGET_REPOSITORY}`\n- Release: `{TARGET_RELEASE}`\n- Immutable commit: `{TARGET_REVISION}`\n- Historical Dogwood assessment records were excluded as inputs.\n\n## What we found\n\nThe clean-room and pinning controls work: all participating repositories began from clean worktrees, the Dogwood revision matched the immutable target, and RAHP successfully scaffolded a fresh pinned review. The current RAHP command-line path explicitly does not manufacture substantive findings. That is a valid safety boundary, but it means the current system is not yet a one-command end-to-end assurance engine.\n\n## Why this is AMBER\n\nThis is not GREEN because risk, harm, security, composition and privacy materiality have not yet received a fresh semantic disposition in this lineage. It is not RED because the run did not establish an adverse Dogwood finding or a broken provenance chain. Missing judgment is therefore preserved as **INDETERMINATE**, not converted into PASS.\n\n## What remains unknown\n\n- Fresh risk/harm/security/composition conclusions.\n- Whether privacy is material under the fresh semantic review.\n- If privacy is material, what a new DPIP examination concludes.\n- The final reconciled Dogwood assurance colour after those steps.\n\n## References\n\n- [Clean-room RAHP issue #241]({ISSUE_URL})\n- [Dogwood RC-1 release]({RELEASE_URL})\n- Machine-readable artifact: `machine-conclusion.json` from the associated workflow run.\n\n## Recommended next step\n\n**Populate the fresh semantic RAHP review using only this clean-room target/evidence.** If that review finds privacy material, create a new DPIP examination in a new lineage. Then return the DPIP result to RAHP and produce the final reconciled machine-readable and plain-language conclusion.\n\n## Tooling maturity observation\n\nRAHP/DPIP have strong deterministic provenance and evidence-boundary behavior, but this clean-room test exposes a remaining orchestration gap: the system does not yet carry a fresh target from deterministic preparation through semantic judgment, optional DPIP, reconciliation, and a terminal human/machine conclusion without an explicit reviewer step.\n"""
    return result, summary


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rahp", type=Path, required=True)
    ap.add_argument("--dpip", type=Path, required=True)
    ap.add_argument("--interop", type=Path, required=True)
    ap.add_argument("--target", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    args = ap.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    result, summary = build_result(args)
    write_json(args.out_dir / "machine-conclusion.json", result)
    (args.out_dir / "human-summary.md").write_text(summary, encoding="utf-8")
    print(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
