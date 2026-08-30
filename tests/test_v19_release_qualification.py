import json, unittest
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]

class V19ReleaseQualificationTests(unittest.TestCase):
    def test_workspace_is_190(self):
        self.assertEqual(json.loads((ROOT/"package.json").read_text())["version"],"1.9.0")
        status=yaml.safe_load((ROOT/"PROJECT-STATUS.yaml").read_text())
        self.assertEqual(str(status["stable_release"]),"1.9.0")

    def test_release_identity(self):
        r=yaml.safe_load((ROOT/"method/release.yaml").read_text())["release"]
        self.assertEqual(r["version"],"1.9.0")
        self.assertEqual(r["theme"],"Portable Clean-Room Assurance")
        self.assertEqual((r["name"]["common"],r["name"]["scientific"]),("Lesser Mime","Papilio epycides"))

    def test_stable_v1_contracts_are_preserved(self):
        s=yaml.safe_load((ROOT/"PROJECT-STATUS.yaml").read_text())
        self.assertEqual(s["compatibility"]["engine_contract"],"rahp-engine-contract-v1")
        self.assertEqual(s["compatibility"]["normalized_result_schema"],1)
        self.assertEqual(s["compatibility"]["evidence_retention_contract"],"rahp-evidence-retention-v1")

    def test_clean_room_executor_is_generic(self):
        text=(ROOT/".github/workflows/clean-room-assessment.yml").read_text().lower()
        for forbidden in ("dogwood","openvtc","verifiable-trust-infrastructure"):
            self.assertNotIn(forbidden,text)

    def test_pressure_acceptance_is_adapter_scoped(self):
        q=yaml.safe_load((ROOT/"method/v1.9-release-qualification.yaml").read_text())
        self.assertTrue(q["portable_clean_room"]["target_specific_behavior_confined_to_adapter_or_run_spec"])
        self.assertTrue(q["experiment_semantics"]["positive_control_join_is_not_privacy_failure"])
        self.assertTrue(q["experiment_semantics"]["composition_evidence_not_promoted_to_target_native"])

if __name__=="__main__": unittest.main()
