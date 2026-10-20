"""Public entry-point checks for the newcomer scenario reading guide."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReadingScenarioCorpusGuideTest(unittest.TestCase):
    def test_guide_has_jekyll_front_matter_and_explicit_limitations(self):
        source = (ROOT / "docs/reading-scenario-corpus.md").read_text()
        self.assertTrue(source.startswith("---\n"))
        for phrase in ("TT-002", "Not declared", "**not** evidence", "not automatically", "unknown"):
            self.assertIn(phrase.lower(), source.lower())

    def test_reader_entry_points_link_to_guide(self):
        for path in ("index.md", "docs/index.md", "corpora/index.md", "docs/scenario-corpora.md", "docs/concepts.md"):
            with self.subTest(path=path):
                self.assertIn("reading-scenario-corpus.md", (ROOT / path).read_text())


if __name__ == "__main__":
    unittest.main()
