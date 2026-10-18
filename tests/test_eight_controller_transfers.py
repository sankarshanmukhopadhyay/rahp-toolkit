"""Fail-closed source and transfer-matrix controls for controller disposal."""
from __future__ import annotations

import copy
import json
import pathlib
import tempfile
import unittest

from tools.validate_eight_controller_transfers import DATA, audit_archives, validate_manifest


class ControllerTransferTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = json.loads(DATA.read_text())

    def test_all_54_distinct_findings_have_explicit_accountability(self):
        self.assertEqual([], validate_manifest(self.original))
        self.assertEqual(54, len(self.original["findings"]))
        self.assertEqual(8, len(self.original["snapshots"]))
        self.assertEqual(9, sum(f["disposition"] == "reasoned-release-aggregate" for f in self.original["findings"]))

    def test_missing_owner_cannot_be_laundered_as_transfer(self):
        data = copy.deepcopy(self.original)
        next(f for f in data["findings"] if f["disposition"] == "review-transfer")["owner_issue"] = 527
        self.assertTrue(any("no active/narrow owner" in x for x in validate_manifest(data)))

    def test_duplicate_or_omitted_finding_fails(self):
        data = copy.deepcopy(self.original)
        data["findings"][1]["finding_id"] = data["findings"][0]["finding_id"]
        self.assertTrue(any("duplicate finding" in x for x in validate_manifest(data)))
        data["findings"].pop()
        self.assertTrue(any("54 distinct" in x for x in validate_manifest(data)))

    def test_false_no_action_and_false_pass_fail(self):
        data = copy.deepcopy(self.original)
        affected = next(f for f in data["findings"] if f["finding_id"] == "aa28149c7babc678e9e7")
        affected["disposition"] = "reasoned-release-aggregate"
        affected["owner_issue"] = None
        self.assertTrue(validate_manifest(data))
        data = copy.deepcopy(self.original)
        data["no_terminal_assurance_claim"] = False
        self.assertTrue(any("terminal" in x for x in validate_manifest(data)))

    def test_source_archive_missing_is_a_failure_not_success(self):
        with tempfile.TemporaryDirectory() as temporary:
            errors = audit_archives(self.original, pathlib.Path(temporary))
        self.assertEqual(8, sum("absent source artifact" in x for x in errors))


if __name__ == "__main__":
    unittest.main()
