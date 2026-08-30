#!/usr/bin/env python3
"""Validate preserved RAHP v1.8.0 qualification evidence after later v1 releases."""
from __future__ import annotations
import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]

def load_yaml(rel):
    return yaml.safe_load((ROOT / rel).read_text(encoding="utf-8")) or {}

def main():
    q = load_yaml("method/v1.8-release-qualification.yaml")
    status = load_yaml("PROJECT-STATUS.yaml")
    history = json.loads((ROOT / "config/release-codename-history.json").read_text(encoding="utf-8"))
    errors = []

    if q.get("release") != "v1.8.0": errors.append("qualification manifest must identify v1.8.0")
    compat = q.get("stable_compatibility") or {}
    for key, value in compat.items():
        if (status.get("compatibility") or {}).get(key) != value:
            errors.append(f"current stable compatibility no longer preserves v1.8 boundary: {key}")

    binding = next((item for item in history.get("releases", []) if item.get("version") == "v1.8.0"), None)
    if not binding or binding.get("codename") != "Common Map" or binding.get("status") != "published":
        errors.append("published v1.8 Common Map codename history is not preserved")

    qcont = q.get("continuing_programmes") or {}
    if qcont.get("false_independence_register_issue") != 193 or qcont.get("release_claims_complete_coverage") is not False:
        errors.append("historical v1.8 continuing-programme boundary is not explicit")

    for rel in ["docs/releases/v1.8.0.md", "method/v1.8-release-qualification.yaml"]:
        if not (ROOT / rel).is_file(): errors.append(f"required v1.8 artifact missing: {rel}")

    notes = (ROOT / "docs/releases/v1.8.0.md").read_text(encoding="utf-8")
    for term in ("v1.8.0", "Common Map", "Cyrestis thyodamas", "workflow success is not assurance success"):
        if term.casefold() not in notes.casefold(): errors.append(f"v1.8 release notes lost historical term: {term}")

    materiality = ROOT / "tests/test_dtg_semantic_materiality.py"
    if not materiality.is_file(): errors.append("semantic materiality regression test missing")
    else:
        text = materiality.read_text(encoding="utf-8")
        for term in ("test_151_like_release_fanout", "test_183_generated_convergence", "test_low_weight_fanout_cannot_mask_one_normative_change", "test_unknown_manifest_change_remains_conservative"):
            if term not in text: errors.append(f"materiality regression missing: {term}")

    worker = (ROOT / "tools/dtg_repository_review_worker.py").read_text(encoding="utf-8")
    for term in ("attempt_auto", "judgment-required", "assurance:dpip-not-required", "assurance:dpip-requested"):
        if term not in worker: errors.append(f"v1.8 repository-worker capability no longer present: {term}")

    if errors:
        for error in errors: print("ERROR:", error)
        return 1
    print("PASS preserved v1.8.0 qualification evidence: Common Map history and stable-v1 compatibility remain intact under later releases.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
