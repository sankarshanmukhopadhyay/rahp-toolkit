import importlib.util
import json
import pathlib
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CTRL = load_module("assessment_controller_routing", ROOT / "tools" / "assessment_controller.py")
ROUTER = load_module("resilience_router", ROOT / "tools" / "resilience_router.py")
PROFILE = ROOT / "profiles" / "resilience" / "default.yaml"


class ResilienceRoutingTests(unittest.TestCase):
    def test_implementation_is_required(self):
        policy = ROUTER.load_policy(PROFILE)
        self.assertEqual(
            CTRL.resilience_applicability("implementation", policy)["decision"],
            "required",
        )

    def test_governance_only_is_explicitly_not_applicable(self):
        record = CTRL.new_lifecycle("gov")
        CTRL.apply_resilience_applicability(
            record,
            "governance-only",
            ROUTER.load_policy(PROFILE),
            policy_source=str(PROFILE),
        )
        value = CTRL.resilience_disposition(record)
        self.assertEqual(value["disposition"], "not-applicable")
        self.assertEqual(value["provenance"]["target_class"], "governance-only")

    def test_ambiguous_specification_fails_closed(self):
        record = CTRL.new_lifecycle("spec")
        CTRL.apply_resilience_applicability(
            record,
            "specification",
            ROUTER.load_policy(PROFILE),
            policy_source=str(PROFILE),
        )
        value = CTRL.resilience_disposition(record)
        self.assertEqual(value["disposition"], "required-but-not-executed")
        self.assertEqual(value["provenance"]["decision"], "unresolved")

    def test_conflicting_profile_policy_is_rejected(self):
        with self.assertRaises(ValueError):
            CTRL.resilience_applicability(
                "implementation",
                {
                    "required_for": ["implementation"],
                    "not_applicable_for": ["implementation"],
                },
            )

    def test_required_without_target_path_remains_unexecuted(self):
        record = CTRL.new_lifecycle("impl-no-path")
        record, result = ROUTER.route_resilience(
            record,
            target_class="implementation",
            target_path=None,
            profile=PROFILE,
        )
        self.assertIsNone(result)
        self.assertEqual(
            CTRL.resilience_disposition(record)["disposition"],
            "required-but-not-executed",
        )

    def test_required_target_invokes_existing_drarm_and_records_execution(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = pathlib.Path(tmp) / "target"
            target.mkdir()

            def fake_runner(cmd, **kwargs):
                result_path = pathlib.Path(cmd[cmd.index("--json") + 1])
                result_path.write_text(
                    json.dumps({"model": "DRARM", "findings": [], "summary": {}}),
                    encoding="utf-8",
                )
                return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")

            record = CTRL.new_lifecycle("impl")
            record, result = ROUTER.route_resilience(
                record,
                target_class="implementation",
                target_path=target,
                profile=PROFILE,
                repository="example/repo",
                revision="abc123",
                runner=fake_runner,
            )
            self.assertEqual(result["model"], "DRARM")
            value = CTRL.resilience_disposition(record)
            self.assertEqual(value["disposition"], "executed")
            self.assertEqual(value["provenance"]["revision"], "abc123")

    def test_failed_drarm_execution_remains_unexecuted(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = pathlib.Path(tmp)

            def failed_runner(cmd, **kwargs):
                return subprocess.CompletedProcess(cmd, 2, stdout="", stderr="boom")

            record = CTRL.new_lifecycle("failed")
            record, result = ROUTER.route_resilience(
                record,
                target_class="deployment",
                target_path=target,
                profile=PROFILE,
                runner=failed_runner,
            )
            self.assertEqual(result["error"], "drarm-execution-failed")
            self.assertEqual(
                CTRL.resilience_disposition(record)["disposition"],
                "required-but-not-executed",
            )


if __name__ == "__main__":
    unittest.main()
