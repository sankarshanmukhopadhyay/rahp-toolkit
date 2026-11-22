import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "monitor_branch_guard", ROOT / "tools/check_monitor_state_branches.py"
)
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)

BRANCH = "automation/instance-monitor-44527955312-1"
SHA = "a" * 40


def ref(sha=SHA, name=BRANCH):
    return {"ref": "refs/heads/" + name, "object": {"sha": sha}}


def pull(sha=SHA, name=BRANCH, state="closed", merged_at="2026-11-19T12:00:00Z"):
    return {"head": {"repo": {"full_name": guard.REPOSITORY}, "ref": name, "sha": sha},
            "state": state, "merged_at": merged_at}


class MonitorStateBranchGuardTests(unittest.TestCase):
    def test_no_pending_branches_is_safe(self):
        self.assertEqual(guard.qualify([], lambda url: self.fail("unexpected API")), 0)

    def test_exact_retained_squash_merged_branch_is_safe(self):
        self.assertEqual(guard.qualify([ref()], lambda url: [pull()]), 1)

    def test_signed_branch_without_pull_request_blocks_republication(self):
        with self.assertRaisesRegex(guard.StateBranchError, "orphaned"):
            guard.qualify([ref()], lambda url: [])

    def test_open_state_pr_blocks_republication(self):
        with self.assertRaisesRegex(guard.StateBranchError, "unaccepted"):
            guard.qualify([ref()], lambda url: [pull(state="open", merged_at=None)])

    def test_closed_unmerged_pr_blocks_republication(self):
        with self.assertRaisesRegex(guard.StateBranchError, "unaccepted"):
            guard.qualify([ref()], lambda url: [pull(merged_at=None)])

    def test_reused_branch_commit_is_not_prior_merge_authority(self):
        with self.assertRaisesRegex(guard.StateBranchError, "unaccepted"):
            guard.qualify([ref()], lambda url: [pull(sha="b" * 40)])

    def test_wrong_repository_is_not_authoritative(self):
        candidate = pull()
        candidate["head"]["repo"]["full_name"] = "other/repo"
        with self.assertRaisesRegex(guard.StateBranchError, "unaccepted"):
            guard.qualify([ref()], lambda url: [candidate])

    def test_ambiguous_pr_or_duplicate_ref_fails_closed(self):
        with self.assertRaises(guard.StateBranchError):
            guard.qualify([ref()], lambda url: [pull(), pull()])
        with self.assertRaises(guard.StateBranchError):
            guard.qualify([ref(), ref()], lambda url: [pull()])

    def test_malformed_or_unknown_listing_fails_closed(self):
        for bad in (None, {}, [{"ref": "refs/heads/main", "object": {"sha": SHA}}],
                    [ref(sha="not-a-sha")]):
            with self.subTest(bad=bad), self.assertRaises(guard.StateBranchError):
                guard.qualify(bad, lambda url: [pull()])

    def test_actual_workflow_guards_before_external_write_and_persist(self):
        source = (ROOT / ".github/workflows/instance-monitor-main.yml").read_text()
        publisher = source.split("\n  publish_external:", 1)[1].split("\n  persist:", 1)[0]
        persist = source.split("\n  persist:", 1)[1].split("\n  local_incidents:", 1)[0]
        invocation = "python3 tools/check_monitor_state_branches.py"
        self.assertIn(invocation, publisher)
        self.assertLess(publisher.index(invocation), publisher.index("Publish DTG assessment issues"))
        self.assertIn(invocation, persist)
        self.assertLess(persist.index(invocation), persist.index("Stage monitored state under protected-main review"))


if __name__ == "__main__":
    unittest.main()
