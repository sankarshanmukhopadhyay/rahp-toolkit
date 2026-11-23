import pathlib
import unittest
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"


class WorkflowRationalizationTests(unittest.TestCase):
    def test_governed_surface_is_twenty_of_twenty(self):
        policy = yaml.safe_load((ROOT / "config" / "workflow-governance.yaml").read_text())
        actual = sorted(path.name for path in WORKFLOWS.glob("*.yml"))
        # Two distinct source-only registrations are required to retire the
        # mixed old writer registrations without losing accepted observations.
        # Do not enlarge the governed workflow budget.
        self.assertEqual(len(actual), 20)
        self.assertEqual(int(policy["max_workflows"]), 20)
        self.assertEqual(sorted(policy["workflows"]), actual)
        for successor in ("registry-observe-instance.yml",
                          "registry-observe-materiality.yml"):
            self.assertIn(successor, actual)

    def test_retired_validation_workflows_do_not_exist(self):
        for name in (
            "vti-composition-wave.yml",
            "vti-semantic-completion.yml",
        ):
            self.assertFalse((WORKFLOWS / name).exists(), name)

    def test_required_validate_surface_preserves_retired_checks(self):
        text = (WORKFLOWS / "validate.yml").read_text()
        required = (
            "python3 tools/validate_vti_composition_wave.py",
            "python3 tools/validate_vti_semantic_completion.py",
            "VTI fixture validation proves the declared evidence vectors are evaluated consistently.",
        )
        for token in required:
            self.assertIn(token, text)

    def test_release_codename_policy_retains_immutable_action_boundary(self):
        path = WORKFLOWS / "release-codename-policy.yml"
        self.assertTrue(path.exists())
        text = path.read_text()
        self.assertIn("actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1", text)
        self.assertIn("actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97", text)

    def test_consolidated_controllers_keep_explicit_workflow_owners(self):
        for name in (
            "review-workers.yml",
            "dtg-materiality-main.yml",
            "dpip-lifecycle.yml",
            "dtg-assurance-reconcile.yml",
            "instance-monitor-main.yml",
        ):
            self.assertTrue((WORKFLOWS / name).exists(), name)
        for name in (
            "combined-review-worker.yml",
            "dtg-repository-review-worker.yml",
            "dpip-handoff.yml",
        ):
            self.assertFalse((WORKFLOWS / name).exists(), name)


if __name__ == "__main__":
    unittest.main()
