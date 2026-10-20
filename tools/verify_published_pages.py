#!/usr/bin/env python3
"""Independently observe the *published* RAHP Pages routes.

Build success does not prove publication. The verifier fetches the public URL,
tests navigation/content, and fails closed on unavailable or malformed pages.
No GitHub issue is automatically closed.
"""
from __future__ import annotations

import argparse
import json
import re
import urllib.request
from datetime import datetime, timezone

ROOT = "https://sankarshanmukhopadhyay.github.io/rahp-toolkit"
CORPORA_ROUTE = "/corpora/"
REASONING_ROUTE = "/docs/reasoning-worked-example/"
CORPORA = (
    "dtg-zkp", "trust-tasks", "credential-spec", "trust-tasks-credential-spec-composed",
)
# Authoritative corpus identifiers are loaded from source YAML filenames by the
# caller, rather than duplicating a possibly stale set of 15 here.

def observe_document(html: str, required_fragments: list[str]) -> list[str]:
    text = re.sub(r"\s+", " ", html.lower())
    if "<html" not in text and "<!doctype html" not in text:
        return ["response is not an HTML document"]
    missing = [f for f in required_fragments if f.lower() not in text]
    return [f"missing published fragment: {f}" for f in missing]


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "rahp-published-evidence/1.0"})
    with urllib.request.urlopen(req, timeout=20) as response:
        if response.status != 200:
            raise RuntimeError(f"{url}: HTTP {response.status}")
        content_type = response.headers.get("Content-Type", "")
        if "text/html" not in content_type:
            raise RuntimeError(f"{url}: unexpected content type {content_type}")
        return response.read(5_000_001).decode("utf-8")


def assess(root: str, corpus_slugs: list[str]) -> dict:
    records: list[dict] = []
    def check(route: str, fragments: list[str]) -> None:
        url = root.rstrip("/") + route
        record = {"url": url, "errors": []}
        try:
            html = fetch(url)
            record["errors"] = observe_document(html, fragments)
        except (OSError, UnicodeError, RuntimeError) as exc:
            record["errors"] = [f"unavailable: {type(exc).__name__}: {exc}"]
        record["status"] = "PASS" if not record["errors"] else "INDETERMINATE"
        records.append(record)

    check(CORPORA_ROUTE, ["how to read a corpus", *[f"{slug}/" for slug in corpus_slugs]])
    for slug in corpus_slugs:
        check(f"/corpora/{slug}/", ["<html"])
    # #1091: publication must include the actual people-impact projection, not merely a working corpus route.
    check("/corpora/trust-tasks/", ["Potential people-impact pathways", "TT-002", "provisional", "not-established"])
    check("/corpora/trust-tasks-credspec-composed/", ["Potential people-impact pathways", "XSP-001", "provisional", "not-established"])
    check("/method/scenario-patterns/", ["scenario"])
    check("/docs/reading-scenario-corpus.html", ["Reading a scenario corpus", "TT-002"])
    check("/docs/glossary.html", ["RAHP glossary"])
    check("/docs/people-impact-pathway-pilot.html", ["People-impact pathway pilot", "TT-002", "XSP-001"])
    check("/docs/people-impact-qualification-acceptance.html", ["People-impact qualification acceptance packet", "TT-005", "XSP-018", "independent"])
    check(REASONING_ROUTE, ["r1", "r2", "r3"])
    return {
        "schema": "rahp-published-pages-observation/v1",
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "scope": "public HTTP published content, not DCO or independent assurance",
        "records": records,
        "disposition": "PASS" if all(r["status"] == "PASS" for r in records) else "INDETERMINATE",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=ROOT)
    parser.add_argument("--output", required=True)
    parser.add_argument("--corpora-dir", default="corpora")
    args = parser.parse_args()
    from pathlib import Path
    slugs = sorted(path.stem for path in Path(args.corpora_dir).glob("*.yaml") if path.name != "sources.yaml")
    if not slugs:
        raise SystemExit("no corpus YAML input found; refusing false publication PASS")
    result = assess(args.root, slugs)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"{result['disposition']}: {len(result['records'])} public routes observed")
    for record in result["records"]:
        print(f"- {record['status']}: {record['url']} " + "; ".join(record["errors"]))
    return 0 if result["disposition"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
