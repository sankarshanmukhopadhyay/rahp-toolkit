import tempfile
import unittest
from pathlib import Path

import yaml

from tools.dtg_portfolio_baseline import load_baseline


CURRENT_BASELINE = Path(__file__).parents[1] / "instances/dtg/baselines/current.yaml"


class DtgPortfolioBaselineTests(unittest.TestCase):
    def write_manifest(self, data):
        td = tempfile.TemporaryDirectory()
        path = Path(td.name) / "baseline.yaml"
        path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
        return td, path

    def test_valid_baseline_returns_distinct_lineage_and_pins(self):
        td, path = self.write_manifest(
            {
                "schema": "rahp-dtg-portfolio-baseline/v1",
                "lineage": "post-graduation-2026-09-09",
                "purpose": "post-graduation-full-portfolio-rebaseline",
                "pins": {
                    "trust_tasks": "a" * 40,
                    "credential_spec": "b" * 40,
                    "openvtc_vti": "c" * 40,
                    "interop_lab": "d" * 40,
                },
            }
        )
        self.addCleanup(td.cleanup)
        result = load_baseline(path)
        self.assertEqual("post-graduation-2026-09-09", result["lineage"])
        self.assertEqual("c" * 40, result["pins"]["openvtc_vti"])

    def test_repository_current_baseline_is_valid(self):
        result = load_baseline(CURRENT_BASELINE)
        self.assertEqual("rahp-dtg-portfolio-baseline/v1", result["schema"])
        self.assertTrue(result["lineage"].startswith("post-graduation-"))

    def test_missing_required_pin_fails_closed(self):
        td, path = self.write_manifest(
            {
                "schema": "rahp-dtg-portfolio-baseline/v1",
                "lineage": "post-graduation-2026-09-09",
                "purpose": "post-graduation-full-portfolio-rebaseline",
                "pins": {
                    "trust_tasks": "a" * 40,
                    "credential_spec": "b" * 40,
                    "openvtc_vti": "c" * 40,
                },
            }
        )
        self.addCleanup(td.cleanup)
        with self.assertRaises(ValueError):
            load_baseline(path)

    def test_non_sha_pin_fails_closed(self):
        td, path = self.write_manifest(
            {
                "schema": "rahp-dtg-portfolio-baseline/v1",
                "lineage": "post-graduation-2026-09-09",
                "purpose": "post-graduation-full-portfolio-rebaseline",
                "pins": {
                    "trust_tasks": "main",
                    "credential_spec": "b" * 40,
                    "openvtc_vti": "c" * 40,
                    "interop_lab": "d" * 40,
                },
            }
        )
        self.addCleanup(td.cleanup)
        with self.assertRaises(ValueError):
            load_baseline(path)


if __name__ == "__main__":
    unittest.main()
