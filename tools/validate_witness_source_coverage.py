"""Witness test coverage is evidence of source assertions, never runtime assurance.

Validate the immutable PR-head source directly when --fetch-source is supplied.
A network failure or source difference must fail, not silently downgrade to PASS.
"""
from __future__ import annotations

import argparse
import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/assurance/witness-source-coverage-1051.json"
TEST_RE = re.compile(r"#\[(?:tokio::test|test)(?:\([^]]*\))?\]\s*(?:async\s+)?fn\s+([a-zA-Z_][a-zA-Z_0-9]*)")
MODULE_RE = re.compile(r'#\[path\s*=\s*"witness_tests\.rs"\]\s*mod\s+tests\s*;')


def verify(data: dict, test_source: str | None = None, module_source: str | None = None) -> list[str]:
    errors = []
    if data.get("schema") != "rahp-vta-witness-source-coverage/v1":
        errors.append("unsupported source coverage manifest")
    if not re.fullmatch(r"[0-9a-f]{40}", str(data.get("revision", ""))):
        errors.append("source revision must be full Git SHA")
    tests = data.get("tests")
    if not isinstance(tests, list) or len(tests) != 10:
        return errors + ["expected exactly ten source-declared witness tests"]
    names = [t.get("name") for t in tests]
    if len(names) != len(set(names)) or any(not isinstance(x, str) or not x for x in names):
        errors.append("missing or duplicate source test names")
    if any(t.get("evidence_status") != "source-assertions-only" for t in tests):
        errors.append("source inventory may not claim executed runtime PASS")
    ci = data.get("ci", {})
    if ci.get("attribution") != "aggregate-success-only" or ci.get("passed") != 6063 or ci.get("skipped") != 23:
        errors.append("workspace CI result must retain aggregate attribution and skips")
    if test_source is not None:
        found = TEST_RE.findall(test_source)
        if len(found) != 10 or set(found) != set(names):
            errors.append(f"source test declaration mismatch: found {found!r}")
    if module_source is not None and not MODULE_RE.search(module_source):
        errors.append("test module not proven wired into witness.rs")
    return errors


def fetch_pinned(data: dict, path: str) -> str:
    revision = data["revision"]
    base = f'https://raw.githubusercontent.com/{data["upstream_repository"]}/{revision}/'
    request = urllib.request.Request(base + path, headers={"User-Agent": "rahp-witness-coverage/1"})
    with urllib.request.urlopen(request, timeout=25) as response:
        if response.status != 200:
            raise ValueError(f"unexpected HTTP {response.status}")
        return response.read(1_000_001).decode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fetch-source", action="store_true", help="obtain actual pinned VTI source; offline manifest check otherwise")
    parser.add_argument("--test-source", type=Path, help="path to an independently retrieved exact revision witness_tests.rs")
    parser.add_argument("--module-source", type=Path, help="path to same-revision witness.rs")
    args = parser.parse_args()
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if bool(args.test_source) != bool(args.module_source):
        parser.error("both local source paths are required together")
    try:
        tests = fetch_pinned(data, data["test_source"]) if args.fetch_source else (args.test_source.read_text() if args.test_source else None)
        module = fetch_pinned(data, data["module_source"]) if args.fetch_source else (args.module_source.read_text() if args.module_source else None)
    except (OSError, UnicodeError, ValueError) as e:
        print(f"INDETERMINATE: source retrieval failed: {e}")
        return 1
    errors = verify(data, tests, module)
    for error in errors:
        print("ERROR:", error)
    if errors:
        return 1
    print("PASS source declaration inventory; test execution and runtime assurance remain UNVERIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
