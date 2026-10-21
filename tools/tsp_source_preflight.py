#!/usr/bin/env python3
"""Reproducible source-evidence preflight for TSP issue #1103.

This is NOT a protocol conformance test or a terminal RAHP/DRARM assessment.
It checks immutable source retrieval and presence of precisely identified
source provisions. A textual match is evidence of text, not of behavior.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import pathlib
import re
import urllib.request

COMMIT = "ccda6b33159d860f05c328eb436dabe83548b705"
URL = f"https://raw.githubusercontent.com/trustoverip/tswg-tsp-specification/{COMMIT}/spec/spec.md"
CHECKS = {
    "vid_definition": r"\[\[def:\s*Verifiable Identifier",
    "relationship_definition": r"\[\[def:\s*TSP Relationship",
    "oobi_definition": r"\[\[def:\s*Out of Band Introduction",
    "direct_and_routed_modes": r"Direct Mode.*?Routed Mode",
    "metadata_privacy_optional": r"optionally, confidentiality and metadata privacy",
    "normative_keywords": r"RFC2119",
}
def examine(source: str) -> dict:
    return {
        "source_url": URL,
        "source_commit": COMMIT,
        "source_path": "spec/spec.md",
        "sha256": hashlib.sha256(source.encode("utf-8")).hexdigest(),
        "byte_length": len(source.encode("utf-8")),
        "checks": {key: bool(re.search(pattern, source, re.I | re.S)) for key, pattern in CHECKS.items()},
        "evidence_class": "static-specification-text",
        "conformance": "NOT_TESTED",
        "security": "NOT_TESTED",
        "composition": "NOT_TESTED",
        "drarm": "NOT_TESTED",
        "published_render_equivalence": "NOT_ESTABLISHED",
        "assurance_disposition": "INDETERMINATE",
    }

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=pathlib.Path, help="Local exact-source copy; bypasses network")
    parser.add_argument("--output", type=pathlib.Path, required=True)
    args = parser.parse_args()
    if args.source:
        source = args.source.read_text(encoding="utf-8")
    else:
        request = urllib.request.Request(URL, headers={"User-Agent": "RAHP-TSP-evidence-preflight/1"})
        with urllib.request.urlopen(request, timeout=25) as response:
            source = response.read().decode("utf-8")
    result = examine(source)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"sha256": result["sha256"], "checks": result["checks"],
                      "assurance_disposition": result["assurance_disposition"]}, indent=2))
    return 0 if all(result["checks"].values()) else 1

if __name__ == "__main__":
    raise SystemExit(main())
