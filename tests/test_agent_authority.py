"""Conformance tests for the optional agent authority profile."""
import copy
import unittest
from tools.agent_authority import evaluate

def sample():
    return {
        "schema":"rahp-agent-authority/v1",
        "delegation":{
            "principal":"did:example:principal","delegate":"did:example:agent",
            "capabilities":["repo.read","repo.merge"],"resource_scope":["repo:qbf/example"],
            "validity":{"valid_from":"2026-01-01T00:00:00Z","valid_until":"2026-12-31T23:59:59Z"},
            "constraints":{"human_confirmation_required":True,"max_delegation_depth":1}},
        "action":{"capability":"repo.merge","resource":"repo:qbf/example","evaluated_at":"2026-10-09T10:00:00Z",
                  "revocation_status":"ACTIVE","human_confirmed":True,"delegation_depth":1}}

class AgentAuthorityTests(unittest.TestCase):
    def test_valid_action_passes(self):
        self.assertEqual(evaluate(sample())["outcome"],"PASS")
    def test_read_does_not_imply_merge(self):
        p=sample();p["delegation"]["capabilities"]=["repo.read"]
        self.assertEqual(evaluate(p)["outcome"],"FAIL")
    def test_resource_scope_cannot_expand(self):
        p=sample();p["action"]["resource"]="repo:qbf/other"
        self.assertEqual(evaluate(p)["outcome"],"FAIL")
    def test_expired_delegation_fails(self):
        p=sample();p["action"]["evaluated_at"]="2027-01-01T00:00:00Z"
        self.assertEqual(evaluate(p)["outcome"],"FAIL")
    def test_revoked_or_suspended_fails(self):
        for state in ("REVOKED","SUSPENDED"):
            p=sample();p["action"]["revocation_status"]=state
            with self.subTest(state=state): self.assertEqual(evaluate(p)["outcome"],"FAIL")
    def test_unavailable_revocation_is_indeterminate(self):
        p=sample();p["action"]["revocation_status"]="UNAVAILABLE"
        self.assertEqual(evaluate(p)["outcome"],"INDETERMINATE")
    def test_required_human_confirmation_is_enforced(self):
        p=sample();p["action"]["human_confirmed"]=False
        self.assertEqual(evaluate(p)["outcome"],"FAIL")
        p=sample();del p["action"]["human_confirmed"]
        self.assertEqual(evaluate(p)["outcome"],"INDETERMINATE")
    def test_delegation_depth_cannot_expand(self):
        p=sample();p["action"]["delegation_depth"]=2
        self.assertEqual(evaluate(p)["outcome"],"FAIL")
    def test_missing_resource_scope_is_indeterminate(self):
        p=sample();del p["delegation"]["resource_scope"]
        self.assertEqual(evaluate(p)["outcome"],"INDETERMINATE")
    def test_input_is_not_mutated(self):
        p=sample();before=copy.deepcopy(p);evaluate(p);self.assertEqual(p,before)

if __name__=="__main__": unittest.main()
