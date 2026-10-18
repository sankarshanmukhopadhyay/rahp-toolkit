"""Offline source-artifact audit for eight immutable DTG controller transfers.

No issue state is mutated here. The source workflow zip archives are optional
in CI, but when supplied every pinned route and classification is rechecked.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/assurance/dtg-eight-controller-transfer-2026-10-18.json"
ROUTES = {"UNMAPPED", "combined", "covered", "no-action"}
STATES = {"review-transfer", "reasoned-release-aggregate", "corrected-material-transfer"}


def validate_manifest(data: dict) -> list[str]:
    errors: list[str] = []
    if data.get("schema") != "rahp-dtg-controller-transfer/v1":
        errors.append("unexpected schema")
    if data.get("no_terminal_assurance_claim") is not True:
        errors.append("terminal-assurance boundary missing")
    snaps = data.get("snapshots")
    findings = data.get("findings")
    if not isinstance(snaps, list) or len(snaps) != 8:
        errors.append("exactly eight snapshots required")
        snaps = []
    if not isinstance(findings, list) or len(findings) != 54:
        errors.append("exactly 54 distinct transfer entries required")
        findings = []
    seen_issues: set[int] = set()
    seen_digests: set[str] = set()
    for item in snaps:
        n, digest = item.get("controller_issue"), item.get("snapshot_digest")
        if n in seen_issues:
            errors.append(f"duplicate controller {n}")
        seen_issues.add(n)
        if digest in seen_digests:
            errors.append(f"duplicate snapshot digest {digest}")
        seen_digests.add(digest)
        for field in ("snapshot_digest", "routing_sha256"):
            if not re.fullmatch("[0-9a-f]{64}", str(item.get(field, ""))):
                errors.append(f"#{n}: missing/invalid {field}")
        if not isinstance(item.get("artifact_id"), int) or item["artifact_id"] <= 0:
            errors.append(f"#{n}: invalid source artifact")
        dist = item.get("distribution", {})
        if set(dist) != ROUTES or any(not isinstance(x, int) or x < 0 for x in dist.values()):
            errors.append(f"#{n}: invalid distribution")
        elif sum(dist.values()) != item.get("count"):
            errors.append(f"#{n}: count does not match distribution")
    seen_ids: set[str] = set()
    for f in findings:
        fid = f.get("finding_id")
        if not re.fullmatch("[0-9a-f]{20}", str(fid)):
            errors.append(f"invalid identity {fid}")
        if fid in seen_ids:
            errors.append(f"duplicate finding {fid}")
        seen_ids.add(fid)
        outcome, disposition, owner = f.get("source_outcome"), f.get("disposition"), f.get("owner_issue")
        if outcome not in ROUTES or disposition not in STATES:
            errors.append(f"{fid}: invalid outcome/disposition")
        if disposition == "reasoned-release-aggregate":
            if outcome != "no-action" or owner is not None:
                errors.append(f"{fid}: unjustified no-action exception")
        elif not isinstance(owner, int) or owner <= 0 or owner in (121, 527):
            errors.append(f"{fid}: no active/narrow owner or old wrapper")
        if disposition == "corrected-material-transfer" and (fid != "aa28149c7babc678e9e7" or outcome != "no-action" or owner != 994):
            errors.append(f"{fid}: undocumented routing correction")
    if sum(f.get("disposition") == "reasoned-release-aggregate" for f in findings) != 9:
        errors.append("release aggregate inventory must have nine source IDs")
    if sum(f.get("disposition") == "corrected-material-transfer" for f in findings) != 1:
        errors.append("exactly one historical false-negative correction required")
    return errors


def audit_archives(data: dict, directory: Path) -> list[str]:
    errors = validate_manifest(data)
    wanted = {f["finding_id"]: f for f in data["findings"]}
    union: set[str] = set()
    for snap in data["snapshots"]:
        number, artifact_id = snap["controller_issue"], snap["artifact_id"]
        path = directory / f"github-actions-artifact-{artifact_id}.zip"
        if not path.is_file():
            errors.append(f"#{number}: absent source artifact {path}")
            continue
        with zipfile.ZipFile(path) as zipped:
            raw = zipped.read("routing.json")
            if hashlib.sha256(raw).hexdigest() != snap["routing_sha256"]:
                errors.append(f"#{number}: source routing digest mismatch")
                continue
            routes = json.loads(raw)
            event = json.loads(zipped.read("controller-events.json"))[0]
            combined = json.loads(zipped.read("combined-result.json")).get("issues", [])
            dpip = json.loads(zipped.read("dpip-events.json"))
            if snap["snapshot_digest"] not in event.get("assessment_key", ""):
                errors.append(f"#{number}: source controller digest mismatch")
            if dpip:
                errors.append(f"#{number}: DPIP referrals require separate child reconciliation")
            if len(routes) != snap["count"]:
                errors.append(f"#{number}: source count mismatch")
            if dict(collections.Counter(x["outcome"] for x in routes)) != {k:v for k,v in snap["distribution"].items() if v}:
                errors.append(f"#{number}: source route distribution mismatch")
            covered_rules = {x["assessment_key"].rsplit(":", 1)[-1] for x in combined}
            seen_in_snapshot: set[str] = set()
            for x in routes:
                finding = x["finding"]
                fid = finding["finding_id"]
                if fid in seen_in_snapshot:
                    errors.append(f"#{number}: duplicate source finding {fid}")
                seen_in_snapshot.add(fid)
                union.add(fid)
                target = wanted.get(fid)
                if target is None or target["source_outcome"] != x["outcome"]:
                    errors.append(f"#{number}: missing/misclassified finding {fid}")
                    continue
                if x["outcome"] == "combined" and x["rule_id"] not in covered_rules:
                    errors.append(f"#{number}: combined child missing for {fid}")
                if target["disposition"] == "reasoned-release-aggregate":
                    title = finding.get("title", "")
                    if not (re.search(r"-v[0-9]+\\.[0-9]+\\.[0-9]+$", title) or title == "chore: release"):
                        errors.append(f"#{number}: non-release silently no-action {fid}")
                if target["disposition"] == "corrected-material-transfer":
                    if "behavior-change" not in x["normalized_finding"].get("change_kind", []):
                        errors.append(f"#{number}: historical correction unsupported {fid}")
    if union != set(wanted):
        errors.append(f"snapshot union mismatch: missing={sorted(set(wanted)-union)}, unexpected={sorted(union-set(wanted))}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive-dir", type=Path, help="directory of exact source GitHub Actions artifact ZIPs")
    parser.add_argument("--manifest", type=Path, default=DATA)
    args = parser.parse_args()
    data = json.loads(args.manifest.read_text())
    errors = audit_archives(data, args.archive_dir) if args.archive_dir else validate_manifest(data)
    for error in errors:
        print("ERROR:", error)
    if not errors:
        print(f"PASS: {len(data['snapshots'])} snapshot pins, {len(data['findings'])} distinct findings; no terminal PASS inferred")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
