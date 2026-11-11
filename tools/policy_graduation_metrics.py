#!/usr/bin/env python3
"""Compute bounded graduation-study metrics from immutable reviewer JSON records."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

SCHEMA = "rahp-policy-graduation-review/v1"
USEFUL = {"accept", "amend", "split", "merge"}


def load_review(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema") != SCHEMA:
        raise ValueError(f"{path}: schema must be {SCHEMA}")
    if not data.get("reviewer_id") or not data.get("corpus_item_id"):
        raise ValueError(f"{path}: reviewer_id and corpus_item_id are required")
    return data


def summarize_review(review: dict[str, Any]) -> dict[str, Any]:
    props = review.get("proposition_reviews") or []
    dispositions = Counter(item.get("disposition") for item in props)
    total = len(props)
    useful = sum(dispositions[name] for name in USEFUL)
    reject = dispositions["reject"]
    return {
        "reviewer_id": review["reviewer_id"],
        "reviewer_class": review.get("reviewer_class"),
        "corpus_item_id": review["corpus_item_id"],
        "proposition_count": total,
        "dispositions": dict(sorted(dispositions.items())),
        "useful_count": useful,
        "useful_percent": round((useful / total) * 100, 2) if total else None,
        "reject_count": reject,
        "reject_percent": round((reject / total) * 100, 2) if total else None,
        "effort_minutes": review.get("effort_minutes"),
        "hypothesis_classifications": dict(sorted(Counter(
            item.get("classification") for item in review.get("hypothesis_reviews") or []
        ).items())),
        "work_queue_classifications": dict(sorted(Counter(
            item.get("classification") for item in review.get("work_queue_reviews") or []
        ).items())),
    }


def compare_pair(a: dict[str, Any], b: dict[str, Any]) -> dict[str, Any]:
    if a["corpus_item_id"] != b["corpus_item_id"]:
        raise ValueError("review pair must cover the same corpus_item_id")
    a_by = {item["proposition_id"]: item for item in a.get("proposition_reviews") or []}
    b_by = {item["proposition_id"]: item for item in b.get("proposition_reviews") or []}
    common = sorted(set(a_by) & set(b_by))
    disposition_agree = sum(a_by[pid].get("disposition") == b_by[pid].get("disposition") for pid in common)
    high = [pid for pid in common if "high" in {a_by[pid].get("materiality"), b_by[pid].get("materiality")}]
    high_agree = sum(a_by[pid].get("disposition") == b_by[pid].get("disposition") for pid in high)
    return {
        "corpus_item_id": a["corpus_item_id"],
        "reviewer_a": a["reviewer_id"],
        "reviewer_b": b["reviewer_id"],
        "common_propositions": len(common),
        "disposition_agreement_count": disposition_agree,
        "disposition_agreement_percent": round((disposition_agree / len(common)) * 100, 2) if common else None,
        "high_materiality_common": len(high),
        "high_materiality_agreement_count": high_agree,
        "high_materiality_agreement_percent": round((high_agree / len(high)) * 100, 2) if high else None,
        "only_reviewer_a": sorted(set(a_by) - set(b_by)),
        "only_reviewer_b": sorted(set(b_by) - set(a_by)),
    }


def eligible_independent_record(review: dict[str, Any]) -> bool:
    """Check documentary eligibility, not actual reviewer identity or independence."""
    attestation = review.get("attestation")
    reviewer_id = review.get("reviewer_id")
    candidate = review.get("candidate_implementation_sha")
    items = review.get("proposition_reviews")
    if (
        review.get("reviewer_class") != "human-independent"
        or not isinstance(reviewer_id, str)
        or not reviewer_id.strip()
        or reviewer_id == "REPLACE"
        or not isinstance(candidate, str)
        or len(candidate) != 40
        or any(c not in "0123456789abcdef" for c in candidate.lower())
        or not isinstance(attestation, dict)
        or attestation.get("independent_of_other_reviewer") is not True
        or attestation.get("saw_other_review_before_completion") is not False
        or attestation.get("ai_assistance_used") is not False
        or not isinstance(items, list)
        or not items
    ):
        return False
    seen = set()
    for item in items:
        if not isinstance(item, dict):
            return False
        proposition_id = item.get("proposition_id")
        if not isinstance(proposition_id, str) or not proposition_id.strip() or proposition_id == "REPLACE" or proposition_id in seen:
            return False
        seen.add(proposition_id)
        if item.get("disposition") not in {
            "accept", "amend", "reject", "split", "merge",
            "judgment-required", "specialist-route",
        }:
            return False
    return True


def study_metrics(reviews: list[dict[str, Any]]) -> dict[str, Any]:
    summaries = [summarize_review(item) for item in reviews]
    by_corpus: dict[str, list[dict[str, Any]]] = {}
    for review in reviews:
        by_corpus.setdefault(review["corpus_item_id"], []).append(review)

    # Documentary eligibility guards against accidental false success. It is
    # not authentication: an attributable human review must still be verified.
    pairs = []
    eligible = [item for item in reviews if eligible_independent_record(item)]
    for corpus_id, items in sorted(by_corpus.items()):
        humans = [item for item in items if eligible_independent_record(item)]
        for i, first in enumerate(humans):
            second = next((
                candidate for candidate in humans[i + 1:]
                if candidate["reviewer_id"] != first["reviewer_id"]
                and candidate["candidate_implementation_sha"] == first["candidate_implementation_sha"]
            ), None)
            if second is not None:
                pair = compare_pair(first, second)
                # An empty/nonoverlapping set cannot establish agreement.
                if pair["common_propositions"] > 0:
                    pairs.append(pair)
                break

    declared_human_ids = {item.get("reviewer_id") for item in reviews
                          if item.get("reviewer_class") == "human-independent"}
    eligible_human_ids = {item["reviewer_id"] for item in eligible}
    ai_rehearsal = {item["reviewer_id"] for item in reviews
                    if item.get("reviewer_class") == "ai-assisted-rehearsal"}
    return {
        "schema": "rahp-policy-graduation-metrics/v1",
        "review_count": len(reviews),
        "corpus_item_count": len(by_corpus),
        "independent_human_reviewer_count": len(declared_human_ids),
        "documentarily_eligible_human_reviewer_count": len(eligible_human_ids),
        "ineligible_declared_human_review_count": sum(
            item.get("reviewer_class") == "human-independent"
            and not eligible_independent_record(item) for item in reviews
        ),
        "ai_rehearsal_reviewer_count": len(ai_rehearsal),
        "human_pair_comparisons": pairs,
        "reviews": summaries,
        # This is a documentary gate only, not authentication, human approval,
        # or authorization to graduate/merge the research capability.
        "graduation_human_review_gate_satisfied": len(pairs) >= 1,
        "human_identity_and_independence_verified": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute policy graduation-study metrics")
    parser.add_argument("reviews", nargs="+", type=Path)
    args = parser.parse_args()
    result = study_metrics([load_review(path) for path in args.reviews])
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
