import json
import unittest
from pathlib import Path

import yaml

from tools.dtg_portfolio_routing import route_findings


ROOT = Path(__file__).parents[1]
FIXTURE = ROOT / "tests/fixtures/dtg-portfolio-unmapped-2026-09-08.json"
ROUTING = ROOT / "instances/dtg/assurance-routing.yaml"
NORMALIZATION = ROOT / "instances/dtg/finding-normalization.yaml"


class DtgPortfolioUnmappedConvergenceTests(unittest.TestCase):
    def test_post_graduation_v2_unmapped_fixture_is_fully_dispositioned(self):
        fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        policy = yaml.safe_load(ROUTING.read_text(encoding="utf-8"))
        normalization = yaml.safe_load(NORMALIZATION.read_text(encoding="utf-8"))

        findings = [
            {k: v for k, v in item.items() if not k.startswith("expected_")}
            for item in fixture
        ]
        routed = route_findings(findings, policy, normalization)
        by_id = {item["finding"]["finding_id"]: item for item in routed}

        self.assertEqual(len(fixture), len(routed))
        self.assertFalse(
            [item["finding"]["finding_id"] for item in routed if item["outcome"] == "UNMAPPED"]
        )

        for expected in fixture:
            actual = by_id[expected["finding_id"]]
            self.assertEqual(
                expected["expected_rule_id"],
                actual["rule_id"],
                expected["finding_id"],
            )
            self.assertEqual(
                expected["expected_outcome"],
                actual["outcome"],
                expected["finding_id"],
            )

    def test_unknown_material_change_still_fails_closed(self):
        policy = yaml.safe_load(ROUTING.read_text(encoding="utf-8"))
        normalization = yaml.safe_load(NORMALIZATION.read_text(encoding="utf-8"))
        finding = {
            "finding_id": "unknown-new-proposition",
            "fingerprint": "unknown-new-proposition",
            "state": "open",
            "review_status": "unreviewed",
            "materiality": "high",
            "assurance_impact": "potentially-breaking",
            "repository": "example/unknown",
            "title": "novel material proposition with no registered semantics",
            "related_repositories": [],
        }
        routed = route_findings([finding], policy, normalization)
        self.assertEqual("UNMAPPED", routed[0]["outcome"])
        self.assertEqual("fallback", routed[0]["rule_id"])


if __name__ == "__main__":
    unittest.main()
