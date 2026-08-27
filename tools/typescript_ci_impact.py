#!/usr/bin/env python3
"""Classify whether a RAHP change can affect Python↔TypeScript conformance.

This is an assurance-impact classifier, not a generic file-change optimiser. A
classification error fails safe: TypeScript conformance is required.
"""
from __future__ import annotations

import argparse
import fnmatch
import json
from pathlib import Path

# Paths are intentionally tied to what tools/validate_typescript_sdk.py consumes
# or to the implementation/build machinery that defines the cross-runtime contract.
AFFECTED_PATTERNS = (
    "packages/**",
    "package.json",
    "package-lock.json",
    "requirements.txt",
    "tools/validate_typescript_sdk.py",
    "tools/typescript_ci_impact.py",
    "tools/engine_contract.py",
    "tools/rahp.py",
    "method/engine-contract.yaml",
    "method/evidence-retention.yaml",
    "method/schema/rahp-result.schema.json",
    "method/schema/rahp-config.schema.json",
    "tests/conformance/**",
    "tests/fixtures/portable-project/rahp.yaml",
    "profiles/dtg/rahp.yaml",
    "profiles/cawg/rahp.yaml",
    "build/rahp.json",
    ".github/workflows/validate.yml",
    ".github/workflows/release.yml",
)


def normalize(path: str) -> str:
    value = path.strip()
    while value.startswith("./"):
        value = value[2:]
    return value.lstrip("/")


def matches(path: str) -> bool:
    path = normalize(path)
    return any(fnmatch.fnmatchcase(path, pattern) for pattern in AFFECTED_PATTERNS)


def classify(paths: list[str] | None, *, full: bool = False) -> dict[str, object]:
    if full:
        return {
            "required": True,
            "reason": "full-validation-backstop",
            "affected_paths": [],
        }
    if paths is None:
        return {
            "required": True,
            "reason": "fail-safe-classification-unavailable",
            "affected_paths": [],
        }
    cleaned = sorted({normalize(p) for p in paths if p.strip()})
    if not cleaned:
        return {
            "required": True,
            "reason": "fail-safe-empty-change-set",
            "affected_paths": [],
        }
    affected = [p for p in cleaned if matches(p)]
    if affected:
        return {
            "required": True,
            "reason": "affected-assurance-paths",
            "affected_paths": affected,
        }
    return {
        "required": False,
        "reason": "no-typescript-contract-assurance-paths-affected",
        "affected_paths": [],
    }


def self_test() -> int:
    required_cases = {
        "typescript-source": ["packages/core/src/index.ts"],
        "package-lock": ["package-lock.json"],
        "engine-contract": ["method/engine-contract.yaml"],
        "result-schema": ["method/schema/rahp-result.schema.json"],
        "python-adapter": ["tools/engine_contract.py"],
        "profile-used-by-conformance": ["profiles/dtg/rahp.yaml"],
        "conformance-fixture": ["tests/conformance/engine/valid-minimal/result.json"],
        "classifier": ["tools/typescript_ci_impact.py"],
        "workflow": [".github/workflows/validate.yml"],
        "workflow-dot-relative": ["./.github/workflows/validate.yml"],
    }
    for name, paths in required_cases.items():
        result = classify(paths)
        assert result["required"] is True, (name, result)
        assert result["reason"] == "affected-assurance-paths", (name, result)

    unrelated_cases = {
        "documentation": ["docs/dpip-handoff-operations.md"],
        "new-corpus": ["corpora/credential-zkp-trust-tasks-composed.yaml"],
        "pressure-test": ["examples/cross-spec/credential-zkp-trust-tasks/pressure-test.yaml"],
        "telemetry-tool": ["tools/dpip_lifecycle.py"],
    }
    for name, paths in unrelated_cases.items():
        result = classify(paths)
        assert result["required"] is False, (name, result)

    assert classify(None)["required"] is True
    assert classify([])["required"] is True
    assert classify(["docs/README.md"], full=True)["required"] is True
    assert classify(["docs/README.md"], full=True)["reason"] == "full-validation-backstop"
    print("PASS TypeScript CI impact classifier self-test")
    return 0


def write_github_output(path: Path, result: dict[str, object]) -> None:
    affected = ",".join(result.get("affected_paths") or [])
    with path.open("a", encoding="utf-8") as fh:
        fh.write(f"required={'true' if result['required'] else 'false'}\n")
        fh.write(f"reason={result['reason']}\n")
        fh.write(f"affected_paths={affected}\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paths-file", type=Path)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--github-output", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()

    paths: list[str] | None = None
    if args.paths_file:
        try:
            paths = args.paths_file.read_text(encoding="utf-8").splitlines()
        except OSError:
            paths = None

    result = classify(paths, full=args.full)
    print(json.dumps(result, indent=2))
    if args.github_output:
        write_github_output(args.github_output, result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
