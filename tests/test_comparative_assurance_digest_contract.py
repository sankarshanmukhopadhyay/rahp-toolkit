import json
from copy import deepcopy
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "method" / "schema" / "comparative-assurance-digest.schema.json"
FIXTURE_DIR = ROOT / "fixtures" / "comparative-assurance"


class ComparativeAssuranceDigestContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.validator = Draft202012Validator(cls.schema, format_checker=FormatChecker())
        cls.valid = json.loads((FIXTURE_DIR / "valid-partial.json").read_text(encoding="utf-8"))

    def errors(self, value):
        return sorted(self.validator.iter_errors(value), key=lambda error: list(error.absolute_path))

    def test_partial_dogwood_eucalyptus_fixture_is_valid(self):
        self.assertEqual([], self.errors(self.valid))

    def test_declared_invalid_fixtures_are_rejected(self):
        for path in sorted(FIXTURE_DIR.glob("invalid-*.json")):
            with self.subTest(path=path.name):
                value = json.loads(path.read_text(encoding="utf-8"))
                self.assertTrue(self.errors(value), f"{path.name} unexpectedly validated")

    def test_assessment_process_improvement_does_not_imply_release_superiority(self):
        process = next(item for item in self.valid["dimensions"] if item["category"] == "assessment_process")
        self.assertEqual("materially_improved", process["judgment"])
        self.assertEqual("indeterminate", self.valid["overall"]["judgment"])
        self.assertFalse(self.valid["overall"]["release_superiority_established"])

    def test_partial_comparability_requires_unmatched_basis(self):
        value = deepcopy(self.valid)
        value["comparability"]["unmatched_basis"] = []
        self.assertTrue(self.errors(value))

    def test_observed_dependency_cannot_carry_independent_assessment_reference(self):
        value = deepcopy(self.valid)
        dependency = value["scope"]["supporting_dependencies"][0]
        dependency["independent_assessment_ref"] = "assessment:invented"
        self.assertTrue(self.errors(value))

    def test_judgment_basis_keeps_justification_and_evidence_distinct(self):
        value = deepcopy(self.valid)
        del value["dimensions"][0]["evidence_refs"]
        self.assertTrue(self.errors(value))


if __name__ == "__main__":
    unittest.main()
