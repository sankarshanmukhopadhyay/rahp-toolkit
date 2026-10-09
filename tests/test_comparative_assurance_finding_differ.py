import json
from copy import deepcopy
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator

from tools.comparative_assurance import compare_findings


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "method" / "schema" / "comparative-assurance-digest.schema.json").read_text(encoding="utf-8"))
PROFILE = json.loads((ROOT / "fixtures" / "comparative-assurance" / "finding-differ-profile.json").read_text(encoding="utf-8"))


def finding(finding_id, disposition="open", evidence=None, **extra):
    return {
        "finding_id": finding_id,
        "disposition": disposition,
        "evidence_refs": evidence or [],
        **extra,
    }


class ComparativeAssuranceFindingDifferTests(unittest.TestCase):
    def setUp(self):
        self.delta_validator = Draft202012Validator({
            "$schema": SCHEMA["$schema"],
            "$defs": SCHEMA["$defs"],
            **SCHEMA["$defs"]["findingDelta"],
        })

    def assert_schema_valid(self, deltas):
        for delta in deltas:
            self.assertEqual([], list(self.delta_validator.iter_errors(delta)))

    def test_stable_identifier_match_precedes_fallback_keys(self):
        baseline = [finding("F-1", criteria_id="C-OLD", affected_components=["a"], claim_id="old")]
        candidate = [finding("F-1", criteria_id="C-NEW", affected_components=["b"], claim_id="new")]
        delta = compare_findings(baseline, candidate, PROFILE)[0]
        self.assertEqual("profile-key:finding_id", delta["match_basis"])
        self.assertEqual("unchanged", delta["state"])

    def test_profile_fallback_matches_renamed_finding(self):
        common = {"criteria_id": "C-1", "affected_components": ["b", "a"], "claim_id": "claim-1"}
        baseline = [finding("OLD", evidence=["E-1"], **common)]
        candidate = [finding("NEW", evidence=["E-1", "E-2"], **common)]
        delta = compare_findings(baseline, candidate, PROFILE)[0]
        self.assertEqual("profile-key:criteria_id+affected_components+claim_id", delta["match_basis"])
        self.assertEqual("evidence_strengthened", delta["state"])
        self.assertEqual("strengthened", delta["evidence_change"])
        self.assertFalse(delta["disposition_changed"])

    def test_titles_do_not_establish_identity(self):
        baseline = [finding("OLD", title="Same title")]
        candidate = [finding("NEW", title="Same title")]
        deltas = compare_findings(baseline, candidate, PROFILE)
        self.assertEqual(["unmatched", "unmatched"], sorted(delta["state"] for delta in deltas))

    def test_ambiguous_profile_key_remains_unmatched(self):
        common = {"criteria_id": "C-1", "affected_components": ["a"], "claim_id": "claim-1"}
        baseline = [finding("B-1", **common), finding("B-2", **common)]
        candidate = [finding("C-1", **common)]
        deltas = compare_findings(baseline, candidate, PROFILE)
        self.assertEqual(3, len(deltas))
        self.assertTrue(all(delta["state"] == "unmatched" for delta in deltas))
        self.assertTrue(any("Ambiguous" in message for delta in deltas for message in delta["limitations"]))

    def test_unmatched_baseline_is_not_resolved(self):
        delta = compare_findings([finding("BASE")], [], PROFILE)[0]
        self.assertEqual("unmatched", delta["state"])
        self.assertIsNone(delta["candidate"])

    def test_candidate_requires_explicit_lineage_to_be_introduced(self):
        implicit = compare_findings([], [finding("NEW")], PROFILE)[0]
        explicit_finding = finding("NEW", lineage_state="introduced")
        explicit = compare_findings([], [explicit_finding], PROFILE)[0]
        self.assertEqual("unmatched", implicit["state"])
        self.assertEqual("introduced", explicit["state"])

    def test_disposition_transition_and_evidence_change_are_independent(self):
        baseline = [finding("F-1", disposition="open", evidence=["E-1"])]
        candidate = [finding("F-1", disposition="resolved", evidence=["E-1"])]
        delta = compare_findings(baseline, candidate, PROFILE)[0]
        self.assertEqual("resolved", delta["state"])
        self.assertEqual("preserved", delta["evidence_change"])
        self.assertTrue(delta["disposition_changed"])

    def test_bidirectional_evidence_change_is_not_ranked(self):
        baseline = [finding("F-1", evidence=["E-1", "E-2"])]
        candidate = [finding("F-1", evidence=["E-2", "E-3"])]
        delta = compare_findings(baseline, candidate, PROFILE)[0]
        self.assertEqual("changed", delta["state"])
        self.assertEqual("not_comparable", delta["evidence_change"])
        self.assertTrue(delta["limitations"])

    def test_output_is_deterministic_under_input_reordering(self):
        baseline = [finding("F-2"), finding("F-1", evidence=["E-1"])]
        candidate = [finding("F-1", evidence=["E-1", "E-2"]), finding("F-3", lineage_state="introduced")]
        first = compare_findings(baseline, candidate, PROFILE)
        second = compare_findings(list(reversed(baseline)), list(reversed(candidate)), deepcopy(PROFILE))
        self.assertEqual(first, second)
        self.assert_schema_valid(first)

    def test_profile_cannot_use_title_as_matching_authority(self):
        with self.assertRaisesRegex(ValueError, "unsupported matching field"):
            compare_findings([], [], {"matching_rules": [["title"]]})


if __name__ == "__main__":
    unittest.main()
