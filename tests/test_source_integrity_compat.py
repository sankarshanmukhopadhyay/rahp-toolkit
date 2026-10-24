"""Fixture, negative-path and claim-boundary checks for source compatibility probe."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "tools/source_integrity_compat.py"
spec = importlib.util.spec_from_file_location("source_integrity_compat", SCRIPT)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)


class SourceIntegrityCompatibility(unittest.TestCase):
    def test_valid_fixture_has_source_and_commit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            probe.fixture(root, "valid")
            data = json.loads((root / "source-manifest.json").read_text())
            self.assertEqual(data["commit"], "a" * 40)
            self.assertTrue((root / data["files"][0]["path"]).is_file())

    def test_negative_cases_have_distinct_faults(self):
        for variant in ("bad_hash", "bad_url", "duplicate", "unsafe_path"):
            with self.subTest(variant=variant), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                probe.fixture(root, variant)
                m = json.loads((root / "source-manifest.json").read_text())
                row = m["files"][0]
                if variant == "bad_hash":
                    self.assertEqual(row["sha256"], "0" * 64)
                elif variant == "bad_url":
                    self.assertIn("/other/", row["url"])
                elif variant == "duplicate":
                    self.assertEqual(len(m["files"]), 2)
                else:
                    self.assertTrue(row["path"].startswith("../"))

    def test_missing_checkouts_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(FileNotFoundError):
                probe.compare(Path(tmp), Path(tmp))

    def test_equivalent_outcomes_do_not_imply_assurance(self):
        with patch.object(probe, "load_function", side_effect=[lambda root: {}, lambda root: {}]):
            result = probe.compare(Path("up"), Path("down"))
        self.assertEqual(len(result["results"]), 5)
        self.assertIn("target assurance", result["not_claimed"])
        self.assertTrue(all(x["classification"] == "compatible" for x in result["results"]))
