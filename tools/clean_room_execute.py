#!/usr/bin/env python3
"""Execute one RAHP clean-room assurance run end to end.

GitHub Actions is transport only. This engine owns clean-room isolation, immutable
checkouts, evidence production, optional autonomous assessor adapters, canonical FSM
progression and citable terminal records.
"""
from __future__ import annotations

import argparse
import copy
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any

import yaml

from autonomous_assurance_controller import build_terminal
from assurance_record import canonical_record, markdown
from clean_room import resolve
from evidence_probe_orchestrator import execute as execute_probes

SHA40=re.compile(r"^[0-9a-f]{40}$",re.I)
REQUIRED={"schema","run","target","resources","assessment","evidence_plan","subject","assurance_contract"}


def run_command(command: Any, cwd: Path) -> None:
    if isinstance(command,list):
        subprocess.run([str(x) for x in command],cwd=cwd,check=True)
    elif isinstance(command,str):
        subprocess.run(command,cwd=cwd,shell=True,check=True)
    else:
        raise ValueError("command must be a string or list")


def validate_spec(spec: dict[str,Any]) -> None:
    missing=sorted(REQUIRED-set(spec))
    if missing: raise ValueError(f"run specification missing keys: {missing}")
    if spec.get("schema") not in {"rahp-clean-room-run/v1","rahp-clean-room-run/v2"}: raise ValueError("unsupported clean-room run schema")
    run=spec.get("run") or {}; target=spec.get("target") or {}; subject=spec.get("subject") or {}; contract=spec.get("assurance_contract") or {}
    for key in ("instance","snapshot"):
        if not run.get(key): raise ValueError(f"run.{key} is required")
    for key in ("repository","revision","release","path"):
        if not target.get(key): raise ValueError(f"target.{key} is required")
    if not SHA40.fullmatch(str(target["revision"])): raise ValueError("target.revision must be immutable 40-character SHA")
    if not subject.get("type") or not subject.get("id"): raise ValueError("subject.type and subject.id are required")
    if "material" not in contract: raise ValueError("assurance_contract.material must be explicit")


def checkout(repo: str, revision: str, path: Path) -> str:
    if path.exists(): raise ValueError(f"checkout path already exists: {path}")
    path.mkdir(parents=True)
    subprocess.run(["git","-C",str(path),"init","-q"],check=True)
    subprocess.run(["git","-C",str(path),"remote","add","origin",f"https://github.com/{repo}.git"],check=True)
    subprocess.run(["git","-C",str(path),"fetch","--depth","1","origin",revision],check=True)
    subprocess.run(["git","-C",str(path),"checkout","--detach","-q","FETCH_HEAD"],check=True)
    actual=subprocess.check_output(["git","-C",str(path),"rev-parse","HEAD"],text=True).strip()
    if SHA40.fullmatch(revision) and actual != revision: raise ValueError(f"immutable pin mismatch for {repo}: {revision} != {actual}")
    if subprocess.check_output(["git","-C",str(path),"status","--porcelain"],text=True).strip(): raise ValueError(f"checkout is dirty: {repo}")
    return actual


def prepare_scaffold(rahp: Path, workspace: Path, spec: dict[str,Any]) -> None:
    target=spec["target"]; assessment=spec["assessment"]
    cfg={
        "version":1,
        "profile":{"id":assessment.get("profile_id","clean-room-assessment"),"title":assessment.get("title","Clean-room assurance assessment")},
        "assessment":{"default_mode":assessment.get("mode","combined"),"rahp_repository":os.getenv("GITHUB_REPOSITORY","sankarshanmukhopadhyay/rahp-toolkit"),"rahp_version":"current-clean-room"},
        "repositories":[{
            "id":assessment.get("target_id","target-under-test"),"repository":target["repository"],"local_path":f"../{target['path']}",
            "version":target["release"],"commit":target["revision"],"reviews":[assessment.get("mode","combined")],
            "context":{"title":assessment.get("target_title",target["repository"])},
        }],"output":{"directory":"build/clean-room-targets"},
    }
    path=workspace/"output"/"clean-room-assessment.yaml"; path.write_text(yaml.safe_dump(cfg,sort_keys=False),encoding="utf-8")
    subprocess.run([sys.executable,str(rahp/"tools"/"rahp.py"),"config-validate","--config",str(path)],cwd=rahp,check=True)
    subprocess.run([sys.executable,str(rahp/"tools"/"rahp.py"),"review","--config",str(path),"--target",assessment.get("target_id","target-under-test"),"--mode",assessment.get("mode","combined"),"--force"],cwd=rahp,check=True)


