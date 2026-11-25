"""Source-event provenance contract, with no Registry admission elevation."""
from __future__ import annotations

import importlib.util
import json
import tempfile
import sys
import unittest
import hashlib
import subprocess
from unittest.mock import patch
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "tools/index_monitored_review_events.py"
SPEC = importlib.util.spec_from_file_location("index_monitored_review_events", MODULE)
index = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(index)
sys.path.insert(0, str(ROOT / "tools"))
import instance_monitor as monitor


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
            event_class="change-triage", labels=["change-triage", "dtg-instance"],
            assessment_key="dtg:classification:trustoverip/dtgwg-trust-tasks-tf"
        )], "dtg")
        self.assertEqual(report["candidate_count"], 0)
        self.assertEqual(report["events"][0]["classification"], "triage_only")
        self.assertEqual(index.qualify([], "cawg")["events"], [])

    def test_producer_identity_case_branch_and_triage(self):
        repo = "OpenVTC/dtg-credentials"
        main = {"repository": repo}
        other = {"repository": repo, "branch": "release/V2"}
        main_event = event(repository=repo, assessment_key=monitor.assessment_key("dtg", main))
        branch_event = event(repository=repo, branch=other["branch"],
                             assessment_key=monitor.assessment_key("dtg", other))
        triage = event(repository=repo, branch=other["branch"],
                       assessment_key=monitor.assessment_key("dtg", other).replace(
                           ":repository:", ":classification:", 1),
                       event_class="change-triage", labels=["change-triage"])
        report = index.qualify([main_event, branch_event, triage], "dtg")
        self.assertEqual(report["candidate_count"], 2)
        self.assertEqual([x["assessment_key"] for x in report["events"]],
                         [x["assessment_key"] for x in (main_event, branch_event, triage)])
        self.assertFalse(report["admission_authorized"])
        self.assertIsNone(report["assurance_determination"])
        for bad in (
            dict(branch_event, branch="main"),
            dict(branch_event, repository=repo.lower()),
            dict(branch_event, event_class="change-triage"),
            dict(branch_event, instance="cawg"),
            dict(branch_event, branch="bad/../name",
                 assessment_key=f"dtg:repository:{repo}@bad/../name"),
        ):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                index.qualify([bad], "dtg")
        with self.assertRaisesRegex(ValueError, "duplicate"):
            index.qualify([branch_event, branch_event], "dtg")

    def test_actual_monitor_batch_replayed_through_index_cli(self):
        # Exercise the producer's main path; only upstream transport is synthetic.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = "OpenVTC/dtg-credentials"
            targets = [
                {"id": "main", "repository": repo, "scope": {"include": ["SPEC.md"]}},
                {"id": "branch", "repository": repo, "branch": "release/V2",
                 "scope": {"include": ["SPEC.md"]}},
                {"id": "triage", "repository": repo, "branch": "docs/Review",
                 "role": "task-force-workspace", "scope": {"include": ["README.md"]}},
            ]
            cfg = {
                "instance": {"id": "dtg", "profile": "profile.yaml"},
                "generated": {"manifest": "manifest.yaml", "events": "dtg.json"},
                "state": {"file": "state.json"},
                "assessment": {"materiality": {
                    "documentation_paths": ["README.md"],
                    "documentation_triage_roles": ["task-force-workspace"]}},
            }
            (root / "profile.yaml").write_text(json.dumps({"repositories": targets}))
            (root / "config.yaml").write_text(json.dumps(cfg))
            (root / "state.json").write_text(json.dumps({
                "version": 1, "targets": {
                    monitor.state_key(target): {"sha": "a" * 40} for target in targets}}))
            comparisons = iter([
                {"files": [{"filename": "SPEC.md"}]},
                {"files": [{"filename": "SPEC.md"}]},
                {"files": [{"filename": "README.md"}]},
            ])
            with patch.object(monitor, "ROOT", root), patch.object(
                monitor, "head_sha", return_value="b" * 40
            ), patch.object(monitor, "compare", side_effect=comparisons), patch.object(
                sys, "argv", ["instance_monitor.py", "check", "--config", str(root / "config.yaml")]
            ):
                self.assertEqual(monitor.main(), 0)
            dtg = root / "dtg.json"
            cawg = root / "cawg.json"
            cawg.write_text("[]")
            events = json.loads(dtg.read_text())
            self.assertEqual([e["assessment_key"] for e in events], [
                f"dtg:repository:{repo}", f"dtg:repository:{repo}@release/V2",
                f"dtg:classification:{repo}@docs/Review"])
            out = root / "receipt.json"
            cmd = [sys.executable, str(MODULE), "--dtg", str(dtg),
                   "--cawg", str(cawg), "--out", str(out)]
            subprocess.run(cmd, check=True, capture_output=True)
            receipt = json.loads(out.read_text())
            self.assertEqual(receipt["sources"][0]["candidate_count"], 2)
            self.assertEqual([x["classification"] for x in receipt["sources"][0]["events"]],
                             ["assessment_required", "assessment_required", "triage_only"])
            self.assertFalse(receipt["admission_authorized"])
            self.assertIsNone(receipt["assurance_determination"])
            for raw, indexed in zip(events, receipt["sources"][0]["events"]):
                digest = hashlib.sha256(json.dumps(
                    raw, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                    allow_nan=False).encode("utf-8")).hexdigest()
                self.assertEqual(indexed["source_evidence_sha256"], digest)
            # Re-serialization must not alter the evidence receipt.
            original = out.read_bytes()
            dtg.write_text(json.dumps([dict(reversed(list(e.items()))) for e in events]))
            subprocess.run(cmd, check=True, capture_output=True)
            self.assertEqual(out.read_bytes(), original)
            for bad in (events + [events[0]],
                        [dict(events[1], branch="main")],
                        [dict(events[2], instance="cawg")],
                        [dict(events[0], new="main")],
                        [dict(events[2], event_class="assessment-required")]):
                with self.subTest(bad=bad):
                    out.unlink(missing_ok=True)
                    dtg.write_text(json.dumps(bad))
                    result = subprocess.run(cmd, capture_output=True)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertFalse(out.exists())

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
            a.write_text(json.dumps([event(repository="OpenVTC/dtg-credentials", branch="release/V2",
                assessment_key=monitor.assessment_key("dtg", {"repository": "OpenVTC/dtg-credentials",
                                                               "branch": "release/V2"}))]))
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
