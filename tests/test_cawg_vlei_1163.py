"""Bounded source-contract regression probes for CAWG vLEI issue 1163.

These tests are *not* KERI, COSE, ACDC or X.509 conformance tests.
They verify deterministic decision obligations derived from the pinned
upstream spec and expose unknown rather than converting absence to success.
"""
import unittest

OLD_SHA = '1fbff9683fb692667a81206274d4b24d17078c0b'
NEW_SHA = '464ee8a937f467ec42be4587e425bd56e7350f9f'


def assess_oobi(value, responses):
    """Contract model: nonempty list, try all, accept only validated matching KEL."""
    if not isinstance(value, list) or not value or any(not isinstance(x, str) or not x for x in value):
        return 'invalid-payload'
    if not all(url in responses for url in value):
        return 'indeterminate-test-input'
    invalid_seen = False
    for url in value:
        state = responses[url]
        if state == 'verified-key-state':
            return 'key-state-established'
        if state == 'invalid-kel':
            invalid_seen = True
    return 'invalid-kel' if invalid_seen else 'unavailable-evidence'


def assess_current_role(credential_status, authorization_status):
    """No successful role claim without both status and authorization."""
    if credential_status == 'revoked' or authorization_status == 'invalid':
        return 'invalid'
    if credential_status == 'valid' and authorization_status == 'valid':
        return 'verified-current'
    return 'indeterminate'


def assess_historical_role(current_role, signing_time_status):
    """Current validity/revocation cannot by itself prove signing-time state."""
    if signing_time_status == 'verified-valid':
        return 'historically-supported'
    if signing_time_status == 'verified-invalid':
        return 'historically-invalid'
    return 'indeterminate-historical'


def assess_trust_display(lane, evidence, authority):
    """Display evidence and authority distinctly; do not collapse trust lanes."""
    if lane not in ('vlei', 'x509'):
        return 'unsupported-lane'
    if evidence != 'validated' or authority != 'established':
        return f'{lane}:not-established'
    return f'{lane}:established'


class SourceContractTests(unittest.TestCase):
    def test_new_oobi_wire_shape(self):
        self.assertEqual(assess_oobi('https://witness', {}), 'invalid-payload')
        self.assertEqual(assess_oobi([], {}), 'invalid-payload')
        self.assertEqual(assess_oobi(['https://w1'], {'https://w1': 'verified-key-state'}), 'key-state-established')

    def test_multiple_oobis_and_missing_evidence(self):
        self.assertEqual(assess_oobi(['w1', 'w2'], {'w1': 'unavailable', 'w2': 'verified-key-state'}), 'key-state-established')
        self.assertEqual(assess_oobi(['w1', 'w2'], {'w1': 'unavailable', 'w2': 'unavailable'}), 'unavailable-evidence')
        self.assertEqual(assess_oobi(['w1'], {}), 'indeterminate-test-input')
        self.assertEqual(assess_oobi(['w1'], {'w1': 'invalid-kel'}), 'invalid-kel')

    def test_current_and_historical_role_are_separate(self):
        self.assertEqual(assess_current_role('valid', 'valid'), 'verified-current')
        self.assertEqual(assess_current_role('revoked', 'valid'), 'invalid')
        self.assertEqual(assess_current_role('valid', 'missing'), 'indeterminate')
        self.assertEqual(assess_historical_role('invalid', 'missing'), 'indeterminate-historical')
        self.assertEqual(assess_historical_role('invalid', 'verified-valid'), 'historically-supported')

    def test_trust_lane_and_authority_are_not_collapsed(self):
        self.assertEqual(assess_trust_display('vlei', 'validated', 'established'), 'vlei:established')
        self.assertEqual(assess_trust_display('x509', 'validated', 'established'), 'x509:established')
        self.assertEqual(assess_trust_display('vlei', 'validated', 'unknown'), 'vlei:not-established')
        self.assertEqual(assess_trust_display('x509', 'missing', 'established'), 'x509:not-established')


if __name__ == '__main__':
    unittest.main()
