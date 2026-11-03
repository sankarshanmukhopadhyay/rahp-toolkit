"""Execute Hello RAHP as an uncoached, isolated *machine* onboarding smoke test.

This tests artifact creation and provenance, not human interpretation or assurance PASS.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]


def checked(*command: str, cwd: Path) -> subprocess.CompletedProcess:
    proc = subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)
    if proc.returncode:
        raise AssertionError(
            f"offline command failed ({proc.returncode}): {command!r}\n"
            f"stdout: {proc.stdout[-2000:]}\nstderr: {proc.stderr[-2000:]}"
        )
    return proc


class HelloRahpOfflineScaffoldTests(unittest.TestCase):
    def test_first_review_is_real_offline_artifact_with_bounded_provenance(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            checkout = workspace / "rahp"
            checkout.mkdir()
            # A local-only Git fetch tests the *committed* repository, not a
            # maintainer's uncommitted working files. No GitHub/network access.
            checked("git", "init", "-q", str(checkout), cwd=workspace)
            checked("git", "-C", str(checkout), "fetch", "--quiet", "--no-tags",
                    str(ROOT), "HEAD", cwd=workspace)
            checked("git", "-C", str(checkout), "checkout", "--detach", "-q",
                    "FETCH_HEAD", cwd=workspace)
            target_sha = checked("git", "rev-parse", "HEAD", cwd=checkout).stdout.strip()
            self.assertEqual(40, len(target_sha))
            declared = yaml.safe_load((checkout / "method/versioning.yaml").read_text())
            method_release = declared["stable_release"]

            args = [sys.executable, "tools/rahp.py", "review",
                    "--config", "examples/hello-rahp/rahp.yaml",
                    "--target", "hello-spec", "--mode", "rahp", "--offline"]
            first = checked(*args, cwd=checkout)
            self.assertIn("scaffold", first.stdout.lower())

            artifact = checkout / ".rahp/reviews/hello-spec/pressure-test.yaml"
            guide = checkout / ".rahp/reviews/hello-spec/README.md"
            self.assertTrue(artifact.is_file(), "working YAML must be generated")
            self.assertTrue(guide.is_file(), "review instructions must be discoverable")
            raw = artifact.read_bytes()
            data = yaml.safe_load(raw)["review"]
            self.assertEqual("in-progress", data["status"])
            self.assertEqual([], data["findings"], "scaffolding is not evidence of a finding")
            self.assertEqual("sankarshanmukhopadhyay/rahp-toolkit",
                             data["target"]["repository"])
            self.assertEqual(target_sha, data["target"]["commit"])
            self.assertEqual(method_release, data["reviewed_against"]["rahp_version"])
            self.assertEqual("rahp-engine-contract-v1",
                             data["reviewed_against"]["engine_contract"])

            # A repeat must not overwrite existing reviewer work without
            # an explicit --force; prove the first artifact stays byte-identical.
            earlier = hashlib.sha256(raw).hexdigest()
            second = subprocess.run(args, cwd=checkout, text=True,
                                    capture_output=True, check=False)
            self.assertNotEqual(0, second.returncode)
            self.assertIn("already exists", second.stdout + second.stderr)
            self.assertEqual(earlier, hashlib.sha256(artifact.read_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main()
