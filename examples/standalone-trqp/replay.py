#!/usr/bin/env python3
"""Replay bounded schema/source checks; this does not assess a live TRQP service."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from jsonschema import FormatChecker, validators

HERE = Path(__file__).resolve().parent


def source_integrity(root: Path) -> dict:
    manifest = json.loads((root / "source-manifest.json").read_text())
    for entry in manifest["files"]:
        data = (root / entry["path"]).read_bytes()
        blob = b"blob " + str(len(data)).encode() + b"\0" + data
        if hashlib.sha1(blob).hexdigest() != entry["git_blob_sha"]:
            raise ValueError(f"Git blob mismatch: {entry['path']}")
        if hashlib.sha256(data).hexdigest() != entry["sha256"]:
            raise ValueError(f"SHA-256 mismatch: {entry['path']}")
    return manifest


def authorization_examples(path: Path) -> tuple[dict, dict]:
    # The first two HTTP blocks are the authorization query and response.
    blocks = re.findall(r"```http\n(.*?)```", path.read_text(), re.S)
    return tuple(json.loads(block[block.index("{"):].strip()) for block in blocks[:2])


def replay(root: Path = HERE) -> dict:
    manifest = source_integrity(root)
    schema = json.loads((root / "source/trqp_authorization_response.schema.json").read_text())
    validator_type = validators.validator_for(schema)
    validator_type.check_schema(schema)
    validator = validator_type(schema, format_checker=FormatChecker())
    cases = json.loads((root / "cases.json").read_text())
    outcomes = []
    for case in cases:
        errors = list(validator.iter_errors(case["response"]))
        actual = not errors
        if actual != case["schema_valid"]:
            raise ValueError(f"Unexpected schema result: {case['id']}")
        outcomes.append({"id": case["id"], "schema_valid": actual})
    api_query, api_response = authorization_examples(root / "source/api.md.txt")
    https_query, https_response = authorization_examples(root / "source/https_binding.md.txt")
    return {
        "target_commit": manifest["commit"],
        "scope": "retained source and constructed response fixtures only",
        "source_integrity": "verified",
        "cases": outcomes,
        "api_example": {
            "query_time": api_query["context"]["time"],
            "response_time_requested": api_response["time_requested"],
            "requested_time_matches": api_query["context"]["time"] == api_response["time_requested"],
            "schema_valid": validator.is_valid(api_response),
        },
        "https_example": {
            "requested_time_matches": https_query["context"]["time"] == https_response["time_requested"],
            "schema_valid": validator.is_valid(https_response),
        },
        "runtime_authorization": "not-assessed",
        "authority_history": "not-assessed",
        "overall_assurance": "review-required",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="compare with the retained expected replay")
    args = parser.parse_args()
    result = replay()
    if args.check:
        expected = json.loads((HERE / "expected-replay.json").read_text())
        if result != expected:
            raise ValueError("Replay differs from retained expected result")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
