import pathlib
import unittest

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
DISPOSITIONS = ROOT / "method" / "catalogue" / "interop-graduation-dispositions.yaml"
ASSURANCE = ROOT / "method" / "catalogue" / "assurance-patterns.yaml"


class InteropPatternGraduationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dispositions = yaml.safe_load(DISPOSITIONS.read_text(encoding="utf-8"))
        assurance = yaml.safe_load(ASSURANCE.read_text(encoding="utf-8"))
        cls.patterns = {record["id"]: record for record in assurance["records"]}

    def test_every_candidate_has_explicit_supported_disposition(self):
        allowed = {
            "already-covered",
            "pattern-refinement",
            "new-generic-pattern",
            "profile-specific",
            "specialist-owned",
            "lab-only",
            "defer",
        }
        candidates = self.dispositions["candidates"]
        self.assertEqual(7, len(candidates))
        for candidate in candidates:
            with self.subTest(candidate=candidate["id"]):
                self.assertIn(candidate["disposition"], allowed)
                self.assertTrue(str(candidate.get("rationale", "")).strip())
                self.assertTrue(str(candidate.get("action", "")).strip())

    def test_referenced_generic_patterns_exist(self):
        for candidate in self.dispositions["candidates"]:
            for pattern_id in candidate.get("generic_patterns", []):
                with self.subTest(candidate=candidate["id"], pattern=pattern_id):
                    self.assertIn(pattern_id, self.patterns)

    def test_portable_already_covered_claims_have_two_distinct_consumer_families(self):
        for candidate in self.dispositions["candidates"]:
            if candidate["disposition"] != "already-covered":
                continue
            consumers = candidate.get("consumers", [])
            families = {consumer["family"] for consumer in consumers}
            with self.subTest(candidate=candidate["id"]):
                self.assertGreaterEqual(len(consumers), 2)
                self.assertIn("dtg-derived", families)
                self.assertIn("independent", families)

    def test_generic_pattern_text_does_not_import_target_vocabulary(self):
        forbidden = [value.lower() for value in self.dispositions["forbidden_generic_vocabulary"]]
        for candidate in self.dispositions["candidates"]:
            for pattern_id in candidate.get("generic_patterns", []):
                rendered = yaml.safe_dump(self.patterns[pattern_id], sort_keys=True).lower()
                for token in forbidden:
                    with self.subTest(candidate=candidate["id"], pattern=pattern_id, token=token):
                        self.assertNotIn(token, rendered)

    def test_unsettled_common_control_is_not_graduated(self):
        candidate = next(c for c in self.dispositions["candidates"] if c["id"] == "common-control-same-subject-integrity")
        self.assertEqual("defer", candidate["disposition"])
        self.assertEqual("RAHP #500", candidate["dependency"])

    def test_profile_specific_candidates_keep_concrete_owner(self):
        profile_specific = [c for c in self.dispositions["candidates"] if c["disposition"] == "profile-specific"]
        self.assertGreaterEqual(len(profile_specific), 1)
        for candidate in profile_specific:
            with self.subTest(candidate=candidate["id"]):
                self.assertTrue(candidate.get("profile_owner"))


if __name__ == "__main__":
    unittest.main()
