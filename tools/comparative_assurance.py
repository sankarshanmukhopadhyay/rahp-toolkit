"""Deterministic, conservative finding comparison for RAHP digests.

The differ establishes identity only through profile-declared stable keys. It
does not infer identity from titles and does not convert an unmatched record
into a resolved or introduced finding without explicit lineage evidence.
"""

from __future__ import annotations

from collections import defaultdict
from copy import deepcopy
import hashlib
import json
from typing import Any


DEFAULT_MATCH_RULES = [
    ["finding_id"],
    ["criteria_id", "affected_components", "claim_id"],
]

ALLOWED_MATCH_FIELDS = {
    "finding_id",
    "criteria_id",
    "affected_components",
    "claim_id",
}

DEFAULT_SCOPE_MATERIALITY = {
    "directly_assessed_change": True,
    "supporting_dependency_change": False,
    "dependency_treatment_change": True,
    "excluded_change": False,
    "coverage_weakening": True,
}

DEFAULT_COVERAGE_ORDER = ["insufficient", "partial", "bounded", "complete"]

COMPARATIVE_JUDGMENTS = {
    "materially_improved",
    "improved",
    "mixed",
    "no_material_change",
    "regressed",
    "materially_regressed",
    "indeterminate",
    "not_comparable",
}

CONFIDENCE_ORDER = ["insufficient", "low", "moderate", "high"]

RELEASE_DISPOSITIONS = {
    "acceptable",
    "conditionally_acceptable",
    "not_acceptable",
    "human_judgment_required",
    "indeterminate",
    "not_applicable",
}


def _canonical(value: Any) -> Any:
    if isinstance(value, list):
        return sorted((_canonical(item) for item in value), key=lambda item: json.dumps(item, sort_keys=True))
    if isinstance(value, dict):
        return {key: _canonical(value[key]) for key in sorted(value)}
    return value


def _validate_rules(rules: list[list[str]]) -> None:
    if not rules or any(not rule for rule in rules):
        raise ValueError("matching_rules must contain at least one non-empty rule")
    for rule in rules:
        unknown = set(rule) - ALLOWED_MATCH_FIELDS
        if unknown:
            raise ValueError(f"unsupported matching field(s): {', '.join(sorted(unknown))}")
        if "title" in rule:
            raise ValueError("human-readable titles cannot establish finding identity")


def _match_key(finding: dict[str, Any], rule: list[str]) -> str | None:
    values = []
    for field in rule:
        value = finding.get(field)
        if value is None or value == "" or value == []:
            return None
        values.append([field, _canonical(value)])
    return json.dumps(values, sort_keys=True, separators=(",", ":"))


def _evidence_refs(finding: dict[str, Any]) -> list[str]:
    return sorted(set(finding.get("evidence_refs") or []))


def _finding_ref(finding: dict[str, Any]) -> dict[str, Any]:
    return {
        "finding_id": finding["finding_id"],
        "evidence_refs": _evidence_refs(finding),
    }


def _evidence_change(baseline: dict[str, Any], candidate: dict[str, Any]) -> tuple[str, list[str]]:
    before = set(_evidence_refs(baseline))
    after = set(_evidence_refs(candidate))
    if before == after:
        return ("preserved" if before else "none"), []
    if before < after:
        return "strengthened", []
    if after < before:
        return "weakened", []
    return "not_comparable", ["Evidence references changed in both directions; strength cannot be inferred."]


def _delta_id(baseline_id: str | None, candidate_id: str | None, match_basis: str) -> str:
    material = json.dumps(
        {"baseline": baseline_id, "candidate": candidate_id, "match_basis": match_basis},
        sort_keys=True,
        separators=(",", ":"),
    )
    return f"delta-{hashlib.sha256(material.encode('utf-8')).hexdigest()[:16]}"


def _matched_state(
    baseline: dict[str, Any],
    candidate: dict[str, Any],
    profile: dict[str, Any],
    evidence_change: str,
) -> str:
    before = baseline.get("disposition")
    after = candidate.get("disposition")
    resolved = set(profile.get("resolved_dispositions") or ["resolved"])
    not_applicable = set(profile.get("not_applicable_dispositions") or ["not_applicable"])
    not_reassessed = set(profile.get("not_reassessed_dispositions") or ["not_reassessed"])

    if after in not_reassessed:
        return "not_reassessed"
    if after in not_applicable and before not in not_applicable:
        return "no_longer_applicable"
    if before in resolved and after not in resolved:
        return "reopened"
    if before not in resolved and after in resolved:
        return "resolved"
    if before != after:
        return "changed"
    if evidence_change == "strengthened":
        return "evidence_strengthened"
    if evidence_change == "weakened":
        return "evidence_weakened"
    if evidence_change == "not_comparable":
        return "changed"
    return "unchanged"


