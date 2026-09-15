#!/usr/bin/env python3
"""End-to-end research workflow for RAHP policy-as-subject experiments (#662).

The workflow deliberately keeps extraction, human review, analytical inference,
evidence requests and presentation as separate records. It does not integrate
with the stable RAHP controller while the capability remains experimental.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from policy_subject import (
    compare_runtime,
    diff_subjects,
    ingest_policy,
    map_risk_hypotheses,
    validate_subject,
)

REVIEW_SCHEMA = "rahp-policy-review/v1"
ASSESSMENT_SCHEMA = "rahp-policy-assessment-research/v1"


def review_subject(subject: dict[str, Any], decisions: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Create review lineage without overwriting machine extraction.

    Supported review actions are accept, amend and reject. Ambiguous propositions
    without an explicit decision stay judgment-required; unambiguous propositions
    may be accepted by the deterministic research baseline, but this is recorded as
    `baseline-accepted`, not as human judgment.
    """
    errors = validate_subject(subject)
    if errors:
        raise ValueError("invalid policy subject: " + "; ".join(errors))

    supplied = {item.get("proposition_id"): item for item in decisions or []}
    known_ids = {item["id"] for item in subject["propositions"]}
    unknown = sorted(set(supplied) - known_ids)
    if unknown:
        raise ValueError("review decisions reference unknown propositions: " + ", ".join(unknown))

    reviewed: list[dict[str, Any]] = []
    for proposition in subject["propositions"]:
        decision = supplied.get(proposition["id"])
        if decision is None:
            state = "judgment-required" if proposition["judgment_required"] else "baseline-accepted"
            reviewed.append(
                {
                    "proposition_id": proposition["id"],
                    "machine_proposal": proposition["normalized_proposition"],
                    "reviewed_proposition": proposition["normalized_proposition"] if state == "baseline-accepted" else None,
                    "review_state": state,
                    "reviewer": None,
                    "rationale": "Deterministic direct-source proposition requires explicit review because ambiguity was detected."
                    if state == "judgment-required"
                    else "Direct source statement accepted by deterministic research baseline; no human-review claim is made.",
                }
            )
            continue

        action = decision.get("action")
        reviewer = decision.get("reviewer")
        rationale = decision.get("rationale")
        if action not in {"accept", "amend", "reject"}:
            raise ValueError(f"unsupported review action for {proposition['id']}: {action}")
        if action in {"amend", "reject"} and not rationale:
            raise ValueError(f"{action} requires rationale for {proposition['id']}")
        if action == "amend" and not str(decision.get("text") or "").strip():
            raise ValueError(f"amend requires replacement text for {proposition['id']}")

        reviewed.append(
            {
                "proposition_id": proposition["id"],
                "machine_proposal": proposition["normalized_proposition"],
                "reviewed_proposition": (
                    proposition["normalized_proposition"]
                    if action == "accept"
                    else decision.get("text")
                    if action == "amend"
                    else None
                ),
                "review_state": {"accept": "accepted", "amend": "amended", "reject": "rejected"}[action],
                "reviewer": reviewer,
                "rationale": rationale,
            }
        )

    return {
        "schema": REVIEW_SCHEMA,
        "subject_sha256": subject["source"]["sha256"],
        "records": reviewed,
    }


