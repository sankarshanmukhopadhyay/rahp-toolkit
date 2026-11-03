"""Boundary tests for pinned Eucalyptus #965 native retest orchestration."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import eucalyptus_native_evidence as native


class EucalyptusRetest965Tests(unittest.TestCase):
    def test_focus_commands_are_exact_and_do_not_modify_target(self):
        with tempfile.TemporaryDirectory() as d:
            suites = native.diagnostic_suites(Path(d))
        self.assertEqual([s['id'] for s in suites],
                         ['openvtc-vetting-focus', 'registry-didcomm-integration'])
        self.assertEqual(suites[0]['command'],
                         ['cargo', 'test', '--locked', '-p', 'openvtc',
                          'no_ticket_is_issued_for_requests_that_cannot_be_attested'])
        self.assertEqual(suites[1]['command'][:6],
                         ['cargo', 'test', '--locked', '-p', 'trust-registry', '--test'])
        self.assertEqual(suites[1]['command'][-2:], ['--', '--test-threads=1'])

    def test_missing_didcomm_prerequisites_never_execute_or_echo_secrets(self):
        with tempfile.TemporaryDirectory() as d:
            suite = native.diagnostic_suites(Path(d))[1]
            omitted = native.missing_prerequisites(suite, {})
            self.assertEqual(omitted, ['CLIENT_DID', 'CLIENT_SECRETS',
                                       'MEDIATOR_DID', 'TRUST_REGISTRY_DID'])
            root = Path(d)
            result = native.unavailable_prerequisite(suite, root, omitted)
            self.assertEqual(result['state'], 'ATTEMPTED_UNAVAILABLE')
            self.assertIsNone(result['returncode'])
            self.assertEqual((root / result['stdout']['path']).read_text(), '')
            self.assertNotIn('PASS', result['reason'])
            self.assertNotIn('CLIENT_SECRET_VALUE', json.dumps(result))

    def test_invalid_secrets_are_rejected_without_persisting_value(self):
        with tempfile.TemporaryDirectory() as d:
            suite = native.diagnostic_suites(Path(d))[1]
            valid = {'CLIENT_DID': 'did:example:a', 'CLIENT_SECRETS': '[{"id":"secret"}]',
                     'MEDIATOR_DID': 'did:example:m', 'TRUST_REGISTRY_DID': 'did:example:r'}
            self.assertEqual([], native.missing_prerequisites(suite, valid))
            for secret in ('secret-not-json', '[]', '{}'):
                with self.subTest(secret=secret):
                    valid['CLIENT_SECRETS'] = secret
                    missing = native.missing_prerequisites(suite, valid)
                    self.assertEqual(len(missing), 1)
                    self.assertIn('CLIENT_SECRETS', missing[0])
                    self.assertNotIn(secret, str(missing))

    def test_vti_partition_exactly_covers_declared_workspace(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / 'verifiable-trust-infrastructure'
            root.mkdir()
            (root / 'Cargo.toml').write_text(
                '[workspace]\nmembers = ["vtc", "tests/e2e", "vta"]\n')
            for path, name in [('vtc', 'vtc-service'), ('tests/e2e', 'vti-e2e-tests'),
                               ('vta', 'vta-service')]:
                target = root / path / 'Cargo.toml'
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text('[package]\nname = "' + name + '"\nversion="0.1.0"\n')
            suites = native.diagnostic_suites(Path(d), True)
            parts = [s for s in suites if s['id'].startswith('vti-part-')]
            self.assertEqual(len(parts), 3)
            self.assertEqual({x['workspace_member'] for x in parts},
                             {'vtc', 'tests/e2e', 'vta'})
            self.assertEqual({x['command'][-1] for x in parts},
                             {'vtc-service', 'vti-e2e-tests', 'vta-service'})
            self.assertTrue(all('--locked' in x['command'] for x in parts))

    def test_partition_rejects_missing_or_ambiguous_members(self):
        for members in ('["missing"]', '["x", "x"]', '["crate-*"]'):
            with self.subTest(members=members), tempfile.TemporaryDirectory() as d:
                root = Path(d) / 'verifiable-trust-infrastructure'
                root.mkdir()
                (root / 'Cargo.toml').write_text('[workspace]\nmembers = ' + members + '\n')
                with self.assertRaises(ValueError):
                    native.diagnostic_suites(Path(d), True)

    def test_unavailable_result_is_not_counted_as_a_native_pass(self):
        with tempfile.TemporaryDirectory() as d:
            suite = native.diagnostic_suites(Path(d))[1]
            result = native.unavailable_prerequisite(
                suite, Path(d), ['CLIENT_DID'])
            qualified = native.qualify(result, Path(d))
            self.assertEqual(qualified['test_counts']['passed'], 0)
            self.assertEqual(qualified['state'], 'ATTEMPTED_UNAVAILABLE')


if __name__ == '__main__':
    unittest.main()
