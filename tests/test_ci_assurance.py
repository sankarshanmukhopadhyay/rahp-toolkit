from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class CIAssuranceContractTests(unittest.TestCase):
    def test_repository_wide_typescript_assurance_contract(self) -> None:
        run = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "validate_ci_assurance.py")],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)


if __name__ == "__main__":
    unittest.main()
