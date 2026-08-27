#!/usr/bin/env python3
"""Classify which DTG cross-specification compositions a change can affect.

The classifier derives composition dependencies from the canonical DTG cross-spec
registry and corpus IDs. Ambiguity fails safe to full DTG validation.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "profiles" / "dtg" / "cross-spec-tests.yaml"
CORPORA = ROOT / "corpora"

FULL_PATHS = {
    "profiles/dtg/cross-spec-tests.yaml",
    "corpora/sources.yaml",
    "tools/dtg_cross_spec_ci_impact.py",
    "tools/validate_dtg_cross_spec_ci.py",
    "tools/validate_cross_spec_registry.py",
    "tools/cross_spec_selection.py",
    "tools/cross_spec_review.py",
    "tools/publish_assessment_issues.py",
    "tools/validate_scenario_corpora.py",
    "tools/validate_pressure_tests.py",
    "method/ci-assurance-propositions.yaml",
    ".github/workflows/validate.yml",
    ".github/workflows/cross-spec-pressure-test.yml",
    ".github/workflows/dtg-cross-spec-pressure-test.yml",
}


def norm(path: str) -> str:
    value = path.strip()
    while value.startswith("./"):
        value = value[2:]
    return value.lstrip("/")


def registry() -> dict:
    return yaml.safe_load(REGISTRY.read_text(encoding="utf-8")) or {}


def runnable_ids(data: dict) -> list[str]:
    return sorted(
        str(item["id"])
        for item in data.get("compositions", [])
        if item.get("runnable") and item.get("status") == "maintained"
    )


def corpus_path_map() -> dict[str, str]:
    result: dict[str, str] = {}
    for path in CORPORA.glob("*.yaml"):
        if path.name == "sources.yaml":
            continue
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except Exception:
            continue
        corpus = data.get("corpus") or {}
        cid = corpus.get("id")
        if cid:
            result[str(cid)] = str(path.relative_to(ROOT))
    return result


def dependencies(data: dict) -> dict[str, set[str]]:
    corpus_paths = corpus_path_map()
    deps: dict[str, set[str]] = {}
    for item in data.get("compositions", []):
        if not item.get("runnable") or item.get("status") != "maintained":
            continue
        cid = str(item["id"])
        paths = {norm(str(item["assessment"]))}
        referenced = [item.get("corpus_id")]
        referenced.extend(c.get("corpus_id") for c in item.get("components", []))
        for corpus_id in referenced:
            if corpus_id and str(corpus_id) in corpus_paths:
                paths.add(corpus_paths[str(corpus_id)])
        deps[cid] = paths
    return deps


def classify(paths: list[str] | None, *, full: bool = False) -> dict[str, object]:
    data = registry()
    all_ids = runnable_ids(data)
    if full:
        return {"required": True, "mode": "all", "reason": "full-validation-backstop", "compositions": all_ids}
    if paths is None:
        return {"required": True, "mode": "all", "reason": "fail-safe-classification-unavailable", "compositions": all_ids}
    cleaned = sorted({norm(p) for p in paths if p.strip()})
    if not cleaned:
        return {"required": True, "mode": "all", "reason": "fail-safe-empty-change-set", "compositions": all_ids}
    if any(p in FULL_PATHS for p in cleaned):
        return {"required": True, "mode": "all", "reason": "shared-dtg-cross-spec-assurance-path", "compositions": all_ids}

    deps = dependencies(data)
    affected = sorted(cid for cid, dep_paths in deps.items() if any(p in dep_paths for p in cleaned))
    known_dtg_paths = set().union(*deps.values()) if deps else set()
    suspicious = [
        p for p in cleaned
        if (p.startswith("examples/cross-spec/") or p.startswith("corpora/"))
        and p not in known_dtg_paths
        and p != "corpora/index.md"
    ]
    if suspicious:
        # A cross-spec/corpus change we cannot map safely must expand rather than narrow.
        return {"required": True, "mode": "all", "reason": "fail-safe-unmapped-cross-spec-path", "compositions": all_ids}
    if affected:
        return {"required": True, "mode": "selected", "reason": "affected-dtg-compositions", "compositions": affected}
    return {"required": False, "mode": "skip", "reason": "no-dtg-cross-spec-assurance-paths-affected", "compositions": []}


def write_output(path: Path, result: dict[str, object]) -> None:
    with path.open("a", encoding="utf-8") as fh:
        fh.write(f"required={'true' if result['required'] else 'false'}\n")
        fh.write(f"mode={result['mode']}\n")
        fh.write(f"reason={result['reason']}\n")
        fh.write("compositions=" + ",".join(result.get("compositions") or []) + "\n")


def self_test() -> int:
    data = registry()
    deps = dependencies(data)
    assert "trust-tasks--zkp" in deps
    assessment = next(x["assessment"] for x in data["compositions"] if x["id"] == "trust-tasks--zkp")
    r = classify([assessment])
    assert r["mode"] == "selected" and r["compositions"] == ["trust-tasks--zkp"], r

    # Shared Trust Tasks corpus must affect every composition that declares it.
    trust_tasks_path = corpus_path_map().get("CORPUS-TRUST-TASKS")
    assert trust_tasks_path, "Trust Tasks corpus path must resolve"
    r = classify([trust_tasks_path])
    expected = sorted(cid for cid, paths in deps.items() if trust_tasks_path in paths)
    assert r["mode"] == "selected" and r["compositions"] == expected and len(expected) >= 2, r

    assert classify(["profiles/dtg/cross-spec-tests.yaml"])["mode"] == "all"
    assert classify(["tools/cross_spec_review.py"])["mode"] == "all"
    assert classify(["docs/dpip-handoff-operations.md"])["mode"] == "skip"
    assert classify(["profiles/cawg/cross-spec-tests.yaml"])["mode"] == "skip"
    assert classify(["corpora/unknown-new-dtg-corpus.yaml"])["mode"] == "all"
    assert classify(None)["mode"] == "all"
    assert classify([], full=True)["mode"] == "all"
    print("PASS DTG cross-spec CI impact classifier self-test")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--paths-file", type=Path)
    ap.add_argument("--full", action="store_true")
    ap.add_argument("--github-output", type=Path)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    paths = None
    if args.paths_file:
        try:
            paths = args.paths_file.read_text(encoding="utf-8").splitlines()
        except OSError:
            paths = None
    result = classify(paths, full=args.full)
    print(json.dumps(result, indent=2))
    if args.github_output:
        write_output(args.github_output, result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
