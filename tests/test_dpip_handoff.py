from __future__ import annotations

import unittest

from tools import dpip_handoff


class DPIPHandoffTests(unittest.TestCase):
    def test_extract_validate_and_identity_are_deterministic(self) -> None:
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

    def test_promotion_gate_rejects_missing_question(self) -> None:
        payload = {
            "affected_interactions": ["C3"],
            "source_change": {
                "monitor_fingerprint": "fp-123",
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
                "monitor_fingerprint": "fp-123",
                "repository": "example/source",
                "revision": "deadbeef",
            },
            "question": "Does this need DPIP?",
        }
        problems = dpip_handoff.validate_payload(payload)
        self.assertTrue(any("target" in problem for problem in problems))


if __name__ == "__main__":
    unittest.main()
