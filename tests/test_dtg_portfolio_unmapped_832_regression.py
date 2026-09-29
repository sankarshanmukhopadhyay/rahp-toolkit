from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from dtg_portfolio_routing import load_yaml, route_findings  # noqa: E402

POLICY = load_yaml(ROOT / "instances" / "dtg" / "assurance-routing.yaml")
NORMALIZATION = load_yaml(ROOT / "instances" / "dtg" / "finding-normalization.yaml")


def finding(fid: str, repo: str, title: str) -> dict[str, object]:
    return {
        "finding_id": fid,
        "fingerprint": fid + "-fingerprint",
        "kind": "material_cross_reference",
        "severity": "high",
        "materiality": "high",
        "urgency": "elevated",
        "assurance_impact": "potentially-breaking",
        "repository": repo,
        "title": title,
        "state": "open",
        "review_status": "unreviewed",
        "related_repositories": [],
    }


def test_controller_832_unmapped_set_is_semantically_owned() -> None:
    fixtures = [
        finding("3cf", "OpenVTC/dtg-credentials", "feat!: add taskDigestMultibase, so a VWC binds to the witness/session it cites"),
        finding("018", "OpenVTC/verifiable-trust-infrastructure", "fix(vtc)!: admin promotion goes through acl/change-role, behind a step-up"),
        finding("51e", "OpenVTC/verifiable-trust-infrastructure", "feat(vtc): git namespaces — forge governance, registry projection and bridge messaging"),
        finding("85c", "OpenVTC/verifiable-trust-infrastructure", "feat(trust-tasks): advertise the acceptance window over trust-task-discovery 0.3 (VTI-TRN-047)"),
        finding("a1e", "OpenVTC/verifiable-trust-infrastructure", "feat(persona)!: where a face may be worn, where it is, and what it has done"),
        finding("4a7", "trustoverip/dtgwg-cred-spec", "Name the correlation-scope declaration issuerScope and pin the v1 context"),
        finding("a86", "trustoverip/dtgwg-cred-spec", "Bind taskContext to the published Trust Tasks mechanisms, and secure credentials with Data Integrity"),
        finding("9b8", "trustoverip/dtgwg-trust-tasks-spec", "feat(spec): a specification may declare its own document size bound"),
        finding("044", "trustoverip/dtgwg-trust-tasks-tf", "spec(auth/step-up): a step-up bound to one operation needs no session"),
        finding("337", "trustoverip/dtgwg-trust-tasks-tf", "feat(vtc/vetting/vetters/show): a by-DID vetter status lookup"),
        finding("443", "trustoverip/dtgwg-trust-tasks-tf", "feat(spec-meta): a specification declares its own maximum document size"),
        finding("6cb", "trustoverip/dtgwg-trust-tasks-tf", "feat(spec): vtc/admin/did-log/install/0.1 — deliver a community its own did:webvh log"),
        finding("21b", "trustoverip/dtgwg-vti-spec", "Close the admin-promotion entry in the divergence register"),
        finding("627", "trustoverip/dtgwg-vti-spec", "Record tasks that require a proof and are served on a bearer token"),
        finding("a82", "trustoverip/dtgwg-vti-spec", "Narrow the bearer-token entry in the divergence register to the tasks it still covers"),
        finding("d3c", "trustoverip/dtgwg-vti-spec", "Do not count a copy collected after its acceptance window as delivered (VTI-TRN-044 – 047)"),
    ]
    routed = route_findings(fixtures, POLICY, NORMALIZATION)
    assert len(routed) == len(fixtures)
    assert all(item["outcome"] != "UNMAPPED" for item in routed)
    by_id = {item["finding"]["finding_id"]: item for item in routed}
    assert by_id["4a7"]["outcome"] == "dpip"
    assert by_id["85c"]["decision"]["covered_by"] == "rahp-toolkit#833"
    assert by_id["d3c"]["decision"]["covered_by"] == "rahp-toolkit#833"
    assert by_id["9b8"]["outcome"] == "no-action"
    assert by_id["443"]["outcome"] == "no-action"
