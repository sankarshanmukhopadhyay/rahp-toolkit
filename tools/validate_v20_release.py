#!/usr/bin/env python3
"""Validate RAHP v2.0.0 portable assurance engine stabilization."""
from pathlib import Path
import json, yaml

ROOT=Path(__file__).resolve().parents[1]

def y(rel):
    return yaml.safe_load((ROOT/rel).read_text(encoding="utf-8")) or {}

def main():
    q=y("method/v2.0-release-qualification.yaml")
    status=y("PROJECT-STATUS.yaml")
    rel=y("method/release.yaml")["release"]
    ver=y("method/versioning.yaml")
    errors=[]

    if q.get("release")!="v2.0.0": errors.append("qualification release must be v2.0.0")
    if q.get("qualification")!="portable-assurance-engine-stabilization": errors.append("qualification theme mismatch")
    if str(status.get("stable_release"))!="2.0.0": errors.append("stable_release must be 2.0.0")
    if str(status.get("development_target"))!="2.0.0": errors.append("development_target must be 2.0.0")
    if status.get("release_status")!="released" or status.get("qualification_status")!="qualified": errors.append("release state must be released/qualified")
    if rel.get("version")!="2.0.0" or rel.get("tag")!="v2.0.0": errors.append("release declaration mismatch")
    if rel.get("theme")!="Portable Assurance Engine Stabilization": errors.append("release theme mismatch")
    if (rel.get("name") or {}).get("common")!="Blue Mormon": errors.append("release codename mismatch")
    if (rel.get("name") or {}).get("scientific")!="Papilio polymnestor": errors.append("release scientific name mismatch")
    if ver.get("stable_release")!="v2.0.0": errors.append("versioning stable_release mismatch")

    compat=status.get("compatibility") or {}
    if compat.get("engine_contract")!="rahp-engine-contract-v1": errors.append("engine contract family changed")
    if compat.get("normalized_result_schema")!=1: errors.append("normalized result schema changed")
    if compat.get("evidence_retention_contract")!="rahp-evidence-retention-v1": errors.append("evidence retention contract changed")
    contracts=ver.get("contracts") or {}
    if str(contracts.get("engine_revision"))!="1.3": errors.append("engine revision must be 1.3")

    required=[
      "method/schema/normalized-finding.schema.json",
      "method/schema/assessor-result.schema.json",
      "method/schema/assessment-lifecycle.schema.json",
      "tools/finding_model.py",
      "tools/assessor_contract.py",
      "tools/assessment_controller.py",
      "tools/clean_room.py",
      "instances/dtg/finding-normalization.yaml",
      "tests/test_portable_lifecycle_contract.py",
      "tests/test_dtg_black_box_acceptance.py",
      "tests/acceptance/dtg/2026-08-28.json",
      "tests/acceptance/dtg/2026-08-29.json",
      "tests/acceptance/dtg/2026-08-30.json",
      "docs/releases/v2.0.0.md",
    ]
    for item in required:
        if not (ROOT/item).is_file(): errors.append(f"missing stabilization artifact: {item}")

    generic=(ROOT/"tools/finding_model.py").read_text(encoding="utf-8")
    for token in ("Dogwood","device heartbeat","relationship DID","OpenVTC"):
        if token in generic: errors.append(f"generic finding model leaks instance vocabulary: {token}")

    pkg=json.loads((ROOT/"package.json").read_text())
    if pkg.get("version")!="2.0.0": errors.append("root package version mismatch")
    portable=y("examples/portable-instance/data/instance.yaml")
    if str((portable.get("instance") or {}).get("toolkit_version"))!="v2.0.0": errors.append("portable fixture version mismatch")

    if errors:
        for e in errors: print("ERROR:",e)
        return 1
    print("PASS v2.0.0 qualified: portable assurance engine stabilization with preserved v1 contract compatibility.")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
