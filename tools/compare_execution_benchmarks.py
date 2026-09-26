#!/usr/bin/env python3
"""Compare like-for-like RAHP benchmark artefacts conservatively."""
from __future__ import annotations
import argparse, json
from pathlib import Path

def load(path: Path) -> dict:
    value=json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value,dict): raise ValueError("benchmark must be an object")
    return value

def compare(baseline: dict, candidate: dict, *, max_regression_percent: float=20.0, min_absolute_seconds: float=1.0) -> dict:
    if baseline.get("contract") != candidate.get("contract"):
        return {"status":"incomparable","reason":"contract-mismatch"}
    if baseline.get("profile") != candidate.get("profile"):
        return {"status":"incomparable","reason":"profile-mismatch"}
    if baseline.get("profile_exit_code") != 0 or candidate.get("profile_exit_code") != 0:
        return {"status":"invalid","reason":"benchmark-command-failure"}
    if baseline.get("semantic_reference_digests") != candidate.get("semantic_reference_digests"):
        return {"status":"fail","reason":"semantic-reference-digest-mismatch"}
    b=float(baseline["wall_seconds"]); c=float(candidate["wall_seconds"])
    delta=c-b
    pct=(delta/b*100.0) if b>0 else 0.0
    meaningful=delta>min_absolute_seconds and pct>max_regression_percent
    return {
      "status":"fail" if meaningful else "pass",
      "reason":"meaningful-performance-regression" if meaningful else "within-policy",
      "baseline_seconds":round(b,6),"candidate_seconds":round(c,6),
      "delta_seconds":round(delta,6),"delta_percent":round(pct,3),
      "policy":{"max_regression_percent":max_regression_percent,"min_absolute_seconds":min_absolute_seconds},
      "authority_boundary":{"assurance_evidence":False,"may_set_assurance_outcome":False,"purpose":"performance-engineering"},
    }

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument("baseline",type=Path); ap.add_argument("candidate",type=Path)
    ap.add_argument("--max-regression-percent",type=float,default=20.0)
    ap.add_argument("--min-absolute-seconds",type=float,default=1.0)
    ap.add_argument("--output",type=Path)
    a=ap.parse_args()
    result=compare(load(a.baseline),load(a.candidate),max_regression_percent=a.max_regression_percent,min_absolute_seconds=a.min_absolute_seconds)
    text=json.dumps(result,indent=2,sort_keys=True)+"\n"
    if a.output: a.output.write_text(text,encoding="utf-8")
    else: print(text,end="")
    return 1 if result["status"]=="fail" else (2 if result["status"] in {"invalid","incomparable"} else 0)
if __name__=="__main__": raise SystemExit(main())
