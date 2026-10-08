"""R2 conformance: historical coverage, knowledge cutoff, freshness and provenance."""
import copy
import unittest
from tools.temporal_provenance import evaluate_temporal


def fixture():
    return {
        "schema": "rahp-temporal-provenance/v1",
        "proposition_id": "HIST-001",
        "target_time": "2026-04-15T00:00:00Z",
        "knowledge_cutoff": "2026-05-01T00:00:00Z",
        "evaluated_at": "2026-08-20T00:00:00Z",
        "required_evidence": ["ER-1"],
        "records": [{
            "id": "REC-1", "evidence_id": "ER-1",
            "source_pin": {"repository": "example/spec", "revision": "a" * 40},
            "observed_at": "2026-04-15T00:00:00Z",
            "recorded_at": "2026-04-16T00:00:00Z",
            "effective_from": "2026-04-10T00:00:00Z",
            "effective_until": "2026-05-01T00:00:00Z",
        }],
    }


class TemporalProvenanceTests(unittest.TestCase):
    def test_inclusive_start_exclusive_end(self):
        p = fixture()
        p["target_time"] = p["records"][0]["effective_from"]
        self.assertEqual(evaluate_temporal(p)["disposition"], "APPLICABLE")
        p["target_time"] = p["records"][0]["effective_until"]
        self.assertEqual(evaluate_temporal(p)["disposition"], "INDETERMINATE")

    def test_offset_equivalence(self):
        p = fixture()
        p["target_time"] = "2026-04-15T05:30:00+05:30"
        self.assertEqual(evaluate_temporal(p)["disposition"], "APPLICABLE")

    def test_not_yet_known(self):
        p = fixture()
        p["knowledge_cutoff"] = "2026-04-15T00:00:00Z"
        self.assertEqual(evaluate_temporal(p)["findings"][0]["status"], "NOT_KNOWN_AT_CUTOFF")

    def test_retroactive_later_record_is_visible_but_not_applied(self):
        p = fixture()
        later = copy.deepcopy(p["records"][0])
        later.update(id="REC-2", recorded_at="2026-08-15T00:00:00Z",
                     effective_from="2026-04-01T00:00:00Z")
        p["records"].append(later)
        result = evaluate_temporal(p)
        self.assertEqual(result["disposition"], "APPLICABLE")
        self.assertEqual(result["findings"][0]["later_record_ids"], ["REC-2"])
        p["knowledge_cutoff"] = "2026-08-20T00:00:00Z"
        self.assertEqual(evaluate_temporal(p)["findings"][0]["status"], "CONFLICT")

    def test_stale(self):
        p = fixture()
        p["max_observation_age_seconds"] = 3600
        self.assertEqual(evaluate_temporal(p)["findings"][0]["status"], "STALE_OR_FUTURE_OBSERVATION")

    def test_no_implicit_freshness_policy(self):
        self.assertEqual(evaluate_temporal(fixture())["disposition"], "APPLICABLE")

    def test_missing_and_open_interval(self):
        p = fixture()
        p["records"] = []
        self.assertEqual(evaluate_temporal(p)["disposition"], "INDETERMINATE")
        p = fixture()
        p["records"][0]["effective_until"] = None
        p["target_time"] = "2026-07-01T00:00:00Z"
        self.assertEqual(evaluate_temporal(p)["disposition"], "APPLICABLE")

    def test_order_invariance_and_no_mutation(self):
        p = fixture()
        p["required_evidence"].append("ER-2")
        p["records"].append(dict(p["records"][0], id="REC-2", evidence_id="ER-2"))
        q = copy.deepcopy(p)
        q["required_evidence"].reverse()
        q["records"].reverse()
        self.assertEqual(evaluate_temporal(p), evaluate_temporal(q))
        self.assertEqual(p["required_evidence"], ["ER-1", "ER-2"])

    def test_invalid_metadata(self):
        changes = [
            lambda p: p["records"][0].pop("source_pin"),
            lambda p: p["records"][0].update(effective_until="2026-04-10T00:00:00Z"),
            lambda p: p["records"][0].update(recorded_at="2026-04-14T00:00:00Z"),
            lambda p: p.update(knowledge_cutoff="2026-09-01T00:00:00Z"),
            lambda p: p.update(target_time="2026-04-15T00:00:00"),
            lambda p: p.update(max_observation_age_seconds=True),
            lambda p: p.update(required_evidence=["ER-1", "ER-1"]),
            lambda p: p["records"][0].update(evidence_id="UNKNOWN"),
        ]
        for change in changes:
            p = fixture()
            change(p)
            with self.subTest(p=p), self.assertRaises(ValueError):
                evaluate_temporal(p)


if __name__ == "__main__":
    unittest.main()
