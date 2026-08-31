#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, shutil, subprocess, sys
from pathlib import Path


def run_case(rahp: Path, root: Path, case: dict, nonce: str) -> dict:
    work=root/'work'/case['id']
    if work.exists(): shutil.rmtree(work)
    work.mkdir(parents=True)
    cmd=[sys.executable,str(rahp/'tools'/'clean_room_execute.py'),'--spec',str(rahp/case['spec']),'--rahp',str(rahp),'--workspace',str(work),'--nonce',nonce]
    subprocess.run(cmd,check=True)
    terminal=json.loads((work/'output'/'clean-room-terminal.json').read_text())
    if terminal['outcome'] != case['expected_outcome']:
        raise AssertionError(f"{case['id']}: {terminal['outcome']} != {case['expected_outcome']}")
    if case.get('expected_reason') and terminal['reason_code'] != case['expected_reason']:
        raise AssertionError(f"{case['id']}: {terminal['reason_code']} != {case['expected_reason']}")
    if terminal.get('stranded') is not False or terminal.get('terminal') is not True:
        raise AssertionError(f"{case['id']}: non-terminal/stranded result")
    dest=root/'qualification-output'/case['id']
    if dest.exists(): shutil.rmtree(dest)
    shutil.copytree(work/'output',dest)
    return terminal


def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument('--manifest',type=Path,required=True); p.add_argument('--rahp',type=Path,required=True); p.add_argument('--root',type=Path,required=True); p.add_argument('--nonce',required=True); a=p.parse_args()
    rahp=a.rahp.resolve(); root=a.root.resolve(); manifest=json.loads(a.manifest.read_text())
    results=[]
    for case in manifest['cases']:
        results.append(run_case(rahp,root,case,f"{a.nonce}-{case['id']}"))
    subject_types={r['subject']['type'] for r in results}
    missing=set(manifest.get('required_subject_types',[]))-subject_types
    if missing: raise AssertionError(f"missing subject types: {sorted(missing)}")
    if manifest.get('require_zero_stranded') and any(r.get('stranded') for r in results): raise AssertionError('stranded qualification run')

    # Replay identity: re-run the standalone A2A subject with a distinct transport nonce.
    replay_case=next(c for c in manifest['cases'] if c['id']=='a2a-standalone')
    original=next(r for r in results if r['subject']['id']=='A2A-v1-specification')
    replay=run_case(rahp,root,{**replay_case,'id':'a2a-standalone-replay'},f"{a.nonce}-replay")
    if replay['assessment_id'] != original['assessment_id']: raise AssertionError('replay changed assessment identity')

    # The DPIP resource pinned by the DTG case carries the durable outbox regression self-test.
    if manifest.get('require_outbox_contract_test'):
        dpip=root/'work'/'dtg-composite'/'dpip'
        subprocess.run([sys.executable,str(dpip/'scripts'/'rahp_return.py'),'--self-test'],cwd=dpip,check=True)

    summary={
      'schema':'rahp-zero-touch-qualification/v1','issue':manifest.get('issue'),'operator_actions_after_trigger':0,
      'stranded_runs':0,'cases':[{'subject':r['subject'],'assessment_id':r['assessment_id'],'outcome':r['outcome'],'reason_code':r['reason_code'],'state':r['state'],'terminal':r['terminal']} for r in results],
      'replay':{'same_assessment_id':True,'assessment_id':original['assessment_id']},
      'outbox_contract_self_test':bool(manifest.get('require_outbox_contract_test')),
    }
    out=root/'qualification-output'; out.mkdir(exist_ok=True); (out/'qualification-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2)); return 0

if __name__=='__main__': raise SystemExit(main())
