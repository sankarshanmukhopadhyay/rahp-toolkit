#!/usr/bin/env python3
"""Validate worked RAHP specification pressure-test records.

Checks every examples/**/pressure-test.yaml against the catalogues available to
the repository: the bundled exemplar catalogue plus any deployment-local catalogues
under instances/*/data/. This is a v0.6 portability invariant: an external
deployment can own risk identifiers without importing them into DTG data.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import subprocess
import sys
from dataclasses import dataclass
from portable_catalogue import validate_block

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("validate_pressure_tests.py requires PyYAML: pip install -r requirements.txt")

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
VOCAB = ROOT / "method" / "vocabularies.yaml"


def load_yaml(path: pathlib.Path):
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def catalogue_paths(filename: str) -> list[pathlib.Path]:
    """Return bundled and deployment-local catalogue files in deterministic order."""
    return [DATA / filename, *sorted((ROOT / "instances").glob(f"*/data/{filename}"))]


def ids(filename: str) -> set[str]:
    values: set[str] = set()
    paths = catalogue_paths(filename)
    for path in paths:
        if not path.exists():
            continue
        doc = load_yaml(path)
        values.update(str(r.get("id")) for r in doc.get("records", []) if r.get("id"))
    return values


def dispositions() -> set[str]:
    doc = load_yaml(VOCAB)
    return set(doc.get("finding_disposition", {}).get("values", []))


@dataclass(frozen=True)
class ValidationContext:
    known_patterns: frozenset[str]
    corpus_scenarios: frozenset[str]
    known: dict[str, frozenset[str]]
    allowed_dispositions: frozenset[str]
    allowed_status: frozenset[str]
    allowed_severity: frozenset[str]


def build_context() -> ValidationContext:
    pattern_doc = load_yaml(ROOT / "method" / "scenario-patterns.yaml")
    known_patterns = frozenset(
        str(p.get("id")) for p in pattern_doc.get("patterns", []) if p.get("id")
    )

    corpus_scenarios: set[str] = set()
    for corpus_path in sorted((ROOT / "corpora").glob("*.yaml")):
        cdoc = load_yaml(corpus_path).get("corpus") or {}
        corpus_scenarios.update(
            str(s.get("id")) for s in cdoc.get("scenarios", []) if s.get("id")
        )

    known = {
        "risks": frozenset(ids("risks.yaml")),
        "controls": frozenset(ids("controls.yaml")),
        "guardrails": frozenset(ids("guardrails.yaml")),
        "assurance_tests": frozenset(ids("assurance-tests.yaml")),
        "personas": frozenset(ids("personas.yaml")),
    }
    return ValidationContext(
        known_patterns=known_patterns,
        corpus_scenarios=frozenset(corpus_scenarios),
        known=known,
        allowed_dispositions=frozenset(dispositions()),
        allowed_status=frozenset(
            {"in-progress", "complete", "open", "monitoring", "resolved", "superseded"}
        ),
        allowed_severity=frozenset({"Low", "Medium", "High", "Critical"}),
    )


def resolve_files(values: list[pathlib.Path] | None) -> list[pathlib.Path]:
    if not values:
        return sorted(ROOT.glob("examples/**/pressure-test.yaml"))
    return [value if value.is_absolute() else ROOT / value for value in values]


def validate_files(
    files: list[pathlib.Path],
    *,
    context: ValidationContext | None = None,
    render_repository: bool = False,
) -> tuple[list[str], int]:
    if not files:
        return ["no examples/**/pressure-test.yaml files found"], 0

    context = context or build_context()
    errors: list[str] = []
    findings_seen = 0

    for path in files:
        rel = path.relative_to(ROOT)
        doc = load_yaml(path)
        review = doc.get("review")
        if not isinstance(review, dict):
            errors.append(f"{rel}: missing review mapping")
            continue

        for field in ("id", "status", "title", "reviewed_on", "target", "reviewed_against"):
            if not review.get(field):
                errors.append(f"{rel}: review.{field} is required")

        if review.get("status") not in context.allowed_status:
            errors.append(f"{rel}: review.status={review.get('status')!r} is not permitted")

        target = review.get("target") or {}
        for field in ("repository", "version"):
            if not target.get(field):
                errors.append(f"{rel}: review.target.{field} is required")
        commit = str(target.get("commit") or "")
        evidence_pin = str(target.get("evidence_pin") or "")
        if not commit and not evidence_pin:
            errors.append(f"{rel}: review.target requires commit or evidence_pin")
        if commit and not re.fullmatch(r"[0-9a-fA-F]{40}", commit):
            errors.append(f"{rel}: review.target.commit must be a full 40-character commit SHA")
        grade = str(review.get("evidence_grade") or "source-pinned")
        if grade == "source-pinned" and not commit:
            errors.append(f"{rel}: source-pinned assessment requires review.target.commit")

        against = review.get("reviewed_against") or {}
        if not against.get("rahp_version"):
            errors.append(f"{rel}: review.reviewed_against.rahp_version is required")

        if "findings" not in review:
            errors.append(f"{rel}: review.findings is required")
            findings = []
        else:
            findings = review.get("findings")
        if not isinstance(findings, list):
            errors.append(f"{rel}: review.findings must be a list")
            continue
        if not findings and review.get("status") != "in-progress":
            errors.append(f"{rel}: completed/non-draft review.findings must be non-empty")
            continue

        local_ids: set[str] = set()
        for finding in findings:
            findings_seen += 1
            fid = str(finding.get("id") or "")
            prefix = f"{rel}:{fid or '<no-id>'}"
            if not re.fullmatch(r"F-[0-9]{3}", fid):
                errors.append(f"{prefix}: id must match F-000")
            if fid in local_ids:
                errors.append(f"{prefix}: duplicate finding id")
            local_ids.add(fid)

            for field in (
                "title",
                "status",
                "severity",
                "primary_disposition",
                "risks",
                "evidence",
                "harm",
                "recommendation",
                "retest_when",
            ):
                if not finding.get(field):
                    errors.append(f"{prefix}: {field} is required")

            if finding.get("status") not in context.allowed_status:
                errors.append(f"{prefix}: status={finding.get('status')!r} is not permitted")
            if finding.get("severity") not in context.allowed_severity:
                errors.append(f"{prefix}: severity={finding.get('severity')!r} is not permitted")

            primary = finding.get("primary_disposition")
            if primary not in context.allowed_dispositions:
                errors.append(
                    f"{prefix}: primary_disposition={primary!r} is not in method/vocabularies.yaml"
                )
            for d in finding.get("secondary_dispositions") or []:
                if d not in context.allowed_dispositions:
                    errors.append(f"{prefix}: secondary disposition {d!r} is not permitted")

            for field, valid in context.known.items():
                refs = finding.get(field) or []
                if not isinstance(refs, list):
                    errors.append(f"{prefix}: {field} must be a list")
                    continue
                for ref in refs:
                    if ref not in valid:
                        errors.append(f"{prefix}: {field} reference {ref!r} does not resolve")

            for ref in finding.get("scenario_patterns") or []:
                if ref not in context.known_patterns:
                    errors.append(
                        f"{prefix}: scenario_patterns reference {ref!r} does not resolve"
                    )
            for ref in finding.get("scenarios") or []:
                if ref not in context.corpus_scenarios:
                    errors.append(
                        f"{prefix}: scenarios reference {ref!r} does not resolve in corpora/"
                    )

            validate_block(finding.get("portable_assurance"), prefix, errors, required=True)

            evidence = finding.get("evidence") or []
            if not isinstance(evidence, list):
                errors.append(f"{prefix}: evidence must be a list")
            else:
                for n, ev in enumerate(evidence, 1):
                    if not isinstance(ev, dict) or not ev.get("source") or not ev.get("observation"):
                        errors.append(
                            f"{prefix}: evidence[{n}] requires source and observation"
                        )

        summary = review.get("summary") or {}
        if "finding_count" in summary and summary.get("finding_count") != len(findings):
            errors.append(
                f"{rel}: summary.finding_count={summary.get('finding_count')} "
                f"but {len(findings)} findings are recorded"
            )
        if "open_count" in summary:
            actual_open = sum(1 for f in findings if f.get("status") == "open")
            if summary.get("open_count") != actual_open:
                errors.append(
                    f"{rel}: summary.open_count={summary.get('open_count')} "
                    f"but {actual_open} findings are open"
                )

    if not errors and render_repository:
        renderer = ROOT / "tools" / "render_pressure_tests.py"
        rendered = subprocess.run(
            [sys.executable, str(renderer), "--check"],
            cwd=ROOT,
            text=True,
        )
        if rendered.returncode != 0:
            errors.append("generated Markdown is missing or stale")

    return errors, findings_seen


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--file",
        type=pathlib.Path,
        action="append",
        help=(
            "Validate one pressure-test YAML. Repeat --file to validate multiple "
            "files while loading shared catalogues only once."
        ),
    )
    args = ap.parse_args()
    files = resolve_files(args.file)

    errors, findings_seen = validate_files(
        files,
        render_repository=not bool(args.file),
    )

    if errors:
        for error in errors:
            print(f"ERROR {error}")
        print(
            f"\nPressure-test validation failed: {len(errors)} error(s) "
            f"across {len(files)} review file(s)."
        )
        return 1

    risk_catalogues = [
        str(p.relative_to(ROOT))
        for p in catalogue_paths("risks.yaml")
        if p.exists()
    ]
    print(
        f"Pressure-test validation clean: {len(files)} review file(s), "
        f"{findings_seen} finding(s), all references resolved, Markdown current."
    )
    print(f"  risk catalogues: {', '.join(risk_catalogues)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
