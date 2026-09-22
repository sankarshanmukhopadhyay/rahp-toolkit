import importlib.util
import unittest
from pathlib import Path

MODULE = Path(__file__).parents[1] / "tools" / "validate_trust_task_error_semantics.py"
spec = importlib.util.spec_from_file_location("trust_task_error_semantics", MODULE)
module = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(module)


class TrustTaskErrorSemanticsTests(unittest.TestCase):
    def test_declared_extended_code_and_retryability_match(self):
        result = module.evaluate(
            {
                "id": "match",
                "type_known": True,
                "declared_error_codes": [
                    {
                        "code": "vtc/join-requests/withdraw:notFound",
                        "retryable": False,
                    }
                ],
                "observed_code": "vtc/join-requests/withdraw:notFound",
                "observed_retryable": False,
            }
        )
        self.assertEqual(module.MATCH, result["semantic_outcome"])

    def test_generic_failure_does_not_preserve_declared_semantics(self):
        result = module.evaluate(
            {
                "id": "collapsed",
                "type_known": True,
                "declared_error_codes": [
                    {
                        "code": "vtc/join-requests/withdraw:alreadyDecided",
                        "retryable": False,
                    }
                ],
                "observed_code": "taskFailed",
                "observed_retryable": False,
            }
        )
        self.assertEqual(module.LOSS, result["semantic_outcome"])

    def test_retryability_is_part_of_the_semantic_contract(self):
        result = module.evaluate(
            {
                "id": "retryability",
                "type_known": True,
                "declared_error_codes": [
                    {
                        "code": "vtc/join-requests/withdraw:notFound",
                        "retryable": False,
                    }
                ],
                "observed_code": "vtc/join-requests/withdraw:notFound",
                "observed_retryable": True,
            }
        )
        self.assertEqual(module.LOSS, result["semantic_outcome"])

    def test_unknown_type_is_distinct_from_known_empty_declaration(self):
        unknown = module.evaluate(
            {
                "id": "unknown",
                "type_known": False,
                "declared_error_codes": [],
            }
        )
        known_empty = module.evaluate(
            {
                "id": "known-empty",
                "type_known": True,
                "declared_error_codes": [],
            }
        )
        self.assertEqual(module.UNKNOWN_SPEC, unknown["semantic_outcome"])
        self.assertEqual(module.NOT_APPLICABLE, known_empty["semantic_outcome"])

    def test_fixture_includes_positive_loss_and_unknown_cases(self):
        results = module.validate()
        joined = "\n".join(results)
        self.assertIn(module.MATCH, joined)
        self.assertIn(module.LOSS, joined)
        self.assertIn(module.UNKNOWN_SPEC, joined)


if __name__ == "__main__":
    unittest.main()
