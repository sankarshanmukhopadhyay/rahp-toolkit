#!/usr/bin/env python3
"""Render one canonical assurance result into machine- and human-readable forms.

The renderer is deliberately subject-agnostic. It preserves the same facts across
JSON/YAML and Markdown so a development issue, specification comment, test plan or UX
remediation can cite the result without reconstructing controller history.
"""
from __future__ import annotations

import argparse
import json
from copy import deepcopy
from typing import Any

import yaml

REQUIRED_TERMINAL = ("assessment_id", "subject", "source_pins", "state", "terminal", "outcome", "reason_code")
ACTION_SURFACES = {
    "normative-specification",
    "composition-profile",
    "implementation-code",
    "evidence-test",
    "deployment-operator",
    "governance-redress",
    "consumer-experience",
    "assurance-model",
}
EVIDENCE_CLASSES = {
    "static-specification-analysis",
    "repository-fixture",
    "synthetic-test",
    "runtime-observation",
    "governance-evidence",
    "model/evidence-contract-definition",
}


def validate_terminal_record(run: dict[str, Any]) -> list[str]:
    errors=[]
    for key in REQUIRED_TERMINAL:
        if key not in run: errors.append(f"{key} is required")
    if run.get("terminal") is not True: errors.append("terminal assurance record requires terminal=true")
    subject=run.get("subject")
    if not isinstance(subject,dict) or not subject.get("type") or not subject.get("id"): errors.append("subject.type and subject.id are required")
    pins=run.get("source_pins")
    if not isinstance(pins,list) or not pins: errors.append("source_pins must be a non-empty list")
    for index,evidence in enumerate(run.get("evidence",[]) or []):
        if not isinstance(evidence,dict): errors.append(f"evidence[{index}] must be a mapping"); continue
        cls=str(evidence.get("class") or "")
        if cls not in EVIDENCE_CLASSES: errors.append(f"evidence[{index}].class is unknown: {cls!r}")
        if not evidence.get("provenance"): errors.append(f"evidence[{index}].provenance is required")
    for index,action in enumerate(run.get("actions",[]) or []):
        if not isinstance(action,dict): errors.append(f"actions[{index}] must be a mapping"); continue
        if action.get("surface") not in ACTION_SURFACES: errors.append(f"actions[{index}].surface is unknown")
        if not str(action.get("action") or "").strip(): errors.append(f"actions[{index}].action is required")
        if not str(action.get("acceptance_criterion") or "").strip(): errors.append(f"actions[{index}].acceptance_criterion is required")
    trace=run.get("harm_traceability")
    if run.get("outcome") not in {"PASS","NOT_APPLICABLE"}:
        if not isinstance(trace,list) or not trace: errors.append("non-PASS material result requires harm_traceability")
    return errors


def canonical_record(run: dict[str, Any]) -> dict[str, Any]:
    errors=validate_terminal_record(run)
    if errors: raise ValueError("; ".join(errors))
    keys=(
        "schema","assessment_id","correlation_key","subject","source_pins","scope","non_scope",
        "personas","scenarios","risks","harms","assurance_propositions","requirements_examined",
        "cross_spec_assumptions","evidence","tests","inference","confidence","boundedness","state",
        "terminal","outcome","reason_code","residuals","actions","harm_traceability","lineage",
    )
    return {key:deepcopy(run[key]) for key in keys if key in run}


