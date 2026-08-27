from __future__ import annotations

import unittest

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


if __name__ == "__main__":
    unittest.main()
