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
                "contents": "read", "issues": "write", "actions": "read",
            }),
            "persist": ("publish_external", {
                "contents": "write", "issues": "read", "actions": "write",
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
        self.assertIn("git push", persisted)
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

    def test_current_head_assurance_dispatch_contract(self) -> None:
        result = subprocess.run(
            [sys.executable, str(VALIDATOR)],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("PASS instance-watch current-head assurance dispatch contract", result.stdout)


if __name__ == "__main__":
    unittest.main()
