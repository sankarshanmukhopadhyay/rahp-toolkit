"""Independent qualification packet invariants: fail closed on stale, unsupported or auto-approved claims."""
import copy
import json
import unittest
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]
PACKET=ROOT/"method/impact-pathways/qualification-acceptance-2026-10-20.json"
PILOT=ROOT/"method/impact-pathways/pilot.json"
SOURCES={"CORPUS-TRUST-TASKS":"corpora/trust-tasks.yaml","CORPUS-TT-CREDSPEC-COMPOSED":"corpora/trust-tasks-credspec-composed.yaml"}

def validate(packet,root=ROOT):
    errors=[]
    if packet.get("contract")!="rahp-impact-qualification-acceptance/v1":
        errors.append("contract mismatch")
    if packet.get("independent_acceptance",{}).get("status") != "not-recorded":
        errors.append("unverified acceptance")
    pilot=json.loads((root/"method/impact-pathways/pilot.json").read_text())
    base={g["corpus_id"]:g for g in pilot["pilot_corpora"]}
    harm={h["id"] for h in yaml.safe_load((root/"method/catalogue/harm-patterns.yaml").read_text())["records"]}
    cases=packet.get("candidates",[])
    names=[c.get("id") for c in cases]
    if len(set(names))!=len(names) or not cases:
        errors.append("duplicate or empty packet")
    for c in cases:
        sid,cid=c.get("scenario_id"),c.get("corpus_id")
        if cid not in SOURCES:
            errors.append(f"{sid}: unknown corpus")
            continue
        corpus=yaml.safe_load((root/SOURCES[cid]).read_text())["corpus"]
        groups=base[cid]
        scenarios={s["id"] for s in corpus["scenarios"]}
        if sid not in scenarios or sid not in {r["scenario_id"] for r in groups["dispositions"]}:
            errors.append(f"{sid}: unknown scenario")
        if c.get("decision") not in {"provisional","not-established","rejected"}:
            errors.append(f"{sid}: unsupported status promotion")
        if not c.get("role") or not c.get("decision_actor") or not c.get("interest") or not c.get("gap"):
            errors.append(f"{sid}: causal roles/interest/gap incomplete")
        if not c.get("countercase") or len(c.get("causal_steps",[]))<2:
            errors.append(f"{sid}: unsupported causal chain")
        if set(c.get("candidate_harms",[]))-harm:
            errors.append(f"{sid}: unknown harm pattern")
        source=c.get("source",{})
        if corpus["source_commit"]=="derived-from-pinned-dependencies":
            deps=source.get("dependencies",[])
            pins={x["commit"] for x in deps}
            expected={x["source_commit"] for x in corpus.get("depends_on",[])}
            if pins!=expected or len(deps)!=len(expected):
                errors.append(f"{sid}: composed dependency pin drift")
        elif source.get("commit")!=corpus["source_commit"]:
            errors.append(f"{sid}: source pin drift")
        if "person_id" in c or "execution_status" in c or "observed_harm" in c:
            errors.append(f"{sid}: inferred observation or persona")
    return errors

class QualificationPacketTests(unittest.TestCase):
    def setUp(self):
        self.packet=json.loads(PACKET.read_text())
    def test_packet(self):
        self.assertEqual(validate(self.packet),[])
        self.assertEqual(len(self.packet["candidates"]),6)
        self.assertEqual(len({x["scenario_id"] for x in self.packet["candidates"]}),4)
        self.assertEqual(sum(x["decision"]=="qualified" for x in self.packet["candidates"]),0)
    def test_no_auto_qualification(self):
        d=copy.deepcopy(self.packet)
        d["candidates"][0]["decision"]="qualified"
        self.assertTrue(validate(d))
    def test_no_unsourced_review(self):
        d=copy.deepcopy(self.packet)
        d["independent_acceptance"]["status"]="approved"
        self.assertTrue(validate(d))
    def test_stale_composed_dependency(self):
        d=copy.deepcopy(self.packet)
        d["candidates"][2]["source"]["dependencies"][0]["commit"]="0"*40
        self.assertTrue(validate(d))
    def test_stale_direct_source(self):
        d=copy.deepcopy(self.packet)
        d["candidates"][0]["source"]["commit"]="0"*40
        self.assertTrue(validate(d))
    def test_no_namespace_confusion(self):
        d=copy.deepcopy(self.packet)
        d["candidates"][0]["scenario_id"]="SEC-TT-002"
        self.assertTrue(validate(d))
    def test_invalid_harm(self):
        d=copy.deepcopy(self.packet)
        d["candidates"][0]["candidate_harms"]=["HRM-NOT-99"]
        self.assertTrue(validate(d))
    def test_missing_consequence(self):
        d=copy.deepcopy(self.packet)
        d["candidates"][0]["causal_steps"]=[]
        self.assertTrue(validate(d))
    def test_invented_personal_and_execution(self):
        d=copy.deepcopy(self.packet)
        d["candidates"][0]["person_id"]="D1"
        self.assertTrue(validate(d))
        d=copy.deepcopy(self.packet)
        d["candidates"][0]["execution_status"]="PASS"
        self.assertTrue(validate(d))
if __name__=="__main__":unittest.main()
