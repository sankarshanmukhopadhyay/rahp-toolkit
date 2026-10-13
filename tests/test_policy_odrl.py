import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from policy_odrl import (  # noqa: E402
    ALIGNMENT_MATRIX,
    ODRL_CONTEXT,
    alignment_matrix,
    ingest_odrl_policy,
    project_reviewed_records,
)


class PolicyOdrlAlignmentTests(unittest.TestCase):
    def test_alignment_matrix_keeps_rahp_only_semantics_outside_odrl(self):
        matrix = alignment_matrix()
        self.assertEqual("rahp-policy-odrl-alignment/v1", matrix["schema"])
        self.assertFalse(matrix["profile_authorized"])
        self.assertEqual("direct", ALIGNMENT_MATRIX["permission"]["status"])
        self.assertEqual("direct", ALIGNMENT_MATRIX["prohibition"]["status"])
        self.assertEqual("partial", ALIGNMENT_MATRIX["obligation"]["status"])
        self.assertEqual("outside-odrl", ALIGNMENT_MATRIX["discretion"]["status"])
        self.assertEqual("outside-odrl", ALIGNMENT_MATRIX["representation"]["status"])

    def test_natural_language_projection_refuses_to_invent_action_or_target(self):
        projected = project_reviewed_records(
            [
                {
                    "id": "pol-1",
                    "type": "permission",
                    "analysis_text": "You may use the service.",
                    "source_proposition_ids": ["pol-1"],
                },
                {
                    "id": "pol-2",
                    "type": "discretion",
                    "analysis_text": "We may act in our sole discretion.",
                    "source_proposition_ids": ["pol-2"],
                },
            ]
        )
        permission = projected["records"][0]
        self.assertEqual("insufficient-structure", permission["projection_state"])
        self.assertEqual(["action", "target"], permission["missing_structured_semantics"])
        self.assertTrue(permission["semantic_loss"])
        discretion = projected["records"][1]
        self.assertEqual("not-applicable", discretion["projection_state"])
        self.assertEqual("outside-odrl", discretion["alignment_status"])

    def test_odrl_native_fixture_is_deterministic_and_nonterminal(self):
        path = ROOT / "examples" / "policy-assurance" / "odrl" / "control-policy.json"
        document = json.loads(path.read_text(encoding="utf-8"))
        first = ingest_odrl_policy(document, source_uri="fixture://odrl-control", source_version="v1")
        second = ingest_odrl_policy(document, source_uri="fixture://odrl-control", source_version="v1")
        self.assertEqual(first, second)
        self.assertEqual(ODRL_CONTEXT, document["@context"])
        self.assertEqual(["permission", "prohibition", "obligation"], [r["rule_type"] for r in first["rules"]])
        self.assertFalse(first["terminal_assurance"])
        self.assertFalse(first["boundary"]["odrl_conformance_implies_rahp_assurance"])
        self.assertFalse(first["boundary"]["rahp_odrl_profile_authorized"])

    def test_odrl_native_fixture_requires_action_and_target(self):
        document = {
            "@context": ODRL_CONTEXT,
            "@type": "Set",
            "uid": "https://example.org/policies/bad",
            "permission": [{"action": "read"}],
        }
        with self.assertRaisesRegex(ValueError, "requires action and target"):
            ingest_odrl_policy(document, source_uri="fixture://bad", source_version="v1")

    def test_wrong_context_is_rejected(self):
        document = {
            "@context": "https://example.org/not-odrl",
            "@type": "Set",
            "uid": "https://example.org/policies/bad-context",
            "permission": [{"action": "read", "target": "https://example.org/asset"}],
        }
        with self.assertRaisesRegex(ValueError, "must use @context"):
            ingest_odrl_policy(document, source_uri="fixture://bad-context", source_version="v1")


if __name__ == "__main__":
    unittest.main()
