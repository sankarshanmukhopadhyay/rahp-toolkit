from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "tools" / "validate_cross_spec_registry.py"
ASSESSMENT = "examples/cross-spec/trust-tasks--zkp/pressure-test.yaml"


class CrossSpecRegistrySelectionTests(unittest.TestCase):
    def run_validator(self, registry: Path, composition: str | None = None) -> subprocess.CompletedProcess[str]:
        cmd = [sys.executable, str(VALIDATOR), "--registry", str(registry)]
        if composition:
            cmd += ["--composition", composition]
        return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)

    def test_selected_composition_ignores_unrelated_invalid_details(self) -> None:
        data = {
            "profile": {"id": "dtg-test"},
            "compositions": [
                {
                    "id": "selected",
                    "runnable": True,
                    "corpus_id": "CORPUS-SELECTED",
                    "assessment": ASSESSMENT,
                    "evidence_grade": "scenario-baseline",
                    "components": [
                        {"repository": "trustoverip/a", "corpus_id": "A"},
                        {"repository": "trustoverip/b", "corpus_id": "B"},
                    ],
                },
                {
                    "id": "unrelated",
                    "runnable": True,
                    "corpus_id": "CORPUS-UNRELATED",
                    "assessment": "does/not/exist.yaml",
                    "evidence_grade": "scenario-baseline",
                    "components": [
                        {"repository": "invalid", "corpus_id": "C"},
                        {"repository": "trustoverip/d", "corpus_id": "D"},
                    ],
                },
            ],
        }
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "registry.yaml"
            path.write_text(yaml.safe_dump(data), encoding="utf-8")
            selected = self.run_validator(path, "selected")
            self.assertEqual(selected.returncode, 0, selected.stderr)
            self.assertIn("composition=selected", selected.stdout)

            full = self.run_validator(path)
            self.assertNotEqual(full.returncode, 0)
            self.assertIn("does not exist", full.stderr)

    def test_selected_mode_still_enforces_global_id_uniqueness(self) -> None:
        data = {
            "profile": {"id": "dtg-test"},
            "compositions": [
                {
                    "id": "selected",
                    "runnable": True,
                    "corpus_id": "A",
                    "assessment": ASSESSMENT,
                    "evidence_grade": "scenario-baseline",
                    "components": [
                        {"repository": "trustoverip/a", "corpus_id": "A"},
                        {"repository": "trustoverip/b", "corpus_id": "B"},
                    ],
                },
                {
                    "id": "selected",
                    "runnable": False,
                    "components": [],
                },
            ],
        }
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "registry.yaml"
            path.write_text(yaml.safe_dump(data), encoding="utf-8")
            result = self.run_validator(path, "selected")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unique", result.stderr)


if __name__ == "__main__":
    unittest.main()
