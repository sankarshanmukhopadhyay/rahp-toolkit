"""Helpers for the RAHP v1.1 portable assurance catalogue."""
from __future__ import annotations

from functools import lru_cache
import pathlib
import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
FILES = {
    "harm_patterns": "harm-patterns.yaml",
    "risk_patterns": "risk-patterns.yaml",
    "control_patterns": "control-patterns.yaml",
    "guardrail_patterns": "guardrail-patterns.yaml",
    "assurance_patterns": "assurance-patterns.yaml",
    "evidence_patterns": "evidence-patterns.yaml",
}


def load_yaml(path):
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


@lru_cache(maxsize=1)
def indexes():
    """Load portable catalogue indexes once per validator process.

    Validation callers may invoke ``validate_block`` hundreds of times in one
    repository-wide run. The catalogue is immutable for the lifetime of that
    process, so re-reading and reparsing all six catalogue files for every
    finding/scenario adds cost without changing assurance semantics.
    """
    out = {}
    for field, fn in FILES.items():
        doc = load_yaml(ROOT / "method" / "catalogue" / fn)
        out[field] = {str(r.get("id")): r for r in doc.get("records") or [] if r.get("id")}
    return out


def validate_block(block, prefix, errors, required=True):
    idx = indexes()
    if not isinstance(block, dict):
        if required:
            errors.append(f"{prefix}: portable_assurance mapping required")
        return
    for field, valid in idx.items():
        vals = block.get(field) or []
        if not isinstance(vals, list):
            errors.append(f"{prefix}: portable_assurance.{field} must be a list")
            continue
        for ref in vals:
            if ref not in valid:
                errors.append(f"{prefix}: portable_assurance.{field} reference {ref!r} does not resolve")
    if required and not block.get("risk_patterns"):
        errors.append(f"{prefix}: portable_assurance.risk_patterns must be non-empty")
    if required and not block.get("harm_patterns"):
        errors.append(f"{prefix}: portable_assurance.harm_patterns must be non-empty")
