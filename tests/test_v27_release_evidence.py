"""Negative and positive tests for pinned release evidence contract."""
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from validate_v27_release_evidence import assess, REQUIRED

SHA = "a" * 40
BASE = "https://github.com/sankarshanmukhopadhyay/rahp-toolkit/actions/runs/123"


def fixture():
    return {
        "contract": "rahp-release-evidence/v1",
        "candidate_version": "v2.7.0",
        "candidate_sha": SHA,
        "publication_authorized": True,
        "gates": {gate: {"result": "PASS", "candidate_sha": SHA, "source": BASE,
                         **({"decision": "GO"} if gate == "owner_approval" else {})}
                  for gate in REQUIRED},
    }


class QualificationEvidenceTests(unittest.TestCase):
    def test_complete_evidence_contract(self):
        self.assertEqual(assess(fixture()), [])

    def test_pending_gate_is_no_go(self):
        record = fixture()
        record["gates"]["full_regression"]["result"] = "PENDING"
        self.assertTrue(assess(record))

    def test_mismatched_sha_is_no_go(self):
        record = fixture()
        record["gates"]["typescript_conformance"]["candidate_sha"] = "b" * 40
        self.assertTrue(assess(record))

    def test_missing_gate_is_no_go(self):
        record = fixture()
        del record["gates"]["security_review"]
        self.assertTrue(assess(record))

    def test_owner_must_explicitly_approve(self):
        record = fixture()
        record["gates"]["owner_approval"]["decision"] = "PENDING"
        self.assertTrue(assess(record))

    def test_no_publication_without_authorization(self):
        record = fixture()
        record["publication_authorized"] = False
        self.assertTrue(assess(record))

    def test_short_sha_rejected(self):
        record = fixture()
        record["candidate_sha"] = "abc123"
        self.assertTrue(assess(record))


if __name__ == "__main__":
    unittest.main()
