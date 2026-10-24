"""Run accepted upstream RAHP review examples without reinterpreting their authority.

This is a contract-boundary probe: it does not convert upstream review statuses
into downstream terminal assurance conclusions.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

EXAMPLES = {
    "trqp": ("review/examples/standalone-trqp/review.yaml",
             "review/examples/standalone-trqp/risks.yaml"),
    "vrc_baseline": ("review/examples/vrc-v03/baseline-review.yaml", "data/risks.yaml"),
    "vrc_reassessed": ("review/examples/vrc-v03/reassessed-review.yaml", "data/risks.yaml"),
}


def check(upstream: Path, review: Path, risks: Path) -> bool:
    args = [sys.executable, str(upstream / "review/validate_spec_review.py"),
            str(review), "--risks", str(risks)]
    run = subprocess.run(args, cwd=upstream, capture_output=True, text=True, check=False)
    return run.returncode == 0


def mutate(original: dict, change: str) -> dict:
    record = json.loads(json.dumps(original))
    if change == "mutable_target":
        record["target"]["revision"] = "main"
    elif change == "unknown_risk":
        record["findings"][0]["risks"] = ["RK-ZZ99"]
    elif change == "duplicate_finding":
        record["findings"].append(json.loads(json.dumps(record["findings"][0])))
    elif change == "invalid_status":
        record["findings"][0]["status"] = "PASS"
    elif change == "unsupported_evidence_extension":
        record["findings"][0]["evidence"] = [{"uri": "example.json"}]
    else:
        raise ValueError(change)
    return record


def evaluate(upstream: Path) -> dict:
    if not (upstream / "review/spec-review.schema.json").is_file():
        raise FileNotFoundError("Pinned upstream review contract missing")
    cases = []
    with tempfile.TemporaryDirectory(prefix="rahp-review-boundary-") as directory:
        temp = Path(directory) / "review.yaml"
        for case, (review_rel, risks_rel) in EXAMPLES.items():
            review_path, risks_path = upstream / review_rel, upstream / risks_rel
            if not review_path.is_file() or not risks_path.is_file():
                raise FileNotFoundError(f"Upstream fixture absent: {case}")
            original = yaml.safe_load(review_path.read_text(encoding="utf-8"))
            accepted = check(upstream, review_path, risks_path)
            cases.append({"case": case, "variant": "retained_valid", "accepted": accepted})
            for variant in ("mutable_target", "unknown_risk", "duplicate_finding",
                            "invalid_status", "unsupported_evidence_extension"):
                temp.write_text(yaml.safe_dump(mutate(original, variant)), encoding="utf-8")
                cases.append({"case": case, "variant": variant,
                              "accepted": check(upstream, temp, risks_path)})
    return {
        "scope": "accepted upstream rahp-spec-review/v1 validator only",
        "not_claimed": ["downstream controller equivalence", "evidence adequacy",
                        "risk acceptance", "independent human review"],
        "cases": cases,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--upstream", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = evaluate(args.upstream.resolve())
    for row in report["cases"]:
        expected = row["variant"] == "retained_valid"
        if row["accepted"] is not expected:
            print(json.dumps(report, indent=2))
            raise SystemExit(f"Unexpected review validation outcome: {row}")
    output = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
