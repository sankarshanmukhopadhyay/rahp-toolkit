import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "resilience_evidence", ROOT / "tools" / "resilience_evidence.py"
)
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


def proposition():
    return {
        "schema": "rahp-resilience-proposition/v1",
        "type": "resilience",
        "source": {"model": "DRARM", "rule": "RLA-012", "finding_id": "DR-001"},
        "target": {"repository": "example/repo", "revision": "abc123"},
        "state": "evidence-required",
        "required_evidence": ["partial-outage-test"],
    }


def evidence(obligation, **changes):
    value = {
        "obligation_id": obligation["id"],
        "source_model": "DRARM",
        "source_rule": "RLA-012",
        "target_revision": "abc123",
        "evidence_class": "partial-outage-test",
        "assurance_level": "DR-A4",
        "producer": "interop-lab",
        "uri": "https://example.invalid/evidence/run-42",
        "sha256": "a" * 64,
        "collected_at": "2026-09-13T00:00:00Z",
        "sensitivity": "internal",
    }
    value.update(changes)
    return value


class ResilienceEvidenceTests(unittest.TestCase):
    def test_obligation_is_deterministic_and_revision_bound(self):
        first = MOD.make_evidence_obligations(proposition(), "DR-A4")[0]
        second = MOD.make_evidence_obligations(proposition(), "DR-A4")[0]
        self.assertEqual(first, second)
        self.assertEqual(first["proposition"]["revision"], "abc123")
        self.assertEqual(first["state"], "unsatisfied")

    def test_valid_pinned_runtime_evidence_satisfies_obligation(self):
        obligation = MOD.make_evidence_obligations(proposition(), "DR-A4")[0]
        result = MOD.reconcile_evidence(obligation, evidence(obligation))
        self.assertEqual(result["state"], "satisfied")
        self.assertEqual(result["evidence"]["producer"], "interop-lab")

    def test_missing_evidence_remains_unsatisfied(self):
        obligation = MOD.make_evidence_obligations(proposition(), "DR-A4")[0]
        result = MOD.reconcile_evidence(obligation, None)
        self.assertEqual(result["state"], "unsatisfied")
        self.assertNotIn("evidence", result)

    def test_wrong_revision_is_rejected(self):
        obligation = MOD.make_evidence_obligations(proposition(), "DR-A4")[0]
        result = MOD.reconcile_evidence(obligation, evidence(obligation, target_revision="def456"))
        self.assertEqual(result["state"], "unsatisfied")
        self.assertIn("revision", result["reason"])

    def test_wrong_rule_is_rejected(self):
        obligation = MOD.make_evidence_obligations(proposition(), "DR-A4")[0]
        result = MOD.reconcile_evidence(obligation, evidence(obligation, source_rule="RLA-004"))
        self.assertEqual(result["state"], "unsatisfied")
        self.assertIn("rule", result["reason"])

    def test_insufficient_assurance_depth_is_rejected(self):
        obligation = MOD.make_evidence_obligations(proposition(), "DR-A4")[0]
        result = MOD.reconcile_evidence(obligation, evidence(obligation, assurance_level="DR-A3"))
        self.assertEqual(result["state"], "unsatisfied")
        self.assertIn("below DR-A4", result["reason"])

    def test_malformed_evidence_digest_is_rejected(self):
        obligation = MOD.make_evidence_obligations(proposition(), "DR-A4")[0]
        with self.assertRaises(ValueError):
            MOD.reconcile_evidence(obligation, evidence(obligation, sha256="not-a-digest"))

    def test_unpinned_target_cannot_create_obligation(self):
        value = proposition()
        value["target"]["revision"] = None
        with self.assertRaises(ValueError):
            MOD.make_evidence_obligations(value, "DR-A4")

    def test_assurance_depth_is_explicit_not_inferred(self):
        with self.assertRaises(TypeError):
            MOD.make_evidence_obligations(proposition())


if __name__ == "__main__":
    unittest.main()
