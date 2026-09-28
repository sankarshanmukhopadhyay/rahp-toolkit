from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from dtg_portfolio_routing import load_yaml, route_findings  # noqa: E402


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


def test_controller_818_disposition_families_route_to_durable_owners() -> None:
    fixtures = [
        (finding("acl-self-grant", "OpenVTC/openvtc", "feat(git-ns): move repo/create to 0.3, name owners, close the self-grant hole"), "acl-non-escalation-elevated-rights"),
        (finding("acl-writer-cover", "trustoverip/dtgwg-vti-spec", "Bound every access control entry by its writer's own, and require full cover to modify one"), "acl-non-escalation-elevated-rights"),
        (finding("key-export-all-transports", "OpenVTC/verifiable-trust-infrastructure", "fix(vta-service)!: apply the key-export and sign capability checks on every transport"), "key-custody-export-rotation"),
        (finding("key-attestation", "trustoverip/dtgwg-trust-tasks-tf", "spec(vta/attestation): mnemonic-export/1.0, sealed, end-to-end or signed at first boot"), "key-custody-export-rotation"),
        (finding("proof-assertion", "OpenVTC/verifiable-trust-infrastructure", "security(vta-service)!: require assertionMethod on an approver's decision"), "proof-purpose-binding"),
        (finding("proof-purpose", "trustoverip/dtgwg-trust-tasks-spec", "feat(spec): check a proof's key against its proofPurpose, and sign for authentication"), "proof-purpose-binding"),
        (finding("passkey-enrol", "OpenVTC/verifiable-trust-infrastructure", "feat(vtc): step-up passkeys a member enrols through an admin's invite"), "step-up-passkey-administration"),
        (finding("passkey-list", "trustoverip/dtgwg-trust-tasks-tf", "feat(auth/passkey): an administrator lists one member's passkeys (admin-list 0.1)"), "step-up-passkey-administration"),
        (finding("backup-transport", "OpenVTC/verifiable-trust-infrastructure", "fix(vtc-service)!: a community backup travels only over DIDComm or TSP"), "trust-tasks-service-backup-transport"),
        (finding("rest-migration", "trustoverip/dtgwg-trust-tasks-tf", "feat(vta): Trust Tasks for the VTA's REST-only health, restore-status, session-revocation and wrapping-key routes"), "trust-tasks-service-backup-transport"),
        (finding("forge-projection", "OpenVTC/verifiable-trust-infrastructure", "feat(vtc-service): re-project git roles, and use the bridge's reported role map"), "forge-projection-provenance"),
        (finding("forge-reseat", "trustoverip/dtgwg-trust-tasks-tf", "feat(git-ns): bridge/job 0.4 and namespace/reseat 0.3, a namespace admin gets no forge role"), "forge-projection-provenance"),
        (finding("outcome-executor", "OpenVTC/vta-browser-plugin", "fix(inbound): believe a task-consent outcome only from the executor it answers"), "task-outcome-executor-binding"),
        (finding("registry-context", "trustoverip/dtgwg-vsc-registry", "Add the DTG credential context as v1, and the rules for contexts"), "credential-registry-context-convergence"),
    ]

    routed = route_findings([item for item, _ in fixtures], POLICY, NORMALIZATION)
    actual = {
        item["finding"]["finding_id"]: (item["rule_id"], item["outcome"], item["decision"].get("covered_by"))
        for item in routed
    }

    assert len(actual) == len(fixtures)
    for item, expected_rule in fixtures:
        rule_id, outcome, covered_by = actual[item["finding_id"]]
        assert rule_id == expected_rule
        assert outcome == "covered"
        assert covered_by
        assert outcome != "UNMAPPED"


def test_controller_818_routing_does_not_weaken_unknown_fail_closed_behavior() -> None:
    unknown = finding(
        "unknown-818-family",
        "example/new-dtg-component",
        "feat!: introduce a materially new authority semantic with no registered proposition",
    )
    routed = route_findings([unknown], POLICY, NORMALIZATION)
    assert len(routed) == 1
    assert routed[0]["rule_id"] == "fallback"
    assert routed[0]["outcome"] == "UNMAPPED"
    assert routed[0]["normalized_finding"]["normalization"]["status"] == "unmapped"
