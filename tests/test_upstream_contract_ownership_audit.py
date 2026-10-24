"""Fail-closed contract ownership audit regressions."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "tools/upstream_contract_ownership_audit.py"
spec = importlib.util.spec_from_file_location("contract_ownership_audit", SCRIPT)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class OwnershipAuditTests(unittest.TestCase):
    def test_missing_owned_interface_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaisesRegex(ValueError, "Required owned interface unavailable"):
                audit.inventory(Path(temp), {"review_schema": "missing.json"})

    def test_symlinked_interface_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "good.txt").write_text("data")
            (root / "alias.txt").symlink_to(root / "good.txt")
            with self.assertRaisesRegex(ValueError, "Required owned interface unavailable"):
                audit.inventory(root, {"bad": "alias.txt"})

    def test_inventory_digest_is_content_derived(self):
        import hashlib
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "sample.txt").write_text("abc")
            report = audit.inventory(root, {"sample": "sample.txt"})
            self.assertEqual(report["sample"]["sha256"], hashlib.sha256(b"abc").hexdigest())

    def test_missing_upstream_root_fails_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(FileNotFoundError):
                audit.assess(Path(temp) / "missing", Path(temp))


if __name__ == "__main__":
    unittest.main()