def _matched_delta(
    baseline: dict[str, Any],
    candidate: dict[str, Any],
    match_basis: str,
    profile: dict[str, Any],
) -> dict[str, Any]:
    evidence_change, limitations = _evidence_change(baseline, candidate)
    return {
        "delta_id": _delta_id(baseline["finding_id"], candidate["finding_id"], match_basis),
        "state": _matched_state(baseline, candidate, profile, evidence_change),
        "match_basis": match_basis,
        "baseline": _finding_ref(baseline),
        "candidate": _finding_ref(candidate),
        "disposition_changed": baseline.get("disposition") != candidate.get("disposition"),
        "evidence_change": evidence_change,
        "limitations": limitations,
    }


def _unmatched_delta(
    finding: dict[str, Any],
    side: str,
    limitations: list[str],
) -> dict[str, Any]:
    explicit_introduction = side == "candidate" and finding.get("lineage_state") == "introduced"
    baseline = _finding_ref(finding) if side == "baseline" else None
    candidate = _finding_ref(finding) if side == "candidate" else None
    match_basis = "explicit-lineage:introduced" if explicit_introduction else "unmatched"
    return {
        "delta_id": _delta_id(
            finding["finding_id"] if side == "baseline" else None,
            finding["finding_id"] if side == "candidate" else None,
            match_basis,
        ),
        "state": "introduced" if explicit_introduction else "unmatched",
        "match_basis": match_basis,
        "baseline": baseline,
        "candidate": candidate,
        "disposition_changed": False,
        "evidence_change": "none",
        "limitations": limitations,
    }


