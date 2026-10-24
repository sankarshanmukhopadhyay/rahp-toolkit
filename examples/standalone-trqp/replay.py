#!/usr/bin/env python3
"""Replay bounded schema/source checks; this does not assess a live TRQP service."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path, PurePosixPath

from jsonschema import FormatChecker, validators

HERE = Path(__file__).resolve().parent


def _retained_path(root: Path, name: str) -> Path:
    """Resolve a retained source only inside root; reject traversal and symlinks."""
    if not isinstance(name, str) or not name or "\\" in name:
        raise ValueError("Unsafe retained path")
    relative = PurePosixPath(name)
    if relative.is_absolute() or any(part in ("", ".", "..") for part in name.split("/")):
        raise ValueError(f"Unsafe retained path: {name}")
    base = root.resolve(strict=True)
    path = base
    for part in relative.parts:
        path = path / part
        if path.is_symlink():
            raise ValueError(f"Symlink retained path: {name}")
    if not path.is_file() or not path.resolve().is_relative_to(base):
        raise ValueError(f"Missing or unsafe retained file: {name}")
    return path


def source_integrity(root: Path) -> dict:
    """Fail closed on source identity, manifest uniqueness, and content digests."""
    manifest = json.loads(_retained_path(root, "source-manifest.json").read_text())
    if (not isinstance(manifest, dict)
            or not isinstance(manifest.get("repository"), str)
            or not manifest["repository"]
            or not isinstance(manifest.get("commit"), str)
            or not re.fullmatch(r"[0-9a-f]{40}", manifest["commit"])
            or not isinstance(manifest.get("files"), list)
            or not manifest["files"]):
        raise ValueError("Manifest requires repository, immutable commit and nonempty files")
    seen_paths, seen_upstream = set(), set()
    for entry in manifest["files"]:
        if not isinstance(entry, dict):
            raise ValueError("Malformed source entry")
        name, upstream = entry.get("path"), entry.get("upstream_path")
        if (not isinstance(upstream, str) or not upstream or "\\" in upstream
                or upstream.startswith("/")
                or any(part in ("", ".", "..") for part in upstream.split("/"))):
            raise ValueError("Unsafe upstream path")
        path = _retained_path(root, name)
        if name in seen_paths or upstream in seen_upstream:
            raise ValueError(f"Duplicate source entry: {name}")
        seen_paths.add(name)
        seen_upstream.add(upstream)
        expected_url = (f"https://github.com/{manifest['repository']}/blob/"
                        f"{manifest['commit']}/{upstream}")
        if entry.get("url") != expected_url:
            raise ValueError(f"Source URL disagrees with identity: {name}")
        for field, digits in (("sha256", 64), ("git_blob_sha", 40)):
            if not isinstance(entry.get(field), str) or not re.fullmatch(
                    rf"[0-9a-f]{{{digits}}}", entry[field]):
                raise ValueError(f"Malformed {field}: {name}")
        data = path.read_bytes()
        blob = b"blob " + str(len(data)).encode() + b"\\0" + data
        if hashlib.sha1(blob).hexdigest() != entry["git_blob_sha"]:
            raise ValueError(f"Git blob mismatch: {name}")
        if hashlib.sha256(data).hexdigest() != entry["sha256"]:
            raise ValueError(f"SHA-256 mismatch: {name}")
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
