"""Falsify pinning, evidence-integrity and inference claims using real git/subprocesses."""
import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import eucalyptus_campaign as campaign

CONFIG = json.loads((ROOT / 'profiles/dtg/eucalyptus/campaign.json').read_text())


class CampaignTests(unittest.TestCase):
    def test_manifest_valid_and_complete(self):
        campaign.validate(CONFIG)
        self.assertEqual(18, len(CONFIG['sources']))
        self.assertEqual(20, len(CONFIG['propositions']))
        covered = {r['source'] for p in CONFIG['propositions'] for r in p['source_refs']}
        self.assertEqual({s['repository'].split('/')[-1] for s in CONFIG['sources']}, covered)

    def test_moving_pin_rejected(self):
        c = copy.deepcopy(CONFIG); c['sources'][0]['revision'] = 'main'
        with self.assertRaises(ValueError): campaign.validate(c)

    def test_missing_pressure_coverage_rejected(self):
        c = copy.deepcopy(CONFIG); c['propositions'][0]['harm'] = ''
        with self.assertRaises(ValueError): campaign.validate(c)

    def test_duplicate_source_rejected(self):
        c = copy.deepcopy(CONFIG); c['sources'][0] = c['sources'][1]
        with self.assertRaises(ValueError): campaign.validate(c)

    def test_duplicate_proposition_rejected(self):
        c = copy.deepcopy(CONFIG); c['propositions'].append(c['propositions'][0])
        with self.assertRaises(ValueError): campaign.validate(c)

    def test_source_reference_traversal_rejected(self):
        c = copy.deepcopy(CONFIG); c['propositions'][0]['source_refs'][0]['path'] = '../secret'
        with self.assertRaises(ValueError): campaign.validate(c)

    def test_workspace_path_traversal_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError): campaign.within(Path(d), '../outside')

    def test_component_success_never_discharges_composition(self):
        p = copy.deepcopy(CONFIG['propositions'][0]); p['suite_ids'] = ['test']
        result = campaign.infer(p, [{'observation': 'source says it is safe'}], [{'id': 'test', 'state': 'EXECUTED_PASS', 'passed': 10000}])
        self.assertEqual('INDETERMINATE', result['outcome'])
        self.assertEqual('NO_APPLICABLE_PRODUCER', result['attempt_state'])

    def test_nonzero_is_not_automatically_a_security_defect(self):
        result = campaign.infer(CONFIG['propositions'][0], [], [{'id': 'test', 'state': 'EXECUTED_NONZERO'}])
        self.assertEqual('INDETERMINATE', result['outcome'])

    def test_integrity_detects_changed_deleted_and_extra_evidence(self):
        for mutation in ('change', 'delete', 'extra'):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as d:
                out = Path(d); evidence = out / 'evidence.json'; evidence.write_text('{}')
                campaign.seal(out); campaign.verify_package(out)
                if mutation == 'change': evidence.write_text('{"pass": true}')
                if mutation == 'delete': evidence.unlink()
                if mutation == 'extra': (out / 'injected').write_text('fake')
                with self.assertRaises(ValueError): campaign.verify_package(out)

    def execute(self, command):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); out = root / 'output'; out.mkdir()
            return campaign.execute_suite({'id': 'test', 'source': 'fixture', 'command': command, 'purpose': 'test', 'timeout_seconds': 1}, root, out)

    def test_actual_failure_and_missing_runtime_distinguished(self):
        failed = self.execute([sys.executable, '-c', 'raise AssertionError("counterexample")'])
        missing = self.execute(['rahp-nonexistent-runtime'])
        self.assertEqual('EXECUTED_NONZERO', failed['state'])
        self.assertEqual('ATTEMPTED_UNAVAILABLE', missing['state'])

    def test_timeout_is_bounded_unavailable(self):
        result = self.execute([sys.executable, '-c', 'import time; time.sleep(10)'])
        self.assertEqual('ATTEMPTED_UNAVAILABLE', result['state'])
        self.assertIn('timeout', result['reason'])

    def test_unavailable_compiler_not_defect(self):
        result = self.execute(['bash', '-c', 'echo "sh: 1: tsc: not found" >&2; exit 127'])
        self.assertEqual('ATTEMPTED_UNAVAILABLE', result['state'])

    def test_zero_node_tests_cannot_pass(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); (root / 'output').mkdir(); (root / 'empty.js').write_text('')
            # An empty test file is reported by Node as one file test; require actual assertions
            # by asserting a completely empty programmatic TAP suite is not credited.
            with patch('eucalyptus_campaign.subprocess.Popen') as popen:
                popen.return_value.communicate.return_value = ('# tests 0\n# pass 0\n', '')
                popen.return_value.returncode = 0
                result = campaign.execute_suite({'id': 'zero', 'command': ['node', '--test'], 'purpose': 'test'}, root, root / 'output')
            self.assertEqual('ATTEMPTED_UNAVAILABLE', result['state'])

    def git_fixture(self, path):
        path.mkdir(parents=True)
        env = {**os.environ, 'GIT_AUTHOR_DATE': '2026-10-07T00:00:00Z', 'GIT_COMMITTER_DATE': '2026-10-07T00:00:00Z'}
        def git(*args): return subprocess.check_output(['git', '-C', str(path), *args], text=True, env=env, stderr=subprocess.DEVNULL).strip()
        git('init', '-q'); git('config', 'user.name', 'RAHP Test'); git('config', 'user.email', 'test@example.invalid')
        (path / 'README.md').write_text('Fixture only. Not target evidence.\n')
        git('add', '.'); git('commit', '-qm', 'fixture'); git('tag', '-am', 'fixture tag', 'VTI-Eucalyptus')
        return git('rev-parse', 'HEAD'), git('rev-parse', 'VTI-Eucalyptus')

    def test_source_dirty_and_mismatch_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / 'repo'; sha, tag = self.git_fixture(root)
            source = {'repository': 'test/repo', 'revision': sha, 'tag_object': tag, 'release': 'VTI-Eucalyptus', 'path': 'sources/repo'}
            campaign.verify_source(source, root)
            bad_tag = {**source, 'tag_object': 'b' * 40}
            with self.assertRaises(ValueError): campaign.verify_source(bad_tag, root)
            bad = {**source, 'revision': 'a' * 40}
            with self.assertRaises(ValueError): campaign.verify_source(bad, root)
            (root / 'README.md').write_text('changed')
            with self.assertRaises(ValueError): campaign.verify_source(source, root)

    def test_real_end_to_end_replay_and_stale_output_rejection(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); identities = []; assessment_ids = []
            for run in (1, 2):
                workspace = root / str(run); workspace.mkdir()
                c = copy.deepcopy(CONFIG)
                c['auxiliary_sources'] = []
                for source in c['sources']:
                    sha, tag = self.git_fixture(workspace / source['path'])
                    source.update(revision=sha, tag_object=tag)
                c['suites'] = [{'id': 'real-subprocess', 'source': c['sources'][0]['repository'].split('/')[-1], 'command': [sys.executable, '-c', 'print("fixture executed")'], 'purpose': 'Synthetic harness verification only.'}]
                for prop in c['propositions']:
                    prop['source_refs'] = [{'source': c['sources'][0]['repository'].split('/')[-1], 'path': 'README.md'}]
                config = root / f'config-{run}.json'; config.write_text(json.dumps(c))
                summary = campaign.campaign(config, workspace, True)
                campaign.verify_package(workspace / 'output')
                record = json.loads((workspace / 'output/assurance-terminal-machine.json').read_text())
                self.assertEqual('INDETERMINATE', record['outcome'])
                self.assertEqual('complete', record['process_state'])
                self.assertEqual('indeterminate', record['assurance_state'])
                self.assertEqual('source-only', record['evidence_maturity'])
                self.assertEqual({'rahp', 'security', 'composition', 'drarm', 'specialist'}, set(record['lenses']))
                self.assertTrue(record['terminal']); self.assertEqual(18, len(record['source_pins']))
                self.assertEqual(20, len(record['harm_traceability']))
                identities.append(summary['campaign_identity']); assessment_ids.append(record['assessment_id'])
                with self.assertRaises(ValueError): campaign.campaign(config, workspace, True)
            self.assertEqual(identities[0], identities[1]); self.assertEqual(assessment_ids[0], assessment_ids[1])


if __name__ == '__main__': unittest.main()