def compare_findings(
    baseline_findings: list[dict[str, Any]],
    candidate_findings: list[dict[str, Any]],
    profile: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Return schema-shaped finding deltas in deterministic order.

    Rules are evaluated in order. A rule establishes a match only where its
    canonical key identifies exactly one still-unmatched record on each side.
    Ambiguous groups remain unmatched and retain an explicit limitation.
    """

    profile = deepcopy(profile or {})
    rules = profile.get("matching_rules") or DEFAULT_MATCH_RULES
    _validate_rules(rules)

    for collection_name, findings in (("baseline", baseline_findings), ("candidate", candidate_findings)):
        ids = [finding.get("finding_id") for finding in findings]
        if any(not finding_id for finding_id in ids):
            raise ValueError(f"every {collection_name} finding requires finding_id")
        if len(ids) != len(set(ids)):
            raise ValueError(f"duplicate finding_id in {collection_name} findings")

    baseline = {finding["finding_id"]: deepcopy(finding) for finding in baseline_findings}
    candidate = {finding["finding_id"]: deepcopy(finding) for finding in candidate_findings}
    unmatched_baseline = set(baseline)
    unmatched_candidate = set(candidate)
    matches: list[tuple[str, str, str]] = []
    ambiguity: dict[tuple[str, str], set[str]] = defaultdict(set)

    for rule in rules:
        basis = "profile-key:" + "+".join(rule)
        left: dict[str, list[str]] = defaultdict(list)
        right: dict[str, list[str]] = defaultdict(list)
        for finding_id in sorted(unmatched_baseline):
            key = _match_key(baseline[finding_id], rule)
            if key is not None:
                left[key].append(finding_id)
        for finding_id in sorted(unmatched_candidate):
            key = _match_key(candidate[finding_id], rule)
            if key is not None:
                right[key].append(finding_id)

        for key in sorted(set(left) & set(right)):
            if len(left[key]) == 1 and len(right[key]) == 1:
                baseline_id, candidate_id = left[key][0], right[key][0]
                matches.append((baseline_id, candidate_id, basis))
                unmatched_baseline.remove(baseline_id)
                unmatched_candidate.remove(candidate_id)
            else:
                message = f"Ambiguous {basis} matched {len(left[key])} baseline and {len(right[key])} candidate findings."
                for finding_id in left[key]:
                    ambiguity[("baseline", finding_id)].add(message)
                for finding_id in right[key]:
                    ambiguity[("candidate", finding_id)].add(message)

    deltas = [
        _matched_delta(baseline[left_id], candidate[right_id], basis, profile)
        for left_id, right_id, basis in matches
    ]
    for finding_id in sorted(unmatched_baseline):
        limitations = sorted(ambiguity.get(("baseline", finding_id), set()))
        limitations.append("No unique candidate match was established; resolution is not inferred.")
        deltas.append(_unmatched_delta(baseline[finding_id], "baseline", limitations))
    for finding_id in sorted(unmatched_candidate):
        limitations = sorted(ambiguity.get(("candidate", finding_id), set()))
        if candidate[finding_id].get("lineage_state") != "introduced":
            limitations.append("No unique baseline match was established; introduction is not inferred.")
        deltas.append(_unmatched_delta(candidate[finding_id], "candidate", limitations))

    return sorted(deltas, key=lambda delta: delta["delta_id"])


def _index_components(scope: dict[str, Any], field: str) -> dict[str, dict[str, Any]]:
    records = scope.get(field) or []
    result: dict[str, dict[str, Any]] = {}
    for record in records:
        component_id = record.get("component_id")
        if not component_id:
            raise ValueError(f"every {field} record requires component_id")
        if component_id in result:
            raise ValueError(f"duplicate component_id {component_id!r} in {field}")
        result[component_id] = record
    return result


def _component_changes(
    baseline: dict[str, dict[str, Any]],
    candidate: dict[str, dict[str, Any]],
    compared_fields: list[str],
) -> dict[str, list[str]]:
    shared = set(baseline) & set(candidate)
    return {
        "added": sorted(set(candidate) - set(baseline)),
        "removed": sorted(set(baseline) - set(candidate)),
        "changed": sorted(
            component_id
            for component_id in shared
            if any(
                _canonical(baseline[component_id].get(field))
                != _canonical(candidate[component_id].get(field))
                for field in compared_fields
            )
        ),
    }


def _coverage_change(baseline: str, candidate: str, order: list[str]) -> str:
    if baseline == candidate:
        return "preserved"
    if baseline not in order or candidate not in order or len(order) != len(set(order)):
        return "not_comparable"
    return "strengthened" if order.index(candidate) > order.index(baseline) else "weakened"


def compare_scope(
    baseline_scope: dict[str, Any],
    candidate_scope: dict[str, Any],
    profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Compare declared assessment boundaries without inferring assurance change.

    Component identity is the stable ``component_id``. A broader candidate
    boundary is reported as scope expansion and newly admitted work, not as an
    assurance regression. Materiality remains profile-declared.
    """

    profile = deepcopy(profile or {})
    materiality = {**DEFAULT_SCOPE_MATERIALITY, **(profile.get("scope_materiality") or {})}
    unknown_materiality = set(materiality) - set(DEFAULT_SCOPE_MATERIALITY)
    if unknown_materiality:
        raise ValueError(f"unsupported scope materiality rule(s): {', '.join(sorted(unknown_materiality))}")
    if any(not isinstance(value, bool) for value in materiality.values()):
        raise ValueError("scope materiality rules must be boolean")

    baseline_direct = _index_components(baseline_scope, "directly_assessed")
    candidate_direct = _index_components(candidate_scope, "directly_assessed")
    baseline_dependencies = _index_components(baseline_scope, "supporting_dependencies")
    candidate_dependencies = _index_components(candidate_scope, "supporting_dependencies")
    baseline_excluded = _index_components(baseline_scope, "excluded")
    candidate_excluded = _index_components(candidate_scope, "excluded")

    direct = _component_changes(baseline_direct, candidate_direct, ["resolved_ref", "reason"])
    dependencies = _component_changes(
        baseline_dependencies,
        candidate_dependencies,
        ["resolved_ref", "treatment", "independent_assessment_ref", "limitations"],
    )
    excluded = _component_changes(baseline_excluded, candidate_excluded, ["reason"])

    baseline_coverage = baseline_scope.get("coverage_state")
    candidate_coverage = candidate_scope.get("coverage_state")
    coverage_order = profile.get("coverage_order") or DEFAULT_COVERAGE_ORDER
    coverage_change = _coverage_change(baseline_coverage, candidate_coverage, coverage_order)

    added = bool(direct["added"] or dependencies["added"] or excluded["added"])
    removed = bool(direct["removed"] or dependencies["removed"] or excluded["removed"])
    changed = bool(direct["changed"] or dependencies["changed"] or excluded["changed"])
    if not (added or removed or changed):
        status = "equivalent"
    elif added and not removed and not changed:
        status = "expanded"
    elif removed and not added and not changed:
        status = "contracted"
    else:
        status = "changed"

    dependency_treatment_changed = any(
        baseline_dependencies[component_id].get("treatment")
        != candidate_dependencies[component_id].get("treatment")
        for component_id in set(baseline_dependencies) & set(candidate_dependencies)
    )
    material_change = any([
        materiality["directly_assessed_change"] and any(direct.values()),
        materiality["supporting_dependency_change"] and bool(dependencies["added"] or dependencies["removed"]),
        materiality["dependency_treatment_change"] and dependency_treatment_changed,
        materiality["excluded_change"] and any(excluded.values()),
        materiality["coverage_weakening"] and coverage_change == "weakened",
    ])

    limitations = sorted(set((baseline_scope.get("limitations") or []) + (candidate_scope.get("limitations") or [])))
    if status == "expanded":
        limitations.append("Newly admitted components require assessment; scope expansion is not an assurance regression.")
    if coverage_change == "not_comparable":
        limitations.append("Coverage states cannot be ranked under the declared comparison profile.")

    return {
        "status": status,
        "material_change": material_change,
        "directly_assessed": direct,
        "supporting_dependencies": dependencies,
        "excluded": excluded,
        "coverage": {
            "baseline": baseline_coverage,
            "candidate": candidate_coverage,
            "change": coverage_change,
        },
        "newly_admitted_components": sorted(
            set(direct["added"]) | set(dependencies["added"])
        ),
        "limitations": sorted(set(limitations)),
    }


def _validate_dimension_results(dimensions: list[dict[str, Any]], profile: dict[str, Any]) -> dict[str, dict[str, Any]]:
    declared = profile.get("dimensions")
    if not declared or not isinstance(declared, list):
        raise ValueError("comparison profile must declare dimensions")
    if len(declared) != len(set(declared)):
        raise ValueError("comparison profile dimensions must be unique")
    results: dict[str, dict[str, Any]] = {}
    for dimension in dimensions:
        dimension_id = dimension.get("dimension_id")
        if not dimension_id:
            raise ValueError("every dimension result requires dimension_id")
        if dimension_id in results:
            raise ValueError(f"duplicate dimension result {dimension_id!r}")
        if dimension_id not in declared:
            raise ValueError(f"dimension {dimension_id!r} is not declared by the comparison profile")
        if dimension.get("judgment") not in COMPARATIVE_JUDGMENTS:
            raise ValueError(f"unsupported comparative judgment for {dimension_id!r}")
        if dimension.get("confidence") not in CONFIDENCE_ORDER:
            raise ValueError(f"unsupported confidence for {dimension_id!r}")
        results[dimension_id] = dimension
    return results


def _overall_judgment(judgments: list[str], profile: dict[str, Any]) -> str:
    blocking = set(profile.get("blocking_judgments") or ["materially_regressed"])
    if any(judgment in blocking for judgment in judgments):
        return "materially_regressed"
    improvement = any(judgment in {"improved", "materially_improved"} for judgment in judgments)
    regression = any(judgment in {"regressed", "materially_regressed"} for judgment in judgments)
    if improvement and regression:
        return "mixed"
    if any(judgment == "materially_regressed" for judgment in judgments):
        return "materially_regressed"
    if regression:
        return "regressed"
    if any(judgment == "mixed" for judgment in judgments):
        return "mixed"
    if any(judgment == "indeterminate" for judgment in judgments):
        return "indeterminate"
    if any(judgment == "not_comparable" for judgment in judgments):
        return "indeterminate"
    if any(judgment == "materially_improved" for judgment in judgments):
        return "materially_improved"
    if improvement:
        return "improved"
    if judgments and all(judgment == "no_material_change" for judgment in judgments):
        return "no_material_change"
    return "indeterminate"


def aggregate_judgment(
    dimensions: list[dict[str, Any]],
    comparability: dict[str, Any],
    scope_delta: dict[str, Any],
    profile: dict[str, Any],
    candidate_release_disposition: str | None = None,
) -> dict[str, Any]:
    """Execute declared comparison policy without numerical compensation.

    Dimension judgments are inputs produced by profile-specific evaluators. The
    engine checks the profile's coverage, evidence and blocking gates, then
    combines the bounded states through a conservative precedence lattice.
    Release disposition remains independent and must come from candidate
    evidence or an explicit profile blocking rule.
    """

    results = _validate_dimension_results(dimensions, profile)
    required = profile.get("required_dimensions") or profile.get("dimensions")
    unknown_required = set(required) - set(profile["dimensions"])
    if unknown_required:
        raise ValueError(f"required dimension(s) are undeclared: {', '.join(sorted(unknown_required))}")

    evidence_refs = sorted({ref for item in dimensions for ref in (item.get("evidence_refs") or [])})
    counterevidence_refs = sorted({ref for item in dimensions for ref in (item.get("counterevidence_refs") or [])})
    limitations = sorted({text for item in dimensions for text in (item.get("unresolved_limitations") or [])})
    reasons: list[str] = []

    if comparability.get("status") == "not_comparable":
        reasons.append("Top-level assessment compatibility was not established.")
        return {
            "judgment": "not_comparable",
            "confidence": "insufficient",
            "justification": "The profile forbids an overall comparison because the assessments are not comparable.",
            "evidence_refs": evidence_refs,
            "counterevidence_refs": counterevidence_refs,
            "unresolved_limitations": sorted(set(limitations + reasons + (comparability.get("reasons") or []))),
            "release_disposition": "not_applicable",
            "release_superiority_established": False,
        }

    missing_dimensions = sorted(set(required) - set(results))
    if missing_dimensions:
        reasons.append("Missing required dimension results: " + ", ".join(missing_dimensions))

    require_evidence = set(profile.get("require_evidence_for") or required)
    missing_evidence = sorted(
        dimension_id
        for dimension_id in require_evidence
        if dimension_id not in results or not results[dimension_id].get("evidence_refs")
    )
    if missing_evidence:
        reasons.append("Missing required evidence for: " + ", ".join(missing_evidence))

    coverage_order = profile.get("coverage_order") or DEFAULT_COVERAGE_ORDER
    minimum_coverage = profile.get("minimum_coverage")
    candidate_coverage = (scope_delta.get("coverage") or {}).get("candidate")
    if minimum_coverage:
        if minimum_coverage not in coverage_order or candidate_coverage not in coverage_order:
            reasons.append("Candidate coverage cannot be ranked against the profile minimum.")
        elif coverage_order.index(candidate_coverage) < coverage_order.index(minimum_coverage):
            reasons.append(f"Candidate coverage {candidate_coverage} is below required {minimum_coverage}.")

    if profile.get("counterevidence_blocks") and counterevidence_refs:
        reasons.append("Unresolved counterevidence is blocking under the comparison profile.")

    required_results = [results[dimension_id] for dimension_id in required if dimension_id in results]
    confidence = min(
        (item["confidence"] for item in required_results),
        key=CONFIDENCE_ORDER.index,
        default="insufficient",
    )
    minimum_confidence = profile.get("minimum_confidence")
    if minimum_confidence:
        if minimum_confidence not in CONFIDENCE_ORDER:
            raise ValueError("unsupported profile minimum_confidence")
        if CONFIDENCE_ORDER.index(confidence) < CONFIDENCE_ORDER.index(minimum_confidence):
            reasons.append(f"Overall confidence {confidence} is below required {minimum_confidence}.")

    judgments = [item["judgment"] for item in required_results]
    bounded_judgment = _overall_judgment(judgments, profile)
    blocking_observed = bounded_judgment == "materially_regressed"
    overall = bounded_judgment if blocking_observed else ("indeterminate" if reasons else bounded_judgment)
    if overall == "indeterminate" and not reasons:
        reasons.append("The bounded dimension states do not support a dominant comparative judgment.")

    disposition = candidate_release_disposition or "human_judgment_required"
    if disposition not in RELEASE_DISPOSITIONS:
        raise ValueError("unsupported candidate release disposition")
    blocking_disposition = profile.get("blocking_release_disposition")
    if overall == "materially_regressed" and blocking_disposition:
        if blocking_disposition not in RELEASE_DISPOSITIONS:
            raise ValueError("unsupported blocking_release_disposition")
        disposition = blocking_disposition
    if reasons and not blocking_observed:
        disposition = "indeterminate"

    superiority = bool(
        overall in {"improved", "materially_improved"}
        and profile.get("improvement_establishes_superiority", False)
        and disposition in {"acceptable", "conditionally_acceptable"}
    )
    if blocking_observed and reasons:
        justification = (
            "A profile-defined material regression remains blocking despite additional evidence limitations: "
            + " ".join(reasons)
        )
    elif reasons:
        justification = "Profile gates produced an indeterminate comparison: " + " ".join(reasons)
    else:
        justification = f"Profile-bound precedence produced {overall} from the required dimension judgments without numerical compensation."
    return {
        "judgment": overall,
        "confidence": confidence,
        "justification": justification,
        "evidence_refs": evidence_refs,
        "counterevidence_refs": counterevidence_refs,
        "unresolved_limitations": sorted(set(limitations + reasons)),
        "release_disposition": disposition,
        "release_superiority_established": superiority,
    }