def run_assessor(workspace: Path, spec: dict[str,Any]) -> Path | None:
    assessor=spec.get("assessor")
    if not isinstance(assessor,dict): return None
    for command in assessor.get("commands",[]) or []: run_command(command,workspace)
    output=assessor.get("result_file")
    if not output: return None
    path=workspace/str(output)
    return path if path.exists() else None


def execute(spec_path: Path, rahp: Path, workspace: Path, nonce: str) -> dict[str,Any]:
    spec=json.loads(spec_path.read_text(encoding="utf-8")); validate_spec(spec)
    output=workspace/"output"; output.mkdir(exist_ok=True)
    resolution=resolve(spec,instance=str(spec["run"]["instance"]),snapshot=str(spec["run"]["snapshot"]),nonce=nonce)
    revisions={}
    resources={"target":spec["target"],**(spec.get("resources") or {})}
    for rid,resource in resources.items():
        revisions[rid]=checkout(str(resource["repository"]),str(resource["revision"]),workspace/str(resource["path"]))
    resolution["resolved_revisions"]=revisions; (output/"clean-room-resolution.json").write_text(json.dumps(resolution,indent=2)+"\n",encoding="utf-8")

    for key,value in (spec.get("environment") or {}).items(): os.environ[str(key)]=str(value).replace("{workspace}",str(workspace))
    for command in spec.get("setup_commands",[]) or []: run_command(command,workspace)
    prepare_scaffold(rahp,workspace,spec)

    plan=copy.deepcopy(spec["evidence_plan"]); plan["lineage"]={"id":resolution["lineage"]["run_id"],**({"issue":spec["run"]["issue"]} if spec["run"].get("issue") is not None else {})}; plan["target"]={"repository":spec["target"]["repository"],"revision":spec["target"]["revision"]}
    (output/"probe-plan.json").write_text(json.dumps(plan,indent=2)+"\n",encoding="utf-8")
    ledger=execute_probes(plan,workspace); (output/"evidence-probe-ledger.json").write_text(json.dumps(ledger,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    if not ledger.get("complete"): raise ValueError(f"evidence orchestration defects: {ledger.get('orchestration_defects')}")
    for command in spec.get("post_probe_commands",[]) or []: run_command(command,workspace)

    assessor_path=run_assessor(workspace,spec); assessor=None
    if assessor_path:
        text=assessor_path.read_text(encoding="utf-8"); assessor=json.loads(text) if assessor_path.suffix.lower()==".json" else yaml.safe_load(text)
    terminal=build_terminal(spec,ledger,assessor); record=canonical_record(terminal)
    (output/"assurance-terminal-machine.json").write_text(json.dumps(record,indent=2)+"\n",encoding="utf-8")
    (output/"assurance-terminal-human.md").write_text(markdown(record),encoding="utf-8")
    qualification={
        "schema":"rahp-clean-room-terminal/v1","lineage_id":resolution["lineage"]["run_id"],"historical_inputs_used":False,
        "subject":record["subject"],"assessment_id":record["assessment_id"],"outcome":record["outcome"],"reason_code":record["reason_code"],
        "state":record["state"],"terminal":record["terminal"],"source_pins":record["source_pins"],"stranded":False,
    }
    (output/"clean-room-terminal.json").write_text(json.dumps(qualification,indent=2)+"\n",encoding="utf-8")
    return qualification


def self_test() -> int:
    good={"schema":"rahp-clean-room-run/v2","run":{"instance":"test","snapshot":"fresh"},"target":{"repository":"example/spec","revision":"a"*40,"release":"v1","path":"target"},"resources":{},"assessment":{},"evidence_plan":{"requirements":[],"producers":{}},"subject":{"type":"specification","id":"example"},"assurance_contract":{"material":True}}
    validate_spec(good)
    bad=dict(good); bad["subject"]={}
    try: validate_spec(bad); raise AssertionError("invalid subject accepted")
    except ValueError: pass
    assert run_assessor(Path("."),good) is None
    print("PASS clean_room_execute self-test")
    return 0


def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--self-test",action="store_true"); p.add_argument("--spec",type=Path); p.add_argument("--rahp",type=Path,default=Path(".")); p.add_argument("--workspace",type=Path,default=Path("..")); p.add_argument("--nonce",default=os.getenv("GITHUB_RUN_ID","local-clean-room")); a=p.parse_args()
    if a.self_test: return self_test()
    if not a.spec: p.error("--spec is required")
    result=execute(a.spec.resolve(),a.rahp.resolve(),a.workspace.resolve(),a.nonce); print(json.dumps(result,indent=2)); return 0

if __name__=="__main__": raise SystemExit(main())
