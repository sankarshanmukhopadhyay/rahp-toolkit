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

    def file(self, filename, additions=1, deletions=1):
        return {"filename": filename, "status": "modified", "additions": additions, "deletions": deletions}

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

    def test_601_normative_body_is_not_hidden_by_registry_path_scope(self):
        target = {
            "repository": "trustoverip/dtgwg-cred-spec",
            "role": "normative-specification",
            "reporting_weight": "critical",
            "lifecycle": "active",
            # Historical #601 shape: external registry admitted workflows but omitted spec/body.md.
            "material_paths": [".github/workflows/**", "schemas/**", "specs/**", "**/*spec*.md"],
        }
        files = [
            self.file(".github/workflows/menu.yml", 2, 2),
            self.file("spec/body.md", 1016, 67),
            self.file("spec/terms-and-definitions/vac.md", 24, 8),
        ]
        classification, matched, reasons = MOD.classify(target, files, self.cfg, [self.commit("feat!: publish WD02 credential semantics")])
        self.assertEqual(classification, "assessment")
        self.assertIn("spec/body.md", matched)
        self.assertIn("spec/terms-and-definitions/vac.md", matched)
        detail = MOD.semantic_assurance_surfaces("spec/body.md", target, self.cfg)
        self.assertIn("normative-semantics", detail["surfaces"])
        self.assertIn("role-semantic-path", detail["sources"])
        self.assertTrue(any("semantic-only=" in reason for reason in reasons))

    def test_604_persona_implementation_is_not_hidden_by_single_doc_match(self):
        target = {
            "repository": "OpenVTC/openvtc",
            "role": "implementation",
            "reporting_weight": "high",
            "lifecycle": "active",
            # Historical #604 shape: one design doc was configured while substantive source was omitted.
            "material_paths": ["docs/**", ".github/workflows/**"],
        }
        files = [
            self.file("docs/design/tui-architecture.md", 1, 0),
            self.file("openvtc-core/src/persona/binding.rs", 409, 0),
            self.file("openvtc-core/src/persona/correlation.rs", 324, 0),
            self.file("openvtc-core/src/persona/disclosure.rs", 229, 0),
            self.file("openvtc/src/state_handler/persona_actions.rs", 2113, 0),
        ]
        classification, matched, reasons = MOD.classify(target, files, self.cfg, [self.commit("feat(persona): implement binding and disclosure")])
        self.assertEqual(classification, "assessment")
        self.assertIn("openvtc-core/src/persona/binding.rs", matched)
        self.assertIn("openvtc-core/src/persona/correlation.rs", matched)
        self.assertIn("openvtc-core/src/persona/disclosure.rs", matched)
        detail = MOD.semantic_assurance_surfaces("openvtc-core/src/persona/correlation.rs", target, self.cfg)
        self.assertIn("privacy-correlation-disclosure", detail["surfaces"])
        self.assertTrue(any("privacy-correlation-disclosure=" in reason for reason in reasons))

    def test_unmapped_implementation_source_stays_visible_as_triage(self):
        target = {
            "repository": "OpenVTC/openvtc",
            "role": "implementation",
            "reporting_weight": "high",
            "lifecycle": "active",
            "material_paths": ["docs/**"],
        }
        files = [self.file("openvtc-core/src/widget/engine.rs", 40, 3)]
        classification, matched, reasons = MOD.classify(target, files, self.cfg, [self.commit("refactor: change widget engine")])
        self.assertEqual(classification, "triage")
        self.assertEqual(matched, ["openvtc-core/src/widget/engine.rs"])
        self.assertTrue(any("low-confidence" in reason for reason in reasons))

    def test_known_good_vti_security_detection_remains_assessment(self):
        target = {
            "repository": "OpenVTC/verifiable-trust-infrastructure",
            "role": "reference-implementation",
            "reporting_weight": "critical",
            "lifecycle": "active",
            "material_paths": ["docs/**", "src/**", "**/src/**", ".github/workflows/**"],
        }
        files = [
            self.file("src/key_custody/export.rs", 80, 12),
            self.file("src/audit/evidence.rs", 50, 5),
        ]
        classification, _, reasons = MOD.classify(target, files, self.cfg, [self.commit("feat: constrain key export and record audit evidence")])
        self.assertEqual(classification, "assessment")
        self.assertTrue(any("key-custody-export-signing=" in reason for reason in reasons))
        self.assertTrue(any("evidence-observability-audit=" in reason for reason in reasons))


if __name__ == "__main__":
    unittest.main()
