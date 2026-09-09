#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import yaml

SCHEMA = "rahp-dtg-portfolio-baseline/v1"
REQUIRED_PINS = ("trust_tasks", "credential_spec", "openvtc_vti", "interop_lab")
SHA40 = re.compile(r"^[0-9a-f]{40}$")
LINEAGE = re.compile(r"^[a-z0-9][a-z0-9._-]{2,95}$")


def load_baseline(path: Path) -> dict:
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(doc, dict):
        raise ValueError("baseline manifest must be a mapping")
    if doc.get("schema") != SCHEMA:
        raise ValueError(f"baseline schema must be {SCHEMA}")
    lineage = doc.get("lineage")
    if not isinstance(lineage, str) or not LINEAGE.fullmatch(lineage):
        raise ValueError("baseline lineage must be a stable lowercase identifier")
    purpose = doc.get("purpose")
    if not isinstance(purpose, str) or not purpose.strip():
        raise ValueError("baseline purpose is required")
    pins = doc.get("pins")
    if not isinstance(pins, dict):
        raise ValueError("baseline pins are required")
    missing = [name for name in REQUIRED_PINS if name not in pins]
    if missing:
        raise ValueError("missing required baseline pins: " + ", ".join(missing))
    for name in REQUIRED_PINS:
        value = pins[name]
        if not isinstance(value, str) or not SHA40.fullmatch(value):
            raise ValueError(f"baseline pin {name} must be an immutable 40-character git SHA")
    return doc


def self_test() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "baseline.yaml"
        path.write_text(
            yaml.safe_dump(
                {
                    "schema": SCHEMA,
                    "lineage": "self-test-baseline",
                    "purpose": "self-test",
                    "pins": {name: str(index) * 40 for index, name in enumerate(REQUIRED_PINS, start=1)},
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )
        assert load_baseline(path)["lineage"] == "self-test-baseline"


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate and expose a DTG portfolio baseline epoch")
    parser.add_argument("manifest", nargs="?", type=Path)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--field", choices=("lineage", "json"), default="json")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    if args.manifest is None:
        parser.error("manifest is required unless --self-test is used")
    doc = load_baseline(args.manifest)
    if args.field == "lineage":
        print(doc["lineage"])
    else:
        print(json.dumps(doc, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
