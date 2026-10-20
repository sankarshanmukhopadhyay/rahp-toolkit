#!/usr/bin/env python3
"""Validate the bounded people-impact pilot without promoting hypotheses to findings."""
import argparse
import json
from collections import Counter
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / "method/impact-pathways/pilot.json"
SCHEMA = "rahp-people-impact-pathways/v1"
STATES = {"qualified", "provisional", "rejected", "not-established"}
ROLE_VOCAB = ROOT / "method/impact-pathways/roles.json"
SOURCE = {"CORPUS-TRUST-TASKS": "corpora/trust-tasks.yaml",
          "CORPUS-TT-CREDSPEC-COMPOSED": "corpora/trust-tasks-credspec-composed.yaml"}

def validate(data, root=ROOT):
    errors = []
    schema = json.loads((root / "method/schema/impact-pathways.schema.json").read_text())
    errors.extend("schema: " + e.message for e in Draft202012Validator(schema).iter_errors(data))
    if data.get("contract") != SCHEMA:
        errors.append("unsupported contract")
    if len(data.get("pilot_corpora", [])) != len(SOURCE):
        errors.append("pilot set differs from declared contract")
    harm_data = yaml.safe_load((root / "method/catalogue/harm-patterns.yaml").read_text())
    harms = {record["id"] for record in harm_data["records"]}
    roles = json.loads(ROLE_VOCAB.read_text())["roles"]
    role_ids = {r["id"] for r in roles}
    seen_groups = set()
    counts = Counter()
    for group in data.get("pilot_corpora", []):
        cid = group.get("corpus_id")
        if cid not in SOURCE or cid in seen_groups:
            errors.append(f"unknown or repeated corpus {cid}")
            continue
        seen_groups.add(cid)
        corpus = yaml.safe_load((root / SOURCE[cid]).read_text())["corpus"]
        if corpus["id"] != cid or str(corpus["adapter_version"]) != str(group.get("adapter_version")):
            errors.append(f"{cid}: identifier/adapter drift")
        baseline = group.get("baseline", {})
        if corpus["source_commit"] == "derived-from-pinned-dependencies":
            expected = sorted((x["corpus_id"], x["source_commit"], str(x["adapter_version"])) for x in corpus["depends_on"])
            actual = sorted((x["corpus_id"], x["source_commit"], str(x["adapter_version"])) for x in baseline.get("depends_on", []))
            if expected != actual:
                errors.append(f"{cid}: composed dependency drift")
        elif baseline.get("source_commit") != corpus["source_commit"]:
            errors.append(f"{cid}: source revision drift")
        ids = {s["id"]: s for s in corpus["scenarios"]}
        records = group.get("dispositions", [])
        actual_ids = [row.get("scenario_id") for row in records]
        if len(actual_ids) != len(set(actual_ids)) or set(actual_ids) != set(ids):
            errors.append(f"{cid}: missing, duplicated or unknown scenario dispositions")
        for row in records:
            sid, status = row.get("scenario_id"), row.get("status")
            counts[status] += 1
            if status not in STATES or not row.get("reason"):
                errors.append(f"{cid}/{sid}: missing valid judgment and reason")
            pathway = row.get("pathway")
            if status in {"qualified", "provisional"}:
                if not isinstance(pathway, dict) or any(not pathway.get(k) for k in ("failure_condition", "affected_role", "relationship", "protected_interest", "potential_consequence", "evidence")):
                    errors.append(f"{cid}/{sid}: incomplete causal pathway")
                    continue
                evidence = pathway["evidence"]
                if not isinstance(evidence, dict) or evidence.get("kind") not in {"analyst-interpretation", "direct-source"} or not evidence.get("source_anchor") or not evidence.get("limitation"):
                    errors.append(f"{cid}/{sid}: missing source qualification")
                if sid in ids and evidence.get("source_anchor") != ids[sid].get("source_anchor"):
                    errors.append(f"{cid}/{sid}: incorrect source anchor")
                role = pathway.get("role_id")
                if role not in role_ids:
                    errors.append(f"{cid}/{sid}: unrecognized portable role {role}")
                if any(token in str(pathway.get("affected_role", "")).lower() for token in ("daniel wright", "laila hassan")):
                    errors.append(f"{cid}/{sid}: named deployment persona in portable pathway")
                if set(pathway.get("harm_patterns", [])) - harms:
                    errors.append(f"{cid}/{sid}: invalid harm IDs")
                if status == "qualified":
                    if not pathway.get("harm_patterns"):
                        errors.append(f"{cid}/{sid}: qualified people-impact claim requires reviewed harm mapping")
                    if evidence.get("kind") != "direct-source" or not row.get("adjudication", {}).get("decision_evidence"):
                        errors.append(f"{cid}/{sid}: qualification needs direct source and accountable reviewed evidence")
            elif pathway:
                errors.append(f"{cid}/{sid}: unsupported positive relationship")
            if status != "qualified" and row.get("adjudication"):
                errors.append(f"{cid}/{sid}: adjudication cannot silently upgrade non-qualified judgment")
            if "execution_status" in row or "persona_id" in row:
                errors.append(f"{cid}/{sid}: execution/persona assertion outside contract")
    if seen_groups != set(SOURCE):
        errors.append("required corpus omitted")
    return errors, dict(sorted(counts.items()))

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--check",action="store_true")
    p.add_argument("--report",action="store_true")
    args=p.parse_args()
    data=json.loads(PILOT.read_text())
    errors,counts=validate(data)
    groups=data.get("pilot_corpora", [])
    report={
      "contract":SCHEMA,"pilot_corpora":len(groups),
      "scenarios":sum(counts.values()),"dispositions":counts,
      "affected_roles":dict(sorted(Counter(row["pathway"]["role_id"] for group in groups for row in group.get("dispositions", []) if isinstance(row.get("pathway"), dict) and row["pathway"].get("role_id")).items())),
      "harm_reference_count":sum(len(row.get("pathway", {}).get("harm_patterns", [])) for group in groups for row in group.get("dispositions", [])),
      "qualified_causal_claims":counts.get("qualified",0),
      "source_baselines":{g.get("corpus_id"):g.get("baseline") for g in groups},
      "unresolved_scenarios":[{"corpus_id":g.get("corpus_id"),"scenario_id":row.get("scenario_id"),"status":row.get("status")} for g in groups for row in g.get("dispositions", []) if row.get("status") in {"not-established","rejected"}],
      "validation":"PASS" if not errors else "FAIL","errors":errors
    }
    result=report
    print(json.dumps(result,indent=2))
    raise SystemExit(1 if errors else 0)

if __name__=="__main__":
    main()
