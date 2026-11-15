import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from policy_structure import ingest_structured_policy  # noqa: E402


class StructuralPolicySemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path = ROOT / "examples" / "policy-assurance" / "real" / "github-terms-structural-snapshot.md"
        cls.text = cls.path.read_text(encoding="utf-8")
        cls.subject = ingest_structured_policy(
            cls.text,
            source_uri="https://github.com/github/site-policy/Policies/github-terms/github-terms-of-service.md",
            source_version="b9578b546d2506febda1da2cd7431644d58e512c",
            retrieved_at="2026-09-15T00:00:00Z",
        )

    def test_definitions_are_detected_as_candidates(self):
        terms = {item["term"] for item in self.subject["document_structure"]["definitions"]}
        self.assertIn("Account", terms)
        self.assertIn("Agreement", terms)
        self.assertIn("Service", terms)
        self.assertIn("Website", terms)
        self.assertTrue(all(item["review_state"] == "candidate" for item in self.subject["document_structure"]["definitions"]))

    def test_incorporated_policy_links_are_candidates_not_traversed(self):
        refs = self.subject["document_structure"]["references"]
        acceptable = [r for r in refs if "acceptable-use-policies" in r["target"]]
        self.assertEqual(1, len(acceptable))
        self.assertEqual("incorporated-document-candidate", acceptable[0]["reference_kind"])
        self.assertFalse(acceptable[0]["traversed"])
        self.assertTrue(acceptable[0]["requires_review"])

    def test_section_cross_reference_is_preserved_unresolved(self):
        refs = self.subject["document_structure"]["section_references"]
        section_e = [r for r in refs if r["section"].upper() == "E"]
        self.assertTrue(section_e)
        self.assertTrue(all(not item["resolved"] for item in section_e))

    def test_proposition_facets_are_candidates_and_review_required(self):
        records = [
            p for p in self.subject["propositions"]
            if "We may refuse or remove User-Generated Content" in p["source_span"]["text"]
        ]
        self.assertEqual(1, len(records))
        facets = records[0]["facets"]
        self.assertIn("operator", facets["actors"])
        self.assertIn("remove", facets["consequence_candidates"])
        self.assertTrue(facets["requires_review"])
        self.assertEqual("deterministic-facet-candidate", facets["derivation"])

    def test_precedence_language_remains_source_statement_not_resolved_rule(self):
        records = [
            p for p in self.subject["propositions"]
            if "the more specific terms apply" in p["source_span"]["text"]
        ]
        self.assertEqual(1, len(records))
        self.assertEqual("direct-source-statement", records[0]["derivation"])
        self.assertFalse(self.subject["authority_boundary"]["facet_candidates_are_reviewed_facts"])


if __name__ == "__main__":
    unittest.main()
