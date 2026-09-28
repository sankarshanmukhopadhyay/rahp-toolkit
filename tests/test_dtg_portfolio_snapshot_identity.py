from __future__ import annotations

import hashlib
import importlib.util
import json
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "fetch_dtg_portfolio_snapshot.py"
SPEC = importlib.util.spec_from_file_location("fetch_dtg_portfolio_snapshot", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class DtgPortfolioSnapshotIdentityTest(unittest.TestCase):
    def test_digest_is_deterministic_across_mapping_order(self) -> None:
        left = [{"finding_id": "x", "materiality": "high", "meta": {"b": 2, "a": 1}}]
        right = [{"meta": {"a": 1, "b": 2}, "materiality": "high", "finding_id": "x"}]
        self.assertEqual(MODULE.snapshot_digest(left), MODULE.snapshot_digest(right))

    def test_digest_changes_when_snapshot_semantics_change(self) -> None:
        before = [{"finding_id": "x", "state": "open"}]
        after = [{"finding_id": "x", "state": "resolved"}]
        self.assertNotEqual(MODULE.snapshot_digest(before), MODULE.snapshot_digest(after))

    def test_digest_matches_canonical_sha256_contract(self) -> None:
        findings = [{"finding_id": "x", "materiality": "high"}]
        canonical = json.dumps(
            findings,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        self.assertEqual(MODULE.snapshot_digest(findings), hashlib.sha256(canonical).hexdigest())


if __name__ == "__main__":
    unittest.main()
