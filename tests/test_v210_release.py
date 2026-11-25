"""Release qualification gates are not assurance determinations."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from validate_v210_release import validate, GATES, CAPABILITIES
from validate_v210_release_evidence import assess

Q = "method/v2.10-release-qualification.yaml"
E = "method/v2.10-release-evidence.json"
C = "method/v2.10-release-candidate.yaml"

class ReleaseQualificationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.q = yaml.safe_load((ROOT / Q).read_text())
        self.e = json.loads((ROOT / E).read_text())
        self.c = yaml.safe_load((ROOT / C).read_text())
        # Exercise prequalification even after publication; never modify repository files.
        self.q["state"] = "PREQUALIFICATION"
        self.q["release_gates"] = dict.fromkeys(GATES, "PENDING")
        self.q["qualified_capabilities"] = dict.fromkeys(CAPABILITIES, "PENDING")
        self.q["release_cut"].update(candidate_sha=None, publication_authorized=False)
        self.q["bounded_or_residual"]["historical_squash_dco"] = "DISCREPANCY_REQUIRES_OWNER_DISPOSITION"
        self.e.update(candidate_sha=None, publication_authorized=False, gates={
            g: dict(result="PENDING", candidate_sha=None, source=None) for g in GATES})
    def check(self):
        for rel in self.q["evidence"].values():
            if rel.startswith("https://"):
                continue
            if rel in (Q,E,C):
                continue
            p = self.root / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.touch()
        for rel, value in ((Q,self.q),(C,self.c),(E,self.e)):
            p = self.root / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(json.dumps(value) if rel == E else yaml.safe_dump(value))
        return validate(self.root)
    def test_candidate_is_valid_and_non_authorizing(self):
        self.assertEqual(self.check(), [])
        self.assertTrue(assess(self.e))
    def test_prequalification_rejects_approval_and_pass(self):
        self.e["publication_authorized"] = True
        self.q["release_gates"]["owner_approval"] = "PASS"
        self.assertTrue(self.check())
    def test_evidence_inventory_cannot_disappear(self):
        del self.q["evidence"]["security_disposition"]
        self.assertTrue(self.check())
    def test_residual_cannot_be_promoted(self):
        self.q["bounded_or_residual"]["people_impact_causal_pathways"] = "PASS"
        self.assertTrue(self.check())
    def test_candidate_history_cannot_authorize(self):
        self.c["candidate"]["publication_authorized"] = True
        self.assertTrue(self.check())
    def qualified(self):
        sha = "a"*40
        self.q["state"] = "QUALIFIED"
        self.q["release_gates"] = dict.fromkeys(GATES,"PASS")
        self.q["qualified_capabilities"] = dict.fromkeys(CAPABILITIES,"PASS")
        self.q["release_cut"].update(candidate_sha=sha,publication_authorized=True)
        self.q["bounded_or_residual"]["historical_squash_dco"] = "DISCLOSED_OWNER_ACCEPTED"
        self.e.update(candidate_sha=sha,publication_authorized=True,gates={
            g:dict(result="PASS",candidate_sha=sha,source="https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1179") for g in GATES})
        self.e["gates"]["owner_approval"].update(decision="GO",historical_dco_disposition="ACCEPT_DISCLOSED_EXCEPTION")
    def test_qualified_fixture_requires_exact_evidence(self):
        self.qualified()
        self.assertEqual(self.check(), [])
        self.e["gates"]["full_regression"]["candidate_sha"] = "b"*40
        self.assertTrue(self.check())
    def test_historical_dco_disposition_required(self):
        self.qualified()
        del self.e["gates"]["owner_approval"]["historical_dco_disposition"]
        self.assertTrue(self.check())
    def test_null_qualified_sha_refused(self):
        self.qualified()
        self.e["candidate_sha"] = None
        self.assertTrue(self.check())
    def test_missing_gate_refused(self):
        self.qualified()
        del self.e["gates"]["security_review"]
        self.assertTrue(self.check())

if __name__ == "__main__":
    unittest.main()
