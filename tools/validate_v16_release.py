#!/usr/bin/env python3
"""Validate the RAHP v1.6.0 qualification and release-state contract."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "method" / "v1.6-release-qualification.yaml"
VALID_RESIDUAL_STATES = {
    "assured", "controlled", "finding", "assurance-gap", "review-required",
    "not-assessed", "not-applicable",
}


def load_yaml(rel: str):
    return yaml.safe_load((ROOT / rel).read_text(encoding="utf-8"))


def semver_tuple(value: str) -> tuple[int, int, int]:
    raw = value.lstrip("v")
    major, minor, patch = raw.split(".")
    return int(major), int(minor), int(patch)


def main() -> int:
    q = load_yaml("method/v1.6-release-qualification.yaml")
    status = load_yaml("PROJECT-STATUS.yaml")
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    lock = json.loads((ROOT / "package-lock.json").read_text(encoding="utf-8"))
    versioning = load_yaml("method/versioning.yaml")
    errors: list[str] = []

    if q.get("release") != "v1.6.0":
        errors.append("qualification manifest must identify release v1.6.0")
    if status.get("stable_release") != "1.6.0":
        errors.append("PROJECT-STATUS stable_release must be 1.6.0")
    if status.get("development_target") != "1.6.0":
        errors.append("PROJECT-STATUS development_target must be 1.6.0")
    if status.get("release_status") != "released":
        errors.append("v1.6.0 release commit must declare release_status released")
    if status.get("qualification_status") != "qualified":
        errors.append("v1.6.0 release commit must declare qualification_status qualified")
    if status.get("qualification_contract") != "method/v1.6-release-qualification.yaml":
        errors.append("PROJECT-STATUS must point at the v1.6 qualification contract")

    compat = status.get("compatibility") or {}
    for key, expected in (q.get("stable_compatibility") or {}).items():
        if compat.get(key) != expected:
            errors.append(f"stable compatibility mismatch for {key}: {compat.get(key)!r} != {expected!r}")

    if versioning.get("stable_release") != "v1.6.0":
        errors.append("method/versioning.yaml stable_release must be v1.6.0")

    if package.get("version") != "1.6.0":
        errors.append("root package version must be 1.6.0")
    if lock.get("version") != "1.6.0" or (lock.get("packages") or {}).get("", {}).get("version") != "1.6.0":
        errors.append("package-lock root version must be 1.6.0")

    workspace_paths = [
        "packages/schema/package.json",
        "packages/core/package.json",
        "packages/graph/package.json",
        "packages/cli/package.json",
    ]
    for rel in workspace_paths:
        doc = json.loads((ROOT / rel).read_text(encoding="utf-8"))
        if doc.get("version") != "1.6.0":
            errors.append(f"workspace package must be 1.6.0: {rel}")
        for dep, dep_version in (doc.get("dependencies") or {}).items():
            if dep.startswith("@rahp/") and dep_version != "1.6.0":
                errors.append(f"workspace dependency {dep} in {rel} must be 1.6.0")

    for label, rel in (q.get("required_evidence") or {}).items():
        if not (ROOT / rel).exists():
            errors.append(f"required evidence missing ({label}): {rel}")

    expectations = q.get("coverage_expectations") or {}
    corpus_docs = []
    total_scenarios = 0
    qualified_corpus_ids = set(q.get("qualified_corpus_ids") or [])
    for path in sorted((ROOT / "corpora").rglob("*.yaml")):
        doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        corpus = doc.get("corpus")
        if not isinstance(corpus, dict):
            continue
        if qualified_corpus_ids and corpus.get("id") not in qualified_corpus_ids:
            continue
        corpus_docs.append(corpus)
        total_scenarios += len(corpus.get("scenarios") or [])

    if len(corpus_docs) != expectations.get("total_corpora"):
        errors.append(f"expected {expectations.get('total_corpora')} qualified corpora, found {len(corpus_docs)}")
    if total_scenarios != expectations.get("total_scenarios"):
        errors.append(f"expected {expectations.get('total_scenarios')} qualified scenarios, found {total_scenarios}")

    by_id = {c.get("id"): c for c in corpus_docs}
    tt = by_id.get("CORPUS-TRUST-TASKS") or {}
    cs = by_id.get("CORPUS-DTG-CREDSPEC") or {}
    xsp = by_id.get("CORPUS-TT-CREDSPEC-COMPOSED") or {}
    pins = q.get("source_pins") or {}
    if tt.get("source_commit") != pins.get("trust_tasks"):
        errors.append("Trust Tasks corpus source pin does not match v1.6 qualification")
    if cs.get("source_commit") != pins.get("credential_spec"):
        errors.append("Credential Spec corpus source pin does not match v1.6 qualification")
    for corpus, key, label in (
        (tt, "trust_tasks_scenarios", "Trust Tasks"),
        (cs, "credential_spec_scenarios", "Credential Spec"),
        (xsp, "composed_scenarios", "composed TT×CredSpec"),
    ):
        actual = len(corpus.get("scenarios") or [])
        expected = expectations.get(key)
        if actual != expected:
            errors.append(f"{label} corpus expected {expected} scenarios, found {actual}")

    deps = {d.get("corpus_id"): d.get("source_commit") for d in xsp.get("depends_on") or []}
    if deps.get("CORPUS-TRUST-TASKS") != pins.get("trust_tasks"):
        errors.append("composed corpus does not depend on the qualified Trust Tasks pin")
    if deps.get("CORPUS-DTG-CREDSPEC") != pins.get("credential_spec"):
        errors.append("composed corpus does not depend on the qualified Credential Spec pin")

    review = load_yaml("examples/cross-spec/trust-tasks-credspec/pressure-test.yaml").get("review") or {}
    if review.get("target", {}).get("commit") != pins.get("trust_tasks"):
        errors.append("TT×CredSpec reassessment is not pinned to the qualified Trust Tasks revision")
    if review.get("target", {}).get("companion_commit") != pins.get("credential_spec"):
        errors.append("TT×CredSpec reassessment is not pinned to the qualified Credential Spec revision")
    if review.get("lineage", {}).get("prior_record") != "history/pre-corpus-expansion-2026-08-23.yaml":
        errors.append("TT×CredSpec reassessment must preserve the pre-expansion history pointer")
    if review.get("assurance", {}).get("assurance_delta", {}).get("disposition") != "refined":
        errors.append("TT×CredSpec reassessment must record the source-pinned corpus delta as refined")

    current_baselines = load_yaml("examples/current-baselines.yaml")
    current = current_baselines.get("current_rahp_release") or {}
    if semver_tuple(str(current.get("version", "v0.0.0"))) > semver_tuple("v1.5.0"):
        errors.append("v1.6 release must not silently promote maintained example baselines without retest")
    for example in current_baselines.get("maintained_examples") or []:
        state = (example.get("current_baseline") or {}).get("residual_state")
        if state not in VALID_RESIDUAL_STATES:
            errors.append(f"maintained example {example.get('id')} has invalid residual state")

    release_name = status.get("release_name") or {}
    cut = q.get("release_cut") or {}
    if release_name.get("common_name") != cut.get("selected_common_name"):
        errors.append("recorded v1.6 common release name does not match qualification manifest")
    if release_name.get("scientific_name") != cut.get("selected_scientific_name"):
        errors.append("recorded v1.6 scientific release name does not match qualification manifest")
    if release_name.get("selected_on") != cut.get("selected_on"):
        errors.append("recorded v1.6 selection date does not match qualification manifest")
    if (status.get("release_naming") or {}).get("selection") != "random-at-release-time":
        errors.append("West Bengal butterfly naming policy must remain random-at-release-time")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    release_notes = (ROOT / "docs/releases/v1.6.0.md").read_text(encoding="utf-8") if (ROOT / "docs/releases/v1.6.0.md").exists() else ""
    for label, text in (("README", readme), ("CHANGELOG", changelog), ("release notes", release_notes)):
        if "v1.6.0" not in text or "Common Earl" not in text:
            errors.append(f"{label} is not synchronized to v1.6.0 Common Earl")

    workflow = ROOT / str(cut.get("publication_workflow", ""))
    if not workflow.exists():
        errors.append("qualified release publication workflow is missing")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(
        "PASS v1.6.0 qualified: stable v1 compatibility preserved; source-pinned corpus coverage, "
        "composed reassessment lineage, documentation routing, workspace metadata and release publication contract are synchronized."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
