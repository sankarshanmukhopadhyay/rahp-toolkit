#!/usr/bin/env python3
"""Stage lossless DTG Registry transfer partitions; never authorize publication.

Use the canonical Toolkit publisher ledger validator. Held observations remain
accounted for and --check-transfers independently blocks all Toolkit writers.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from publish_assessment_issues import TRANSFER_LEDGER, load_transfer_keys


def sha(payload):
    return hashlib.sha256(payload).hexdigest()


def canonical(event):
    return json.dumps(event, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")


def stage(batches: list[Path], out_dir: Path, ledger: Path = TRANSFER_LEDGER, *, source_combined: Path | None = None):
    keys = load_transfer_keys(ledger)
    records = json.loads(ledger.read_text(encoding="utf-8"))["transfers"]
    by_key = {item["assessment_key"]: item for item in records}
    if set(by_key) != keys:
        raise ValueError("transfer record identity mismatch")
    if not batches or len({p.name for p in batches}) != len(batches):
        raise ValueError("nonempty uniquely named publication batches required")
    raw_combined = None
    if source_combined is not None:
        source_data = json.loads(source_combined.read_text(encoding="utf-8"))
        if not isinstance(source_data, list):
            raise ValueError("original combined source snapshot must be a JSON array")
        raw_combined = source_data
    staged, outputs = [], []
    for path in batches:
        data = path.read_bytes()
        source = json.loads(data.decode("utf-8"))
        if not isinstance(source, list):
            raise ValueError(f"{path}: source batch must be a JSON array")
        retained, held = [], []
        for item in source:
            if not isinstance(item, dict):
                raise ValueError(f"{path}: every event must be an object")
            key, related = item.get("assessment_key"), item.get("related_assessment_key")
            for value in (key, related):
                if value is not None and (not isinstance(value, str) or not value.strip()):
                    raise ValueError(f"{path}: malformed key/related-key")
            names = {value for value in (key, related) if value in keys}
            if len(names) > 1:
                raise ValueError("one event matches multiple Registry transfer owners")
            if not names:
                retained.append(item)
            else:
                transfer = by_key[next(iter(names))]
                if transfer["state"] in ("reserved_group", "accepted_group"):
                    if item.get("assessment_key") != transfer["assessment_key"]:
                        raise ValueError("group reservation must match the primary event key")
                    if raw_combined is not None:
                        matches = [row for row in raw_combined if isinstance(row, dict)
                                   and row.get("assessment_key") == transfer["assessment_key"]]
                        if len(matches) != 1:
                            raise ValueError("one original combined source event required")
                        source_event = matches[0]
                    else:
                        source_event = item
                    if (item.get("observed_at") != transfer["snapshot_date"] or
                            source_event.get("observed_at") != transfer["snapshot_date"]):
                        raise ValueError("group reservation snapshot date differs")
                    observations = source_event.get("source_observations")
                    if not isinstance(observations, list):
                        raise ValueError("group reservation requires original source observations")
                    finding_ids = [
                        obs.get("finding_id") for obs in observations if isinstance(obs, dict)]
                    if (len(finding_ids) != len(observations)
                            or sorted(finding_ids) != transfer["finding_ids"]):
                        raise ValueError("group reservation finding membership differs")
                    if (item.get("source_observations") != observations or
                            item.get("body") != source_event.get("body")):
                        raise ValueError("journal-enriched group differs from original source evidence")
                    if sha(canonical(source_event)) != transfer["group_sha256"]:
                        raise ValueError("group reservation source event digest differs")
                held.append({
                    "event": item,
                    "event_sha256": sha(canonical(item)),
                    "source_event_sha256": (
                        sha(canonical(source_event))
                        if transfer["state"] in ("reserved_group", "accepted_group")
                        else sha(canonical(item))),
                    "transfer": transfer,
                    "delivery_acknowledged": False,
                    "publication_suppression_authorized": False,
                    "reason": ("reserved_without_successor" if transfer["state"] in
                               ("reserved", "reserved_group") else
                               "accepted_owner_lacks_current_event_receipt"),
                })
        if len(source) != len(held) + len(retained):
            raise ValueError("source event conservation violated")
        staged.append({
            "input": str(path), "source_sha256": sha(data),
            "source_count": len(source), "retained_count": len(retained),
            "held_count": len(held),
            "retained_file": path.name + ".retained.json",
            "held_file": path.name + ".held.json",
        })
        outputs.extend([(path.name + ".retained.json", retained),
                        (path.name + ".held.json", held)])
    receipt = {
        "schema": "rahp-toolkit-registry-staged-partition/v1",
        "mode": "read_only_no_cutover",
        "batches": staged,
        "source_count": sum(item["source_count"] for item in staged),
        "retained_count": sum(item["retained_count"] for item in staged),
        "held_count": sum(item["held_count"] for item in staged),
        "registry_delivery_acknowledged": False,
        "toolkit_publication_suppressed": False,
        "cutover_authorized": False,
    }
    # All validation completes before any staging output is created.
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, rows in outputs:
        (out_dir / name).write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n",
                                    encoding="utf-8")
    (out_dir / "receipt.json").write_text(json.dumps(receipt, indent=2, sort_keys=True)
                                         + "\n", encoding="utf-8")
    return receipt


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--batches", nargs="+", required=True, type=Path)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--source-combined", type=Path,
                    help="pinned pre-journal combined source event batch")
    args = ap.parse_args()
    try:
        result = stage(args.batches, args.out_dir,
                       source_combined=args.source_combined)
    except (OSError, ValueError, UnicodeError) as exc:
        ap.exit(1, f"Registry transfer stage refused: {exc}\n")
    print(f"STAGED {result['retained_count']} retained, {result['held_count']} held; "
          "no Toolkit suppression or Registry delivery")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
