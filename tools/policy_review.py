#!/usr/bin/env python3
"""Human-review lineage and reviewed-analysis helpers for RAHP policy research (#662)."""

from __future__ import annotations

from typing import Any

from policy_subject import _RISK_RULES, classify, sha256_text, validate_subject

REVIEW_SCHEMA = "rahp-policy-review/v2"


def _decision_ids(decision: dict[str, Any]) -> list[str]:
    if decision.get("action") == "merge":
        ids = list(decision.get("proposition_ids") or [])
        if not ids and decision.get("proposition_id"):
            ids = [decision["proposition_id"]] + list(decision.get("merge_with") or [])
        return ids
    return [decision.get("proposition_id")] if decision.get("proposition_id") else []


def review_subject(subject: dict[str, Any], decisions: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Review propositions while preserving immutable extraction lineage.

    Supported actions: accept, amend, reject, split and merge. Split/merge are
    explicitly human-review operations and require rationale. No operation mutates
    the source proposition or source span.
    """
    errors = validate_subject(subject)
    if errors:
        raise ValueError("invalid policy subject: " + "; ".join(errors))

    decisions = list(decisions or [])
    known_ids = {item["id"] for item in subject["propositions"]}
    referenced = {pid for decision in decisions for pid in _decision_ids(decision) if pid}
    unknown = sorted(referenced - known_ids)
    if unknown:
        raise ValueError("review decisions reference unknown propositions: " + ", ".join(unknown))

    single: dict[str, dict[str, Any]] = {}
    merge_for: dict[str, dict[str, Any]] = {}
    merge_records: list[dict[str, Any]] = []

    for decision in decisions:
        action = decision.get("action")
        if action == "merge":
            ids = _decision_ids(decision)
            if len(ids) < 2 or len(set(ids)) != len(ids):
                raise ValueError("merge requires at least two distinct proposition_ids")
            if any(pid in merge_for or pid in single for pid in ids):
                raise ValueError("a proposition cannot participate in multiple review decisions")
            text = str(decision.get("text") or "").strip()
            rationale = str(decision.get("rationale") or "").strip()
            if not text:
                raise ValueError("merge requires replacement text")
            if not rationale:
                raise ValueError("merge requires rationale")
            merge_id = "review-merge-" + sha256_text(":".join(ids) + ":" + text)[:16]
            record = {
                "proposition_id": merge_id,
                "source_proposition_ids": ids,
                "machine_proposal": [
                    next(p["normalized_proposition"] for p in subject["propositions"] if p["id"] == pid)
                    for pid in ids
                ],
                "reviewed_proposition": text,
                "review_state": "merged",
                "reviewer": decision.get("reviewer"),
                "rationale": rationale,
            }
            merge_records.append(record)
            for pid in ids:
                merge_for[pid] = record
            continue

        pid = decision.get("proposition_id")
        if not pid:
            raise ValueError(f"{action} requires proposition_id")
        if pid in single or pid in merge_for:
            raise ValueError("a proposition cannot participate in multiple review decisions")
        single[pid] = decision

    reviewed: list[dict[str, Any]] = []
    for proposition in subject["propositions"]:
        pid = proposition["id"]
        if pid in merge_for:
            reviewed.append(
                {
                    "proposition_id": pid,
                    "machine_proposal": proposition["normalized_proposition"],
                    "reviewed_proposition": None,
                    "review_state": "merged-into",
                    "reviewer": merge_for[pid].get("reviewer"),
                    "rationale": merge_for[pid]["rationale"],
                    "merged_into": merge_for[pid]["proposition_id"],
                }
            )
            continue

        decision = single.get(pid)
        if decision is None:
            state = "judgment-required" if proposition["judgment_required"] else "baseline-accepted"
            reviewed.append(
                {
                    "proposition_id": pid,
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
        rationale = str(decision.get("rationale") or "").strip() or None
        if action not in {"accept", "amend", "reject", "split"}:
            raise ValueError(f"unsupported review action for {pid}: {action}")
        if action in {"amend", "reject", "split"} and not rationale:
            raise ValueError(f"{action} requires rationale for {pid}")
        if action == "amend":
            text = str(decision.get("text") or "").strip()
            if not text:
                raise ValueError(f"amend requires replacement text for {pid}")
            reviewed.append(
                {
                    "proposition_id": pid,
                    "machine_proposal": proposition["normalized_proposition"],
                    "reviewed_proposition": text,
                    "review_state": "amended",
                    "reviewer": reviewer,
                    "rationale": rationale,
                }
            )
        elif action == "reject":
            reviewed.append(
                {
                    "proposition_id": pid,
                    "machine_proposal": proposition["normalized_proposition"],
                    "reviewed_proposition": None,
                    "review_state": "rejected",
                    "reviewer": reviewer,
                    "rationale": rationale,
                }
            )
        elif action == "split":
            parts = [str(item).strip() for item in (decision.get("parts") or []) if str(item).strip()]
            if len(parts) < 2:
                raise ValueError(f"split requires at least two non-empty parts for {pid}")
            children = [
                {
                    "proposition_id": f"{pid}:split:{index}",
                    "source_proposition_ids": [pid],
                    "reviewed_proposition": text,
                    "review_state": "split-child",
                    "reviewer": reviewer,
                    "rationale": rationale,
                }
                for index, text in enumerate(parts, 1)
            ]
            reviewed.append(
                {
                    "proposition_id": pid,
                    "machine_proposal": proposition["normalized_proposition"],
                    "reviewed_proposition": None,
                    "review_state": "split",
                    "reviewer": reviewer,
                    "rationale": rationale,
                    "children": children,
                }
            )
        else:
            reviewed.append(
                {
                    "proposition_id": pid,
                    "machine_proposal": proposition["normalized_proposition"],
                    "reviewed_proposition": proposition["normalized_proposition"],
                    "review_state": "accepted",
                    "reviewer": reviewer,
                    "rationale": rationale,
                }
            )

    reviewed.extend(merge_records)
    return {
        "schema": REVIEW_SCHEMA,
        "subject_sha256": subject["source"]["sha256"],
        "records": reviewed,
    }


def analysis_records(subject: dict[str, Any], review: dict[str, Any]) -> list[dict[str, Any]]:
    """Produce the reviewed proposition set consumed by risk/harm analysis."""
    source_by_id = {item["id"]: item for item in subject["propositions"]}
    records: list[dict[str, Any]] = []

    def add(analysis_id: str, text: str, source_ids: list[str], state: str) -> None:
        ptype, ambiguity = classify(text)
        records.append(
            {
                "id": analysis_id,
                "analysis_text": text,
                "type": ptype,
                "ambiguity_signals": ambiguity,
                "source_proposition_ids": source_ids,
                "source_spans": [source_by_id[pid]["source_span"] for pid in source_ids],
                "review_state": state,
                "derivation": "human-reviewed-proposition" if state not in {"baseline-accepted"} else "deterministic-baseline-proposition",
            }
        )

    for record in review["records"]:
        state = record["review_state"]
        pid = record["proposition_id"]
        if state in {"rejected", "merged-into", "judgment-required"}:
            continue
        if state == "split":
            for child in record.get("children") or []:
                add(child["proposition_id"], child["reviewed_proposition"], [pid], "split-child")
            continue
        if state == "merged":
            add(pid, record["reviewed_proposition"], list(record["source_proposition_ids"]), "merged")
            continue
        text = record.get("reviewed_proposition")
        if text:
            add(pid, text, [pid], state)
    return records


def map_reviewed_risk_hypotheses(subject: dict[str, Any], records: list[dict[str, Any]]) -> dict[str, Any]:
    """Map only the reviewed analytical proposition set to bounded RAHP hypotheses."""
    hypotheses: list[dict[str, Any]] = []
    for record in records:
        text = record["analysis_text"]
        for rule in _RISK_RULES:
            if rule["when"].search(text):
                hypotheses.append(
                    {
                        "proposition_id": record["id"],
                        "source_proposition_ids": record["source_proposition_ids"],
                        "risk_pattern": rule["id"],
                        "risk_name": rule["name"],
                        "derivation": "rahp-inference-from-reviewed-proposition",
                        "rationale": rule["rationale"],
                        "finding_state": "hypothesis",
                        "evidence_required": True,
                    }
                )

    has_adverse_action = any(item["type"] == "termination" for item in records)
    has_remedy = any(item["type"] == "remedy" for item in records)
    gaps: list[dict[str, str]] = []
    if has_adverse_action and not has_remedy:
        gaps.append(
            {
                "id": "policy-redress-evidence-gap",
                "state": "INDETERMINATE",
                "reason": "The reviewed proposition set contains termination/suspension language but no reviewed remedy proposition; this does not prove that redress is unavailable.",
            }
        )
    return {
        "schema": "rahp-policy-reviewed-risk-hypotheses/v1",
        "subject_sha256": subject["source"]["sha256"],
        "review_schema": REVIEW_SCHEMA,
        "hypotheses": hypotheses,
        "evidence_gaps": gaps,
    }
