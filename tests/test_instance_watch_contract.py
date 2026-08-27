from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "tools" / "validate_instance_watch_contract.py"


class InstanceWatchContractTests(unittest.TestCase):
    def test_current_head_assurance_dispatch_contract(self) -> None:
        result = subprocess.run(
            [sys.executable, str(VALIDATOR)],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("PASS instance-watch current-head assurance dispatch contract", result.stdout)


if __name__ == "__main__":
    unittest.main()
