import json
from pathlib import Path
import unittest

from tools.comparative_assurance import build_digest, render_digest_markdown

ROOT = Path(__file__).resolve().parents[1]


class ComparativeAssuranceGeneralityTests(unittest.TestCase):
    def arbitrary_inputs(self):
        baseline = {
            "assessment": {"assessment_id": "Release-Alpha", "artifact_ref": "artifact:alpha", "schema_version": "example-assessment/v3", "profile_id": "supply-chain-profile", "profile_version": "2026.1"},
            "scope": {"directly_assessed": [{"component_id": "service", "resolved_ref": "alpha", "reason": "release target"}], "supporting_dependencies": [], "excluded": [], "coverage_state": "bounded", "limitations": []},
            "findings": [{"finding_id": "SC-1", "disposition": "open", "evidence_refs": ["artifact:alpha#SC-1"]}],
        }
        candidate = {
            "assessment": {"assessment_id": "Release-Beta", "artifact_ref": "artifact:beta", "schema_version": "example-assessment/v3", "profile_id": "supply-chain-profile", "profile_version": "2026.1"},
            "scope": {"directly_assessed": [{"component_id": "service", "resolved_ref": "beta", "reason": "release target"}], "supporting_dependencies": [], "excluded": [], "coverage_state": "bounded", "limitations": []},
            "findings": [{"finding_id": "SC-1", "disposition": "controlled", "evidence_refs": ["artifact:alpha#SC-1", "artifact:beta#SC-1"]}],
            "comparison": {
                "comparison_id": "alpha-to-beta",
                "baseline_assessment_id": "Release-Alpha",
                "candidate_release_disposition": "conditionally_acceptable",
                "dimensions": [{"dimension_id": "supply-chain-assurance", "category": "assurance_outcome", "comparability": "compatible", "judgment": "improved", "confidence": "moderate", "justification": "The declared supply-chain control has stronger evidence.", "evidence_refs": ["artifact:alpha#SC-1", "artifact:beta#SC-1"], "counterevidence_refs": [], "unresolved_limitations": []}],
                "recommendations": [],
                "reassessment_triggers": ["material supply-chain change"],
            },
        }
        profile = {
            "profile": {"id": "generic-release-comparison", "version": "3", "artifact_ref": "profile:generic-release-comparison-v3"},
            "dimensions": ["supply-chain-assurance"],
            "required_dimensions": ["supply-chain-assurance"],
            "require_evidence_for": ["supply-chain-assurance"],
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

    def test_arbitrary_release_family_and_dimension_are_supported(self):
        baseline, candidate, profile = self.arbitrary_inputs()
        digest = build_digest(baseline, candidate, profile)
        self.assertEqual("alpha-to-beta", digest["comparison_id"])
        self.assertEqual("Release-Alpha", digest["baseline"]["assessment_id"])
        self.assertEqual("Release-Beta", digest["candidate"]["assessment_id"])
        self.assertEqual("supply-chain-assurance", digest["dimensions"][0]["dimension_id"])
        self.assertEqual("improved", digest["overall"]["judgment"])
        self.assertEqual("conditionally_acceptable", digest["overall"]["release_disposition"])
        self.assertFalse(digest["overall"]["release_superiority_established"])

    def test_renderer_contains_only_supplied_release_identity(self):
        baseline, candidate, profile = self.arbitrary_inputs()
        markdown = render_digest_markdown(build_digest(baseline, candidate, profile))
        self.assertIn("Release-Alpha", markdown)
        self.assertIn("Release-Beta", markdown)
        self.assertIn("supply-chain-assurance", markdown)
        self.assertNotIn("Dogwood", markdown)
        self.assertNotIn("Eucalyptus", markdown)

    def test_engine_and_cli_do_not_embed_fixture_release_names(self):
        engine = (ROOT / "tools" / "comparative_assurance.py").read_text(encoding="utf-8")
        cli = (ROOT / "tools" / "rahp.py").read_text(encoding="utf-8")
        for name in ("Dogwood", "Eucalyptus", "VTI-Dogwood", "VTI-Eucalyptus"):
            self.assertNotIn(name, engine)
            self.assertNotIn(name, cli)

    def test_arbitrary_output_is_deterministic(self):
        baseline, candidate, profile = self.arbitrary_inputs()
        first = build_digest(baseline, candidate, profile)
        second = build_digest(json.loads(json.dumps(baseline)), json.loads(json.dumps(candidate)), json.loads(json.dumps(profile)))
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
