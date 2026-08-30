import copy
import unittest

from tools.semantic_review_resume import fingerprint, reconcile, validate

REV = "cb01d0a758863fb3a02f9f4eef2c4f15f56c4c3b"


def record(materiality="NOT_MATERIAL", dpip_state="NOT_REQUIRED", dpip_conclusion=None):
    value = {
        "schema": "rahp-semantic-review/v1",
        "lineage": {"id": "clean-room-241"},
        "target": {"repository": "OpenVTC/verifiable-trust-infrastructure", "revision": REV},
        "reviewer": {"actor": "reviewer", "role": "assurance-reviewer", "reviewed_at": "2026-08-30T06:00:00Z"},
        "propositions": ["missing evidence remains explicit"],
        "evidence": [{"id": "source-review", "status": "SATISFIED", "provenance": "immutable target source"}],
        "dimensions": {"risk": "PASS", "harm": "PASS", "security": "PASS", "composition": "PASS"},
        "privacy_materiality": {"decision": materiality, "rationale": "bounded test rationale"},
        "dpip": {"state": dpip_state},
        "acceptance": {"accepted": True},
        "residuals": [],
        "references": ["https://example.test/evidence"],
    }
    if dpip_conclusion:
        value["dpip"]["conclusion"] = dpip_conclusion
    value["acceptance"]["fingerprint"] = fingerprint(value)
    return value


class SemanticReviewResumeTests(unittest.TestCase):
    def test_missing_acceptance_stays_review_required(self):
        value = record(); value["acceptance"]["accepted"] = False
        self.assertEqual(reconcile(value)["terminal"]["colour"], "AMBER")

    def test_not_material_can_reconcile_green(self):
        result = reconcile(record())
        self.assertEqual(result["terminal"]["colour"], "GREEN")
        self.assertEqual(result["dpip"]["state"], "NOT_REQUIRED")

    def test_material_pending_is_amber(self):
        result = reconcile(record("MATERIAL", "REQUIRED_PENDING"))
        self.assertEqual(result["terminal"]["colour"], "AMBER")
        self.assertIn("DPIP", result["terminal"]["reason"])

    def test_material_indeterminate_dpip_is_amber(self):
        self.assertEqual(reconcile(record("MATERIAL", "COMPLETE", "INDETERMINATE"))["terminal"]["colour"], "AMBER")

    def test_material_adverse_dpip_is_red(self):
        self.assertEqual(reconcile(record("MATERIAL", "COMPLETE", "FAIL"))["terminal"]["colour"], "RED")

    def test_wrong_pin_rejected(self):
        self.assertTrue(validate(record(), "0" * 40))

    def test_tampered_semantic_review_rejected(self):
        value = record(); value["dimensions"]["risk"] = "FAIL"
        self.assertTrue(any("fingerprint" in e for e in validate(value)))

    def test_same_review_is_deterministic(self):
        value = record("MATERIAL", "COMPLETE", "PASS")
        self.assertEqual(reconcile(value), reconcile(copy.deepcopy(value)))

    def test_indeterminate_dimension_never_green(self):
        value = record(); value["dimensions"]["security"] = "INDETERMINATE"
        value["acceptance"]["fingerprint"] = fingerprint(value)
        self.assertEqual(reconcile(value)["terminal"]["colour"], "AMBER")

    def test_dpip_state_can_advance_without_reaccepting_semantic_judgment(self):
        value = record("MATERIAL", "REQUIRED_PENDING")
        accepted = value["acceptance"]["fingerprint"]
        value["dpip"] = {"state": "COMPLETE", "conclusion": "INDETERMINATE", "examination": "DPIP#134"}
        value["residuals"].append("runtime evidence still missing")
        value["references"].append("https://example.test/dpip/134")
        self.assertEqual(fingerprint(value), accepted)
        self.assertEqual(validate(value), [])
        self.assertEqual(reconcile(value)["terminal"]["colour"], "AMBER")


if __name__ == "__main__":
    unittest.main()
