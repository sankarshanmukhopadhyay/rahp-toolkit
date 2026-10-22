import importlib.util
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "build_assurance_registry", ROOT / "tools" / "build_assurance_registry.py"
)
module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(module)


class AssuranceRegistryTests(unittest.TestCase):
    def test_current_catalogue_builds_one_derived_registry(self):
        registry = module.build_registry()
        self.assertEqual(registry["schema"], "rahp-assurance-registry-index/v1")
        self.assertTrue(registry["authority"]["derived"])
        self.assertEqual(
            registry["authority"]["canonical_source"], "method/catalogue/"
        )
        self.assertGreaterEqual(len(registry["entries"]), 10)

        ids = [entry["id"] for entry in registry["entries"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(ids, sorted(ids))

    def test_duplicate_identifier_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            catalogue = Path(tmp)
            self._write_minimal_catalogue(catalogue)
            risk_path = catalogue / "risk-patterns.yaml"
            doc = yaml.safe_load(risk_path.read_text())
            doc["records"].append(
                {
                    "id": "HRM-TST-01",
                    "name": "Duplicate",
                    "description": "A duplicate identifier used only by this negative test.",
                }
            )
            risk_path.write_text(yaml.safe_dump(doc, sort_keys=False))

            with self.assertRaisesRegex(module.RegistryError, "duplicate catalogue id"):
                module.build_registry(catalogue)

    def test_unknown_portable_reference_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            catalogue = Path(tmp)
            self._write_minimal_catalogue(catalogue)
            risk_path = catalogue / "risk-patterns.yaml"
            doc = yaml.safe_load(risk_path.read_text())
            doc["records"][0]["harm_patterns"] = ["HRM-MISSING-99"]
            risk_path.write_text(yaml.safe_dump(doc, sort_keys=False))

            with self.assertRaisesRegex(module.RegistryError, "unknown portable id"):
                module.build_registry(catalogue)

    def test_trust_tasks_assessment_resolves_through_registry(self):
        registry = module.build_registry()
        by_id = {entry["id"]: entry for entry in registry["entries"]}

        assessment_path = ROOT / "examples" / "trust-tasks-spec" / "pressure-test.yaml"
        assessment = yaml.safe_load(assessment_path.read_text(encoding="utf-8"))
        findings = assessment["review"]["findings"]

        family_types = {
            "harm_patterns": "harm_pattern",
            "risk_patterns": "risk_pattern",
            "control_patterns": "control_pattern",
            "guardrail_patterns": "guardrail_pattern",
            "assurance_patterns": "assurance_pattern",
            "evidence_patterns": "evidence_pattern",
        }

        resolved = 0
        for finding in findings:
            portable = finding.get("portable_assurance") or {}
            for family, expected_type in family_types.items():
                for record_id in portable.get(family) or []:
                    self.assertIn(record_id, by_id)
                    entry = by_id[record_id]
                    self.assertEqual(entry["type"], expected_type)
                    self.assertTrue(entry["source"].startswith("method/catalogue/"))
                    resolved += 1

        self.assertGreater(resolved, 0)

        # F-003 is a useful concrete authority/revocation path: the assessment
        # retains its own evidence while the registry resolves reusable method
        # semantics and their canonical source.
        f003 = next(f for f in findings if f["id"] == "F-003")
        self.assertIn("RKP-AUTH-02", f003["portable_assurance"]["risk_patterns"])
        self.assertEqual(by_id["RKP-AUTH-02"]["type"], "risk_pattern")
        self.assertEqual(
            by_id["RKP-AUTH-02"]["source"],
            "method/catalogue/risk-patterns.yaml",
        )
        self.assertIn("ATP-AUTH-02", f003["portable_assurance"]["assurance_patterns"])
        self.assertEqual(by_id["ATP-AUTH-02"]["type"], "assurance_pattern")

    @staticmethod
    def _write_minimal_catalogue(catalogue: Path):
        records = {
            "harm_pattern": [
                {
                    "id": "HRM-TST-01",
                    "name": "Test harm",
                    "definition": "A test-only harm definition long enough for registry testing.",
                }
            ],
            "risk_pattern": [
                {
                    "id": "RKP-TST-01",
                    "name": "Test risk",
                    "description": "A test-only reusable failure mechanism.",
                    "harm_patterns": ["HRM-TST-01"],
                }
            ],
            "control_pattern": [
                {
                    "id": "CTP-TST-01",
                    "name": "Test control",
                    "control_objective": "A test-only control objective.",
                    "risk_patterns": ["RKP-TST-01"],
                }
            ],
            "guardrail_pattern": [
                {
                    "id": "GRP-TST-01",
                    "name": "Test guardrail",
                    "prohibited_state": "A test-only prohibited state.",
                    "risk_patterns": ["RKP-TST-01"],
                    "control_patterns": ["CTP-TST-01"],
                }
            ],
            "assurance_pattern": [
                {
                    "id": "ATP-TST-01",
                    "name": "Test assurance",
                    "assertion": "A test-only assurance proposition.",
                    "control_patterns": ["CTP-TST-01"],
                    "guardrail_patterns": ["GRP-TST-01"],
                    "evidence_patterns": ["EVP-TST-01"],
                }
            ],
            "evidence_pattern": [
                {
                    "id": "EVP-TST-01",
                    "name": "Test evidence",
                    "claim_supported": "A test-only evidence claim.",
                }
            ],
        }

        filenames = module.CATALOGUE_FILES
        for object_type, filename in filenames.items():
            (catalogue / filename).write_text(
                yaml.safe_dump(
                    {
                        "catalogue_version": "1.1.0",
                        "record_type": object_type,
                        "records": records[object_type],
                    },
                    sort_keys=False,
                )
            )


if __name__ == "__main__":
    unittest.main()
