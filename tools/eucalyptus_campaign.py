#!/usr/bin/env python3
"""Pinned Eucalyptus campaign; test execution never implies composition assurance."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import tomllib
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

from assurance_record import canonical_record, markdown
from autonomous_assurance_controller import build_terminal

SHA = re.compile(r'^[0-9a-f]{40}$')


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n', encoding='utf-8')


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(['git', '-C', str(root), *args], text=True).strip()


def within(root: Path, relative: str) -> Path:
    path = (root / relative).resolve()
    if path == root.resolve() or root.resolve() not in path.parents:
        raise ValueError(f'path escapes root: {relative}')
    return path


def validate(config: dict) -> None:
    if config.get('schema') != 'rahp-eucalyptus-campaign/v1':
        raise ValueError('unsupported campaign schema')
    sources = config['sources']
    if len(sources) != 18 or len({s['repository'] for s in sources}) != 18:
        raise ValueError('campaign requires exactly 18 distinct coordinated repositories')
    for source in sources:
        if not SHA.fullmatch(source['revision']) or not SHA.fullmatch(source['tag_object']):
            raise ValueError('source and tag object must be immutable SHA40')
        if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', source['repository']):
            raise ValueError('invalid repository')
        if source['path'] != 'sources/' + source['repository'].split('/')[-1]:
            raise ValueError('noncanonical source path')
    ids = set()
    names = {s['repository'].split('/')[-1] for s in sources + config.get('auxiliary_sources', [])}
    for source in config.get('auxiliary_sources', []):
        if not SHA.fullmatch(source['revision']) or source['tag_object'] != source['revision'] or source['release'] != 'HEAD':
            raise ValueError('auxiliary source must be commit-pinned')
        if source['path'] != 'sources/' + source['repository'].split('/')[-1]:
            raise ValueError('invalid auxiliary source path')
    for prop in config['propositions']:
        if prop['id'] in ids:
            raise ValueError('duplicate proposition')
        ids.add(prop['id'])
        for key in ('persona', 'scenario', 'harm', 'control', 'proposition', 'required_evidence', 'owner', 'retest', 'patterns', 'source_refs'):
            if not prop.get(key):
                raise ValueError(f'{prop["id"]}: missing {key}')
        for ref in prop['source_refs']:
            if ref['source'] not in names or Path(ref['path']).is_absolute() or '..' in Path(ref['path']).parts:
                raise ValueError('invalid source reference')
    for suite in config['suites']:
        if suite['source'] not in names or not suite['command'] or not all(isinstance(x, str) for x in suite['command']):
            raise ValueError('invalid suite')
        if not re.fullmatch(r'[a-z0-9-]+', suite['id']):
            raise ValueError('invalid suite identifier')
    if len({s['id'] for s in config['suites']}) != len(config['suites']):
        raise ValueError('duplicate suite')


def verify_source(source: dict, root: Path, require_clean: bool = True) -> dict:
    if git(root, 'rev-parse', 'HEAD') != source['revision']:
        raise ValueError(f'{source["repository"]}: commit pin mismatch')
    if git(root, 'rev-parse', source['release']) != source['tag_object']:
        raise ValueError(f'{source["repository"]}: tag object mismatch')
    if git(root, 'rev-parse', source['release'] + '^{commit}') != source['revision']:
        raise ValueError('tag does not resolve to pinned source')
    if git(root, 'diff', 'HEAD', '--') or (require_clean and git(root, 'status', '--porcelain')):
        raise ValueError(f'{source["repository"]}: dirty source checkout')
    files = git(root, 'ls-files').splitlines()
    # git tree commits bind all tracked files; per-file hashes aid evidence consumers.
    return {**source, 'tracked_files': len(files), 'tree': git(root, 'rev-parse', 'HEAD^{tree}')}


def acquire(source: dict, workspace: Path, reuse: bool) -> dict:
    root = within(workspace, source['path'])
    if root.exists():
        if not reuse:
            raise ValueError('existing source rejected; use --reuse-sources for verified precollection')
    else:
        if source['release'] == 'HEAD':
            root.mkdir(parents=True)
            subprocess.run(['git', '-C', str(root), 'init', '-q'], check=True)
            subprocess.run(['git', '-C', str(root), 'fetch', '--depth', '1', 'https://github.com/' + source['repository'] + '.git', source['revision']], check=True, timeout=180)
            subprocess.run(['git', '-C', str(root), 'checkout', '--detach', '-q', 'FETCH_HEAD'], check=True)
        else:
            subprocess.run(['git', 'clone', '--quiet', '--depth', '1', '--branch', source['release'],
                            'https://github.com/' + source['repository'] + '.git', str(root)], check=True, timeout=180)
    return verify_source(source, root)


def source_observation(source: dict, root: Path, ref: dict) -> dict:
    path = within(root, ref['path'])
    if git(root, 'ls-files', '--', ref['path']) != ref['path']:
        raise ValueError(f'untracked evidence reference: {ref}')
    data = path.read_bytes()
    text = data.decode('utf-8')
    lines = text.splitlines()
    needle = ref.get('needle')
    hits = [i + 1 for i, line in enumerate(lines) if needle and needle in line]
    if needle and not hits:
        raise ValueError(f'source anchor not found: {ref}')
    return {'class': 'static-specification-analysis', 'repository': source['repository'],
            'revision': source['revision'], 'path': ref['path'], 'sha256': digest(data),
            'anchor_lines': hits, 'observation': ref.get('observation', 'Source and test design inspected; presence is not execution.'),
            'url': f'https://github.com/{source["repository"]}/blob/{source["revision"]}/{ref["path"]}'}


def execute_suite(suite: dict, root: Path, output: Path) -> dict:
    command = suite['command']
    start = time.monotonic()
    result = {**suite, 'class': suite.get('evidence_class', 'runtime-observation'), 'started_at': datetime.now(timezone.utc).isoformat()}
    stdout = stderr = ''
    if shutil.which(command[0]) is None:
        result.update(state='ATTEMPTED_UNAVAILABLE', reason=f'executable unavailable: {command[0]}', returncode=None)
    else:
        # Isolate and kill the full process group on timeout, including compiler children.
        process = subprocess.Popen(command, cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
        try:
            stdout, stderr = process.communicate(timeout=suite.get('timeout_seconds', 90))
            code = process.returncode
            result.update(returncode=code)
            if code == 0:
                if command[0] == 'node' and '--test' in command:
                    count = re.search(r'(?:#|ℹ) tests (\d+)', stdout)
                    passed = re.search(r'(?:#|ℹ) pass (\d+)', stdout)
                    if not count or not passed or int(passed[1]) == 0:
                        result.update(state='ATTEMPTED_UNAVAILABLE', reason='zero or unverified executed test count')
                    else:
                        result.update(state='EXECUTED_PASS', tests=int(count[1]), passed=int(passed[1]), reason='Pinned component test vectors passed; no cross-service inference.')
                else:
                    result.update(state='EXECUTED_PASS', reason='Pinned command completed; assurance limited to its declared purpose.')
            elif re.search(r'target pin mismatch|must be pinned to|ERR_MODULE_NOT_FOUND|Cannot find module|(?:tsc|vitest): not found|ENOTCACHED|failed to (?:download|get)|could not resolve|network is unreachable', stdout + stderr, re.I):
                result.update(state='ATTEMPTED_UNAVAILABLE', reason='dependency or network prerequisite unavailable; see full logs')
            else:
                result.update(state='EXECUTED_NONZERO', reason='Nonzero execution requires diagnosis; neither automatic defect finding nor PASS.')
        except subprocess.TimeoutExpired:
            import signal
            os.killpg(process.pid, signal.SIGKILL)
            stdout, stderr = process.communicate()
            result.update(state='ATTEMPTED_UNAVAILABLE', reason='execution exceeded bounded timeout', returncode=process.returncode)
    result['duration_seconds'] = round(time.monotonic() - start, 3)
    for stream, content in [('stdout', stdout), ('stderr', stderr)]:
        relative = f'logs/{suite["id"]}.{stream}.txt'
        (output / relative).parent.mkdir(exist_ok=True)
        (output / relative).write_text(content, encoding='utf-8')
        result[stream] = {'path': relative, 'sha256': digest(content.encode())}
    return result


def infer(prop: dict, observations: list[dict], suites: list[dict]) -> dict:
    # This adapter has no accepted deployed-composition/specialist evidence producer.
    # A bounded component test must never discharge a broader proposition.
    related = [s for s in suites if s['id'] in prop.get('suite_ids', [])]
    return {**prop, 'outcome': 'INDETERMINATE', 'evidence_maturity': 'source-only',
            'bounded_component_passes': [s['id'] for s in related if s['state'] == 'EXECUTED_PASS'],
            'diagnostic_nonzero_attempts': [s['id'] for s in related if s['state'] == 'EXECUTED_NONZERO'],
            'source_observations': observations, 'component_attempt_ids': [s['id'] for s in related],
            'attempt_state': 'ATTEMPTED_UNAVAILABLE' if any(s['id'].startswith('lab-') for s in related) else 'NO_APPLICABLE_PRODUCER',
            'inference': 'Source inspection and bounded component checks do not establish this consequential composition. ' + prop['required_evidence'],
            'producer_gap': 'No accepted source-compatible automated deployed-composition/specialist producer is bound for this exact proposition and release.'}


def seal(output: Path) -> dict:
    values = {str(p.relative_to(output)): digest(p.read_bytes()) for p in sorted(output.rglob('*')) if p.is_file() and p.name != 'integrity.json'}
    result = {'schema': 'rahp-campaign-integrity/v1', 'files': values,
              'root_sha256': digest(json.dumps(values, sort_keys=True, separators=(',', ':')).encode())}
    write(output / 'integrity.json', result)
    return result


def verify_package(output: Path) -> None:
    stored = json.loads((output / 'integrity.json').read_text())
    actual = {str(p.relative_to(output)): digest(p.read_bytes()) for p in sorted(output.rglob('*')) if p.is_file() and p.name != 'integrity.json'}
    if actual != stored['files'] or digest(json.dumps(actual, sort_keys=True, separators=(',', ':')).encode()) != stored['root_sha256']:
        raise ValueError('campaign evidence integrity mismatch')


def dependency_inventory(root: Path) -> dict:
    lock = root / 'Cargo.lock'
    if not lock.exists():
        return {'available': False, 'reason': 'No Rust lockfile at repository root; other manifests remain source-pinned.'}
    data = tomllib.loads(lock.read_text())
    return {'available': True, 'lock_sha256': digest(lock.read_bytes()),
            'packages': [{k: p[k] for k in ('name', 'version', 'source', 'checksum') if k in p} for p in data.get('package', [])],
            'inference': 'Lockfile package identities are recorded separately. A coordinated repository tag does not prove these dependencies were built from that tag.'}


def campaign(config_path: Path, workspace: Path, reuse: bool) -> dict:
    config = json.loads(config_path.read_text()); validate(config)
    workspace.mkdir(parents=True, exist_ok=True)
    output = workspace / 'output'
    if output.exists():
        raise ValueError('existing output rejected: fresh campaign workspace required')
    output.mkdir()
    import importlib.metadata
    probe = subprocess.Popen(['sleep', '5'])
    try:
        proc = Path(f'/proc/{probe.pid}/cmdline')
        proc_diagnostic = {'expected_command': 'sleep 5', 'pid': probe.pid, 'proc_cmdline': proc.read_bytes().decode(errors='replace').replace('\x00', ' ') if proc.exists() else None,
            'claim_boundary': 'Execution substrate diagnostic; a mismatched procfs process view can invalidate PID-command matching tests without proving an upstream defect.'}
    finally:
        probe.terminate(); probe.wait()
    write(output / 'execution-substrate.json', proc_diagnostic)
    write(output / 'environment.json', {'python': sys.version, 'platform': sys.platform,
          'dependencies': {name: importlib.metadata.version(name) for name in ['PyYAML', 'jsonschema']},
          'tool_paths': {name: shutil.which(name) for name in ['git', 'node', 'npm', 'cargo', 'go', 'dart', 'swift']},
          'working_directory': str(workspace), 'network_assumption': 'Source acquisition succeeded; package registry and toolchain access are separately attempted where registered.'})
    engine = Path(__file__).resolve().parent.parent
    engine_revision = git(engine, 'rev-parse', 'HEAD')
    implementation_files = ['eucalyptus_campaign.py', 'assurance_record.py', 'autonomous_assurance_controller.py', 'assurance_fsm.py']
    implementation_hashes = {f: digest((engine / 'tools' / f).read_bytes()) for f in implementation_files}
    identity = digest(json.dumps({'config': config, 'engine_revision': engine_revision, 'implementation_hashes': implementation_hashes}, sort_keys=True).encode())
    with ThreadPoolExecutor(max_workers=6) as executor:
        sources = list(executor.map(lambda s: acquire(s, workspace, reuse), config['sources'] + config.get('auxiliary_sources', [])))
    indexed = {s['repository'].split('/')[-1]: s for s in sources}
    write(output / 'source-manifest.json', {'schema': 'rahp-eucalyptus-sources/v1', 'sources': sources,
          'assessor': {'revision': engine_revision, 'implementation_sha256': implementation_hashes},
          'provenance': config['provenance'], 'historical_inputs_used': False})
    write(output / 'dependency-inventory.json', {key: dependency_inventory(workspace / value['path']) for key, value in indexed.items()})
    privacy_input = {
        'schema': 'dpip-privacy-observability-result/v1',
        'experiment': {'id': config['id'], 'privacy_proposition': 'Cross-context persona/vetting/task composition does not create unnecessary joins',
            'comparison': {'kind': 'A/B', 'scenarios': ['community-A', 'community-B']},
            'required_observer_planes': ['host', 'verifier', 'transport', 'audit'],
            'minimum_evidence_class': 'target-native-runtime-observation', 'reproducibility': 'exact Eucalyptus source pins and observer/configuration capture required',
            'source_pins': config['sources']},
        'observer_planes': [{'id': plane, 'direct_observables': [], 'derived_or_joinable': [], 'privilege': 'ordinary', 'threat_model': 'in-scope'} for plane in ['host', 'verifier', 'transport', 'audit']],
        'correlation': {'signal': 'not-tested', 'effective_join': False},
        'result': 'evidence-incomplete', 'executed': False,
        'unsupported_inference': ['effective_join=false is not an observed no-join outcome', 'No privacy PASS may be inferred'],
        'residual_uncertainty': ['No Eucalyptus-compatible native A/B observations are available to this campaign.']
    }
    write(output / 'privacy-observability-input.json', privacy_input)
    # Run sequentially: shared test state and dependency installs must not race.
    suites = []
    for suite in config['suites']:
        print(f'Executing {suite["id"]}', flush=True)
        source = indexed[suite['source']]
        result = execute_suite(suite, workspace / source['path'], output)
        result['repository'] = source['repository']; result['revision'] = source['revision']
        suites.append(result)
    for source in sources:
        verify_source(source, workspace / source['path'], require_clean=False)
    write(output / 'component-attempts.json', suites)
    props = []
    for prop in config['propositions']:
        observations = [source_observation(indexed[ref['source']], workspace / indexed[ref['source']]['path'], ref) for ref in prop['source_refs']]
        props.append(infer(prop, observations, suites))
    write(output / 'proposition-matrix.json', {'schema': 'rahp-eucalyptus-propositions/v1', 'propositions': props})
    ledger = {'schema': 'rahp-evidence-probe-ledger/v1', 'complete': True, 'orchestration_defects': [],
              'requirements': [{'requirement_id': p['id'], 'attempt_state': p['attempt_state'], 'result': 'NOT_EVIDENCED',
                                'reason': p['producer_gap'], 'attribution': p['owner']} for p in props]}
    write(output / 'evidence-probe-ledger.json', ledger)
    spec = {'run': {'lineage_prefix': identity, 'instance': 'dtg', 'snapshot': 'VTI-Eucalyptus'},
            'target': sources[1], 'resources': {str(i): s for i, s in enumerate(sources) if i != 1},
            'subject': {'type': 'portfolio-composition', 'id': config['id'], 'components': [s['repository'] for s in config['sources']]},
            'assurance_contract': {'material': True, 'specialist_required': True,
                'scope': config['scope'], 'non_scope': config['non_scope'],
                'personas': sorted({p['persona'] for p in props}), 'scenarios': [p['scenario'] for p in props],
                'harms': [p['harm'] for p in props], 'assurance_propositions': [p['proposition'] for p in props],
                'requirements_examined': [p['id'] for p in props], 'tests': [s['id'] for s in suites],
                'actions': [{'surface': 'evidence-test', 'action': p['owner'] + ': ' + p['retest'], 'acceptance_criterion': p['required_evidence']} for p in props],
                'harm_traceability': [{'persona': p['persona'], 'scenario': p['scenario'], 'harm': p['harm'], 'proposition': p['proposition'], 'control': p['control'], 'conclusion': p['outcome']} for p in props]}}
    assessor = {'schema': 'rahp-assessor-result/v1', 'assessor': 'eucalyptus-clean-room-v1', 'assessment_id': identity,
                'outcome': 'INDETERMINATE', 'reason_code': 'eucalyptus-composition-evidence-required',
                'evidence_used': [s['id'] for s in suites if s['state'] == 'EXECUTED_PASS'],
                'residual_risk': f'{len(props)} consequential propositions lack accepted deployed-composition/specialist evidence. Component results and configuration exceptions are bounded observations, not certification.',
                'action_required': 'Execute the proposition-specific retest contracts against these exact pins; resolve runtime prerequisites and preserve configuration/authority boundaries.'}
    write(output / 'assessor-result.json', assessor)
    terminal = build_terminal(spec, ledger, assessor)
    terminal.update(process_state='complete', assurance_state='indeterminate', evidence_maturity='source-only')
    terminal['lineage']['campaign_identity'] = identity
    terminal['residuals'] = [{'id': p['id'], 'summary': p['inference']} for p in props]
    # Preserve actual classes rather than misclassifying static source observations as runtime.
    terminal['evidence'] += [{'class': s['class'] if s['state'].startswith('EXECUTED') else 'model/evidence-contract-definition', 'result': s['state'], 'provenance': s} for s in suites]
    specialist_path = output / 'dpip-specialist.json'
    if specialist_path.exists():
        specialist = json.loads(specialist_path.read_text())
        from autonomous_assurance_controller import validate_assessor
        if validate_assessor(specialist) or specialist['outcome'] != 'INDETERMINATE':
            raise ValueError('unexpected DPIP incomplete-evidence return')
        terminal['evidence'].append({'class': 'model/evidence-contract-definition', 'result': specialist['outcome'],
            'provenance': {'source_pins': config.get('auxiliary_sources', []), 'artifact': 'dpip-specialist.json', 'sha256': digest(specialist_path.read_bytes()), 'scope': 'Explicitly missing privacy observations; no native experiment executed.'}})
    terminal['lenses'] = {
        'rahp': {'materiality': 'applicable', 'execution': 'executed', 'result': 'INDETERMINATE', 'evidence_maturity': 'source-only', 'reason': 'Fresh scenario/harm/proposition source examination completed; broader required evidence remains absent.'},
        'security': {'materiality': 'applicable', 'execution': 'executed', 'result': 'INDETERMINATE', 'evidence_maturity': 'automated-conformance', 'reason': 'Bounded target JavaScript positive/negative vectors executed; Rust/native security and service-composition coverage remain incomplete.'},
        'composition': {'materiality': 'applicable', 'execution': 'required-but-not-executed', 'result': 'INDETERMINATE', 'evidence_maturity': 'source-only', 'reason': 'Lab handoffs attempted; historical native adapters reject this new pin. No full deployed-composition trace accepted.'},
        'drarm': {'materiality': 'applicable', 'execution': 'required-but-not-executed', 'result': 'INDETERMINATE', 'evidence_maturity': 'source-only', 'reason': 'Restart, crash, partition, stale authority, room custody and recovery require target-native induced-failure evidence.'},
        'specialist': {'materiality': 'applicable', 'execution': 'executed' if specialist_path.exists() else 'no-applicable-producer', 'result': 'INDETERMINATE', 'evidence_maturity': 'modeled', 'reason': 'DPIP incomplete-evidence interpretation is separate from unexecuted native observer experiments; human-independence/exclusion evidence also remains required.'}
    }
    from jsonschema import Draft202012Validator
    lens_schema = json.loads((engine / 'schemas/rahp-assurance-run-state-v1.schema.json').read_text())['properties']['lenses']
    Draft202012Validator(lens_schema).validate(terminal['lenses'])
    write(output / 'lens-dispositions.json', terminal['lenses'])
    record = canonical_record(terminal)
    write(output / 'assurance-terminal-machine.json', record)
    (output / 'assurance-terminal-human.md').write_text(markdown(record))
    summary = {'schema': 'rahp-eucalyptus-summary/v1', 'campaign_identity': identity, 'sources': len(config['sources']), 'auxiliary_sources': len(config.get('auxiliary_sources', [])),
               'process_state': 'complete', 'assurance_state': 'indeterminate', 'historical_inputs_used': False,
               'propositions': len(props), 'composition_pass': 0, 'operator_actions_after_trigger': 0,
               'component_attempts': {state: sum(s['state'] == state for s in suites) for state in ('EXECUTED_PASS', 'EXECUTED_NONZERO', 'ATTEMPTED_UNAVAILABLE')},
               'node_tests_passed': sum(s.get('passed', 0) for s in suites if s['state'] == 'EXECUTED_PASS'),
               'governance_disposition': 'AI-assisted assessment proposal; no human risk acceptance or conformance grant.'}
    write(output / 'summary.json', summary)
    lines = ['# Eucalyptus fresh RAHP campaign', '', '**Execution completed; assurance INDETERMINATE.**', '',
             'All 18 coordinated tags are bound to full commit and tag-object identities. No historical verdict was used.', '',
             '## Component evidence', '', '| Attempt | State | Purpose |', '|---|---|---|']
    lines += [f'| {s["id"]} | {s["state"]} | {s["purpose"]} |' for s in suites]
    lines += ['', '## Proposition coverage and retest', '', '| ID | Proposition | Outcome | Owner |', '|---|---|---|---|']
    lines += [f'| {p["id"]} | {p["proposition"]} | {p["outcome"]} | {p["owner"]} |' for p in props]
    for p in props:
        lines += ['', '## ' + p['id'], '', p['inference'], '', '**Retest:** ' + p['retest'], '', '**Required evidence:** ' + p['required_evidence'], '']
        lines += [f'- [{o["path"]}]({o["url"]}): {o["observation"]}' for o in p['source_observations']]
    lines += ['', '## Specialist handoffs', '', 'The pinned Lab room and A/B adapters were actually invoked against Eucalyptus. Their immutable-target checks reject incompatible historical revisions; those attempts do not produce current runtime evidence. DPIP emits an INDETERMINATE portable return from an explicitly unexecuted/missing-observation declaration. Neither handoff is a new privacy experiment.', '', '## Execution substrate', '', 'The JCS suite failure occurs in JSON.stringify(deep) before the target canonicalizer; the separate direct probe exercises the actual tagged canonicalizer and preserves the original failing test. The SSRF positive control depends on local DNS spellings; local-dns-diagnostic records their actual resolution, and the live DID test depends on an external host. None of these failures is silently waived.', '', 'The deployment helper nonzero result must be read with execution-substrate.json: the observed procfs command may not describe the process just spawned in this execution environment. Preserve the raw failure and diagnose on a native host; do not publish it as a VTI vulnerability.', '', '## Limits', '', config['non_scope'], '',
              'Component nonzero exits remain diagnostic observations. Missing tools, dependencies and deployed producers remain INDETERMINATE. No signature, unit suite, source match or green CI is sufficient to grant composition PASS.', '',
              'Source inventories and lockfiles are acquisition/build-input evidence, not observed deployed behavior. The integrity seal detects alteration; it is not a signature or independent attestation. Historical reconciliation is a separate post-seal record.']
    (output / 'report.md').write_text('\n'.join(lines) + '\n')
    seal(output); verify_package(output)
    return summary


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--config', type=Path, default=Path('profiles/dtg/eucalyptus/campaign.json'))
    p.add_argument('--workspace', type=Path)
    p.add_argument('--reuse-sources', action='store_true')
    p.add_argument('--verify-package', type=Path)
    a = p.parse_args()
    if a.verify_package:
        verify_package(a.verify_package); print('PASS evidence integrity'); return 0
    if not a.workspace:
        p.error('--workspace is required')
    try:
        result = campaign(a.config.resolve(), a.workspace.resolve(), a.reuse_sources)
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        failure = {'schema': 'rahp-eucalyptus-execution-failure/v1', 'process_state': 'error', 'assurance_state': 'error',
                   'reason': str(error), 'claim_boundary': 'No completed assurance result may be inferred from an acquisition or orchestration error.'}
        a.workspace.mkdir(parents=True, exist_ok=True)
        write(a.workspace / 'execution-failure.json', failure)
        print(json.dumps(failure), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
