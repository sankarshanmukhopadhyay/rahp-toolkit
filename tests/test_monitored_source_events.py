"""Source-event provenance contract, with no Registry admission elevation."""
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "tools/index_monitored_review_events.py"
SPEC = importlib.util.spec_from_file_location("index_monitored_review_events", MODULE)
index = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(index)


def event(instance="dtg", **updates):
    value = {
        "assessment_key": instance + ":repository:trustoverip/dtgwg-trust-tasks-tf",
        "repository": "trustoverip/dtgwg-trust-tasks-tf",
        "old": "a" * 40,
        "new": "b" * 40,
        "title": "[RAHP review required] A material change",
        "body": "Review the source version and affected trust boundary.",
        "labels": ["assessment-required", instance + "-instance"],
    }
    value.update(updates)
    return value


class MonitoredSourceEventTests(unittest.TestCase):
    def test_canonical_evidence_hash_is_stable_but_does_not_admit_a_case(self):
        obj = event()
        report = index.qualify([obj], "dtg")
        self.assertEqual(report["candidate_count"], 1)
        self.assertFalse(report["admission_authorized"])
        self.assertIsNone(report["assurance_determination"])
        entry = report["events"][0]
        self.assertEqual(entry["assessment_key"], obj["assessment_key"])
        self.assertEqual(entry["source_revision"], obj["new"])
        self.assertEqual(entry["finding_id"], entry["source_evidence_sha256"][:20])
        self.assertEqual(entry["source_evidence_sha256"],
                         index.qualify([dict(reversed(list(obj.items())))], "dtg")
                         ["events"][0]["source_evidence_sha256"])

    def test_nonassessment_and_no_change_never_promote(self):
        report = index.qualify([event(
            event_class="change-triage", labels=["change-triage", "dtg-instance"
        )], "dtg")
        self.assertEqual(report["candidate_count"], 0)
        self.assertEqual(report["events"][0]["classification"], "triage_only")
        self.assertEqual(index.qualify([], "cawg")["events"], [])

    def test_corrupt_or_foreign_event_fails_before_state_review(self):
        for bad in (
            None, {"assessment_key": "dtg:repository:without-source"},
            event(new="main"),
            event(repository="../unsafe"),
            event(assessment_key="cawg:repository:other"),
            event(body=""),
            event(labels="not-a-list"),
            event(event_class="invalid"),
        ):
            with self.subTest(bad=bad), self.assertRaises((ValueError, TypeError)):
                index.qualify([bad], "dtg")
        with self.assertRaisesRegex(ValueError, "duplicate"):
            index.qualify([event(), event()], "dtg")
        with self.assertRaisesRegex(ValueError, "array"):
            index.qualify({}, "dtg")

    def test_instance_monitor_persists_exact_review_events_and_artifact_index(self):
        text = (ROOT / ".github/workflows/instance-monitor-main.yml").read_text()
        persist = text.split("\n  persist:", 1)[1]
        for required in (
            "tools/index_monitored_review_events.py",
            "--dtg instances/dtg/generated/review-events.json",
            "--cawg instances/cawg/generated/review-events.json",
            "build/instance-monitor/registry-review-event-index.json",
            "instances/dtg/generated/review-events.json",
            "instances/cawg/generated/review-events.json",
            "git commit -s",
        ):
            self.assertIn(required, text)
        self.assertLess(text.index("Validate and index immutable review-event provenance"),
                        text.index("Bundle exact observed event and state snapshot"))
        self.assertLess(persist.index("instances/dtg/generated/review-events.json"),
                        persist.index("git commit -s"))

    def test_cli_emits_source_index_from_exact_json_batches(self):
        import subprocess
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            a, b, result = (root / n for n in ("dtg.json", "cawg.json", "index.json"))
            a.write_text(json.dumps([event()]))
            b.write_text(json.dumps([event(
                instance="cawg", assessment_key="cawg:repository:decentralized-identity/cawg-identity-assertion",
                repository="decentralized-identity/cawg-identity-assertion",
            )]))
            subprocess.run([
                "python3", str(MODULE), "--dtg", str(a), "--cawg", str(b),
                "--out", str(result),
            ], check=True, capture_output=True)
            receipt = json.loads(result.read_text())
            self.assertEqual(receipt["schema"], index.SCHEMA)
            self.assertEqual(sum(x["candidate_count"] for x in receipt["sources"]), 2)
            self.assertFalse(receipt["admission_authorized"])


if __name__ == "__main__":
    unittest.main()
