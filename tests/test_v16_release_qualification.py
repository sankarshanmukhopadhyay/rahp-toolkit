import json
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


class V16ReleaseQualificationTests(unittest.TestCase):
    def test_stable_v1_contracts_are_preserved(self):
        status = yaml.safe_load((ROOT / "PROJECT-STATUS.yaml").read_text())
        self.assertEqual(status["compatibility"]["engine_contract"], "rahp-engine-contract-v1")
        self.assertEqual(status["compatibility"]["normalized_result_schema"], 1)
        self.assertEqual(status["compatibility"]["evidence_retention_contract"], "rahp-evidence-retention-v1")

    def test_release_workspace_is_synchronized(self):
        self.assertEqual(json.loads((ROOT / "package.json").read_text())["version"], "1.6.0")
        for rel in [
            "packages/schema/package.json",
            "packages/core/package.json",
            "packages/graph/package.json",
            "packages/cli/package.json",
        ]:
            self.assertEqual(json.loads((ROOT / rel).read_text())["version"], "1.6.0")

    def test_source_pinned_corpus_expansion_is_present(self):
        q = yaml.safe_load((ROOT / "method/v1.6-release-qualification.yaml").read_text())
        expected = q["coverage_expectations"]
        corpora = []
        for path in (ROOT / "corpora").rglob("*.yaml"):
            doc = yaml.safe_load(path.read_text()) or {}
            corpus = doc.get("corpus")
            if isinstance(corpus, dict):
                corpora.append(corpus)
        self.assertEqual(len(corpora), expected["total_corpora"])
        self.assertEqual(sum(len(c.get("scenarios") or []) for c in corpora), expected["total_scenarios"])

    def test_release_does_not_silently_promote_maintained_baselines(self):
        registry = yaml.safe_load((ROOT / "examples/current-baselines.yaml").read_text())
        self.assertEqual(registry["current_rahp_release"]["version"], "v1.5.0")
        self.assertTrue(registry["policy"]["historical_records_are_immutable"])

    def test_common_earl_release_metadata_is_recorded(self):
        status = yaml.safe_load((ROOT / "PROJECT-STATUS.yaml").read_text())
        self.assertEqual(status["stable_release"], "1.6.0")
        self.assertEqual(status["release_name"]["common_name"], "Common Earl")
        self.assertEqual(status["release_name"]["scientific_name"], "Tanaecia julii")
        self.assertEqual(status["release_name"]["selected_on"], "2026-08-23")
        self.assertTrue((ROOT / "docs/releases/v1.6.0.md").is_file())


if __name__ == "__main__":
    unittest.main()
