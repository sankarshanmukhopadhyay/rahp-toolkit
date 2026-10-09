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
