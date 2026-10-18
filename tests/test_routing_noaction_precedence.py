"""Archived portfolio snapshot #1028/#1040 regression for behavioral no-action."""
from __future__ import annotations

import json
import pathlib
import sys
import unittest

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from dtg_portfolio_routing import route_findings
from finding_model import semantic_match


def finding(title: str, fid: str):
    return {
        "finding_id": fid,
        "fingerprint": fid + "412c",
        "state": "open",
        "review_status": "unreviewed",
        "materiality": "high",
        "assurance_impact": "potentially-breaking",
        "repository": "OpenVTC/verifiable-trust-infrastructure",
        "title": title,
        "related_repositories": ["OpenVTC/vta-browser-plugin", "trustoverip/dtgwg-vti-spec"],
    }


class NoActionPrecedenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.routing = yaml.safe_load((ROOT / "instances/dtg/assurance-routing.yaml").read_text())
        cls.normalization = yaml.safe_load((ROOT / "instances/dtg/finding-normalization.yaml").read_text())

    def test_breaking_wallet_sign_in_cannot_be_no_action(self):
        """Exact source title and ID observed in 2026-10-14 to 2026-10-17 archives."""
        f = finding(
            "feat(vta-sdk)!: wallet sign-in with a trigger link: sign auth/oob grants, "
            "enrol UV keys, advertise TrustTaskHTTPS and SignInPortal",
            "aa28149c7babc678e9e7",
        )
        route = route_findings([f], self.routing, self.normalization)[0]
        self.assertIn("behavior-change", route["normalized_finding"]["change_kind"])
        self.assertEqual("combined", route["outcome"])
        self.assertEqual("openvtc-security-combined", route["rule_id"])

    def test_real_release_marker_stays_no_action(self):
        f = finding("vta-sdk-v0.65.0", "93176b4d2a918609a33b")
        route = route_findings([f], self.routing, self.normalization)[0]
        self.assertEqual("no-action", route["outcome"])
        self.assertEqual("routine-release-or-plan", route["rule_id"])

    def test_exclusion_clause_is_fail_closed_for_unknown_fields(self):
        normalized = {"dimensions": ["release"], "concerns": ["aggregation"], "change_kind": ["behavior-change"]}
        self.assertFalse(semantic_match(
            {"when": {"dimensions": ["release"], "concerns": ["aggregation"]},
             "unless": {"change_kind": ["behavior-change"]}}, normalized))
        self.assertFalse(semantic_match(
            {"when": {"dimensions": ["release"]}, "unless": {"unsupported": ["x"]}}, normalized))


if __name__ == "__main__":
    unittest.main()
