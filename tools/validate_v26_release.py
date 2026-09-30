#!/usr/bin/env python3
"""Validate RAHP v2.6.0 full-stack assurance release qualification."""
from pathlib import Path
import json
import yaml

ROOT = Path(__file__).resolve().parents[1]

def load_yaml(rel):
    return yaml.safe_load((ROOT / rel).read_text(encoding="utf-8")) or {}

def main():
    q = load_yaml("method/v2.6-release-qualification.yaml")
    status = load_yaml("PROJECT-STATUS.yaml")
    release = load_yaml("method/release.yaml")["release"]
    versioning = load_yaml("method/versioning.yaml")
    errors = []

    if q.get("release") != "v2.6.0":
        errors.append("qualification release must be v2.6.0")
    if q.get("qualification") != "full-stack-assurance-orchestration-and-explicit-evidence-state":
        errors.append("qualification theme mismatch")
    if str(status.get("stable_release")) != "2.6.0" or str(status.get("development_target")) != "2.6.0":
        errors.append("project version must be 2.6.0")
    if release.get("version") != "2.6.0" or release.get("tag") != "v2.6.0":
        errors.append("release declaration mismatch")
    if release.get("theme") != "Full-Stack Assurance Orchestration and Explicit Evidence State":
        errors.append("release theme mismatch")
    if (release.get("name") or {}).get("common") != "Commander":
        errors.append("release codename mismatch")
    if (release.get("name") or {}).get("scientific") != "Moduza procris":
        errors.append("release scientific name mismatch")
    if versioning.get("stable_release") != "v2.6.0":
        errors.append("versioning stable_release mismatch")

    compat = status.get("compatibility") or {}
    contracts = versioning.get("contracts") or {}
    if compat.get("engine_contract") != "rahp-engine-contract-v1" or str(contracts.get("engine_revision")) != "1.3":
        errors.append("engine compatibility changed")
    if compat.get("normalized_result_schema") != 1:
        errors.append("normalized result schema changed")
    if compat.get("evidence_retention_contract") != "rahp-evidence-retention-v1":
        errors.append("evidence retention contract changed")

    required = [
        "docs/full-stack-assurance-orchestration.md",
        "tests/test_post_851_full_stack_assurance.py",
        "data/negative-fixture-inventory.yaml",
        "docs/vc-data-model-threat-model-gap-analysis.md",
        "docs/performance-architecture.md",
        "docs/performance-characterisation.md",
        "docs/lpc-pre-demo-scope-manifest.md",
        "docs/lpc-pre-demo-evidence-templates.md",
        "docs/lpc-pre-demo-assurance-record.md",
        "tools/composition_compatibility.py",
        "tools/profile_execution.py",
        "tools/cross_spec_scale_workload.py",
        "docs/releases/v2.6.0.md",
    ]
    for item in required:
        if not (ROOT / item).is_file():
            errors.append(f"missing v2.6 qualification artifact: {item}")

    for key, value in (q.get("qualified_capabilities") or {}).items():
        if value is not True:
            errors.append(f"qualified capability is not true: {key}")
    for key, value in (q.get("invariants") or {}).items():
        if value is not True:
            errors.append(f"release invariant is not true: {key}")

    research = q.get("research_boundary") or {}
    if research.get("stable_release_includes_policy_as_subject") is not False:
        errors.append("policy-as-subject research leaked into stable release")
    if research.get("stable_release_includes_decision_resolution_research") is not False:
        errors.append("decision-resolution research leaked into stable release")

    orchestration = (ROOT / "docs/full-stack-assurance-orchestration.md").read_text(encoding="utf-8")
    for token in ("process_state", "assurance_state", "evidence_maturity",
                  "required-but-not-executed", "ATTEMPTED_UNAVAILABLE",
                  "NO_APPLICABLE_PRODUCER", "DRARM silence is invalid",
                  "component PASS does not count as composition PASS"):
        if token not in orchestration:
            errors.append(f"full-stack contract missing required marker: {token}")

    inventory = load_yaml("data/negative-fixture-inventory.yaml")
    fixture_ids = {item.get("id") for item in inventory.get("entries") or []}
    for fixture_id in ("INV-POST851-LENS-OMISSION",
                       "INV-POST851-SECURITY-TYPE-CONFUSION",
                       "INV-POST851-DRARM-OMISSION"):
        if fixture_id not in fixture_ids:
            errors.append(f"missing post-851 negative fixture: {fixture_id}")

    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    if package.get("version") != "2.6.0":
        errors.append("root package version mismatch")
    portable = load_yaml("examples/portable-instance/data/instance.yaml")
    if str((portable.get("instance") or {}).get("toolkit_version")) != "v2.6.0":
        errors.append("portable fixture version mismatch")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS v2.6.0 qualified: full-stack assurance orchestration and explicit evidence state with stable compatibility boundaries.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
