import unittest
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]

class V19HistoricalQualificationTests(unittest.TestCase):
    def test_v19_manifest_remains_immutable_historical_evidence(self):
        q=yaml.safe_load((ROOT/"method/v1.9-release-qualification.yaml").read_text())
        self.assertEqual(q["release"],"v1.9.0")
        self.assertEqual(q["qualification"],"portable-clean-room-assurance")
        self.assertEqual(q["release_cut"]["selected_common_name"],"Lesser Mime")
        self.assertEqual(q["release_cut"]["selected_scientific_name"],"Papilio epycides")

    def test_v19_notes_remain_available(self):
        text=(ROOT/"docs/releases/v1.9.0.md").read_text()
        self.assertIn("RAHP Toolkit v1.9.0",text)
        self.assertIn("Lesser Mime",text)

    def test_v19_contract_compatibility_is_preserved_by_current_release(self):
        s=yaml.safe_load((ROOT/"PROJECT-STATUS.yaml").read_text())
        self.assertEqual(s["compatibility"]["engine_contract"],"rahp-engine-contract-v1")
        self.assertEqual(s["compatibility"]["normalized_result_schema"],1)
        self.assertEqual(s["compatibility"]["evidence_retention_contract"],"rahp-evidence-retention-v1")

if __name__=="__main__": unittest.main()
