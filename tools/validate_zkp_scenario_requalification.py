#!/usr/bin/env python3
"""Validate the bounded DTG ZKP legacy-scenario semantic requalification (#1147)."""
from __future__ import annotations

from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parent.parent
CORPUS_PATH = ROOT / "corpora" / "dtg-zkp.yaml"
REVIEW_PATH = ROOT / "corpora" / "reviews" / "dtg-zkp-semantic-requalification-2026-10-25.yaml"
ALLOWED = {"retain", "revise", "scenario-baseline"}
AUTHORITY_REPOSITORY = "trustoverip/dtgwg-zkp-spec"


def load(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def validate(corpus_doc: dict, review: dict) -> list[str]:
    errors: list[str] = []
    corpus = corpus_doc.get("corpus") or {}
    scenarios = corpus.get("scenarios") or []
    scenario_ids = [s.get("id") for s in scenarios if isinstance(s, dict)]
    entries = review.get("dispositions") or []
    entry_ids = [e.get("scenario_id") for e in entries if isinstance(e, dict)]

    if corpus.get("id") != review.get("corpus_id"):
        errors.append("review corpus_id does not match canonical corpus")
    authority = review.get("authority") or {}
    if authority.get("repository") != AUTHORITY_REPOSITORY:
        errors.append("review authority repository is not canonical DTG ZKP specification")
    if authority.get("commit") != corpus.get("source_commit"):
        errors.append("review authority commit does not match corpus source_commit")
    if corpus.get("source_repository") != AUTHORITY_REPOSITORY:
        errors.append("canonical corpus source repository is not DTG ZKP specification")
    if len(scenario_ids) != 30 or set(scenario_ids) != {f"UC-{i:03d}" for i in range(1, 31)}:
        errors.append("canonical corpus must contain exactly UC-001 through UC-030")
    if len(entry_ids) != 30:
        errors.append("requalification must contain exactly 30 dispositions")
    if len(set(entry_ids)) != len(entry_ids):
        errors.append("requalification contains duplicate scenario dispositions")
    missing = set(scenario_ids) - set(entry_ids)
    extra = set(entry_ids) - set(scenario_ids)
    if missing:
        errors.append(f"requalification missing scenarios: {sorted(missing)}")
    if extra:
        errors.append(f"requalification references unknown scenarios: {sorted(extra)}")

    counts = {key: 0 for key in ALLOWED}
    for entry in entries:
        if not isinstance(entry, dict):
            errors.append("requalification disposition must be a mapping")
            continue
        sid = entry.get("scenario_id")
        disposition = entry.get("disposition")
        if disposition not in ALLOWED:
            errors.append(f"{sid}: invalid disposition {disposition!r}")
            continue
        counts[disposition] += 1
        if not entry.get("canonical_action"):
            errors.append(f"{sid}: canonical_action is required")
        if not entry.get("establishes"):
            errors.append(f"{sid}: establishes/limitation statement is required")
        evidence = entry.get("source_evidence") or []
        if disposition in {"retain", "revise"} and not evidence:
            errors.append(f"{sid}: source-grounded disposition requires source_evidence")
        for path in evidence:
            if not isinstance(path, str) or not (
                path.startswith("spec/") or path.startswith("conformance/")
            ):
                errors.append(f"{sid}: invalid authority evidence path {path!r}")

    expected_counts = ((review.get("summary") or {}).get("total"), 30)
    if expected_counts[0] != expected_counts[1]:
        errors.append("summary.total must be 30")
    summary = review.get("summary") or {}
    for key, count in counts.items():
        if summary.get(key) != count:
            errors.append(f"summary.{key}={summary.get(key)!r} does not match {count}")

    requal = corpus.get("semantic_requalification") or {}
    if requal.get("review_id") != review.get("review_id"):
        errors.append("corpus semantic_requalification.review_id does not match review")
    if requal.get("reviewed_commit") != authority.get("commit"):
        errors.append("corpus reviewed_commit does not match authority commit")
    if corpus.get("provenance_status") != "semantic-requalification-complete-mixed-grounding":
        errors.append("corpus provenance_status does not declare completed mixed-grounding requalification")
    if corpus.get("evidence_grade"):
        errors.append("mixed-grounding ZKP corpus must not declare a corpus-wide evidence_grade")

    return errors


def main() -> int:
    errors = validate(load(CORPUS_PATH), load(REVIEW_PATH))
    if errors:
        for error in errors:
            print("ERROR", error)
        print(f"ZKP semantic requalification validation failed: {len(errors)} error(s).")
        return 1
    print("ZKP semantic requalification clean: 30 scenarios, immutable authority pin, mixed grounding explicitly preserved.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
