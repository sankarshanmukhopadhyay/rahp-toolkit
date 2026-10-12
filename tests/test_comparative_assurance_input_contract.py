import json
from copy import deepcopy
from pathlib import Path
import unittest

from tools.comparative_assurance import build_digest

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "fixtures" / "comparative-assurance"


def dimension(dimension_id="assurance", judgment="no_material_change", evidence=None):
    return {
        "dimension_id": dimension_id,
        "category": "assurance_outcome",
        "comparability": "compatible",
        "judgment": judgment,
        "confidence": "high",
        "justification": f"Fixture judgment for {dimension_id}.",
        "evidence_refs": evidence if evidence is not None else [f"evidence:{dimension_id}"],
        "counterevidence_refs": [],
        "unresolved_limitations": [],
    }


def simple_inputs():
    baseline = {
        "assessment": {
            "assessment_id": "release-a",
            "artifact_ref": "artifact:a",
            "schema_version": "example-assessment/v1",
            "profile_id": "example-profile",
            "profile_version": "1",
        },
        "scope": {
            "directly_assessed": [{"component_id": "service", "resolved_ref": "a", "reason": "release target"}],
            "supporting_dependencies": [],
            "excluded": [],
            "coverage_state": "bounded",
            "limitations": [],
        },
        "findings": [{"finding_id": "F-1", "disposition": "open", "evidence_refs": ["evidence:F-1"]}],
    }
    candidate = deepcopy(baseline)
    candidate["comparison"] = {
        "comparison_id": "release-a-to-release-a",
        "baseline_assessment_id": "release-a",
        "dimensions": [dimension()],
        "recommendations": [],
        "reassessment_triggers": [],
    }
    profile = {
        "profile": {"id": "example-comparison", "version": "1", "artifact_ref": "profile:example"},
        "dimensions": ["assurance"],
        "required_dimensions": ["assurance"],
        "require_evidence_for": ["assurance"],
        "matching_rules": [["finding_id"]],
        "minimum_coverage": "bounded",
        "coverage_order": ["insufficient", "partial", "bounded", "complete"],
        "minimum_confidence": "moderate",
        "blocking_judgments": ["materially_regressed"],
        "counterevidence_blocks": True,
        "blocking_release_disposition": "not_acceptable",
        "improvement_establishes_superiority": False,
    }
    return baseline, candidate, profile


class ComparativeAssuranceInputContractTests(unittest.TestCase):
    def test_complete_input_contract_rejects_nested_malformed_candidate(self):
        baseline, candidate, profile = simple_inputs()
        del candidate["scope"]["directly_assessed"][0]["component_id"]
        with self.assertRaisesRegex(ValueError, "invalid candidate assessment input at scope.directly_assessed.0"):
            build_digest(baseline, candidate, profile)

    def test_incompatible_profile_versions_without_equivalence_are_not_comparable(self):
        baseline = json.loads((FIXTURES / "dogwood-assessment.json").read_text(encoding="utf-8"))
        candidate = json.loads((FIXTURES / "eucalyptus-assessment.json").read_text(encoding="utf-8"))
        profile = json.loads((FIXTURES / "release-comparison-profile.json").read_text(encoding="utf-8"))
        profile["compatible_profile_versions"] = []
        digest = build_digest(baseline, candidate, profile)
        self.assertEqual("not_comparable", digest["comparability"]["status"])
        self.assertIn("assessment profile version", digest["comparability"]["unmatched_basis"])
        self.assertEqual("not_comparable", digest["overall"]["judgment"])
        self.assertEqual("not_applicable", digest["overall"]["release_disposition"])

    def test_identical_assessments_produce_bounded_no_change(self):
        baseline, candidate, profile = simple_inputs()
        digest = build_digest(baseline, candidate, profile)
        self.assertEqual("compatible", digest["comparability"]["status"])
        self.assertEqual("equivalent", digest["scope_delta"]["status"])
        self.assertEqual("no_material_change", digest["overall"]["judgment"])
        self.assertEqual("human_judgment_required", digest["overall"]["release_disposition"])
        self.assertFalse(digest["overall"]["release_superiority_established"])

    def test_profile_declared_stale_evidence_is_indeterminate(self):
        baseline, candidate, profile = simple_inputs()
        profile["evidence_freshness"] = {
            "reference_date": "2026-10-12",
            "max_age_days": 30,
            "required_dimensions": ["assurance"],
            "evidence_dates": {"evidence:assurance": "2026-01-01"},
        }
        digest = build_digest(baseline, candidate, profile)
        self.assertEqual("indeterminate", digest["overall"]["judgment"])
        self.assertEqual("indeterminate", digest["overall"]["release_disposition"])
        self.assertTrue(any("Stale required evidence" in item for item in digest["overall"]["unresolved_limitations"]))


if __name__ == "__main__":
    unittest.main()
