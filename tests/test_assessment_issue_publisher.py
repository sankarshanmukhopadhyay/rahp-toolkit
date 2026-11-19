from __future__ import annotations

import importlib.util
from io import BytesIO
from pathlib import Path
import unittest
from unittest.mock import patch
import urllib.error

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "publish_assessment_issues.py"
SPEC = importlib.util.spec_from_file_location("publish_assessment_issues", MODULE_PATH)
assert SPEC and SPEC.loader
publisher = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(publisher)


class AssessmentIssuePublisherTests(unittest.TestCase):
    def setUp(self) -> None:
        self.key = "dtg:portfolio:combined:delegation-credential-composition"
        self.issues = [
            {
                "state": "closed",
                "number": 584,
                "body": f"<!-- rahp-assessment-key:{self.key} -->",
            },
            {
                "state": "closed",
                "number": 611,
                "body": f"<!-- rahp-assessment-key:{self.key} -->",
            },
        ]

    def test_actions_issue_publisher_rejects_off_main_and_foreign_refs(self) -> None:
        base = {
            "GITHUB_ACTIONS": "true",
            "GITHUB_REPOSITORY": publisher.CANONICAL_RAHP_ISSUE_REPOSITORY,
            "GITHUB_REF": "refs/heads/main",
            "GITHUB_SHA": "a" * 40,
        }
        publisher.enforce_actions_main_publication_context(base)
        # Local CLI remains a separate operator permission question.
        publisher.enforce_actions_main_publication_context({})
        cases = [
            {**base, "GITHUB_REF": "refs/heads/assurance/stale-2026"},
            {**base, "GITHUB_REF": "refs/tags/v1.0.0"},
            {**base, "GITHUB_REF": "refs/pull/1/merge"},
            {**base, "GITHUB_REPOSITORY": "attacker/fork"},
            {**base, "GITHUB_SHA": "main"},
            {**base, "GITHUB_SHA": ""},
            {**base, "GITHUB_REF": ""},
        ]
        for context in cases:
            with self.subTest(context=context), self.assertRaisesRegex(
                    ValueError, "canonical Toolkit main"):
                publisher.enforce_actions_main_publication_context(context)

    def test_registry_transfer_guard_honors_committed_source_reservation(self) -> None:
        # The authoritative ledger is now deliberately source-scoped, rather
        # than empty. Unrelated RAHP publication must continue, but the
        # reserved combined group must never be published or coalesced here.
        keys = publisher.load_transfer_keys(publisher.TRANSFER_LEDGER)
        self.assertEqual(keys, {"dtg:portfolio:combined:spec-dependency-alignment"})
        publisher.enforce_registry_transfer_boundary([{"assessment_key": self.key}], keys)
        with self.assertRaisesRegex(ValueError, "Registry-owned"):
            publisher.enforce_registry_transfer_boundary(
                [{"assessment_key": "dtg:portfolio:combined:spec-dependency-alignment"}], keys)
        with self.assertRaisesRegex(ValueError, "Registry-owned"):
            publisher.enforce_registry_transfer_boundary(
                [{"assessment_key": self.key,
                  "related_assessment_key": "dtg:portfolio:combined:spec-dependency-alignment"}],
                keys)

    def test_reserved_transfer_blocks_toolkit_before_successor_exists(self) -> None:
        import json
        import tempfile
        key = "dtg:portfolio:combined:reserved-example"
        reservation = {
            "assessment_key": key,
            "toolkit_issue_url": "https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1194",
            "registry_intent_path": "outbox/pending/transfer-example.json",
            "source_revision": "a" * 40,
            "finding_id": "finding-12345",
            "state": "reserved",
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "transfers.json"
            path.write_text(json.dumps({"schema": "rahp-registry-transfers/v1", "transfers": [reservation]}))
            self.assertEqual(publisher.load_transfer_keys(path), {key})
            with self.assertRaisesRegex(ValueError, "Registry-owned"):
                publisher.enforce_registry_transfer_boundary([{"assessment_key": key}], {key})
            invalid = (
                {**reservation, "registry_intent_path": "../unexpected.json"},
                {**reservation, "source_revision": "main"},
                {**reservation, "finding_id": ""},
                {**reservation, "registry_issue_url": "https://github.com/example/issues/1"},
            )
            for changed in invalid:
                with self.subTest(changed=changed), self.assertRaises(ValueError):
                    path.write_text(json.dumps({"schema": "rahp-registry-transfers/v1", "transfers": [changed]}))
                    publisher.load_transfer_keys(path)

    def test_registry_transfer_rejects_exact_and_related_key_before_writes(self) -> None:
        for event in ({"assessment_key": self.key},
                      {"assessment_key": "dtg:other-case", "related_assessment_key": self.key}):
            with self.subTest(event=event), self.assertRaisesRegex(ValueError, "Registry-owned"):
                publisher.enforce_registry_transfer_boundary([event], {self.key})

    def test_registry_transfer_rejects_malformed_and_duplicate_ledger(self) -> None:
        import json
        import tempfile
        good = {"assessment_key": self.key,
                "toolkit_issue_url": "https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1203",
                "registry_issue_url": "https://github.com/sankarshanmukhopadhyay/rahp-assessment-registry/issues/4",
                "state": "accepted"}
        bad = [
            {"schema": "rahp-registry-transfers/v1", "transfers": [good, good]},
            {"schema": "rahp-registry-transfers/v1", "transfers": [{**good, "state": "proposed"}]},
            {"schema": "rahp-registry-transfers/v1", "transfers": [{**good, "registry_issue_url": "https://github.com/evil/issues/1"}]},
            {"schema": "rahp-registry-transfers/v1", "transfers": [{**good, "extra": True}]},
            {"schema": "different", "transfers": []},
        ]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "transfers.json"
            path.write_text(json.dumps({"schema": "rahp-registry-transfers/v1", "transfers": [good]}))
            self.assertEqual(publisher.load_transfer_keys(path), {self.key})
            for payload in bad:
                with self.subTest(payload=payload), self.assertRaises(ValueError):
                    path.write_text(json.dumps(payload))
                    publisher.load_transfer_keys(path)

    def test_preflight_blocks_later_batch_without_network_or_publishing(self) -> None:
        import json
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ledger = root / "transfers.json"
            key = "dtg:portfolio:combined:transferred-example"
            ledger.write_text(json.dumps({
                "schema": "rahp-registry-transfers/v1",
                "transfers": [{
                    "assessment_key": key,
                    "toolkit_issue_url": "https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1203",
                    "registry_issue_url": "https://github.com/sankarshanmukhopadhyay/rahp-assessment-registry/issues/4",
                    "state": "accepted",
                }],
            }))
            early = root / "controller.json"
            later = root / "combined.json"
            early.write_text(json.dumps([{"assessment_key": "dtg:portfolio:controller:sample"}]))
            later.write_text(json.dumps([{"assessment_key": "dtg:other-case", "related_assessment_key": key}]))
            with patch.object(publisher, "request", side_effect=AssertionError("no GitHub calls")):
                with self.assertRaisesRegex(ValueError, "Registry-owned"):
                    publisher.preflight_transfer_files([early, later], ledger)
                later.write_text("[]")
                self.assertEqual(publisher.preflight_transfer_files([early, later], ledger), 1)

    def test_preflight_rejects_missing_malformed_and_non_array_batches(self) -> None:
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "events.json"
            ledger = publisher.TRANSFER_LEDGER
            with self.assertRaises(FileNotFoundError):
                publisher.preflight_transfer_files([path], ledger)
            for content in ('{"assessment_key":"x"}', 'not-json', '[null]'):
                path.write_text(content)
                with self.subTest(content=content), self.assertRaises((ValueError, TypeError)):
                    publisher.preflight_transfer_files([path], ledger)

    def test_policy_validator_only_exempts_standalone_transfer_preflight(self) -> None:
        policy = (ROOT / "tools/validate_issue_publication_policy.py").read_text(encoding="utf-8")
        self.assertIn('re.match(r"^--(?:check-transfers|verify-transfer-rollback)(?:\\s|$)", fragment.lstrip())', policy)
        self.assertIn('if f\'--repository "{CANONICAL}"\' not in fragment:', policy)

    def test_workflow_preflights_all_dtg_batches_before_first_issue_write(self) -> None:
        path = ROOT / ".github/workflows/dtg-materiality-main.yml"
        text = path.read_text(encoding="utf-8")
        selector = text.index("name: Qualify Registry observation and select exact publication inputs")
        preflight = text.index("name: Preflight all DTG publication batches against Registry transfer ledger")
        first_write = text.index("name: Publish or coalesce portfolio controller")
        self.assertLess(selector, preflight)
        self.assertLess(preflight, first_write)
        selector_block = text[selector:preflight]
        preflight_block = text[preflight:first_write]
        # All three original batches are source-qualified by the selection
        # step; preflight and effectful publishers consume precisely its
        # selected paths, not an unguarded original batch.
        for file in ("controller-events.json", "combined-events.json", "dpip-events.json"):
            self.assertIn(file, selector_block)
        for name in ("controller", "combined", "dpip"):
            self.assertIn("needs.handoff.outputs." + name, preflight_block)
            self.assertIn("--events " + "${{ needs.handoff.outputs." +
                          name + " }}", text[first_write:])
        self.assertIn("--check-transfers", preflight_block)
        self.assertIn("publish_external:", text)
        self.assertIn("permissions:\\n      contents: read\\n      issues: write", text)
        self.assertIn("issues: read", text[:text.index("  publish_external:")])
        self.assertIn("actions/download-artifact@v7", text)
        self.assertIn("Refuse source drift before any issue mutation", text)
        self.assertLess(text.index("Retain exact source-qualified publication inputs"), first_write)


    def test_live_fence_rejects_stale_writer_after_reservation(self) -> None:
        import base64
        import json
        key = "dtg:portfolio:combined:spec-dependency-alignment"
        ledger = {"schema": "rahp-registry-transfers/v1", "transfers": [{
            "state": "reserved_group", "assessment_key": key,
            "toolkit_issue_url": publisher.TOOLKIT_ISSUE_PREFIX + "272",
            "registry_intent_path": "outbox/pending/spec-dependency-2026-11-16.json",
            "monitor_revision": "a"*40, "snapshot_date": "2026-11-16",
            "finding_ids": ["a"*20], "group_sha256": "b"*64
        }]}
        def fake(method, url, token, payload=None):
            if url.endswith("/branches/main"):
                return {"commit": {"sha": "a"*40}}
            if "/contents/instances/dtg/registry-transfers.json?" in url:
                return {"encoding": "base64", "content": base64.b64encode(
                    json.dumps(ledger).encode()).decode()}
            raise AssertionError("unexpected API " + url)
        with patch.object(publisher, "request", side_effect=fake):
            with self.assertRaisesRegex(ValueError, "Registry-owned"):
                publisher.enforce_live_transfer_boundary({"assessment_key": key}, "token")
            publisher.enforce_live_transfer_boundary(
                {"assessment_key": "dtg:portfolio:controller:unrelated"}, "token")

    def test_live_fence_rejects_main_head_drift(self) -> None:
        import base64
        import json
        heads = iter(["a"*40, "b"*40])
        def fake(method, url, token, payload=None):
            if url.endswith("/branches/main"):
                return {"commit": {"sha": next(heads)}}
            return {"encoding": "base64", "content": base64.b64encode(
                json.dumps({"schema": "rahp-registry-transfers/v1",
                            "transfers": []}).encode()).decode()}
        with patch.object(publisher, "request", side_effect=fake):
            with self.assertRaisesRegex(ValueError, "main changed"):
                publisher.enforce_live_transfer_boundary(
                    {"assessment_key": "dtg:portfolio:controller:other"}, "token")

    def test_live_fence_rejects_unavailable_authority(self) -> None:
        with patch.object(publisher, "request", return_value={}):
            with self.assertRaisesRegex(ValueError, "authority unavailable"):
                publisher.enforce_live_transfer_boundary(
                    {"assessment_key": "dtg:portfolio:controller:other"}, "token")

    def test_accepted_transfer_cannot_be_deleted_or_replaced(self) -> None:
        key = "dtg:portfolio:combined:spec-dependency-alignment"
        original = {"schema": "rahp-registry-transfers/v1", "transfers": [{
            "state": "accepted_group", "assessment_key": key,
            "toolkit_issue_url": publisher.TOOLKIT_ISSUE_PREFIX + "272",
            "registry_issue_url": publisher.REGISTRY_ISSUE_PREFIX + "88",
            "monitor_revision": "a"*40, "snapshot_date": "2026-11-16",
            "finding_ids": ["a"*20], "group_sha256": "b"*64,
            "maintainer_scope_sha256": "c"*64
        }]}
        publisher.enforce_accepted_transfer_monotonicity(original, original)
        with self.assertRaisesRegex(ValueError, "cannot be removed"):
            publisher.enforce_accepted_transfer_monotonicity(
                original, {"schema": "rahp-registry-transfers/v1", "transfers": []})
        with self.assertRaisesRegex(ValueError, "invalid registry transfer ledger schema"):
            publisher.enforce_accepted_transfer_monotonicity(
                original, {"**": "not a valid ledger"})
        changed = {"schema": "rahp-registry-transfers/v1", "transfers": [
            {**original["transfers"][0], "registry_issue_url":
             publisher.REGISTRY_ISSUE_PREFIX + "89"}]}
        with self.assertRaisesRegex(ValueError, "cannot be removed"):
            publisher.enforce_accepted_transfer_monotonicity(original, changed)

    def test_reserved_group_cannot_be_removed_after_unobserved_registry_post(self) -> None:
        reservation = {"assessment_key": "dtg:portfolio:combined:spec-dependency-alignment",
                       "state": "reserved_group",
                       "toolkit_issue_url": publisher.TOOLKIT_ISSUE_PREFIX + "272",
                       "registry_intent_path": "outbox/pending/spec-dependency-2026-11-16.json",
                       "monitor_revision": "a"*40, "snapshot_date": "2026-11-16",
                       "finding_ids": ["a"*20], "group_sha256": "b"*64}
        baseline = {"schema": "rahp-registry-transfers/v1", "transfers": [reservation]}
        empty = {"schema": "rahp-registry-transfers/v1", "transfers": []}
        with self.assertRaisesRegex(ValueError, "cannot be removed"):
            publisher.enforce_accepted_transfer_monotonicity(baseline, empty)
        accepted = {name: value for name, value in reservation.items()
                    if name != "registry_intent_path"}
        accepted["state"] = "accepted_group"
        accepted["registry_issue_url"] = publisher.REGISTRY_ISSUE_PREFIX + "88"
        accepted["maintainer_scope_sha256"] = "c"*64
        publisher.enforce_accepted_transfer_monotonicity(
            baseline, {"schema": "rahp-registry-transfers/v1", "transfers": [accepted]})
        for field, value in (("monitor_revision", "f"*40),
                             ("group_sha256", "f"*64),
                             ("toolkit_issue_url", publisher.TOOLKIT_ISSUE_PREFIX + "273")):
            with self.subTest(field=field):
                with self.assertRaisesRegex(ValueError, "cannot be removed"):
                    publisher.enforce_accepted_transfer_monotonicity(
                        baseline, {"schema": "rahp-registry-transfers/v1",
                                   "transfers": [{**accepted, field: value}]})

    def test_nonaccepted_ledger_retains_legacy_compatibility(self) -> None:
        baseline = {"schema": "rahp-registry-transfers/v1", "transfers": []}
        publisher.enforce_accepted_transfer_monotonicity(baseline, baseline)

    def test_api_errors_never_expose_response_body(self) -> None:
        secret_body = b'{"message":"private request detail"}'
        error = urllib.error.HTTPError(
            "https://api.github.com/repos/example/private",
            422,
            "Unprocessable Entity",
            {"X-GitHub-Request-Id": "request-123"},
            BytesIO(secret_body),
        )
        with patch.object(publisher.urllib.request, "urlopen", side_effect=error):
            with self.assertRaises(publisher.GitHubAPIError) as caught:
                publisher.request("POST", "https://api.github.com/repos/example/private", "token")
        self.assertNotIn("private request detail", str(caught.exception))
        self.assertNotIn(secret_body.decode(), str(caught.exception))
        self.assertIn("HTTP 422", str(caught.exception))
        self.assertEqual(caught.exception.request_id, "request-123")

    def test_earliest_closed_owner_survives_duplicate_history(self) -> None:
        index = publisher.issues_by_key(self.issues)
        self.assertEqual(index["closed"][self.key]["number"], 584)

    def test_repeated_observation_resolves_to_closed_owner(self) -> None:
        index = publisher.issues_by_key(self.issues)
        owner, state = publisher.resolve_owner(index, self.key)
        self.assertIsNotNone(owner)
        self.assertEqual(owner["number"], 584)
        self.assertEqual(state, "closed")

    def test_closed_owner_does_not_reopen_without_explicit_trigger(self) -> None:
        event = {"assessment_key": self.key, "observed_at": "2026-09-11"}
        self.assertFalse(publisher.should_reopen_closed_owner(event))

    def test_closed_owner_reopens_only_on_governed_trigger(self) -> None:
        base = {"assessment_key": self.key, "observed_at": "2026-09-12"}
        self.assertTrue(
            publisher.should_reopen_closed_owner(
                {**base, "invalidation_reason": "authoritative semantic delta invalidates prior proposition evidence"}
            )
        )
        self.assertTrue(
            publisher.should_reopen_closed_owner(
                {**base, "retest_reason": "new negative evidence intersects prior terminal conclusion"}
            )
        )
        self.assertTrue(publisher.should_reopen_closed_owner({**base, "reopen_closed_owner": True}))


    def test_existing_issue_scan_does_not_drop_owner_beyond_five_pages(self) -> None:
        calls: list[int] = []
        canonical = {
            "state": "closed",
            "number": 410,
            "body": "<!-- rahp-assessment-key:cawg:issue:decentralized-identity/cawg-identity-assertion#275 -->",
        }

        def fake_request(method, url, token, payload=None):
            page = int(url.rsplit("page=", 1)[1])
            calls.append(page)
            if page <= 5:
                return [{"number": page * 100 + i, "state": "closed", "body": ""} for i in range(100)]
            if page == 6:
                filler = [{"number": 600 + i, "state": "closed", "body": ""} for i in range(99)]
                return filler + [canonical]
            return []

        original = publisher.request
        publisher.request = fake_request
        try:
            issues = publisher.existing_issues("sankarshanmukhopadhyay/rahp-toolkit", "token")
        finally:
            publisher.request = original

        self.assertIn(canonical, issues)
        self.assertEqual(calls, [1, 2, 3, 4, 5, 6, 7])

        index = publisher.issues_by_key(issues)
        owner, state = publisher.resolve_owner(
            index,
            "cawg:issue:decentralized-identity/cawg-identity-assertion#275",
        )
        self.assertIsNotNone(owner)
        self.assertEqual(owner["number"], 410)
        self.assertEqual(state, "closed")

    def test_open_owner_is_preferred_when_both_states_exist(self) -> None:
        issues = self.issues + [
            {
                "state": "open",
                "number": 622,
                "body": f"<!-- rahp-assessment-key:{self.key} -->",
            }
        ]
        index = publisher.issues_by_key(issues)
        owner, state = publisher.resolve_owner(index, self.key)
        self.assertEqual(owner["number"], 622)
        self.assertEqual(state, "open")


if __name__ == "__main__":
    unittest.main()
