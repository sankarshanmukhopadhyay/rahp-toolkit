#!/usr/bin/env python3
"""Validate the RAHP v1.8.0 qualification and release-state contract."""
from __future__ import annotations
import json
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]
def load_yaml(rel): return yaml.safe_load((ROOT/rel).read_text(encoding="utf-8"))

def main():
    q=load_yaml("method/v1.8-release-qualification.yaml")
    status=load_yaml("PROJECT-STATUS.yaml")
    release=load_yaml("method/release.yaml")
    versioning=load_yaml("method/versioning.yaml")
    errors=[]
    if q.get("release")!="v1.8.0": errors.append("qualification manifest must identify v1.8.0")
    if str(status.get("stable_release"))!="1.8.0": errors.append("PROJECT-STATUS stable_release must be 1.8.0")
    if status.get("development_target")!="1.8.0": errors.append("development_target must be 1.8.0")
    if status.get("release_status")!="released" or status.get("qualification_status")!="qualified":
        errors.append("release state must be released/qualified")
    if status.get("qualification_contract")!="method/v1.8-release-qualification.yaml":
        errors.append("qualification contract mismatch")
    compat=q.get("stable_compatibility") or {}
    for k,v in compat.items():
        if (status.get("compatibility") or {}).get(k)!=v: errors.append(f"compatibility mismatch: {k}")
    if versioning.get("stable_release")!="v1.8.0": errors.append("versioning stable_release must be v1.8.0")
    declared=(release.get("release") or {})
    if declared.get("version")!="1.8.0": errors.append("release declaration version mismatch")
    if declared.get("theme")!="Semantically Governed Assurance Pipeline": errors.append("release theme mismatch")
    name=declared.get("name") or {}
    if name.get("common")!="Common Map" or name.get("scientific")!="Cyrestis thyodamas":
        errors.append("release name mismatch")

    package=json.loads((ROOT/"package.json").read_text())
    lock=json.loads((ROOT/"package-lock.json").read_text())
    if package.get("version")!="1.8.0": errors.append("root package version mismatch")
    if lock.get("version")!="1.8.0" or (lock.get("packages") or {}).get("",{}).get("version")!="1.8.0":
        errors.append("lock root version mismatch")
    for rel in ["packages/schema/package.json","packages/core/package.json","packages/graph/package.json","packages/cli/package.json"]:
        d=json.loads((ROOT/rel).read_text())
        if d.get("version")!="1.8.0": errors.append(f"workspace version mismatch: {rel}")
        for dep,dv in (d.get("dependencies") or {}).items():
            if dep.startswith("@rahp/") and dv!="1.8.0": errors.append(f"workspace dependency mismatch: {rel} {dep}")

    materiality=ROOT/"tests/test_dtg_semantic_materiality.py"
    if not materiality.is_file(): errors.append("semantic materiality regression test missing")
    else:
        text=materiality.read_text()
        for term in ("test_151_like_release_fanout","test_183_generated_convergence","test_low_weight_fanout_cannot_mask_one_normative_change","test_unknown_manifest_change_remains_conservative"):
            if term not in text: errors.append(f"materiality regression missing: {term}")

    worker=(ROOT/"tools/dtg_repository_review_worker.py").read_text()
    for term in ("attempt_auto", "judgment-required", "assurance:dpip-not-required", "assurance:dpip-requested"):
        if term not in worker: errors.append(f"repository worker capability missing: {term}")

    qcont=q.get("continuing_programmes") or {}
    if qcont.get("false_independence_register_issue")!=193 or qcont.get("release_claims_complete_coverage") is not False:
        errors.append("continuing false-independence programme boundary is not explicit")

    for rel in ["docs/releases/v1.8.0.md","tools/validate_v18_release.py","tests/test_v18_release_qualification.py"]:
        if not (ROOT/rel).is_file(): errors.append(f"required v1.8 artifact missing: {rel}")

    for label,rel in [("README","README.md"),("CHANGELOG","CHANGELOG.md"),("ROADMAP","ROADMAP.md")]:
        text=(ROOT/rel).read_text()
        if "v1.8.0" not in text or "Common Map" not in text:
            errors.append(f"{label} not synchronized to v1.8.0")

    portable=load_yaml("examples/portable-instance/data/instance.yaml")
    if (portable.get("instance") or {}).get("toolkit_version")!="v1.8.0":
        errors.append("portable instance not synchronized to v1.8.0")

    if errors:
        for e in errors: print("ERROR:",e)
        return 1
    print("PASS v1.8.0 qualified: semantically governed assurance pipeline and stable-v1 compatibility are synchronized; continuing evidence programmes remain explicitly non-terminal.")
    return 0

if __name__=="__main__": raise SystemExit(main())
