#!/usr/bin/env python3
"""Validate current release surfaces from the generic release declaration."""
from __future__ import annotations

import sys

from release import declaration, metadata, verify


def main() -> int:
    try:
        doc = declaration()
    except Exception as exc:
        print(f"ERROR: {exc}")
        return 1
    errors = verify(doc)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    meta = metadata(doc)
    print(f"PASS release metadata: {meta['tag']} via method/release.yaml")
    return 0


if __name__ == "__main__":
    sys.exit(main())
