import json
from copy import deepcopy
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator

from tools.comparative_assurance import compare_scope


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "method" / "schema" / "comparative-assurance-digest.schema.json").read_text(encoding="utf-8"))


def component(component_id, resolved_ref="v1", reason="declared target"):
    return {"component_id": component_id, "resolved_ref": resolved_ref, "reason": reason}


def dependency(component_id, treatment="observed_not_assessed", resolved_ref="v1", **extra):
    return {"component_id": component_id, "resolved_ref": resolved_ref, "treatment": treatment, **extra}


def scope(direct=None, dependencies=None, excluded=None, coverage="bounded", limitations=None):
    return {
        "directly_assessed": direct or [],
        "supporting_dependencies": dependencies or [],
        "excluded": excluded or [],
        "coverage_state": coverage,
        "limitations": limitations or [],
    }


class ComparativeAssuranceScopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validator = Draft202012Validator({
            "$schema": SCHEMA["$schema"],
            "$defs": SCHEMA["$defs"],
            **SCHEMA["$defs"]["scopeDelta"],
        })

    def test_equivalent_scope_is_deterministic_and_schema_valid(self):
        value = scope(
            direct=[component("b"), component("a")],
            dependencies=[dependency("dep")],
        )
        first = compare_scope(value, deepcopy(value))
        reordered = deepcopy(value)
        reordered["directly_assessed"].reverse()
        second = compare_scope(value, reordered)
        self.assertEqual(first, second)
        self.assertEqual("equivalent", first["status"])
        self.assertFalse(first["material_change"])
        self.assertEqual([], list(self.validator.iter_errors(first)))

    def test_broader_candidate_scope_is_expansion_not_regression(self):
        baseline = scope(direct=[component("core")])
        candidate = scope(direct=[component("core"), component("new-component")])
        delta = compare_scope(baseline, candidate)
        self.assertEqual("expanded", delta["status"])
        self.assertTrue(delta["material_change"])
        self.assertEqual(["new-component"], delta["newly_admitted_components"])
        self.assertTrue(any("not an assurance regression" in item for item in delta["limitations"]))

    def test_dependency_never_becomes_directly_assessed_by_inclusion(self):
        baseline = scope()
        candidate = scope(dependencies=[dependency("library")])
        delta = compare_scope(baseline, candidate)
        self.assertEqual(["library"], delta["supporting_dependencies"]["added"])
        self.assertEqual([], delta["directly_assessed"]["added"])
        self.assertFalse(delta["material_change"])

    def test_dependency_treatment_change_is_material_by_default(self):
        baseline = scope(dependencies=[dependency("library")])
        candidate = scope(dependencies=[dependency("library", "independently_assessed", independent_assessment_ref="assessment:lib")])
        delta = compare_scope(baseline, candidate)
        self.assertEqual(["library"], delta["supporting_dependencies"]["changed"])
        self.assertTrue(delta["material_change"])

    def test_direct_ref_change_is_material(self):
        baseline = scope(direct=[component("core", "v1")])
        candidate = scope(direct=[component("core", "v2")])
        delta = compare_scope(baseline, candidate)
        self.assertEqual("changed", delta["status"])
        self.assertEqual(["core"], delta["directly_assessed"]["changed"])
        self.assertTrue(delta["material_change"])

    def test_coverage_weakening_is_separate_and_material(self):
        delta = compare_scope(scope(coverage="complete"), scope(coverage="partial"))
        self.assertEqual("weakened", delta["coverage"]["change"])
        self.assertTrue(delta["material_change"])

    def test_profile_can_decline_to_rank_coverage(self):
        profile = {"coverage_order": ["insufficient", "complete"]}
        delta = compare_scope(scope(coverage="bounded"), scope(coverage="partial"), profile)
        self.assertEqual("not_comparable", delta["coverage"]["change"])
        self.assertTrue(any("cannot be ranked" in item for item in delta["limitations"]))

    def test_duplicate_component_identity_is_rejected(self):
        duplicate = scope(direct=[component("core"), component("core", "v2")])
        with self.assertRaisesRegex(ValueError, "duplicate component_id"):
            compare_scope(duplicate, scope())

    def test_profile_controls_dependency_addition_materiality(self):
        baseline = scope()
        candidate = scope(dependencies=[dependency("library")])
        profile = {"scope_materiality": {"supporting_dependency_change": True}}
        self.assertTrue(compare_scope(baseline, candidate, profile)["material_change"])


if __name__ == "__main__":
    unittest.main()
