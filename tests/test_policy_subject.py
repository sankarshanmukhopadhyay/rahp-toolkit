import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from policy_subject import (  # noqa: E402
    compare_runtime,
    diff_subjects,
    ingest_policy,
    map_risk_hypotheses,
    sha256_text,
    validate_subject,
)


class PolicySubjectResearchTests(unittest.TestCase):
    def _ingest_fixture(self, name: str, version: str = "v1"):
        path = ROOT / "examples" / "policy-assurance" / name
        text = path.read_text(encoding="utf-8")
        return text, ingest_policy(
            text,
            source_uri=f"fixture://{name}",
            source_version=version,
            retrieved_at="2026-09-15T00:00:00Z",
        )

    def test_platform_terms_preserve_exact_source_spans(self):
        source, subject = self._ingest_fixture("platform-terms-v1.md")
        self.assertEqual("rahp-policy-subject/v1", subject["schema"])
        self.assertEqual(sha256_text(source), subject["source"]["sha256"])
        self.assertEqual(4, len(subject["propositions"]))
        self.assertEqual([], validate_subject(subject))

        for proposition in subject["propositions"]:
            span = proposition["source_span"]
            self.assertEqual(span["text"], source[span["start"] : span["end"]])
            self.assertEqual(sha256_text(span["text"]), span["sha256"])
            self.assertEqual("direct-source-statement", proposition["derivation"])

    def test_two_materially_different_documents_classify_without_false_certainty(self):
        _, platform = self._ingest_fixture("platform-terms-v1.md")
        _, privacy = self._ingest_fixture("privacy-notice-v1.md")

        self.assertEqual(
            ["termination", "discretion", "disclosure", "remedy"],
            [p["type"] for p in platform["propositions"]],
        )
        self.assertEqual(
            ["retention", "disclosure", "remedy", "retention"],
            [p["type"] for p in privacy["propositions"]],
        )
        self.assertTrue(platform["propositions"][0]["judgment_required"])
        self.assertIn("undefined_reasonableness", platform["propositions"][0]["ambiguity_signals"])
        self.assertTrue(privacy["propositions"][3]["judgment_required"])
        self.assertIn("legal_dependency", privacy["propositions"][3]["ambiguity_signals"])

    def test_risk_mapping_is_hypothesis_not_terminal_finding(self):
        _, subject = self._ingest_fixture("platform-terms-v1.md")
        mapped = map_risk_hypotheses(subject)
        pattern_ids = {item["risk_pattern"] for item in mapped["hypotheses"]}
        self.assertIn("RKP-GOV-01", pattern_ids)
        self.assertIn("RKP-GOV-03", pattern_ids)
        self.assertIn("RKP-GOV-04", pattern_ids)
        for hypothesis in mapped["hypotheses"]:
            self.assertEqual("hypothesis", hypothesis["finding_state"])
            self.assertTrue(hypothesis["evidence_required"])

    def test_missing_remedy_stays_evidence_gap_not_negative_claim(self):
        text = "We may suspend your account at our sole discretion."
        subject = ingest_policy(text, source_uri="fixture://no-remedy", source_version="v1")
        mapped = map_risk_hypotheses(subject)
        self.assertEqual("INDETERMINATE", mapped["evidence_gaps"][0]["state"])
        self.assertIn("not proof", mapped["evidence_gaps"][0]["reason"])

    def test_policy_delta_requires_reassessment_for_changed_clause(self):
        old_text = "We retain transaction records for seven years.\n\nYou may request correction of inaccurate records."
        new_text = "We retain transaction records for ten years.\n\nYou may request correction of inaccurate records."
        old = ingest_policy(old_text, source_uri="fixture://retention", source_version="v1")
        new = ingest_policy(new_text, source_uri="fixture://retention", source_version="v2")
        delta = diff_subjects(old, new)
        self.assertTrue(delta["reassessment_required"])
        self.assertEqual(1, len(delta["changed"]))
        self.assertTrue(delta["changed"][0]["reassessment_required"])

    def test_identical_policy_delta_is_stable_and_requires_no_reassessment(self):
        text = "Users must protect their authentication secrets."
        first = ingest_policy(text, source_uri="fixture://stable", source_version="v1")
        second = ingest_policy(text, source_uri="fixture://stable", source_version="v1")
        self.assertEqual(diff_subjects(first, second), diff_subjects(first, second))
        self.assertFalse(diff_subjects(first, second)["reassessment_required"])

    def test_runtime_comparison_preserves_evidence_class_separation(self):
        _, subject = self._ingest_fixture("platform-terms-v1.md")
        proposition_id = subject["propositions"][0]["id"]
        comparison = compare_runtime(
            subject,
            [
                {
                    "proposition_id": proposition_id,
                    "evidence_class": "runtime-observation",
                    "observed": False,
                    "evidence_ref": "run://suspension-001",
                }
            ],
        )
        record = comparison["comparisons"][0]
        self.assertEqual("governance-source", record["policy_evidence_class"])
        self.assertEqual("runtime-observation", record["runtime_evidence_class"])
        self.assertEqual("MISMATCH", record["state"])
        self.assertFalse(record["terminal_assurance"])

    def test_runtime_comparison_rejects_policy_text_as_runtime_evidence(self):
        _, subject = self._ingest_fixture("platform-terms-v1.md")
        proposition_id = subject["propositions"][0]["id"]
        with self.assertRaisesRegex(ValueError, "evidence_class=runtime-observation"):
            compare_runtime(
                subject,
                [
                    {
                        "proposition_id": proposition_id,
                        "evidence_class": "governance-source",
                        "observed": True,
                    }
                ],
            )

    def test_tampered_source_span_is_rejected(self):
        _, subject = self._ingest_fixture("platform-terms-v1.md")
        subject = json.loads(json.dumps(subject))
        subject["propositions"][0]["source_span"]["text"] += " tampered"
        errors = validate_subject(subject)
        self.assertTrue(any("sha256 does not match" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
