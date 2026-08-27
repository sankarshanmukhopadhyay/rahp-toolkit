import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "dtg_gatherer_lineage", ROOT / "tools" / "dtg_gatherer_lineage.py"
)
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


class DtgGathererLineageTests(unittest.TestCase):
    def event(self):
        return {
            "assessment_key": "dtg:repository:OpenVTC/openvtc",
            "repository": "OpenVTC/openvtc",
            "old": "a" * 40,
            "new": "b" * 40,
            "event_class": "assessment-required",
            "body": "assessment body",
        }

    def test_same_event_and_run_are_deterministic(self):
        first, run1 = MOD.stamp([self.event()], "gha-123-1")
        second, run2 = MOD.stamp([self.event()], "gha-123-1")
        self.assertEqual(run1["fingerprint"], run2["fingerprint"])
        self.assertEqual(first[0]["gatherer_event_id"], second[0]["gatherer_event_id"])

    def test_run_and_event_markers_are_embedded_for_issue_publication(self):
        stamped, run = MOD.stamp([self.event()], "gha-123-1")
        body = stamped[0]["body"]
        self.assertIn("rahp-dtg-gatherer-run:gha-123-1", body)
        self.assertIn("rahp-dtg-gatherer-event:", body)
        self.assertTrue(stamped[0]["observed_at"].startswith("gatherer-gha-123-1-"))
        self.assertEqual(run["qualifying_events"], [stamped[0]["gatherer_event_id"]])

    def test_changed_revision_changes_event_identity(self):
        first = self.event()
        second = self.event()
        second["new"] = "c" * 40
        self.assertNotEqual(MOD.event_id(first), MOD.event_id(second))


if __name__ == "__main__":
    unittest.main()
