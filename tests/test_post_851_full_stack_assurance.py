from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import unittest

import jsonschema

ROOT = Path(__file__).resolve().parents[1]

def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module

CTRL = load_module("assessment_controller_post851", ROOT / "tools" / "assessment_controller.py")
CMP = load_module("composition_compatibility_post851", ROOT / "tools" / "composition_compatibility.py")
SCHEMA = json.loads((ROOT / "method" / "schema" / "assessment-lifecycle.schema.json").read_text(encoding="utf-8"))


class Post851FullStackAssuranceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.record = CTRL.new_lifecycle("post-851")

    def disposition(
        self,
        lens: str,
        *,
        materiality: str = "applicable",
        execution: str = "executed",
        result: str = "PASS",
        maturity: str = "source-only",
        reason: str = "source-pinned evidence",
        provenance: dict | None = None,
        depth: dict | None = None,
    ) -> None:
        if provenance is None and (execution == "executed" or materiality in {"not-applicable", "not-material"}):
            provenance = {"source": "post-851-fixture", "pin": "fixture"}
        CTRL.set_lens_disposition(
            self.record,
            lens,
            materiality=materiality,
            execution=execution,
            result=result,
            evidence_maturity=maturity,
            reason=reason,
            provenance=provenance,
            assurance_depth=depth,
        )

    def test_process_assurance_and_evidence_are_independent_dimensions(self) -> None:
        CTRL.set_run_dimensions(
            self.record,
            process_state="complete",
            assurance_state="indeterminate",
            evidence_maturity="source-only",
        )
        self.assertEqual("complete", self.record["process_state"])
        self.assertEqual("indeterminate", self.record["assurance_state"])
        self.assertEqual("source-only", self.record["evidence_maturity"])
        jsonschema.Draft202012Validator(SCHEMA).validate(self.record)

    def test_851_shape_can_terminate_indeterminate_with_explicit_unexecuted_lens(self) -> None:
        CTRL.set_run_dimensions(
            self.record,
            process_state="complete",
            assurance_state="indeterminate",
            evidence_maturity="source-only",
        )
        self.disposition("rahp", result="INDETERMINATE")
        self.disposition(
            "security",
            execution="required-but-not-executed",
            result="INDETERMINATE",
            maturity="none",
            reason="target implementation not available",
            provenance=None,
        )
        self.disposition("composition", result="KNOWN_RESIDUAL")
        self.disposition(
            "drarm",
            execution="required-but-not-executed",
            result="INDETERMINATE",
            maturity="modeled",
            reason="resilience applicability recorded; target runtime unavailable",
            provenance=None,
            depth={"achieved": "DR-A1", "required": "DR-A3"},
        )
        self.disposition(
            "specialist",
            materiality="not-applicable",
            execution="no-applicable-producer",
            result="N/A",
            maturity="none",
            reason="no specialist proposition in fixture",
        )
        self.assertEqual([], CTRL.full_stack_terminalization_errors(self.record))
        CTRL.assert_full_stack_terminalizable(self.record)
        jsonschema.Draft202012Validator(SCHEMA).validate(self.record)

    def test_silent_security_composition_or_drarm_omission_blocks_terminalization(self) -> None:
        CTRL.set_run_dimensions(
            self.record,
            process_state="complete",
            assurance_state="indeterminate",
            evidence_maturity="source-only",
        )
        self.record["lenses"].pop("security")
        self.record["lenses"].pop("composition")
        self.record["lenses"].pop("drarm")
        errors = CTRL.full_stack_terminalization_errors(self.record)
        self.assertTrue(any("security: lens disposition missing" in e for e in errors), errors)
        self.assertTrue(any("composition: lens disposition missing" in e for e in errors), errors)
        self.assertTrue(any("drarm: lens disposition missing" in e for e in errors), errors)

    def test_process_complete_cannot_synthesize_full_stack_pass(self) -> None:
        CTRL.set_run_dimensions(
            self.record,
            process_state="complete",
            assurance_state="pass",
            evidence_maturity="source-only",
        )
        self.disposition("rahp")
        self.disposition(
            "security",
            execution="required-but-not-executed",
            result="INDETERMINATE",
            maturity="none",
            reason="not executed",
            provenance=None,
        )
        self.disposition("composition")
        self.disposition("drarm", depth={"achieved": "DR-A1", "required": "DR-A3"})
        self.disposition(
            "specialist",
            materiality="not-material",
            execution="no-applicable-producer",
            result="N/A",
            maturity="none",
            reason="not material",
        )
        errors = CTRL.full_stack_terminalization_errors(self.record)
        self.assertTrue(any("security: full-stack PASS prohibited" in e for e in errors), errors)

    def test_security_shaped_rahp_evidence_does_not_count_as_security_execution(self) -> None:
        self.disposition("rahp", reason="RAHP includes replay and proof-purpose cases")
        security = self.record["lenses"]["security"]
        self.assertEqual("required-but-not-executed", security["execution"])
        self.assertEqual("PENDING", security["result"])

    def test_drarm_depth_is_visible_and_silence_is_invalid(self) -> None:
        CTRL.set_run_dimensions(
            self.record,
            process_state="complete",
            assurance_state="indeterminate",
            evidence_maturity="source-only",
        )
        for lens in ("rahp", "security", "composition"):
            self.disposition(lens, result="INDETERMINATE")
        self.disposition(
            "drarm",
            execution="required-but-not-executed",
            result="INDETERMINATE",
            maturity="modeled",
            reason="migration has retry/queue/partial-deployment surfaces",
            provenance=None,
            depth={"achieved": "DR-A1", "required": "DR-A4"},
        )
        self.disposition(
            "specialist",
            materiality="not-applicable",
            execution="no-applicable-producer",
            result="N/A",
            maturity="none",
            reason="not applicable",
        )
        self.assertEqual("DR-A1", self.record["lenses"]["drarm"]["assurance_depth"]["achieved"])
        self.assertEqual("DR-A4", self.record["lenses"]["drarm"]["assurance_depth"]["required"])
        self.assertEqual([], CTRL.full_stack_terminalization_errors(self.record))

        self.record["lenses"].pop("drarm")
        self.assertTrue(any("drarm: lens disposition missing" in e for e in CTRL.full_stack_terminalization_errors(self.record)))

    def test_genericized_870_version_skew_generates_review_propositions(self) -> None:
        descriptor = {
            "schema": "rahp-composition-compatibility/v1",
            "producer": {
                "old": {"semantic_role": "statement", "meaning": "endorsement"},
                "new": {"semantic_role": "statement", "meaning": "predicate"},
            },
            "contract": {
                "old": {"semantic_role": "statement", "meaning": "endorsement"},
                "new": {"semantic_role": "statement", "meaning": "predicate"},
            },
            "consumer": {
                "old": {"semantic_role": "statement", "meaning": "endorsement"},
                "new": {"semantic_role": "statement", "meaning": "predicate"},
            },
            "mixed_version_policy": {
                "old-producer/new-consumer": "explicit-refusal",
                "new-producer/old-consumer": "explicit-refusal",
            },
        }
        rows = CMP.derive_matrix(descriptor)
        self.assertEqual(4, len(rows))
        same = [r for r in rows if r["producer_version"] == r["consumer_version"]]
        mixed = [r for r in rows if r["producer_version"] != r["consumer_version"]]
        self.assertTrue(all(r["state"] == "COMPATIBLE_PROPOSITION" for r in same), rows)
        self.assertTrue(all(r["state"] == "REVIEW_REQUIRED" for r in mixed), rows)
        self.assertTrue(all(r["expected"] == "explicit-refusal" for r in mixed), rows)

    def test_semantic_substitution_is_not_hidden_by_same_version(self) -> None:
        descriptor = {
            "schema": "rahp-composition-compatibility/v1",
            "producer": {
                "old": {"semantic_role": "authority", "meaning": "endorsement-role"},
                "new": {"semantic_role": "authority", "meaning": "bounded-action-grant"},
            },
            "contract": {
                "old": {"semantic_role": "authority", "meaning": "endorsement-role"},
                "new": {"semantic_role": "authority", "meaning": "endorsement-role"},
            },
            "consumer": {
                "old": {"semantic_role": "authority", "meaning": "endorsement-role"},
                "new": {"semantic_role": "authority", "meaning": "bounded-action-grant"},
            },
            "mixed_version_policy": {
                "old-producer/new-consumer": "unspecified",
                "new-producer/old-consumer": "unspecified",
            },
        }
        rows = CMP.derive_matrix(descriptor)
        new_new = next(r for r in rows if r["producer_version"] == "new" and r["consumer_version"] == "new")
        self.assertEqual("REVIEW_REQUIRED", new_new["state"])
        self.assertFalse(new_new["semantic_match"])


if __name__ == "__main__":
    unittest.main()
