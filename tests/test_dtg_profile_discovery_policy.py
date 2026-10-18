"""DTG discovery failure classification and fail-closed freshness gates (#1016)."""
import contextlib
import importlib.util
import io
from pathlib import Path
from unittest import TestCase, mock
import urllib.error

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("sync_dtg_profile", ROOT / "tools" / "sync_dtg_profile.py")
sync = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(sync)


class DTGProfileDiscoveryPolicyTests(TestCase):
    def test_http_500_is_distinct_from_semantic_drift(self):
        error = urllib.error.HTTPError("https://example.test/registry", 500, "Server Error", None, None)
        classified = sync._classify_discovery_exception(error)
        self.assertEqual("authoritative-discovery-unavailable", classified.failure_class)
        self.assertIn("HTTP 500", classified.detail)
        self.assertIn("https://example.test/registry", classified.detail)

        actual = {"repositories": []}
        expected = [{"repository": "trustoverip/example", "id": "example"}]
        self.assertIn("missing repository: trustoverip/example", sync.diff(actual, expected))

    def test_authentication_error_does_not_get_transient_skip(self):
        error = urllib.error.HTTPError("https://example.test/registry", 403, "Forbidden", None, None)
        self.assertEqual(
            "authoritative-discovery-authentication-or-rate-limit",
            sync._classify_discovery_exception(error).failure_class,
        )

    def _run(self, strict=False, expected=None, error=None):
        args = ["sync_dtg_profile.py", "--check"] + (["--strict-live-discovery"] if strict else [])
        load = [{"portfolio": {"registry_repository": "x", "registry_path": "y"}}, {"repositories": []}]
        with mock.patch("sys.argv", args), \
             mock.patch.object(sync.dtg_portfolio, "load_yaml", side_effect=load), \
             mock.patch.object(sync, "authoritative_repositories", side_effect=error) if error else mock.patch.object(sync, "authoritative_repositories", return_value=expected), \
             contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return sync.main()

    def test_transient_http_500_skips_only_pr_check(self):
        failure = sync.AuthoritativeDiscoveryUnavailable("authoritative-discovery-unavailable", "HTTP 500")
        self.assertEqual(0, self._run(error=failure, strict=False))
        self.assertEqual(1, self._run(error=failure, strict=True))

    def test_semantic_drift_still_fails_non_strict_pr_check(self):
        expected = [sync.portable_target({
            "id": "example", "repository": "trustoverip/example",
            "source": "portfolio-monitor", "role": "normative-specification",
        })]
        self.assertEqual(1, self._run(expected=expected, strict=False))

    def test_auth_failure_never_skipped(self):
        failure = sync.AuthoritativeDiscoveryUnavailable(
            "authoritative-discovery-authentication-or-rate-limit", "HTTP 403"
        )
        self.assertEqual(1, self._run(error=failure, strict=False))
