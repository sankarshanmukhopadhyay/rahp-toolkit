#!/usr/bin/env python3
import importlib.util
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("release_codenames", Path(__file__).with_name("release_codenames.py"))
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


class ReleaseCodenameTests(unittest.TestCase):
    def test_repository_state_is_valid(self):
        self.assertEqual([], mod.validate_repository())

    def test_current_release_is_grandfathered_without_rewriting_history(self):
        policy = mod.load_json(mod.POLICY)
        alias = mod.aliases(policy)["common map"]
        self.assertEqual("Cyrestis thyodamas", alias["scientific"])

    def test_existing_version_is_idempotent(self):
        codename, existing = mod.select("v1.8.0", seed="ignored")
        self.assertTrue(existing)
        self.assertEqual("Common Map", codename)

    def test_future_selection_does_not_reuse_historical_names(self):
        codename, existing = mod.select("v9.9.9", seed="fixed")
        self.assertFalse(existing)
        self.assertNotIn(codename, {"Purple Leaf Blue", "Common Earl", "Common Palmfly", "Common Map"})

    def test_unknown_current_release_binding_fails(self):
        doc = {"release": {"tag": "v9.9.9", "name": {"common": "Common Raven", "scientific": "x"}}}
        self.assertTrue(any("no persisted codename history binding" in e for e in mod.validate_repository(doc)))


if __name__ == "__main__":
    unittest.main()
