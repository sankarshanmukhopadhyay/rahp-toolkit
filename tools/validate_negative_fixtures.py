#!/usr/bin/env python3
"""Validate the reusable RAHP negative-fixture contract and inventory."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "negative-fixture.schema.json"
FIXTURE_DIR = ROOT / "fixtures" / "negative"
INVENTORY = ROOT / "data" / "negative-fixture-inventory.yaml"
LENSES = {"rahp", "security", "composition", "drarm", "specialist"}
POSITIVE_STATES = {"pass", "verified", "permit"}
POSITIVE_TERMINALS = {"green"}


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: top-level value must be a mapping")
    return value


def split_ref(ref: str) -> tuple[Path, str | None]:
    raw_path, marker = (ref.split("#", 1) + [None])[:2] if "#" in ref else (ref, None)
    return ROOT / raw_path, marker


def validate_ref(ref: str, label: str) -> list[str]:
    errors: list[str] = []
    path, marker = split_ref(ref)
    if not path.is_file():
        return [f"{label}: referenced file does not exist: {ref}"]
    if marker:
        text = path.read_text(encoding="utf-8")
        if marker not in text:
            errors.append(f"{label}: fragment {marker!r} not found in {path.relative_to(ROOT)}")
    return errors


def validate_fixture(path: Path, schema: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    fixture = load_yaml(path)
    errors = [
        f"{path.relative_to(ROOT)} schema: {'/'.join(map(str, error.absolute_path)) or '(root)'}: {error.message}"
        for error in Draft202012Validator(schema).iter_errors(fixture)
    ]
    if errors:
        return fixture, errors

    fixture_id = fixture["id"]
    owner = fixture["proposition"]["owner"]
    primary = fixture["lens"]["primary"]
    if owner != primary:
        errors.append(f"{fixture_id}: proposition.owner must equal lens.primary")

    evidence = fixture["evidence"]
    deficient = {
        state: values
        for state, values in evidence.items()
        if state in {"missing", "stale", "contradicted", "unsupported"} and values
    }
    expected = fixture["expected"]
    if deficient and (
        expected["state"] in POSITIVE_STATES
        or expected.get("terminal_colour") in POSITIVE_TERMINALS
    ):
        errors.append(
            f"{fixture_id}: deficient material evidence {sorted(deficient)} cannot produce "
            f"{expected['state']}/{expected.get('terminal_colour', 'n/a')}"
        )

    if expected["state"] in expected["prohibited"]:
        errors.append(f"{fixture_id}: expected state is also prohibited")
    if expected.get("terminal_colour") in expected["prohibited"]:
        errors.append(f"{fixture_id}: expected terminal colour is also prohibited")

    errors.extend(validate_ref(fixture["source"]["ref"], f"{fixture_id} source"))
    errors.extend(validate_ref(fixture["positive_control"]["ref"], f"{fixture_id} positive_control"))

    specialist = fixture["specialist"]
    if specialist["required"] and not specialist.get("name"):
        errors.append(f"{fixture_id}: specialist.required=true requires specialist.name")
    if primary == "specialist":
        if not specialist["required"]:
            errors.append(f"{fixture_id}: specialist-owned fixture must require a specialist")
        if not specialist["owns"]:
            errors.append(f"{fixture_id}: specialist-owned fixture must state what the specialist owns")
        if not specialist["does_not_own"]:
            errors.append(f"{fixture_id}: specialist-owned fixture must state an ownership boundary")

    drarm = fixture["drarm"]
    if primary == "drarm":
        if not drarm["applicable"]:
            errors.append(f"{fixture_id}: DRARM-owned fixture must set drarm.applicable=true")
        if not drarm.get("does_not_own"):
            errors.append(f"{fixture_id}: DRARM-owned fixture must preserve a does_not_own boundary")

    return fixture, errors


def validate_inventory(contract_ids: set[str]) -> tuple[dict[str, Any], list[str]]:
    inventory = load_yaml(INVENTORY)
    errors: list[str] = []
    if inventory.get("schema") != "rahp-negative-fixture-inventory/v1":
        errors.append("inventory: unsupported schema")
        return inventory, errors

    entries = inventory.get("entries")
    if not isinstance(entries, list) or not entries:
        return inventory, ["inventory: entries must be a non-empty list"]

    seen: set[str] = set()
    linked_contracts: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            errors.append("inventory: every entry must be a mapping")
            continue
        entry_id = str(entry.get("id") or "")
        if not entry_id or entry_id in seen:
            errors.append(f"inventory: entry id must be non-empty and unique: {entry_id!r}")
        seen.add(entry_id)
        lens = entry.get("owning_lens")
        if lens not in LENSES:
            errors.append(f"{entry_id}: invalid owning_lens {lens!r}")
        source_ref = str(entry.get("path") or "")
        errors.extend(validate_ref(source_ref, f"{entry_id} path"))
        positive_ref = str(entry.get("positive_counter_case") or "")
        errors.extend(validate_ref(positive_ref, f"{entry_id} positive_counter_case"))
        if entry.get("polarity") == "negative" and not positive_ref:
            errors.append(f"{entry_id}: negative inventory entry requires a positive counter-case")
        contract = entry.get("contract_fixture")
        if contract:
            linked_contracts.add(str(contract))
            if contract not in contract_ids:
                errors.append(f"{entry_id}: unknown contract_fixture {contract}")

    missing_links = contract_ids - linked_contracts
    if missing_links:
        errors.append(f"inventory: contract fixtures missing inventory linkage: {sorted(missing_links)}")
    return inventory, errors


def validate_all() -> tuple[dict[str, Any], list[str]]:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    fixture_paths = sorted(FIXTURE_DIR.glob("*.yaml"))
    errors: list[str] = []
    fixtures: list[dict[str, Any]] = []
    ids: set[str] = set()

    if not fixture_paths:
        return {}, ["no negative fixtures found"]

    for path in fixture_paths:
        fixture, fixture_errors = validate_fixture(path, schema)
        fixture_id = str(fixture.get("id") or path.name)
        if fixture_id in ids:
            errors.append(f"duplicate fixture id: {fixture_id}")
        ids.add(fixture_id)
        fixtures.append(fixture)
        errors.extend(fixture_errors)

    _inventory, inventory_errors = validate_inventory(ids)
    errors.extend(inventory_errors)

    lenses = {fixture.get("lens", {}).get("primary") for fixture in fixtures}
    missing_lenses = LENSES - lenses
    if missing_lenses:
        errors.append(f"cross-lens starter set missing: {sorted(missing_lenses)}")

    summary = {
        "schema": "rahp-negative-fixture-validation/v1",
        "fixture_count": len(fixtures),
        "lenses": sorted(lens for lens in lenses if lens),
        "fixture_ids": sorted(ids),
        "missing_evidence_invariant": "enforced",
        "positive_control_requirement": "enforced",
        "errors": len(errors),
    }
    return summary, errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="emit a machine-readable validation summary")
    args = parser.parse_args()
    try:
        summary, errors = validate_all()
    except (OSError, ValueError, json.JSONDecodeError, yaml.YAMLError) as exc:
        print(f"FAIL negative-fixture contract: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps({**summary, "problems": errors}, indent=2, sort_keys=True))
    elif errors:
        print("FAIL negative-fixture contract")
        for error in errors:
            print(f"- {error}")
    else:
        print(
            "PASS negative-fixture contract: "
            f"{summary['fixture_count']} fixtures across {', '.join(summary['lenses'])}"
        )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
