import importlib.util
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
SPEC = importlib.util.spec_from_file_location(
    "dtg_automated_disposition", ROOT / "tools" / "dtg_automated_disposition.py"
)
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


class DtgAutomatedDispositionTests(unittest.TestCase):
    def test_spec_surface_forces_uncertainty(self):
        result = MOD.assess({
            "commits": [{"commit": {"message": "spec(registry): gate item"}}],
            "files": [
                {"filename": "SPEC.md", "patch": "+ clarify identifierScope"},
                {"filename": "specs/spec.meta.schema.json", "patch": "+ gate"},
                {"filename": ".github/workflows/rust.yml", "patch": "+ check"},
            ],
        })
        self.assertFalse(result["terminal"])
        self.assertEqual(result["composition"], "uncertain")
        self.assertEqual(result["dpip"], "uncertain")

    def test_bounded_security_fix_with_regression_test_can_auto_dispose(self):
        result = MOD.assess({
            "commits": [{"commit": {"message": "fix(auth): stop revoke-session telling a stranger the session exists"}}],
            "files": [
                {"filename": "vta-service/src/trust_tasks/auth.rs", "patch": "+ reject unauthorized caller"},
                {"filename": "vta-service/tests/revoke_session_trust_task.rs", "patch": "+ stranger_cannot_observe_session"},
            ],
        })
        self.assertTrue(result["terminal"])
        self.assertEqual(result["security"], "strengthened")
        self.assertEqual(result["risk"], "mitigated")
        self.assertEqual(result["harm"], "mitigated")
        self.assertEqual(result["dpip"], "not-required")

    def test_security_keyword_without_regression_test_is_not_enough(self):
        result = MOD.assess({
            "commits": [{"commit": {"message": "fix(auth): reject unauthorized caller"}}],
            "files": [{"filename": "src/auth.rs", "patch": "+ reject caller"}],
        })
        self.assertFalse(result["terminal"])

    def test_weakening_signal_blocks_auto_disposition(self):
        result = MOD.assess({
            "commits": [{"commit": {"message": "fix(auth): relax access check"}}],
            "files": [
                {"filename": "src/auth.rs", "patch": "+ bypass check"},
                {"filename": "tests/auth_test.rs", "patch": "+ test"},
            ],
        })
        self.assertFalse(result["terminal"])

    def test_composed_correlation_signal_blocks_local_auto_close(self):
        result = MOD.assess({
            "commits": [{"commit": {"message": "fix(auth): prevent stable identifier correlation across contexts"}}],
            "files": [
                {"filename": "src/auth.rs", "patch": "+ pairwise binding"},
                {"filename": "tests/auth_test.rs", "patch": "+ cross-context test"},
            ],
        })
        self.assertFalse(result["terminal"])
        self.assertTrue(result["evidence"]["correlation_signal"])


if __name__ == "__main__":
    unittest.main()
