from __future__ import annotations

import pathlib
import subprocess
import sys
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class DtgPortfolioRoutingTest(unittest.TestCase):
    def test_routing_policy_self_test(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "tools" / "dtg_portfolio_routing.py"),
                    "--findings",
                    str(ROOT / "README.md"),
                    "--policy",
                    str(ROOT / "instances" / "dtg" / "assurance-routing.yaml"),
                    "--snapshot-date",
                    "2026-08-27",
                    "--out-dir",
                    tmp,
                    "--self-test",
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS dtg portfolio routing self-test", result.stdout)


if __name__ == "__main__":
    unittest.main()
