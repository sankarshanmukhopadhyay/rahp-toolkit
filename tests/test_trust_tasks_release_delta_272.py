"""Offline integrity checks for the frozen Trust Tasks #272 release-delta ledger.

No live GitHub access is needed. Git blob IDs are immutable provenance claims,
not verification that a consumer implemented the corresponding semantics.
"""
import json
import re
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data/assurance/trust-tasks-release-delta-272.json"
HEX40 = re.compile(r"^[a-f0-9]{40}$")
VERSIONS = [
    "trust-tasks-rs-v0.24.4", "trust-tasks-rs-v0.26.3",
    "trust-tasks-rs-v0.27.1", "trust-tasks-rs-v0.29.0",
]
COUNTS = (226, 14, 152)


def read():
    return json.loads(LEDGER.read_text(encoding="utf-8"))


class TrustTasksReleaseDeltaLedgerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = read()

    def test_immutable_release_refs_and_complete_tree_preconditions(self):
        d = self.doc
        self.assertEqual("rahp-trust-tasks-dependency-delta/v1", d["schema"])
        self.assertEqual(VERSIONS, [row["ref"] for row in d["release_refs"]])
        for ref in d["release_refs"]:
            self.assertFalse(ref["truncated"], "partial Git tree cannot evidence exhaustive scope")
            self.assertRegex(ref["git_tree_sha"], HEX40)

    def test_exact_per_interval_normative_inventory(self):
        intervals = self.doc["intervals"]
        self.assertEqual(COUNTS, tuple(x["changed_normative_paths"] for x in intervals))
        self.assertEqual(392, sum(x["changed_normative_paths"] for x in intervals))
        for ix, interval in enumerate(intervals):
            self.assertEqual((VERSIONS[ix], VERSIONS[ix+1]), (interval["from"], interval["to"]))
            self.assertEqual(
                (self.doc["release_refs"][ix]["git_tree_sha"],
                 self.doc["release_refs"][ix+1]["git_tree_sha"]),
                (interval["from_tree"], interval["to_tree"]),
            )
            self.assertEqual(interval["changed_normative_paths"], len(interval["changes"]))
            self.assertEqual(sum(interval["counts_by_family"].values()), len(interval["changes"]))

    def test_each_changed_path_attributed_exactly_once(self):
        rules = self.doc["rules"]
        families = [r["family"] for r in rules]
        self.assertEqual(len(families), len(set(families)), "unique family IDs required")
        self.assertEqual(len({r["path_prefix"] for r in rules}), len(rules))
        for interval in self.doc["intervals"]:
            seen = set()
            counted = Counter()
            for change in interval["changes"]:
                path = change["path"]
                self.assertNotIn(path, seen, f"duplicate changed path: {path}")
                seen.add(path)
                self.assertTrue(path.startswith("specs/"), path)
                self.assertTrue(path.endswith(("spec.md", ".schema.json")), path)
                matches = [r for r in rules if path.startswith(r["path_prefix"])]
                self.assertTrue(matches, f"unclassified: {path}")
                longest = max(matches, key=lambda r: len(r["path_prefix"]))
                self.assertEqual(longest["family"], change["family"], path)
                self.assertNotEqual("other_spec", change["family"],
                                    f"fallback obscures unreviewed new family {path}")
                before, after = change["git_blob_before"], change["git_blob_after"]
                self.assertNotEqual(before, after)
                self.assertTrue(before or after)
                for oid in (before, after):
                    if oid is not None:
                        self.assertRegex(oid, HEX40)
                counted[change["family"]] += 1
            self.assertEqual(dict(counted), interval["counts_by_family"])

    def test_transfers_are_specific_and_noncovering(self):
        allowed = {"transferred", "partial-owner", "not-assessed", "source-only-normative-change"}
        for rule in self.doc["rules"]:
            self.assertIn(rule["classification"], {"new", "uncertain", "transferred"})
            self.assertIn(rule["disposition"], allowed)
            self.assertTrue(rule["limits"].strip())
            self.assertEqual(
                rule["disposition"] in ("transferred", "partial-owner"),
                bool(rule["issue_numbers"]),
                "an owner is required only for a demonstrated partial/exact transfer",
            )
            for owner in rule["issue_numbers"]:
                self.assertIsInstance(owner, int)
                self.assertGreater(owner, 0)

    def test_no_assurance_positive_state_is_manufactured(self):
        d = self.doc
        self.assertFalse(d["runtime_pass"])
        self.assertFalse(d["composition_pass"])
        self.assertEqual("INDETERMINATE_FOR_NEW_CONSUMER_CONFORMANCE", d["assurance"])
        self.assertIn("historical", d["baseline_boundary"].lower())

    def test_high_impact_examples_are_classified_separately(self):
        ix = self.doc["intervals"][-1]
        mapping = {x["path"]: x["family"] for x in ix["changes"]}
        expected = {
            "specs/device/_shared/0.2/device-binding.schema.json": "device_binding",
            "specs/rooms/_shared/0.1/room.schema.json": "rooms",
            "specs/keys/sign-jws/0.1/spec.md": "sign_jws",
            "specs/keys/sign-csr/0.1/spec.md": "sign_csr",
            "specs/keys/sign-sshsig/0.1/spec.md": "sign_sshsig",
            "specs/auth/oob/request/0.1/spec.md": "out_of_band_auth",
            "specs/external/accounts/create/0.1/spec.md": "external_accounts",
        }
        for path, family in expected.items():
            self.assertEqual(family, mapping.get(path), path)
        self.assertEqual(
            "framework_metadata",
            {x["path"]: x["family"] for x in self.doc["intervals"][0]["changes"]}[
                "specs/spec.meta.schema.json"
            ],
        )


if __name__ == "__main__":
    unittest.main()
