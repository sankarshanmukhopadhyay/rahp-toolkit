#!/usr/bin/env python3
"""Generic RAHP normalized-finding adapter.

Portfolio-specific extraction rules are data. This module applies those rules and
emits a portfolio-neutral finding contract consumed by routing and lifecycle code.
"""
from __future__ import annotations

import re
from typing import Any


SEMANTIC_LIST_FIELDS = ("dimensions", "concerns", "affected_surfaces", "change_kind")


def _strings(value: Any) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError("semantic fields must be lists")
    return list(dict.fromkeys(str(item).strip() for item in value if str(item).strip()))


def _matches(rule: dict[str, Any], raw: dict[str, Any]) -> bool:
    repo = str(raw.get("repository") or "")
    title = str(raw.get("title") or "")
    if rule.get("repository_regex") and not re.search(str(rule["repository_regex"]), repo, re.I):
        return False
    if rule.get("title_regex") and not re.search(str(rule["title_regex"]), title, re.I):
        return False
    return True


def normalize_finding(raw: dict[str, Any], adapter: dict[str, Any]) -> dict[str, Any]:
    """Normalize one source finding using instance-owned extraction rules."""
    semantic: dict[str, list[str]] = {field: [] for field in SEMANTIC_LIST_FIELDS}
    matched: list[str] = []
    for rule in adapter.get("mapping_rules") or []:
        if not _matches(rule, raw):
            continue
        matched.append(str(rule.get("id") or f"rule-{len(matched) + 1}"))
        values = rule.get("semantics") or {}
        for field in SEMANTIC_LIST_FIELDS:
            semantic[field].extend(_strings(values.get(field)))
    for field in SEMANTIC_LIST_FIELDS:
        semantic[field] = list(dict.fromkeys(semantic[field]))

    identifier = str(raw.get("finding_id") or raw.get("fingerprint") or "").strip()
    if not identifier:
        raise ValueError("finding_id or fingerprint is required")

    normalized = {
        "schema": "rahp-normalized-finding/v1",
        "id": identifier,
        "source": {
            "repository": str(raw.get("repository") or ""),
            "revision": str(raw.get("revision") or raw.get("commit_sha") or ""),
            "title": str(raw.get("title") or ""),
            "fingerprint": str(raw.get("fingerprint") or ""),
        },
        "state": str(raw.get("state") or ""),
        "review_status": raw.get("review_status"),
        "materiality": str(raw.get("materiality") or ""),
        "assurance_impact": str(raw.get("assurance_impact") or ""),
        **semantic,
        "related_repositories": _strings(raw.get("related_repositories")),
        "normalization": {
            "status": "mapped" if matched else "unmapped",
            "matched_rule_ids": matched,
        },
        "raw": raw,
    }
    validate_normalized_finding(normalized)
    return normalized


def validate_normalized_finding(finding: dict[str, Any]) -> None:
    if finding.get("schema") != "rahp-normalized-finding/v1":
        raise ValueError("unsupported normalized finding schema")
    if not str(finding.get("id") or "").strip():
        raise ValueError("normalized finding id is required")
    source = finding.get("source")
    if not isinstance(source, dict):
        raise ValueError("normalized finding source must be a mapping")
    for field in ("repository", "title"):
        if field not in source:
            raise ValueError(f"normalized finding source.{field} is required")
    for field in ("materiality", "assurance_impact"):
        if not str(finding.get(field) or "").strip():
            raise ValueError(f"normalized finding {field} is required")
    for field in SEMANTIC_LIST_FIELDS:
        _strings(finding.get(field))
    normalization = finding.get("normalization")
    if not isinstance(normalization, dict) or normalization.get("status") not in {"mapped", "unmapped"}:
        raise ValueError("normalization.status must be mapped or unmapped")


def semantic_match(rule: dict[str, Any], finding: dict[str, Any]) -> bool:
    """Return True when a normalized finding satisfies a declarative semantic rule."""
    when = rule.get("when")
    if not isinstance(when, dict):
        return False
    for field, required in when.items():
        if field in SEMANTIC_LIST_FIELDS:
            actual = set(_strings(finding.get(field)))
            wanted = set(_strings(required))
            if not wanted.issubset(actual):
                return False
        else:
            expected = required if isinstance(required, list) else [required]
            if finding.get(field) not in expected:
                return False
    return True


def self_test() -> None:
    adapter = {
        "mapping_rules": [{
            "id": "generic-metadata",
            "title_regex": "metadata",
            "semantics": {
                "dimensions": ["privacy"],
                "concerns": ["metadata", "correlation"],
                "affected_surfaces": ["protocol-envelope"],
                "change_kind": ["behavior-change"],
            },
        }]
    }
    base = {
        "finding_id": "F-1",
        "state": "open",
        "review_status": "unreviewed",
        "materiality": "high",
        "assurance_impact": "potentially-breaking",
        "repository": "example/portable",
        "title": "Expose extra metadata",
    }
    one = normalize_finding(base, adapter)
    two = normalize_finding({**base, "finding_id": "F-2", "title": "Metadata shape changed"}, adapter)
    rule = {"when": {"dimensions": ["privacy"], "concerns": ["metadata"]}}
    assert semantic_match(rule, one)
    assert semantic_match(rule, two)
    assert one["source"]["repository"] == "example/portable"
    unknown = normalize_finding({**base, "finding_id": "F-3", "title": "Unclassified semantic change"}, adapter)
    assert unknown["normalization"]["status"] == "unmapped"
    print("PASS normalized finding model self-test")


if __name__ == "__main__":
    self_test()
