#!/usr/bin/env python3
"""Validate the RAHP v1.9.0 portable clean-room assurance qualification."""
from __future__ import annotations
import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]

def load_yaml(rel: str):
    return yaml.safe_load((ROOT / rel).read_text(encoding="utf-8")) or {}

def main() -> int:
    q = load_yaml("method/v1.9-release-qualification.yaml")
    status = load_yaml("PROJECT-STATUS.yaml")
    release = load_yaml("method/release.yaml")
    versioning = load_yaml("method/versioning.yaml")
    errors: list[str] = []

    if q.get("release") != "v1.9.0": errors.append("qualification manifest must identify v1.9.0")
    if q.get("qualification") != "portable-clean-room-assurance": errors.append("qualification theme mismatch")
    if str(status.get("stable_release")) != "1.9.0": errors.append("PROJECT-STATUS stable_release must be 1.9.0")
    if status.get("development_target") != "1.9.0": errors.append("development_target must be 1.9.0")
    if status.get("release_status") != "released" or status.get("qualification_status") != "qualified": errors.append("release state must be released/qualified")
    if status.get("qualification_contract") != "method/v1.9-release-qualification.yaml": errors.append("qualification contract mismatch")
    if versioning.get("stable_release") != "v1.9.0": errors.append("versioning stable_release must be v1.9.0")

    declared = release.get("release") or {}
    if declared.get("version") != "1.9.0": errors.append("release declaration version mismatch")
    if declared.get("theme") != "Portable Clean-Room Assurance": errors.append("release theme mismatch")
    name = declared.get("name") or {}
    if name.get("common") != "Lesser Mime" or name.get("scientific") != "Papilio epycides": errors.append("release name mismatch")

    compat = q.get("stable_compatibility") or {}
    for key, value in compat.items():
        if (status.get("compatibility") or {}).get(key) != value: errors.append(f"compatibility mismatch: {key}")

    clean_room = ROOT / ".github/workflows/clean-room-assessment.yml"
    if not clean_room.is_file(): errors.append("generic clean-room executor missing")
    else:
        text = clean_room.read_text(encoding="utf-8").lower()
        for forbidden in ("dogwood", "openvtc", "verifiable-trust-infrastructure"):
            if forbidden in text: errors.append(f"generic clean-room workflow leaks target token: {forbidden}")

    governance = ROOT / ".github/workflows/workflow-governance.yml"
    if not governance.is_file(): errors.append("workflow governance guard missing")
    workflow_dir = ROOT / ".github/workflows"
    offenders = [p.name for p in workflow_dir.glob("*clean-room*.yml") if p.name != "clean-room-assessment.yml"]
    if offenders: errors.append(f"target/issue-specific clean-room workflows remain: {offenders}")

    run_spec = json.loads((ROOT / "clean-room/run-spec.json").read_text(encoding="utf-8"))
    if run_spec.get("schema") != "rahp-clean-room-run/v1": errors.append("clean-room run spec schema mismatch")
    revision = str((run_spec.get("target") or {}).get("revision") or "")
    if len(revision) != 40: errors.append("clean-room target revision is not immutable")

    pca = q.get("portable_clean_room") or {}
    for key in ("declarative_run_spec","immutable_target_pins","historical_inputs_excluded","producer_attribution_required","target_specific_behavior_confined_to_adapter_or_run_spec"):
        if pca.get(key) is not True: errors.append(f"portable clean-room capability not qualified: {key}")

    exp = q.get("experiment_semantics") or {}
    for key in ("positive_control_is_detector_sensitivity","positive_control_join_is_not_privacy_failure","unlinkability_pressure_requires_context_distinct_execution","missing_evidence_is_not_pass","composition_evidence_not_promoted_to_target_native"):
        if exp.get(key) is not True: errors.append(f"experiment semantic invariant missing: {key}")

    req = q.get("required_evidence") or {}
    for key in ("generic_clean_room_issue","generic_clean_room_pr","dpip_clean_room_examination","target_native_pressure_issue","target_native_pressure_pr"):
        if not str(req.get(key) or "").startswith("https://github.com/"): errors.append(f"required evidence link missing: {key}")

    for rel in ("docs/releases/v1.9.0.md", "tools/validate_v19_release.py", "method/v1.9-release-qualification.yaml"):
        if not (ROOT / rel).is_file(): errors.append(f"required v1.9 artifact missing: {rel}")

    if errors:
        for error in errors: print("ERROR:", error)
        return 1
    print("PASS v1.9.0 qualified: portable clean-room assurance is reusable, bounded, attributable, and stable-v1 compatible.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
