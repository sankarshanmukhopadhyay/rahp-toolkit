"""Reject success without test execution and preserve native evidence boundaries."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import eucalyptus_native_evidence as native


class NativeEvidenceTests(unittest.TestCase):
    def test_cargo_aggregates_suites_without_crediting_ignored(self):
        text = 'test result: ok. 2 passed; 0 failed; 3 ignored;\ntest result: ok. 4 passed; 0 failed; 0 ignored;'
        self.assertEqual({'passed': 6, 'failed': 0, 'skipped': 3}, native.test_counts(['cargo', 'test'], text))

    def test_go_package_success_is_not_test_success(self):
        text = '\n'.join(json.dumps(x) for x in [
            {'Action': 'pass', 'Package': 'example'},
            {'Action': 'pass', 'Package': 'example', 'Test': 'TestAuthority'},
            {'Action': 'skip', 'Test': 'TestDevice'}])
        self.assertEqual({'passed': 1, 'failed': 0, 'skipped': 1}, native.test_counts(['go', 'test'], text))

    def test_dart_skips_and_hidden_load_events_are_not_passes(self):
        text = '\n'.join(json.dumps(x) for x in [
            {'type': 'testDone', 'hidden': True, 'result': 'success'},
            {'type': 'testDone', 'skipped': True, 'result': 'success'},
            {'type': 'testDone', 'result': 'success'},
            {'type': 'testDone', 'result': 'error'}])
        self.assertEqual({'passed': 1, 'failed': 1, 'skipped': 1}, native.test_counts(['dart', 'test'], text))

    def test_malformed_events_do_not_create_evidence(self):
        self.assertEqual(0, native.test_counts(['go', 'test'], 'PASS\n{"Action":')['passed'])
        self.assertEqual(0, native.test_counts(['dart', 'test'], '[]\nnull')['passed'])

    def test_outer_failures_are_preserved_without_test_identifier(self):
        self.assertEqual(1, native.test_counts(['go', 'test'], '{"Action":"fail","Package":"example"}')['failed'])
        self.assertEqual(1, native.test_counts(['dart', 'test'], '{"type":"done","success":false}')['failed'])

    def test_zero_and_contradictory_events_reject_exit_zero(self):
        for text in ('test result: ok. 0 passed; 0 failed; 2 ignored;',
                     'test result: FAILED. 2 passed; 1 failed; 0 ignored;'):
            with self.subTest(text=text), tempfile.TemporaryDirectory() as d:
                root = Path(d); (root / 'stdout').write_text(text)
                result = native.qualify({'state': 'EXECUTED_PASS', 'command': ['cargo', 'test'], 'stdout': {'path': 'stdout'}}, root)
                self.assertEqual('ATTEMPTED_UNAVAILABLE', result['state'])

    def test_plan_uses_tagged_consuming_paths_and_uncached_go_tests(self):
        config = json.loads((ROOT / 'profiles/dtg/eucalyptus/campaign.json').read_text())
        original = copy.deepcopy(config)
        plan = {s['id']: s for s in native.plan(config)}
        self.assertIn('-count=1', plan['go-tsp']['command'])
        self.assertIn('--locked', plan['vtc-consent']['command'])
        self.assertEqual(['EUC-04'], plan['vtc-consent']['propositions'])
        self.assertEqual(config, original)

    def test_unknown_selection_rejected_without_output(self):
        with tempfile.TemporaryDirectory() as d:
            output = Path(d) / 'output'
            with self.assertRaisesRegex(ValueError, 'unknown suite'):
                native.collect(Path(d), output, ['invented-pass'])
            self.assertFalse(output.exists())

    def test_unbounded_timeout_and_duplicate_selection_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            output = Path(d) / 'output'
            for timeout in (0, 3601):
                with self.assertRaisesRegex(ValueError, 'timeout'):
                    native.collect(Path(d), output, timeout_seconds=timeout)
            with self.assertRaisesRegex(ValueError, 'duplicate'):
                native.collect(Path(d), output, ['go-tsp', 'go-tsp'])
            self.assertFalse(output.exists())


if __name__ == '__main__': unittest.main()
