from __future__ import annotations

import copy
import json
import pathlib
import sys
import unittest

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from dtg_portfolio_routing import combined_event, route_findings


class OctoberRoutingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.policy = yaml.safe_load((ROOT / "instances/dtg/assurance-routing.yaml").read_text())
        cls.normalization = yaml.safe_load((ROOT / "instances/dtg/finding-normalization.yaml").read_text())
        cls.findings = json.loads((ROOT / "tests/fixtures/dtg-2026-10-06-routing.json").read_text())

    def route(self, findings=None):
        return route_findings(self.findings if findings is None else findings, self.policy, self.normalization)

    def test_all_twelve_unmapped_observations_receive_explicit_ownership(self):
        result = self.route()
        self.assertEqual(len(result), 13)
        self.assertNotIn("UNMAPPED", {item["outcome"] for item in result})
        for item in result:
            if item["outcome"] == "covered":
                self.assertRegex(item["decision"]["covered_by"], r"^rahp-toolkit#\d+$")
            else:
                self.assertEqual((item["outcome"], item["rule_id"]), ("combined", "openvtc-security-combined"))

    def test_redelivery_and_replacement_retain_remediation_owners(self):
        result = {x["finding"]["finding_id"]: x for x in self.route()}
        for fid, owner in [("7dd4cece89d11aac5a8a", "rahp-toolkit#898"), ("ec101912064707597281", "rahp-toolkit#899")]:
            self.assertEqual(result[fid]["decision"]["covered_by"], owner)
            self.assertEqual(result[fid]["outcome"], "covered")

    def test_administrative_changes_remain_reviews_instead_of_closed_owner_passes(self):
        admin_ids = {"8d5718ce13e794725aab", "f4cdc35d8f2c782f247c", "09ccb1d242fb33d91c00", "8d8326aa785c31620f36", "adde5ccf990f1abb1fdd"}
        result = [x for x in self.route() if x["finding"]["finding_id"] in admin_ids]
        self.assertEqual(len(result), 5)
        for item in result:
            self.assertEqual(item["outcome"], "combined")
        event = combined_event("openvtc-security-combined", result, "2026-10-06")
        repeated = combined_event("openvtc-security-combined", list(reversed(result)), "2026-10-07")
        self.assertEqual(event["assessment_key"], "dtg:portfolio:combined:openvtc-security-combined")
        self.assertEqual(event["assessment_key"], repeated["assessment_key"])

    def test_pcs_publication_retains_nonterminal_privacy_owner(self):
        pcs = next(x for x in self.route() if x["finding"]["finding_id"] == "f5ad8aa1399207519fb6")
        self.assertEqual(pcs["outcome"], "covered")
        self.assertEqual(pcs["decision"]["covered_by"], "rahp-toolkit#889")

    def test_sdk_error_semantics_override_routine_release_classification(self):
        sdk = next(x for x in self.route() if x["finding"]["finding_id"] == "a775c9693b223f68a751")
        self.assertEqual(sdk["rule_id"], "declared-error-propagation")
        self.assertEqual(sdk["decision"]["covered_by"], "rahp-toolkit#691")

    def test_unseen_predicate_semantics_remain_unmapped(self):
        changed = copy.deepcopy(self.findings[0])
        changed.update(finding_id="changed-predicate", title="feat!: redefine the community predicate's evidentiary meaning")
        self.assertEqual(self.route([changed])[0]["outcome"], "UNMAPPED")

    def test_unrelated_repository_cannot_inherit_durable_owner(self):
        changed = copy.deepcopy(self.findings[0])
        changed["repository"] = "example/unrelated"
        self.assertEqual(self.route([changed])[0]["outcome"], "UNMAPPED")


if __name__ == "__main__":
    unittest.main()
