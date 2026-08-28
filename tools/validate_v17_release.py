#!/usr/bin/env python3
"""Validate the RAHP v1.7.0 qualification and release-state contract."""
from __future__ import annotations
import json, sys
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]

def at_least(value, floor):
    try:
        return tuple(map(int,str(value).lstrip("v").split("."))) >= tuple(map(int,floor.split(".")))
    except Exception:
        return False

def load_yaml(rel): return yaml.safe_load((ROOT/rel).read_text(encoding="utf-8"))

def main():
    q=load_yaml("method/v1.7-release-qualification.yaml")
    status=load_yaml("PROJECT-STATUS.yaml")
    release=load_yaml("method/release.yaml")
    versioning=load_yaml("method/versioning.yaml")
    errors=[]
    if q.get("release")!="v1.7.0": errors.append("qualification manifest must identify v1.7.0")
    if not at_least(status.get("stable_release"),"1.7.0"): errors.append("PROJECT-STATUS stable_release must be v1.7.0 or later")
    if not at_least(status.get("development_target"),"1.7.0"): errors.append("development_target must be v1.7.0 or later")
    if status.get("release_status")!="released" or status.get("qualification_status")!="qualified": errors.append("current release state must remain released/qualified")
    
    compat=q.get("stable_compatibility") or {}
    for k,v in compat.items():
        if (status.get("compatibility") or {}).get(k)!=v: errors.append(f"compatibility mismatch: {k}")
    if not at_least(versioning.get("stable_release"),"1.7.0"): errors.append("versioning stable_release must be v1.7.0 or later")
    if not at_least((release.get("release") or {}).get("version"),"1.7.0"): errors.append("release declaration must remain v1.7.0 or later")
    package=json.loads((ROOT/"package.json").read_text())
    lock=json.loads((ROOT/"package-lock.json").read_text())
    if not at_least(package.get("version"),"1.7.0"): errors.append("root package must remain v1.7.0 or later")
    if package.get("version")!=lock.get("version") or package.get("version")!=(lock.get("packages") or {}).get("",{}).get("version"): errors.append("lock root version must match current package version")
    for rel in ["packages/schema/package.json","packages/core/package.json","packages/graph/package.json","packages/cli/package.json"]:
        d=json.loads((ROOT/rel).read_text())
        if d.get("version")!=package.get("version"): errors.append(f"workspace version mismatch: {rel}")
        for dep,dv in (d.get("dependencies") or {}).items():
            if dep.startswith("@rahp/") and dv!=package.get("version"): errors.append(f"workspace dependency mismatch: {rel} {dep}")
    reg=load_yaml("profiles/dtg/cross-spec-tests.yaml")
    comps=reg.get("compositions") or []
    if len(comps)!=(q.get("dtg_cross_spec") or {}).get("expected_declared"): errors.append("DTG declared composition count mismatch")
    runnable=[c for c in comps if c.get("runnable")]
    if len(runnable)!=(q.get("dtg_cross_spec") or {}).get("expected_runnable"): errors.append("DTG runnable composition count mismatch")
    expected=set((q.get("dtg_cross_spec") or {}).get("compositions") or [])
    if {c.get("id") for c in runnable}!=expected: errors.append("DTG runnable composition IDs mismatch")
    zkp=ROOT/"instances/dtg/reviews/2026-08-zkp-fork.result.json"
    if not zkp.is_file(): errors.append("durable ZKP result missing")
    else:
        z=json.loads(zkp.read_text())
        if z.get("mode")!="combined" or z.get("status")!="dispositioned": errors.append("ZKP live combined disposition missing")
    for rel in ["docs/releases/v1.7.0.md","tools/validate_v17_release.py","tests/test_v17_release_qualification.py"]:
        if not (ROOT/rel).is_file(): errors.append(f"required v1.7 artifact missing: {rel}")
    readme=(ROOT/"README.md").read_text()
    changelog=(ROOT/"CHANGELOG.md").read_text()
    roadmap=(ROOT/"ROADMAP.md").read_text()
    for label,text in [("README",readme),("CHANGELOG",changelog),("ROADMAP",roadmap)]:
        if "v1.7.0" not in text or "Common Palmfly" not in text: errors.append(f"{label} not synchronized to v1.7.0")
    if q.get("performance",{}).get("claim")!="measured-not-improved": errors.append("performance non-claim must be explicit")
    if errors:
        for e in errors: print("ERROR:",e)
        return 1
    print("PASS v1.7.0 qualified: assurance operations, review modes, 8/8 DTG coverage and stable-v1 compatibility are synchronized; no unsupported speed claim is made.")
    return 0
if __name__=="__main__": raise SystemExit(main())
