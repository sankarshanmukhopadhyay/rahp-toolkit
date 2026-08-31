#!/usr/bin/env python3
"""First-class RAHP clean-room run contract.

This module resolves engine-owned clean-room lineage and validates that a run
cannot silently consume historical state/evidence or coalesce with prior work.
"""
from __future__ import annotations
import argparse, json, pathlib
from typing import Any
from assessment_controller import clean_room_lineage

REQUIRED = {"schema", "run", "target", "resources", "assessment", "evidence_plan"}
SUPPORTED = {"rahp-clean-room-run/v1", "rahp-clean-room-run/v2"}


def resolve(spec: dict[str, Any], *, instance: str, snapshot: str, nonce: str) -> dict[str, Any]:
    missing = sorted(REQUIRED - set(spec))
    if missing:
        raise ValueError(f"run specification missing keys: {missing}")
    if spec.get("schema") not in SUPPORTED:
        raise ValueError("unsupported clean-room run schema")
    target = spec.get("target") or {}
    if not all(target.get(k) for k in ("repository", "revision", "path")):
        raise ValueError("target repository/revision/path are required")
    if spec.get("schema") == "rahp-clean-room-run/v2":
        subject = spec.get("subject") or {}
        contract = spec.get("assurance_contract") or {}
        if not subject.get("type") or not subject.get("id"):
            raise ValueError("v2 clean-room run requires subject.type and subject.id")
        if "material" not in contract:
            raise ValueError("v2 clean-room run requires assurance_contract.material")
    lineage = clean_room_lineage(instance, snapshot, nonce)
    return {
        "schema": "rahp-clean-room-resolution/v1",
        "run_schema": spec.get("schema"),
        "mode": "clean-room",
        "lineage": lineage,
        "target": target,
        **({"subject": spec.get("subject")} if spec.get("subject") else {}),
        "historical_inputs_used": False,
        "coalescing_allowed": False,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", type=pathlib.Path, required=True)
    ap.add_argument("--instance")
    ap.add_argument("--snapshot")
    ap.add_argument("--nonce", required=True)
    ap.add_argument("--output", type=pathlib.Path)
    args = ap.parse_args()
    spec = json.loads(args.spec.read_text(encoding="utf-8"))
    run = spec.get("run") or {}
    instance = args.instance or str(run.get("instance") or "").strip()
    snapshot = args.snapshot or str(run.get("snapshot") or "").strip()
    if not instance:
        raise SystemExit("clean-room instance is required in run.instance or --instance")
    if not snapshot:
        raise SystemExit("clean-room snapshot is required in run.snapshot or --snapshot")
    result = resolve(spec, instance=instance, snapshot=snapshot, nonce=args.nonce)
    text = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
