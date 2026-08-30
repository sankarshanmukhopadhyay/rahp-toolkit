import importlib.util
import pathlib
import sys
import unittest

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

finding_spec = importlib.util.spec_from_file_location("finding_model", TOOLS / "finding_model.py")
FINDING = importlib.util.module_from_spec(finding_spec)
finding_spec.loader.exec_module(FINDING)

routing_spec = importlib.util.spec_from_file_location("dtg_portfolio_routing", TOOLS / "dtg_portfolio_routing.py")
ROUTING = importlib.util.module_from_spec(routing_spec)
routing_spec.loader.exec_module(ROUTING)


class NormalizedFindingContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.adapter = yaml.safe_load((ROOT / "instances" / "dtg" / "finding-normalization.yaml").read_text())
        cls.policy = yaml.safe_load((ROOT / "instances" / "dtg" / "assurance-routing.yaml").read_text())

    def raw(self, finding_id, repository, title):
        return {
            "finding_id": finding_id,
            "fingerprint": finding_id,
            "state": "open",
            "review_status": "unreviewed",
            "materiality": "high",
            "assurance_impact": "potentially-breaking",
            "repository": repository,
            "title": title,
            "related_repositories": [],
        }

    def test_generic_normalizer_routes_semantics_not_source_identity(self):
        adapter = {
            "mapping_rules": [{
                "id": "metadata",
                "title_regex": "metadata",
                "semantics": {
                    "dimensions": ["privacy"],
                    "concerns": ["metadata"],
                    "affected_surfaces": ["protocol-envelope"],
                    "change_kind": ["behavior-change"],
                },
            }]
        }
        rule = {"when": {"dimensions": ["privacy"], "concerns": ["metadata"]}}
        first = FINDING.normalize_finding(self.raw("A", "one/example", "Metadata expanded"), adapter)
        second = FINDING.normalize_finding(self.raw("B", "two/example", "Different metadata wording"), adapter)
        self.assertTrue(FINDING.semantic_match(rule, first))
        self.assertTrue(FINDING.semantic_match(rule, second))

    def test_dtg_device_heartbeat_maps_then_routes_semantically(self):
        item = self.raw("D", "OpenVTC/openvtc", "feat(devices): send this install's current name on the heartbeat")
        routed = ROUTING.route_findings([item], self.policy, self.adapter)
        self.assertEqual(routed[0]["outcome"], "dpip")
        normalized = routed[0]["normalized_finding"]
        self.assertEqual(normalized["normalization"]["status"], "mapped")
        self.assertIn("privacy", normalized["dimensions"])
        self.assertIn("metadata", normalized["concerns"])

    def test_unknown_qualifying_finding_becomes_unmapped(self):
        item = self.raw("U", "example/portable", "Novel assurance concept with no profile mapping")
        routed = ROUTING.route_findings([item], self.policy, self.adapter)
        self.assertEqual(routed[0]["outcome"], "UNMAPPED")
        self.assertEqual(routed[0]["normalized_finding"]["normalization"]["status"], "unmapped")

    def test_legacy_compatibility_path_remains_available(self):
        item = self.raw("L", "OpenVTC/openvtc", "fix auth conformance")
        routed = ROUTING.route_findings([item], self.policy)
        self.assertEqual(routed[0]["outcome"], "combined")

    def test_generic_model_contains_no_dtg_source_vocabulary(self):
        source = (TOOLS / "finding_model.py").read_text()
        for token in ("OpenVTC", "Dogwood", "Trust Tasks", "relationship DID", "device heartbeat"):
            self.assertNotIn(token, source)


if __name__ == "__main__":
    unittest.main()