def evidence_work_queue(subject: dict[str, Any], mapping: dict[str, Any]) -> list[dict[str, Any]]:
    by_id = {item["id"]: item for item in subject["propositions"]}
    queue: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()

    def add(proposition_id: str, evidence_class: str, question: str, route: str) -> None:
        key = (proposition_id, question)
        if key in seen:
            return
        seen.add(key)
        queue.append(
            {
                "proposition_id": proposition_id,
                "source_text": by_id[proposition_id]["source_span"]["text"],
                "evidence_class": evidence_class,
                "question": question,
                "route": route,
                "state": "evidence-required",
            }
        )

    for proposition in subject["propositions"]:
        pid = proposition["id"]
        ptype = proposition["type"]
        if ptype == "termination":
            add(pid, "runtime-observation", "Can the adverse action occur with the notice and review conditions represented by the policy?", "interop-or-runtime-test")
            add(pid, "user-experience", "Can an affected person understand, challenge and recover from the adverse action in practice?", "ux-evidence")
        elif ptype == "retention":
            add(pid, "runtime-observation", "Do observed storage and deletion behaviours match the declared retention boundary?", "runtime-data-flow-evidence")
            add(pid, "specialist", "Does the retention proposition raise privacy-specific minimisation or proportionality questions?", "DPIP-or-privacy-specialist")
        elif ptype == "disclosure":
            add(pid, "runtime-observation", "Do observed data flows and recipients match the declared disclosure proposition?", "runtime-data-flow-evidence")
            add(pid, "specialist", "Does the disclosure proposition require privacy-specific purpose or recipient analysis?", "DPIP-or-privacy-specialist")
        elif ptype == "delegation":
            add(pid, "runtime-observation", "Is downstream authority constrained to the scope represented by the policy?", "authority-runtime-evidence")

        if "legal_dependency" in proposition["ambiguity_signals"]:
            add(pid, "specialist", "What jurisdiction-dependent meaning, if any, changes the interpretation of this clause?", "qualified-legal-or-domain-specialist")
        if proposition["judgment_required"]:
            add(pid, "human-judgment", "Resolve the ambiguity signal before relying on this proposition for stronger assurance conclusions.", "policy-reviewer")

    for hypothesis in mapping["hypotheses"]:
        add(
            hypothesis["proposition_id"],
            "assurance-evidence",
            f"What evidence would confirm or falsify the {hypothesis['risk_pattern']} hypothesis?",
            "RAHP-assessment",
        )

    for gap in mapping["evidence_gaps"]:
        if gap["id"] == "policy-redress-evidence-gap":
            termination = next((p for p in subject["propositions"] if p["type"] == "termination"), None)
            if termination:
                add(
                    termination["id"],
                    "governance-or-ux-evidence",
                    "Is a correction, appeal or redress path defined elsewhere and usable in practice?",
                    "policy-review-plus-ux-evidence",
                )
    return queue


def synthesize_assessment(
    subject: dict[str, Any],
    *,
    review: dict[str, Any] | None = None,
    runtime_records: list[dict[str, Any]] | None = None,
    previous_subject: dict[str, Any] | None = None,
) -> dict[str, Any]:
    mapping = map_risk_hypotheses(subject)
    review = review or review_subject(subject)
    runtime = compare_runtime(subject, runtime_records or []) if runtime_records is not None else None
    delta = diff_subjects(previous_subject, subject) if previous_subject is not None else None
    queue = evidence_work_queue(subject, mapping)

    unresolved = [record for record in review["records"] if record["review_state"] == "judgment-required"]
    return {
        "schema": ASSESSMENT_SCHEMA,
        "experimental": True,
        "terminal_assurance": False,
        "source": subject["source"],
        "policy_text_establishes": subject["propositions"],
        "review": review,
        "rahp_infers": mapping,
        "evidence_shows": runtime,
        "change_impact": delta,
        "evidence_work_queue": queue,
        "current_disposition": {
            "state": "JUDGMENT_REQUIRED" if unresolved else "EVIDENCE_REQUIRED",
            "unresolved_review_count": len(unresolved),
            "evidence_item_count": len(queue),
            "reason": "Research output is non-terminal; stronger conclusions require reviewed propositions and the evidence classes identified in the work queue.",
        },
        "authority_boundary": subject["authority_boundary"],
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

    lines.extend(["## What RAHP infers", ""])
    hypotheses = assessment["rahp_infers"]["hypotheses"]
    if not hypotheses:
        lines.append("No bounded portable risk-pattern hypothesis was generated by the deterministic research rules.\n")
    for item in hypotheses:
        lines.extend(
            [
                f"- **{item['risk_pattern']} — {item['risk_name']}** from `{item['proposition_id']}`: {item['rationale']}",
                "  This remains a hypothesis and requires evidence.",
            ]
        )

    lines.extend(["", "## What remains uncertain / what to investigate next", ""])
    for item in assessment["evidence_work_queue"]:
        lines.append(f"- `{item['evidence_class']}` via **{item['route']}** for `{item['proposition_id']}`: {item['question']}")

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
    parser = argparse.ArgumentParser(description="Run the experimental RAHP policy assurance workflow")
    parser.add_argument("source", help="plain-text or Markdown policy file")
    parser.add_argument("--uri", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--retrieved-at")
    parser.add_argument("--review", help="JSON array of review decisions")
    parser.add_argument("--runtime", help="JSON array of runtime-observation records")
    parser.add_argument("--previous-subject", help="previous source-pinned policy subject JSON")
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    args = parser.parse_args()

    subject = ingest_policy(
        Path(args.source).read_text(encoding="utf-8"),
        source_uri=args.uri,
        source_version=args.version,
        retrieved_at=args.retrieved_at,
    )
    review = review_subject(subject, _read_json(args.review)) if args.review else None
    assessment = synthesize_assessment(
        subject,
        review=review,
        runtime_records=_read_json(args.runtime),
        previous_subject=_read_json(args.previous_subject),
    )
    if args.format == "json":
        print(json.dumps(assessment, indent=2, sort_keys=True))
    else:
        print(render_markdown(assessment), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
