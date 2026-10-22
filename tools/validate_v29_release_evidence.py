#!/usr/bin/env python3
"""Validate v2.9 release evidence without publishing the release."""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path
REQUIRED=("full_regression","typescript_conformance","stable_compatibility","docs_rendering","publication_metadata","release_publication_preflight","security_review","owner_approval")
SHA=re.compile(r"^[0-9a-f]{40}$")
REPO_PREFIX="https://github.com/sankarshanmukhopadhyay/rahp-toolkit/"
def assess(record: dict, *, require_pass: bool=True)->list[str]:
    errors=[]
    if record.get("contract")!="rahp-release-evidence/v1": errors.append("unsupported release evidence contract")
    if record.get("candidate_version")!="v2.9.0": errors.append("candidate version mismatch")
    sha=record.get("candidate_sha")
    if sha is not None and (not isinstance(sha,str) or not SHA.fullmatch(sha)): errors.append("candidate_sha must be null or a full 40-character commit SHA")
    gates=record.get("gates")
    if not isinstance(gates,dict) or set(gates)!=set(REQUIRED): return errors+["release gate inventory must be exact"]
    for gate in REQUIRED:
        item=gates[gate]
        if not isinstance(item,dict): errors.append(f"{gate}: evidence must be a mapping"); continue
        result=item.get("result")
        if result not in {"PENDING","PASS","FAIL","INDETERMINATE"}: errors.append(f"{gate}: invalid result {result!r}")
        if require_pass and result!="PASS": errors.append(f"{gate}: not PASS ({result})")
        item_sha=item.get("candidate_sha")
        if require_pass and item_sha!=sha: errors.append(f"{gate}: evidence SHA differs from candidate SHA")
        if item_sha is not None and (not isinstance(item_sha,str) or not SHA.fullmatch(item_sha)): errors.append(f"{gate}: candidate_sha must be null or full SHA")
        source=item.get("source")
        if result=="PASS" and (not isinstance(source,str) or not source.startswith(REPO_PREFIX)): errors.append(f"{gate}: PASS requires repository evidence URL")
        if gate=="owner_approval" and result=="PASS" and item.get("decision")!="GO": errors.append("owner_approval: explicit GO decision required")
    if require_pass and record.get("publication_authorized") is not True: errors.append("publication is not authorized")
    if not require_pass and record.get("publication_authorized") not in {False,True}: errors.append("publication_authorized must be boolean")
    return errors
def main()->int:
    p=argparse.ArgumentParser(); p.add_argument("evidence",type=Path); p.add_argument("--allow-pending",action="store_true"); a=p.parse_args()
    try: record=json.loads(a.evidence.read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError) as exc: print(f"ERROR: cannot read evidence: {exc}"); return 1
    errors=assess(record,require_pass=not a.allow_pending)
    if errors:
        for error in errors: print("NO-GO:",error)
        return 1
    print("PASS v2.9 release evidence structure"+(" (pending gates permitted)" if a.allow_pending else "")); return 0
if __name__=="__main__": sys.exit(main())
