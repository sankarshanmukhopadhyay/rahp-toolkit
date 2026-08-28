from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


class ProjectInvariantTests(unittest.TestCase):
    def test_portable_architecture_invariant_cli_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "validate_project_invariants.py")],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        self.assertIn("PASS INV-PORTABLE-001", result.stdout)

    def test_contract_keeps_two_distinct_non_dtg_fixtures(self) -> None:
        doc = yaml.safe_load((ROOT / "method" / "project-invariants.yaml").read_text(encoding="utf-8"))
        invariant = next(item for item in doc["invariants"] if item["id"] == "INV-PORTABLE-001")
        fixtures = invariant["portability_fixtures"]
        self.assertGreaterEqual(len(fixtures), 2)
        profile_ids = []
        for rel in fixtures:
            fixture = yaml.safe_load((ROOT / rel).read_text(encoding="utf-8"))
            profile_ids.append(fixture["profile"]["id"])
            text = (ROOT / rel).read_text(encoding="utf-8").lower()
            for forbidden in ("trustoverip", "dtgwg-", "portfolio-monitor", "profiles/dtg", "instances/dtg"):
                self.assertNotIn(forbidden, text)
        self.assertEqual(len(profile_ids), len(set(profile_ids)))


if __name__ == "__main__":
    unittest.main()
