#!/usr/bin/env python3
"""Assurance-safe operational telemetry for RAHP execution.

Telemetry describes how RAHP work executed. It is deliberately separate from
assessment evidence and MUST NOT create or modify assurance outcomes.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

SCHEMA = "rahp-execution-telemetry/v1"
_ALLOWED_CONTEXT = {
    "mode",
    "plan",
    "profile_id",
    "subject_id",
    "source_revision",
    "target_class",
}
_ALLOWED_METRIC_TYPES = (bool, int, float, str, type(None))


def _safe_scalar(value: Any) -> Any:
    if not isinstance(value, _ALLOWED_METRIC_TYPES):
        raise ValueError("telemetry values must be scalar")
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("telemetry floats must be finite")
    return value


def sanitize_context(context: dict[str, Any] | None) -> dict[str, Any]:
    """Return only explicitly approved, low-sensitivity context fields."""
    if not context:
        return {}
    if not isinstance(context, dict):
        raise ValueError("telemetry context must be an object")
    out: dict[str, Any] = {}
    for key in sorted(_ALLOWED_CONTEXT):
        if key in context:
            out[key] = _safe_scalar(context[key])
    return out


def sanitize_metrics(metrics: dict[str, Any] | None) -> dict[str, Any]:
    """Validate metric names and scalar values.

    Metric payloads intentionally reject nested objects/lists so evidence bodies,
    credentials, findings, and arbitrary user content cannot be smuggled into
    operational telemetry.
    """
    if not metrics:
        return {}
    if not isinstance(metrics, dict):
        raise ValueError("telemetry metrics must be an object")
    out: dict[str, Any] = {}
    for key, value in sorted(metrics.items()):
        if not isinstance(key, str) or not key or not key.replace("_", "").isalnum():
            raise ValueError(f"invalid telemetry metric name: {key!r}")
        out[key] = _safe_scalar(value)
    return out


def build_event(
    *,
    operation: str,
    run_id: str,
    duration_seconds: float,
    context: dict[str, Any] | None = None,
    metrics: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not isinstance(operation, str) or not operation.strip():
        raise ValueError("telemetry operation must be non-empty")
    if not isinstance(run_id, str) or not run_id.strip():
        raise ValueError("telemetry run_id must be non-empty")
    duration = float(duration_seconds)
    if not math.isfinite(duration) or duration < 0:
        raise ValueError("telemetry duration_seconds must be finite and non-negative")
    return {
        "schema": SCHEMA,
        "operation": operation.strip(),
        "run_id": run_id.strip(),
        "duration_seconds": round(duration, 6),
        "context": sanitize_context(context),
        "metrics": sanitize_metrics(metrics),
        "authority_boundary": {
            "assurance_evidence": False,
            "may_set_assurance_outcome": False,
            "purpose": "operational-observability",
        },
    }


def lifecycle_metrics(record: dict[str, Any]) -> dict[str, Any]:
    """Summarize controller state without inventing assurance conclusions."""
    if not isinstance(record, dict):
        raise ValueError("lifecycle record must be an object")
    history = record.get("history") or []
    if not isinstance(history, list):
        raise ValueError("lifecycle history must be a list")
    blocker = record.get("blocking_reason")
    blocker_code = None
    if isinstance(blocker, dict):
        raw = blocker.get("code")
        if isinstance(raw, str) and raw:
            blocker_code = raw
    resilience = ((record.get("capabilities") or {}).get("resilience") or {})
    resilience_disposition = (
        resilience.get("disposition") if isinstance(resilience, dict) else None
    )
    terminal = record.get("terminal_outcome") if record.get("state") == "TERMINAL" else None
    return {
        "transition_count": max(0, len(history) - 1),
        "terminal": bool(record.get("state") == "TERMINAL"),
        "terminal_outcome": terminal,
        "blocking_reason_code": blocker_code,
        "resilience_disposition": resilience_disposition,
    }


def selection_metrics(*, available_count: int, selected_count: int) -> dict[str, Any]:
    if available_count < 0 or selected_count < 0:
        raise ValueError("selection counts must be non-negative")
    if selected_count > available_count:
        raise ValueError("selected_count cannot exceed available_count")
    return {
        "available_count": int(available_count),
        "selected_count": int(selected_count),
        "skipped_count": int(available_count - selected_count),
    }


def write_event(path: Path, event: dict[str, Any]) -> None:
    if event.get("schema") != SCHEMA:
        raise ValueError("unsupported telemetry schema")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(event, indent=2, sort_keys=True) + "\n", encoding="utf-8")
