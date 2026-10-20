"""Pinned source-review packet must remain exact, conservative and non-promotional."""
import json
import pathlib
import unittest
import yaml

ROOT=pathlib.Path(__file__).resolve().parents[1]
DOSSIER=ROOT/"method/impact-pathways/source-review-2026-10-20.json"
PILOT=ROOT/"method/impact-pathways/pilot.json"
CATALOGUE=ROOT/"method/catalogue/harm-patterns.yaml"

class SourceAdjudicationTests(unittest.TestCase):
    def test_source_review_tracks_exact_pilot(self):
        review=json.loads(DOSSIER.read_text())
        pilot=json.loads(PILOT.read_text())
        groups={g["corpus_id"]:g for g in pilot["pilot_corpora"]}
        self.assertEqual(review["contract"],"rahp-people-impact-source-review/v1")
        self.assertEqual(len(review["cases"]),2)
        self.assertEqual(len({(c["corpus_id"],c["scenario_id"]) for c in review["cases"]}),2)
        harms={h["id"] for h in yaml.safe_load(CATALOGUE.read_text())["records"]}
        for case in review["cases"]:
            group=groups[case["corpus_id"]]
            row=next(r for r in group["dispositions"] if r["scenario_id"]==case["scenario_id"])
            self.assertEqual(row["status"],case["status"])
            self.assertEqual(case["qualification"]["status_change"],"none")
            self.assertEqual(case["qualification"]["observed_harm"],"not-established")
            self.assertEqual(case["qualification"]["executed_test"],"not-established")
            self.assertNotEqual(case["qualification"]["affected_role"],"qualified")
            self.assertTrue(case["source_support"])
            self.assertTrue(case["countercase"])
            self.assertTrue(case["needed_for_qualification"])
            for relation in case["taxonomy"]:
                self.assertIn(relation["id"],harms)
                self.assertNotEqual(relation["disposition"],"qualified")
            baseline=group["baseline"]
            if "dependencies" in case["source"]:
                expected={(x["source_commit"],x["corpus_id"]) for x in baseline["depends_on"]}
                self.assertEqual(
                    {("4937c70df95e56ed6404b8c004106ecb121a23cf","CORPUS-TRUST-TASKS"),("b89f389abbdae77ba60b673c0836c781c2b54169","CORPUS-DTG-CREDSPEC")},
                    expected)
                self.assertEqual(
                    {x["commit"] for x in case["source"]["dependencies"]},
                    {sha for sha,_ in expected})
            else:
                self.assertEqual(case["source"]["commit"],baseline["source_commit"])
    def test_no_source_review_auto_qualifies(self):
        review=json.loads(DOSSIER.read_text())
        self.assertEqual(sum(c["status"]=="qualified" for c in review["cases"]),0)
        self.assertEqual(sum(t["disposition"]=="qualified" for c in review["cases"] for t in c["taxonomy"]),0)

if __name__=="__main__":unittest.main()
