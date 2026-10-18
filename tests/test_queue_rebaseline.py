"""Queue inventory classification and anti-false-closure regressions."""
import copy
import json
from pathlib import Path
import unittest

from tools.validate_queue_rebaseline import validate_queue

ROOT = Path(__file__).resolve().parents[1]
BASE = json.loads((ROOT / "data/assurance/queue-rebaseline-2026-10-18.json").read_text(encoding="utf-8"))


class QueueRebaselineTests(unittest.TestCase):
    def test_exact_open_issue_checkpoint(self):
        self.assertEqual([], validate_queue(BASE))
        self.assertEqual(52, BASE["open_issue_count"])
        ids = {x["number"] for x in BASE["issues"]}
        self.assertNotIn(121, ids)
        self.assertNotIn(527, ids)
        self.assertNotIn(1022, ids)
        self.assertIn(1054, ids)
        self.assertIn(1057, ids)

    def test_missing_entry_fails(self):
        value = copy.deepcopy(BASE)
        value["issues"].pop()
        self.assertTrue(any("declared count" in e for e in validate_queue(value)))

    def test_duplicate_owner_record_fails(self):
        value = copy.deepcopy(BASE)
        value["issues"][1]["number"] = value["issues"][0]["number"]
        self.assertTrue(any("duplicate" in e for e in validate_queue(value)))

    def test_unrecognized_disposition_fails(self):
        value = copy.deepcopy(BASE)
        value["issues"][0]["classification"] = "assurance-PASS"
        self.assertTrue(any("unclassified" in e for e in validate_queue(value)))

    def test_routing_cannot_authorize_terminal_assurance(self):
        value = copy.deepcopy(BASE)
        value["issues"][0]["closure_authorized"] = True
        self.assertTrue(any("cannot assert" in e for e in validate_queue(value)))


if __name__ == "__main__":
    unittest.main()
