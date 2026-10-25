#!/usr/bin/env python3
"""Claim-integrity helpers for RAHP scenario corpora (#1144).

These helpers assess only contradictions and lifecycle states observable from
recorded corpus/source metadata. They do not establish substantive evidence
sufficiency, implementation conformance, safety, or governance legitimacy.
"""
from __future__ import annotations

import re

SHA_RE = re.compile(r"^[0-9a-f]{40}$")
REASSESSMENT_SOURCE_STATES = {
    "CORPUS_REVIEW_REQUIRED",
    "DEPENDENCY_REVIEW_REQUIRED",
}
PENDING_PROVENANCE_STATES = {
    "composition-review-pending",
    "authoritative-source-pinned-scenario-review-pending",
}
MIXED_GROUNDING_STATE = "semantic-requalification-complete-mixed-grounding"


def is_pending(provenance_status: str | None) -> bool:
    value = str(provenance_status or "")
    return value in PENDING_PROVENANCE_STATES or value.endswith("review-pending")


def static_claim_errors(corpus: dict, source_cfg: dict | None = None) -> list[str]:
    """Return only machine-observable claim contradictions.

    Grade assignment remains a reviewed classification. Passing these checks is
    necessary metadata consistency, not proof that a grade is substantively deserved.
    """
    errors: list[str] = []
    grade = corpus.get("evidence_grade")
    provenance = corpus.get("provenance_status")
    source_cfg = source_cfg or {}
    update_mode = source_cfg.get("update_mode")

    if grade != "source-pinned":
        return errors

    if is_pending(provenance):
        errors.append("source-pinned grade contradicts pending provenance/composition review")

    if provenance == MIXED_GROUNDING_STATE:
        errors.append("source-pinned grade contradicts completed mixed-grounding requalification")

    if update_mode == "derived":
        dependencies = corpus.get("depends_on") or []
        pins = [
            d.get("source_commit")
            for d in dependencies
            if isinstance(d, dict)
        ]
        if not pins or any(not SHA_RE.match(str(pin or "")) for pin in pins):
            errors.append("source-pinned derived corpus requires immutable dependency source_commit pins")
    else:
        if not SHA_RE.match(str(corpus.get("source_commit") or "")):
            errors.append("source-pinned standalone corpus requires an immutable 40-character source_commit")

    return errors


def derive_claim_state(corpus: dict, source_status: str | None = None) -> dict:
    """Derive a reader/monitor state without pretending to adjudicate assurance.

    source_status is the drift/recomposition result from corpus_status.py when
    available. Remote drift can require reassessment but never mechanically changes
    or downgrades a corpus evidence grade.
    """
    grade = corpus.get("evidence_grade")
    provenance = corpus.get("provenance_status")

    if source_status in REASSESSMENT_SOURCE_STATES:
        return {
            "state": "reassessment-required",
            "message": "Tracked source/dependency material changed; reassess the recorded grounding before relying on its currentness.",
        }

    if is_pending(provenance):
        return {
            "state": "review-pending",
            "message": "Recorded provenance says review is pending; do not infer a stronger evidence claim.",
        }

    if provenance == MIXED_GROUNDING_STATE:
        return {
            "state": "mixed-grounding",
            "message": "Semantic review is complete but grounding is mixed; a corpus-wide source-pinned claim is not established.",
        }

    if not grade:
        return {
            "state": "undeclared",
            "message": "No corpus evidence grade is declared.",
        }

    if source_status == "PINNED_NOT_CHECKED":
        return {
            "state": "declared-currentness-unchecked",
            "message": "An evidence grade is declared, but this offline run did not check source currentness.",
        }

    return {
        "state": "declared",
        "message": "An evidence grade is declared; metadata consistency does not establish runtime assurance or substantive evidence sufficiency.",
    }
