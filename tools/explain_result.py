#!/usr/bin/env python3
"""Read-only explanation of an existing, validated normalized RAHP result."""
from __future__ import annotations
import html
import json
import re
from pathlib import Path
from typing import Any
import yaml
from jsonschema import Draft202012Validator, FormatChecker

try:
    from .engine_contract import ROOT, load_result, validate_result
    from .assurance_state import freshness_from_basis
except ImportError:
    from engine_contract import ROOT, load_result, validate_result
    from assurance_state import freshness_from_basis

UNRESOLVED = {"finding", "assurance-gap", "review-required", "not-assessed"}


def read_freshness(path: Path, assessment_id: str, run_id: str) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    doc = json.loads(text) if path.suffix.lower() == ".json" else yaml.safe_load(text)
    schema = json.loads((ROOT / "method/schema/assurance-freshness.schema.json").read_text(encoding="utf-8"))
    errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(doc))
    if errors:
        raise ValueError("freshness schema invalid: " + "; ".join(e.message for e in errors))
    if doc["assessment_id"] != assessment_id or doc["assessment_run_id"] != run_id:
        raise ValueError("freshness assessment/run identity mismatch")
    derived, retest = freshness_from_basis(doc["basis"])
    if doc["status"] != derived or doc.get("retest_required", False) != retest:
        raise ValueError("freshness state contradicts its declared basis")
    return {
        "state": derived, "retest_required": retest, "assessment_run_id": run_id,
        "evaluated_at": doc["evaluated_at"], "basis": doc["basis"],
        "verification": "caller-declared; source and run identity not independently authenticated",
    }


def explain_file(result_path: Path, freshness_path: Path | None = None, run_id: str | None = None) -> dict[str, Any]:
    if (freshness_path is None) != (run_id is None):
        raise ValueError("--freshness and --run-id must be supplied together")
    if run_id is not None and not run_id.strip():
        raise ValueError("--run-id must not be empty")
    if not validate_result(result_path, quiet=True):
        raise ValueError("normalized result schema or semantic validation failed")
    doc = load_result(result_path)
    evaluations = doc.get("evaluations") or []
    residuals = [{
        "proposition_id": (e.get("proposition") or {}).get("id"),
        "subject": (e.get("proposition") or {}).get("subject"),
        "state": (e.get("residual") or {}).get("status"),
        "reason": (e.get("residual") or {}).get("reason"),
        "missing": (e.get("residual") or {}).get("missing") or [],
        "evidence_linkage": "not-inferred; consult original evaluation",
    } for e in evaluations]
    freshness = (read_freshness(freshness_path, doc["assessment"]["id"], run_id)
                 if freshness_path is not None else
                 {"state": "not-established", "reason": "no separately bound freshness record supplied"})
    return {
        "projection": "rahp-result-explanation/v1",
        "authority": "read-only derived view, not an assurance or governance decision",
        "input_validation": "normalized result schema and local semantic constraints only",
        "assessment": {
            "id": doc["assessment"]["id"], "key": doc["assessment"]["key"],
            "mode": doc["mode"], "target": doc["target"],
        },
        "decision": {
            "record_status": doc["status"], "disposition": doc["disposition"],
            "controller_terminal_outcome": "not-established-by-normalized-result",
        },
        "findings": doc["findings"],
        "evaluation": {
            "state": "recorded" if "evaluations" in doc else "not-recorded",
            "declared_summary": doc.get("assurance_summary"),
            "residuals": residuals,
            "unresolved_count": sum(x["state"] in UNRESOLVED for x in residuals),
            "overall_assurance": "not-derived",
        },
        "evidence": [{
            "id": e["id"], "class": e["class"], "description": e["description"],
            "external_reference": e.get("uri"), "digest_declared": bool(e.get("sha256")),
        } for e in doc["evidence"]],
        "freshness": freshness,
        "retest_triggers": doc.get("retest_triggers") or [],
        "limitations": [
            "Valid input and successful execution are not assurance PASS.",
            "Evidence references are not retrieved, authenticated or correlated with propositions.",
            "Missing freshness/evaluations/retest triggers do not establish current assurance.",
            "Controller terminalization, source authority and governance decisions remain external.",
        ],
    }


def _md(value: Any) -> str:
    if value is None:
        return "not recorded"
    value = html.escape(str(value).replace("\r", " ").replace("\n", " "), quote=False)
    return re.sub(r"([\\\x60*_{}\[\]<>|])", r"\\\1", value)


def render_markdown(view: dict[str, Any]) -> str:
    a, d, e, f = view["assessment"], view["decision"], view["evaluation"], view["freshness"]
    lines = [
        "# RAHP normalized-result explanation", "",
        "**Read-only projection, not a new assurance determination.**", "",
        "## Assessment", "",
        f"- ID: {_md(a['id'])}",
        f"- Key: {_md(a['key'])}",
        f"- Mode: {_md(a['mode'])}",
        f"- Target: {_md(a['target']['repository'])}@{_md(a['target']['reviewed_revision'])}",
        f"- Record status: {_md(d['record_status'])}",
        f"- Disposition: {_md(d['disposition']['outcome'])}",
        "- Controller terminal outcome: not established by this record", "",
        "## Residual evaluations", "",
    ]
    if not e["residuals"]:
        lines.append("Not recorded. No conclusion of assurance can be inferred.")
    for item in e["residuals"]:
        missing = ", ".join(item["missing"]) if item["missing"] else "not declared"
        lines.append(f"- {_md(item['proposition_id'])}: **{_md(item['state'])}**; reason: {_md(item['reason'])}; missing: {_md(missing)}")
    lines.extend(["", f"Unresolved residuals: {e['unresolved_count']}. Overall assurance: not derived.", "",
                  "## Declared evidence", ""])
    if not view["evidence"]:
        lines.append("No evidence declared.")
    for item in view["evidence"]:
        lines.append(f"- {_md(item['id'])} ({_md(item['class'])}): {_md(item['description'])}")
    lines.extend(["", "Evidence-to-proposition links are not inferred.", "",
                  "## Freshness and retest", "", f"- Freshness: {_md(f['state'])}"])
    if "reason" in f:
        lines.append(f"- Basis: {_md(f['reason'])}")
    if "assessment_run_id" in f:
        lines.append(f"- Caller-declared run: {_md(f['assessment_run_id'])}")
        lines.append(f"- Verification: {_md(f['verification'])}")
    triggers = view["retest_triggers"]
    lines.append("- Retest triggers: " + (_md("; ".join(triggers)) if triggers else "not recorded"))
    lines.extend(["", "## Limitations", ""])
    lines.extend("- " + _md(limitation) for limitation in view["limitations"])
    return "\n".join(lines) + "\n"
