#!/usr/bin/env python3
"""Compatibility entry point for the experimental RAHP policy workflow (#662).

The reviewed v2 research workflow is implemented in ``policy_assessment_v2``.
This module preserves the original import/CLI path used by tests and research
notes while keeping the stable RAHP controller untouched.
"""

from typing import Any

from policy_assessment_v2 import (  # noqa: F401
    ASSESSMENT_SCHEMA,
    evidence_work_queue as _v2_evidence_work_queue,
    main,
    reconcile_evidence_obligations,
    render_markdown,
    review_subject,
    synthesize_assessment,
)


def evidence_work_queue(
    subject: dict[str, Any],
    mapping: dict[str, Any],
    reviewed_records: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Preserve the v1 caller contract while delegating reviewed flows to v2.

    Legacy callers pass only ``subject`` and ``mapping`` and expect ambiguous
    source propositions to appear as human-judgment work. The v2 synthesis path
    adds those items from explicit review state instead, so this compatibility
    layer restores the old behavior only when no reviewed record set is supplied.
    """
    queue = _v2_evidence_work_queue(subject, mapping, reviewed_records)
    if reviewed_records is not None:
        return queue
    existing = {(item["proposition_id"], item["evidence_class"]) for item in queue}
    for proposition in subject.get("propositions") or []:
        if not proposition.get("judgment_required"):
            continue
        key = (proposition["id"], "human-judgment")
        if key in existing:
            continue
        queue.append(
            {
                "proposition_id": proposition["id"],
                "source_proposition_ids": [proposition["id"]],
                "analysis_text": proposition["normalized_proposition"],
                "obligation_id": "legacy-human-judgment-" + proposition["id"],
                "evidence_class": "human-judgment",
                "question": "Resolve the ambiguity signal before relying on this proposition for stronger assurance conclusions.",
                "why_required": "The source proposition carries unresolved ambiguity and must not silently enter stronger assurance reasoning.",
                "materiality": "context-dependent",
                "route": "policy-reviewer",
                "state": "judgment-required",
                "terminal_effect": "none-until-judgment-resolved",
            }
        )
    return queue


if __name__ == "__main__":
    raise SystemExit(main())
