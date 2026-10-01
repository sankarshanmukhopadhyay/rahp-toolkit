#!/usr/bin/env python3
"""ODRL 2.2 alignment helpers for experimental RAHP policy research (#662).

This module does not make ODRL authoritative for RAHP assurance semantics.
It provides:
1. an explicit alignment matrix for the local proposition vocabulary;
2. loss-aware projection metadata for reviewed natural-language propositions; and
3. a deterministic control-path parser for bounded ODRL 2.2 JSON-LD policies.

Generated ODRL alignment/projection records are derived semantic artifacts.
They are not legal conclusions, runtime evidence, or terminal assurance.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

ALIGNMENT_SCHEMA = "rahp-policy-odrl-alignment/v1"
ODRL_NATIVE_SCHEMA = "rahp-policy-odrl-native/v1"
ODRL_CONTEXT = "http://www.w3.org/ns/odrl.jsonld"

ALIGNMENT_MATRIX: dict[str, dict[str, Any]] = {
    "permission": {
        "status": "direct",
        "odrl_term": "Permission",
        "note": "Rule polarity aligns, but a usable ODRL rule still requires explicit action/target and applicable party/constraint semantics.",
    },
    "prohibition": {
        "status": "direct",
        "odrl_term": "Prohibition",
        "note": "Rule polarity aligns, but a usable ODRL rule still requires explicit action/target and applicable party/constraint semantics.",
    },
    "obligation": {
        "status": "partial",
        "odrl_term": "Duty",
        "note": "ODRL Duty expresses an action that must be performed; generic natural-language obligations are not assumed to be losslessly equivalent.",
    },
    "condition": {
        "status": "partial",
        "odrl_term": "Constraint",
        "note": "ODRL Constraint has structured operands/operators; generic textual conditions are not projected without those semantics.",
    },
    "remedy": {
        "status": "partial",
        "odrl_term": "remedy/consequence",
        "note": "ODRL supports remedy/consequence relations around Duties/Prohibitions, but RAHP remedy language may describe broader redress.",
    },
    "discretion": {
        "status": "outside-odrl",
        "odrl_term": None,
        "note": "RAHP uses discretion as an analytical/governance proposition type; it is not forced into an ODRL Core rule class.",
    },
    "exception": {
        "status": "partial",
        "odrl_term": "Constraint/LogicalConstraint",
        "note": "Some exceptions can be structured as ODRL constraints, but generic exceptions are not assumed equivalent.",
    },
    "representation": {
        "status": "outside-odrl",
        "odrl_term": None,
        "note": "A generic source representation is an ingestion fallback, not an ODRL policy rule.",
    },
    "retention": {
        "status": "profile-candidate",
        "odrl_term": "Action/Constraint via profile",
        "note": "Retention semantics may be expressible through actions/constraints or a profile, but no RAHP ODRL Profile is authorized.",
    },
    "disclosure": {
        "status": "profile-candidate",
        "odrl_term": "Action/Party/Asset via profile",
        "note": "Disclosure may be expressible using ODRL actions and party/asset semantics, but equivalence depends on structured facets.",
    },
    "termination": {
        "status": "profile-candidate",
        "odrl_term": "Action via profile",
        "note": "Termination/suspension may be represented as actions in a domain profile; this research does not define such a profile.",
    },
    "delegation": {
        "status": "profile-candidate",
        "odrl_term": "Party function/Action via profile",
        "note": "Delegation and authority semantics exceed a simple Core mapping and require a separately justified profile or external model.",
    },
}

_ODRL_RULE_KEYS = {
    "permission": "Permission",
    "prohibition": "Prohibition",
    "obligation": "Duty",
}


def _digest_json(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def alignment_matrix() -> dict[str, Any]:
    return {
        "schema": ALIGNMENT_SCHEMA,
        "odrl_version": "2.2",
        "odrl_context": ODRL_CONTEXT,
        "profile_authorized": False,
        "mappings": ALIGNMENT_MATRIX,
    }


def project_reviewed_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Report ODRL projection readiness without inventing missing semantics.

    Reviewed RAHP records currently carry textual propositions and coarse local
    types. They generally do not carry reviewed ODRL action/target/party facets.
    This function therefore emits a loss-aware readiness report rather than
    fabricating an ODRL Policy.
    """
    projections: list[dict[str, Any]] = []
    for record in records:
        ptype = record.get("type")
        mapping = ALIGNMENT_MATRIX.get(
            ptype,
            {
                "status": "outside-odrl",
                "odrl_term": None,
                "note": "No reviewed ODRL alignment exists for this proposition type.",
            },
        )
        state = "not-applicable"
        missing: list[str] = []
        if ptype in {"permission", "prohibition", "obligation"}:
            state = "insufficient-structure"
            missing = ["action", "target"]
        elif mapping["status"] in {"partial", "profile-candidate"}:
            state = "semantic-review-required"

        projections.append(
            {
                "proposition_id": record.get("id"),
                "source_proposition_ids": list(record.get("source_proposition_ids") or []),
                "rahp_type": ptype,
                "alignment_status": mapping["status"],
                "odrl_term": mapping["odrl_term"],
                "projection_state": state,
                "missing_structured_semantics": missing,
                "semantic_loss": state != "not-applicable",
                "note": mapping["note"],
            }
        )

    return {
        "schema": "rahp-policy-odrl-projection-readiness/v1",
        "derived": True,
        "source_authority_replaced": False,
        "odrl_profile_defined": False,
        "records": projections,
    }


