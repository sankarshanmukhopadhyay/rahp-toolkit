"""Newcomer review provenance must be truthful and source-qualified."""
from __future__ import annotations

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import argparse
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import rahp
from rahp_version import stable_release


class AdoptionProvenanceTests(unittest.TestCase):
    def test_release_comes_from_declared_versioning_authority(self):
        self.assertEqual("v2.9.0", stable_release())
        self.assertNotEqual("v0.9.0", stable_release())

    def test_invalid_release_metadata_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "versioning.yaml"
            for data in ("", "stable_release: v3.1.0\n",
                         "id: rahp-versioning-v1\nstable_release: latest\n",
                         "id: rahp-versioning-v1\nstable_release: v2.9.0\nextra: ["):
                with self.subTest(data=data):
                    path.write_text(data, encoding="utf-8")
                    with self.assertRaises(ValueError):
                        stable_release(path)
            with self.assertRaises(ValueError):
                stable_release(Path(directory) / "missing.yaml")

    def test_default_scaffold_records_current_stable_method_not_old_literal(self):
        args = argparse.Namespace(mode="rahp", reviewed_on="2026-11-03",
                                  force=False, dry_run=True, offline=True)
        item = {"id": "sample", "repository": "example/sample",
                "reviews": ["rahp"], "branch": "main"}
        cfg = {"assessment": {"default_mode": "rahp"}}
        buf = StringIO()
        with patch.object(rahp, "resolve_commit", return_value="a" * 40):
            with redirect_stdout(buf):
                rahp.scaffold_one(cfg, item, "rahp", args)
        output = buf.getvalue()
        self.assertIn("--rahp-version v2.9.0", output)
        self.assertNotIn("--rahp-version v0.9.0", output)
        self.assertIn("--commit " + "a" * 40, output)
        self.assertIn("--storage working", output)

    def test_explicit_method_override_is_retained_for_historical_reviews(self):
        args = argparse.Namespace(mode="rahp", reviewed_on="2026-11-03",
                                  force=False, dry_run=True, offline=True)
        item = {"id": "sample", "repository": "example/sample",
                "reviews": ["rahp"], "branch": "main"}
        cfg = {"assessment": {"rahp_version": "v2.8.0"}}
        buf = StringIO()
        with patch.object(rahp, "resolve_commit", return_value="b" * 40):
            with redirect_stdout(buf):
                rahp.scaffold_one(cfg, item, "rahp", args)
        self.assertIn("--rahp-version v2.8.0", buf.getvalue())
        self.assertNotIn("--rahp-version v2.9.0", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
