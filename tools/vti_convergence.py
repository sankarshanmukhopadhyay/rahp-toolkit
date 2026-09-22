#!/usr/bin/env python3
"""Validate and summarize selective VTI source convergence."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "profiles" / "dtg" / "vti-assessment-profile.yaml"
HISTORY = ROOT / "data" / "vti-baseline-history.yaml"
EVENT = ROOT / "data" / "vti-convergence-events" / "75391a27-to-3cbd7300.yaml"
NEGATIVE_FIXTURE_DIR = ROOT / "fixtures" / "negative"
ALLOWED_CHANGE_CLASSES = {"normative-semantic", "evidence-only", "structural-normative-contract"}
ALLOWED_IMPACT_STATES = {"evidence-required", "specialist-evidence-required", "verified", "indeterminate"}
SHA40 = 40


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: top-level value must be a mapping")
    return value


def negative_fixture_ids() -> set[str]:
    ids: set[str] = set()
    for path in sorted(NEGATIVE_FIXTURE_DIR.glob("*.yaml")):
        fixture = load_yaml(path)
        fixture_id = str(fixture.get("id") or "").strip()
        if fixture_id:
            ids.add(fixture_id)
    return ids


def validate_fixture_mappings(event: dict[str, Any], known_fixture_ids: set[str]) -> tuple[set[str], list[str]]:
    selected: set[str] = set()
    errors: list[str] = []
    for impact in event.get("family_impacts") or []:
        family = str(impact.get("family") or "<unknown>")
        refs = impact.get("negative_fixture_ids")
        if not isinstance(refs, list) or not refs:
            errors.append(f"{family}: impacted family must declare at least one negative_fixture_id")
            continue
        if len(refs) != len(set(refs)):
            errors.append(f"{family}: negative_fixture_ids must be unique")
        for fixture_id in refs:
            if fixture_id not in known_fixture_ids:
                errors.append(f"{family}: unknown negative fixture {fixture_id}")
            else:
                selected.add(str(fixture_id))
    return selected, errors


def _sha(value: Any) -> bool:
    text = str(value or "")
    return len(text) == SHA40 and all(ch in "0123456789abcdef" for ch in text)


def validate() -> tuple[dict[str, Any], list[str]]:
    profile = load_yaml(PROFILE)
    history = load_yaml(HISTORY)
    event = load_yaml(EVENT)
    errors: list[str] = []

    if history.get("schema") != "rahp-vti-baseline-history/v1":
        errors.append("baseline history schema is not supported")
    if event.get("schema") != "rahp-vti-convergence-event/v1":
        errors.append("convergence event schema is not supported")

    source = profile.get("vti_source") or {}
    baseline = event.get("baseline") or {}
    head = event.get("observed_head") or {}
    active = history.get("active_baseline") or {}

    for label, commit in (
        ("profile baseline", source.get("commit")),
        ("event baseline", baseline.get("commit")),
        ("observed head", head.get("commit")),
        ("history active baseline", active.get("commit")),
    ):
        if not _sha(commit):
            errors.append(f"{label} must be a lowercase immutable 40-hex commit")

    if source.get("repository") != event.get("repository") or source.get("repository") != history.get("repository"):
        errors.append("VTI repository identity differs across profile, history, and event")
    if source.get("commit") != baseline.get("commit") or source.get("commit") != active.get("commit"):
        errors.append("active profile baseline must remain unchanged until reconciliation")
    if head.get("commit") == baseline.get("commit"):
        errors.append("event claims drift but baseline and head are identical")
    if event.get("drift_detected") is not True:
        errors.append("live event must explicitly record source drift")
    if event.get("automatic_repin") is not False:
        errors.append("source drift must not automatically repin the assessment baseline")
    if (history.get("policy") or {}).get("automatic_repin") is not False:
        errors.append("baseline history must prohibit automatic repinning")

    mappings = profile.get("requirement_map") or []
    known_families = {item.get("family") for item in mappings if isinstance(item, dict)}
    family_impacts = event.get("family_impacts") or []
    impacted = set()
    for impact in family_impacts:
        family = impact.get("family")
        if family not in known_families:
            errors.append(f"unknown impacted family: {family}")
        impacted.add(family)
        if impact.get("state") not in ALLOWED_IMPACT_STATES:
            errors.append(f"{family}: unsupported impact state {impact.get('state')!r}")
        if not impact.get("triggering_requirements"):
            errors.append(f"{family}: triggering_requirements must not be empty")

    selected_fixtures, fixture_errors = validate_fixture_mappings(event, negative_fixture_ids())
    errors.extend(fixture_errors)

    unaffected = set(event.get("unaffected_families") or [])
    expected_unaffected = known_families - impacted
    if unaffected != expected_unaffected:
        errors.append(
            "unaffected family set must equal active profile families minus selectively impacted families"
        )

    changes = event.get("changes") or []
    classes = set()
    added_requirements: set[str] = set()
    for change in changes:
        change_id = change.get("id")
        change_class = change.get("class")
        classes.add(change_class)
        if change_class not in ALLOWED_CHANGE_CLASSES:
            errors.append(f"{change_id}: unsupported change class {change_class!r}")
        additions = set(change.get("requirements_added") or [])
        added_requirements |= additions
        if change_class == "evidence-only":
            if change.get("requirement_text_changed") is not False:
                errors.append(f"{change_id}: evidence-only change cannot claim requirement text changed")
            if change.get("invalidates_existing_assessment") is not False:
                errors.append(f"{change_id}: evidence-only drift must not automatically invalidate assessment families")
            if change.get("affected_families"):
                errors.append(f"{change_id}: evidence-only drift must not stale composition families by default")
        if change_class == "normative-semantic" and not additions:
            errors.append(f"{change_id}: normative-semantic change requires requirement additions or changes")

    mapped_triggers = {
        requirement
        for impact in family_impacts
        for requirement in (impact.get("triggering_requirements") or [])
    }
    composition_additions = {item for item in added_requirements if item.startswith("VTI-CMP-")}
    if not composition_additions <= mapped_triggers:
        errors.append(
            f"new composition requirements lack family impact mapping: {sorted(composition_additions - mapped_triggers)}"
        )

    reassessment = event.get("reassessment") or {}
    if reassessment.get("mode") != "selective":
        errors.append("VTI drift must use selective reassessment")
    if reassessment.get("whole_programme_stale") is not False:
        errors.append("unrelated VTI families must not be marked stale")

    contracts = event.get("contract_impacts") or []
    for contract in contracts:
        state = contract.get("state")
        evidence = contract.get("evidence")
        if state == "verified-compatible":
            if not evidence:
                errors.append(f"{contract.get('id')}: verified-compatible contract impact requires evidence")
            elif not (ROOT / str(evidence)).is_file():
                errors.append(f"{contract.get('id')}: compatibility evidence does not exist: {evidence}")
    unresolved_family = [
        item for item in family_impacts
        if item.get("state") in {"evidence-required", "specialist-evidence-required"}
    ]
    unresolved_contracts = [item for item in contracts if item.get("state") == "review-required"]
    rebaseline = event.get("rebaseline") or {}
    should_block = bool(unresolved_family or unresolved_contracts)
    if should_block and rebaseline.get("state") != "blocked":
        errors.append("rebaseline must remain blocked while impacted evidence or contract review is unresolved")
    if not should_block and rebaseline.get("state") != "ready":
        errors.append("rebaseline must be ready once every impacted family and contract review is reconciled")
    if rebaseline.get("baseline_mutated") is not False:
        errors.append("event must not claim the baseline changed before controlled rebaseline")

    observations = history.get("observations") or []
    observed_commits = [item.get("commit") for item in observations]
    for required in (baseline.get("commit"), *(item.get("commit") for item in event.get("intermediate_heads") or []), head.get("commit")):
        if required not in observed_commits:
            errors.append(f"baseline history missing observed commit {required}")

    summary = {
        "schema": "rahp-vti-convergence-validation/v1",
        "baseline": baseline.get("commit"),
        "observed_head": head.get("commit"),
        "drift_detected": event.get("drift_detected"),
        "change_classes": sorted(classes),
        "impacted_families": sorted(impacted),
        "unaffected_families": sorted(unaffected),
        "negative_fixture_ids": sorted(selected_fixtures),
        "rebaseline_state": rebaseline.get("state"),
        "unresolved_family_impacts": [item.get("family") for item in unresolved_family],
        "unresolved_contract_impacts": [item.get("id") for item in unresolved_contracts],
        "errors": len(errors),
    }
    return summary, errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument(
        "--require-rebaseline-ready",
        action="store_true",
        help="fail unless all impacted evidence is reconciled and the event declares rebaseline ready",
    )
    args = parser.parse_args()
    try:
        summary, errors = validate()
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f"FAIL VTI convergence: {exc}", file=sys.stderr)
        return 1

    if args.require_rebaseline_ready and summary.get("rebaseline_state") != "ready":
        errors.append("controlled rebaseline is not ready")

    if args.json:
        print(json.dumps({**summary, "problems": errors}, indent=2, sort_keys=True))
    elif errors:
        print("FAIL VTI convergence")
        for error in errors:
            print(f"- {error}")
    else:
        print(
            "PASS VTI convergence: "
            f"{str(summary['baseline'])[:8]} -> {str(summary['observed_head'])[:8]}, "
            f"impacted={','.join(summary['impacted_families'])}, "
            f"rebaseline={summary['rebaseline_state']}"
        )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
