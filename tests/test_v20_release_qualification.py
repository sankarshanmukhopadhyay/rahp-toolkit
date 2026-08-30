import json, unittest
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]

class V20ReleaseQualificationTests(unittest.TestCase):
    def test_workspace_is_200(self):
        self.assertEqual(json.loads((ROOT/"package.json").read_text())["version"],"2.0.0")
        status=yaml.safe_load((ROOT/"PROJECT-STATUS.yaml").read_text())
        self.assertEqual(str(status["stable_release"]),"2.0.0")

    def test_release_identity(self):
        r=yaml.safe_load((ROOT/"method/release.yaml").read_text())["release"]
        self.assertEqual(r["version"],"2.0.0")
        self.assertEqual(r["theme"],"Portable Assurance Engine Stabilization")
        self.assertEqual((r["name"]["common"],r["name"]["scientific"]),("Blue Mormon","Papilio polymnestor"))

    def test_contract_compatibility_is_preserved(self):
        s=yaml.safe_load((ROOT/"PROJECT-STATUS.yaml").read_text())
        self.assertEqual(s["compatibility"]["engine_contract"],"rahp-engine-contract-v1")
        self.assertEqual(s["compatibility"]["normalized_result_schema"],1)
        self.assertEqual(s["compatibility"]["evidence_retention_contract"],"rahp-evidence-retention-v1")
        v=yaml.safe_load((ROOT/"method/versioning.yaml").read_text())
        self.assertEqual(str(v["contracts"]["engine_revision"]),"1.3")

    def test_stabilization_contracts_exist(self):
        for rel in (
            "method/schema/normalized-finding.schema.json",
            "method/schema/assessor-result.schema.json",
            "method/schema/assessment-lifecycle.schema.json",
            "tools/assessment_controller.py",
            "tools/clean_room.py",
            "tests/test_dtg_black_box_acceptance.py",
        ):
            self.assertTrue((ROOT/rel).is_file(),rel)

if __name__=="__main__": unittest.main()
