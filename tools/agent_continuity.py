"""Portable agent substitution, handoff, and redress continuity checks."""
from __future__ import annotations
from typing import Any
SCHEMA="rahp-agent-continuity/v1"

def evaluate(case: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(case,dict) or case.get("schema")!=SCHEMA: raise ValueError("unsupported agent continuity schema")
    chain=case.get("chain")
    if not isinstance(chain,list) or not chain: raise ValueError("chain must be a nonempty array")
    findings=[]
    root=None
    previous=None
    for i,hop in enumerate(chain):
        if not isinstance(hop,dict): raise ValueError("chain hop must be an object")
        for f in ("agent","principal","authority_id","scope"):
            if not isinstance(hop.get(f),str) or not hop[f]: raise ValueError(f"hop {i}.{f} must be nonempty")
        if i==0: root=hop["principal"]
        if hop["principal"]!=root:
            findings.append({"control":"principal-continuity","status":"NOT_SATISFIED","reason":f"hop {i} changes root principal"})
        if previous is not None:
            parent=set(previous.get("capabilities",[]));child=set(hop.get("capabilities",[]))
            if not child.issubset(parent):
                findings.append({"control":"capability-attenuation","status":"NOT_SATISFIED","reason":f"hop {i} expands capabilities"})
            if hop.get("parent_authority_id")!=previous["authority_id"]:
                findings.append({"control":"lineage","status":"NOT_SATISFIED","reason":f"hop {i} does not bind previous authority"})
        previous=hop
    if not findings:
        findings.append({"control":"chain","status":"SATISFIED","reason":"principal, lineage, and capability attenuation preserved"})

    substitution=case.get("substitution")
    if substitution is not None:
        if not isinstance(substitution,dict): raise ValueError("substitution must be an object")
        required=("old_agent","new_agent","continuity_evidence")
        missing=[x for x in required if not substitution.get(x)]
        if missing:
            findings.append({"control":"substitution","status":"UNAVAILABLE","reason":"substitution continuity evidence incomplete"})
        elif substitution["old_agent"]==substitution["new_agent"]:
            findings.append({"control":"substitution","status":"NOT_SATISFIED","reason":"substitution does not identify a replacement"})
        else:
            findings.append({"control":"substitution","status":"SATISFIED","reason":"replacement is explicitly linked by continuity evidence"})

    redress=case.get("redress")
    if redress is not None:
        if not isinstance(redress,dict): raise ValueError("redress must be an object")
        for key in ("challenge_id","action_evidence_id","resolution","closed_at"):
            if not redress.get(key):
                findings.append({"control":"redress","status":"UNAVAILABLE","reason":f"redress lacks {key}"})
                break
        else:
            findings.append({"control":"redress","status":"SATISFIED","reason":"challenge is linked to action evidence and closure"})

    statuses={x["status"] for x in findings}
    if "UNAVAILABLE" in statuses: outcome,reason="INDETERMINATE","continuity-evidence-unavailable"
    elif "NOT_SATISFIED" in statuses: outcome,reason="FAIL","agent-continuity-constraint-not-satisfied"
    else: outcome,reason="PASS","agent-continuity-satisfied"
    return {"schema":SCHEMA,"outcome":outcome,"reason_code":reason,"findings":findings,
            "authority_note":"Bounded continuity assessment only; does not authorize a handoff or replacement."}
