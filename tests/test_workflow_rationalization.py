import pathlib
import unittest
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"


class WorkflowRationalizationTests(unittest.TestCase):
    def test_governed_surface_is_eighteen_of_twenty(self):
        policy = yaml.safe_load((ROOT / "config" / "workflow-governance.yaml").read_text())
        actual = sorted(path.name for path in WORKFLOWS.glob("*.yml"))
        self.assertEqual(len(actual), 18)
        self.assertLessEqual(len(actual), int(policy["max_workflows"]))
        self.assertEqual(sorted(policy["workflows"]), actual)

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

    def test_lifecycle_controllers_remain_separate_in_this_tranche(self):
        for name in (
            "combined-review-worker.yml",
            "dtg-repository-review-worker.yml",
            "dtg-portfolio-materiality-handoff.yml",
            "dpip-handoff.yml",
            "dpip-lifecycle.yml",
            "dtg-assurance-reconcile.yml",
            "instance-watch.yml",
        ):
            self.assertTrue((WORKFLOWS / name).exists(), name)


if __name__ == "__main__":
    unittest.main()
