from __future__ import annotations

import copy
import json
from pathlib import Path
import tempfile
import unittest

import yaml

from tools import validate_negative_fixtures as validator


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schemas" / "negative-fixture.schema.json").read_text(encoding="utf-8"))
EXAMPLE = ROOT / "fixtures" / "negative" / "rahp-collective-authority.yaml"


class NegativeFixtureContractTests(unittest.TestCase):
    def test_repository_contract_is_valid_and_cross_lens(self) -> None:
        summary, errors = validator.validate_all()
        self.assertEqual([], errors)
        self.assertEqual(
            {"rahp", "security", "composition", "drarm", "specialist"},
            set(summary["lenses"]),
        )
        self.assertEqual("enforced", summary["missing_evidence_invariant"])
        self.assertEqual("enforced", summary["positive_control_requirement"])

    def test_missing_material_evidence_cannot_become_pass(self) -> None:
        fixture = yaml.safe_load(EXAMPLE.read_text(encoding="utf-8"))
        fixture["expected"]["state"] = "pass"
        fixture["expected"]["terminal_colour"] = "green"
        fixture["expected"]["prohibited"] = ["reject", "red"]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.yaml"
            path.write_text(yaml.safe_dump(fixture, sort_keys=False), encoding="utf-8")
            _loaded, errors = validator.validate_fixture(path, SCHEMA)
        self.assertTrue(any("deficient material evidence" in error for error in errors), errors)

    def test_positive_control_must_resolve(self) -> None:
        fixture = yaml.safe_load(EXAMPLE.read_text(encoding="utf-8"))
        fixture["positive_control"]["ref"] = "tests/fixtures/does-not-exist.yaml"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.yaml"
            path.write_text(yaml.safe_dump(fixture, sort_keys=False), encoding="utf-8")
            _loaded, errors = validator.validate_fixture(path, SCHEMA)
        self.assertTrue(any("positive_control" in error and "does not exist" in error for error in errors), errors)

    def test_specialist_fixture_preserves_ownership_boundary(self) -> None:
        specialist = yaml.safe_load(
            (ROOT / "fixtures" / "negative" / "specialist-dpip-boundary.yaml").read_text(encoding="utf-8")
        )
        self.assertTrue(specialist["specialist"]["required"])
        self.assertIn("privacy_applicability", specialist["specialist"]["owns"])
        self.assertIn("authorization", specialist["specialist"]["does_not_own"])

    def test_validator_rejects_specialist_without_boundary(self) -> None:
        fixture = yaml.safe_load(
            (ROOT / "fixtures" / "negative" / "specialist-dpip-boundary.yaml").read_text(encoding="utf-8")
        )
        fixture = copy.deepcopy(fixture)
        fixture["specialist"]["does_not_own"] = []
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.yaml"
            path.write_text(yaml.safe_dump(fixture, sort_keys=False), encoding="utf-8")
            _loaded, errors = validator.validate_fixture(path, SCHEMA)
        self.assertTrue(any("ownership boundary" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
