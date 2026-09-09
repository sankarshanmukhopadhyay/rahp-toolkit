import json
import pathlib
import unittest

import jsonschema

ROOT = pathlib.Path(__file__).resolve().parents[1]
LIVE_SCHEMA_PATH = ROOT / "method" / "schema" / "assessor-result.schema.json"
PORTABLE_SCHEMA_PATH = ROOT / "schemas" / "rahp-assessor-result-v1.schema.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def valid(schema, value):
    return not list(jsonschema.Draft202012Validator(schema).iter_errors(value))


def base_result(**overrides):
    value = {
        "schema": "rahp-assessor-result/v1",
        "assessor": "DPIP privacy observability",
        "assessment_id": "dpip-privacy-observability:track-b-policy",
        "outcome": "PASS",
        "reason_code": "bounded-privacy-supported",
        "evidence_used": ["dpip-privacy-observability-result/v1:track-b-policy"],
        "residual_risk": "Deployment-wide unlinkability is not established.",
        "action_required": "Reconcile only within the specialist claim boundary.",
    }
    value.update(overrides)
    return value


class AssessorResultContractCharacterizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.live = load(LIVE_SCHEMA_PATH)
        cls.portable = load(PORTABLE_SCHEMA_PATH)

    def test_strict_intersection_used_by_dpip_is_accepted_by_both(self):
        value = base_result(
            provenance={"producer": "dtg-privacy-implementation-profile"},
            details={"ownership_boundary": "DPIP owns privacy semantics; RAHP owns terminal reconciliation."},
        )
        self.assertTrue(valid(self.live, value))
        self.assertTrue(valid(self.portable, value))

    def test_live_consumer_rejects_structured_evidence_entries(self):
        value = base_result(evidence_used=[{"schema": "dpip-privacy-observability-result/v1"}])
        self.assertFalse(valid(self.live, value))

    def test_live_consumer_accepts_details_and_provenance(self):
        value = base_result(provenance={"run": "fixture"}, details={"scope": "bounded"})
        self.assertTrue(valid(self.live, value))

    def test_live_consumer_rejects_legacy_extra_fields(self):
        self.assertFalse(valid(self.live, base_result(boundedness="bounded-runtime")))
        self.assertFalse(valid(self.live, base_result(confidence="high")))
        self.assertFalse(valid(self.live, base_result(unexpected="value")))

    def test_all_portable_outcomes_remain_valid(self):
        for outcome in ("PASS", "FAIL", "INDETERMINATE", "NOT_APPLICABLE"):
            with self.subTest(outcome=outcome):
                self.assertTrue(valid(self.live, base_result(outcome=outcome)))

    def test_schema_representations_are_semantically_equivalent(self):
        # Titles/IDs are publication metadata; the validation surface must not drift.
        live = {k: v for k, v in self.live.items() if k not in {"$id", "title"}}
        portable = {k: v for k, v in self.portable.items() if k not in {"$id", "title"}}
        self.assertEqual(live, portable)


if __name__ == "__main__":
    unittest.main()
