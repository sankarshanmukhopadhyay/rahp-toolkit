import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location(
    "registry_route_gate", Path(__file__).resolve().parents[1] / "tools/registry_route_gate.py"
)
assert spec and spec.loader
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


class RoutingGateTest(unittest.TestCase):
    def event(self):
        return {"assessment_key": "dtg:portfolio:combined:identity-review",
                "body": "# Bounded combined review\n\n| Finding | Repository | Change |"}

    def groups(self, **overrides):
        return {**{"controller": [], "combined": [], "dpip": []}, **overrides}

    def test_controller_cannot_be_retained_as_external_toolkit_issue(self):
        item = gate.audit(self.groups(controller=[self.event()]))["events"][0]
        self.assertIn("controller_requires_non_issue_execution_state", item["blockers"])

    def test_specialist_outbox_must_remain_compatible(self):
        item = gate.audit(self.groups(dpip=[self.event()]))["events"][0]
        self.assertIn("dpip_return_requires_controller_compatible_transport", item["blockers"])

    def test_current_combined_event_lacks_routing_proofs(self):
        item = gate.audit(self.groups(combined=[self.event()]))["events"][0]
        self.assertIn("missing_source_pins", item["blockers"])
        self.assertIn("missing_accepted_external_owner", item["blockers"])

    def test_combined_worker_remains_blocker_even_with_pins(self):
        x = self.event()
        x.update(source_pins=[{"repository": "OpenVTC/verifiable-trust-infrastructure",
                               "revision": "a" * 40}],
                 responsible_owner="OpenVTC/verifiable-trust-infrastructure")
        self.assertIn("combined_worker_requires_registry_aware_consumer",
                      gate.audit(self.groups(combined=[x]))["events"][0]["blockers"])

    def test_duplicate_event_across_channels_rejected(self):
        result = gate.audit(self.groups(controller=[self.event()], combined=[self.event()]))
        self.assertIn("duplicate_assessment_key", result["events"][1]["blockers"])

    def test_malformed_source_pin_detected(self):
        x = self.event()
        x.update(source_pins=[{"repository": "OpenVTC/verifiable-trust-infrastructure",
                               "revision": "main"}], responsible_owner="OpenVTC/vti")
        self.assertIn("invalid_source_pins",
                      gate.audit(self.groups(combined=[x]))["events"][0]["blockers"])

    def test_bad_input_fails(self):
        with self.assertRaises(ValueError):
            gate.audit(self.groups(dpip={}))

    def test_empty_snapshot_is_not_live_cutover_approval(self):
        result = gate.audit(self.groups())
        self.assertFalse(result["live_cutover_authorized"])
        self.assertEqual(result["blocked"], 0)


if __name__ == "__main__":
    unittest.main()
