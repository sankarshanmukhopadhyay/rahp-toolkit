"""Negative source-identity regressions for the retained TRQP teaching replay."""
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

EXAMPLE = Path(__file__).resolve().parents[1] / "examples/standalone-trqp"
spec = importlib.util.spec_from_file_location("hardened_trqp_replay", EXAMPLE / "replay.py")
replay = importlib.util.module_from_spec(spec)
spec.loader.exec_module(replay)


class RetainedSourceIntegrity(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / "sample"
        shutil.copytree(EXAMPLE, self.root)
        self.manifest_path = self.root / "source-manifest.json"
        self.manifest = json.loads(self.manifest_path.read_text())

    def apply_manifest(self):
        self.manifest_path.write_text(json.dumps(self.manifest))

    def test_valid_retained_trqp_replays_unchanged(self):
        self.assertEqual(replay.replay(self.root),
                         json.loads((EXAMPLE / "expected-replay.json").read_text()))

    def test_duplicate_retained_entry(self):
        self.manifest["files"].append(dict(self.manifest["files"][0]))
        self.apply_manifest()
        with self.assertRaisesRegex(ValueError, "Duplicate source entry"):
            replay.source_integrity(self.root)

    def test_duplicate_upstream_path(self):
        self.manifest["files"][1]["upstream_path"] = self.manifest["files"][0]["upstream_path"]
        self.apply_manifest()
        with self.assertRaisesRegex(ValueError, "Duplicate source entry"):
            replay.source_integrity(self.root)

    def test_wrong_url_binding(self):
        self.manifest["files"][0]["url"] = "https://github.com/other/project/blob/" + (
            self.manifest["commit"] + "/spec.md")
        self.apply_manifest()
        with self.assertRaisesRegex(ValueError, "Source URL disagrees"):
            replay.source_integrity(self.root)

    def test_existing_external_file_cannot_be_referenced(self):
        entry = self.manifest["files"][0]
        shutil.copyfile(self.root / entry["path"], self.root.parent / "outside.txt")
        entry["path"] = "../outside.txt"
        self.apply_manifest()
        with self.assertRaisesRegex(ValueError, "Unsafe retained path"):
            replay.source_integrity(self.root)

    def test_symlink_outside_root_cannot_be_referenced(self):
        entry = self.manifest["files"][0]
        outside = self.root.parent / "outside.txt"
        shutil.copyfile(self.root / entry["path"], outside)
        (self.root / "source" / "link.txt").symlink_to(outside)
        entry["path"] = "source/link.txt"
        self.apply_manifest()
        with self.assertRaisesRegex(ValueError, "Symlink retained path"):
            replay.source_integrity(self.root)

    def test_malformed_commit_rejected(self):
        self.manifest["commit"] = "main"
        self.apply_manifest()
        with self.assertRaisesRegex(ValueError, "immutable commit"):
            replay.source_integrity(self.root)

    def test_tampered_source_remains_rejected(self):
        (self.root / self.manifest["files"][0]["path"]).write_text("changed")
        with self.assertRaisesRegex(ValueError, "Git blob mismatch"):
            replay.source_integrity(self.root)


if __name__ == "__main__":
    unittest.main()
