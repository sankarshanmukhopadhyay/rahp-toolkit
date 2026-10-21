"""Offline tests for source-delta discovery; no TSP implementation required."""
import importlib.util
from pathlib import Path
import unittest

TOOL = Path(__file__).resolve().parents[1] / "tools/tsp_normative_delta.py"
spec = importlib.util.spec_from_file_location("tsp_normative_delta", TOOL)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class NormativeDeltaTests(unittest.TestCase):
    def test_normative_change_is_flagged_without_assurance_pass(self):
        old = "# Sender binding\nSender MAY be NULL.\n"
        new = "# Sender binding\nSender MUST match envelope.\n"
        result = module.inventory(old, new)
        self.assertGreater(result["changed_hunks"], 0)
        self.assertEqual(result["assurance_disposition"], "INDETERMINATE")
        self.assertTrue(all(x["needs_human_normative_review"] for x in result["hunks"]))
        self.assertTrue(any("MUST" in x["new_normative_keywords"] for x in result["hunks"]))

    def test_identical_sources_have_no_changes(self):
        result = module.inventory("# Heading\nunchanged\n", "# Heading\nunchanged\n")
        self.assertEqual(result["changed_hunks"], 0)
        self.assertEqual(result["old_sha256"], result["new_sha256"])

    def test_nonnormative_changes_still_recorded(self):
        result = module.inventory("# Heading\nfoo\n", "# Heading\nbar\n")
        self.assertEqual(result["changed_hunks"], 1)
        self.assertEqual(result["hunks"][0]["old_section"], "Heading")
        self.assertEqual(result["hunks"][0]["new_section"], "Heading")
        self.assertEqual(result["hunks"][0]["new_normative_keywords"], [])

if __name__ == "__main__":
    unittest.main()
