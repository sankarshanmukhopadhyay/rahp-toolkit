"""Exercise the actual terminal CLI and keep observation semantics separate."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / 'tools/autonomous_assurance_controller.py'
PIN = {'repository': 'example/implementation', 'revision': 'a' * 40}
OTHER_PIN = {'repository': 'example/spec', 'revision': 'b' * 40}
RID = 'ER-1'


def inputs():
    spec = {'target': dict(PIN), 'subject': {'id': 'bounded-implementation', 'type': 'implementation'},
            'resources': {'spec': dict(OTHER_PIN)},
            'assurance_contract': {'material': True, 'required_evidence': [RID]}}
    ledger = {'schema': 'rahp-evidence-probe-ledger/v1', 'target': dict(PIN), 'complete': True,
              'requirements': [{'requirement_id': RID, 'attempt_state': 'EXECUTED',
                                'result': 'SATISFIED', 'producer': 'test-producer',
                                'producer_revision': 'c' * 40, 'attribution': 'fixture',
                                'evidence_file': 'capture.json'}]}
    assessor = {'schema': 'rahp-assessor-result/v1', 'assessor': 'local-assessor',
                'assessment_id': 'assessor-local-id', 'outcome': 'PASS',
                'reason_code': 'bounded-predicate', 'evidence_used': [RID],
                'residual_risk': 'Other surfaces not examined.', 'action_required': 'Retest on change.',
                'source_pins': [dict(PIN)]}
    return spec, ledger, assessor


class TerminalEvidenceReconciliationTests(unittest.TestCase):
    def cli(self, spec, ledger, assessor):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name, doc in [('spec', spec), ('ledger', ledger), ('assessor', assessor)]:
                (root / (name + '.json')).write_text(json.dumps(doc), encoding='utf-8')
            p = subprocess.run([sys.executable, str(CLI), '--spec', str(root / 'spec.json'),
                                '--ledger', str(root / 'ledger.json'), '--assessor-result', str(root / 'assessor.json'),
                                '--machine-output', str(root / 'result.json'), '--human-output', str(root / 'result.md')],
                               cwd=ROOT, text=True, capture_output=True, timeout=30)
            self.assertEqual(p.returncode, 0, p.stderr)
            result = json.loads((root / 'result.json').read_text())
            self.assertTrue(result['terminal'])
            self.assertIn('**' + result['outcome'] + '**', (root / 'result.md').read_text())
            return result

    def test_valid_local_identifier_and_optional_pin(self):
        spec, ledger, assessor = inputs()
        self.assertEqual('PASS', self.cli(spec, ledger, assessor)['outcome'])
        assessor.pop('source_pins')
        self.assertEqual('PASS', self.cli(spec, ledger, assessor)['outcome'])

    def test_declared_source_context_consistency(self):
        for kind in ('ledger-revision', 'ledger-repository', 'assessor-revision', 'assessor-artifact', 'empty-pins'):
            with self.subTest(kind=kind):
                spec, ledger, assessor = inputs()
                if kind == 'ledger-revision':
                    ledger['target']['revision'] = 'd' * 40
                elif kind == 'ledger-repository':
                    ledger['target']['repository'] = 'example/other'
                elif kind == 'assessor-revision':
                    assessor['source_pins'][0]['revision'] = 'd' * 40
                elif kind == 'assessor-artifact':
                    assessor['source_pins'][0]['artifact'] = 'unconfigured.md'
                else:
                    assessor['source_pins'] = []
                result = self.cli(spec, ledger, assessor)
                self.assertEqual('INDETERMINATE', result['outcome'])
                self.assertEqual('contract-incompatible', result['reason_code'])

    def test_positive_references_must_cover_addressed_observations(self):
        for refs in ([], ['ER-OTHER'], [RID, 'ER-OTHER'], [RID, RID], [None]):
            with self.subTest(refs=refs):
                spec, ledger, assessor = inputs()
                assessor['evidence_used'] = refs
                self.assertEqual('INDETERMINATE', self.cli(spec, ledger, assessor)['outcome'])

    def test_multi_requirement_coverage_and_resource_pin(self):
        spec, ledger, assessor = inputs()
        spec['assurance_contract']['required_evidence'].append('ER-2')
        other = copy.deepcopy(ledger['requirements'][0]); other['requirement_id'] = 'ER-2'
        ledger['requirements'].append(other)
        assessor['source_pins'].append(dict(OTHER_PIN))
        self.assertEqual('INDETERMINATE', self.cli(spec, ledger, assessor)['outcome'])
        assessor['evidence_used'].append('ER-2')
        self.assertEqual('PASS', self.cli(spec, ledger, assessor)['outcome'])

    def test_missing_unknown_and_duplicate_evidence_is_not_success(self):
        for kind in ('missing', 'unknown-result', 'null-result', 'not-executed', 'missing-target', 'duplicate', 'incomplete'):
            with self.subTest(kind=kind):
                spec, ledger, assessor = inputs()
                if kind == 'missing':
                    ledger['requirements'] = []
                elif kind == 'unknown-result':
                    ledger['requirements'][0]['result'] = 'UNRECOGNIZED'
                elif kind == 'null-result':
                    ledger['requirements'][0]['result'] = None
                elif kind == 'not-executed':
                    ledger['requirements'][0]['attempt_state'] = 'ATTEMPTED_UNAVAILABLE'
                elif kind == 'missing-target':
                    del ledger['target']
                elif kind == 'duplicate':
                    ledger['requirements'].append(copy.deepcopy(ledger['requirements'][0]))
                else:
                    ledger['complete'] = False
                self.assertEqual('INDETERMINATE', self.cli(spec, ledger, assessor)['outcome'])

    def test_observation_absence_is_not_universally_failure(self):
        spec, ledger, assessor = inputs()
        ledger['requirements'][0]['result'] = 'ABSENT'
        # A scoped assessor may establish the absence of a prohibited surface.
        self.assertEqual('PASS', self.cli(spec, ledger, assessor)['outcome'])
        # A required positive predicate can instead be judged failed.
        assessor['outcome'] = 'FAIL'
        self.assertEqual('FAIL', self.cli(spec, ledger, assessor)['outcome'])

    def test_historical_lineage_and_not_applicable_fixture_compatibility(self):
        spec, ledger, assessor = inputs()
        spec['assurance_contract'].pop('required_evidence')
        ledger['requirements'] = []
        assessor['evidence_used'] = []
        assessor.pop('source_pins')
        self.assertEqual('PASS', self.cli(spec, ledger, assessor)['outcome'])
        spec['assurance_contract']['specialist_required'] = True
        assessor['outcome'] = 'NOT_APPLICABLE'
        self.assertEqual('NOT_APPLICABLE', self.cli(spec, ledger, assessor)['outcome'])


if __name__ == '__main__':
    unittest.main()
