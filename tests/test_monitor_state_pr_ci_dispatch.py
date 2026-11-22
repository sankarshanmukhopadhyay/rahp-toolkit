"""Contract checks for GITHUB_TOKEN-created monitor-state PR validation."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1] / ".github" / "workflows"


class MonitorStatePRCIDispatchTests(unittest.TestCase):
    def test_monitor_dispatches_existing_required_check_workflows_after_pr_creation(self):
        text = (ROOT / "instance-monitor-main.yml").read_text()
        persist = text.split("\n  persist:", 1)[1].split("\n  local_incidents:", 1)[0]
        self.assertIn('pr_head" != "$(git rev-parse HEAD)"', persist)
        self.assertIn('gh workflow run validate.yml --ref "$branch" -f state_pr_number="$pr_number"', persist)
        self.assertIn('gh workflow run pages.yml --ref "$branch" -f state_pr_number="$pr_number"', persist)
        self.assertLess(persist.index('gh pr create --base main'),
                        persist.index('gh workflow run validate.yml'))
        self.assertLess(persist.index('gh workflow run validate.yml'),
                        persist.index('echo "disposition=staged_pending_review"'))
        self.assertNotIn("pull-requests: write\n      issues: write", persist)

    def test_dco_dispatch_is_pinned_to_one_open_main_pr_and_exact_head(self):
        text = (ROOT / "validate.yml").read_text()
        self.assertIn("state_pr_number:", text)
        dco = text.split("\n  dco:", 1)[1].split("\n  impact:", 1)[0]
        for required in ("github.event_name == 'workflow_dispatch'",
                         "inputs.state_pr_number != ''",
                         '[[ "$GITHUB_REF" == refs/heads/automation/instance-monitor-* ]]',
                         'gh api "repos/${GITHUB_REPOSITORY}/pulls/${PR_NUMBER}"',
                         '"$state" == open', '"$base" == main',
                         '"$owner" == "$GITHUB_REPOSITORY"',
                         '"$head_sha" == "$GITHUB_SHA"',
                         "bash tools/dco-check.sh pr"):
            self.assertIn(required, dco)

    def test_dispatched_state_pr_build_cannot_publish_pages(self):
        text = (ROOT / "pages.yml").read_text()
        self.assertIn("state_pr_number:", text)
        predicate = ("github.event_name != 'pull_request' && "
                     "(github.event_name != 'workflow_dispatch' || inputs.state_pr_number == '')")
        self.assertEqual(text.count("if: " + predicate), 3)
        self.assertIn("if: " + predicate + "\n        uses: actions/upload-pages-artifact", text)
        self.assertIn("  deploy:\n    if: " + predicate, text)
        self.assertIn("  observe_published:\n    if: " + predicate, text)


if __name__ == "__main__":
    unittest.main()
