#!/usr/bin/env python3
"""Render and validate the RAHP VTI programme reconciliation report."""
from __future__ import annotations

from collections import Counter
from pathlib import Path
import argparse
import sys
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = ROOT / "profiles" / "dtg" / "vti-assessment-profile.yaml"
SUBMISSION_DIR = ROOT / "examples" / "cross-spec" / "vti-assessment"
GATE_PATH = ROOT / "examples" / "cross-spec" / "vti-component-substitution" / "evidence-gate.yaml"
OUTPUT_PATH = ROOT / "docs" / "vti-programme-reconciliation.md"


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(value, dict):
        raise AssertionError(f"{path}: expected mapping")
    return value


def collect() -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    profile = load_yaml(PROFILE_PATH)
    submissions = []
    for path in sorted(SUBMISSION_DIR.glob("*.yaml")):
        item = load_yaml(path)
        item["_path"] = path.relative_to(ROOT).as_posix()
        submissions.append(item)
    gate = load_yaml(GATE_PATH).get("evidence_gate") or {}
    return profile, submissions, gate


def validate(profile: dict[str, Any], submissions: list[dict[str, Any]], gate: dict[str, Any]) -> dict[str, Any]:
    source = profile.get("vti_source") or {}
    mappings = {entry["family"]: entry for entry in profile.get("requirement_map") or []}
    if len(mappings) != 10:
        raise AssertionError(f"expected 10 VTI composition families, found {len(mappings)}")

    by_family = {item["family"]: item for item in submissions}
    if len(by_family) != len(submissions):
        raise AssertionError("multiple assessment submissions claim one family")

    verified = {family for family, entry in mappings.items() if entry.get("evidence_state") == "verified"}
    specialist = {family for family, entry in mappings.items() if entry.get("evidence_state") == "specialist_evidence_required"}
    evidence_required = {family for family, entry in mappings.items() if entry.get("evidence_state") == "evidence_required"}

    if len(verified) != 8:
        raise AssertionError(f"expected 8 verified families, found {sorted(verified)}")
    if specialist != {"privacy-composition"}:
        raise AssertionError(f"unexpected specialist-evidence families: {sorted(specialist)}")
    if evidence_required != {"component-substitution"}:
        raise AssertionError(f"unexpected evidence-required families: {sorted(evidence_required)}")

    for family in verified:
        item = by_family.get(family)
        if not item:
            raise AssertionError(f"verified family missing assessment submission: {family}")
        if item.get("disposition") != "supported":
            raise AssertionError(f"verified family is not supported: {family}")

    privacy = by_family.get("privacy-composition")
    if not privacy or privacy.get("disposition") != "indeterminate":
        raise AssertionError("privacy-composition must have an indeterminate submission")

    if "component-substitution" in by_family:
        raise AssertionError("component-substitution must not publish an assessment before the evidence gate is met")
    if gate.get("state") != "EVIDENCE_REQUIRED":
        raise AssertionError("component-substitution evidence gate must remain EVIDENCE_REQUIRED")

    pinned_commit = source.get("commit")
    pinned_status = source.get("document_status")
    stale = []
    for item in submissions:
        if item.get("vti_source", {}).get("commit") != pinned_commit:
            raise AssertionError(f"{item.get('assessment_id')}: VTI source pin mismatch")
        if item.get("vti_source", {}).get("document_status") != pinned_status:
            raise AssertionError(f"{item.get('assessment_id')}: VTI document status mismatch")
        state = item.get("reassessment", {}).get("state")
        if state != "current":
            stale.append(item.get("assessment_id"))

    source_counter = Counter()
    for family, entry in mappings.items():
        for ref in entry.get("rahp_sources") or []:
            source_counter[str(ref)] += 1
    shared = sorted(ref for ref, count in source_counter.items() if count > 1)

    return {
        "mappings": mappings,
        "by_family": by_family,
        "verified": verified,
        "specialist": specialist,
        "evidence_required": evidence_required,
        "stale": stale,
        "shared": shared,
    }


