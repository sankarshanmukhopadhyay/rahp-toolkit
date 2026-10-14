from __future__ import annotations

import contextlib
import io
import pathlib
import sys
import tempfile
import unittest
import urllib.error
from unittest import mock

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import sync_dtg_profile  # noqa: E402


class SyncDtgProfileResilienceTests(unittest.TestCase):
    def _write_yaml(self, path: pathlib.Path, payload: dict) -> None:
        path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    def _run_main(self, *args: str) -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with mock.patch.object(sys, "argv", ["sync_dtg_profile.py", *args]):
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                result = sync_dtg_profile.main()
        return result, stdout.getvalue(), stderr.getvalue()

    def test_pr_check_soft_skips_transient_authoritative_http_500(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            instance = root / "instance.yaml"
            profile = root / "profile.yaml"
            self._write_yaml(instance, {"portfolio": {}, "instance": {}})
            self._write_yaml(profile, {"repositories": []})
            http_500 = urllib.error.HTTPError(
                url="https://api.github.com/repos/example/repo",
                code=500,
                msg="Internal Server Error",
                hdrs=None,
                fp=None,
            )

            with mock.patch.object(sync_dtg_profile.dtg_portfolio, "discover", side_effect=http_500):
                result, stdout, stderr = self._run_main(
                    "--instance",
                    str(instance),
                    "--profile",
                    str(profile),
                    "--check",
                )

            self.assertEqual(result, 0)
            self.assertIn("SKIP DTG profile live-discovery check", stdout)
            self.assertIn("authoritative-discovery-unavailable", stderr)
            self.assertIn("HTTP 500", stderr)

    def test_strict_live_discovery_fails_transient_authoritative_http_500(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            instance = root / "instance.yaml"
            profile = root / "profile.yaml"
            self._write_yaml(instance, {"portfolio": {}, "instance": {}})
            self._write_yaml(profile, {"repositories": []})
            http_500 = urllib.error.HTTPError(
                url="https://api.github.com/repos/example/repo",
                code=500,
                msg="Internal Server Error",
                hdrs=None,
                fp=None,
            )

            with mock.patch.object(sync_dtg_profile.dtg_portfolio, "discover", side_effect=http_500):
                result, _stdout, stderr = self._run_main(
                    "--instance",
                    str(instance),
                    "--profile",
                    str(profile),
                    "--check",
                    "--strict-live-discovery",
                )

            self.assertEqual(result, 1)
            self.assertIn("authoritative-discovery-unavailable", stderr)

    def test_profile_semantic_drift_remains_hard_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            instance = root / "instance.yaml"
            profile = root / "profile.yaml"
            self._write_yaml(instance, {"portfolio": {}, "instance": {}})
            self._write_yaml(profile, {"repositories": []})
            expected = [
                sync_dtg_profile.portable_target(
                    {
                        "id": "trustoverip-dtg-example",
                        "repository": "trustoverip/dtg-example",
                        "branch": "main",
                        "source": "portfolio-monitor",
                        "upstream": None,
                        "workstream": "example",
                        "role": "normative-specification",
                        "lifecycle": "active",
                        "reporting_weight": "medium",
                        "material_paths": ["README.md"],
                    }
                )
            ]

            with mock.patch.object(sync_dtg_profile, "authoritative_repositories", return_value=expected):
                result, _stdout, stderr = self._run_main(
                    "--instance",
                    str(instance),
                    "--profile",
                    str(profile),
                    "--check",
                )

            self.assertEqual(result, 1)
            self.assertIn("DTG profile drift detected", stderr)
            self.assertIn("missing repository: trustoverip/dtg-example", stderr)


if __name__ == "__main__":
    unittest.main()
