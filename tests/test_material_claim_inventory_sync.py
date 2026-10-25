import unittest

from tools import validate_review_readiness as readiness


class MaterialClaimInventorySynchronizationTests(unittest.TestCase):
    def test_all_claim_ids_present_is_accepted(self):
        claims = [{"id": "RCL-001"}, {"id": "RCL-002"}]
        text = "| RCL-001 | claim one |\n| RCL-002 | claim two |\n"
        self.assertEqual(readiness.missing_claim_inventory_ids(claims, text), [])

    def test_missing_claim_id_is_rejected(self):
        claims = [{"id": "RCL-001"}, {"id": "RCL-002"}]
        text = "| RCL-001 | claim one |\n"
        self.assertEqual(
            readiness.missing_claim_inventory_ids(claims, text),
            ["RCL-002"],
        )


if __name__ == "__main__":
    unittest.main()
