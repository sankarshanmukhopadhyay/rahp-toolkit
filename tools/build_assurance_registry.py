#!/usr/bin/env python3
"""Build a derived, machine-consumable index over the portable RAHP catalogue.

The canonical assurance semantics remain in method/catalogue/. This module does
not mint new assurance identifiers or create an independent authority surface.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOGUE_DIR = ROOT / "method" / "catalogue"
DEFAULT_OUTPUT = ROOT / "build" / "assurance-registry.json"

CATALOGUE_FILES = {
    "harm_pattern": "harm-patterns.yaml",
    "risk_pattern": "risk-patterns.yaml",
    "control_pattern": "control-patterns.yaml",
    "guardrail_pattern": "guardrail-patterns.yaml",
    "assurance_pattern": "assurance-patterns.yaml",
    "evidence_pattern": "evidence-patterns.yaml",
}

RELATIONSHIP_FIELDS = {
    "harm_patterns",
    "risk_patterns",
    "control_patterns",
    "guardrail_patterns",
    "evidence_patterns",
    "related_patterns",
}

SUMMARY_FIELDS = (
    "definition",
    "description",
    "control_objective",
    "prohibited_state",
    "assertion",
    "claim_supported",
)


class RegistryError(ValueError):
    """Raised when canonical catalogue state cannot form a coherent registry."""


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = yaml.safe_load(handle) or {}
    if not isinstance(value, dict):
        raise RegistryError(f"{path}: expected a YAML mapping")
    return value


def _summary(record: dict[str, Any]) -> str:
    for field in SUMMARY_FIELDS:
        value = record.get(field)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def build_registry(catalogue_dir: Path = DEFAULT_CATALOGUE_DIR) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    ids: dict[str, str] = {}
    versions: set[str] = set()

    for object_type, filename in CATALOGUE_FILES.items():
        path = catalogue_dir / filename
        document = _load_yaml(path)

        declared_type = document.get("record_type")
        if declared_type != object_type:
            raise RegistryError(
                f"{path}: record_type {declared_type!r} does not match {object_type!r}"
            )

        version = str(document.get("catalogue_version") or "").strip()
        if not version:
            raise RegistryError(f"{path}: catalogue_version is required")
        versions.add(version)

        records = document.get("records") or []
        if not isinstance(records, list):
            raise RegistryError(f"{path}: records must be a list")

        for record in records:
            if not isinstance(record, dict):
                raise RegistryError(f"{path}: each record must be a mapping")
            record_id = str(record.get("id") or "").strip()
            if not record_id:
                raise RegistryError(f"{path}: record id is required")
            if record_id in ids:
                raise RegistryError(
                    f"duplicate catalogue id {record_id}: {ids[record_id]} and {filename}"
                )
            ids[record_id] = filename

            relationships: dict[str, list[str]] = {}
            for field in sorted(RELATIONSHIP_FIELDS):
                refs = record.get(field)
                if refs:
                    if not isinstance(refs, list) or not all(isinstance(v, str) for v in refs):
                        raise RegistryError(
                            f"{path}:{record_id}: {field} must be a list of string identifiers"
                        )
                    relationships[field] = list(refs)

            entries.append(
                {
                    "id": record_id,
                    "type": object_type,
                    "name": record.get("name", ""),
                    "summary": _summary(record),
                    "source": f"method/catalogue/{filename}",
                    "relationships": relationships,
                }
            )

    if len(versions) != 1:
        raise RegistryError(
            "catalogue files do not share one catalogue_version: "
            + ", ".join(sorted(versions))
        )

    known_ids = set(ids)
    for entry in entries:
        for field, refs in entry["relationships"].items():
            for ref in refs:
                if ref not in known_ids:
                    raise RegistryError(
                        f"{entry['id']}: {field} references unknown portable id {ref}"
                    )

    entries.sort(key=lambda item: item["id"])
    catalogue_version = next(iter(versions))

    return {
        "schema": "rahp-assurance-registry-index/v1",
        "catalogue_version": catalogue_version,
        "authority": {
            "canonical_source": "method/catalogue/",
            "derived": True,
            "statement": (
                "This index is a derived discovery surface. The canonical catalogue "
                "files remain authoritative for portable assurance semantics."
            ),
        },
        "counts": {
            object_type: sum(1 for entry in entries if entry["type"] == object_type)
            for object_type in CATALOGUE_FILES
        },
        "entries": entries,
    }


def render(registry: dict[str, Any]) -> str:
    return json.dumps(registry, indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalogue-dir", type=Path, default=DEFAULT_CATALOGUE_DIR)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--stdout", action="store_true")
    args = parser.parse_args()

    rendered = render(build_registry(args.catalogue_dir))

    if args.stdout:
        print(rendered, end="")

    if args.check:
        if not args.output.exists():
            raise RegistryError(f"{args.output}: generated registry is missing")
        current = args.output.read_text(encoding="utf-8")
        if current != rendered:
            raise RegistryError(
                f"{args.output}: generated registry is stale; rebuild it"
            )
        return 0

    if not args.stdout:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
