from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from dtg_portfolio_routing import combined_event, load_yaml, route_findings  # noqa: E402


POLICY = load_yaml(ROOT / "instances" / "dtg" / "assurance-routing.yaml")
NORMALIZATION = load_yaml(ROOT / "instances" / "dtg" / "finding-normalization.yaml")


def finding(finding_id: str, repository: str, title: str) -> dict[str, object]:
    return {
        "finding_id": finding_id,
        "fingerprint": finding_id + "-fingerprint",
        "kind": "material_cross_reference",
        "severity": "high",
        "materiality": "high",
        "urgency": "elevated",
        "assurance_impact": "potentially-breaking",
        "repository": repository,
        "title": title,
        "state": "open",
        "review_status": "unreviewed",
        "related_repositories": [],
    }


def test_controller_629_known_semantics_no_longer_fall_back_to_unmapped() -> None:
    fixtures = [
        (
            finding("01c0b3e160885ecb9f81", "OpenVTC/dtg-credentials", "feat!: a VAC is not a bearer credential; remove `audience`"),
            "vac-presenter-binding",
            "combined",
        ),
        (
            finding("034f21a5e8d61d059257", "OpenVTC/dtg-credentials", "feat: set `credentialStatus` on a credential being built; `PartialEq` on the type"),
            "credential-status-lifecycle",
            "combined",
        ),
        (
            finding("2a53f45ce2cc63e5bd7f", "OpenVTC/dtg-credentials", "ci: pin actions to commit SHAs, scope the publish token, add Dependabot"),
            "ci-supply-chain-hardening",
            "no-action",
        ),
        (
            finding("5e066277145877762c4a", "OpenVTC/openvtc", "docs(design): vetted admission via peer identity vetting"),
            "vetting-admission-composition",
            "combined",
        ),
        (
            finding("9ff50bc250c0f83b4002", "OpenVTC/openvtc", "feat(vetting): guided join, vetter directory and profile, QR tickets, grant checks, resend and branding"),
            "vetting-admission-composition",
            "combined",
        ),
        (
            finding("05e4c8568c99a6a4e45b", "OpenVTC/verifiable-trust-infrastructure", "feat(vta): a key can be marked as never leaving the VTA"),
            "key-custody-service-authority",
            "combined",
        ),
        (
            finding("19b572ed1989920f312a", "OpenVTC/verifiable-trust-infrastructure", "feat(deps)!: dtg-credentials 0.6 -> 0.9.1"),
            "dependency-version-covered",
            "covered",
        ),
        (
            finding("22075d14e2d888f29014", "OpenVTC/verifiable-trust-infrastructure", "feat(vta): a service can fetch the keys of the DID it operates"),
            "key-custody-service-authority",
            "combined",
        ),
        (
            finding("e35dba725a56eba1af94", "OpenVTC/verifiable-trust-infrastructure", "feat(keys): export one key by name, and retire seeds/export-mnemonic"),
            "key-custody-service-authority",
            "combined",
        ),
        (
            finding("f3b2d9eb826c61626f1a", "OpenVTC/verifiable-trust-infrastructure", "feat(vtc)!: vetter registry, grant resend, community branding and automatic vetter grants"),
            "vetting-admission-composition",
            "combined",
        ),
        (
            finding("283e2b3aa4b8fc0d13ae", "OpenVTC/vta-browser-plugin", "fix(did): refuse to resolve a did:webvh hosted on a local-only name or non-public address"),
            "defensive-did-resolution",
            "no-action",
        ),
        (
            finding("e1da90feba8c351056cc", "trustoverip/dtgwg-cred-spec", "docs: add an informative identity-vetting profile of the VEC"),
            "vec-vetting-profile-evidence",
            "covered",
        ),
    ]

    routed = route_findings([item for item, _, _ in fixtures], POLICY, NORMALIZATION)
    actual = {item["finding"]["finding_id"]: (item["rule_id"], item["outcome"]) for item in routed}

    assert len(actual) == len(fixtures)
    for item, expected_rule, expected_outcome in fixtures:
        assert actual[item["finding_id"]] == (expected_rule, expected_outcome)
        assert actual[item["finding_id"]][1] != "UNMAPPED"


def test_unknown_material_semantics_still_fail_safe_to_unmapped() -> None:
    unknown = finding(
        "unknown-semantic-family",
        "example/new-dtg-component",
        "feat!: introduce an assurance-significant semantic nobody has classified",
    )
    routed = route_findings([unknown], POLICY, NORMALIZATION)
    assert len(routed) == 1
    assert routed[0]["rule_id"] == "fallback"
    assert routed[0]["outcome"] == "UNMAPPED"
    assert routed[0]["normalized_finding"]["normalization"]["status"] == "unmapped"


def test_vetting_combined_review_preserves_canonical_dpip_promotion_instruction() -> None:
    item = finding(
        "vetting-example",
        "OpenVTC/openvtc",
        "feat(vetting): guided join and vetter registry",
    )
    routed = route_findings([item], POLICY, NORMALIZATION)
    assert routed[0]["rule_id"] == "vetting-admission-composition"
    body = combined_event("vetting-admission-composition", routed, "2026-09-12")["body"]
    assert "canonical DPIP handoff" in body
