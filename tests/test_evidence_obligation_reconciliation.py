import copy
import importlib.util
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("eor", ROOT / "tools" / "evidence_obligation_reconciliation.py")
mod = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(mod)
FIXTURE = ROOT / "fixtures" / "human-power" / "dpip-191-evidence-obligations.json"


class ReconciliationTests(unittest.TestCase):
    def setUp(self):
        self.items = json.loads(FIXTURE.read_text())["obligations"]

    def test_current_191_obligations_keep_passing_rahp_proposition_indeterminate(self):
        for ob in self.items:
            result = mod.reconcile(ob, dependent_rahp_outcome="PASS")
            self.assertEqual(result["outcome"], "INDETERMINATE")
            self.assertEqual(result["reason"], "material-dpip-evidence-obligation-unresolved")
            self.assertFalse(result["deployment_claim_supported"])

    def test_rahp_fail_remains_fail(self):
        result = mod.reconcile(self.items[0], dependent_rahp_outcome="FAIL")
        self.assertEqual(result["outcome"], "FAIL")

    def test_non_material_blocked_obligation_does_not_block_pass(self):
        ob = copy.deepcopy(self.items[0])
        ob["materiality"] = "non-material"
        self.assertEqual(mod.reconcile(ob, dependent_rahp_outcome="PASS")["outcome"], "PASS")

    def test_satisfied_material_obligation_allows_dependent_pass(self):
        ob = copy.deepcopy(self.items[0])
        ob["state"] = "SATISFIED"
        ob["access"] = {"status": "AVAILABLE", "blocker": "NONE"}
        ob["target"] = {"repository": "example/target", "revision": "0123456789abcdef"}
        result = mod.reconcile(ob, dependent_rahp_outcome="PASS")
        self.assertEqual(result["outcome"], "PASS")
        self.assertTrue(result["deployment_claim_supported"])

    def test_assurability_gap_remains_explicit(self):
        ob = copy.deepcopy(self.items[0])
        ob["access"] = {"status": "BLOCKED", "blocker": "NO_OBSERVATION_SURFACE"}
        result = mod.reconcile(ob, dependent_rahp_outcome="PASS")
        self.assertEqual(result["assurability"], "ASSURABILITY_GAP")
        self.assertEqual(result["outcome"], "INDETERMINATE")

    def test_residual_risk_acceptance_requires_authority(self):
        ob = copy.deepcopy(self.items[0])
        ob["state"] = "ACCEPTED_RESIDUAL_RISK"
        ob["residual_risk_acceptance"] = {"scope": "bounded"}
        with self.assertRaisesRegex(ValueError, "named authority and scope"):
            mod.reconcile(ob, dependent_rahp_outcome="PASS")

    def test_authorized_residual_risk_acceptance_is_not_material_unresolved(self):
        ob = copy.deepcopy(self.items[0])
        ob["state"] = "ACCEPTED_RESIDUAL_RISK"
        ob["residual_risk_acceptance"] = {"authority": "named-authority", "scope": "bounded proposition"}
        result = mod.reconcile(ob, dependent_rahp_outcome="PASS")
        self.assertEqual(result["outcome"], "PASS")

    def test_dpip_status_does_not_claim_broader_harm(self):
        result = mod.reconcile(self.items[0], dependent_rahp_outcome="PASS")
        self.assertIn("does not mechanically establish broader harm", result["authority_boundary"]["rule"])


if __name__ == "__main__":
    unittest.main()
