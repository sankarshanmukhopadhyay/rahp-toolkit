"""Runnable R1-R3 worked consumption example; no terminal assurance decision."""
from __future__ import annotations

import hashlib
import json

from tools.evidence_adequacy import evaluate
from tools.temporal_provenance import evaluate_temporal
from tools.reproducibility_challenge import compare


def _pin(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def run_scenario(scenario: str = "baseline") -> dict:
    """Return deterministic bounded outputs for one declared historical proposition."""
    if scenario not in {"baseline", "missing", "retroactive", "disagreement"}:
        raise ValueError("unknown scenario")
    scope = "illustrative TRQP historical answer at pinned draft"
    proposition = "EX-TRQP-HISTORY-001"
    adequacy = {
        "schema": "rahp-evidence-adequacy/v1",
        "proposition_id": proposition, "scope": scope,
        "required_evidence": ["authority-assertion", "source-snapshot"],
        "observations": [
            {"id": "OBS-A", "evidence_id": "authority-assertion", "scope": scope, "state": "SATISFIED"},
            {"id": "OBS-S", "evidence_id": "source-snapshot", "scope": scope, "state": "SATISFIED"},
        ],
    }
    if scenario == "missing":
        adequacy["observations"] = [x for x in adequacy["observations"] if x["evidence_id"] != "source-snapshot"]

    def record(eid: str, rid: str) -> dict:
        return {"id": rid, "evidence_id": eid,
                "source_pin": {"repository": "example/trqp-draft", "revision": "a" * 40},
                "observed_at": "2026-04-15T00:00:00Z", "recorded_at": "2026-04-16T00:00:00Z",
                "effective_from": "2026-04-10T00:00:00Z", "effective_until": "2026-05-01T00:00:00Z"}

    temporal = {
        "schema": "rahp-temporal-provenance/v1", "proposition_id": proposition,
        "target_time": "2026-04-15T00:00:00Z",
        "knowledge_cutoff": "2026-05-01T00:00:00Z",
        "evaluated_at": "2026-08-20T00:00:00Z",
        "required_evidence": ["authority-assertion", "source-snapshot"],
        "records": [record("authority-assertion", "REC-A"), record("source-snapshot", "REC-S")],
    }
    if scenario == "retroactive":
        later = record("authority-assertion", "REC-LATER")
        later["recorded_at"] = "2026-08-15T00:00:00Z"
        later["effective_from"] = "2026-04-01T00:00:00Z"
        temporal["records"].append(later)

    a = evaluate(adequacy)
    t = evaluate_temporal(temporal)
    declared_input = {"adequacy": adequacy, "temporal": temporal}
    pin = _pin(declared_input)
    runs = [
        {"id": rid, "evaluator_id": "example-consumer", "evaluator_version": "1",
         "input_pin": {"algorithm": "sha256", "digest": pin},
         "outcome": "INDETERMINATE" if a["outcome"] != "PASS" or t["disposition"] != "APPLICABLE" else "PASS"}
        for rid in ("RUN-A", "RUN-B")
    ]
    challenges = []
    if scenario == "disagreement":
        runs[1]["outcome"] = "FAIL"
        challenges = [{"id": "CH-1", "run_id": "RUN-B", "reason": "METHOD",
                       "evidence_refs": ["OBS-A"]}]
    r = compare({"schema": "rahp-reproducibility-challenge/v1",
                 "proposition_id": proposition, "runs": runs, "challenges": challenges})
    return {"scenario": scenario, "r1": a, "r2": t, "r3": r,
            "assurance_note": "Example consumer only: no terminal RAHP assurance decision; synthetic evidence and declared source pins."}


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", choices=["baseline", "missing", "retroactive", "disagreement"],
                        default="baseline")
    args = parser.parse_args()
    print(json.dumps(run_scenario(args.scenario), sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
