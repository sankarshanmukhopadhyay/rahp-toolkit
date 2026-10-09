import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tools.comparative_assurance import build_digest, render_digest_markdown

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "fixtures" / "comparative-assurance"

class ComparativeAssuranceCliTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.baseline = json.loads((FIXTURES / "dogwood-assessment.json").read_text(encoding="utf-8"))
        cls.candidate = json.loads((FIXTURES / "eucalyptus-assessment.json").read_text(encoding="utf-8"))
        cls.profile = json.loads((FIXTURES / "release-comparison-profile.json").read_text(encoding="utf-8"))

    def test_builder_emits_schema_valid_bounded_conclusion(self):
        digest = build_digest(self.baseline, self.candidate, self.profile)
        self.assertEqual("partial", digest["comparability"]["status"])
        self.assertEqual("indeterminate", digest["overall"]["judgment"])
        self.assertFalse(digest["overall"]["release_superiority_established"])

    def test_builder_is_deterministic(self):
        self.assertEqual(build_digest(self.baseline, self.candidate, self.profile), build_digest(self.baseline, self.candidate, self.profile))

    def test_renderer_uses_authoritative_artifact(self):
        digest = build_digest(self.baseline, self.candidate, self.profile)
        markdown = render_digest_markdown(digest)
        self.assertIn("Overall judgment | indeterminate", markdown)
        self.assertIn("Release superiority established | no", markdown)
        self.assertIn("## Scope and coverage", markdown)
        self.assertIn("Added supporting dependencies (not independently assessed by inclusion): rahp-toolkit", markdown)
        self.assertIn("## Unresolved limitations", markdown)
        self.assertIn("## Recommended next actions", markdown)

    def test_renderer_is_deterministic(self):
        digest = build_digest(self.baseline, self.candidate, self.profile)
        self.assertEqual(render_digest_markdown(digest), render_digest_markdown(digest))

    def test_cli_writes_json_and_markdown(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "comparison"
            run = subprocess.run([sys.executable,str(ROOT / "tools" / "rahp.py"),"compare","--baseline",str(FIXTURES / "dogwood-assessment.json"),"--candidate",str(FIXTURES / "eucalyptus-assessment.json"),"--profile",str(FIXTURES / "release-comparison-profile.json"),"--output",str(output)],cwd=ROOT,text=True,capture_output=True)
            self.assertEqual(0, run.returncode, run.stderr)
            artifact = json.loads((output / "comparison.json").read_text(encoding="utf-8"))
            report = (output / "comparison.md").read_text(encoding="utf-8")
            self.assertEqual("dogwood-to-eucalyptus", artifact["comparison_id"])
            self.assertIn(artifact["overall"]["judgment"], report)

    def test_candidate_must_bind_to_supplied_baseline(self):
        candidate = json.loads(json.dumps(self.candidate))
        candidate["comparison"]["baseline_assessment_id"] = "another-baseline"
        with self.assertRaisesRegex(ValueError, "does not identify"):
            build_digest(self.baseline, candidate, self.profile)

if __name__ == "__main__":
    unittest.main()
