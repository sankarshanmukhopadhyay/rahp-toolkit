#!/usr/bin/env python3
"""Compute a DTG portfolio assurance terminal state from durable lineage evidence.

This module is deliberately DTG-instance-specific. It does not infer assurance from CI
success and it does not call GitHub. Orchestration supplies a normalized evidence
record; this controller validates coverage/provenance and computes a conservative
terminal state that can be rendered or published elsewhere.
"""
from __future__ import annotations

import argparse
import json
import pathlib
from typing import Any

import yaml


GREEN = "GREEN"
AMBER = "AMBER"
RED = "RED"


def _count(items: list[dict[str, Any]], key: str, value: Any = True) -> int:
    return sum(1 for item in items if item.get(key) == value)


def _unique(values: list[str]) -> list[str]:
    return sorted(set(values))


def compute(evidence: dict[str, Any]) -> dict[str, Any]:
    """Return a deterministic portfolio-assurance result.

    Expected evidence shape is intentionally small and transport-neutral:

    snapshot: {id, fingerprint, qualifying_findings:[ids...]}
    findings: [{id, accounted_for, disposition, assessment_ids:[...]}]
    assessments: [{id, required, complete, adverse, provenance_valid}]
    dpip: [{id, required, complete, disposition, return_received, provenance_valid}]

    ``disposition`` for DPIP may be PASS, NOT_APPLICABLE, INDETERMINATE or ADVERSE.
    Unknown/missing terminal dispositions are treated conservatively as open work.
    """
    snapshot = evidence.get("snapshot") or {}
    qualifying = list(snapshot.get("qualifying_findings") or [])
    finding_rows = list(evidence.get("findings") or [])
    assessments = list(evidence.get("assessments") or [])
    dpip = list(evidence.get("dpip") or [])

    finding_by_id = {row.get("id"): row for row in finding_rows if row.get("id")}
    missing_findings = [fid for fid in qualifying if fid not in finding_by_id]
    unaccounted = [
        fid for fid in qualifying
        if fid in finding_by_id and not finding_by_id[fid].get("accounted_for", False)
    ]

    required_assessments = [a for a in assessments if a.get("required", True)]
    open_assessments = [a.get("id", "unknown") for a in required_assessments if not a.get("complete", False)]
    invalid_assessment_provenance = [
        a.get("id", "unknown") for a in required_assessments if not a.get("provenance_valid", True)
    ]
    adverse_assessments = [a.get("id", "unknown") for a in required_assessments if a.get("adverse", False)]

    required_dpip = [d for d in dpip if d.get("required", True)]
    open_dpip: list[str] = []
    indeterminate_dpip: list[str] = []
    adverse_dpip: list[str] = []
    invalid_dpip_provenance: list[str] = []
    orphaned_handoffs: list[str] = []

    for item in required_dpip:
        ident = item.get("id", "unknown")
        if not item.get("provenance_valid", True):
            invalid_dpip_provenance.append(ident)
        if not item.get("complete", False):
            open_dpip.append(ident)
            continue
        if not item.get("return_received", False):
            orphaned_handoffs.append(ident)
        disposition = str(item.get("disposition") or "").upper()
        if disposition == "INDETERMINATE":
            indeterminate_dpip.append(ident)
        elif disposition in {"ADVERSE", "FAIL", "FAILED"}:
            adverse_dpip.append(ident)
        elif disposition not in {"PASS", "NOT_APPLICABLE", "NOT_REQUIRED"}:
            open_dpip.append(ident)

    provenance_failures = _unique(invalid_assessment_provenance + invalid_dpip_provenance)
    coverage_failures = _unique(missing_findings + unaccounted)
    open_work = _unique(open_assessments + open_dpip)
    adverse = _unique(adverse_assessments + adverse_dpip)

    if provenance_failures or orphaned_handoffs:
        pipeline_status, disposition = RED, "PIPELINE_BROKEN"
    elif adverse:
        pipeline_status, disposition = RED, "ADVERSE_FINDING"
    elif indeterminate_dpip:
        pipeline_status, disposition = AMBER, "INDETERMINATE"
    elif coverage_failures or open_work:
        pipeline_status, disposition = AMBER, "WORK_OPEN"
    else:
        if required_dpip:
            pipeline_status, disposition = GREEN, "DPIP_COMPLETE"
        else:
            pipeline_status, disposition = GREEN, "DPIP_NOT_REQUIRED"

    result = {
        "portfolio_assurance": {
            "snapshot": snapshot.get("id"),
            "fingerprint": snapshot.get("fingerprint"),
            "monitor_findings": len(qualifying),
            "findings_accounted_for": len(qualifying) - len(coverage_failures),
            "assessments": {
                "required": len(required_assessments),
                "complete": len(required_assessments) - len(open_assessments),
            },
            "dpip": {
                "required": bool(required_dpip),
                "requests": len(required_dpip),
                "completed": len(required_dpip) - len(open_dpip),
                "indeterminate": len(indeterminate_dpip),
            },
            "orphaned_handoffs": len(orphaned_handoffs),
            "unresolved_required_work": len(open_work) + len(coverage_failures),
            "adverse_findings": len(adverse),
            "provenance_failures": len(provenance_failures),
            "disposition": disposition,
            "pipeline_status": pipeline_status,
            "blockers": {
                "coverage": coverage_failures,
                "open_work": open_work,
                "indeterminate": _unique(indeterminate_dpip),
                "adverse": adverse,
                "orphaned_handoffs": _unique(orphaned_handoffs),
                "provenance": provenance_failures,
            },
        }
    }
    return result


def render_markdown(result: dict[str, Any]) -> str:
    p = result["portfolio_assurance"]
    d = p["dpip"]
    a = p["assessments"]
    lines = [
        f"# DTG Portfolio Assurance — {p.get('snapshot') or 'unknown snapshot'}",
        "",
        f"**{p['pipeline_status']} — {p['disposition']}**",
        "",
        f"{p['findings_accounted_for']}/{p['monitor_findings']} material findings accounted for · "
        f"{a['complete']}/{a['required']} required assessments complete · "
        f"DPIP {'required' if d['required'] else 'not required'}"
        + (f" ({d['completed']}/{d['requests']} returned)" if d['required'] else "")
        + f" · {p['orphaned_handoffs']} orphaned handoffs · {p['adverse_findings']} adverse findings",
    ]
    blockers = p.get("blockers") or {}
    nonempty = [(name, vals) for name, vals in blockers.items() if vals]
    if nonempty:
        lines.extend(["", "## Blocking evidence"])
        for name, vals in nonempty:
            lines.append(f"- **{name.replace('_', ' ')}:** " + ", ".join(f"`{v}`" for v in vals))
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("evidence", type=pathlib.Path)
    parser.add_argument("--format", choices=["yaml", "json", "markdown"], default="yaml")
    parser.add_argument("--output", type=pathlib.Path)
    args = parser.parse_args()

    evidence = yaml.safe_load(args.evidence.read_text(encoding="utf-8")) or {}
    result = compute(evidence)
    if args.format == "json":
        text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    elif args.format == "markdown":
        text = render_markdown(result)
    else:
        text = yaml.safe_dump(result, sort_keys=False)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
