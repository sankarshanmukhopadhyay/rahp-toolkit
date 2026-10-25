"""Regression tests for composed corpus provenance invariants (#1142)."""
import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))
import validate_scenario_corpora as validator


class ComposedProvenanceTests(unittest.TestCase):
    def check_case(self, *, derived=False, note=True, grade=None, pending=True, same=False):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "corpora").mkdir()
            (root / "method").mkdir()
            (root / "method" / "scenario-patterns.yaml").write_text(
                yaml.safe_dump({"patterns": [{"id": "SP-TEST"}]}))
            parent_pin = "a" * 40
            input_pin = parent_pin if same else "b" * 40
            scenario = {"id": "T-001", "title": "Test", "domain": "Test",
                        "primary_goal": "Test", "primary_pressure": "Test",
                        "priority": "P0", "scenario_patterns": ["SP-TEST"]}
            parent = {"id": "PARENT", "title": "Parent", "adapter_version": "1",
                      "description": "Test", "source_repository": "org/repo",
                      "source_path": "SPEC.md", "source_commit": parent_pin,
                      "scenarios": [scenario]}
            child = {"id": "COMPOSED", "title": "Composed", "adapter_version": "1",
                     "description": "Test", "source_commit":
                     "derived-from-pinned-dependencies" if derived else "independently-pinned-upstream-revisions",
                     "depends_on": [{"corpus_id": "PARENT", "source_commit": input_pin}],
                     "scenarios": [scenario]}
            if note:
                child["provenance_note"] = "Reviewed as independently selected upstream revision"
            if pending:
                child["provenance_status"] = "composition-review-pending"
            if grade:
                child["evidence_grade"] = grade
            (root / "corpora" / "parent.yaml").write_text(yaml.safe_dump({"corpus": parent}))
            (root / "corpora" / "composed.yaml").write_text(yaml.safe_dump({"corpus": child}))
            sources = {"sources": [
                {"corpus_id": "PARENT", "corpus_file": "corpora/parent.yaml",
                 "update_mode": "assisted", "source": {"repository": "org/repo",
                 "paths": ["SPEC.md"]}},
                {"corpus_id": "COMPOSED", "corpus_file": "corpora/composed.yaml",
                 "update_mode": "derived", "dependencies": ["PARENT"]}]}
            (root / "corpora" / "sources.yaml").write_text(yaml.safe_dump(sources))
            output = io.StringIO()
            with patch.object(validator, "ROOT", root), patch.object(sys, "argv", ["validator"]), contextlib.redirect_stdout(output):
                code = validator.main()
            return code, output.getvalue()

    def test_documented_independent_pin_is_accepted(self):
        self.assertEqual(self.check_case()[0], 0)

    def test_matching_derived_pin_is_accepted(self):
        self.assertEqual(self.check_case(derived=True, same=True)[0], 0)

    def test_divergent_derived_pin_is_rejected(self):
        code, output = self.check_case(derived=True)
        self.assertEqual(code, 1)
        self.assertIn("pin differs from parent", output)

    def test_undocumented_independent_pin_is_rejected(self):
        code, output = self.check_case(note=False)
        self.assertEqual(code, 1)
        self.assertIn("requires corpus.provenance_note", output)

    def test_source_pinned_with_pending_review_is_rejected(self):
        code, output = self.check_case(grade="source-pinned")
        self.assertEqual(code, 1)
        self.assertIn("evidence grade contradicts pending provenance/composition review", output)

    def test_independently_reviewed_grade_not_inherited_or_blocked(self):
        self.assertEqual(self.check_case(grade="source-pinned", pending=False)[0], 0)


if __name__ == "__main__":
    unittest.main()
