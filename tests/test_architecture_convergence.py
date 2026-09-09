from pathlib import Path
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "architecture" / "convergence-matrix.yaml"


class ArchitectureConvergenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = yaml.safe_load(MATRIX.read_text(encoding="utf-8"))

    def test_all_stable_primitives_have_exactly_one_owner(self):
        owners = {"RAHP", "DPIP", "Interop Lab"}
        primitives = self.model["stable_primitives"]
        self.assertGreaterEqual(len(primitives), 10)
        for primitive in primitives:
            with self.subTest(primitive=primitive["id"]):
                self.assertIn(primitive["owner"], owners)
                self.assertTrue(str(primitive.get("contract_or_surface", "")).strip())
                self.assertTrue(str(primitive.get("non_inference", "")).strip())

    def test_core_ownership_boundaries_are_not_duplicated(self):
        owner_by_id = {p["id"]: p["owner"] for p in self.model["stable_primitives"]}
        self.assertEqual("RAHP", owner_by_id["terminal-reconciliation"])
        self.assertEqual("RAHP", owner_by_id["materiality-and-routing"])
        self.assertEqual("RAHP", owner_by_id["portable-evidence-producer-result"])
        self.assertEqual("RAHP", owner_by_id["portable-specialist-result"])
        self.assertEqual("DPIP", owner_by_id["privacy-observability-semantics"])
        self.assertEqual("DPIP", owner_by_id["privacy-interpretation"])
        self.assertEqual("Interop Lab", owner_by_id["target-specific-execution"])
        self.assertEqual("Interop Lab", owner_by_id["case-fixtures-and-raw-observations"])

    def test_mechanism_classifications_are_explicit(self):
        allowed = {"KEEP", "CONSOLIDATE", "GENERALISE", "RETIRE", "DEFER"}
        mechanisms = self.model["mechanisms"]
        self.assertGreaterEqual(len(mechanisms), 15)
        for mechanism in mechanisms:
            with self.subTest(repository=mechanism["repository"], mechanism=mechanism["mechanism"]):
                self.assertIn(mechanism["classification"], allowed)
                self.assertTrue(str(mechanism.get("evidence", "")).strip())
                self.assertTrue(str(mechanism.get("action", "")).strip())

    def test_target_execution_does_not_leak_into_generic_rahp(self):
        for mechanism in self.model["mechanisms"]:
            if mechanism["repository"] != "RAHP":
                continue
            self.assertNotEqual("target-specific execution", mechanism.get("responsibility", "").lower())

    def test_completed_graduation_dependencies_are_recorded(self):
        completed = set(self.model["completed_graduation_dependencies"])
        self.assertTrue({"RAHP #490", "RAHP #491", "DPIP #221", "RAHP #506"}.issubset(completed))

    def test_non_inference_chain_remains_explicit(self):
        text = " ".join(p["non_inference"] for p in self.model["stable_primitives"]).lower()
        self.assertIn("workflow", text)
        self.assertIn("terminal", text)
        self.assertIn("privacy", text)
        self.assertIn("evidence", text)


if __name__ == "__main__":
    unittest.main()
