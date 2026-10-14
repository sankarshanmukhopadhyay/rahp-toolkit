"""Adversarial qualification of existing RAHP full-stack integrity gates (#1023).

Synthetic local inputs only. These tests establish narrow guard behaviour,
not source authenticity, controller-wide completeness, or independent assurance.
"""
import unittest

from tools.assessment_controller import (
    FULL_STACK_LENSES,
    assert_full_stack_terminalizable,
    attach_evidence_probe_ledger,
    full_stack_terminalization_errors,
    new_lifecycle,
    set_lens_disposition,
    set_run_dimensions,
    transition,
)


def passing_record():
    record = new_lifecycle("AA-BASELINE")
    set_run_dimensions(
        record, process_state="complete", assurance_state="pass",
        evidence_maturity="automated-conformance",
    )
    for lens in FULL_STACK_LENSES:
        set_lens_disposition(
            record, lens, materiality="applicable", execution="executed",
            result="PASS", evidence_maturity="automated-conformance",
            reason="controlled synthetic positive baseline",
            provenance={"source": "AA-BASELINE-synthetic"},
        )
    return record


class AdversarialFullStackQualification(unittest.TestCase):
    def test_positive_control_is_terminalizable(self):
        record = passing_record()
        self.assertEqual(full_stack_terminalization_errors(record), [])
        assert_full_stack_terminalizable(record)

    def test_AA09_missing_material_lens_blocks_pass(self):
        record = passing_record()
        del record["lenses"]["security"]
        with self.assertRaisesRegex(ValueError, "security: lens disposition missing"):
            assert_full_stack_terminalizable(record)

    def test_AA09_unexecuted_material_lens_blocks_pass(self):
        record = passing_record()
        set_lens_disposition(
            record, "composition", materiality="applicable",
            execution="required-but-not-executed", result="INDETERMINATE",
            evidence_maturity="source-only", reason="synthetic interrupted producer",
        )
        with self.assertRaisesRegex(ValueError, "composition: full-stack PASS prohibited"):
            assert_full_stack_terminalizable(record)

    def test_AA09_terminal_transition_cannot_bypass_lens_guard(self):
        record = passing_record()
        record["state"] = "ASSESSED"
        del record["lenses"]["security"]
        with self.assertRaisesRegex(ValueError, "security: lens disposition missing"):
            transition(record, "TERMINAL", "synthetic bypass attempt", terminal_outcome="PASS")
        self.assertEqual(record["state"], "ASSESSED")

    def test_AA09_removed_entire_lens_ledger_cannot_bypass_guard(self):
        record = passing_record()
        record["state"] = "ASSESSED"
        del record["lenses"]
        with self.assertRaisesRegex(ValueError, "full-stack lens ledger missing"):
            transition(record, "TERMINAL", "synthetic ledger deletion", terminal_outcome="PASS")
        self.assertEqual(record["state"], "ASSESSED")

    def test_AA07_missing_required_probe_blocks_pass(self):
        record = passing_record()
        record["required_evidence"] = ["REQ-A"]
        with self.assertRaisesRegex(ValueError, "required evidence has no attributable probe ledger"):
            assert_full_stack_terminalizable(record)

    def test_AA07_unattempted_requirement_blocks_pass(self):
        record = passing_record()
        record["required_evidence"] = ["REQ-A", "REQ-B"]
        record["evidence_probe_ledger"] = {
            "schema": "rahp-evidence-probe-ledger/v1",
            "requirements": [{"requirement_id": "REQ-A", "attempt_state": "EXECUTED"}],
        }
        with self.assertRaisesRegex(ValueError, "REQ-B: required evidence has no attributable probe attempt"):
            assert_full_stack_terminalizable(record)

    def test_AA07_unavailable_probe_is_attributed_not_conflated_with_success(self):
        record = passing_record()
        record["required_evidence"] = ["REQ-A"]
        attach_evidence_probe_ledger(record, {
            "schema": "rahp-evidence-probe-ledger/v1",
            "requirements": [{
                "requirement_id": "REQ-A", "attempt_state": "ATTEMPTED_UNAVAILABLE",
                "result": "NOT_EVIDENCED",
            }],
        })
        # Probe-attribution validation deliberately does not establish evidence
        # satisfaction. Separate lens and substantive assurance checks are required.
        set_lens_disposition(
            record, "rahp", materiality="applicable",
            execution="required-but-not-executed", result="INDETERMINATE",
            evidence_maturity="none", reason="unavailable required evidence",
        )
        with self.assertRaisesRegex(ValueError, "rahp: full-stack PASS prohibited"):
            assert_full_stack_terminalizable(record)


if __name__ == "__main__":
    unittest.main()
