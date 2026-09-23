#!/usr/bin/env python3
"""End-to-end reviewed policy assurance research workflow for RAHP issue #662."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from policy_relationships import build_policy_relationship_model
from policy_review import analysis_records, map_reviewed_risk_hypotheses, review_subject
from policy_structure import ingest_structured_policy
from policy_subject import compare_runtime, diff_subjects, map_risk_hypotheses

ASSESSMENT_SCHEMA = "rahp-policy-assessment-research/v2"


def _baseline_analysis_records(subject: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "id": item["id"],
            "analysis_text": item["normalized_proposition"],
            "type": item["type"],
            "ambiguity_signals": item["ambiguity_signals"],
            "source_proposition_ids": [item["id"]],
            "source_spans": [item["source_span"]],
            "review_state": "source-baseline",
            "derivation": "direct-source-statement",
        }
        for item in subject["propositions"]
    ]


def evidence_work_queue(
    subject: dict[str, Any],
    mapping: dict[str, Any],
    reviewed_records: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    records = reviewed_records or _baseline_analysis_records(subject)
    by_id = {item["id"]: item for item in records}
    queue: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()

    def add(
        proposition_id: str,
        evidence_class: str,
        question: str,
        route: str,
        *,
        why_required: str,
        materiality: str = "context-dependent",
    ) -> None:
        key = (proposition_id, question)
        if key in seen:
            return
        seen.add(key)
        record = by_id.get(proposition_id)
        source_ids = list((record or {}).get("source_proposition_ids") or [proposition_id])
        obligation_seed = "|".join([proposition_id, evidence_class, route, question])
        obligation_id = "peo-" + hashlib.sha256(obligation_seed.encode("utf-8")).hexdigest()[:16]
        queue.append(
            {
                "obligation_id": obligation_id,
                "proposition_id": proposition_id,
                "source_proposition_ids": source_ids,
                "analysis_text": (record or {}).get("analysis_text"),
                "evidence_class": evidence_class,
                "question": question,
                "why_required": why_required,
                "materiality": materiality,
                "route": route,
                "state": "evidence-required",
                "terminal_effect": "none-until-evidence-evaluated",
            }
        )

    for record in records:
        pid = record["id"]
        ptype = record["type"]
        if ptype == "termination":
            add(pid, "runtime-observation", "Can the adverse action occur with the notice and review conditions represented by the reviewed proposition?", "interop-or-runtime-test", why_required="Policy text can declare an adverse-action boundary but cannot establish runtime enforcement behavior.", materiality="high")
            add(pid, "user-experience", "Can an affected person understand, challenge and recover from the adverse action in practice?", "ux-evidence", why_required="A declared remedy or notice path does not establish that an affected person can use it effectively.", materiality="high")
        elif ptype == "retention":
            add(pid, "runtime-observation", "Do observed storage and deletion behaviours match the reviewed retention boundary?", "runtime-data-flow-evidence", why_required="A retention declaration is governance-source evidence, not proof of storage or deletion behavior.", materiality="high")
            add(pid, "specialist", "Does the retention proposition raise privacy-specific minimisation or proportionality questions?", "DPIP-or-privacy-specialist", why_required="Retention can create privacy-specific harms that require specialist analysis outside the policy adapter's authority.", materiality="context-dependent")
        elif ptype == "disclosure":
            add(pid, "runtime-observation", "Do observed data flows and recipients match the reviewed disclosure proposition?", "runtime-data-flow-evidence", why_required="A disclosure declaration cannot establish the actual recipients, purposes, or data flows at runtime.", materiality="high")
            add(pid, "specialist", "Does the disclosure proposition require privacy-specific purpose or recipient analysis?", "DPIP-or-privacy-specialist", why_required="Disclosure scope can require privacy-specific purpose and recipient analysis outside the adapter's authority.", materiality="context-dependent")
        elif ptype == "delegation":
            add(pid, "runtime-observation", "Is downstream authority constrained to the scope represented by the reviewed proposition?", "authority-runtime-evidence", why_required="A delegation statement does not prove that delegated runtime authority is technically constrained to the represented scope.", materiality="high")
        if "legal_dependency" in record.get("ambiguity_signals", []):
            add(pid, "specialist", "What jurisdiction-dependent meaning, if any, changes the interpretation of this proposition?", "qualified-legal-or-domain-specialist", why_required="The proposition contains a legal dependency that the policy adapter must not resolve automatically.", materiality="high")

    for hypothesis in mapping["hypotheses"]:
        add(
            hypothesis["proposition_id"],
            "assurance-evidence",
            f"What evidence would confirm or falsify the {hypothesis['risk_pattern']} hypothesis?",
            "RAHP-assessment",
            why_required="The reviewed proposition triggered a portable RAHP risk pattern; evidence is required to confirm, bound, or falsify that hypothesis.",
            materiality="context-dependent",
        )

    for gap in mapping["evidence_gaps"]:
        if gap["id"] == "policy-redress-evidence-gap":
            termination = next((p for p in records if p["type"] == "termination"), None)
            if termination:
                add(
                    termination["id"],
                    "governance-or-ux-evidence",
                    "Is a correction, appeal or redress path defined elsewhere and usable in practice?",
                    "policy-review-plus-ux-evidence",
                    why_required="The assessed source does not establish whether a usable redress path exists elsewhere; absence of text is not evidence of absence.",
                    materiality="high",
                )
    return queue


def synthesize_assessment(
    subject: dict[str, Any],
    *,
    review: dict[str, Any] | None = None,
    runtime_records: list[dict[str, Any]] | None = None,
    previous_subject: dict[str, Any] | None = None,
    related_subjects: list[dict[str, Any]] | None = None,
    reference_decisions: list[dict[str, Any]] | None = None,
    precedence_decisions: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    review = review or review_subject(subject)
    analytical = analysis_records(subject, review)
    mapping = map_reviewed_risk_hypotheses(subject, analytical)
    runtime = compare_runtime(subject, runtime_records or []) if runtime_records is not None else None
    delta = diff_subjects(previous_subject, subject) if previous_subject is not None else None
    relationships = build_policy_relationship_model(
        subject,
        related_subjects=related_subjects,
        reference_decisions=reference_decisions,
        precedence_decisions=precedence_decisions,
    ) if subject.get("document_structure") is not None else None
    queue = evidence_work_queue(subject, mapping, analytical)

    source_by_id = {item["id"]: item for item in subject["propositions"]}
    unresolved_review = [record for record in review["records"] if record["review_state"] == "judgment-required"]
    for record in unresolved_review:
        pid = record["proposition_id"]
        queue.append(
            {
                "proposition_id": pid,
                "source_proposition_ids": [pid],
                "analysis_text": source_by_id[pid]["normalized_proposition"],
                "evidence_class": "human-judgment",
                "obligation_id": "pjo-" + hashlib.sha256(("review|" + pid).encode("utf-8")).hexdigest()[:16],
                "question": "Resolve the extraction ambiguity before this proposition can enter reviewed RAHP analysis.",
                "why_required": "The source proposition carries unresolved ambiguity and is barred from reviewed RAHP analysis until explicit human judgment.",
                "materiality": "context-dependent",
                "route": "policy-reviewer",
                "state": "judgment-required",
                "terminal_effect": "none-until-judgment-resolved",
            }
        )

    relationship_unresolved = (relationships or {}).get("unresolved_judgment_count", 0)
    unresolved_total = len(unresolved_review) + relationship_unresolved
    return {
        "schema": ASSESSMENT_SCHEMA,
        "experimental": True,
        "terminal_assurance": False,
        "source": subject["source"],
        "policy_text_establishes": subject["propositions"],
        "review": review,
        "reviewed_analysis": analytical,
        "policy_relationships": relationships,
        "rahp_infers": mapping,
        "evidence_shows": runtime,
        "change_impact": delta,
        "evidence_work_queue": queue,
        "current_disposition": {
            "state": "JUDGMENT_REQUIRED" if unresolved_total else "EVIDENCE_REQUIRED",
            "unresolved_review_count": len(unresolved_review),
            "unresolved_relationship_count": relationship_unresolved,
            "evidence_item_count": len(queue),
            "reason": "Research output is non-terminal; analysis consumes only reviewed propositions, while unresolved review/relationship questions and evidence obligations remain explicit.",
        },
        "authority_boundary": {
            **subject["authority_boundary"],
            "rejected_propositions_enter_analysis": False,
            "unreviewed_ambiguous_propositions_enter_analysis": False,
            "reviewed_precedence_is_legal_conclusion": False,
        },
    }


def render_markdown(assessment: dict[str, Any]) -> str:
    source = assessment["source"]
    lines = [
        "# Experimental RAHP Policy Assurance Assessment",
        "",
        "> Research output only. This is not legal advice, regulatory certification, or a terminal RAHP assurance result.",
        "",
        "## Source",
        "",
        f"- URI: `{source['uri']}`",
        f"- Version: `{source['version']}`",
        f"- SHA-256: `{source['sha256']}`",
        "",
        "## What the policy text establishes",
        "",
    ]
    for proposition in assessment["policy_text_establishes"]:
        flags = ", ".join(proposition["ambiguity_signals"]) or "none"
        lines.extend(
            [
                f"### {proposition['id']} — {proposition['type']}",
                "",
                f"> {proposition['source_span']['text'].replace(chr(10), ' ')}",
                "",
                f"Ambiguity signals: `{flags}`. Judgment required: `{str(proposition['judgment_required']).lower()}`.",
                "",
            ]
        )

    lines.extend(["## Reviewed proposition set used for analysis", ""])
    reviewed = assessment.get("reviewed_analysis") or []
    if not reviewed:
        lines.append("No proposition has crossed the review boundary into analysis.\n")
    for record in reviewed:
        lines.append(
            f"- `{record['id']}` ({record['review_state']}, {record['type']}) from `{', '.join(record['source_proposition_ids'])}`: {record['analysis_text']}"
        )

    relationships = assessment.get("policy_relationships")
    if relationships is not None:
        lines.extend(["", "## Definitions and policy relationships", ""])
        lines.append(f"- Definition-use candidates: {len(relationships['definition_bindings'])}")
        lines.append(f"- Referenced documents/anchors: {len(relationships['references'])}; automatic traversal: **false**")
        lines.append(f"- Precedence candidates: {len(relationships['precedence_candidates'])}")
        lines.append(f"- Cross-document definition conflicts: {len(relationships['definition_conflicts'])}")
        lines.append(f"- Unresolved relationship judgments: {relationships['unresolved_judgment_count']}")

    lines.extend(["", "## What RAHP infers", ""])
    hypotheses = assessment["rahp_infers"]["hypotheses"]
    if not hypotheses:
        lines.append("No bounded portable risk-pattern hypothesis was generated from the reviewed proposition set.\n")
    for item in hypotheses:
        lines.extend(
            [
                f"- **{item['risk_pattern']} — {item['risk_name']}** from `{item['proposition_id']}`: {item['rationale']}",
                "  This remains a hypothesis and requires evidence.",
            ]
        )

    lines.extend(["", "## What remains uncertain / what to investigate next", ""])
    for item in assessment["evidence_work_queue"]:
        lines.append(f"- `{item['obligation_id']}` · `{item['evidence_class']}` via **{item['route']}** for `{item['proposition_id']}`: {item['question']}")
        lines.append(f"  Why required: {item['why_required']} Materiality: `{item['materiality']}`.")

    disposition = assessment["current_disposition"]
    lines.extend(
        [
            "",
            "## Current disposition",
            "",
            f"**{disposition['state']}** — {disposition['reason']}",
            "",
        ]
    )

    if assessment.get("change_impact") is not None:
        delta = assessment["change_impact"]
        lines.extend(
            [
                "## Policy-change impact",
                "",
                f"Reassessment required: **{str(delta['reassessment_required']).lower()}**.",
                f"Added: {len(delta['added'])}; removed: {len(delta['removed'])}; changed: {len(delta['changed'])}.",
                "",
            ]
        )

    if assessment.get("evidence_shows") is not None:
        lines.extend(["## Runtime comparison", ""])
        comparisons = assessment["evidence_shows"]["comparisons"]
        if not comparisons:
            lines.append("No runtime observations supplied.\n")
        for item in comparisons:
            lines.append(f"- `{item['proposition_id']}`: **{item['state']}** against `{item.get('evidence_ref')}` (non-terminal).")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _read_json(path: str | None) -> Any:
    if path is None:
        return None
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the experimental RAHP reviewed policy assurance workflow")
    parser.add_argument("source", help="plain-text or Markdown policy file")
    parser.add_argument("--uri", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--retrieved-at")
    parser.add_argument("--review", help="JSON array of accept/amend/reject/split/merge review decisions")
    parser.add_argument("--runtime", help="JSON array of runtime-observation records")
    parser.add_argument("--previous-subject", help="previous source-pinned policy subject JSON")
    parser.add_argument("--related-subject", action="append", default=[], help="related structured policy subject JSON; may be repeated")
    parser.add_argument("--reference-decisions", help="JSON array of incorporated/reference review decisions")
    parser.add_argument("--precedence-decisions", help="JSON array of explicit precedence decisions")
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    args = parser.parse_args()

    subject = ingest_structured_policy(
        Path(args.source).read_text(encoding="utf-8"),
        source_uri=args.uri,
        source_version=args.version,
        retrieved_at=args.retrieved_at,
    )
    review = review_subject(subject, _read_json(args.review)) if args.review else None
    related = [_read_json(path) for path in args.related_subject]
    assessment = synthesize_assessment(
        subject,
        review=review,
        runtime_records=_read_json(args.runtime),
        previous_subject=_read_json(args.previous_subject),
        related_subjects=related,
        reference_decisions=_read_json(args.reference_decisions),
        precedence_decisions=_read_json(args.precedence_decisions),
    )
    if args.format == "json":
        print(json.dumps(assessment, indent=2, sort_keys=True))
    else:
        print(render_markdown(assessment), end="")
    return 0
