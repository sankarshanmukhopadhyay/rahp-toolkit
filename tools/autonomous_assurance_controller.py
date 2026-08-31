#!/usr/bin/env python3
"""Autonomous RAHP assurance controller for clean-room and monitored runs.

The controller never promotes evidence-production success into assurance PASS. It
consumes a multi-granularity subject descriptor, attributable evidence ledger and one
portable assessor result when a substantive judgment is required. If no applicable
assessor can produce a valid result, the machine terminates fail-closed as
INDETERMINATE/model-gap with actionable remediation rather than requesting a human to
advance the workflow.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml

from assurance_fsm import new_run, transition, terminal_from_specialist
from assurance_record import canonical_record, markdown

ASSESSOR_SCHEMA = "rahp-assessor-result/v1"
PORTABLE_OUTCOMES = {"PASS", "FAIL", "INDETERMINATE", "NOT_APPLICABLE"}


def load(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    value = json.loads(text) if path.suffix.lower() == ".json" else yaml.safe_load(text)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: document root must be a mapping")
    return value


def validate_assessor(result: dict[str, Any]) -> list[str]:
    errors=[]
    if result.get("schema") != ASSESSOR_SCHEMA: errors.append(f"schema must be {ASSESSOR_SCHEMA}")
    if not str(result.get("assessor") or "").strip(): errors.append("assessor is required")
    if not str(result.get("assessment_id") or "").strip(): errors.append("assessment_id is required")
    if result.get("outcome") not in PORTABLE_OUTCOMES: errors.append("outcome must be portable")
    for key in ("reason_code","residual_risk","action_required"):
        if not str(result.get(key) or "").strip(): errors.append(f"{key} is required")
    if not isinstance(result.get("evidence_used"),list): errors.append("evidence_used must be a list")
    return errors


def evidence_index(ledger: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(item.get("requirement_id")):item for item in ledger.get("requirements",[]) or [] if isinstance(item,dict) and item.get("requirement_id")}


def evidence_records(ledger: dict[str, Any]) -> list[dict[str, Any]]:
    records=[]
    for item in ledger.get("requirements",[]) or []:
        if not isinstance(item,dict): continue
        attempt=str(item.get("attempt_state") or "")
        cls="runtime-observation" if attempt == "EXECUTED" else "model/evidence-contract-definition"
        records.append({
            "requirement_id":item.get("requirement_id"),
            "class":cls,
            "result":item.get("result"),
            "attempt_state":attempt,
            "surface_classifications":item.get("surface_classifications",[]),
            "provenance":{
                "producer":item.get("producer"),
                "producer_revision":item.get("producer_revision"),
                "attribution":item.get("attribution"),
                "evidence_file":item.get("evidence_file"),
            },
        })
    return records


def missing_required_evidence(contract: dict[str, Any], ledger: dict[str, Any]) -> list[str]:
    indexed=evidence_index(ledger); missing=[]
    for rid in contract.get("required_evidence",[]) or []:
        item=indexed.get(str(rid))
        if not item or item.get("attempt_state") != "EXECUTED" or item.get("result") == "NOT_EVIDENCED": missing.append(str(rid))
    return missing


def default_trace(contract: dict[str, Any], outcome: str, evidence_label: str) -> list[dict[str, Any]]:
    traces=[]
    for trace in contract.get("harm_traceability",[]) or []:
        if isinstance(trace,dict):
            item=dict(trace); item.setdefault("evidence",evidence_label); item.setdefault("conclusion",outcome); traces.append(item)
    return traces


def model_gap_result(assessment_id: str, contract: dict[str, Any], reason: str, missing: list[str] | None=None) -> dict[str, Any]:
    subject=contract.get("subject") or {}
    missing=missing or []
    gap=(f"No autonomous assessor contract can decide the material proposition for {subject.get('id','subject')}." if not missing else f"Required evidence is unavailable for: {', '.join(missing)}.")
    action=("Bind a target-agnostic assessor adapter that emits rahp-assessor-result/v1 for this proposition and rerun from the same immutable subject contract." if not missing else "Produce the named attributable evidence in an accepted class and execute a new pinned comparable run.")
    return {"schema":ASSESSOR_SCHEMA,"assessor":"rahp-controller","assessment_id":assessment_id,"outcome":"INDETERMINATE","reason_code":reason,"evidence_used":[],"residual_risk":gap,"action_required":action}


def build_terminal(spec: dict[str, Any], ledger: dict[str, Any], assessor: dict[str, Any] | None) -> dict[str, Any]:
    contract=spec.get("assurance_contract") or {}
    subject=spec.get("subject") or contract.get("subject")
    if not isinstance(subject,dict) or not subject.get("type") or not subject.get("id"):
        raise ValueError("clean-room spec requires subject.type and subject.id")
    pins=[{"repository":spec["target"]["repository"],"revision":spec["target"]["revision"],**({"artifact":spec["target"].get("document")} if spec["target"].get("document") else {})}]
    for resource in (spec.get("resources") or {}).values():
        if isinstance(resource,dict) and resource.get("repository") and resource.get("revision"):
            pins.append({"repository":resource["repository"],"revision":resource["revision"]})
    run=new_run(subject,pins,correlation_key=str((spec.get("run") or {}).get("lineage_prefix") or "") or None)
    transition(run,"OBSERVED","fresh immutable source observation","clean-room:observed")
    transition(run,"GATHERED","subject and configured resources gathered","clean-room:gathered")
    material=bool(contract.get("material",True))
    transition(run,"MATERIALITY_COMPLETE","configured assurance propositions evaluated for materiality","clean-room:materiality")
    if not material:
        transition(run,"TERMINAL_NOT_APPLICABLE","configured proposition is not material",reason_code="not-material")
        return enrich(run,spec,contract,ledger,None)
    transition(run,"ASSESSMENT_COMPLETE","bounded RAHP assessment contract established","clean-room:assessment")

    missing=missing_required_evidence(contract,ledger)
    specialist=bool(contract.get("specialist_required"))
    if specialist:
        transition(run,"SPECIALIST_REQUIRED","material proposition requires configured specialist","clean-room:specialist-required")
        transition(run,"SPECIALIST_IN_PROGRESS","configured specialist assessment started","clean-room:specialist-start")

    if missing:
        result=model_gap_result(run["assessment_id"],contract,"evidence-required",missing)
    elif assessor is None:
        result=model_gap_result(run["assessment_id"],contract,"model-gap")
    else:
        problems=validate_assessor(assessor)
        if problems:
            result=model_gap_result(run["assessment_id"],contract,"contract-incompatible")
            result["residual_risk"]="; ".join(problems)
            result["action_required"]="Repair the assessor producer/consumer contract and rerun automatically from the same immutable subject pins."
        else:
            result=assessor

    if specialist:
        transition(run,"SPECIALIST_RETURN_READY","portable specialist result constructed","clean-room:return-ready")
        transition(run,"SPECIALIST_RETURNED","specialist result available to local controller","clean-room:returned")
        transition(run,"RECONCILED","RAHP reconciled specialist result","clean-room:reconciled")
    outcome=str(result["outcome"]); reason=str(result.get("reason_code") or "")
    terminal=terminal_from_specialist(outcome,"model-gap" if reason in {"model-gap","contract-incompatible"} else reason)
    transition(run,terminal,f"autonomous assurance conclusion: {outcome}",reason_code=reason or None)
    return enrich(run,spec,contract,ledger,result)


def enrich(run: dict[str, Any], spec: dict[str, Any], contract: dict[str, Any], ledger: dict[str, Any], assessor: dict[str, Any] | None) -> dict[str, Any]:
    run["scope"]=contract.get("scope") or f"Configured assurance scope for {run['subject']['id']}"
    run["non_scope"]=contract.get("non_scope") or "Anything outside the immutable configured subject and source pins."
    for key in ("personas","scenarios","risks","harms","assurance_propositions","requirements_examined","cross_spec_assumptions","tests"):
        run[key]=contract.get(key,[]) or []
    run["evidence"]=evidence_records(ledger)
    if assessor:
        run["inference"]=contract.get("inference") or assessor.get("residual_risk") or assessor.get("reason_code")
    else:
        run["inference"]=contract.get("inference") or "No portable autonomous assessor result was available; the controller failed closed rather than inventing substantive judgment."
    run["confidence"]=contract.get("confidence") or ("bounded by named evidence and assessor result" if assessor else "indeterminate")
    run["boundedness"]=contract.get("boundedness") or "Conclusion applies only to the configured subject, immutable pins and evidence classes represented in this run."
    if run.get("outcome") not in {"PASS","NOT_APPLICABLE"}:
        residual=(assessor or {}).get("residual_risk") or "Assurance proposition remains unresolved."
        action=(assessor or {}).get("action_required") or "Supply the missing model/evidence contract and rerun."
        run["residuals"]=[{"id":f"{run['assessment_id']}:residual","summary":residual}]
        actions=contract.get("actions",[]) or []
        if not actions:
            surface="assurance-model" if run.get("reason_code") in {"model-gap","contract-incompatible"} else "evidence-test"
            actions=[{"surface":surface,"action":action,"acceptance_criterion":"A new immutable comparable run produces a valid portable assessor result and terminal RAHP reconciliation without operator intervention."}]
        run["actions"]=actions
        run["harm_traceability"]=default_trace(contract,str(run.get("outcome")),", ".join(str(x.get("requirement_id")) for x in run["evidence"]))
        if not run["harm_traceability"]:
            run["harm_traceability"]=[{"persona":"affected party","scenario":"configured assurance scenario","harm":"material harm proposition remains unresolved","proposition":str((contract.get("assurance_propositions") or ["configured assurance proposition"])[0]),"control":"configured control/guardrail or missing assurance-model contract","evidence":"attributable evidence ledger","conclusion":str(run.get("outcome"))}]
    else:
        run["residuals"]=contract.get("residuals",[]) or []
        run["actions"]=contract.get("actions",[]) or []
        run["harm_traceability"]=default_trace(contract,str(run.get("outcome")),"attributable evidence ledger")
    run["lineage"]={"clean_room":True,"historical_inputs_used":False,"run":spec.get("run")}
    return run


def self_test() -> int:
    spec={"run":{"lineage_prefix":"q"},"target":{"repository":"example/spec","revision":"a"*40},"resources":{},"subject":{"type":"cross-specification","id":"spec-a×spec-b","components":["a","b"]},"assurance_contract":{"material":True,"specialist_required":True,"required_evidence":["ER-1"],"personas":["holder"],"scenarios":["cross-context presentation"],"harms":["correlation"],"assurance_propositions":["no unnecessary correlation"],"harm_traceability":[{"persona":"holder","scenario":"cross-context presentation","harm":"correlation","proposition":"no unnecessary correlation","control":"context-bound identifiers"}]}}
    ledger={"requirements":[{"requirement_id":"ER-1","attempt_state":"EXECUTED","result":"SATISFIED","producer":"p","producer_revision":"b"*40,"attribution":"runtime","evidence_file":"capture.yaml"}]}
    assessor={"schema":ASSESSOR_SCHEMA,"assessor":"privacy","assessment_id":"dpip:1","outcome":"INDETERMINATE","reason_code":"evidence-required","evidence_used":["ER-1"],"residual_risk":"Correlation cannot yet be ruled out.","action_required":"Run a stronger A/B experiment."}
    run=build_terminal(spec,ledger,assessor); assert run["terminal"] and run["outcome"]=="INDETERMINATE" and run["state"]=="TERMINAL_INDETERMINATE_EVIDENCE_REQUIRED"
    assert canonical_record(run)
    gap=build_terminal(spec,ledger,None); assert gap["reason_code"]=="model-gap" and gap["state"]=="TERMINAL_INDETERMINATE_MODEL_GAP"
    missing=build_terminal(spec,{"requirements":[]},assessor); assert missing["reason_code"]=="evidence-required"
    print("PASS autonomous_assurance_controller self-test")
    return 0


def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--self-test",action="store_true"); p.add_argument("--spec",type=Path); p.add_argument("--ledger",type=Path); p.add_argument("--assessor-result",type=Path); p.add_argument("--machine-output",type=Path); p.add_argument("--human-output",type=Path); a=p.parse_args()
    if a.self_test: return self_test()
    if not a.spec or not a.ledger: p.error("--spec and --ledger are required")
    spec=load(a.spec); ledger=load(a.ledger); assessor=load(a.assessor_result) if a.assessor_result and a.assessor_result.exists() else None
    run=build_terminal(spec,ledger,assessor); record=canonical_record(run); human=markdown(record)
    if a.machine_output: a.machine_output.write_text(json.dumps(record,indent=2)+"\n",encoding="utf-8")
    else: print(json.dumps(record,indent=2))
    if a.human_output: a.human_output.write_text(human,encoding="utf-8")
    return 0

if __name__=="__main__": raise SystemExit(main())
