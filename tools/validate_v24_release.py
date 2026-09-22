#!/usr/bin/env python3
"""Validate RAHP v2.4.0 VTI composition-assessment release qualification."""
from pathlib import Path
import json
import yaml

ROOT = Path(__file__).resolve().parents[1]


def y(rel):
    return yaml.safe_load((ROOT / rel).read_text(encoding="utf-8")) or {}


def main():
    q = y("method/v2.4-release-qualification.yaml")
    status = y("PROJECT-STATUS.yaml")
    rel = y("method/release.yaml")["release"]
    ver = y("method/versioning.yaml")
    profile = y("profiles/dtg/vti-assessment-profile.yaml")
    t12 = y("data/vti-programme-t12.yaml")
    errors = []

    if q.get("release") != "v2.4.0":
        errors.append("qualification release must be v2.4.0")
    if q.get("qualification") != "vti-composition-assessment-and-evidence-conservative-reconciliation":
        errors.append("qualification theme mismatch")
    if str(status.get("stable_release")) != "2.4.0" or str(status.get("development_target")) != "2.4.0":
        errors.append("project version must be 2.4.0")
    if status.get("qualification_status") != "qualified":
        errors.append("qualification status must be qualified")
    if rel.get("version") != "2.4.0" or rel.get("tag") != "v2.4.0":
        errors.append("release declaration mismatch")
    if rel.get("theme") != "VTI Composition Assessment and Evidence-Conservative Reconciliation":
        errors.append("release theme mismatch")
    if (rel.get("name") or {}).get("common") != "Redbreast Jezebel":
        errors.append("release codename mismatch")
    if (rel.get("name") or {}).get("scientific") != "Delias acalis":
        errors.append("release scientific name mismatch")
    if ver.get("stable_release") != "v2.4.0":
        errors.append("versioning stable_release mismatch")

    compat = status.get("compatibility") or {}
    contracts = ver.get("contracts") or {}
    if compat.get("engine_contract") != "rahp-engine-contract-v1" or str(contracts.get("engine_revision")) != "1.3":
        errors.append("engine compatibility changed")
    if compat.get("normalized_result_schema") != 1 or compat.get("evidence_retention_contract") != "rahp-evidence-retention-v1":
        errors.append("result/evidence compatibility changed")

    required = [
        "profiles/dtg/vti-assessment-profile.yaml",
        "schemas/vti-assessment.schema.json",
        "docs/vti-assessment-index.md",
        "docs/vti-programme-reconciliation.md",
        "docs/vti-release-upstream-judgment.md",
        "data/vti-programme-t12.yaml",
        "tools/validate_vti_assessment_profile.py",
        "tools/render_vti_programme_reconciliation.py",
        "tools/validate_vti_t12_judgment.py",
        "docs/releases/v2.4.0.md",
    ]
    for item in required:
        if not (ROOT / item).is_file():
            errors.append(f"missing v2.4 qualification artifact: {item}")

    caps = q.get("qualified_capabilities") or {}
    for key in (
        "vti_version_pinned_assessment_profile",
        "vti_machine_readable_assessment_contract",
        "multi_submission_validation",
        "deterministic_assessment_index",
        "deterministic_programme_reconciliation",
        "eight_supported_composition_families",
        "specialist_privacy_indeterminacy_preserved",
        "component_substitution_evidence_gate_preserved",
        "release_upstream_packaging_judgment",
    ):
        if not caps.get(key):
            errors.append(f"missing qualified capability: {key}")

    inv = q.get("invariants") or {}
    for key in (
        "missing_evidence_never_pass",
        "component_pass_not_composition_pass",
        "workflow_success_not_assurance_success",
        "normative_convergence_not_implementation_conformance",
        "indeterminate_not_silently_promoted",
        "specialist_boundary_preserved",
        "synthetic_substitution_not_promoted",
        "upstream_vti_remains_normative_authority",
    ):
        if not inv.get(key):
            errors.append(f"missing invariant: {key}")

    baseline = q.get("vti_baseline") or {}
    psource = profile.get("vti_source") or {}
    if baseline.get("commit") != psource.get("commit"):
        errors.append("qualification VTI source pin differs from active profile")
    mappings = profile.get("requirement_map") or []
    verified = [m for m in mappings if m.get("evidence_state") == "verified"]
    if len(mappings) != 10 or len(verified) != 8:
        errors.append("VTI family reconciliation count mismatch")
    if baseline.get("current_submissions") != 9:
        errors.append("expected nine current assessment submissions")
    if (baseline.get("privacy_assessment") or {}).get("disposition") != "indeterminate":
        errors.append("privacy indeterminate boundary not preserved")
    if (baseline.get("component_substitution") or {}).get("disposition") != "evidence-required":
        errors.append("component substitution evidence-required boundary not preserved")

    release_judgment = t12.get("release_judgment") or {}
    if release_judgment.get("disposition") != "minor_release_warranted":
        errors.append("T12 did not warrant minor release")
    if release_judgment.get("candidate_next_version") != "2.4.0":
        errors.append("T12 candidate next version is not 2.4.0")

    pkg = json.loads((ROOT / "package.json").read_text())
    if pkg.get("version") != "2.4.0":
        errors.append("root package version mismatch")
    portable = y("examples/portable-instance/data/instance.yaml")
    if str((portable.get("instance") or {}).get("toolkit_version")) != "v2.4.0":
        errors.append("portable fixture version mismatch")

    if errors:
        for e in errors:
            print("ERROR:", e)
        return 1
    print("PASS v2.4.0 qualified: VTI composition assessment and evidence-conservative reconciliation with preserved compatibility boundaries.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
