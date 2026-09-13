import importlib.util
import pathlib
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "resilience_propositions", ROOT / "tools" / "resilience_propositions.py"
)
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


def result_for(*findings):
    return {
        "model": "distributed-resilience-amplification",
        "target": {
            "path": "/tmp/example",
            "type": "implementation",
            "repository": "example/repo",
            "revision": "abc123",
        },
        "findings": list(findings),
    }


def finding(rule, *, status="review-required", evidence_required=None):
    return {
        "id": "DR-001",
        "risk_id": rule,
        "title": "example",
        "status": status,
        "confidence": "medium",
        "required_controls": ["bounded-retry"],
        "evidence_required": evidence_required or ["runtime-test"],
        "evidence": [{"kind": "risk-signal", "path": "src/app.py"}],
    }


class ResiliencePropositionTests(unittest.TestCase):
    def test_rla004_uses_authoritative_mapping_and_preserves_source(self):
        proposition = MOD.normalize_drarm_result(result_for(finding("RLA-004")))[0]
        self.assertEqual(proposition["source"]["model"], "DRARM")
        self.assertEqual(proposition["source"]["rule"], "RLA-004")
        self.assertEqual(
            proposition["mapped_patterns"],
            {
                "risk": "RKP-OPS-02",
                "control": "CTP-OPS-02",
                "guardrail": "GRP-OPS-01",
                "assurance": "ATP-OPS-02",
            },
        )
        self.assertEqual(proposition["mapping_state"], "mapped")
        self.assertEqual(proposition["state"], "evidence-required")

    def test_rla009_remains_first_class_explicitly_unmapped_obligation(self):
        proposition = MOD.normalize_drarm_result(result_for(finding("RLA-009")))[0]
        self.assertEqual(proposition["source"]["rule"], "RLA-009")
        self.assertEqual(proposition["mapped_patterns"], [])
        self.assertEqual(proposition["mapping_state"], "explicitly-unmapped")
        self.assertEqual(proposition["state"], "evidence-required")

    def test_unknown_mapping_is_not_fabricated(self):
        proposition = MOD.normalize_drarm_result(result_for(finding("RLA-999")))[0]
        self.assertEqual(proposition["mapped_patterns"], [])
        self.assertEqual(proposition["mapping_state"], "unmapped")

    def test_static_finding_does_not_become_terminal_assurance(self):
        proposition = MOD.normalize_drarm_result(
            result_for(finding("RLA-004", status="finding"))
        )[0]
        self.assertEqual(proposition["source"]["status"], "finding")
        self.assertEqual(proposition["state"], "evidence-required")
        self.assertNotIn("terminal_outcome", proposition)

    def test_required_evidence_and_target_revision_are_preserved(self):
        proposition = MOD.normalize_drarm_result(
            result_for(finding("RLA-012", evidence_required=["partial-outage-test"]))
        )[0]
        self.assertEqual(proposition["required_evidence"], ["partial-outage-test"])
        self.assertEqual(proposition["target"]["revision"], "abc123")

    def test_invalid_finding_status_is_rejected(self):
        with self.assertRaises(ValueError):
            MOD.normalize_drarm_result(result_for(finding("RLA-004", status="pass")))

    def test_mapping_cannot_mark_rule_both_mapped_and_unmapped(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "mapping.yaml"
            path.write_text(
                "version: 1\nmappings:\n  RLA-004:\n    risk: RKP-OPS-02\nunmapped:\n  RLA-004:\n    rationale: conflict\n",
                encoding="utf-8",
            )
            with self.assertRaises(ValueError):
                MOD.load_mapping(path)


if __name__ == "__main__":
    unittest.main()
