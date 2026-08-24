import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

from tools import release

ROOT = Path(__file__).resolve().parents[1]


class GenericReleaseContractTests(unittest.TestCase):
    def test_current_declaration_is_valid_and_synchronized(self):
        doc = release.declaration()
        self.assertEqual(doc["contract"], "rahp-release-declaration-v1")
        self.assertEqual(release.verify(doc), [])

    def test_metadata_is_release_generic(self):
        meta = release.metadata(release.declaration())
        self.assertEqual(meta["tag"], f"v{meta['version']}")
        self.assertTrue(meta["qualification_manifest"].startswith("method/"))
        self.assertTrue(meta["qualification_validator"].startswith("tools/"))
        self.assertTrue(meta["notes_path"].startswith("docs/releases/"))

    def test_github_output_is_machine_readable(self):
        meta = release.metadata(release.declaration())
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "out"
            release.write_github_output(meta, path)
            parsed = dict(line.split("=", 1) for line in path.read_text().splitlines())
        self.assertEqual(parsed["tag"], meta["tag"])
        self.assertEqual(parsed["qualification_validator"], meta["qualification_validator"])
        self.assertEqual(parsed["notes_path"], meta["notes_path"])

    def test_repository_path_escape_is_rejected(self):
        with self.assertRaises(ValueError):
            release.resolve_repo_path("../outside", "test path")

    def test_cli_verify_and_metadata(self):
        verify = subprocess.run(
            [sys.executable, "tools/release.py", "verify"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(verify.returncode, 0, verify.stdout + verify.stderr)
        metadata = subprocess.run(
            [sys.executable, "tools/release.py", "metadata", "--json"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(metadata.returncode, 0, metadata.stdout + metadata.stderr)
        parsed = json.loads(metadata.stdout)
        self.assertEqual(parsed["tag"], f"v{parsed['version']}")


if __name__ == "__main__":
    unittest.main()
