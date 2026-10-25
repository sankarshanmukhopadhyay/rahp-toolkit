"""Regression tests for standalone corpus authority provenance (#1145)."""
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


class StandaloneAuthorityProvenanceTests(unittest.TestCase):
    def check_case(self, *, corpus_pin=None, grade=None, pending=True):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "corpora").mkdir()
            (root / "method").mkdir()
            (root / "method" / "scenario-patterns.yaml").write_text(
                yaml.safe_dump({"patterns": [{"id": "SP-TEST"}]}),
                encoding="utf-8",
            )
            authority_pin = "a" * 40
            corpus = {
                "id": "CORPUS-TEST",
                "title": "Test corpus",
                "adapter_version": "1",
                "description": "Test",
                "source_repository": "upstream/spec",
                "source_path": "spec/** + conformance/**",
                "source_commit": corpus_pin or authority_pin,
                "scenarios": [{
                    "id": "T-001",
                    "title": "Test",
                    "domain": "Test",
                    "primary_goal": "Test",
                    "primary_pressure": "Test",
                    "priority": "P0",
                    "scenario_patterns": ["SP-TEST"],
                }],
            }
            if pending:
                corpus["provenance_status"] = "authoritative-source-pinned-scenario-review-pending"
            if grade:
                corpus["evidence_grade"] = grade

            (root / "corpora" / "test.yaml").write_text(
                yaml.safe_dump({"corpus": corpus}), encoding="utf-8")
            sources = {
                "sources": [{
                    "corpus_id": "CORPUS-TEST",
                    "corpus_file": "corpora/test.yaml",
                    "update_mode": "assisted",
                    "source": {
                        "repository": "upstream/spec",
                        "paths": ["spec/**", "conformance/**"],
                        "authority_pin": authority_pin,
                    },
                }]
            }
            (root / "corpora" / "sources.yaml").write_text(
                yaml.safe_dump(sources), encoding="utf-8")

            output = io.StringIO()
            with patch.object(validator, "ROOT", root),                  patch.object(sys, "argv", ["validator"]),                  contextlib.redirect_stdout(output):
                code = validator.main()
            return code, output.getvalue()

    def test_matching_reviewed_authority_pin_is_accepted(self):
        self.assertEqual(self.check_case()[0], 0)

    def test_authority_pin_mismatch_is_rejected(self):
        code, output = self.check_case(corpus_pin="b" * 40)
        self.assertEqual(code, 1)
        self.assertIn("source_commit differs from sources.yaml authority_pin", output)

    def test_grade_is_rejected_while_scenario_requalification_is_pending(self):
        code, output = self.check_case(grade="source-pinned")
        self.assertEqual(code, 1)
        self.assertIn("evidence grade contradicts pending provenance/composition review", output)

    def test_grade_boundary_no_longer_blocks_after_requalification_status_changes(self):
        self.assertEqual(self.check_case(grade="source-pinned", pending=False)[0], 0)


if __name__ == "__main__":
    unittest.main()
