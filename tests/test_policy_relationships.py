import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from policy_relationships import build_policy_relationship_model  # noqa: E402
from policy_structure import ingest_structured_policy  # noqa: E402


class PolicyRelationshipResearchTests(unittest.TestCase):
    def _subject(self, text, uri="fixture://primary.md", version="v1"):
        return ingest_structured_policy(text, source_uri=uri, source_version=version)

    def test_definition_use_is_candidate_not_automatic_binding(self):
        subject = self._subject(
            '# Definitions\n\n"Service" means the hosted platform.\n\n# Rules\n\nYou may use the Service only for authorized purposes.'
        )
        model = build_policy_relationship_model(subject)
        bindings = [item for item in model["definition_bindings"] if item["term"] == "Service"]
        self.assertTrue(bindings)
        self.assertTrue(all(item["requires_review"] for item in bindings))
        self.assertTrue(all(item["state"] == "candidate" for item in bindings))

    def test_incorporated_document_stays_unresolved_without_review(self):
        subject = self._subject(
            'You must comply with the [Acceptable Use Policy](https://example.test/aup) when using the Service.'
        )
        model = build_policy_relationship_model(subject)
        rel = model["references"][0]
        self.assertEqual("incorporated-document-candidate", rel["relationship_type"])
        self.assertEqual("unresolved", rel["review_state"])
        self.assertFalse(rel["traversed"])
        self.assertGreater(model["unresolved_judgment_count"], 0)

    def test_reference_review_can_accept_without_traversing(self):
        subject = self._subject('You must comply with the [Policy](https://example.test/policy).')
        raw_ref = subject["document_structure"]["references"][0]
        model = build_policy_relationship_model(
            subject,
            reference_decisions=[{
                "unit_id": raw_ref["unit_id"],
                "target": raw_ref["target"],
                "action": "accept",
                "reviewer": "human",
            }],
        )
        rel = model["references"][0]
        self.assertEqual("accepted", rel["review_state"])
        self.assertFalse(rel["traversed"])

    def test_cross_document_definition_conflict_is_judgment_required(self):
        primary = self._subject('"Service" means the hosted platform.', "fixture://a.md")
        related = self._subject('"Service" means the API and all related software.', "fixture://b.md")
        model = build_policy_relationship_model(primary, related_subjects=[related])
        conflicts = [item for item in model["definition_conflicts"] if item["term"] == "Service"]
        self.assertEqual(1, len(conflicts))
        self.assertEqual("judgment-required", conflicts[0]["state"])
        self.assertIsNone(conflicts[0]["resolution"])

    def test_explicit_precedence_resolution_is_non_legal_and_non_terminal(self):
        primary = self._subject('"Service" means the hosted platform.', "fixture://a.md")
        related = self._subject('"Service" means the API and all related software.', "fixture://b.md")
        initial = build_policy_relationship_model(primary, related_subjects=[related])
        conflict = initial["definition_conflicts"][0]
        model = build_policy_relationship_model(
            primary,
            related_subjects=[related],
            precedence_decisions=[{
                "candidate_id": conflict["id"],
                "winner_subject_sha256": primary["source"]["sha256"],
                "reviewer": "human",
                "rationale": "The reviewed contract hierarchy designates the primary document for this research interpretation.",
            }],
        )
        resolved = model["definition_conflicts"][0]
        self.assertEqual("reviewed-resolution", resolved["state"])
        self.assertFalse(resolved["resolution"]["legal_conclusion"])
        self.assertFalse(resolved["resolution"]["terminal_assurance"])

    def test_precedence_language_is_detected_but_not_auto_resolved(self):
        subject = self._subject("If these terms conflict with product-specific terms, the more specific terms apply.")
        model = build_policy_relationship_model(subject)
        self.assertEqual(1, len(model["precedence_candidates"]))
        self.assertEqual("judgment-required", model["precedence_candidates"][0]["state"])


if __name__ == "__main__":
    unittest.main()
