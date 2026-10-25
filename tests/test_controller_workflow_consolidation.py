import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"


class ControllerWorkflowConsolidationTests(unittest.TestCase):
    def test_dpip_label_trigger_is_handoff_only(self):
        text = (WORKFLOWS / "dpip-lifecycle.yml").read_text()
        self.assertIn("issues:\n    types: [labeled]", text)
        lifecycle = text.split("  lifecycle:", 1)[1].split("\n  handoff:", 1)[0]
        handoff = text.split("\n  handoff:", 1)[1]
        self.assertNotIn("github.event_name == 'issues'", lifecycle)
        self.assertIn("github.event_name == 'issues'", handoff)
        self.assertIn("github.event.label.name == 'assurance:dpip-requested'", handoff)
        self.assertIn("group: rahp-dpip-handoff", handoff)

    def test_dpip_recovery_is_three_hour_lifecycle_with_serialized_handoff(self):
        text = (WORKFLOWS / "dpip-lifecycle.yml").read_text()
        self.assertIn("cron: '47 */3 * * *'", text)
        self.assertIn("needs.lifecycle.result == 'success'", text)
        self.assertIn("python3 tools/dpip_handoff.py", text)
        self.assertFalse((WORKFLOWS / "dpip-handoff.yml").exists())

    def test_review_workers_keep_two_explicit_jobs(self):
        text = (WORKFLOWS / "review-workers.yml").read_text()
        self.assertIn("\n  combined_review:\n", text)
        self.assertIn("\n  dtg_repository_review:\n", text)
        self.assertIn("python3 tools/combined_review_worker.py", text)
        self.assertIn("python3 tools/dtg_repository_review_worker.py", text)
        self.assertIn("rahp-combined-review-worker-", text)
        self.assertIn("rahp-dtg-repository-review-", text)

    def test_issue_routing_is_mutually_bounded(self):
        text = (WORKFLOWS / "review-workers.yml").read_text()
        combined = text.split("  combined_review:", 1)[1].split("\n  dtg_repository_review:", 1)[0]
        repository = text.split("  dtg_repository_review:", 1)[1]
        self.assertIn("dtg:portfolio:combined:", combined)
        self.assertNotIn("rahp-assessment-key:dtg:repository:", combined)
        self.assertIn("rahp-assessment-key:dtg:repository:", repository)
        self.assertNotIn("dtg:portfolio:combined:", repository)

    def test_manual_targeting_cannot_broaden_to_both_workers(self):
        text = (WORKFLOWS / "review-workers.yml").read_text()
        self.assertIn("issue_number may only be supplied when exactly one worker is selected.", text)
        self.assertIn("inputs.worker == 'combined'", text)
        self.assertIn("inputs.worker == 'repository'", text)
        self.assertIn("inputs.worker == 'all' && inputs.issue_number == ''", text)

    def test_schedule_recovers_both_workers_at_one_six_hour_boundary(self):
        text = (WORKFLOWS / "review-workers.yml").read_text()
        self.assertEqual(text.count("cron: '23 */6 * * *'"), 1)
        combined = text.split("  combined_review:", 1)[1].split("\n  dtg_repository_review:", 1)[0]
        repository = text.split("  dtg_repository_review:", 1)[1]
        self.assertIn("github.event_name == 'schedule'", combined)
        self.assertIn("github.event_name == 'schedule'", repository)

    def test_push_path_is_combined_worker_only(self):
        text = (WORKFLOWS / "review-workers.yml").read_text()
        combined = text.split("  combined_review:", 1)[1].split("\n  dtg_repository_review:", 1)[0]
        repository = text.split("  dtg_repository_review:", 1)[1]
        self.assertIn("github.event_name == 'push'", combined)
        self.assertNotIn("github.event_name == 'push'", repository)

    def test_legacy_worker_files_are_absent(self):
        for name in (
            "combined-review-worker.yml",
            "dtg-repository-review-worker.yml",
            "dpip-handoff.yml",
        ):
            self.assertFalse((WORKFLOWS / name).exists(), name)


if __name__ == "__main__":
    unittest.main()
