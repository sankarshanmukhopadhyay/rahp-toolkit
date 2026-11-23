from __future__ import annotations

import subprocess
import sys
import unittest

import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "tools" / "validate_instance_watch_contract.py"


class InstanceWatchContractTests(unittest.TestCase):
    def test_incremental_issue_writers_are_separate_after_exact_observation(self):
        workflow = ROOT / ".github/workflows/instance-monitor-main.yml"
        source = workflow.read_text(encoding="utf-8")
        config = yaml.load(source, Loader=yaml.BaseLoader)
        jobs = config["jobs"]
        self.assertEqual(set(jobs), {
            "monitor", "publish_external", "persist", "local_incidents",
        })
        self.assertEqual(config["permissions"], {"contents": "read", "issues": "read"})
        expected = {
            "monitor": (None, {"contents": "read", "issues": "read"}),
            "publish_external": ("monitor", {
                "contents": "read", "issues": "write", "actions": "read", "pull-requests": "read",
            }),
            "persist": ("publish_external", {
                "contents": "read", "issues": "read", "pull-requests": "read",
            }),
            "local_incidents": ("persist", {
                "contents": "read", "issues": "write",
            }),
        }
        for name, (needs, permissions) in expected.items():
            job = jobs[name]
            self.assertEqual(job.get("needs"), needs, name)
            self.assertEqual(job.get("permissions", config["permissions"]), permissions, name)
            self.assertIn("refs/heads/main", job["if"], name)
        def steps(name):
            return "\n".join(s.get("run", "") for s in jobs[name]["steps"])
        observation = steps("monitor")
        publisher = steps("publish_external")
        persisted = steps("persist")
        local = steps("local_incidents")
        self.assertNotIn("publish_assessment_issues.py", observation)
        self.assertNotIn("publish_dtg_controller_incidents.py", observation)
        self.assertEqual(publisher.count("publish_assessment_issues.py"), 4)
        self.assertIn("dtg_repository_review_worker.py", publisher)
        self.assertNotIn("publish_assessment_issues.py", persisted)
        self.assertNotIn("publish_dtg_controller_incidents.py", persisted)
        self.assertIn('push -u origin "$branch"', persisted)
        self.assertIn("credential.helper=", persisted)
        self.assertIn("dtg_assurance_reconcile.py", persisted)
        self.assertIn("publish_dtg_controller_incidents.py", local)
        self.assertNotIn("publish_assessment_issues.py", local)
        self.assertIn("source.sha256", source)
        self.assertIn("sha256sum --check build/instance-monitor/source.sha256", source)
        self.assertNotIn("(cd build/instance-monitor && sha256sum --check", source)
        self.assertEqual(source.count("Require unchanged Toolkit main before effect"), 2)
        self.assertIn("group: rahp-instance-monitor", source)
        self.assertIn("cancel-in-progress: false", source)
        # The source snapshot must be created before any issue effect and
        # baseline persistence may not run without successful publication.
        self.assertIn("Retain exact monitored source", source)
        self.assertIn("needs: publish_external", source)

    def test_protected_main_requires_state_pr_not_bot_direct_push(self):
        source = (ROOT / ".github/workflows/instance-monitor-main.yml").read_text()
        self.assertIn("permission-pull-requests: write", source)
        self.assertIn("permission-contents: write", source)
        self.assertIn("persist-credentials: false", source)
        self.assertIn("gh pr create --base main", source)
        self.assertIn("git commit -s", source)
        self.assertIn('push -u origin "$branch"', source)
        self.assertIn("credential.helper=", source)
        self.assertNotIn("git push\n", source)
        self.assertIn("automation/instance-monitor-", source)
        self.assertIn("Unmerged monitored-state PR exists", source)
        self.assertIn("Pending protected-main instance state PR blocks re-publication", source)
        self.assertIn("disposition=staged_pending_review", source)
        self.assertIn("if: steps.persist.outputs.disposition == 'unchanged'", source)
        self.assertIn("needs.persist.outputs.disposition == 'unchanged'", source)
        self.assertIn("do not reconcile unmerged findings", source)
        self.assertNotIn("git push origin main", source)

    def test_accepted_state_reconciliation_reuses_canonical_controller(self):
        source = (ROOT / ".github/workflows/dtg-assurance-reconcile.yml").read_text()
        self.assertIn("github.event_name == 'push'", source)
        self.assertIn("'instances/dtg/state/**'", source)
        self.assertIn("'instances/cawg/state/**'", source)
        self.assertIn("Retain accepted-state incident decision", source)
        self.assertIn("needs: reconcile", source)
        self.assertIn("issues: write", source)
        self.assertIn("issues: read", source)
        self.assertIn("publish_dtg_controller_incidents.py", source)
        self.assertIn("github.ref == 'refs/heads/main'", source)
        self.assertNotIn("instance-state-reconcile-main.yml", source)

    def test_current_head_assurance_dispatch_contract(self) -> None:
        result = subprocess.run(
            [sys.executable, str(VALIDATOR)],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("PASS instance-watch protected-main state acceptance and assurance dispatch contract", result.stdout)


if __name__ == "__main__":
    unittest.main()
