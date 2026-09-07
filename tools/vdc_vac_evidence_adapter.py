#!/usr/bin/env python3
"""Run the pinned Interop Lab VDC/VAC semantic vectors and expose RAHP evidence surfaces."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--interop-root", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    root = args.interop_root.resolve()
    run_py = root / "experiments" / "dtg-vdc-vac-composition" / "run.py"
    proc = subprocess.run(
        [sys.executable, str(run_py)],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        print(proc.stdout, end="")
        print(proc.stderr, end="", file=sys.stderr)
        return proc.returncode

    raw = json.loads(proc.stdout)
    matched = bool(raw.get("all_expected_outcomes_matched"))
    vectors = raw.get("vectors") or []
    if not vectors or not matched:
        print("VDC/VAC semantic vectors are absent or do not all match expected outcomes", file=sys.stderr)
        return 1

    doc = {
        **raw,
        "requirements": {
            "ER-VDC-VAC-NON-SUBSTITUTION": {
                "surfaces": {
                    "semantic-negative-vectors": {
                        "classification": "verified",
                        "observation": f"{len(vectors)} source-pinned vectors executed; every expected allow/deny outcome matched."
                    }
                }
            }
        }
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"vectors": len(vectors), "all_expected_outcomes_matched": matched}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
