import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import prepare_registry_partition_publication as guard
import publish_assessment_issues as publisher
import stage_registry_source_partition as partition

class RetainedSelectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.ledger = self.root / "ledger.json"
        self.paths = [self.root / name for name in (
            "controller-events.json", "combined-events.json", "dpip-events.json")]
        self.key = guard.KEY
        self.observations = ["0add1f4cc0f048ce6bfc", "29e39a0329123d8839a6",
                             "a60eaffaf3cbc1394553", "acc9772126b1a3820240"]
        self.group = {"assessment_key": self.key, "observed_at": "2026-11-16",
                      "source_observations": [{"finding_id": fid} for fid in self.observations],
                      "body": "Bounded source observation"}
        self.controller = {"assessment_key": "dtg:portfolio:controller:other",
                           "body": "unrelated controller"}
        self.dpip = {"assessment_key": "dtg:portfolio:dpip:other",
                     "body": "unrelated specialist"}
        for path, rows in zip(self.paths, [[self.controller], [self.group], [self.dpip]]):
            path.write_text(json.dumps(rows))
        self.scope = "c"*64
        self.record = {"assessment_key": self.key, "state": "accepted_group",
            "toolkit_issue_url": publisher.TOOLKIT_ISSUE_PREFIX + "272",
            "registry_issue_url": publisher.REGISTRY_ISSUE_PREFIX + "88",
            "monitor_revision": "a"*40, "snapshot_date": "2026-11-16",
            "finding_ids": self.observations,
            "group_sha256": partition.sha(partition.canonical(self.group)),
            "maintainer_scope_sha256": self.scope}
        self.issue = {"number": 88, "state": "open",
            "html_url": self.record["registry_issue_url"],
            "body": guard.CASE_MARK + "\n" +
                guard.GROUP_MARK + self.record["group_sha256"] + " -->\n" +
                self.record["toolkit_issue_url"] + "\n" + "\n".join(self.observations)}
        self.ack = {"id": 123,
                    "html_url": self.record["registry_issue_url"] + "#issuecomment-123",
                    "body": (guard.ACK_MARK + self.record["group_sha256"] + " -->\\n\\n" +
                             "Registry monitored source observation received for administrative case " +
                             self.record["registry_issue_url"]),
                    "user": {"login": "github-actions[bot]", "type": "Bot"}}
        self.accept = {"id": 234, "author_association": "OWNER",
                       "body": guard.SCOPE_MARK + "accept:" + self.scope + " -->",
                       "user": {"login": guard.USER, "type": "User"}}
        self.epoch_scope = []

        self.context = {"GITHUB_ACTIONS": "true",
                        "GITHUB_REF": "refs/heads/main",
                        "GITHUB_REPOSITORY": guard.TK, "GITHUB_SHA": "b"*40}
        self.write_ledger([self.record])

    def write_ledger(self, rows):
        self.ledger.write_text(json.dumps({"schema": "rahp-registry-transfers/v1",
                                           "transfers": rows}))

    def get(self, url):
        if url == guard.API + guard.TK + "/branches/main":
            return {"commit": {"sha": "b"*40}}
        if url == guard.API + guard.REG + "/branches/main":
            return {"commit": {"sha": "a"*40}}
        if url == guard.API + guard.REG + "/issues/88":
            return self.issue
        if url == guard.API + guard.TK + "/issues/272":
            return {"number": 272, "state": "open",
                    "html_url": self.record["toolkit_issue_url"],
                    "body": "<!-- rahp-assessment-key:" + self.key + " -->"}
        if url.startswith(guard.API + guard.REG + "/issues?state=all"):
            return [self.issue]
        if url.startswith(guard.API + guard.REG + "/issues/88/comments?"):
            return [self.ack]
        if url.startswith(guard.API + guard.REG + "/issues/11/comments?"):
            return [self.accept]
        if url.startswith(guard.API + guard.REG + "/issues/77/comments?"):
            return self.epoch_scope
        raise AssertionError("unreviewed GitHub API: " + url)

    def plan(self):
        return guard.plan(self.paths, self.root / "partition", self.ledger,
                          token="readtoken", get=self.get, context=self.context)

    def test_empty_ledger_preserves_all_original_publication_inputs(self):
        self.write_ledger([])
        selection = self.plan()
        self.assertEqual(selection["mode"], "legacy_no_transfer")
        self.assertEqual(selection["paths"], [str(p) for p in self.paths])
        self.assertEqual(selection["held_count"], 0)

    def test_exact_live_ack_routes_only_retained_events(self):
        selection = self.plan()
        self.assertEqual(selection["mode"], "registry_acknowledged_retained")
        self.assertTrue(selection["registry_observation_acknowledged"])
        self.assertFalse(selection["cutover_authorized"])
        self.assertEqual((selection["retained_count"], selection["held_count"]), (2, 1))
        self.assertEqual(json.loads(Path(selection["paths"][0]).read_text()), [self.controller])
        self.assertEqual(json.loads(Path(selection["paths"][1]).read_text()), [])
        self.assertEqual(json.loads(Path(selection["paths"][2]).read_text()), [self.dpip])
        held = json.loads((self.root / "partition/combined-events.json.held.json").read_text())
        self.assertEqual(held[0]["event"], self.group)
        with self.assertRaises(ValueError):
            publisher.preflight_transfer_files(self.paths, self.ledger)

    def test_transferred_group_absent_does_not_block_unrelated_snapshot(self):
        # Later snapshots may not contain the original group at all.
        self.paths[1].write_text("[]")
        for state in ("accepted_group", "reserved_group"):
            with self.subTest(state=state):
                record = dict(self.record)
                if state == "reserved_group":
                    record["state"] = state
                    record["registry_intent_path"] = (
                        "outbox/pending/spec-dependency-2026-11-16.json")
                    record.pop("registry_issue_url")
                    record.pop("maintainer_scope_sha256")
                self.write_ledger([record])
                selected = self.plan()
                self.assertEqual(selected["mode"], "no_current_transfer_event_retained")
                self.assertEqual((selected["held_count"], selected["retained_count"]), (0, 2))
                self.assertFalse(selected["registry_observation_acknowledged"])
                self.assertEqual(json.loads(Path(selected["paths"][0]).read_text()),
                                 [self.controller])
                self.assertEqual(json.loads(Path(selected["paths"][2]).read_text()),
                                 [self.dpip])

    def test_new_source_epoch_is_held_without_inheriting_old_ack(self):
        # The exact November reservation may remain active when the next
        # independently pinned monitor snapshot reports a changed group.
        raw = self.root / "later-original-combined.json"
        later = {**self.group, "observed_at": "2026-11-17",
                 "body": "New monitored source requiring separate qualification"}
        raw.write_text(json.dumps([later]))
        enriched = {**later, "evidence_impact": "uncertain"}
        self.paths[1].write_text(json.dumps([enriched]))
        for state in ("accepted_group", "reserved_group"):
            with self.subTest(state=state):
                record = dict(self.record)
                if state == "reserved_group":
                    record["state"] = state
                    record["registry_intent_path"] = (
                        "outbox/pending/spec-dependency-2026-11-16.json")
                    record.pop("registry_issue_url")
                    record.pop("maintainer_scope_sha256")
                self.write_ledger([record])
                chosen = guard.plan(
                    self.paths, self.root / ("changed-" + state), self.ledger,
                    token="token", get=self.get, context=self.context,
                    source_combined=raw)
                self.assertEqual(chosen["mode"], "changed_group_unqualified_retained")
                self.assertEqual((chosen["retained_count"], chosen["held_count"]), (2, 1))
                self.assertFalse(chosen["registry_observation_acknowledged"])
                self.assertFalse(chosen["cutover_authorized"])
                held = json.loads((self.root / ("changed-" + state) /
                                   "combined-events.json.held.json").read_text())[0]
                self.assertEqual(held["reason"], "unqualified_current_group_observation")
                self.assertEqual(held["event"], enriched)
                self.assertNotEqual(held["source_event_sha256"],
                                    record["group_sha256"])
                self.assertEqual(json.loads(Path(chosen["paths"][0]).read_text()),
                                 [self.controller])
                self.assertEqual(json.loads(Path(chosen["paths"][2]).read_text()),
                                 [self.dpip])
                # Without preserved original source, the new epoch is not
                # qualified to proceed even as a held event.
                with self.assertRaisesRegex(ValueError, "snapshot date"):
                    guard.plan(self.paths, self.root / ("unproven-" + state),
                               self.ledger, token="token", get=self.get,
                               context=self.context)

    def test_changed_epoch_requires_new_authenticated_registry_ack(self):
        raw = self.root / "changed-original-combined.json"
        changed = {**self.group, "observed_at": "2026-11-18",
                   "body": "New source event requiring a new Registry observation"}
        raw.write_text(json.dumps([changed]))
        self.paths[1].write_text(json.dumps([{**changed, "evidence_impact": "uncertain"}]))
        event_sha = partition.sha(partition.canonical(changed))
        self.assertNotEqual(event_sha, self.record["group_sha256"])
        # The first group's old accepted ACK must not authorize this epoch.
        unacknowledged = guard.plan(
            self.paths, self.root / "unacknowledged-epoch", self.ledger,
            token="token", get=self.get, context=self.context,
            source_combined=raw)
        self.assertEqual(unacknowledged["mode"], "changed_group_unqualified_retained")
        self.assertFalse(unacknowledged["registry_observation_acknowledged"])
        self.epoch_scope = [{
            "id": 301, "author_association": "OWNER",
            "user": {"login": guard.USER, "type": "User"},
            "body": guard.EPOCH_SCOPE_MARK + "accept:" + event_sha + " -->"}]
        self.ack["body"] = (
            guard.ACK_MARK + event_sha + " -->\\n\\n" +
            "Registry monitored source observation received for administrative case " +
            self.record["registry_issue_url"] +
            ". Reviewed as a separate source-group reassessment epoch.")
        accepted = guard.plan(
            self.paths, self.root / "accepted-new-epoch", self.ledger,
            token="token", get=self.get, context=self.context, source_combined=raw)
        self.assertEqual(accepted["mode"], "changed_group_acknowledged_retained")
        self.assertEqual(accepted["source_event_sha256"], event_sha)
        self.assertTrue(accepted["registry_observation_acknowledged"])
        self.assertFalse(accepted["cutover_authorized"])
        self.assertEqual((accepted["held_count"], accepted["retained_count"]), (1, 2))
        self.assertEqual(json.loads(Path(accepted["paths"][1]).read_text()), [])
        self.assertEqual(json.loads(Path(accepted["paths"][2]).read_text()), [self.dpip])

    def test_subsequent_epoch_requires_fresh_current_maintainer_scope(self):
        raw = self.root / "newer-original-group.json"
        later = {**self.group, "observed_at": "2026-11-18",
                 "body": "A materially changed source requires renewed owner consent"}
        raw.write_text(json.dumps([later]))
        self.paths[1].write_text(json.dumps([later]))
        digest = partition.sha(partition.canonical(later))
        self.ack["body"] = (guard.ACK_MARK + digest + " -->\\n" +
                            "Registry monitored source observation received for administrative case " +
                            self.record["registry_issue_url"])
        self.epoch_scope = []
        with self.assertRaisesRegex(guard.PartitionError, "scope absent"):
            guard.plan(self.paths, self.root / "no-scope", self.ledger,
                       token="token", get=self.get, context=self.context,
                       source_combined=raw)
        self.epoch_scope = [{
            "id": 10, "author_association": "OWNER",
            "user": {"login": guard.USER, "type": "User"},
            "body": guard.EPOCH_SCOPE_MARK + "accept:" + digest + " -->"},
            {"id": 11, "author_association": "OWNER",
             "user": {"login": guard.USER, "type": "User"},
             "body": guard.EPOCH_SCOPE_MARK + "withdraw:" + digest + " -->"}]
        with self.assertRaisesRegex(guard.PartitionError, "withdrawn"):
            guard.plan(self.paths, self.root / "withdrawn-scope", self.ledger,
                       token="token", get=self.get, context=self.context,
                       source_combined=raw)
        self.epoch_scope[-1]["user"]["login"] = "attacker"
        with self.assertRaisesRegex(guard.PartitionError, "unauthorized"):
            guard.plan(self.paths, self.root / "spoofed-scope", self.ledger,
                       token="token", get=self.get, context=self.context,
                       source_combined=raw)

    def test_new_epoch_cannot_inherit_wrong_or_spoofed_receipt(self):
        raw = self.root / "another-epoch-combined.json"
        changed = {**self.group, "observed_at": "2026-11-18"}
        raw.write_text(json.dumps([changed]))
        self.paths[1].write_text(json.dumps([changed]))
        digest = partition.sha(partition.canonical(changed))
        self.ack["body"] = (
            guard.ACK_MARK + digest + " -->\\n" +
            "Registry monitored source observation received for administrative case " +
            self.record["registry_issue_url"])
        self.ack["user"] = {"login": "attacker", "type": "User"}
        selected = guard.plan(
            self.paths, self.root / "spoofed-epoch", self.ledger,
            token="token", get=self.get, context=self.context, source_combined=raw)
        self.assertFalse(selected["registry_observation_acknowledged"])
        self.assertEqual(selected["mode"], "changed_group_unqualified_retained")
        self.ack["user"] = {"login": "github-actions[bot]", "type": "Bot"}
        self.ack["html_url"] = self.record["registry_issue_url"] + "#issuecomment-999"
        with self.assertRaisesRegex(guard.PartitionError, "canonical GitHub"):
            guard.plan(self.paths, self.root / "wrong-comment-id", self.ledger,
                       token="token", get=self.get, context=self.context,
                       source_combined=raw)

    def test_tampered_journal_source_still_blocks_all_publication(self):
        raw = self.root / "later-original-combined.json"
        later = {**self.group, "observed_at": "2026-11-17"}
        raw.write_text(json.dumps([later]))
        tampered = {**later, "body": "different journal body"}
        self.paths[1].write_text(json.dumps([tampered]))
        with self.assertRaisesRegex(ValueError, "journal-enriched"):
            guard.plan(self.paths, self.root / "tampered-journal", self.ledger,
                       token="token", get=self.get, context=self.context,
                       source_combined=raw)

    def test_journal_enrichment_preserves_approved_raw_source_digest(self):
        raw = self.root / "raw-combined.json"
        raw.write_text(json.dumps([self.group]))
        enriched = {**self.group, "evidence_impact": "uncertain",
                    "journal_findings": [{"finding_id": fid} for fid in self.observations],
                    "theme": "materiality-journal impact=uncertain"}
        self.paths[1].write_text(json.dumps([enriched]))
        self.assertNotEqual(partition.sha(partition.canonical(enriched)),
                            self.record["group_sha256"])
        receipt = guard.plan(self.paths, self.root / "partition", self.ledger,
                             token="token", get=self.get, context=self.context,
                             source_combined=raw)
        self.assertEqual(receipt["mode"], "registry_acknowledged_retained")
        held = json.loads((self.root / "partition/combined-events.json.held.json").read_text())[0]
        self.assertEqual(held["event"], enriched)
        self.assertEqual(held["source_event_sha256"], self.record["group_sha256"])
        self.assertNotEqual(held["event_sha256"], held["source_event_sha256"])
        enriched["body"] = "tampered journal data"
        self.paths[1].write_text(json.dumps([enriched]))
        with self.assertRaisesRegex(ValueError, "journal-enriched"):
            guard.plan(self.paths, self.root / "tampered", self.ledger,
                       token="token", get=self.get, context=self.context,
                       source_combined=raw)

    def test_workflow_preserves_original_before_materiality_enrichment(self):
        wf = (ROOT / ".github/workflows/dtg-portfolio-materiality-handoff.yml").read_text()
        raw = wf.index("Preserve original canonical combined source")
        journal = wf.index("Journal combined-review materiality")
        staged = wf.index("Stage lossless Registry source partitions")
        selected = wf.index("Qualify Registry observation and select exact publication inputs")
        publisher = wf.index("Publish or coalesce portfolio controller")
        self.assertLess(raw, journal)
        self.assertLess(journal, staged)
        self.assertLess(staged, selected)
        self.assertLess(selected, publisher)
        self.assertIn("--source-combined build/dtg-routing/source-combined-events.json", wf)

    def test_reserved_group_publishes_only_unrelated_retained_events(self):
        records = [{
            "assessment_key": self.key, "state": "reserved_group",
            "toolkit_issue_url": self.record["toolkit_issue_url"],
            "registry_intent_path": "outbox/pending/spec-dependency-2026-11-16.json",
            "monitor_revision": self.record["monitor_revision"],
            "snapshot_date": self.record["snapshot_date"],
            "finding_ids": self.observations,
            "group_sha256": self.record["group_sha256"]}]
        self.write_ledger(records)
        selection = self.plan()
        self.assertEqual(selection["mode"], "reserved_group_retained")
        self.assertFalse(selection["registry_observation_acknowledged"])
        self.assertFalse(selection["cutover_authorized"])
        self.assertEqual((selection["held_count"], selection["retained_count"]), (1, 2))
        for index, expected in enumerate(([self.controller], [], [self.dpip])):
            self.assertEqual(json.loads(Path(selection["paths"][index]).read_text()), expected)
        with self.assertRaises(ValueError):
            publisher.preflight_transfer_files(self.paths, self.ledger)
        self.context["GITHUB_SHA"] = "c"*40
        with self.assertRaisesRegex(guard.PartitionError, "branch moved"):
            self.plan()
        self.context["GITHUB_SHA"] = "b"*40
        self.group["body"] = "unaccepted source mutation"
        self.paths[1].write_text(json.dumps([self.group]))
        with self.assertRaisesRegex(ValueError, "digest"):
            self.plan()

    def test_legacy_accepted_without_group_contract_is_not_selected(self):
        self.write_ledger([{
            "assessment_key": self.key, "state": "accepted",
            "toolkit_issue_url": self.record["toolkit_issue_url"],
            "registry_issue_url": self.record["registry_issue_url"]}])
        with self.assertRaisesRegex(guard.PartitionError, "blocks"):
            self.plan()

    def test_missing_or_spoofed_current_ack_refuses_publication(self):
        self.ack["body"] = "no current observation"
        with self.assertRaisesRegex(guard.PartitionError, "acknowledgment"):
            self.plan()
        self.ack["body"] = (guard.ACK_MARK + self.record["group_sha256"] + " -->\\n\\n" +
                             "Registry monitored source observation received for administrative case " +
                             self.record["registry_issue_url"])
        self.ack["user"] = {"login": "untrusted", "type": "User"}
        with self.assertRaisesRegex(guard.PartitionError, "acknowledgment"):
            self.plan()

    def test_duplicate_or_noncanonical_ack_never_authorizes_group_suppression(self):
        acknowledged = dict(self.ack)
        for modified in (
            {**acknowledged, "id": True},
            {**acknowledged, "id": 0},
            {**acknowledged, "html_url": self.record["registry_issue_url"] + "#issuecomment-999"},
            {**acknowledged, "html_url": publisher.TOOLKIT_ISSUE_PREFIX + "272#issuecomment-123"},
            {**acknowledged, "body": guard.ACK_MARK + self.record["group_sha256"] + " -->"},
        ):
            with self.subTest(modified=modified):
                previous = self.ack
                self.ack = modified
                with self.assertRaises(guard.PartitionError):
                    self.plan()
                self.ack = previous

        original = self.get
        def duplicate(url):
            if url.startswith(guard.API + guard.REG + "/issues/88/comments?"):
                return [self.ack, {**self.ack, "id": 124,
                                   "html_url": self.record["registry_issue_url"] + "#issuecomment-124"}]
            return original(url)
        with self.assertRaisesRegex(guard.PartitionError, "unique authenticated"):
            guard.plan(self.paths, self.root / "dupe", self.ledger,
                       token="token", get=duplicate, context=self.context)

    def test_historical_toolkit_issue_namespace_and_exact_marker_must_resolve(self):
        original = self.get
        for substituted in (
            {"number": 88, "state": "open",
             "html_url": publisher.REGISTRY_ISSUE_PREFIX + "88",
             "body": "<!-- rahp-assessment-key:" + self.key + " -->"},
            {"number": 272, "state": "open",
             "html_url": publisher.TOOLKIT_ISSUE_PREFIX + "272",
             "body": "<!-- rahp-assessment-key:dtg:wrong-owner -->"},
            {"number": 272, "state": "open",
             "html_url": publisher.TOOLKIT_ISSUE_PREFIX + "999",
             "body": "<!-- rahp-assessment-key:" + self.key + " -->"},
        ):
            with self.subTest(substituted=substituted):
                def wrong(url):
                    if url == guard.API + guard.TK + "/issues/272":
                        return substituted
                    return original(url)
                with self.assertRaisesRegex(guard.PartitionError, "historical Toolkit"):
                    guard.plan(self.paths, self.root / "wrong-owner",
                               self.ledger, token="token", get=wrong,
                               context=self.context)

    def test_withdrawal_and_duplicate_owner_refuse_publication(self):
        self.accept["body"] = guard.SCOPE_MARK + "withdraw:" + self.scope + " -->"
        with self.assertRaisesRegex(guard.PartitionError, "withdrawn"):
            self.plan()
        self.accept["body"] = guard.SCOPE_MARK + "accept:" + self.scope + " -->"
        self.issue["body"] = guard.CASE_MARK + "\nnot the same source"
        with self.assertRaisesRegex(guard.PartitionError, "exact group"):
            self.plan()

    def test_changed_event_and_main_context_fail_closed(self):
        self.group["body"] = "new unacknowledged observation"
        self.paths[1].write_text(json.dumps([self.group]))
        with self.assertRaisesRegex(ValueError, "digest"):
            self.plan()
        self.setUp()
        self.context["GITHUB_SHA"] = "c"*40
        with self.assertRaisesRegex(guard.PartitionError, "branch moved"):
            self.plan()

    def test_accepted_record_requires_owner_and_scope_fields(self):
        for field in ("registry_issue_url", "maintainer_scope_sha256",
                      "group_sha256", "finding_ids"):
            with self.subTest(field=field):
                broken = {k:v for k,v in self.record.items() if k != field}
                self.write_ledger([broken])
                with self.assertRaises(ValueError):
                    publisher.load_transfer_keys(self.ledger)
        self.write_ledger([self.record])

if __name__ == "__main__":
    unittest.main()
