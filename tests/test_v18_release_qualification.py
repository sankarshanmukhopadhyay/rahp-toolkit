import json, unittest
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]

class V18ReleaseQualificationTests(unittest.TestCase):
    def test_stable_v1_contracts_are_preserved(self):
        s=yaml.safe_load((ROOT/"PROJECT-STATUS.yaml").read_text())
        self.assertEqual(s["compatibility"]["engine_contract"],"rahp-engine-contract-v1")
        self.assertEqual(s["compatibility"]["normalized_result_schema"],1)
        self.assertEqual(s["compatibility"]["evidence_retention_contract"],"rahp-evidence-retention-v1")

    def test_workspace_is_180(self):
        self.assertEqual(json.loads((ROOT/"package.json").read_text())["version"],"1.8.0")

    def test_semantic_materiality_regression_is_present(self):
        text=(ROOT/"tests/test_dtg_semantic_materiality.py").read_text()
        self.assertIn("test_183_generated_convergence",text)
        self.assertIn("test_low_weight_fanout_cannot_mask_one_normative_change",text)

    def test_materiality_score_is_not_assurance_verdict(self):
        q=yaml.safe_load((ROOT/"method/v1.8-release-qualification.yaml").read_text())
        self.assertFalse(q["semantic_materiality"]["score_is_assurance_verdict"])

    def test_false_independence_register_is_continuing_work(self):
        q=yaml.safe_load((ROOT/"method/v1.8-release-qualification.yaml").read_text())
        self.assertEqual(q["continuing_programmes"]["false_independence_register_issue"],193)
        self.assertFalse(q["continuing_programmes"]["release_claims_complete_coverage"])

    def test_release_name(self):
        r=yaml.safe_load((ROOT/"method/release.yaml").read_text())["release"]
        self.assertEqual((r["name"]["common"],r["name"]["scientific"]),("Common Map","Cyrestis thyodamas"))

if __name__=="__main__": unittest.main()
