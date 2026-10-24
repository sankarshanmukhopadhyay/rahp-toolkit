"""Falsify upstream example-local evidence and reassessment bindings.

Imports only a trusted, source-pinned upstream checkout. Never executes
untrusted files copied into temporary evidence directories.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import sys
import tempfile
from pathlib import Path

import yaml


def load(upstream: Path, name: str, filename: Path):
    spec = importlib.util.spec_from_file_location(name, filename)
    if spec is None or spec.loader is None:
        raise ValueError("Cannot load pinned evaluator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def accepted(action, root: Path) -> bool:
    try:
        action(root)
    except (OSError, ValueError, KeyError, TypeError, IndexError):
        return False
    return True


def trqp_variant(root: Path, kind: str):
    if kind == "original":
        return
    if kind == "changed_source":
        (root / "source/api.md.txt").write_text("tampered source", encoding="utf-8")
        return
    path = root / "evidence.json"
    sidecar = json.loads(path.read_text(encoding="utf-8"))
    if kind == "wrong_assessment":
        sidecar["assessment_id"] = "SR-999"
    elif kind == "missing_finding_evidence":
        sidecar["findings"][0]["evidence"] = ["E-999"]
    elif kind == "incomplete_execution":
        sidecar["execution"]["state"] = "incomplete"
    else:
        raise ValueError(kind)
    path.write_text(json.dumps(sidecar), encoding="utf-8")


def vrc_variant(root: Path, kind: str):
    if kind == "original":
        return
    if kind == "changed_source":
        path = root / "reassessed/source/dtg.md.txt"
        path.write_text("tampered revised source", encoding="utf-8")
        return
    if kind == "reused_revision":
        path = root / "reassessed-review.yaml"
        record = yaml.safe_load(path.read_text(encoding="utf-8"))
        old = yaml.safe_load((root / "baseline-review.yaml").read_text(encoding="utf-8"))
        record["target"]["revision"] = old["target"]["revision"]
        path.write_text(yaml.safe_dump(record), encoding="utf-8")
        return
    if kind == "missing_evidence_reference":
        path = root / "reassessed-evidence.json"
        sidecar = json.loads(path.read_text(encoding="utf-8"))
        sidecar["findings"][0]["evidence"] = ["E-999"]
        path.write_text(json.dumps(sidecar), encoding="utf-8")
        return
    if kind == "false_closure":
        path = root / "reassessed-review.yaml"
        record = yaml.safe_load(path.read_text(encoding="utf-8"))
        record["findings"][1]["status"] = "resolved"
        path.write_text(yaml.safe_dump(record), encoding="utf-8")
        return
    raise ValueError(kind)


def evaluate(upstream: Path) -> dict:
    upstream = upstream.resolve()
    paths = {
        "trqp": upstream / "review/examples/standalone-trqp",
        "vrc": upstream / "review/examples/vrc-v03",
    }
    if not all(p.is_dir() for p in paths.values()):
        raise FileNotFoundError("Pinned upstream evidence examples missing")
    sys.path.insert(0, str(upstream / "review"))
    trqp = load(upstream, "pinned_trqp_examiner", upstream / "review/examine.py")
    vrc = load(upstream, "pinned_vrc_evaluator", paths["vrc"] / "evaluate.py")
    scenarios = {
        "trqp": ("original", "changed_source", "wrong_assessment",
                 "missing_finding_evidence", "incomplete_execution"),
        "vrc": ("original", "changed_source", "reused_revision",
                "missing_evidence_reference", "false_closure"),
    }
    report = []
    for name, variants in scenarios.items():
        for variant in variants:
            with tempfile.TemporaryDirectory(prefix="rahp-evidence-boundary-") as tmp:
                root = Path(tmp) / "exam"
                shutil.copytree(paths[name], root)
                if name == "trqp":
                    trqp_variant(root, variant)
                    ok = accepted(trqp.examine, root)
                else:
                    vrc_variant(root, variant)
                    ok = accepted(vrc.evaluate, root)
                report.append({"example": name, "variant": variant, "accepted": ok})
    return {
        "scope": "accepted upstream example-local evidence binding and VRC reassessment only",
        "not_claimed": ["shared evidence sidecar schema", "downstream controller equivalence",
                        "deployment assurance", "risk acceptance"],
        "cases": report,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--upstream", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = evaluate(args.upstream)
    for case in result["cases"]:
        if case["accepted"] != (case["variant"] == "original"):
            print(json.dumps(result, indent=2))
            raise SystemExit(f"Evidence boundary diverged from expectation: {case}")
    output = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
