from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"


class RegistryObservationSuccessorTests(unittest.TestCase):
    def test_registry_successors_have_no_external_issue_or_dispatch_authority(self):
        for filename in ("registry-observe-instance.yml", "registry-observe-materiality.yml"):
            with self.subTest(workflow=filename):
                body = (WORKFLOWS / filename).read_text(encoding="utf-8")
                self.assertIn("owner=\"$(python3 tools/publish_assessment_issues.py --publication-owner)\"", body)
                self.assertIn("needs.route.outputs.registry_mode == 'true'", body)
                self.assertIn("  issues: read", body)
                self.assertNotIn("issues: write", body)
                self.assertNotIn("actions: write", body)
                self.assertNotIn("gh workflow run", body)
                # The issue-watch observation tool legitimately writes a local
                # event *file* with --events; reject only external issue POST
                # invocations, not that read-only observation contract.
                self.assertNotIn("tools/publish_assessment_issues.py\\n          --events", body)
                self.assertNotIn("dpip_handoff.py", body)
                self.assertNotIn("dtg_repository_review_worker.py", body)
                self.assertIn("cancel-in-progress: false", body)
                self.assertIn("workflow_dispatch:", body)

    def test_incremental_observation_is_exact_and_protected(self):
        body = (WORKFLOWS / "registry-observe-instance.yml").read_text(encoding="utf-8")
        self.assertIn("group: rahp-instance-monitor", body)
        self.assertIn("name: instance-monitor-source-${{ github.run_id }}-${{ github.run_attempt }}", body)
        self.assertIn("sha256sum --check build/instance-monitor/source.sha256", body)
        self.assertIn("  persist:\n    needs: monitor", body)
        self.assertIn("Stage monitored state under protected-main review", body)
        self.assertIn("Generate repository-scoped state PR credential", body)
        self.assertIn("permission-contents: write", body)
        self.assertIn("permission-pull-requests: write", body)
        self.assertIn("instances/dtg/generated/review-events.json", body)
        self.assertIn("instances/cawg/generated/review-events.json", body)
        self.assertIn("No assurance PASS", body.replace("No assurance PASS", "No assurance PASS"))
        self.assertNotIn("Source observation and external issue publication completed", body)

    def test_materiality_evidence_retained_without_case_effects(self):
        body = (WORKFLOWS / "registry-observe-materiality.yml").read_text(encoding="utf-8")
        self.assertIn("group: dtg-portfolio-materiality-handoff", body)
        self.assertIn("Fetch newest recent Portfolio Monitor snapshot", body)
        self.assertIn("source-qualified", body)
        self.assertIn("dtg-source-qualified-queue-${{ github.run_id }}-${{ github.run_attempt }}", body)
        self.assertIn("build/dtg-routing/registry-partition/", body)
        self.assertNotIn("Publish or coalesce portfolio controller", body)
        self.assertNotIn("Transport qualified privacy referrals to DPIP", body)

    def test_toolkit_local_incidents_remain_independent(self):
        local = (WORKFLOWS / "dtg-assurance-reconcile.yml").read_text(encoding="utf-8")
        self.assertIn("  local_incidents:", local)
        self.assertIn("Publish only unowned Toolkit-local controller incidents", local)
        self.assertIn("issues: write", local)


if __name__ == "__main__":
    unittest.main()
