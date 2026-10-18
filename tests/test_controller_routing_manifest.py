"""Negative and positive regression coverage for snapshot routing invariants."""
import copy
import json
import unittest
from pathlib import Path

from tools.validate_controller_routing_manifest import validate_manifest

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "data/assurance/controller-1054-routing.json").read_text(encoding="utf-8"))


class RoutingManifestTests(unittest.TestCase):
    def test_controller_1054_manifest_is_exact_and_nonterminal(self):
        self.assertEqual([], validate_manifest(DATA))
        self.assertFalse(DATA["closure_authorized"])
        self.assertEqual(15, len(DATA["findings"]))
        self.assertEqual(0, sum(x["status"] == "owner-unresolved" for x in DATA["findings"]))

    def test_a_missing_finding_fails(self):
        modified = copy.deepcopy(DATA)
        modified["findings"].pop()
        self.assertIn("unmapped finding count mismatch", validate_manifest(modified))

    def test_duplicate_finding_fails(self):
        modified = copy.deepcopy(DATA)
        modified["findings"][1]["finding_id"] = modified["findings"][0]["finding_id"]
        self.assertTrue(any("duplicate" in e for e in validate_manifest(modified)))

    def test_partial_reconciliation_cannot_assert_closure(self):
        modified = copy.deepcopy(DATA)
        modified["closure_authorized"] = True
        self.assertTrue(any("cannot authorize" in e for e in validate_manifest(modified)))

    def test_unknown_must_not_be_silently_assigned(self):
        modified = copy.deepcopy(DATA)
        unresolved = modified["findings"][0]
        unresolved["status"] = "owner-unresolved"
        self.assertTrue(any("cannot declare owner" in e for e in validate_manifest(modified)))

    def test_routed_owners_cannot_be_omitted(self):
        modified = copy.deepcopy(DATA)
        modified["findings"][0]["owner_issue"] = None
        self.assertTrue(any("requires durable owner" in e for e in validate_manifest(modified)))


if __name__ == "__main__":
    unittest.main()
