from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "tools" / "review.py"
RAHP = ROOT / "tools" / "rahp.py"
FIXTURE = ROOT / "tests" / "fixtures" / "review-mode-matrix.yaml"
WORK = ROOT / ".rahp" / "reviews"
SHA = "0123456789abcdef0123456789abcdef01234567"


class ReviewModeRegressionTests(unittest.TestCase):
    def tearDown(self) -> None:
        for slug in (
            "mode-smoke-rahp",
            "mode-smoke-security",
            "mode-smoke-combined",
            "fixture-one",
            "fixture-two",
        ):
            shutil.rmtree(WORK / slug, ignore_errors=True)

    def run_ok(self, *args: str) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [sys.executable, *args],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        self.assertEqual(result.returncode, 0, result.stdout)
        return result

    def init_mode(self, mode: str, slug: str) -> None:
        self.run_ok(
            str(REVIEW),
            "init",
            "--mode",
            mode,
            "--slug",
            slug,
            "--title",
            "Review mode smoke",
            "--repository",
            "example/review-mode-smoke",
            "--version",
            "fixture",
            "--commit",
            SHA,
            "--storage",
            "working",
            "--force",
        )

    def test_rahp_mode_creates_canonical_record(self) -> None:
        self.init_mode("rahp", "mode-smoke-rahp")
        record = WORK / "mode-smoke-rahp" / "pressure-test.yaml"
        self.assertTrue(record.is_file())
        data = yaml.safe_load(record.read_text(encoding="utf-8"))
        self.assertEqual(data["review"]["target"]["commit"], SHA)
        self.run_ok(str(REVIEW), "validate", "--mode", "rahp")

    def test_security_mode_creates_canonical_record(self) -> None:
        self.init_mode("security", "mode-smoke-security")
        record = WORK / "mode-smoke-security" / "security-findings.yaml"
        self.assertTrue(record.is_file())
        data = yaml.safe_load(record.read_text(encoding="utf-8"))
        self.assertEqual(data["review"]["target"]["commit"], SHA)
        self.run_ok(str(REVIEW), "validate", "--mode", "security")

    def test_combined_mode_creates_both_lenses_and_synthesis(self) -> None:
        self.init_mode("combined", "mode-smoke-combined")
        base = WORK / "mode-smoke-combined"
        for name in ("pressure-test.yaml", "security-findings.yaml", "combined-review.yaml"):
            self.assertTrue((base / name).is_file(), name)
        combined = yaml.safe_load((base / "combined-review.yaml").read_text(encoding="utf-8"))
        self.assertEqual(combined["review"]["target"]["commit"], SHA)
        self.run_ok(str(REVIEW), "validate", "--mode", "combined")

    def test_all_target_selection_scaffolds_every_configured_target(self) -> None:
        self.run_ok(
            str(RAHP),
            "review",
            "--config",
            str(FIXTURE.relative_to(ROOT)),
            "--mode",
            "combined",
            "--all",
            "--offline",
            "--force",
            "--reviewed-on",
            "2026-01-01",
        )
        for slug in ("fixture-one", "fixture-two"):
            base = WORK / slug
            for name in ("pressure-test.yaml", "security-findings.yaml", "combined-review.yaml"):
                self.assertTrue((base / name).is_file(), f"{slug}/{name}")

    def test_disallowed_target_mode_fails_closed(self) -> None:
        fixture = yaml.safe_load(FIXTURE.read_text(encoding="utf-8"))
        fixture["repositories"][0]["reviews"] = ["security"]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "restricted.yaml"
            path.write_text(yaml.safe_dump(fixture, sort_keys=False), encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(RAHP),
                    "review",
                    "--config",
                    str(path),
                    "--mode",
                    "rahp",
                    "--target",
                    "fixture-one",
                    "--offline",
                ],
                cwd=ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("does not permit", result.stdout)


if __name__ == "__main__":
    unittest.main()
