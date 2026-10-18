"""Guard against source-level test inventory being misrepresented as runtime evidence."""
import copy
import json
import unittest

from tools.validate_witness_source_coverage import MANIFEST, verify

BASE = json.loads(MANIFEST.read_text())


class WitnessSourceCoverageTests(unittest.TestCase):
    def test_source_manifest_is_nonterminal(self):
        self.assertEqual([], verify(BASE))
        self.assertEqual(10, len(BASE["tests"]))
        self.assertEqual("aggregate-success-only", BASE["ci"]["attribution"])

    def test_missing_and_duplicate_test_rejected(self):
        altered = copy.deepcopy(BASE)
        altered["tests"].pop()
        self.assertTrue(verify(altered))
        altered = copy.deepcopy(BASE)
        altered["tests"][1]["name"] = altered["tests"][0]["name"]
        self.assertTrue(any("duplicate" in x for x in verify(altered)))

    def test_source_only_cannot_claim_executed(self):
        altered = copy.deepcopy(BASE)
        altered["tests"][0]["evidence_status"] = "PASS"
        self.assertTrue(any("runtime PASS" in x for x in verify(altered)))

    def test_fabricated_or_unwired_source_rejected(self):
        source = "#[tokio::test] async fn fake_test() {}"
        self.assertTrue(any("declaration mismatch" in x for x in verify(BASE, source)))
        source = "\n".join("#[tokio::test] async fn " + x["name"] + "() {}" for x in BASE["tests"])
        self.assertEqual([], verify(BASE, source, '#[path = "witness_tests.rs"] mod tests;'))
        self.assertTrue(any("module not proven" in x for x in verify(BASE, source, "mod other;")))


if __name__ == "__main__":
    unittest.main()
