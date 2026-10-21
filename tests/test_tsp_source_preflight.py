"""Unit tests for TSP immutable-source evidence preflight (no external network)."""
import importlib.util
import pathlib
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "tools/tsp_source_preflight.py"
spec = importlib.util.spec_from_file_location("tsp_source_preflight", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

GOOD = """[[def: Verifiable Identifier, VID]]
[[def: TSP Relationship, Relationship]]
[[def: Out of Band Introduction, OOBI]]
Direct Mode and Routed Mode
A message provides optionally, confidentiality and metadata privacy.
Normative references: RFC2119.
"""

class SourcePreflightTests(unittest.TestCase):
    def test_text_observation_is_not_assurance(self):
        result = module.examine(GOOD)
        self.assertTrue(all(result["checks"].values()))
        self.assertEqual(result["assurance_disposition"], "INDETERMINATE")
        for lens in ("conformance", "security", "composition", "drarm"):
            self.assertEqual(result[lens], "NOT_TESTED")
        self.assertEqual(result["published_render_equivalence"], "NOT_ESTABLISHED")

    def test_missing_text_does_not_pass(self):
        result = module.examine("Only a heading")
        self.assertFalse(all(result["checks"].values()))

    def test_hash_changes_when_source_changes(self):
        self.assertNotEqual(module.examine(GOOD)["sha256"], module.examine(GOOD + "changed")["sha256"])

    def test_pin_is_full_commit(self):
        self.assertEqual(len(module.COMMIT), 40)
        self.assertIn(module.COMMIT, module.URL)

if __name__ == "__main__":
    unittest.main()
