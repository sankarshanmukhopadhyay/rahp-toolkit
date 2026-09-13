#!/usr/bin/env python3
"""Issue and reconcile external evidence obligations for DRARM propositions."""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
from typing import Any

ASSURANCE_LEVELS = {"DR-A1": 1, "DR-A2": 2, "DR-A3": 3, "DR-A4": 4, "DR-A5": 5}
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")


def _binding(proposition: dict[str, Any]) -> dict[str, Any]:
    source = proposition.get("source")
    target = proposition.get("target")
    if not isinstance(source, dict) or source.get("model") != "DRARM" or not source.get("rule"):
        raise ValueError("evidence obligation requires a source-preserving DRARM proposition")
    if not isinstance(target, dict) or not target.get("revision"):
        raise ValueError("evidence obligation requires a pinned target revision")
    return {
        "model": "DRARM",
        "rule": source["rule"],
        "finding_id": source.get("finding_id"),
        "repository": target.get("repository"),
        "revision": target["revision"],
    }


def _obligation_id(binding: dict[str, Any], evidence_class: str, required_level: str) -> str:
    canonical = json.dumps(
        {"binding": binding, "evidence_class": evidence_class, "required_level": required_level},
        sort_keys=True,
        separators=(",", ":"),
    )
    return "DR-EV-" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:20]


def make_evidence_obligations(
    proposition: dict[str, Any],
    required_level: str,
) -> list[dict[str, Any]]:
    if required_level not in ASSURANCE_LEVELS:
        raise ValueError(f"unknown DRARM assurance level: {required_level}")
    if proposition.get("state") != "evidence-required":
        raise ValueError("runtime evidence obligations require an evidence-required proposition")
    required = proposition.get("required_evidence") or []
    if not isinstance(required, list) or not required or not all(isinstance(item, str) and item for item in required):
        raise ValueError("proposition requires at least one named evidence class")
    binding = _binding(proposition)
    return [
        {
            "schema": "rahp-resilience-evidence-obligation/v1",
            "id": _obligation_id(binding, evidence_class, required_level),
            "type": "resilience-runtime-evidence",
            "proposition": binding,
            "evidence_class": evidence_class,
            "required_assurance_level": required_level,
            "state": "unsatisfied",
        }
        for evidence_class in required
    ]


def _validate_evidence(evidence: dict[str, Any]) -> None:
    if not isinstance(evidence, dict):
        raise ValueError("evidence return must be an object")
    required = (
        "obligation_id", "source_model", "source_rule", "target_revision",
        "evidence_class", "assurance_level", "producer", "uri", "sha256",
        "collected_at", "sensitivity",
    )
    missing = [key for key in required if not evidence.get(key)]
    if missing:
        raise ValueError("evidence return missing: " + ", ".join(missing))
    if evidence["assurance_level"] not in ASSURANCE_LEVELS:
        raise ValueError("evidence return has unknown DRARM assurance level")
    if not SHA256_RE.fullmatch(str(evidence["sha256"])):
        raise ValueError("evidence return sha256 must be a 64-character hexadecimal digest")


def reconcile_evidence(
    obligation: dict[str, Any],
    evidence: dict[str, Any] | None,
) -> dict[str, Any]:
    """Pure, deterministic reconciliation; unresolved evidence never becomes PASS."""
    result = dict(obligation)
    if evidence is None:
        result.update(state="unsatisfied", reason="required runtime evidence has not been supplied")
        return result
    _validate_evidence(evidence)
    binding = obligation.get("proposition") or {}
    checks = {
        "obligation": evidence.get("obligation_id") == obligation.get("id"),
        "model": evidence.get("source_model") == binding.get("model"),
        "rule": evidence.get("source_rule") == binding.get("rule"),
        "revision": evidence.get("target_revision") == binding.get("revision"),
        "class": evidence.get("evidence_class") == obligation.get("evidence_class"),
    }
    failed = [name for name, ok in checks.items() if not ok]
    if failed:
        result.update(state="unsatisfied", reason="evidence binding mismatch: " + ", ".join(failed))
        return result
    achieved = ASSURANCE_LEVELS[evidence["assurance_level"]]
    required = ASSURANCE_LEVELS[obligation["required_assurance_level"]]
    if achieved < required:
        result.update(
            state="unsatisfied",
            reason=f"evidence assurance level {evidence['assurance_level']} is below {obligation['required_assurance_level']}",
        )
        return result
    result.update(
        state="satisfied",
        reason="pinned external evidence satisfies the obligation",
        evidence={
            "producer": evidence["producer"],
            "uri": evidence["uri"],
            "sha256": evidence["sha256"].lower(),
            "collected_at": evidence["collected_at"],
            "sensitivity": evidence["sensitivity"],
            "assurance_level": evidence["assurance_level"],
        },
    )
    return result


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("proposition", type=pathlib.Path)
    ap.add_argument("--required-level", required=True, choices=sorted(ASSURANCE_LEVELS))
    ap.add_argument("--output", type=pathlib.Path)
    args = ap.parse_args()
    proposition = json.loads(args.proposition.read_text(encoding="utf-8"))
    obligations = make_evidence_obligations(proposition, args.required_level)
    rendered = json.dumps({"obligations": obligations}, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
