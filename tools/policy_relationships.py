#!/usr/bin/env python3
"""Relationship and precedence research helpers for RAHP policy subjects (#662).

This module never resolves legal meaning automatically. It produces reviewable
candidates for definition use, incorporated documents, cross-document definition
conflicts, and precedence. Explicit reviewer decisions can change research state,
but never create terminal RAHP assurance or a legal conclusion.
"""

from __future__ import annotations

import re
from typing import Any

from policy_subject import sha256_text

_PRECEDENCE = re.compile(
    r"\b(?:more specific terms apply|terms .* prevail|prevail over|controls? over|"
    r"in the event of (?:a )?conflict|if .* conflict .* terms)\b",
    re.I | re.S,
)


def _normalized_term(term: str) -> str:
    return re.sub(r"\s+", " ", term.strip()).casefold()


def definition_index(subject: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    structure = subject.get("document_structure") or {}
    index: dict[str, list[dict[str, Any]]] = {}
    for definition in structure.get("definitions") or []:
        term = str(definition.get("term") or "").strip()
        if not term:
            continue
        index.setdefault(_normalized_term(term), []).append(definition)
    return index


def definition_bindings(subject: dict[str, Any]) -> list[dict[str, Any]]:
    """Find lexical definition-use candidates without claiming semantic binding."""
    index = definition_index(subject)
    bindings: list[dict[str, Any]] = []
    for proposition in subject.get("propositions") or []:
        text = proposition.get("normalized_proposition") or ""
        source_unit = (proposition.get("structure") or {}).get("unit_id")
        for normalized, definitions in index.items():
            display_term = definitions[0]["term"]
            if not re.search(rf"\b{re.escape(display_term)}\b", text, re.I):
                continue
            defining_units = {item.get("unit_id") for item in definitions}
            if source_unit in defining_units:
                continue
            bindings.append(
                {
                    "id": "defbind-" + sha256_text(f"{proposition['id']}:{normalized}")[:16],
                    "term": display_term,
                    "proposition_id": proposition["id"],
                    "definition_unit_ids": sorted(item for item in defining_units if item),
                    "state": "candidate",
                    "requires_review": True,
                    "derivation": "lexical-definition-use-candidate",
                }
            )
    return bindings


def reference_relationships(subject: dict[str, Any], decisions: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    structure = subject.get("document_structure") or {}
    refs = structure.get("references") or []
    supplied: dict[tuple[str, str], dict[str, Any]] = {}
    for decision in decisions or []:
        key = (str(decision.get("unit_id") or ""), str(decision.get("target") or ""))
        supplied[key] = decision

    relationships: list[dict[str, Any]] = []
    for ref in refs:
        key = (ref.get("unit_id") or "", ref.get("target") or "")
        decision = supplied.get(key)
        state = "unresolved"
        reviewer = None
        rationale = None
        relationship_type = ref.get("reference_kind", "external-reference")
        if decision:
            action = decision.get("action")
            if action not in {"accept", "reject", "reclassify"}:
                raise ValueError(f"unsupported reference relationship action: {action}")
            reviewer = decision.get("reviewer")
            rationale = decision.get("rationale")
            if action in {"reject", "reclassify"} and not rationale:
                raise ValueError(f"{action} requires rationale for reference {key[1]}")
            if action == "accept":
                state = "accepted"
            elif action == "reject":
                state = "rejected"
            else:
                relationship_type = str(decision.get("relationship_type") or "").strip()
                if not relationship_type:
                    raise ValueError("reclassify requires relationship_type")
                state = "amended"
        relationships.append(
            {
                "id": "rel-" + sha256_text(f"{key[0]}:{key[1]}")[:16],
                "unit_id": key[0],
                "label": ref.get("label"),
                "target": key[1],
                "relationship_type": relationship_type,
                "traversed": False,
                "review_state": state,
                "reviewer": reviewer,
                "rationale": rationale,
            }
        )
    return relationships


def precedence_candidates(subject: dict[str, Any]) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for proposition in subject.get("propositions") or []:
        text = proposition.get("normalized_proposition") or ""
        if not _PRECEDENCE.search(text):
            continue
        candidates.append(
            {
                "id": "precedence-" + sha256_text(proposition["id"])[:16],
                "proposition_id": proposition["id"],
                "source_text": proposition["source_span"]["text"],
                "state": "judgment-required",
                "requires_review": True,
                "derivation": "precedence-language-candidate",
                "resolution": None,
            }
        )
    return candidates


def definition_conflicts(subjects: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Surface cross-document same-term/different-definition candidates."""
    occurrences: dict[str, list[dict[str, Any]]] = {}
    for subject in subjects:
        for normalized, definitions in definition_index(subject).items():
            for definition in definitions:
                occurrences.setdefault(normalized, []).append(
                    {
                        "term": definition["term"],
                        "subject_sha256": subject["source"]["sha256"],
                        "subject_uri": subject["source"]["uri"],
                        "text": definition["source_span"]["text"],
                        "unit_id": definition.get("unit_id"),
                    }
                )

    conflicts: list[dict[str, Any]] = []
    for normalized, items in occurrences.items():
        subject_ids = {item["subject_sha256"] for item in items}
        texts = {re.sub(r"\s+", " ", item["text"].strip()).casefold() for item in items}
        if len(subject_ids) < 2 or len(texts) < 2:
            continue
        conflicts.append(
            {
                "id": "defconflict-" + sha256_text(normalized + ":" + ":".join(sorted(subject_ids)))[:16],
                "term": items[0]["term"],
                "occurrences": items,
                "state": "judgment-required",
                "requires_review": True,
                "resolution": None,
            }
        )
    return conflicts


def apply_precedence_decisions(
    candidates: list[dict[str, Any]],
    conflicts: list[dict[str, Any]],
    decisions: list[dict[str, Any]] | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    supplied = {item.get("candidate_id"): item for item in decisions or []}
    known = {item["id"] for item in candidates + conflicts}
    unknown = sorted(set(supplied) - known)
    if unknown:
        raise ValueError("precedence decisions reference unknown candidates: " + ", ".join(unknown))

    def apply(item: dict[str, Any]) -> dict[str, Any]:
        result = dict(item)
        decision = supplied.get(item["id"])
        if not decision:
            return result
        winner = str(decision.get("winner_subject_sha256") or "").strip()
        rationale = str(decision.get("rationale") or "").strip()
        reviewer = decision.get("reviewer")
        if not winner or not rationale:
            raise ValueError(f"precedence resolution requires winner_subject_sha256 and rationale for {item['id']}")
        result["state"] = "reviewed-resolution"
        result["resolution"] = {
            "winner_subject_sha256": winner,
            "reviewer": reviewer,
            "rationale": rationale,
            "legal_conclusion": False,
            "terminal_assurance": False,
        }
        return result

    return [apply(item) for item in candidates], [apply(item) for item in conflicts]


def build_policy_relationship_model(
    primary: dict[str, Any],
    *,
    related_subjects: list[dict[str, Any]] | None = None,
    reference_decisions: list[dict[str, Any]] | None = None,
    precedence_decisions: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    subjects = [primary] + list(related_subjects or [])
    precedence = precedence_candidates(primary)
    conflicts = definition_conflicts(subjects)
    precedence, conflicts = apply_precedence_decisions(precedence, conflicts, precedence_decisions)
    references = reference_relationships(primary, reference_decisions)
    unresolved = sum(1 for item in precedence + conflicts if item["state"] == "judgment-required")
    unresolved += sum(1 for item in references if item["review_state"] == "unresolved" and item["relationship_type"] == "incorporated-document-candidate")
    return {
        "schema": "rahp-policy-relationships/v1",
        "terminal_assurance": False,
        "automatic_document_traversal": False,
        "definitions": definition_index(primary),
        "definition_bindings": definition_bindings(primary),
        "references": references,
        "precedence_candidates": precedence,
        "definition_conflicts": conflicts,
        "unresolved_judgment_count": unresolved,
    }