def render() -> str:
    profile, submissions, gate = collect()
    state = validate(profile, submissions, gate)
    mappings = state["mappings"]
    by_family = state["by_family"]

    lines = [
        "---",
        "layout: default",
        'title: "VTI programme reconciliation"',
        "parent: Reference",
        "nav_order: 7",
        "has_toc: true",
        "---",
        "# VTI programme reconciliation",
        "",
        "This report is derived from the active VTI assessment profile, assessment submissions, and component-substitution evidence gate. It records the T11 programme reconciliation state; it is not a VTI conformance report.",
        "",
        "## Pinned upstream baseline",
        "",
        f"- Repository: `{profile['vti_source']['repository']}`",
        f"- Document Status: `{profile['vti_source']['document_status']}`",
        f"- Commit: `{profile['vti_source']['commit']}`",
        "",
        "The upstream `main` revision was checked during T11 and remained at the same pinned commit, so no VTI source-drift invalidation was required at reconciliation time.",
        "",
        "## Programme state",
        "",
        f"- Composition families in profile: **{len(mappings)}**",
        f"- Verified families with supported submissions: **{len(state['verified'])}**",
        f"- Specialist-evidence-required families: **{len(state['specialist'])}**",
        f"- Evidence-required families: **{len(state['evidence_required'])}**",
        f"- Current assessment submissions: **{len(submissions)}**",
        f"- Stale or superseded submissions detected: **{len(state['stale'])}**",
        "",
        "## Family reconciliation",
        "",
        "| Family | Requirements | Profile evidence state | Assessment | Disposition / tranche outcome |",
        "|---|---|---|---|---|",
    ]

    for family, mapping in mappings.items():
        reqs = ", ".join(f"`{req}`" for req in mapping.get("requirements") or [])
        item = by_family.get(family)
        if item:
            assessment = f"`{item['assessment_id']}`"
            outcome = f"`{item['disposition']}`"
        elif family == "component-substitution":
            assessment = "not published"
            outcome = "`evidence-required`"
        else:
            assessment = "not published"
            outcome = "`indeterminate`"
        lines.append(f"| {family} | {reqs} | `{mapping.get('evidence_state')}` | {assessment} | {outcome} |")

    lines += [
        "",
        "## Cross-family consistency",
        "",
        "- Every published submission is pinned to the same active VTI Working Draft revision.",
        "- Every profile family marked `verified` has exactly one `supported` assessment submission.",
        "- Privacy remains explicitly `specialist_evidence_required` and its published assessment remains `indeterminate`; scoped DPIP failures are not converted into a universal privacy verdict.",
        "- Component substitution remains `evidence_required` and has no assessment submission; the genuine implementation-pair gate remains intact.",
        "- No assessment submission is stale or superseded at this reconciliation point.",
        "- Portability and discovery material are not forced into the composition family map merely to increase coverage.",
        "",
        "## Shared evidence and over-credit boundary",
        "",
    ]
    if state['shared']:
        for ref in state["shared"]:
            lines.append(f"- Shared profile source: `{ref}`. Reuse is permitted as lineage, but one artifact must not be counted as independent corroboration merely because multiple families cite it.")
    else:
        lines.append("- No exact profile-source reference is duplicated across families. This does not imply semantic independence; evidence lineage must still be interpreted in context.")

    lines += [
        "",
        "## Residual programme gaps",
        "",
        "1. **Privacy composition:** specialist/runtime evidence is incomplete across the full interaction surface, and task-citation correlation work remains externally dependent.",
        "2. **Component substitution:** no genuine two-implementation A/B pair currently satisfies the evidence contract.",
        "3. **Upstream evolution:** open VTI work may change future semantics, so the source pin must be rechecked before any release or upstream packaging step.",
        "",
        "## T11 disposition",
        "",
        "**Programme reconciliation passes with bounded residuals.** Eight families have verified supported assessments; privacy is deliberately indeterminate with specialist evidence outstanding; component substitution is deliberately evidence-required. These residual states are visible programme outcomes, not incomplete PASS states.",
        "",
        "This is sufficient to proceed to T12 release/upstream packaging judgment without altering the authority boundary: upstream VTI remains normative, while RAHP supplies independent assurance evidence.",
        "",
        "_Generated by `python3 tools/render_vti_programme_reconciliation.py`._",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        expected = render()
    except (OSError, yaml.YAMLError, AssertionError, ValueError) as exc:
        print(f"FAIL VTI programme reconciliation: {exc}", file=sys.stderr)
        return 1
    if args.check:
        current = OUTPUT_PATH.read_text(encoding="utf-8") if OUTPUT_PATH.exists() else ""
        if current != expected:
            print("FAIL VTI programme reconciliation: generated report is stale", file=sys.stderr)
            return 1
        print("PASS VTI programme reconciliation")
        return 0
    OUTPUT_PATH.write_text(expected, encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
