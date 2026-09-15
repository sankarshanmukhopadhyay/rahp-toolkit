import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from policy_structure import ingest_structured_policy, parse_markdown_structure  # noqa: E402
from policy_subject import map_risk_hypotheses, validate_subject  # noqa: E402


class RealPolicyCorpusPressureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.aup_path = ROOT / "examples" / "policy-assurance" / "real" / "github-acceptable-use-policies.md"
        cls.appeal_path = ROOT / "examples" / "policy-assurance" / "real" / "github-appeal-and-reinstatement.md"
        cls.aup_text = cls.aup_path.read_text(encoding="utf-8")
        cls.appeal_text = cls.appeal_path.read_text(encoding="utf-8")

    def _subject(self, text, name):
        return ingest_structured_policy(
            text,
            source_uri=f"https://github.com/github/site-policy/{name}",
            source_version="b9578b546d2506febda1da2cd7431644d58e512c",
            retrieved_at="2026-09-15T00:00:00Z",
        )

    def test_front_matter_is_metadata_not_policy_proposition(self):
        subject = self._subject(self.aup_text, "acceptable-use")
        self.assertEqual([], validate_subject(subject))
        self.assertTrue(subject["document_structure"]["front_matter_excluded_from_propositions"])
        self.assertEqual("GitHub Acceptable Use Policies", subject["document_structure"]["front_matter"]["title"])
        combined = "\n".join(p["source_span"]["text"] for p in subject["propositions"])
        self.assertNotIn("source_blob_sha:", combined)
        self.assertNotIn("retrieved_for_research:", combined)

    def test_heading_hierarchy_is_preserved_on_propositions(self):
        subject = self._subject(self.appeal_text, "appeal")
        appeal_records = [
            p for p in subject["propositions"]
            if "All decisions on Appeal are made by humans" in p["source_span"]["text"]
        ]
        self.assertEqual(1, len(appeal_records))
        titles = [h["title"] for h in appeal_records[0]["structure"]["heading_context"]]
        self.assertEqual(["How this works", "Appeals"], titles)

    def test_list_items_are_independent_source_spans(self):
        structure = parse_markdown_structure(self.aup_text)
        user_safety = [
            unit for unit in structure["units"]
            if unit["kind"] == "list-item"
            and unit["heading_context"]
            and unit["heading_context"][-1]["title"] == "2. User Safety"
        ]
        self.assertGreaterEqual(len(user_safety), 5)
        for unit in user_safety:
            span = unit["source_span"]
            self.assertEqual(span["text"], self.aup_text[span["start"]:span["end"]])

    def test_materially_different_real_policies_produce_different_models(self):
        aup = self._subject(self.aup_text, "acceptable-use")
        appeal = self._subject(self.appeal_text, "appeal")
        self.assertNotEqual(aup["source"]["sha256"], appeal["source"]["sha256"])
        aup_types = {p["type"] for p in aup["propositions"]}
        appeal_types = {p["type"] for p in appeal["propositions"]}
        self.assertIn("prohibition", aup_types)
        self.assertIn("remedy", appeal_types)
        self.assertNotEqual(aup_types, appeal_types)

    def test_discretion_remains_judgment_required_and_non_terminal(self):
        appeal = self._subject(self.appeal_text, "appeal")
        discretionary = [
            p for p in appeal["propositions"]
            if "in its discretion" in p["source_span"]["text"]
        ]
        self.assertTrue(discretionary)
        self.assertTrue(all(p["judgment_required"] for p in discretionary))
        mapped = map_risk_hypotheses(appeal)
        self.assertTrue(all(h["finding_state"] == "hypothesis" for h in mapped["hypotheses"]))

    def test_source_offsets_are_lossless_across_real_policy_units(self):
        for text, name in ((self.aup_text, "acceptable-use"), (self.appeal_text, "appeal")):
            subject = self._subject(text, name)
            for proposition in subject["propositions"]:
                span = proposition["source_span"]
                self.assertEqual(span["text"], text[span["start"]:span["end"]])


if __name__ == "__main__":
    unittest.main()
