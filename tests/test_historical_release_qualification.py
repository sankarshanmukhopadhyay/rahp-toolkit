"""Historical release qualification must survive future current-release metadata."""
import tempfile
import unittest
from pathlib import Path
import sys
import shutil

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import validate_v26_release


class HistoricalQualificationTests(unittest.TestCase):
    def test_validator_does_not_read_mutable_current_release_metadata(self):
        source = (ROOT / "tools/validate_v26_release.py").read_text(encoding="utf-8")
        for mutable in ("PROJECT-STATUS.yaml", "method/release.yaml",
                        "method/versioning.yaml", "package.json",
                        "examples/portable-instance/data/instance.yaml"):
            with self.subTest(mutable=mutable):
                self.assertNotIn(f'load_yaml("{mutable}")', source)
                self.assertNotIn(f'ROOT / "{mutable}"', source)

    def test_historical_qualification_manifest_is_pinned(self):
        import yaml
        q = yaml.safe_load((ROOT / "method/v2.6-release-qualification.yaml").read_text())
        self.assertEqual(q["release"], "v2.6.0")
        self.assertEqual(q["release_cut"]["selected_common_name"], "Commander")
        self.assertEqual(q["release_cut"]["selected_scientific_name"], "Moduza procris")
        self.assertTrue(q["release_cut"]["publish_only_after_qualification"])


if __name__ == "__main__":
    unittest.main()
