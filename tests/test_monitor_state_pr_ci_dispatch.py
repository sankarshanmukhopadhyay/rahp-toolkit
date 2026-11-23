"""Contract checks for GITHUB_TOKEN-created monitor-state PR validation."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1] / ".github" / "workflows"


class MonitorStatePRCIDispatchTests(unittest.TestCase):
    def test_app_settings_preflight_precedes_monitor_observation_and_all_issue_writes(self):
        text = (ROOT / "instance-monitor-main.yml").read_text()
        monitor = text.split("\n  monitor:", 1)[1].split("\n  publish_external:", 1)[0]
        publisher = text.split("\n  publish_external:", 1)[1].split("\n  persist:", 1)[0]
        for required in (
            "Require state-PR GitHub App configuration before observation and publication",
            "STATE_APP_ID: ${{ vars.RAHP_STATE_APP_ID }}",
            "STATE_APP_KEY: ${{ secrets.RAHP_STATE_APP_PRIVATE_KEY }}",
            '[[ "${STATE_APP_ID:-}" =~ ^[1-9][0-9]*$ ]]',
            '[ -z "${STATE_APP_KEY:-}" ]',
            "abort before external issue publication",
        ):
            self.assertIn(required, monitor)
        self.assertLess(monitor.index("Require state-PR GitHub App configuration"),
                        monitor.index("Authenticate scoped App installation"))
        self.assertLess(monitor.index("Authenticate scoped App installation"),
                        monitor.index("Check DTG instance"))
        self.assertEqual(monitor.count("actions/create-github-app-token@f418cff399f7aef4c2f0ad47e25ca7a6abbdd6fc"), 1)
        self.assertIn("permission-contents: write", monitor)
        self.assertIn("permission-pull-requests: write", monitor)
        self.assertIn("repositories: rahp-toolkit", monitor)
        self.assertIn("needs: monitor", text.split("\n  publish_external:", 1)[1])
        self.assertIn("Publish DTG assessment issues", publisher)

    def test_native_pr_checks_use_scoped_app_token(self):
        text = (ROOT / "instance-monitor-main.yml").read_text()
        persist = text.split("\n  persist:", 1)[1].split("\n  local_incidents:", 1)[0]
        for required in (
            "persist-credentials: false",
            "actions/create-github-app-token@f418cff399f7aef4c2f0ad47e25ca7a6abbdd6fc",
            "app-id: ${{ vars.RAHP_STATE_APP_ID }}",
            "private-key: ${{ secrets.RAHP_STATE_APP_PRIVATE_KEY }}",
            "repositories: rahp-toolkit",
            "permission-contents: write",
            "permission-pull-requests: write",
            "GH_TOKEN: ${{ steps.state-app.outputs.token }}",
            "APP_SLUG: ${{ steps.state-app.outputs.app-slug }}",
            'bot_login="${APP_SLUG}[bot]"',
            'git config user.name "$bot_login"',
            'git commit -s -m "chore(assurance): stage monitored instance revisions"',
            "credential.helper=",
            'gh pr create --base main',
            'pr_head" != "$(git rev-parse HEAD)"',
        ):
            with self.subTest(required=required):
                self.assertIn(required, persist)
        self.assertNotIn("GH_TOKEN: ${{ github.token }}", persist)
        self.assertNotIn("actions: write", persist)
        self.assertNotIn("gh workflow run validate.yml", persist)
        self.assertNotIn("gh workflow run pages.yml", persist)
        self.assertLess(persist.index("persist-credentials: false"),
                        persist.index("Generate repository-scoped state PR credential"))
        self.assertLess(persist.index("Verify and restore pinned observation snapshot"),
                        persist.index("Generate repository-scoped state PR credential"))
        self.assertLess(persist.index('git commit -s -m'),
                        persist.index("credential.helper="))
        self.assertLess(persist.index("credential.helper="),
                        persist.index("gh pr create --base main"))

    def test_app_identity_is_required_and_no_secret_is_logged_or_stored(self):
        text = (ROOT / "instance-monitor-main.yml").read_text()
        persist = text.split("\n  persist:", 1)[1].split("\n  local_incidents:", 1)[0]
        self.assertIn('if [ -z "${GH_TOKEN:-}" ] || [ -z "${APP_SLUG:-}" ]; then', persist)
        self.assertIn('bot_id="$(gh api "/users/${bot_login}" --jq \'.id\')"', persist)
        self.assertIn('git config user.email "${bot_id}+${bot_login}@users.noreply.github.com"', persist)
        self.assertNotIn("git remote set-url", persist)
        self.assertNotIn("echo \"$GH_TOKEN\"", persist)
        self.assertNotIn("git -c http.", persist)

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
