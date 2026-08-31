import json, unittest
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]

class V20ReleaseQualificationTests(unittest.TestCase):
    def test_current_workspace_has_advanced_beyond_200(self):
        package_version=json.loads((ROOT/"package.json").read_text())["version"]
        status=yaml.safe_load((ROOT/"PROJECT-STATUS.yaml").read_text())
        self.assertNotEqual(package_version,"2.0.0")
        self.assertNotEqual(str(status["stable_release"]),"2.0.0")

    def test_v20_release_identity_is_preserved_as_history(self):
        notes=(ROOT/"docs/releases/v2.0.0.md").read_text(encoding="utf-8")
        changelog=(ROOT/"CHANGELOG.md").read_text(encoding="utf-8")
        readme=(ROOT/"README.md").read_text(encoding="utf-8")
        for text in (notes,changelog,readme):
            self.assertIn("v2.0.0",text)
            self.assertIn("Blue Mormon",text)
        self.assertIn("Portable Assurance Engine Stabilization",notes)

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
