import ast
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "tools" / "validate_review_readiness.py"


class ReviewReadinessVersioningTests(unittest.TestCase):
    def test_validator_does_not_hardcode_a_toolkit_release(self):
        source = VALIDATOR.read_text(encoding="utf-8")
        tree = ast.parse(source)
        string_literals = {
            node.value
            for node in ast.walk(tree)
            if isinstance(node, ast.Constant) and isinstance(node.value, str)
        }
        hardcoded_release_literals = {
            value
            for value in string_literals
            if value.startswith("v2.") and value.count(".") == 2
        }
        self.assertEqual(
            hardcoded_release_literals,
            set(),
            "independent-review readiness must derive the toolkit release from method/versioning.yaml",
        )

    def test_validator_uses_stable_release_from_versioning(self):
        source = VALIDATOR.read_text(encoding="utf-8")
        self.assertIn('versioning.get("stable_release")', source)
        self.assertIn('stable_release = str(expected["toolkit_release"] or "")', source)
        self.assertIn("stable_release,", source)


if __name__ == "__main__":
    unittest.main()
