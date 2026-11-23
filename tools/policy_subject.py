#!/usr/bin/env python3
"""Experimental policy-as-assurance-subject adapter for RAHP issue #662.

This module is deliberately outside the stable assessment controller. It converts
plain-text/Markdown policy material into source-pinned proposition records and
provides bounded research helpers for risk hypotheses, policy deltas, and
policy-versus-runtime comparison.

Policy text is governance/source evidence. It is never treated as runtime proof,
legal advice, or a terminal assurance PASS/FAIL determination.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Iterable

SCHEMA = "rahp-policy-subject/v1"
PROPOSITION_TYPES = {
    "obligation",
    "permission",
    "prohibition",
    "discretion",
    "condition",
    "exception",
    "representation",
    "retention",
    "disclosure",
    "remedy",
    "termination",
    "delegation",
}

# Ordered from semantically specific to general. These rules are intentionally
# conservative: a clause may remain "representation" rather than receiving a
# stronger interpretation that the source text does not support.
_CLASSIFICATION_RULES: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("prohibition", re.compile(r"\b(?:must not|shall not|may not|prohibited|forbidden)\b", re.I)),
    ("retention", re.compile(r"\b(?:retain|retention|stored? for|keep (?:your|the) data)\b", re.I)),
    ("disclosure", re.compile(r"\b(?:disclose|share|provide|transfer)\b.*\b(?:third[- ]part(?:y|ies)?|partners?|affiliates?|providers?)\b", re.I)),
    ("remedy", re.compile(r"\b(?:appeal|challenge|complaint|complain|correct|correction|contest|redress|remedy)\b", re.I)),
    ("termination", re.compile(r"\b(?:terminate|termination|suspend|suspension|disable|close your account)\b", re.I)),
    ("delegation", re.compile(r"\b(?:delegate|delegation|agent|subcontract|third[- ]party (?:may|can|will) act)\b", re.I)),
    ("exception", re.compile(r"\b(?:except|exception|unless)\b", re.I)),
    ("condition", re.compile(r"\b(?:if|when|provided that|subject to)\b", re.I)),
    ("discretion", re.compile(r"\b(?:sole discretion|our discretion|reserve the right|at any time)\b", re.I)),
    ("obligation", re.compile(r"\b(?:must|shall|required to|is required to|will)\b", re.I)),
    ("permission", re.compile(r"\b(?:may|can|permitted to|allowed to)\b", re.I)),
)

_AMBIGUITY_SIGNALS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("open_ended_discretion", re.compile(r"\b(?:sole discretion|at our discretion|at any time)\b", re.I)),
    ("undefined_reasonableness", re.compile(r"\b(?:reasonable|reasonably|appropriate)\b", re.I)),
    ("purpose_elasticity", re.compile(r"\b(?:as necessary|as needed|other purposes|including but not limited to)\b", re.I)),
    ("legal_dependency", re.compile(r"\b(?:applicable law|required by law|legal obligation|lawful request)\b", re.I)),
)

_RISK_RULES: tuple[dict[str, Any], ...] = (
    {
        "id": "RKP-GOV-01",
        "name": "Concentrated governance authority",
        "when": re.compile(r"\b(?:sole discretion|our discretion|reserve the right)\b", re.I),
        "rationale": "The source grants unilateral discretionary power; whether that power is constrained requires additional evidence.",
    },
    {
        "id": "RKP-GOV-03",
        "name": "Rule change without safe transition",
        "when": re.compile(r"\b(?:change|modify|update|revise)\b.*\b(?:terms|policy|rules|agreement)\b", re.I),
        "rationale": "The source contemplates rule change; notice, migration and transition protections require separate evaluation.",
    },
    {
        "id": "RKP-GOV-04",
        "name": "Responsibility fragmentation",
        "when": re.compile(r"\b(?:third[- ]part(?:y|ies)?|partners?|affiliates?|subcontracts?|service providers?)\b", re.I),
        "rationale": "The source introduces another responsible actor; accountability and remedy ownership may be fragmented.",
    },
    {
        "id": "RKP-DEL-01",
        "name": "Transitive delegation expansion",
        "when": re.compile(r"\b(?:delegate|subcontract|agent)\b", re.I),
        "rationale": "The source permits delegated action; scope preservation and downstream authority need evidence.",
    },
)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _iter_source_spans(text: str) -> Iterable[tuple[int, int, str]]:
    """Yield non-empty paragraph-like spans while preserving exact offsets."""
    for match in re.finditer(r"(?:^|\n\s*\n)(.*?)(?=\n\s*\n|\Z)", text, flags=re.S):
        raw = match.group(1)
        if not raw.strip():
            continue
        leading = len(raw) - len(raw.lstrip())
        trailing = len(raw.rstrip())
        start = match.start(1) + leading
        end = match.start(1) + trailing
        span = text[start:end]
        # Markdown headings alone are structural labels, not propositions.
        if re.fullmatch(r"#{1,6}\s+[^\n]+", span.strip()):
            continue
        yield start, end, span


def classify(text: str) -> tuple[str, list[str]]:
    for proposition_type, pattern in _CLASSIFICATION_RULES:
        if pattern.search(text):
            signals = [name for name, signal in _AMBIGUITY_SIGNALS if signal.search(text)]
            return proposition_type, signals
    signals = [name for name, signal in _AMBIGUITY_SIGNALS if signal.search(text)]
    return "representation", signals


def ingest_policy(
    text: str,
    *,
    source_uri: str,
    source_version: str,
    retrieved_at: str | None = None,
) -> dict[str, Any]:
    if not isinstance(text, str) or not text.strip():
        raise ValueError("policy source must be non-empty UTF-8 text")
    if not source_uri or not source_version:
        raise ValueError("source_uri and source_version are required")

    source_hash = sha256_text(text)
    propositions: list[dict[str, Any]] = []
    for start, end, source_text in _iter_source_spans(text):
        proposition_type, ambiguity = classify(source_text)
        proposition_id = "pol-" + sha256_text(f"{source_hash}:{start}:{end}")[:16]
        propositions.append(
            {
                "id": proposition_id,
                "type": proposition_type,
                "source_span": {
                    "start": start,
                    "end": end,
                    "text": source_text,
                    "sha256": sha256_text(source_text),
                },
                # The normalized proposition is intentionally verbatim in T1/T2.
                # Later AI/human interpretation can add a distinct inferred record.
                "normalized_proposition": source_text.strip(),
                "derivation": "direct-source-statement",
                "ambiguity_signals": ambiguity,
                "judgment_required": bool(ambiguity),
            }
        )

    return {
        "schema": SCHEMA,
        "experimental": True,
        "authority_boundary": {
            "legal_advice": False,
            "regulatory_conformance": False,
            "policy_is_runtime_evidence": False,
            "ai_output_is_assurance_evidence": False,
        },
        "source": {
            "uri": source_uri,
            "version": source_version,
            "sha256": source_hash,
            "retrieved_at": retrieved_at,
            "length": len(text),
        },
        "propositions": propositions,
    }


def validate_subject(subject: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if subject.get("schema") != SCHEMA:
        errors.append(f"schema must be {SCHEMA}")
    source = subject.get("source") or {}
    for key in ("uri", "version", "sha256", "length"):
        if source.get(key) in (None, ""):
            errors.append(f"source.{key} is required")
    propositions = subject.get("propositions")
    if not isinstance(propositions, list):
        return errors + ["propositions must be a list"]
    for index, proposition in enumerate(propositions):
        prefix = f"propositions[{index}]"
        if proposition.get("type") not in PROPOSITION_TYPES:
            errors.append(f"{prefix}.type is invalid")
        span = proposition.get("source_span") or {}
        text = span.get("text")
        if not isinstance(text, str) or not text:
            errors.append(f"{prefix}.source_span.text is required")
        elif span.get("sha256") != sha256_text(text):
            errors.append(f"{prefix}.source_span.sha256 does not match text")
        if proposition.get("derivation") != "direct-source-statement":
            errors.append(f"{prefix}.derivation must preserve direct-source-statement in the ingestion record")
    return errors


def map_risk_hypotheses(subject: dict[str, Any]) -> dict[str, Any]:
    errors = validate_subject(subject)
    if errors:
        raise ValueError("invalid policy subject: " + "; ".join(errors))

    hypotheses: list[dict[str, Any]] = []
    for proposition in subject["propositions"]:
        source_text = proposition["source_span"]["text"]
        for rule in _RISK_RULES:
            if rule["when"].search(source_text):
                hypotheses.append(
                    {
                        "proposition_id": proposition["id"],
                        "risk_pattern": rule["id"],
                        "risk_name": rule["name"],
                        "derivation": "rahp-inference",
                        "rationale": rule["rationale"],
                        "finding_state": "hypothesis",
                        "evidence_required": True,
                    }
                )

    has_adverse_action = any(p["type"] == "termination" for p in subject["propositions"])
    has_remedy = any(p["type"] == "remedy" for p in subject["propositions"])
    evidence_gaps: list[dict[str, str]] = []
    if has_adverse_action and not has_remedy:
        evidence_gaps.append(
            {
                "id": "policy-redress-evidence-gap",
                "state": "INDETERMINATE",
                "reason": "The document contains termination/suspension language but no directly extracted remedy proposition; absence from this source is not proof that redress is unavailable.",
            }
        )

    return {
        "schema": "rahp-policy-risk-hypotheses/v1",
        "subject_sha256": subject["source"]["sha256"],
        "hypotheses": hypotheses,
        "evidence_gaps": evidence_gaps,
    }


def _normalized_text(proposition: dict[str, Any]) -> str:
    return re.sub(r"\s+", " ", proposition["normalized_proposition"].strip()).casefold()


def diff_subjects(old: dict[str, Any], new: dict[str, Any]) -> dict[str, Any]:
    for name, subject in (("old", old), ("new", new)):
        errors = validate_subject(subject)
        if errors:
            raise ValueError(f"invalid {name} policy subject: " + "; ".join(errors))

    old_items = old["propositions"]
    new_items = new["propositions"]
    old_by_text = {_normalized_text(p): p for p in old_items}
    new_by_text = {_normalized_text(p): p for p in new_items}

    removed = [p for key, p in old_by_text.items() if key not in new_by_text]
    added = [p for key, p in new_by_text.items() if key not in old_by_text]
    changed: list[dict[str, Any]] = []
    used_added: set[str] = set()
    remaining_removed: list[dict[str, Any]] = []

    for before in removed:
        best: tuple[float, dict[str, Any] | None] = (0.0, None)
        before_text = _normalized_text(before)
        for after in added:
            if after["id"] in used_added:
                continue
            ratio = SequenceMatcher(None, before_text, _normalized_text(after)).ratio()
            if ratio > best[0]:
                best = (ratio, after)
        if best[1] is not None and best[0] >= 0.55:
            after = best[1]
            used_added.add(after["id"])
            changed.append(
                {
                    "before_id": before["id"],
                    "after_id": after["id"],
                    "similarity": round(best[0], 3),
                    "before": before["normalized_proposition"],
                    "after": after["normalized_proposition"],
                    "reassessment_required": True,
                }
            )
        else:
            remaining_removed.append(before)

    remaining_added = [p for p in added if p["id"] not in used_added]
    return {
        "schema": "rahp-policy-delta/v1",
        "old_sha256": old["source"]["sha256"],
        "new_sha256": new["source"]["sha256"],
        "added": [p["id"] for p in remaining_added],
        "removed": [p["id"] for p in remaining_removed],
        "changed": changed,
        "reassessment_required": bool(remaining_added or remaining_removed or changed),
    }


def compare_runtime(subject: dict[str, Any], runtime_records: list[dict[str, Any]]) -> dict[str, Any]:
    errors = validate_subject(subject)
    if errors:
        raise ValueError("invalid policy subject: " + "; ".join(errors))
    by_id = {p["id"]: p for p in subject["propositions"]}
    comparisons: list[dict[str, Any]] = []

    for record in runtime_records:
        proposition_id = record.get("proposition_id")
        if proposition_id not in by_id:
            raise ValueError(f"runtime record references unknown proposition: {proposition_id}")
        if record.get("evidence_class") != "runtime-observation":
            raise ValueError("runtime comparison requires evidence_class=runtime-observation")
        observed = record.get("observed")
        if observed not in (True, False, None):
            raise ValueError("runtime record observed must be true, false, or null")
        state = "CONSISTENT" if observed is True else "MISMATCH" if observed is False else "INDETERMINATE"
        comparisons.append(
            {
                "proposition_id": proposition_id,
                "policy_evidence_class": "governance-source",
                "runtime_evidence_class": "runtime-observation",
                "state": state,
                "terminal_assurance": False,
                "evidence_ref": record.get("evidence_ref"),
            }
        )

    return {
        "schema": "rahp-policy-runtime-comparison/v1",
        "subject_sha256": subject["source"]["sha256"],
        "comparisons": comparisons,
    }


def _read_json(path: str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Experimental RAHP policy-as-subject research adapter")
    sub = parser.add_subparsers(dest="command", required=True)

    ingest = sub.add_parser("ingest", help="ingest Markdown/plain text into a source-pinned policy subject")
    ingest.add_argument("source")
    ingest.add_argument("--uri", required=True)
    ingest.add_argument("--version", required=True)
    ingest.add_argument("--retrieved-at")

    map_cmd = sub.add_parser("map", help="derive bounded RAHP risk hypotheses from a policy subject")
    map_cmd.add_argument("subject")

    diff_cmd = sub.add_parser("diff", help="compare two source-pinned policy subjects")
    diff_cmd.add_argument("old")
    diff_cmd.add_argument("new")

    runtime = sub.add_parser("compare-runtime", help="compare policy declarations with separate runtime observations")
    runtime.add_argument("subject")
    runtime.add_argument("evidence")

    args = parser.parse_args()
    if args.command == "ingest":
        output = ingest_policy(
            Path(args.source).read_text(encoding="utf-8"),
            source_uri=args.uri,
            source_version=args.version,
            retrieved_at=args.retrieved_at,
        )
    elif args.command == "map":
        output = map_risk_hypotheses(_read_json(args.subject))
    elif args.command == "diff":
        output = diff_subjects(_read_json(args.old), _read_json(args.new))
    else:
        output = compare_runtime(_read_json(args.subject), _read_json(args.evidence))

    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
