#!/usr/bin/env python3
"""Validate RAHP v2.6.0 full-stack assurance release qualification."""
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]

def load_yaml(rel):
    return yaml.safe_load((ROOT / rel).read_text(encoding="utf-8")) or {}

def main():
    q = load_yaml("method/v2.6-release-qualification.yaml")
    errors = []

    if q.get("release") != "v2.6.0":
        errors.append("qualification release must be v2.6.0")
    if q.get("qualification") != "full-stack-assurance-orchestration-and-explicit-evidence-state":
        errors.append("qualification theme mismatch")
    # Historical v2.6 qualification is immutable evidence, not a constraint on
    # the current release declaration. Current metadata is verified by release.py.
    # A later release must not make this historical validator fail solely because
    # package/status/versioning/codename moved forward.
    compat = q.get("stable_compatibility") or {}
    expected_compat = {
        "engine_contract": "rahp-engine-contract-v1",
        "engine_revision": "1.3",
        "normalized_result_schema": 1,
        "evidence_retention_contract": "rahp-evidence-retention-v1",
    }
    if str(compat.get("engine_revision")) != "1.3" or {
        key: value for key, value in compat.items() if key != "engine_revision"
    } != {key: value for key, value in expected_compat.items() if key != "engine_revision"}:
        errors.append("historical v2.6 compatibility baseline changed")
    release_cut = q.get("release_cut") or {}
    if (release_cut.get("tag"), release_cut.get("selected_common_name"), release_cut.get("selected_scientific_name")) != (
        "v2.6.0", "Commander", "Moduza procris"
    ):
        errors.append("historical v2.6 release identity changed")

    required = [
        "docs/full-stack-assurance-orchestration.md",
        "tests/test_post_851_full_stack_assurance.py",
        "data/negative-fixture-inventory.yaml",
        "docs/review/vc-data-model-threat-model-2.1-gap-analysis.md",
        "docs/performance-architecture-decision.md",
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
        if token.casefold() not in orchestration.casefold():
            errors.append(f"full-stack contract missing required marker: {token}")

    inventory = load_yaml("data/negative-fixture-inventory.yaml")
    fixture_ids = {item.get("id") for item in inventory.get("entries") or []}
    for fixture_id in ("INV-POST851-LENS-OMISSION",
                       "INV-POST851-SECURITY-TYPE-CONFUSION",
                       "INV-POST851-DRARM-OMISSION"):
        if fixture_id not in fixture_ids:
            errors.append(f"missing post-851 negative fixture: {fixture_id}")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS v2.6.0 qualified: full-stack assurance orchestration and explicit evidence state with stable compatibility boundaries.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
