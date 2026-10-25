from __future__ import annotations

import unittest
from pathlib import Path

from tools import dpip_handoff


class DPIPHandoffTests(unittest.TestCase):
    def test_historical_monitor_provenance_remains_supported(self) -> None:
        body = """```yaml
dpip:
  recommendation: examine
  affected_interactions: [C3]
  affected_reference_flows: [RF-001]
  affected_invariants: [P2, P4]
  source_change:
    monitor_fingerprint: fp-123
    repository: example/source
    revision: deadbeef
  question: Does the change widen effective correlation scope?
```"""
        payload = dpip_handoff.handoff_payload(body)
        self.assertEqual([], dpip_handoff.validate_payload(payload))
        first = dpip_handoff.identity(12, payload)
        second = dpip_handoff.identity(12, payload)
        self.assertEqual(first, second)
        self.assertIn("fp-123", first[0])

    def test_gatherer_native_provenance_is_supported(self) -> None:
        payload = {
            "affected_interactions": ["C3"],
            "affected_invariants": ["P2"],
            "source_change": {
                "gatherer_run_id": "gha-33000000000-1",
                "gatherer_event_id": "a" * 20,
                "repository": "OpenVTC/openvtc",
                "revision": "b" * 40,
            },
            "question": "Does the gathered change widen effective correlation scope?",
        }
        self.assertEqual([], dpip_handoff.validate_payload(payload))
        marker, _ = dpip_handoff.identity(91, payload)
        self.assertIn("gha-33000000000-1", marker)
        self.assertNotIn("monitor", marker)

    def test_promotion_gate_rejects_missing_lineage(self) -> None:
        payload = {
            "affected_interactions": ["C3"],
            "source_change": {"repository": "example/source", "revision": "deadbeef"},
            "question": "Does this need DPIP?",
        }
        problems = dpip_handoff.validate_payload(payload)
        self.assertTrue(any("gatherer_run_id" in problem and "monitor_fingerprint" in problem for problem in problems))

    def test_promotion_gate_rejects_missing_question(self) -> None:
        payload = {
            "affected_interactions": ["C3"],
            "source_change": {
                "gatherer_run_id": "gha-123-1",
                "repository": "example/source",
                "revision": "deadbeef",
            },
            "question": "",
        }
        problems = dpip_handoff.validate_payload(payload)
        self.assertTrue(any("question" in problem for problem in problems))

    def test_promotion_gate_rejects_missing_target(self) -> None:
        payload = {
            "source_change": {
                "gatherer_run_id": "gha-123-1",
                "repository": "example/source",
                "revision": "deadbeef",
            },
            "question": "Does this need DPIP?",
        }
        problems = dpip_handoff.validate_payload(payload)
        self.assertTrue(any("target" in problem for problem in problems))


    def test_consolidated_workflow_globally_serializes_handoff_transport(self) -> None:
        root = Path(__file__).resolve().parents[1]
        workflow = (root / ".github" / "workflows" / "dpip-lifecycle.yml").read_text(encoding="utf-8")
        self.assertIn("issues:\n    types: [labeled]", workflow)
        self.assertIn("github.event.label.name == 'assurance:dpip-requested'", workflow)
        self.assertIn("group: rahp-dpip-handoff", workflow)
        self.assertIn('python3 tools/dpip_handoff.py --issue-number "$EVENT_ISSUE_NUMBER"', workflow)
        self.assertIn("needs.lifecycle.result == 'success'", workflow)
        lifecycle_block = workflow.split("  lifecycle:", 1)[1].split("\n  handoff:", 1)[0]
        self.assertNotIn("github.event_name == 'issues'", lifecycle_block)
        self.assertNotIn("\n          python3 tools/dpip_handoff.py\n", lifecycle_block)


if __name__ == "__main__":
    unittest.main()
