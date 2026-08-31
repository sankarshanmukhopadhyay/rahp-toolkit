#!/usr/bin/env python3
"""Regression checks for DTG instance-owned finding normalization and routing."""
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from dtg_portfolio_routing import route_findings  # noqa: E402

POLICY = yaml.safe_load((ROOT / "instances/dtg/assurance-routing.yaml").read_text(encoding="utf-8"))
NORMALIZATION = yaml.safe_load((ROOT / "instances/dtg/finding-normalization.yaml").read_text(encoding="utf-8"))


def finding(fid: str, repository: str, title: str) -> dict:
    return {
        "finding_id": fid,
        "fingerprint": fid,
        "kind": "material_cross_reference",
        "severity": "high",
        "materiality": "high",
        "urgency": "elevated",
        "assurance_impact": "potentially-breaking",
        "repository": repository,
        "title": title,
        "state": "open",
        "review_status": "unreviewed",
        "related_repositories": ["OpenVTC/verifiable-trust-infrastructure"],
    }


wallet_profile = finding(
    "8ef75e6e2fa45fa9a9c8",
    "OpenVTC/vta-browser-plugin",
    "feat(rp-login): add walletProfile — ask who this site knows you as",
)
unknown = finding(
    "unknown-control",
    "example/unknown",
    "introduce an unrelated material semantic change",
)

routed = route_findings([wallet_profile, unknown], POLICY, NORMALIZATION)
wallet, control = routed

assert wallet["normalized_finding"]["normalization"]["status"] == "mapped", wallet
assert "rp-wallet-origin-binding" in wallet["normalized_finding"]["normalization"]["matched_rule_ids"], wallet
assert wallet["rule_id"] == "rp-wallet-origin-binding", wallet
assert wallet["outcome"] == "no-action", wallet
assert control["outcome"] == "UNMAPPED", control

print("DTG instance routing validation: PASS (walletProfile -> rp-wallet-origin-binding/no-action; unknown control -> UNMAPPED)")