def ingest_odrl_policy(document: dict[str, Any], *, source_uri: str, source_version: str) -> dict[str, Any]:
    """Parse a bounded ODRL 2.2 JSON-LD policy as a deterministic control fixture.

    This is intentionally not a complete ODRL validator/evaluator. It accepts a
    small conformance-oriented subset sufficient to separate machine-readable
    policy semantics from natural-language extraction uncertainty.
    """
    if not isinstance(document, dict):
        raise ValueError("ODRL source must be a JSON object")
    if not source_uri or not source_version:
        raise ValueError("source_uri and source_version are required")
    context = document.get("@context")
    if context != ODRL_CONTEXT:
        raise ValueError(f"ODRL control source must use @context={ODRL_CONTEXT}")
    uid = document.get("uid")
    if not isinstance(uid, str) or not uid:
        raise ValueError("ODRL policy uid is required")

    rules: list[dict[str, Any]] = []
    for key, odrl_class in _ODRL_RULE_KEYS.items():
        raw = document.get(key) or []
        if isinstance(raw, dict):
            raw = [raw]
        if not isinstance(raw, list):
            raise ValueError(f"ODRL {key} must be an object or list")
        for index, rule in enumerate(raw):
            if not isinstance(rule, dict):
                raise ValueError(f"ODRL {key}[{index}] must be an object")
            action = rule.get("action")
            target = rule.get("target")
            if not action or not target:
                raise ValueError(f"ODRL {key}[{index}] requires action and target")
            rules.append(
                {
                    "id": f"odrl-{key}-{index + 1}-{_digest_json(rule)[:12]}",
                    "rule_type": key,
                    "odrl_class": odrl_class,
                    "action": action,
                    "target": target,
                    "assigner": rule.get("assigner"),
                    "assignee": rule.get("assignee"),
                    "constraint": rule.get("constraint"),
                    "duty": rule.get("duty"),
                    "source_pointer": f"/{key}/{index}",
                    "source_rule_sha256": _digest_json(rule),
                    "derivation": "direct-machine-policy-statement",
                    "judgment_required": False,
                }
            )

    if not rules:
        raise ValueError("ODRL control source must contain at least one permission, prohibition, or obligation")

    return {
        "schema": ODRL_NATIVE_SCHEMA,
        "experimental": True,
        "terminal_assurance": False,
        "source": {
            "uri": source_uri,
            "version": source_version,
            "sha256": _digest_json(document),
            "policy_uid": uid,
            "odrl_type": document.get("@type", "Set"),
            "profile": document.get("profile"),
            "conflict": document.get("conflict"),
        },
        "semantic_authority": "source-odrl-policy",
        "rules": rules,
        "boundary": {
            "odrl_conformance_implies_rahp_assurance": False,
            "odrl_conformance_implies_legal_validity": False,
            "odrl_evaluation_is_terminal_rahp_assurance": False,
            "rahp_odrl_profile_authorized": False,
        },
    }
