#!/usr/bin/env python3
"""Evidence-conservative, opt-in sociotechnical profile over reviewed assertions.

The profile does not discover harms, verify consent or establish independence from
metadata alone. It reconciles explicitly reviewed, source/context-bound assertions.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

try:
    from .assurance_fsm import new_run, transition, terminal_from_specialist
    from .human_choice_invariants import evaluate_disclosure_pressure, evaluate_meaningful_choice
except ImportError:  # CLI execution from tools/
    from assurance_fsm import new_run, transition, terminal_from_specialist
    from human_choice_invariants import evaluate_disclosure_pressure, evaluate_meaningful_choice

ROOT = Path(__file__).resolve().parents[1]
PROFILE = "rahp-sociotechnical/v1"
BOUNDARY = "Reviewed assertion reconciliation only; no deployment approval, legal certification or independent human validation is inferred."
SCHEMA_PATH = ROOT / "schemas/rahp-sociotechnical-input-v1.schema.json"
EVALUATORS = {"disclosure-pressure": evaluate_disclosure_pressure, "meaningful-choice": evaluate_meaningful_choice}
MAX_INPUT_BYTES = 1_048_576


def read_json_limited(path: Path, *, max_bytes: int = MAX_INPUT_BYTES) -> Any:
    """Read one JSON file while bounding bytes consumed before parsing."""
    with path.open("rb") as handle:
        raw = handle.read(max_bytes + 1)
    if len(raw) > max_bytes:
        raise ValueError(f"JSON input exceeds the {max_bytes}-byte size limit")
    return json.loads(raw.decode("utf-8"))


def digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def validate_input(value: dict[str, Any]) -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    errors = sorted(Draft202012Validator(schema).iter_errors(value), key=lambda e: str(list(e.path)))
    if errors:
        raise ValueError("; ".join(f"{list(e.path)}: {e.message}" for e in errors))
    for collection in ("propositions", "evidence", "assessors", "disagreements", "obligations"):
        ids = [item["id"] for item in value[collection]]
        if len(set(ids)) != len(ids):
            raise ValueError(f"duplicate {collection} identity")
    props = {p["id"]: p for p in value["propositions"]}
    evidence = {e["id"]: e for e in value["evidence"]}
    assessors = {a["id"] for a in value["assessors"]}
    actors = {a["id"] for a in value["frame"]["actors"]}
    for control in value["frame"]["controls"]:
        if control["beneficiary"] not in actors or control["burden_bearer"] not in actors:
            raise ValueError("control role must reference a framed actor")
    for e in evidence.values():
        if e["proposition"] not in props or e["assessor"] not in assessors:
            raise ValueError("unknown evidence proposition/assessor")
        if e["id"] not in props[e["proposition"]]["evidence_ids"]:
            raise ValueError("supplied proposition evidence must not be silently excluded")
    for item in [*props.values(), *value["disagreements"], *value["obligations"]]:
        pid = item.get("proposition", item["id"])
        if pid not in props:
            raise ValueError("unknown contested/remedy proposition")
        for eid in item["evidence_ids"]:
            if eid not in evidence or evidence[eid]["proposition"] != pid:
                raise ValueError("unknown or wrong-proposition evidence reference")
    for eid in value["challenge_route"]["evidence"]:
        if eid not in evidence:
            raise ValueError("unknown challenge-route evidence")
    if value["review"]["independent_human"] == "completed":
        # Completed review needs an actual reviewer record, not merely a flag.
        raise ValueError("independent human review must use an attributable external review packet; not an input flag")
    if value["lineage"]["previous_context"] is not None and not value["lineage"]["previous_assessment"]:
        raise ValueError("previous context requires an assessment lineage owner")


def admission(evidence: dict[str, Any], value: dict[str, Any]) -> list[str]:
    reasons = []
    if evidence["context_digest"] != digest(value["context"]):
        reasons.append("context-mismatch")
    if evidence["source_pin"] not in value["source_pins"]:
        reasons.append("source-pin-mismatch")
    if evidence["provenance"]["revision"] != evidence["source_pin"]["revision"]:
        reasons.append("provenance-revision-mismatch")
    if evidence["freshness"] != "current":
        reasons.append("evidence-not-current")
    if evidence["sufficient"] is not True:
        reasons.append("evidence-insufficient")
    if evidence["status"] == "unknown":
        reasons.append("assertion-unknown")
    return reasons


def dependence_groups(assessors: list[dict[str, Any]]) -> list[list[str]]:
    """Conservatively join reviewed assessors sharing any declared material basis."""
    groups: list[set[str]] = []
    by_id = {a["id"]: a for a in assessors}
    for a in assessors:
        group = {a["id"]}
        remaining = []
        for existing in groups:
            shared = any(
                set(a["dependence"][key]) & set(by_id[other]["dependence"][key])
                for other in existing for key in a["dependence"]
            )
            if shared:
                group.update(existing)
            else:
                remaining.append(existing)
        groups = [*remaining, group]
    return sorted(sorted(g) for g in groups)


def evaluate(value: dict[str, Any]) -> dict[str, Any]:
    validate_input(value)
    evidence = {e["id"]: e for e in value["evidence"]}
    assessors = {a["id"]: a for a in value["assessors"]}
    results = []
    for p in value["propositions"]:
        admitted, rejected = [], []
        for eid in p["evidence_ids"]:
            e = evidence[eid]
            reasons = admission(e, value)
            if e["class"] not in p["required_classes"]:
                reasons.append("wrong-evidence-class")
            if reasons:
                rejected.append({"id": eid, "reasons": reasons})
            else:
                admitted.append(e)
        supported = [e for e in admitted if e["status"] == "supported"]
        refuted = [e["id"] for e in admitted if e["status"] == "refuted"]
        missing = [c for c in p["required_classes"] if not any(e["class"] == c for e in supported)]
        reviewed_ids = sorted({e["assessor"] for e in supported if assessors[e["assessor"]]["independence_review"]["state"] == "verified"})
        groups = dependence_groups([assessors[a] for a in reviewed_ids])
        unknown = sorted({e["assessor"] for e in supported} - set(reviewed_ids))
        independent = True
        if p["independent_corroboration_required"]:
            for cls in p["required_classes"]:
                ids = {e["assessor"] for e in supported if e["class"] == cls}
                if sum(bool(ids & set(g)) for g in groups) < 2:
                    independent = False
        reasons = []
        if refuted:
            outcome = "FAIL"
            reasons.append("admitted-refutation:" + ",".join(refuted))
        elif missing or not independent:
            outcome = "INDETERMINATE"
        elif not p["applicable"]:
            outcome = "NOT_APPLICABLE" if p["not_applicable_reason"].strip() else "INDETERMINATE"
            reasons.append(p["not_applicable_reason"] or "non-applicability-unjustified")
        elif p["evaluator"] in EVALUATORS:
            result = EVALUATORS[p["evaluator"]](p["facts"])
            outcome = result["outcome"]
            reasons.extend(result["reasons"])
            # A privacy-depth referral is an obligation, not evidence of its resolution.
            if result.get("dpip_handoff_required") and outcome == "PASS":
                outcome = "INDETERMINATE"
                reasons.append("material-specialist-return-required")
        else:
            outcome = "PASS"
            reasons.append("reviewed-assertion-supported-within-scope")
        if missing:
            reasons.append("required-evidence-missing:" + ",".join(missing))
        if not independent:
            reasons.append("independent-corroboration-not-established")
        results.append({"proposition": p["id"], "claim": p["claim"], "outcome": outcome,
                        "reasons": reasons, "admitted_evidence": [e["id"] for e in admitted],
                        "rejected_evidence": rejected, "dependence_groups": groups,
                        "independence_unknown": unknown})
    by_prop = {r["proposition"]: r for r in results}
    unresolved = []
    for item in value["disagreements"]:
        if item["state"] == "unresolved":
            unresolved.append(item["id"])
    for item in value["obligations"]:
        if (item["state"] != "resolved" or not item["evidence_ids"]
                or by_prop[item["proposition"]]["outcome"] != "PASS"
                or any(eid not in by_prop[item["proposition"]]["admitted_evidence"]
                       or evidence[eid]["status"] != "supported"
                       for eid in item["evidence_ids"])):
            unresolved.append(item["id"])
    route = value["challenge_route"]
    if route["state"] == "demonstrated" and (route["account_independent"] is not True or not route["evidence"]
            or any(eid not in by_prop[evidence[eid]["proposition"]]["admitted_evidence"]
                   or by_prop[evidence[eid]["proposition"]]["outcome"] != "PASS"
                   or evidence[eid]["status"] != "supported" for eid in route["evidence"])):
        unresolved.append("challenge-route-not-demonstrated")
    outcomes = {r["outcome"] for r in results}
    overall = ("FAIL" if "FAIL" in outcomes else "INDETERMINATE" if "INDETERMINATE" in outcomes or unresolved
               else "NOT_APPLICABLE" if outcomes == {"NOT_APPLICABLE"} else "PASS")
    previous = value["lineage"]["previous_context"]
    changed = sorted(k for k in value["context"] if previous is not None and previous[k] != value["context"][k])
    return {"profile": PROFILE, "input": deepcopy(value), "input_digest": digest(value),
            "context_digest": digest(value["context"]), "changed_context": changed,
            "results": results, "unresolved": sorted(unresolved), "outcome": overall,
            "deployment_approval": False, "boundary": BOUNDARY}


def build_record(value: dict[str, Any]) -> dict[str, Any]:
    result = evaluate(value)
    subject = {**value["subject"], "assurance_profile": PROFILE, "context_digest": result["context_digest"]}
    pins = [*deepcopy(value["source_pins"]), {"repository": PROFILE, "revision": result["input_digest"], "artifact": "reviewed-input"}]
    run = new_run(subject, pins)
    for state in ("OBSERVED", "GATHERED", "MATERIALITY_COMPLETE", "ASSESSMENT_COMPLETE", "RECONCILED"):
        transition(run, state, "explicit reviewed sociotechnical profile")
    transition(run, terminal_from_specialist(result["outcome"]), "bounded profile reconciliation")
    run.update(sociotechnical=result, scope=value["frame"]["scope"], non_scope=value["frame"]["non_scope"],
               process_state="complete", assurance_state=result["outcome"].lower().replace("_", "-"),
               evidence_maturity="modeled", boundedness=BOUNDARY, lineage=deepcopy(value["lineage"]),
               evidence=[{"class": e["class"], "provenance": deepcopy(e["provenance"])} for e in value["evidence"]],
               harm_traceability=[{"persona": " / ".join(a["id"] for a in value["frame"]["actors"]),
                                  "scenario": value["frame"]["purpose"], "harm": "access, burden or remedy proposition",
                                  "proposition": r["proposition"], "control": "explicit profile obligations",
                                  "evidence": ",".join(r["admitted_evidence"]) or "evidence required",
                                  "conclusion": r["outcome"]} for r in result["results"]],
               residuals=[{"id": item, "summary": "Unresolved disagreement or remedy: " + item} for item in result["unresolved"]])
    return run


def validate_record(run: dict[str, Any]) -> list[str]:
    section = run.get("sociotechnical")
    if section is None:
        return ["selected sociotechnical profile is missing"] if run.get("subject", {}).get("assurance_profile") == PROFILE else []
    try:
        expected = build_record(section["input"])
        keys = ("sociotechnical", "assessment_id", "subject", "source_pins", "scope", "non_scope", "outcome",
                "state", "process_state", "assurance_state", "evidence_maturity", "boundedness", "lineage",
                "evidence", "harm_traceability", "residuals")
        return [f"sociotechnical {key} differs from evidence-bound reconciliation" for key in keys if run.get(key) != expected[key]]
    except (KeyError, TypeError, ValueError) as exc:
        return [f"invalid sociotechnical record: {exc}"]


def replay(corpus_path: Path, output: Path | None = None) -> dict[str, Any]:
    try:
        from .assurance_record import canonical_record, markdown
    except ImportError:
        from assurance_record import canonical_record, markdown
    corpus = read_json_limited(corpus_path)
    if not isinstance(corpus, dict) or corpus.get("schema") != "rahp-sociotechnical-corpus/v1" or not corpus.get("cases"):
        raise ValueError("non-empty sociotechnical corpus/v1 is required")
    paths = [case.get("path") for case in corpus["cases"]]
    if any(not isinstance(path, str) or not path for path in paths) or len(set(paths)) != len(paths):
        raise ValueError("corpus paths must be non-empty and unique")
    records = []
    for case in corpus["cases"]:
        path = (corpus_path.parent / case["path"]).resolve()
        if not path.is_relative_to(corpus_path.parent.resolve()):
            raise ValueError("corpus case escapes its input directory")
        value = read_json_limited(path)
        if digest(value) != case["sha256"]:
            raise ValueError(f"corpus input digest mismatch: {case['path']}")
        record = canonical_record(build_record(value))
        if record["outcome"] != case["expected_outcome"]:
            raise ValueError(f"unexpected outcome for {case['path']}: {record['outcome']}")
        # Rendering must retain the complete canonical record, not just an outcome.
        human = markdown(record)
        if output:
            output.mkdir(parents=True, exist_ok=True)
            stem = Path(case["path"]).stem
            (output / f"{stem}.json").write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            (output / f"{stem}.md").write_text(human, encoding="utf-8")
        records.append({"case": case["path"], "input_digest": digest(value), "outcome": record["outcome"], "assessment_id": record["assessment_id"]})
    return {"profile": PROFILE, "baseline": corpus["baseline"], "cases": records,
            "independent_human_review": "pending", "boundary": BOUNDARY}


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog="Generated records include reviewed input. Store outputs only in access-controlled locations.",
    )
    parser.add_argument("--input", type=Path)
    parser.add_argument("--corpus", type=Path)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    if bool(args.input) == bool(args.corpus):
        parser.error("provide exactly one of --input or --corpus")
    try:
        result = replay(args.corpus, args.output_dir) if args.corpus else build_record(read_json_limited(args.input))
        print(json.dumps(result, indent=2, sort_keys=True))
    except (ValueError, OSError) as exc:
        parser.exit(1, f"ERROR: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
