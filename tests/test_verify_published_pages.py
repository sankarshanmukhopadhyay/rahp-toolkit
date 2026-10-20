"""Published-route verifier safeguards; no live network in unit tests."""
import unittest
from unittest.mock import patch

from tools import verify_published_pages as pages


class PublishedPagesTests(unittest.TestCase):
    def test_html_and_required_fragments(self):
        self.assertEqual([], pages.observe_document("<!doctype html><html>How to read a corpus dtg-zkp/</html>", ["how to read a corpus", "dtg-zkp/"]))
        self.assertTrue(pages.observe_document("<html></html>", ["dtg-zkp/"]))
        self.assertTrue(pages.observe_document("not html", ["anything"]))

    def test_one_missing_page_fails_entire_observation(self):
        def fake(url):
            if url.endswith("/corpora/vds/"):
                raise OSError("network unavailable")
            return "<!doctype html><html>how to read a corpus vds/ r1 r2 r3 scenario Reading a scenario corpus TT-002 RAHP glossary</html>"
        with patch.object(pages, "fetch", side_effect=fake):
            report = pages.assess("https://example.invalid/rahp-toolkit", ["vds"])
        self.assertEqual("INDETERMINATE", report["disposition"])
        self.assertTrue(any(x["status"] == "INDETERMINATE" for x in report["records"]))

    def test_all_expected_pages_meet_bounded_contract(self):
        with patch.object(pages, "fetch", return_value="<!doctype html><html>how to read a corpus vds/ r1 r2 r3 scenario</html>"):
            report = pages.assess("https://example.invalid/rahp-toolkit", ["vds"])
        self.assertEqual("PASS", report["disposition"])
        self.assertEqual(6, len(report["records"]))


if __name__ == "__main__":
    unittest.main()
