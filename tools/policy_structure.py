#!/usr/bin/env python3
"""Structure-preserving Markdown ingestion for RAHP policy research (#662).

This module is intentionally experimental and additive. It preserves front matter,
heading hierarchy, list-item boundaries, source offsets, and incorporated-document
references before reusing the bounded proposition classification from
``policy_subject``. It does not alter the stable RAHP controller.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import yaml

from policy_subject import SCHEMA, classify, sha256_text

_HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
_LIST_ITEM = re.compile(r"^(\s*)(?:[*+-]|\d+[.)])\s+(.*)$")
_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
_DEFINITION = re.compile(r"(?:[\"“])([^\"”]{1,80})(?:[\"”])\s+(?:means|refers to|is where|represents)\b", re.I)


def _trim_span(text: str, start: int, end: int) -> tuple[int, int, str]:
    raw = text[start:end]
    leading = len(raw) - len(raw.lstrip())
    trailing = len(raw.rstrip())
    start += leading
    end = start + max(0, trailing - leading)
    return start, end, text[start:end]


def _front_matter(text: str) -> tuple[dict[str, Any], int]:
    if not text.startswith("---\n"):
        return {}, 0
    closing = text.find("\n---\n", 4)
    if closing < 0:
        return {}, 0
    raw = text[4:closing]
    data = yaml.safe_load(raw) or {}
    if not isinstance(data, dict):
        data = {"raw": raw}
    return data, closing + len("\n---\n")


def parse_markdown_structure(text: str) -> dict[str, Any]:
    """Return source-preserving structural units without semantic assurance claims."""
    front_matter, body_start = _front_matter(text)
    lines = text.splitlines(keepends=True)
    offsets: list[int] = []
    cursor = 0
    for line in lines:
        offsets.append(cursor)
        cursor += len(line)

    heading_stack: list[dict[str, Any]] = []
    units: list[dict[str, Any]] = []
    headings: list[dict[str, Any]] = []
    references: list[dict[str, Any]] = []
    definitions: list[dict[str, Any]] = []

    index = 0
    while index < len(lines) and offsets[index] < body_start:
        index += 1

    while index < len(lines):
        line = lines[index]
        stripped = line.rstrip("\r\n")
        start = offsets[index]

        heading_match = _HEADING.match(stripped)
        if heading_match:
            level = len(heading_match.group(1))
            title = heading_match.group(2).strip()
            heading_stack = [h for h in heading_stack if h["level"] < level]
            heading = {"level": level, "title": title, "start": start, "end": start + len(stripped)}
            heading_stack.append(heading)
            headings.append(heading.copy())
            index += 1
            continue

        if not stripped.strip():
            index += 1
            continue

        list_match = _LIST_ITEM.match(stripped)
        if list_match:
            end_index = index + 1
            while end_index < len(lines):
                candidate = lines[end_index].rstrip("\r\n")
                if not candidate.strip() or _HEADING.match(candidate) or _LIST_ITEM.match(candidate):
                    break
                if candidate.startswith((" ", "\t")):
                    end_index += 1
                    continue
                break
            end = offsets[end_index] if end_index < len(lines) else len(text)
            unit_start, unit_end, source_text = _trim_span(text, start, end)
            kind = "list-item"
            index = end_index
        else:
            end_index = index + 1
            while end_index < len(lines):
                candidate = lines[end_index].rstrip("\r\n")
                if not candidate.strip() or _HEADING.match(candidate) or _LIST_ITEM.match(candidate):
                    break
                end_index += 1
            end = offsets[end_index] if end_index < len(lines) else len(text)
            unit_start, unit_end, source_text = _trim_span(text, start, end)
            kind = "paragraph"
            index = end_index

        if not source_text:
            continue
        context = [{"level": h["level"], "title": h["title"]} for h in heading_stack]
        unit_id = "unit-" + sha256_text(f"{unit_start}:{unit_end}:{source_text}")[:16]
        unit = {
            "id": unit_id,
            "kind": kind,
            "source_span": {
                "start": unit_start,
                "end": unit_end,
                "text": source_text,
                "sha256": sha256_text(source_text),
            },
            "heading_context": context,
        }
        units.append(unit)

        for label, target in _LINK.findall(source_text):
            references.append(
                {
                    "unit_id": unit_id,
                    "label": label,
                    "target": target,
                    "traversed": False,
                }
            )
        definition = _DEFINITION.search(source_text)
        if definition:
            definitions.append(
                {
                    "unit_id": unit_id,
                    "term": definition.group(1).strip(),
                    "source_span": unit["source_span"],
                }
            )

    return {
        "front_matter": front_matter,
        "front_matter_excluded_from_propositions": bool(front_matter),
        "headings": headings,
        "units": units,
        "references": references,
        "definitions": definitions,
    }


def ingest_structured_policy(
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

    structure = parse_markdown_structure(text)
    source_hash = sha256_text(text)
    propositions: list[dict[str, Any]] = []
    for unit in structure["units"]:
        source_text = unit["source_span"]["text"]
        proposition_type, ambiguity = classify(source_text)
        proposition_id = "pol-" + sha256_text(
            f"{source_hash}:{unit['source_span']['start']}:{unit['source_span']['end']}"
        )[:16]
        propositions.append(
            {
                "id": proposition_id,
                "type": proposition_type,
                "source_span": unit["source_span"],
                "normalized_proposition": source_text.strip(),
                "derivation": "direct-source-statement",
                "ambiguity_signals": ambiguity,
                "judgment_required": bool(ambiguity),
                "structure": {
                    "unit_kind": unit["kind"],
                    "heading_context": unit["heading_context"],
                },
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
        "document_structure": structure,
        "propositions": propositions,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Experimental structure-preserving policy ingestion")
    parser.add_argument("source")
    parser.add_argument("--uri", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--retrieved-at")
    args = parser.parse_args()
    text = Path(args.source).read_text(encoding="utf-8")
    result = ingest_structured_policy(
        text,
        source_uri=args.uri,
        source_version=args.version,
        retrieved_at=args.retrieved_at,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
