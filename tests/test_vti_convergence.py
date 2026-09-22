from __future__ import annotations

import unittest

from tools import vti_convergence


class VTIConvergenceTests(unittest.TestCase):
    def test_live_event_is_selective_and_consistent(self) -> None:
        summary, errors = vti_convergence.validate()
        self.assertEqual([], errors)
        self.assertEqual(
            {"semantic-completion", "privacy-composition"},
            set(summary["impacted_families"]),
        )
        self.assertNotIn("authority-continuity", set(summary["impacted_families"]))
        self.assertEqual("blocked", summary["rebaseline_state"])

    def test_evidence_only_drift_does_not_stale_composition_families(self) -> None:
        event = vti_convergence.load_yaml(vti_convergence.EVENT)
        evidence_only = next(change for change in event["changes"] if change["class"] == "evidence-only")
        self.assertFalse(evidence_only["invalidates_existing_assessment"])
        self.assertEqual([], evidence_only["affected_families"])
        self.assertFalse(evidence_only["requirement_text_changed"])

    def test_normative_additions_are_mapped_to_impacted_families(self) -> None:
        event = vti_convergence.load_yaml(vti_convergence.EVENT)
        normative = next(change for change in event["changes"] if change["id"] == "VTI-DRIFT-PR33")
        mapped = {
            requirement
            for impact in event["family_impacts"]
            for requirement in impact["triggering_requirements"]
        }
        self.assertTrue(
            {item for item in normative["requirements_added"] if item.startswith("VTI-CMP-")} <= mapped
        )

    def test_historical_baseline_is_not_mutated_by_observation(self) -> None:
        event = vti_convergence.load_yaml(vti_convergence.EVENT)
        history = vti_convergence.load_yaml(vti_convergence.HISTORY)
        self.assertNotEqual(event["baseline"]["commit"], event["observed_head"]["commit"])
        self.assertEqual(event["baseline"]["commit"], history["active_baseline"]["commit"])
        self.assertFalse(event["automatic_repin"])
        self.assertFalse(event["rebaseline"]["baseline_mutated"])


if __name__ == "__main__":
    unittest.main()
