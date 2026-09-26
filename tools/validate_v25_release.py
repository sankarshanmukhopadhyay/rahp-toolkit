#!/usr/bin/env python3
"""Validate RAHP v2.5.0 continuous-realization release qualification."""
from pathlib import Path
import json

import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_yaml(rel):
    return yaml.safe_load((ROOT / rel).read_text(encoding="utf-8")) or {}


def main():
    q = load_yaml("method/v2.5-release-qualification.yaml")
    status = load_yaml("PROJECT-STATUS.yaml")
    release = load_yaml("method/release.yaml")["release"]
    versioning = load_yaml("method/versioning.yaml")
    benchmarks = load_yaml("method/execution-benchmarks.yaml")
    portability = load_yaml("examples/cawg-c2pa/post-v2.4-portability-proof.yaml")
    errors = []

    if q.get("release") != "v2.5.0":
        errors.append("qualification release must be v2.5.0")
    if q.get("qualification") != "continuous-realization-assurance-and-portable-adoption":
        errors.append("qualification theme mismatch")
    if str(status.get("stable_release")) != "2.5.0" or str(status.get("development_target")) != "2.5.0":
        errors.append("project version must be 2.5.0")
    if release.get("version") != "2.5.0" or release.get("tag") != "v2.5.0":
        errors.append("release declaration mismatch")
    if release.get("theme") != "Continuous Realization Assurance and Portable Adoption":
        errors.append("release theme mismatch")
    if (release.get("name") or {}).get("common") != "Psyche":
        errors.append("release codename mismatch")
    if (release.get("name") or {}).get("scientific") != "Leptosia nina":
        errors.append("release scientific name mismatch")
    if versioning.get("stable_release") != "v2.5.0":
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
        "docs/post-v2.4-realization-conformance.md",
        "tools/execution_telemetry.py",
        "docs/operational-telemetry.md",
        "method/execution-benchmarks.yaml",
        "tools/compare_execution_benchmarks.py",
        "docs/performance.md",
        "examples/cawg-c2pa/post-v2.4-portability-proof.yaml",
        "docs/post-v2.4-portability-proof.md",
        "tests/test_execution_telemetry.py",
        "tests/test_execution_benchmarks.py",
        "tests/test_performance_policy.py",
        "tests/test_post_v24_non_dtg_portability.py",
        "docs/releases/v2.5.0.md",
    ]
    for item in required:
        if not (ROOT / item).is_file():
            errors.append(f"missing v2.5 qualification artifact: {item}")

    for key, value in (q.get("qualified_capabilities") or {}).items():
        if value is not True:
            errors.append(f"qualified capability is not true: {key}")

    for key, value in (q.get("invariants") or {}).items():
        if value is not True:
            errors.append(f"release invariant is not true: {key}")

    research = q.get("research_boundary") or {}
    if research.get("stable_release_includes_policy_as_subject") is not False:
        errors.append("policy-as-subject research leaked into stable release")

    policy = benchmarks.get("regression_policy") or {}
    if policy.get("mode") != "relative-baseline":
        errors.append("performance regression policy mode mismatch")
    if not policy.get("require_semantic_reference_digest_match"):
        errors.append("performance policy must require semantic reference digest match")
    if not policy.get("require_same_profile") or not policy.get("require_same_contract"):
        errors.append("performance comparison must remain like-for-like")

    proof_contracts = portability.get("stable_contracts") or {}
    if proof_contracts.get("engine") != "rahp-engine-contract-v1@1.3":
        errors.append("non-DTG proof does not use stable engine contract")
    if proof_contracts.get("normalized_result_schema") != 1:
        errors.append("non-DTG proof result schema mismatch")
    if proof_contracts.get("evidence_retention") != "rahp-evidence-retention-v1":
        errors.append("non-DTG proof evidence-retention mismatch")
    if portability.get("consumer", {}).get("kind") != "non-dtg":
        errors.append("portability proof is not non-DTG")

    telemetry = (ROOT / "tools/execution_telemetry.py").read_text(encoding="utf-8")
    if 'SCHEMA = "rahp-execution-telemetry/v1"' not in telemetry:
        errors.append("execution telemetry schema missing")
    if '"assurance_evidence": False' not in telemetry or '"may_set_assurance_outcome": False' not in telemetry:
        errors.append("telemetry authority boundary missing")

    comparator = (ROOT / "tools/compare_execution_benchmarks.py").read_text(encoding="utf-8")
    if '"assurance_evidence": False' not in comparator or '"may_set_assurance_outcome": False' not in comparator:
        errors.append("performance authority boundary missing")

    realization = (ROOT / "docs/post-v2.4-realization-conformance.md").read_text(encoding="utf-8")
    for token in ("#799", "#609", "#691", "#797", "#690", "EVIDENCE_REQUIRED", "WAITING_EXTERNAL"):
        if token not in realization:
            errors.append(f"realization reconciliation missing required residual marker: {token}")

    adoption = (ROOT / "docs/adoption-guide.md").read_text(encoding="utf-8")
    for token in ("DPIP v0.3.0", "Trust Protocol Interop Lab v0.7.0"):
        if token not in adoption:
            errors.append(f"adoption guidance missing current portfolio version: {token}")

    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    if package.get("version") != "2.5.0":
        errors.append("root package version mismatch")

    portable = load_yaml("examples/portable-instance/data/instance.yaml")
    if str((portable.get("instance") or {}).get("toolkit_version")) != "v2.5.0":
        errors.append("portable fixture version mismatch")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1

    print(
        "PASS v2.5.0 qualified: continuous realization assurance, "
        "assurance-safe telemetry, semantic-preserving performance controls, "
        "and non-DTG portability with stable compatibility boundaries."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
