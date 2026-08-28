import importlib.util
import pathlib
import unittest

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "dtg_portfolio", ROOT / "tools" / "dtg_portfolio.py"
)
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


class DtgSemanticMaterialityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg = yaml.safe_load((ROOT / "instances" / "dtg" / "instance.yaml").read_text())
        cls.target = {
            "repository": "trustoverip/dtgwg-trust-tasks-tf",
            "role": "task-force-workspace",
            "reporting_weight": "high",
            "lifecycle": "active",
            "material_paths": [
                "README.md",
                "docs/**",
                "bindings/**",
                "trust-tasks-rs/**",
                "trust-tasks-ts/**",
                "trust-tasks-proof/**",
                "trust-tasks-https/**",
                "trust-tasks-didcomm/**",
                "trust-tasks-didcomm-v1/**",
                "trust-tasks-capability-client/**",
                "scripts/**",
                ".github/workflows/**",
            ],
        }

    def commit(self, subject):
        return {"commit": {"message": subject}}

    def file(self, filename):
        return {"filename": filename, "status": "modified", "additions": 1, "deletions": 1}

    def test_151_like_release_fanout_still_escalates_real_semantic_change(self):
        files = [
            self.file("specs/provision/integration/0.3/payload.schema.json"),
            self.file("scripts/build-registry.mjs"),
            self.file("trust-tasks-rs/src/payload.rs"),
            self.file("trust-tasks-rs/src/schema_index.rs"),
            self.file("trust-tasks-rs/tests/schema_index.rs"),
        ]
        files += [self.file(f"trust-tasks-capability-client/{name}") for name in ("CHANGELOG.md", "Cargo.toml")]
        commits = [
            self.commit("feat(rs): index the consumer policy by Type URI, not just the schema"),
            self.commit("chore: release v0.17.1"),
        ]
        classification, matched, reasons = MOD.classify(self.target, files, self.cfg, commits)
        self.assertEqual(classification, "assessment")
        self.assertEqual(len(matched), len(files))
        self.assertTrue(any("semantic materiality profile:" in r for r in reasons))
        profile = MOD.materiality_breakdown(files, self.cfg, commits)
        self.assertTrue(profile["buckets"]["normative"])
        self.assertTrue(profile["buckets"]["semantic"])
        self.assertTrue(profile["buckets"]["release"])
        self.assertTrue(profile["release_propagation_present"])
        self.assertFalse(profile["release_propagation_window"])

    def test_183_generated_convergence_becomes_triage_not_broad_assessment(self):
        files = [
            self.file("trust-tasks-ts/CHANGELOG.md"),
            self.file("trust-tasks-ts/package-lock.json"),
            self.file("trust-tasks-ts/package.json"),
            self.file("trust-tasks-ts/src/provision/integration/0.3/payload.ts"),
        ]
        commits = [
            self.commit("fix(ts): regenerate the provision/integration/0.3 binding"),
            self.commit("chore: release @openvtc/trust-tasks 0.16.2"),
        ]
        classification, _, reasons = MOD.classify(self.target, files, self.cfg, commits)
        self.assertEqual(classification, "triage")
        self.assertTrue(any("generated/evidence/release surfaces" in r for r in reasons))
        profile = MOD.materiality_breakdown(files, self.cfg, commits)
        self.assertEqual(len(profile["buckets"]["generated"]), 1)
        self.assertEqual(len(profile["buckets"]["release"]), 3)
        self.assertTrue(profile["release_propagation_window"])

    def test_release_only_fanout_is_informational(self):
        files = [
            self.file("trust-tasks-rs/CHANGELOG.md"),
            self.file("trust-tasks-rs/Cargo.toml"),
            self.file("trust-tasks-ts/CHANGELOG.md"),
            self.file("trust-tasks-ts/package.json"),
            self.file("trust-tasks-ts/package-lock.json"),
        ]
        commits = [self.commit("chore: release v0.17.1")]
        classification, _, reasons = MOD.classify(self.target, files, self.cfg, commits)
        self.assertEqual(classification, "ignore")
        self.assertTrue(any("only release propagation remains" in r for r in reasons))

    def test_dependency_change_is_not_downgraded_to_release_metadata(self):
        files = [
            self.file("trust-tasks-ts/package.json"),
            self.file("trust-tasks-ts/package-lock.json"),
        ]
        commits = [self.commit("chore: bump dependency example-lib to 4.2.0")]
        classification, _, _ = MOD.classify(self.target, files, self.cfg, commits)
        self.assertEqual(classification, "assessment")
        profile = MOD.materiality_breakdown(files, self.cfg, commits)
        self.assertEqual(len(profile["buckets"]["dependency"]), 2)
        self.assertFalse(profile["release_propagation_window"])

    def test_low_weight_fanout_cannot_mask_one_normative_change(self):
        files = [self.file("specs/provision/integration/0.3/payload.schema.json")]
        files += [self.file(f"trust-tasks-rs/crate{i}/CHANGELOG.md") for i in range(25)]
        commits = [self.commit("chore: release v1.2.3")]
        classification, _, _ = MOD.classify(self.target, files, self.cfg, commits)
        self.assertEqual(classification, "assessment")
        profile = MOD.materiality_breakdown(files, self.cfg, commits)
        self.assertEqual(len(profile["buckets"]["normative"]), 1)
        self.assertEqual(len(profile["buckets"]["release"]), 25)

    def test_existing_documentation_only_triage_is_preserved(self):
        files = [self.file("README.md"), self.file("docs/routing.md")]
        commits = [self.commit("docs: clarify canonical repository routing")]
        classification, _, reasons = MOD.classify(self.target, files, self.cfg, commits)
        self.assertEqual(classification, "triage")
        self.assertTrue(any("documentation/routing paths" in r for r in reasons))

    def test_unknown_manifest_change_remains_conservative(self):
        files = [self.file("trust-tasks-rs/Cargo.toml")]
        commits = [self.commit("chore: adjust workspace configuration")]
        classification, _, _ = MOD.classify(self.target, files, self.cfg, commits)
        self.assertEqual(classification, "assessment")


if __name__ == "__main__":
    unittest.main()
