from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from dtg_portfolio_routing import load_yaml, route_findings  # noqa: E402


POLICY = load_yaml(ROOT / "instances" / "dtg" / "assurance-routing.yaml")
NORMALIZATION = load_yaml(ROOT / "instances" / "dtg" / "finding-normalization.yaml")


def finding(finding_id: str, title: str) -> dict[str, object]:
    return {
        "finding_id": finding_id,
        "fingerprint": finding_id + "-fingerprint",
        "kind": "material_cross_reference",
        "severity": "high",
        "materiality": "high",
        "urgency": "elevated",
        "assurance_impact": "potentially-breaking",
        "repository": "trustoverip/dtgwg-vsc-registry",
        "title": title,
        "state": "open",
        "review_status": "unreviewed",
        "related_repositories": [],
    }


def route_one(title: str) -> dict[str, object]:
    routed = route_findings([finding("vsc-fixture", title)], POLICY, NORMALIZATION)
    assert len(routed) == 1
    return routed[0]


def test_routine_vsc_registry_publication_is_no_action() -> None:
    routed = route_one("docs(registry): publish the refreshed context registry index")
    assert routed["rule_id"] == "vsc-registry-routine-publication"
    assert routed["outcome"] == "no-action"


def test_vsc_context_authority_semantics_retain_durable_owner() -> None:
    routed = route_one("Add the DTG credential context as v1, and the rules for contexts")
    assert routed["rule_id"] == "credential-registry-context-convergence"
    assert routed["outcome"] == "covered"
    assert routed["covered_by"] == "rahp-toolkit#474"


def test_unknown_material_vsc_semantics_remain_unmapped() -> None:
    routed = route_one("feat!: redefine an assurance-significant registry behavior nobody has classified")
    assert routed["rule_id"] == "fallback"
    assert routed["outcome"] == "UNMAPPED"
    assert routed["normalized_finding"]["normalization"]["status"] == "unmapped"
