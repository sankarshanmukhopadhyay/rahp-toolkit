from __future__ import annotations

import pathlib
import re
import unittest

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[1]
PACKET = (
    ROOT / "instances" / "dtg" / "reviews" /
    "portfolio-2026-11-13" / "replay-cases.yaml"
)
EXPECTED_CASES = {1194: 5, 1195: 5, 1197: 4, 1196: 5, 827: 4}
HEX_SHA = re.compile(r"^[0-9a-f]{40}$")


class DtgMaterialityReplayPacketTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.packet = yaml.safe_load(PACKET.read_text(encoding="utf-8"))

    def test_controller_lineage_and_distinct_assurance_state(self) -> None:
        meta = self.packet["metadata"]
        self.assertEqual(meta["controller"], 1191)
        self.assertEqual(meta["snapshot_date"], "2026-11-13")
        self.assertEqual(
            meta["snapshot_sha256"],
            "6b8f4bb2327b7319e6a0ff65708e50a7ae69ac04f07c6132d565a743e2a61da5",
        )
        self.assertEqual(meta["assurance_state"], "INDETERMINATE")
        self.assertEqual(meta["review_stage"], "source-assessed-runtime-pending")

    def test_bounded_distinct_owners_and_complete_case_inventory(self) -> None:
        owners = self.packet["owners"]
        self.assertEqual({o["issue"]: len(o["cases"]) for o in owners}, EXPECTED_CASES)
        case_ids = [c["id"] for o in owners for c in o["cases"]]
        self.assertEqual(len(case_ids), len(set(case_ids)), "duplicate replay case")
        for o in owners:
            self.assertTrue(o["scope"])
            self.assertTrue(o["source_refs"])
            for c in o["cases"]:
                self.assertTrue(c["proposition"])
                self.assertTrue(c["consumer_path"])
                self.assertIn(c["expected_behavior"], {"PASS", "FAIL_CLOSED", "INDETERMINATE"})

    def test_source_references_are_exact_pins(self) -> None:
        for owner in self.packet["owners"]:
            for source in owner["source_refs"]:
                self.assertRegex(source["ref"], HEX_SHA)
                self.assertEqual(
                    source["url"],
                    f"https://github.com/{source['repository']}/commit/{source['ref']}",
                )

    def test_no_false_runtime_success_or_fabricated_artifacts(self) -> None:
        for owner in self.packet["owners"]:
            for case in owner["cases"]:
                self.assertEqual(case["execution_state"], "not-run")
                self.assertEqual(case["result"], "INDETERMINATE")
                self.assertEqual(case["evidence_refs"], [])

    def test_adversarial_coverage_is_not_only_positive(self) -> None:
        for owner in self.packet["owners"]:
            behaviors = {c["expected_behavior"] for c in owner["cases"]}
            self.assertIn("FAIL_CLOSED", behaviors, owner["scope"])


if __name__ == "__main__":
    unittest.main()
