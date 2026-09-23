from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "tools" / "review.py"


class ReviewCliSecurityTests(unittest.TestCase):
    def test_promote_rejects_path_traversal_slug(self):
        result = subprocess.run(
            [sys.executable, str(REVIEW), "promote", "--mode", "rahp", "--slug", "../../examples"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--slug must use lowercase letters, digits and single hyphens", result.stderr + result.stdout)

    def test_promote_rejects_absolute_like_slug(self):
        result = subprocess.run(
            [sys.executable, str(REVIEW), "promote", "--mode", "security", "--slug", "/tmp/rahp"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--slug must use lowercase letters, digits and single hyphens", result.stderr + result.stdout)


if __name__ == "__main__":
    unittest.main()
