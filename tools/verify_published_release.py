#!/usr/bin/env python3
"""Fail closed on stale release notes and incomplete GitHub publication."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


STALE = re.compile(
    r"(?im)^\s*(?:\*\*)?(?:status|release date)(?:\*\*)?:?\s*(?:\*\*)?\s*"
    r"(?:UNPUBLISHED|NOT QUALIFIED|PENDING|Pending qualification)"
)


def preflight(notes: str) -> list[str]:
    if not notes.strip():
        return ["release notes must not be empty"]
    if STALE.search(notes):
        return ["release notes contain unpublished, unqualified or pending candidate metadata"]
    if "(candidate)" in notes.splitlines()[0].lower():
        return ["release notes still have a candidate title"]
    return []


def postflight(payload: dict, notes: str, tag: str, title: str, latest: str) -> list[str]:
    errors = preflight(notes)
    if payload.get("tagName") != tag:
        errors.append("published tag does not match release declaration")
    if payload.get("name") != title:
        errors.append("published title does not match release declaration")
    if payload.get("isDraft") is not False or payload.get("isPrerelease") is not False:
        errors.append("release must be published, non-draft and non-prerelease")
    if payload.get("body", "").strip().replace("\r\n", "\n") != notes.strip().replace("\r\n", "\n"):
        errors.append("published release notes differ from canonical notes")
    if latest != tag:
        errors.append("latest release tag differs from published release")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="mode", required=True)
    pre = subs.add_parser("preflight")
    pre.add_argument("notes")
    post = subs.add_parser("postflight")
    for field in ("published_json", "notes", "tag", "title", "latest"):
        post.add_argument(field)
    args = parser.parse_args()
    notes = Path(args.notes).read_text(encoding="utf-8")
    if args.mode == "preflight":
        errors = preflight(notes)
    else:
        errors = postflight(
            json.loads(Path(args.published_json).read_text(encoding="utf-8")),
            notes,
            args.tag,
            args.title,
            args.latest,
        )
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        return 1
    print(f"PASS release {args.mode}: canonical notes and publication state verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
