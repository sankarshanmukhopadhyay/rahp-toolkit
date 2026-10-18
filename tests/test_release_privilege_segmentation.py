"""Assure release qualification cannot receive publication write permission."""
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/release.yml"


class ReleasePrivilegeSegmentationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
        cls.jobs = cls.data["jobs"]

    def test_read_only_qualification_and_write_only_publisher(self):
        self.assertEqual("read", self.data["permissions"]["contents"])
        self.assertEqual("read", self.jobs["qualify"]["permissions"]["contents"])
        self.assertEqual("write", self.jobs["publish"]["permissions"]["contents"])
        self.assertEqual("qualify", self.jobs["publish"]["needs"])
        self.assertIn("needs.qualify.outputs.publish", self.jobs["publish"]["if"])

    def test_qualify_never_runs_mutating_tag_or_release_commands(self):
        steps = "\n".join(str(x.get("run", "")) for x in self.jobs["qualify"]["steps"])
        self.assertNotIn("git push", steps)
        self.assertNotIn("gh release create", steps)
        self.assertNotIn("gh release edit", steps)
        self.assertIn("tools/release.py qualify", steps)
        self.assertIn("verify_published_release.py preflight", steps)

    def test_publisher_requalifies_and_rechecks_declaration_before_mutation(self):
        steps = self.jobs["publish"]["steps"]
        text = "\n".join(str(x.get("run", "")) for x in steps)
        self.assertIn("tools/release.py qualify", text)
        self.assertIn("Qualified tag changed between jobs", text)
        self.assertIn("Qualified branch changed between jobs", text)
        first_mutation = next(i for i, x in enumerate(steps) if "git push origin" in str(x.get("run", "")))
        handoff = next(i for i, x in enumerate(steps) if x.get("name") == "Check qualified-to-publish handoff")
        self.assertLess(handoff, first_mutation)

    def test_only_one_job_can_write_contents(self):
        writers = [name for name, job in self.jobs.items() if job.get("permissions", {}).get("contents") == "write"]
        self.assertEqual(["publish"], writers)


if __name__ == "__main__":
    unittest.main()