def markdown(record: dict[str, Any]) -> str:
    subject=record["subject"]
    lines=[
        f"# RAHP assurance conclusion — {subject['id']}","",
        f"- Assessment: `{record['assessment_id']}`",
        f"- Subject type: `{subject['type']}`",
        f"- Outcome: **{record['outcome']}**",
        f"- Reason: `{record['reason_code']}`",
        f"- Controller state: `{record['state']}`",
    ]
    if record.get("boundedness"): lines.append(f"- Boundedness: {record['boundedness']}")
    if record.get("confidence"): lines.append(f"- Confidence: {record['confidence']}")
    lines += ["","## Source pins",""]
    for pin in record["source_pins"]:
        suffix=f" — `{pin.get('artifact')}`" if pin.get("artifact") else ""
        lines.append(f"- `{pin['repository']}@{pin['revision']}`{suffix}")
    if record.get("inference"):
        lines += ["","## Assurance inference","",str(record["inference"])]
    trace=record.get("harm_traceability") or []
    if trace:
        lines += ["","## Human-harm traceability",""]
        for item in trace:
            lines.append(f"- **{item.get('persona','affected party')} / {item.get('scenario','scenario')}** → {item.get('harm','harm')} → `{item.get('proposition','proposition')}` → {item.get('control','control/guardrail')} → {item.get('evidence','evidence')} → {item.get('conclusion',record['outcome'])}")
    residuals=record.get("residuals") or []
    if residuals:
        lines += ["","## Residuals",""]
        for item in residuals: lines.append(f"- {item.get('summary') or item.get('id') or item}")
    actions=record.get("actions") or []
    if actions:
        lines += ["","## Actionable remediation",""]
        for item in actions:
            lines += [f"### {item['surface']}","",str(item["action"]),"",f"**Acceptance criterion:** {item['acceptance_criterion']}",""]
    lines += ["","## Machine-readable record","","```yaml",yaml.safe_dump(record,sort_keys=False).rstrip(),"```",""]
    return "\n".join(lines)


def self_test() -> int:
    sample={
        "schema":"rahp-assurance-run-state/v1","assessment_id":"rahp:test","correlation_key":"rahp:test",
        "subject":{"type":"composition","id":"credential×zkp protected access","components":["credential","zkp"]},
        "source_pins":[{"repository":"example/spec","revision":"a"*40},{"repository":"example/impl","revision":"b"*40}],
        "scope":"cross-context credential presentation in a protected-person service flow","non_scope":"issuer compromise",
        "personas":["protected person"],"scenarios":["service access without unnecessary correlation"],
        "risks":["cross-context correlation"],"harms":["unwanted linkage and exposure"],
        "assurance_propositions":["credential object identity must not expand declared correlation scope"],
        "evidence":[{"class":"runtime-observation","provenance":{"run_id":"123","repository":"example/impl","revision":"b"*40}}],
        "tests":["A/B presentation across unrelated relying contexts"],"inference":"A durable identifier was observed as reusable across the contexts under test.",
        "confidence":"high for tested path","boundedness":"does not generalize beyond pinned implementation/path",
        "state":"TERMINAL_FAIL","terminal":True,"outcome":"FAIL","reason_code":"prohibited-correlation-observed",
        "residuals":[{"id":"R1","summary":"Other presentation modes were not exercised."}],
        "actions":[{"surface":"implementation-code","action":"Remove or context-bind the reusable presentation identifier.","acceptance_criterion":"Pinned A/B rerun shows no joinable identifier across unrelated relying contexts."},{"surface":"consumer-experience","action":"Ensure any unavoidable correlation is disclosed and contestable.","acceptance_criterion":"UX test demonstrates clear disclosure and a usable contest/redress path before consequential use."}],
        "harm_traceability":[{"persona":"protected person","scenario":"confidential service access","harm":"cross-context exposure","proposition":"no unnecessary cross-context correlation","control":"context-bound presentation identifiers","evidence":"pinned runtime A/B observation","conclusion":"FAIL"}],
        "lineage":{"previous_assessment":None,"supersedes":[]},
    }
    record=canonical_record(sample); rendered=markdown(record)
    assert "Human-harm traceability" in rendered and "consumer-experience" in rendered and "Machine-readable record" in rendered
    bad=deepcopy(sample); bad["actions"][0].pop("acceptance_criterion")
    assert validate_terminal_record(bad)
    print("PASS assurance_record self-test")
    return 0


def main() -> int:
    parser=argparse.ArgumentParser(); parser.add_argument("--self-test",action="store_true"); parser.add_argument("path",nargs="?")
    args=parser.parse_args()
    if args.self_test: return self_test()
    if not args.path: parser.error("provide a JSON/YAML assurance-run file or --self-test")
    text=open(args.path,encoding="utf-8").read(); run=json.loads(text) if args.path.endswith(".json") else yaml.safe_load(text)
    record=canonical_record(run); print(markdown(record)); return 0

if __name__=="__main__": raise SystemExit(main())
