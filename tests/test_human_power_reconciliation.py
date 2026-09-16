import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "human_power_reconciliation.py"
FIXTURE = ROOT / "fixtures" / "human-power" / "dpip-reconciliation-input.json"

spec = importlib.util.spec_from_file_location("human_power_reconciliation", SCRIPT)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


class HumanPowerReconciliationTests(unittest.TestCase):
    def setUp(self):
        self.bundle = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_current_disclosure_tranche_reconciles_fail(self):
        result = mod.reconcile_bundle(self.bundle)["results"][0]
        self.assertEqual(result["proposition"], "compelled-expanded-disclosure")
        self.assertEqual(result["inputs"]["rahp"]["outcome"], "FAIL")
        self.assertEqual(result["inputs"]["dpip"]["outcome"], "FAIL")
        self.assertEqual(result["outcome"], "FAIL")
        self.assertIn("rahp-human-power-invariant-failed", result["reasons"])
        self.assertIn("dpip-privacy-depth-negative", result["reasons"])

    def test_current_proxy_tranche_remains_indeterminate(self):
        result = mod.reconcile_bundle(self.bundle)["results"][1]
        self.assertEqual(result["inputs"]["rahp"]["outcome"], "INDETERMINATE")
        self.assertEqual(result["inputs"]["dpip"]["outcome"], "INDETERMINATE")
        self.assertEqual(result["outcome"], "INDETERMINATE")
        self.assertTrue(any("sensitive/social characteristic" in item for item in result["residual_evidence_requirements"]))

    def test_synthetic_specialist_evidence_never_supports_deployment_claim(self):
        result = mod.reconcile_bundle(self.bundle)["results"][0]
        self.assertFalse(result["deployment_claim_supported"])
        self.assertIn("target-deployment-behavior-not-established-by-synthetic-evidence", result["residual_evidence_requirements"])

    def test_dpip_indeterminate_blocks_material_rahp_pass(self):
        rahp = {"outcome": "PASS", "reasons": ["model-pass"], "dpip_handoff_required": True}
        dpip = copy.deepcopy(self.bundle["dpip_results"][1])
        result = mod.reconcile(
            "test", rahp, dpip, rahp_issue=179,
            dpip_revision=self.bundle["provenance"]["dpip_revision"],
            interop_revision=self.bundle["provenance"]["interop_revision"],
        )
        self.assertEqual(result["outcome"], "INDETERMINATE")
        self.assertIn("dpip-material-privacy-depth-indeterminate", result["reasons"])

    def test_dpip_fail_does_not_mechanically_replace_rahp_pass(self):
        rahp = {"outcome": "PASS", "reasons": ["governed-model-pass"], "dpip_handoff_required": True}
        dpip = copy.deepcopy(self.bundle["dpip_results"][0])
        result = mod.reconcile(
            "test", rahp, dpip, rahp_issue=161,
            dpip_revision=self.bundle["provenance"]["dpip_revision"],
            interop_revision=self.bundle["provenance"]["interop_revision"],
        )
        self.assertEqual(result["outcome"], "INDETERMINATE")
        self.assertIn("dpip-privacy-negative-but-human-power-attribution-not-established", result["reasons"])

    def test_dpip_pass_resolves_material_handoff_when_rahp_passes(self):
        rahp = {"outcome": "PASS", "reasons": ["enhanced-assurance-disclosure-justified"], "dpip_handoff_required": True}
        dpip = copy.deepcopy(self.bundle["dpip_results"][0])
        dpip["outcome"] = "PASS"
        dpip["deployment_claim_supported"] = True
        result = mod.reconcile(
            "governed-countercase", rahp, dpip, rahp_issue=161,
            dpip_revision=self.bundle["provenance"]["dpip_revision"],
            interop_revision=self.bundle["provenance"]["interop_revision"],
        )
        self.assertEqual(result["outcome"], "PASS")
        self.assertIn("dpip-specialist-obligation-resolved", result["reasons"])

    def test_rahp_fail_remains_fail_even_if_dpip_is_indeterminate(self):
        rahp = {"outcome": "FAIL", "reasons": ["unnecessary-expanded-disclosure-compelled"], "dpip_handoff_required": True}
        dpip = copy.deepcopy(self.bundle["dpip_results"][1])
        result = mod.reconcile(
            "test", rahp, dpip, rahp_issue=161,
            dpip_revision=self.bundle["provenance"]["dpip_revision"],
            interop_revision=self.bundle["provenance"]["interop_revision"],
        )
        self.assertEqual(result["outcome"], "FAIL")
        self.assertIn("dpip-privacy-depth-remains-indeterminate", result["reasons"])

    def test_non_material_specialist_obligation_does_not_block_rahp_pass(self):
        rahp = {"outcome": "PASS", "reasons": ["model-pass"], "dpip_handoff_required": False}
        dpip = copy.deepcopy(self.bundle["dpip_results"][1])
        result = mod.reconcile(
            "test", rahp, dpip, rahp_issue=179,
            dpip_revision=self.bundle["provenance"]["dpip_revision"],
            interop_revision=self.bundle["provenance"]["interop_revision"],
        )
        self.assertEqual(result["outcome"], "PASS")

    def test_interop_revision_mismatch_is_rejected(self):
        dpip = copy.deepcopy(self.bundle["dpip_results"][0])
        with self.assertRaises(ValueError):
            mod.reconcile(
                "test",
                {"outcome": "FAIL", "reasons": [], "dpip_handoff_required": True},
                dpip,
                rahp_issue=161,
                dpip_revision=self.bundle["provenance"]["dpip_revision"],
                interop_revision="wrong-revision",
            )

    def test_invalid_dpip_schema_is_rejected(self):
        dpip = copy.deepcopy(self.bundle["dpip_results"][0])
        dpip["schema"] = "wrong/v1"
        with self.assertRaises(ValueError):
            mod.validate_dpip_result(dpip)

    def test_bundle_preserves_source_revisions(self):
        results = mod.reconcile_bundle(self.bundle)["results"]
        for result in results:
            self.assertEqual(result["provenance"]["interop_revision"], self.bundle["provenance"]["interop_revision"])
            self.assertEqual(result["provenance"]["dpip_revision"], self.bundle["provenance"]["dpip_revision"])

    def test_portfolio_outcome_is_bounded_fail_not_whole_portfolio_claim(self):
        result = mod.reconcile_bundle(self.bundle)
        self.assertEqual(result["portfolio_outcome"], "FAIL")
        self.assertIn("bounded human-power tranche only", result["portfolio_boundary"])


if __name__ == "__main__":
    unittest.main()
