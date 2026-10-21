#!/usr/bin/env python3
"""Compare two *locally supplied* specification snapshots without network access.

Produces a reproducible, reviewable changed-clause inventory. This is a
change-discovery aid, not a normative classification or conformance verdict.
"""
from __future__ import annotations
import argparse
import difflib
import hashlib
import json
from pathlib import Path
import re

KEYWORDS = re.compile(r"\b(?:MUST(?: NOT)?|SHALL(?: NOT)?|SHOULD(?: NOT)?|REQUIRED|RECOMMENDED|MAY|OPTIONAL)\b")
HEADINGS = re.compile(r"^#{1,6}\s+(.+)$")
def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def inventory(before: str, after: str) -> dict:
    old, new = before.splitlines(), after.splitlines()
    matcher = difflib.SequenceMatcher(None, old, new, autojunk=False)
    changes = []
    old_section, new_section = "Preamble", "Preamble"
    old_heads = []
    new_heads = []
    for lines, target in ((old, old_heads), (new, new_heads)):
        section = "Preamble"
        for line in lines:
            m = HEADINGS.match(line)
            if m:
                section = m.group(1)
            target.append(section)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            continue
        removed = old[i1:i2]
        added = new[j1:j2]
        changes.append({
            "kind": tag,
            "old_lines": [i1 + 1, i2],
            "new_lines": [j1 + 1, j2],
            "old_section": old_heads[i1] if i1 < len(old_heads) else (old_heads[-1] if old_heads else "Preamble"),
            "new_section": new_heads[j1] if j1 < len(new_heads) else (new_heads[-1] if new_heads else "Preamble"),
            "old_normative_keywords": KEYWORDS.findall("\n".join(removed)),
            "new_normative_keywords": KEYWORDS.findall("\n".join(added)),
            "removed": removed,
            "added": added,
            "needs_human_normative_review": True,
        })
    return {
        "evidence_class": "source-diff",
        "assurance_disposition": "INDETERMINATE",
        "old_sha256": digest(before.encode("utf-8")),
        "new_sha256": digest(after.encode("utf-8")),
        "changed_hunks": len(changes),
        "hunks": changes,
    }

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--before", type=Path, required=True)
    p.add_argument("--after", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    result = inventory(args.before.read_text(encoding="utf-8"),
                       args.after.read_text(encoding="utf-8"))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Changed hunks: {result['changed_hunks']}; review required; assurance INDETERMINATE")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
