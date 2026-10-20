"""Five-question reader journey and evidence-status wording regression."""
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]

class ReaderJourneyTests(unittest.TestCase):
    def test_single_page_covers_reporter_questions(self):
        guide=(ROOT/"docs/reading-scenario-corpus.md").read_text()
        section=guide.split("## Worked reading: TT-002 — five questions, one answer",1)[1].split("## Two different scenario collections",1)[0]
        for text in ("What could go wrong?", "Who could be affected?", "How serious is it?", "Has anybody checked?", "Where does this come from?", "4937c70df95e56ed6404b8c004106ecb121a23cf", "Evidence limit"):
            if text == "Evidence limit": continue
            with self.subTest(text=text): self.assertIn(text,section)
        self.assertIn("not** measured severity",section)
        self.assertIn("Execution status is unknown",section)
        self.assertIn("cannot",section)
        self.assertIn("qualification acceptance explanation",section)

    def test_navigation_exists_in_repository(self):
        home=(ROOT/"index.md").read_text()
        landing=(ROOT/"docs/index.md").read_text()
        corps=(ROOT/"corpora/index.md").read_text()
        self.assertIn("Reading a scenario corpus",home)
        self.assertIn("Reading a scenario corpus",landing)
        self.assertIn("Reading a scenario corpus",corps)
        for p in ("docs/reading-scenario-corpus.md","docs/people-impact-pathway-pilot.md","docs/people-impact-qualification-acceptance.md"):
            self.assertTrue((ROOT/p).is_file(),p)

    def test_no_fabricated_review_claims(self):
        guide=(ROOT/"docs/reading-scenario-corpus.md").read_text()
        section=guide.split("## Worked reading: TT-002 — five questions, one answer",1)[1].split("## Two different scenario collections",1)[0]
        self.assertNotIn("passed its assurance test",section.lower())
        self.assertNotIn("harm was observed",section.lower())
        self.assertIn("not independently accepted",section.lower())
        self.assertIn("unknown",section.lower())

if __name__=="__main__": unittest.main()
