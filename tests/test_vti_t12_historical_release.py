import ast
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "tools" / "validate_vti_t12_judgment.py"


class VtiT12HistoricalReleaseTests(unittest.TestCase):
    def test_historical_validator_does_not_cap_current_release_at_v24(self):
        source = VALIDATOR.read_text(encoding="utf-8")
        self.assertNotIn("repository_version not in {current, expected}", source)
        self.assertIn("semver_tuple(repository_version) < semver_tuple(expected)", source)

    def test_historical_release_versions_are_data_driven(self):
        source = VALIDATOR.read_text(encoding="utf-8")
        tree = ast.parse(source)
        literals = {
            node.value
            for node in ast.walk(tree)
            if isinstance(node, ast.Constant) and isinstance(node.value, str)
        }
        self.assertNotIn("2.4.0", literals)
        self.assertNotIn("2.3.0", literals)


if __name__ == "__main__":
    unittest.main()
