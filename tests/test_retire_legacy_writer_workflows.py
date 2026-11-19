from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "retire_legacy_writer_workflows",
    ROOT / "tools/retire_legacy_writer_workflows.py",
)
assert SPEC and SPEC.loader
retirement = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(retirement)


class WorkflowRetirementTests(unittest.TestCase):
    def setUp(self):
        self.records = {
            1001: {"id": 1001, "path": ".github/workflows/dtg-materiality-main.yml",
                   "state": "active"},
            1002: {"id": 1002, "path": ".github/workflows/instance-monitor-main.yml",
                   "state": "active"},
            **{
                ident: {"id": ident, "path": path, "state": "active"}
                for ident, path in retirement.LEGACY
            },
        }
        self.writes = []

    def inventory(self):
        return {"workflows": list(self.records.values())}

    def fetch(self, ident):
        return self.records[ident].copy()

    def disable(self, ident):
        self.writes.append(ident)
        self.records[ident]["state"] = "disabled_manually"

    def execute(self, inventory=None):
        return retirement.retire(
            self.inventory() if inventory is None else inventory,
            self.fetch, self.disable, "a" * 40,
        )

    def test_exact_old_ids_disabled_only_after_replacement_preflight(self):
        result = self.execute()
        self.assertEqual(self.writes, [x[0] for x in retirement.LEGACY])
        self.assertEqual(result["toolkit_commit"], "a" * 40)
        self.assertEqual(len(result["legacy_registrations"]), 2)
        self.assertFalse(result["registry_cutover_authorized"])
        self.assertFalse(result["historical_ref_dispatch_denial_tested"])
        self.assertFalse(result["global_issues_api_exclusivity_verified"])

    def test_replayed_retirement_is_idempotent(self):
        self.execute()
        self.writes.clear()
        self.assertEqual(len(self.execute()["legacy_registrations"]), 2)
        self.assertEqual(self.writes, [])

    def test_missing_or_unready_replacement_never_disables_old_workflow(self):
        for changed in ("missing", "disabled", "duplicate"):
            with self.subTest(changed=changed):
                self.setUp()
                entries = self.inventory()["workflows"]
                if changed == "missing":
                    entries = [x for x in entries if x["id"] != 1001]
                elif changed == "disabled":
                    entries[0]["state"] = "disabled_manually"
                else:
                    entries.append(entries[0].copy())
                with self.assertRaises(retirement.RetirementError):
                    self.execute({"workflows": entries})
                self.assertEqual(self.writes, [])

    def test_old_id_or_path_substitution_denied_before_any_write(self):
        for key, value in (("path", ".github/workflows/review-workers.yml"),
                           ("id", 123456), ("state", "unknown")):
            with self.subTest(key=key):
                self.setUp()
                legacy_id = retirement.LEGACY[1][0]
                self.records[legacy_id][key] = value
                with self.assertRaises(retirement.RetirementError):
                    self.execute()
                self.assertEqual(self.writes, [])

    def test_failed_disable_and_contradictory_readback_not_satisfied(self):
        with self.assertRaises(retirement.RetirementError):
            retirement.retire(self.inventory(), self.fetch, lambda _: None, "a" * 40)
        self.setUp()
        def incomplete(ident):
            self.writes.append(ident)
            self.records[ident]["state"] = "disabled_inactivity"
        with self.assertRaises(retirement.RetirementError):
            retirement.retire(self.inventory(), self.fetch, incomplete, "a" * 40)

    def test_wrong_repo_or_ref_denied(self):
        approved = {
            "GITHUB_ACTIONS": "true",
            "GITHUB_REPOSITORY": retirement.REPOSITORY,
            "GITHUB_REF": "refs/heads/main",
            "GITHUB_EVENT_NAME": "push",
            "GITHUB_ACTOR": "sankarshanmukhopadhyay",
            "GITHUB_SHA": "a" * 40,
        }
        self.assertEqual(retirement.require_operator_context(approved), "a" * 40)
        for key, value in (
            ("GITHUB_REPOSITORY", "attacker/repo"),
            ("GITHUB_REF", "refs/heads/old"),
            ("GITHUB_EVENT_NAME", "workflow_dispatch"),
            ("GITHUB_ACTOR", "github-actions[bot]"),
            ("GITHUB_SHA", "main"),
            ("GITHUB_ACTIONS", "false"),
        ):
            with self.subTest(key=key), self.assertRaises(retirement.RetirementError):
                retirement.require_operator_context({**approved, key: value})


if __name__ == "__main__":
    unittest.main()
