#!/usr/bin/env python3
"""Collect supplemental native evidence without changing the sealed assessment."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tomllib
from datetime import datetime, timezone

import eucalyptus_campaign as campaign

ROOT = Path(__file__).resolve().parents[1]


def test_counts(command: list[str], text: str) -> dict:
    """Require actual test events; exit zero and skipped tests are insufficient."""
    runtime = command[0]
    passed = failed = skipped = 0
    if runtime == 'cargo':
        for p, f, s in re.findall(r'test result: \w+\. (\d+) passed; (\d+) failed; (\d+) ignored;', text):
            passed += int(p); failed += int(f); skipped += int(s)
    elif runtime == 'go':
        for line in text.splitlines():
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not isinstance(event, dict): continue
            if event.get('Test'):
                passed += event.get('Action') == 'pass'
                failed += event.get('Action') == 'fail'
                skipped += event.get('Action') == 'skip'
            elif event.get('Action') == 'fail':
                failed += 1
    elif runtime == 'dart':
        for line in text.splitlines():
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not isinstance(event, dict): continue
            if event.get('type') == 'testDone' and not event.get('hidden', False):
                skipped += bool(event.get('skipped'))
                passed += event.get('result') == 'success' and not event.get('skipped')
                failed += event.get('result') in ('failure', 'error')
            elif event.get('type') == 'done' and event.get('success') is False and not failed:
                failed += 1
    return {'passed': passed, 'failed': failed, 'skipped': skipped}


def qualify(result: dict, output: Path) -> dict:
    if result['command'][0] in ('cargo', 'go', 'dart') and 'test' in result['command']:
        text = (output / result['stdout']['path']).read_text()
        counts = test_counts(result['command'], text)
        result['test_counts'] = counts
        if result['state'] == 'EXECUTED_PASS' and (not counts['passed'] or counts['failed']):
            result.update(state='ATTEMPTED_UNAVAILABLE', reason='No verified passing native tests, or contradictory test events; exit zero is insufficient.')
    return result


def plan(config: dict) -> list[dict]:
    items = []
    for suite in config['suites']:
        if suite['id'].startswith('rust-') or suite['id'] in ('go-tsp', 'dart-tsp', 'ios-approval', 'lab-room-handoff', 'lab-privacy-handoff'):
            item = {**suite, 'command': list(suite['command'])}
            item['timeout_seconds'] = 900
            if item['id'] == 'go-tsp': item['command'] = ['go', 'test', '-count=1', '-json', './...']
            if item['id'] == 'dart-tsp': item['command'] += ['--reporter=json']
            items.append(item)
            if item['id'] == 'dart-tsp':
                items.append({**item, 'id': 'dart-tsp-package', 'command': ['dart', 'test', '--reporter=json'],
                              'working_directory': 'packages/affinidi_tsp',
                              'purpose': 'Same tagged Dart tests from their package-relative fixture directory; original invocation retained separately.'})
    # Native consuming paths are distinct from whole-workspace component checks.
    consuming = [
        ('vtc-sender', 'vtc-service', ['--test', 'it', 'auth_authcrypt_sender_binding::'], ['EUC-01']),
        ('vtc-self-edit', 'vtc-service', ['--test', 'it', 'acl_self_edit::'], ['EUC-03']),
        ('vtc-consent', 'vtc-service', ['--test', 'it', 'unrestricted_admin_consent::'], ['EUC-04']),
        ('vta-freshness', 'vta-service', ['--test', 'it', 'push_new_attempt_freshness::'], ['EUC-05']),
        ('vta-refresh', 'vta-service', ['--test', 'it', 'refresh_trust_task::'], ['EUC-05']),
        ('rooms-native', None, ['-p', 'vti-rooms', '-p', 'vti-rooms-dtg', '-p', 'room-host'], ['EUC-07', 'EUC-13']),
        ('vetting-native', 'vti-vetting-pcs', [], ['EUC-08']),
        ('e2e-native', 'vti-e2e-tests', [], ['EUC-01', 'EUC-05', 'EUC-06']),
    ]
    for identifier, package, args, propositions in consuming:
        cmd = ['cargo', 'test', '--locked'] + (['-p', package] if package else []) + args
        items.append({'id': identifier, 'source': 'verifiable-trust-infrastructure', 'command': cmd,
                      'timeout_seconds': 900, 'purpose': 'Tagged native consuming-path tests; fixture participants do not establish real-person governance or deployment-wide assurance.',
                      'propositions': propositions})
    return items


def diagnostic_suites(sources: Path, include_partition: bool = False) -> list[dict]:
    """Exact-source retests; no synthetic identities, credentials or upstream changes."""
    suites = [
        {'id': 'openvtc-vetting-focus', 'source': 'openvtc',
         'command': ['cargo', 'test', '--locked', '-p', 'openvtc',
                     'no_ticket_is_issued_for_requests_that_cannot_be_attested'],
         'purpose': 'Reproduce the exact Eucalyptus vetting test without altering target assertions.'},
        {'id': 'registry-didcomm-integration', 'source': 'affinidi-trust-registry-rs',
         'command': ['cargo', 'test', '--locked', '-p', 'trust-registry',
                     '--test', 'didcomm_integration_test', '--', '--test-threads=1'],
         'required_environment': ['CLIENT_DID', 'CLIENT_SECRETS', 'MEDIATOR_DID', 'TRUST_REGISTRY_DID'],
         'purpose': 'Retest the nine previously unexercised DIDComm integration paths only with operator-supplied live prerequisites.'},
    ]
    if include_partition:
        root = sources / 'verifiable-trust-infrastructure'
        manifest = tomllib.loads((root / 'Cargo.toml').read_text(encoding='utf-8'))
        members = manifest['workspace']['members']
        if not members or len(set(members)) != len(members):
            raise ValueError('VTI workspace member list empty or duplicated')
        names = set()
        for member in members:
            if not isinstance(member, str) or any(x in member for x in '*?['):
                raise ValueError('unresolved VTI workspace member')
            crate = campaign.within(root, member) / 'Cargo.toml'
            if not crate.is_file():
                raise ValueError(f'VTI workspace manifest missing: {member}')
            name = tomllib.loads(crate.read_text(encoding='utf-8'))['package']['name']
            if name in names:
                raise ValueError(f'duplicate VTI crate name: {name}')
            names.add(name)
            suites.append({
                'id': 'vti-part-' + name.replace('_', '-'),
                'source': 'verifiable-trust-infrastructure',
                'command': ['cargo', 'test', '--locked', '-p', name],
                'workspace_member': member,
                'purpose': 'One exact Eucalyptus workspace member; cross-member tests and full workspace behavior are not established.',
            })
        if len({s['id'] for s in suites}) != len(suites):
            raise ValueError('duplicate VTI partition identifier')
    return suites


def missing_prerequisites(suite: dict, environment: dict[str, str]) -> list[str]:
    """Return variable names only. Never persist credentials or their values."""
    missing = [key for key in suite.get('required_environment', []) if not environment.get(key)]
    if suite['id'] == 'registry-didcomm-integration' and 'CLIENT_SECRETS' not in missing:
        try:
            secrets = json.loads(environment['CLIENT_SECRETS'])
            if not isinstance(secrets, list) or not secrets:
                missing.append('CLIENT_SECRETS (nonempty JSON array required)')
        except (ValueError, TypeError):
            missing.append('CLIENT_SECRETS (invalid JSON)')
    return missing


def unavailable_prerequisite(suite: dict, output: Path, missing: list[str]) -> dict:
    """Record NOT_EXECUTED as unavailable without implying a target test failure."""
    result = {**suite, 'class': 'runtime-observation', 'state': 'ATTEMPTED_UNAVAILABLE',
              'reason': 'external DIDComm prerequisites unavailable or invalid: ' + ', '.join(missing),
              'returncode': None, 'duration_seconds': 0, 'started_at': datetime.now(timezone.utc).isoformat()}
    for stream in ('stdout', 'stderr'):
        relative = f'logs/{suite["id"]}.{stream}.txt'
        dest = output / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text('', encoding='utf-8')
        result[stream] = {'path': relative, 'sha256': campaign.digest(b'')}
    return result


def collect(sources: Path, output: Path, selected: list[str] | None = None, timeout_seconds: int = 900,
            diagnostics: bool = False, vti_partition: bool = False) -> dict:
    config_path = ROOT / 'profiles/dtg/eucalyptus/campaign.json'
    config = json.loads(config_path.read_text()); campaign.validate(config)
    if not 30 <= timeout_seconds <= 3600: raise ValueError('native timeout must be between 30 and 3600 seconds')
    if vti_partition and not diagnostics:
        raise ValueError('VTI partition requires diagnostics mode')
    suites = plan(config)
    if diagnostics:
        suites += diagnostic_suites(sources, vti_partition)
    if selected:
        unknown = set(selected) - {s['id'] for s in suites}
        if unknown: raise ValueError(f'unknown suite identifiers: {sorted(unknown)}')
        indexed_suites = {s['id']: s for s in suites}
        if len(set(selected)) != len(selected): raise ValueError('duplicate suite selection')
        suites = [indexed_suites[name] for name in selected]
    suites = [{**s, 'timeout_seconds': timeout_seconds} for s in suites]
    if output.exists(): raise ValueError('fresh supplemental output required')
    output.mkdir(parents=True)
    indexed = {s['repository'].split('/')[-1]: s for s in config['sources'] + config['auxiliary_sources']}
    used = {s['source'] for s in suites}
    for name in used: campaign.verify_source(indexed[name], sources / name, require_clean=False)
    versions = {}
    for name in ('cargo', 'rustc', 'go', 'dart', 'swift'):
        if shutil.which(name):
            cp = subprocess.run([name, 'version' if name == 'go' else '--version'], capture_output=True, text=True, timeout=60)
            versions[name] = {'path': shutil.which(name), 'returncode': cp.returncode, 'output': cp.stdout + cp.stderr}
        else: versions[name] = {'available': False}
    campaign.write(output / 'run-contract.json', {'schema': 'rahp-eucalyptus-native-evidence/v1', 'created_at': datetime.now(timezone.utc).isoformat(),
                   'assessor_revision': campaign.git(ROOT, 'rev-parse', 'HEAD'), 'assessor_sha256': campaign.digest(Path(__file__).read_bytes()),
                   'baseline_contract_sha256': campaign.digest(config_path.read_bytes()), 'sources': [indexed[n] for n in sorted(used)],
                   'suites': suites, 'versions': versions, 'selection': selected,
                   'executor_sha256': campaign.digest((ROOT / 'tools/eucalyptus_campaign.py').read_bytes()),
                   'build_environment': {key: os.environ[key] for key in ('RUSTUP_TOOLCHAIN', 'CARGO_BUILD_JOBS', 'CARGO_INCREMENTAL', 'CARGO_PROFILE_DEV_DEBUG', 'CARGO_PROFILE_DEV_CODEGEN_UNITS', 'CARGO_PROFILE_DEV_BUILD_OVERRIDE_CODEGEN_UNITS', 'CARGO_TARGET_DIR', 'PKG_CONFIG_PATH', 'LD_LIBRARY_PATH') if key in os.environ},
                   'boundary': 'Supplemental component/native-fixture evidence. No consequential proposition is automatically closed.'})
    (output / 'assessor-implementation.py').write_bytes(Path(__file__).read_bytes())
    results = []
    for suite in suites:
        print('Executing ' + suite['id'], flush=True)
        root = sources / suite['source']
        cwd = campaign.within(root, suite['working_directory']) if suite.get('working_directory') else root
        lock = root / 'Cargo.lock'
        item = dict(suite)
        # A library can omit a release lock. Resolve explicitly and preserve the
        # actual generated input rather than claiming a release-locked build.
        release_lock = campaign.git(root, 'ls-files', '--', 'Cargo.lock') == 'Cargo.lock'
        if item['command'][0] == 'cargo' and not release_lock:
            item['command'] = [x for x in item['command'] if x != '--locked']
        absent = missing_prerequisites(item, os.environ)
        if absent:
            result = unavailable_prerequisite(item, output, absent)
        else:
            result = qualify(campaign.execute_suite(item, cwd, output), output)
        result.update(repository=indexed[suite['source']]['repository'], revision=indexed[suite['source']]['revision'])
        lock_name = {'cargo': 'Cargo.lock', 'go': 'go.sum', 'dart': 'pubspec.lock'}.get(item['command'][0])
        tracked_lock = bool(lock_name and campaign.git(root, 'ls-files', '--', lock_name) == lock_name)
        result['build_inputs'] = {'release_lock_available': tracked_lock,
                                  'state': 'release-locked' if tracked_lock else 'fresh-resolution-not-release-locked'}
        for filename in ('Cargo.lock', 'pubspec.lock', 'go.mod', 'go.sum'):
            path = root / filename
            if path.exists():
                dest = output / 'build-inputs' / suite['id'] / suite['source'] / filename
                dest.parent.mkdir(parents=True, exist_ok=True); dest.write_bytes(path.read_bytes())
                result['build_inputs'][filename] = {'path': str(dest.relative_to(output)), 'sha256': campaign.digest(path.read_bytes())}
        campaign.verify_source(indexed[suite['source']], root, require_clean=False)
        results.append(result); campaign.write(output / 'attempts.json', results)
    summary = {'schema': 'rahp-eucalyptus-native-summary/v1', 'process_state': 'complete', 'assurance_state': 'INDETERMINATE',
               'attempts': {state: sum(r['state'] == state for r in results) for state in ('EXECUTED_PASS', 'EXECUTED_NONZERO', 'ATTEMPTED_UNAVAILABLE')},
               'native_test_counts': {key: sum(r.get('test_counts', {}).get(key, 0) for r in results) for key in ('passed', 'failed', 'skipped')},
               'composition_pass': 0, 'closed_propositions': [],
               'residual': 'Actual deployment, observer captures, real participant independence, Apple device and accessibility/redress evidence remain required. Native fixture passes are bounded.'}
    campaign.write(output / 'summary.json', summary)
    lines = ['# Supplemental Eucalyptus native evidence', '', '**Overall assurance remains INDETERMINATE.**', '',
             'The sealed initial campaign is retained. This packet records additional native attempts and actual resolved build inputs.', '',
             '| Attempt | State | Passing native tests | Build input state |', '|---|---|---:|---|']
    lines += [f"| {r['id']} | {r['state']} | {r.get('test_counts', {}).get('passed', 0)} | {r['build_inputs']['state']} |" for r in results]
    lines += ['', summary['residual'], '', 'Counts are test events, not distinct assurance claims; suites may overlap. Full commands, versions, revisions and logs are in the sealed machine records.']
    (output / 'report.md').write_text('\n'.join(lines) + '\n')
    campaign.seal(output); campaign.verify_package(output)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sources', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--suite', action='append')
    parser.add_argument('--timeout-seconds', type=int, default=900)
    parser.add_argument('--diagnostics-965', action='store_true',
                        help='Enable bounded source-pinned Eucalyptus #965 diagnostics')
    parser.add_argument('--vti-partition', action='store_true',
                        help='Expand diagnostic suites to all exact VTI workspace members (costly)')
    args = parser.parse_args()
    output_existed = args.output.exists()
    try:
        suites = args.suite
        if args.diagnostics_965 and suites is None:
            suites = ['openvtc-vetting-focus', 'registry-didcomm-integration']
        summary = collect(args.sources.resolve(), args.output.resolve(), suites, args.timeout_seconds,
                          diagnostics=args.diagnostics_965, vti_partition=args.vti_partition)
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        if not output_existed and args.output.exists():
            campaign.write(args.output / 'execution-failure.json', {'process_state': 'failed', 'error': str(exc), 'type': type(exc).__name__})
        print(f'Native evidence collection failed: {exc}', file=sys.stderr)
        return 1
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

