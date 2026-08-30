import json
import pathlib
import sys
import unittest

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from dtg_portfolio_routing import qualifies, route_findings

SNAPSHOTS = [
    "2026-08-28.json",
    "2026-08-29.json",
    "2026-08-30.json",
]


class DtgBlackBoxAcceptanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.policy = yaml.safe_load((ROOT / "instances" / "dtg" / "assurance-routing.yaml").read_text())
        cls.adapter = yaml.safe_load((ROOT / "instances" / "dtg" / "finding-normalization.yaml").read_text())

    def test_three_frozen_snapshots_execute_against_same_core(self):
        signatures = []
        for name in SNAPSHOTS:
            findings = json.loads((ROOT / "tests" / "acceptance" / "dtg" / name).read_text())
            qualified = [f for f in findings if qualifies(f, self.policy)]
            routed = route_findings(findings, self.policy, self.adapter)
            self.assertEqual(len(routed), len(qualified), name)
            self.assertTrue(all(item["outcome"] in {"dpip", "combined", "no-action", "covered", "UNMAPPED"} for item in routed), name)
            self.assertTrue(all("normalized_finding" in item for item in routed), name)
            self.assertFalse(any(item["outcome"] == "unresolved" for item in routed), name)
            signatures.append((name, len(routed), tuple(sorted({item["outcome"] for item in routed}))))

        self.assertEqual(len(signatures), 3)
        # Distinct snapshots are intentionally processed by one unchanged engine
        # implementation and one declarative instance profile.
        self.assertGreater(len({count for _, count, _ in signatures}), 1)

    def test_profile_changes_not_core_vocabulary_define_dtg_semantics(self):
        generic = (TOOLS / "finding_model.py").read_text()
        router = (TOOLS / "dtg_portfolio_routing.py").read_text()
        for token in ("Dogwood", "device heartbeat", "relationship DID"):
            self.assertNotIn(token, generic)
        # Compatibility code may know it is serving the DTG instance, but semantic
        # source phrases must remain in instance profile data, not the generic model.
        self.assertIn("semantic_rules", self.policy)
        self.assertIn("mapping_rules", self.adapter)


if __name__ == "__main__":
    unittest.main()
