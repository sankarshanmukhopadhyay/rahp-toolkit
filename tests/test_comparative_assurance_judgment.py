import json
from copy import deepcopy
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator

from tools.comparative_assurance import aggregate_judgment


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "method" / "schema" / "comparative-assurance-digest.schema.json").read_text(encoding="utf-8"))
PROFILE = json.loads((ROOT / "fixtures" / "comparative-assurance" / "release-comparison-profile.json").read_text(encoding="utf-8"))


def dimension(dimension_id, judgment="no_material_change", confidence="high", evidence=None, counterevidence=None):
    return {
        "dimension_id": dimension_id,
        "category": "assurance_outcome",
        "comparability": "compatible",
        "judgment": judgment,
        "confidence": confidence,
        "justification": f"Fixture judgment for {dimension_id}.",
        "evidence_refs": evidence if evidence is not None else [f"evidence:{dimension_id}"],
        "counterevidence_refs": counterevidence or [],
        "unresolved_limitations": [],
    }


def all_dimensions(**judgments):
    return [dimension(item, judgments.get(item, "no_material_change")) for item in PROFILE["dimensions"]]


COMPARABLE = {"status": "compatible", "reasons": [], "matched_basis": ["profile"], "unmatched_basis": []}
NOT_COMPARABLE = {"status": "not_comparable", "reasons": ["Profiles differ."], "matched_basis": [], "unmatched_basis": ["all"]}
SCOPE = {"coverage": {"baseline": "bounded", "candidate": "bounded", "change": "preserved"}}


class ComparativeAssuranceJudgmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validator = Draft202012Validator({
            "$schema": SCHEMA["$schema"],
            "$defs": SCHEMA["$defs"],
            **SCHEMA["$defs"]["overallResult"],
        })

    def test_critical_regression_cannot_be_masked_by_improvements(self):
        values = all_dimensions(
            **{
                "assessment-capability": "materially_improved",
                "evidence-preservation": "improved",
                "privacy-assurance": "materially_regressed",
            }
        )
        result = aggregate_judgment(values, COMPARABLE, SCOPE, PROFILE)
        self.assertEqual("materially_regressed", result["judgment"])
        self.assertEqual("not_acceptable", result["release_disposition"])

    def test_missing_required_evidence_is_indeterminate(self):
        values = all_dimensions()
        values[0]["evidence_refs"] = []
        result = aggregate_judgment(values, COMPARABLE, SCOPE, PROFILE)
        self.assertEqual("indeterminate", result["judgment"])
        self.assertEqual("indeterminate", result["release_disposition"])

    def test_missing_evidence_cannot_mask_established_blocking_regression(self):
        values = all_dimensions(**{"privacy-assurance": "materially_regressed"})
        values[0]["evidence_refs"] = []
        result = aggregate_judgment(values, COMPARABLE, SCOPE, PROFILE)
        self.assertEqual("materially_regressed", result["judgment"])
        self.assertEqual("not_acceptable", result["release_disposition"])
        self.assertTrue(any("Missing required evidence" in item for item in result["unresolved_limitations"]))

    def test_incompatible_assessments_decline_overall_judgment(self):
        result = aggregate_judgment(all_dimensions(), NOT_COMPARABLE, SCOPE, PROFILE)
        self.assertEqual("not_comparable", result["judgment"])
        self.assertEqual("not_applicable", result["release_disposition"])
        self.assertFalse(result["release_superiority_established"])

    def test_improvement_and_regression_produce_mixed(self):
        values = all_dimensions(**{"assessment-capability": "improved", "privacy-assurance": "regressed"})
        result = aggregate_judgment(values, COMPARABLE, SCOPE, PROFILE)
        self.assertEqual("mixed", result["judgment"])

    def test_comparative_improvement_does_not_imply_acceptability(self):
        values = all_dimensions(**{"assessment-capability": "materially_improved"})
        result = aggregate_judgment(values, COMPARABLE, SCOPE, PROFILE)
        self.assertEqual("materially_improved", result["judgment"])
        self.assertEqual("human_judgment_required", result["release_disposition"])
        self.assertFalse(result["release_superiority_established"])

    def test_candidate_release_disposition_remains_independent(self):
        values = all_dimensions(**{"assessment-capability": "improved"})
        result = aggregate_judgment(values, COMPARABLE, SCOPE, PROFILE, "conditionally_acceptable")
        self.assertEqual("improved", result["judgment"])
        self.assertEqual("conditionally_acceptable", result["release_disposition"])

    def test_coverage_below_profile_minimum_is_indeterminate(self):
        scope = {"coverage": {"baseline": "bounded", "candidate": "partial", "change": "weakened"}}
        result = aggregate_judgment(all_dimensions(), COMPARABLE, scope, PROFILE)
        self.assertEqual("indeterminate", result["judgment"])
        self.assertTrue(any("below required" in item for item in result["unresolved_limitations"]))

    def test_missing_required_dimension_is_indeterminate(self):
        result = aggregate_judgment(all_dimensions()[:-1], COMPARABLE, SCOPE, PROFILE)
        self.assertEqual("indeterminate", result["judgment"])
        self.assertTrue(any("Missing required dimension" in item for item in result["unresolved_limitations"]))

    def test_confidence_is_conservative_across_required_dimensions(self):
        values = all_dimensions()
        values[0]["confidence"] = "moderate"
        result = aggregate_judgment(values, COMPARABLE, SCOPE, PROFILE)
        self.assertEqual("moderate", result["confidence"])

    def test_counterevidence_blocks_when_profile_declares_it(self):
        values = all_dimensions()
        values[0]["counterevidence_refs"] = ["counter:E-1"]
        result = aggregate_judgment(values, COMPARABLE, SCOPE, PROFILE)
        self.assertEqual("indeterminate", result["judgment"])
        self.assertIn("counter:E-1", result["counterevidence_refs"])

    def test_output_is_deterministic_and_schema_valid(self):
        values = all_dimensions(**{"assessment-capability": "improved"})
        first = aggregate_judgment(values, COMPARABLE, SCOPE, PROFILE)
        second = aggregate_judgment(list(reversed(values)), deepcopy(COMPARABLE), deepcopy(SCOPE), deepcopy(PROFILE))
        self.assertEqual(first, second)
        self.assertEqual([], list(self.validator.iter_errors(first)))

    def test_unprofiled_dimension_is_rejected(self):
        values = all_dimensions() + [dimension("invented-dimension")]
        with self.assertRaisesRegex(ValueError, "not declared"):
            aggregate_judgment(values, COMPARABLE, SCOPE, PROFILE)


if __name__ == "__main__":
    unittest.main()
