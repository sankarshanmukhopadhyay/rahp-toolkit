import copy, unittest
from tools.agent_continuity import evaluate

def sample():
    return {"schema":"rahp-agent-continuity/v1","chain":[
      {"agent":"agent:a","principal":"principal:p","authority_id":"auth:1","scope":"repo:x","capabilities":["read","merge"]},
      {"agent":"agent:b","principal":"principal:p","authority_id":"auth:2","parent_authority_id":"auth:1","scope":"repo:x","capabilities":["read"]}],
      "substitution":{"old_agent":"agent:a","new_agent":"agent:b","continuity_evidence":"ev:rotation"},
      "redress":{"challenge_id":"ch:1","action_evidence_id":"ev:action","resolution":"corrected","closed_at":"2026-10-09T10:00:00Z"}}

class Tests(unittest.TestCase):
    def test_valid_chain(self): self.assertEqual(evaluate(sample())["outcome"],"PASS")
    def test_principal_laundering_fails(self):
        p=sample();p["chain"][1]["principal"]="principal:other";self.assertEqual(evaluate(p)["outcome"],"FAIL")
    def test_capability_amplification_fails(self):
        p=sample();p["chain"][1]["capabilities"].append("publish");self.assertEqual(evaluate(p)["outcome"],"FAIL")
    def test_broken_lineage_fails(self):
        p=sample();p["chain"][1]["parent_authority_id"]="auth:other";self.assertEqual(evaluate(p)["outcome"],"FAIL")
    def test_missing_substitution_evidence_indeterminate(self):
        p=sample();p["substitution"]["continuity_evidence"]="";self.assertEqual(evaluate(p)["outcome"],"INDETERMINATE")
    def test_missing_redress_closure_indeterminate(self):
        p=sample();del p["redress"]["closed_at"];self.assertEqual(evaluate(p)["outcome"],"INDETERMINATE")
    def test_input_immutable(self):
        p=sample();q=copy.deepcopy(p);evaluate(p);self.assertEqual(p,q)
if __name__=="__main__": unittest.main()
