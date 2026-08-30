#!/usr/bin/env python3
"""Prepare a durable GitHub review issue for a declared cross-specification assessment."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any
import yaml

ROOT = Path(__file__).resolve().parent.parent


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a mapping")
    return data


def composition(registry: dict[str, Any], composition_id: str) -> dict[str, Any]:
    item = next((x for x in registry.get("compositions", []) if x.get("id") == composition_id), None)
    if not item:
        raise ValueError(f"Unknown composition id: {composition_id}")
    if not item.get("runnable"):
        raise ValueError(f"Composition {composition_id} is declared but not yet runnable")
    if not item.get("assessment"):
        raise ValueError(f"Runnable composition {composition_id} has no assessment path")
    return item


def md_list(values: list[str]) -> str:
    return ", ".join(f"`{v}`" for v in values) if values else "None declared"


def upstream_targets(item: dict[str, Any]) -> list[str]:
    return [c["repository"] for c in item.get("components", []) if c.get("upstream_issue_target")]


def render_issue(item: dict[str, Any], assessment: dict[str, Any], run_url: str = "", assessment_lineage: str = "") -> str:
    review = assessment.get("review") or assessment
    summary = review.get("summary") or {}
    target = review.get("target") or {}
    findings = review.get("findings") or []
    repos = [c.get("repository", "") for c in item.get("components", [])]
    lines = [
        f"# Cross-specification pressure test: {item['title']}", "",
        "> This is the durable RAHP review record for a manually invoked cross-specification pressure test. It is evidence for Working Group review; it does not itself change either upstream specification.", "",
        "## Review status", "",
        f"- Profile: `{item.get('_profile_id', 'unknown')}`",
        f"- Composition ID: `{item['id']}`",
        f"- Priority: **{item.get('priority', 'unspecified')}**",
        f"- RAHP assessment: `{item['assessment']}`",
        f"- Assessment status: **{review.get('status', 'unknown')}**",
        f"- Reviewed on: `{review.get('reviewed_on', 'unknown')}`",
        f"- Source repositories: {md_list(repos)}",
    ]
    if assessment_lineage:
        lines += [
            f"- Clean-room lineage: `{assessment_lineage}`",
            f"<!-- rahp-clean-room-lineage:{assessment_lineage} -->",
        ]
    if run_url:
        lines.append(f"- GitHub Actions run: {run_url}")
    lines += [
        "", "## Executive assessment", "",
        summary.get("overall_assessment", "No executive assessment recorded."), "",
        f"Open findings: **{summary.get('open_count', sum(1 for f in findings if f.get('status') == 'open'))}** of **{summary.get('finding_count', len(findings))}**.", "",
        "## Scope and provenance", "",
        f"- Reviewed composition/version: `{target.get('version', 'not recorded')}`",
        f"- Evidence grade: `{review.get('evidence_grade', item.get('evidence_grade', 'not recorded'))}`",
        f"- Evidence pin: `{target.get('commit') or target.get('evidence_pin', 'not recorded')}`",
        f"- RAHP version: `{(review.get('reviewed_against') or {}).get('rahp_version', 'not recorded')}`",
        f"- Corpus: `{item.get('corpus_id', 'not recorded')}`",
        f"- Assurance focus: {md_list(item.get('assurance_focus', []))}", "",
        "### Included", "",
    ]
    lines += [f"- {x}" for x in (review.get("scope") or {}).get("included", [])] or ["- Not recorded."]
    lines += ["", "### Excluded", ""]
    lines += [f"- {x}" for x in (review.get("scope") or {}).get("excluded", [])] or ["- Not recorded."]
    lines += ["", "## Findings", "", "| ID | Severity | Finding | Primary disposition |", "|---|---|---|---|"]
    for f in findings:
        lines.append(f"| `{f.get('id')}` | **{f.get('severity', 'Unknown')}** | {f.get('title', '')} | `{f.get('primary_disposition', 'unassigned')}` |")
    for f in findings:
        lines += [
            "", f"### {f.get('id')}: {f.get('title')}", "",
            f"**Status:** `{f.get('status', 'unknown')}`  ",
            f"**Severity:** `{f.get('severity', 'unknown')}`  ",
            f"**Primary disposition:** `{f.get('primary_disposition', 'unassigned')}`  ",
            f"**Secondary dispositions:** {md_list(f.get('secondary_dispositions', []))}", "",
            f"**Harm / failure mode:** {f.get('harm', 'Not recorded.')}", "",
            f"**Recommendation:** {f.get('recommendation', 'Not recorded.')}", "",
            f"**Scenarios:** {md_list(f.get('scenarios', []))}", "",
            "**Evidence:**",
        ]
        evidence = f.get("evidence") or []
        lines += [f"- `{e.get('source', '')}` — {e.get('observation', '')}" for e in evidence] or ["- No evidence entry recorded."]
    targets = upstream_targets(item)
    lines += [
        "", "## Upstream issue candidates", "",
        "> Use this section when a finding needs normative or repository-level remediation upstream. File upstream only after WG/maintainer triage confirms the target repository and ownership. When filing, include the URL of this RAHP issue as the provenance link.", "",
        f"Declared upstream targets: {md_list(targets)}", "",
    ]
    for f in findings:
        if f.get("status") != "open":
            continue
        lines += [
            f"### Upstream candidate — {f.get('id')}", "",
            f"**Suggested title:** `[Cross-spec][{f.get('id')}] {f.get('title')}`", "",
            f"**Candidate repositories:** {md_list(targets)}", "",
            "**Problem statement**", "",
            f.get("harm", "Not recorded."), "",
            "**Requested clarification/change**", "",
            f.get("recommendation", "Not recorded."), "",
            "**RAHP evidence**", "",
            f"- Composition: `{item['id']}`",
            f"- Scenarios: {md_list(f.get('scenarios', []))}",
            f"- Assessment path: `{item['assessment']}`",
            "- Provenance: link back to this RAHP review issue.", "",
            "**Upstream triage checklist**", "",
            "- [ ] Confirm this finding belongs in this upstream repository.",
            "- [ ] Identify the normative or guidance text that owns the semantic contract.",
            "- [ ] Preserve the RAHP issue URL and finding ID in the upstream issue.",
            "- [ ] Record the upstream issue URL back in this RAHP issue.",
            "- [ ] Define a retest condition before closing the RAHP finding.", "",
        ]
    lines += [
        "## WG review and disposition", "",
        "- [ ] WG/maintainers reviewed the assessment scope and evidence pins.",
        "- [ ] Each open finding has an agreed owner or explicit external-governance disposition.",
        "- [ ] Upstream issues, where needed, are linked from this issue.",
        "- [ ] Retest conditions are recorded for upstream-remediated findings.",
        "- [ ] Closure is based on evidence, not only discussion consensus.", "",
        "## Assurance boundary", "",
        "A component-level pass does not imply a composition-level pass. This issue records the seam assessment and its disposition history; upstream repositories remain authoritative for their own normative changes.",
    ]
    return "\n".join(lines).rstrip() + "\n"


def event_for(item: dict[str, Any], body: str, assessment_lineage: str = "") -> dict[str, Any]:
    profile_id = item.get("_profile_id", "external")
    labels = item.get("_issue_labels") or ["assessment-required", "cross-specification"]
    return {
        "assessment_key": (
            f"{profile_id}:cross-spec:{item['id']}:lineage:{assessment_lineage}"
            if assessment_lineage
            else f"{profile_id}:cross-spec:{item['id']}"
        ),
        "source": "manual-cross-spec-pressure-test",
        "title": f"[Cross-spec] {item['title']} pressure-test review",
        "body": body,
        "labels": labels,
        "repository": " + ".join(c.get("repository", "") for c in item.get("components", [])),
        "theme": "cross-specification-assurance",
        "affected_reviews": [item.get("assessment", "")],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("composition_id")
    ap.add_argument("--registry", type=Path, required=True, help="Profile-owned cross-spec registry path")
    ap.add_argument("--output", type=Path, default=ROOT / "build/cross-spec-review.md")
    ap.add_argument("--events", type=Path, default=ROOT / "build/cross-spec-review-events.json")
    ap.add_argument("--run-url", default="")
    ap.add_argument("--assessment-lineage", default="", help="Optional clean-room lineage discriminator")
    args = ap.parse_args()
    registry_path = args.registry if args.registry.is_absolute() else ROOT / args.registry
    registry = load_yaml(registry_path)
    if registry.get("deprecated") and registry.get("canonical_registry"):
        registry = load_yaml(ROOT / registry["canonical_registry"])
    item = composition(registry, args.composition_id)
    profile = registry.get("profile") or {}
    item["_profile_id"] = profile.get("id", "external")
    item["_issue_labels"] = profile.get("issue_labels") or ["assessment-required", "cross-specification"]
    assessment = load_yaml(ROOT / item["assessment"])
    body = render_issue(item, assessment, args.run_url, args.assessment_lineage.strip())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(body, encoding="utf-8")
    args.events.write_text(json.dumps([event_for(item, body, args.assessment_lineage.strip())], indent=2) + "\n", encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
