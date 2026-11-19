import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import stage_registry_source_partition as partition
import publish_assessment_issues as publisher


class RegistrySourcePartitionTests(unittest.TestCase):
    def fixture(self, root):
        reserved = "dtg:portfolio:combined:reserved-proposition"
        accepted = "dtg:portfolio:dpip:accepted-proposition"
        ledger = root / "transfers.json"
        ledger.write_text(json.dumps({"schema": "rahp-registry-transfers/v1",
                                      "transfers": [
            {"assessment_key": reserved, "state": "reserved",
             "toolkit_issue_url": publisher.TOOLKIT_ISSUE_PREFIX + "1194",
             "registry_intent_path": "outbox/pending/transfer-example.json",
             "source_revision": "a"*40, "finding_id": "finding-12345"},
            {"assessment_key": accepted, "state": "accepted",
             "toolkit_issue_url": publisher.TOOLKIT_ISSUE_PREFIX + "1203",
             "registry_issue_url": publisher.REGISTRY_ISSUE_PREFIX + "4"},
        ]}))
        events = [
            [{"assessment_key": "dtg:portfolio:controller:keep", "body": "controller"}],
            [{"assessment_key": "dtg:combined:child", "related_assessment_key": reserved,
              "body": "related exact source"}],
            [{"assessment_key": accepted, "body": "dpip exact source"}],
        ]
        paths = []
        for name, rows in zip(("controller", "combined", "dpip"), events):
            path = root / (name + ".json")
            path.write_text(json.dumps(rows))
            paths.append(path)
        return ledger, paths, events

    def test_held_events_are_losslessly_staged_and_preflight_still_blocks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ledger, paths, originals = self.fixture(root)
            with patch.object(publisher, "request", side_effect=AssertionError("no API")):
                receipt = partition.stage(paths, root / "out", ledger)
            self.assertEqual((receipt["source_count"], receipt["retained_count"],
                              receipt["held_count"]), (3, 1, 2))
            self.assertFalse(receipt["cutover_authorized"])
            self.assertFalse(receipt["toolkit_publication_suppressed"])
            self.assertEqual(json.loads((root / "out/controller.json.retained.json").read_text()),
                             originals[0])
            self.assertEqual(json.loads((root / "out/combined.json.held.json").read_text())[0]["event"],
                             originals[1][0])
            self.assertEqual(json.loads((root / "out/dpip.json.held.json").read_text())[0]["event"],
                             originals[2][0])
            with self.assertRaisesRegex(ValueError, "Registry-owned"):
                publisher.preflight_transfer_files(paths, ledger)

    def test_group_reservation_is_not_a_single_finding_or_acceptance(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ledger = root / "transfers.json"
            key = "dtg:portfolio:combined:spec-dependency-alignment"
            record = {
                "assessment_key": key,
                "toolkit_issue_url": publisher.TOOLKIT_ISSUE_PREFIX + "272",
                "registry_intent_path": "outbox/pending/spec-dependency-2026-11-16.json",
                "monitor_revision": "7e2813c8daf867a21e4064513cc83612726aeb44",
                "snapshot_date": "2026-11-16",
                "finding_ids": ["0add1f4cc0f048ce6bfc", "29e39a0329123d8839a6",
                                "a60eaffaf3cbc1394553", "acc9772126b1a3820240"],
                "group_sha256": "a"*64,
                "state": "reserved_group",
            }
            def write(item):
                ledger.write_text(json.dumps({"schema": "rahp-registry-transfers/v1",
                                              "transfers": [item]}))
            event = root / "combined.json"
            source_group = {"assessment_key": key, "observed_at": record["snapshot_date"],
                            "source_observations": [{"finding_id": fid}
                                for fid in record["finding_ids"]], "body": "full group"}
            record["group_sha256"] = partition.sha(partition.canonical(source_group))
            write(record)
            event.write_text(json.dumps([source_group]))
            self.assertEqual(publisher.load_transfer_keys(ledger), {key})
            receipt = partition.stage([event], root / "stage", ledger)
            self.assertEqual((receipt["held_count"], receipt["retained_count"]), (1, 0))
            held = json.loads((root / "stage/combined.json.held.json").read_text())[0]
            self.assertEqual(held["transfer"], record)
            self.assertEqual(held["reason"], "reserved_without_successor")
            self.assertFalse(held["publication_suppression_authorized"])
            with self.assertRaisesRegex(ValueError, "Registry-owned"):
                publisher.preflight_transfer_files([event], ledger)
            for mutation in ({"finding_ids": list(reversed(record["finding_ids"]))},
                             {"finding_ids": [record["finding_ids"][0]]*2},
                             {"finding_ids": []}, {"group_sha256": "invalid"},
                             {"monitor_revision": "not-a-commit"},
                             {"registry_intent_path": "../other"},
                             {"source_revision": "f"*40}):
                with self.subTest(mutation=mutation):
                    write({**record, **mutation})
                    with self.assertRaises(ValueError):
                        publisher.load_transfer_keys(ledger)
            write(record)
            for mutated, expected in (
                ({**source_group, "observed_at": "2026-11-15"}, "snapshot date"),
                ({**source_group, "source_observations": source_group[
                    "source_observations"][:-1]}, "finding membership"),
                ({**source_group, "body": "altered observation"}, "digest"),
                ({**source_group, "related_assessment_key": key,
                  "assessment_key": "other:combined:scope"}, "primary event key")):
                with self.subTest(expected=expected):
                    event.write_text(json.dumps([mutated]))
                    with self.assertRaisesRegex(ValueError, expected):
                        partition.stage([event], root / "failed", ledger)
                    self.assertFalse((root / "failed").exists())
            event.write_text(json.dumps([source_group]))
            write({**record, "state": "accepted"})
            with self.assertRaises(ValueError):
                publisher.load_transfer_keys(ledger)

    def test_empty_transfer_ledger_keeps_all_events_and_allows_normal_preflight(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "combined.json"
            originals = [{"assessment_key": "dtg:combined:keep", "body": "unchanged"}]
            path.write_text(json.dumps(originals))
            report = partition.stage([path], root / "out", publisher.TRANSFER_LEDGER)
            self.assertEqual(report["held_count"], 0)
            self.assertEqual(json.loads((root / "out/combined.json.retained.json").read_text()),
                             originals)
            self.assertEqual(publisher.preflight_transfer_files(
                [path], publisher.TRANSFER_LEDGER), 1)

    def test_malformed_or_ambiguous_input_fails_before_creating_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ledger, paths, _ = self.fixture(root)
            other = "dtg:portfolio:combined:reserved-proposition"
            paths[0].write_text(json.dumps([{"assessment_key":
                "dtg:portfolio:dpip:accepted-proposition", "related_assessment_key": other}]))
            with self.assertRaisesRegex(ValueError, "multiple Registry"):
                partition.stage(paths, root / "out", ledger)
            self.assertFalse((root / "out").exists())
            paths[0].write_text('{"not":"array"}')
            with self.assertRaisesRegex(ValueError, "JSON array"):
                partition.stage(paths, root / "out", ledger)
            self.assertFalse((root / "out").exists())

    def test_workflow_stages_after_enrichment_before_existing_preflight(self):
        text = (ROOT / ".github/workflows/dtg-materiality-main.yml").read_text()
        journal = text.index("name: Journal DPIP materiality and gate reassessment")
        stage = text.index("name: Stage lossless Registry source partitions")
        preflight = text.index("name: Preflight all DTG publication batches")
        publication = text.index("name: Publish or coalesce portfolio controller")
        self.assertLess(journal, stage)
        self.assertLess(stage, preflight)
        self.assertLess(preflight, publication)
        self.assertIn("build/dtg-routing/registry-partition/", text)


if __name__ == "__main__":
    unittest.main()
