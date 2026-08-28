import json, unittest
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]
class V17ReleaseQualificationTests(unittest.TestCase):
    def test_stable_v1_contracts_are_preserved(self):
        s=yaml.safe_load((ROOT/"PROJECT-STATUS.yaml").read_text())
        self.assertEqual(s["compatibility"]["engine_contract"],"rahp-engine-contract-v1")
        self.assertEqual(s["compatibility"]["normalized_result_schema"],1)
        self.assertEqual(s["compatibility"]["evidence_retention_contract"],"rahp-evidence-retention-v1")
    def test_historical_v17_manifest_is_preserved(self):
        q=yaml.safe_load((ROOT/"method/v1.7-release-qualification.yaml").read_text())
        self.assertEqual(q["release"],"v1.7.0")
    def test_dtg_registry_is_eight_of_eight(self):
        d=yaml.safe_load((ROOT/"profiles/dtg/cross-spec-tests.yaml").read_text())
        self.assertEqual(len(d["compositions"]),8)
        self.assertEqual(sum(1 for c in d["compositions"] if c.get("runnable")),8)
    def test_live_zkp_review_is_combined_and_dispositioned(self):
        d=json.loads((ROOT/"instances/dtg/reviews/2026-08-zkp-fork.result.json").read_text())
        self.assertEqual(d["mode"],"combined")
        self.assertEqual(d["status"],"dispositioned")
    def test_speed_nonclaim_is_recorded(self):
        q=yaml.safe_load((ROOT/"method/v1.7-release-qualification.yaml").read_text())
        self.assertEqual(q["performance"]["claim"],"measured-not-improved")
if __name__=="__main__": unittest.main()
