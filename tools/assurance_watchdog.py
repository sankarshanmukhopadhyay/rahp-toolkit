#!/usr/bin/env python3
"""Watch RAHP transient assurance containers for controller stalls.

The watchdog runs after normal lifecycle reconciliation. It does not ask a human to
advance the controller. If a transient state remains beyond the configured SLA, it
creates/reuses a deterministic controller-defect issue keyed to the stranded source
and reason. Normal scheduled lifecycle jobs keep retrying the underlying transition.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
import urllib.parse
from datetime import datetime, timezone
from typing import Any

from dpip_lifecycle import DEFAULT_RAHP_REPO, api

OPEN="assurance:dpip-open"; COMPLETE="assurance:dpip-complete"
RETURN_RE=re.compile(r"<!--\s*dpip-return:[^#\s]+#\d+\s*-->")
RECON_RE=re.compile(r"<!--\s*rahp-dpip-reconciliation:v\d+:")
DEFECT_VERSION="v1"
DEFAULT_SLA_HOURS=6


def has_label(issue: dict[str,Any], name: str) -> bool:
    return any(label.get("name")==name for label in issue.get("labels",[]))


def classify(issue: dict[str,Any], comments: list[dict[str,Any]]) -> str | None:
    text="\n".join(str(c.get("body") or "") for c in comments)
    returned=bool(RETURN_RE.search(text)); reconciled=bool(RECON_RE.search(text))
    opened=has_label(issue,OPEN); complete=has_label(issue,COMPLETE)
    if reconciled: return None
    if complete and not returned: return "specialist-return-stranded"
    if returned: return "reconciliation-stranded"
    if opened: return "specialist-examination-stranded"
    return None


def age_hours(issue: dict[str,Any], now: datetime | None=None) -> float:
    now=now or datetime.now(timezone.utc)
    stamp=str(issue.get("updated_at") or issue.get("created_at") or "")
    if not stamp: return float("inf")
    parsed=datetime.fromisoformat(stamp.replace("Z","+00:00"))
    return max(0.0,(now-parsed).total_seconds()/3600)


def defect_marker(number: int, reason: str) -> str:
    return f"<!-- rahp-controller-defect:{DEFECT_VERSION}:{number}:{reason} -->"


def list_candidates(repo: str, token: str) -> list[dict[str,Any]]:
    out={}
    for label_name in (OPEN,COMPLETE):
        label=urllib.parse.quote(label_name,safe="")
        for issue in api("GET",repo,f"issues?state=open&labels={label}&per_page=100",token) or []:
            if "pull_request" not in issue: out[int(issue["number"])]=issue
    return [out[n] for n in sorted(out)]


def find_defect(repo: str, token: str, marker: str) -> dict[str,Any] | None:
    for page in range(1,5):
        issues=api("GET",repo,f"issues?state=all&per_page=100&page={page}",token) or []
        if not issues: break
        for issue in issues:
            if "pull_request" not in issue and marker in str(issue.get("body") or ""): return issue
        if len(issues)<100: break
    return None


def ensure_defect(repo: str, token: str, source: dict[str,Any], reason: str, age: float) -> dict[str,Any]:
    marker=defect_marker(int(source["number"]),reason); existing=find_defect(repo,token,marker)
    if existing: return existing
    source_url=source.get("html_url") or f"https://github.com/{repo}/issues/{source['number']}"
    body=f"""{marker}

## Autonomous assurance controller defect

The scheduled watchdog found a non-terminal assurance container that remained in a transient state beyond its SLA after normal retry/reconciliation logic ran.

- Source container: {source_url}
- Controller reason: **`{reason}`**
- Observed transient age: **{age:.1f} hours**
- Retry policy: normal scheduled lifecycle reconciliation remains enabled

## Machine disposition

This is a controller/error artefact, not a target assurance FAIL and not a request for a human to advance the workflow. The assurance run remains fail-closed until an automated retry reaches a valid next state or a contract/model remediation supersedes this defect.

## Closure criterion

Close automatically or administratively only after the source lineage contains a valid specialist return/reconciliation/terminal transition and a repeat watchdog scan reports no stranded state.
"""
    return api("POST",repo,"issues",token,{"title":f"[Controller defect] {reason} on RAHP #{source['number']}","body":body,"labels":["assurance"],"assignees":["sankarshanmukhopadhyay"]})


def scan(repo: str, token: str, sla_hours: float) -> tuple[int,int]:
    stranded=0; defects=0
    for issue in list_candidates(repo,token):
        comments=api("GET",repo,f"issues/{issue['number']}/comments?per_page=100",token) or []
        reason=classify(issue,comments)
        if not reason: continue
        age=age_hours(issue)
        if age < sla_hours:
            print(f"PENDING {repo}#{issue['number']}: {reason}; age={age:.1f}h < SLA={sla_hours:.1f}h")
            continue
        stranded+=1; defect=ensure_defect(repo,token,issue,reason,age); defects+=1
        print(f"STRANDED {repo}#{issue['number']}: {reason}; defect={defect.get('html_url')}")
    print(f"WATCHDOG stranded_run_count={stranded} controller_defect_count={defects}")
    return stranded,defects


def self_test() -> int:
    base={"number":9,"labels":[{"name":OPEN}],"updated_at":"2026-08-30T00:00:00Z"}
    assert classify(base,[])=="specialist-examination-stranded"
    complete={**base,"labels":[{"name":COMPLETE}]}; assert classify(complete,[])=="specialist-return-stranded"
    returned=[{"body":"<!-- dpip-return:example/dpip#7 -->"}]; assert classify(complete,returned)=="reconciliation-stranded"
    reconciled=returned+[{"body":"<!-- rahp-dpip-reconciliation:v2:9:7 -->"}]; assert classify(complete,reconciled) is None
    assert defect_marker(309,"specialist-return-stranded")=="<!-- rahp-controller-defect:v1:309:specialist-return-stranded -->"
    assert age_hours({"updated_at":"2026-08-30T00:00:00Z"},datetime(2026,8,30,7,tzinfo=timezone.utc))==7
    print("PASS assurance_watchdog self-test")
    return 0


def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--self-test",action="store_true"); p.add_argument("--sla-hours",type=float,default=float(os.getenv("RAHP_CONTROLLER_SLA_HOURS",DEFAULT_SLA_HOURS))); p.add_argument("--repository",default=os.getenv("RAHP_REPOSITORY",DEFAULT_RAHP_REPO)); a=p.parse_args()
    if a.self_test: return self_test()
    token=os.getenv("GITHUB_TOKEN","")
    if not token: print("GITHUB_TOKEN is required",file=sys.stderr); return 2
    scan(a.repository,token,a.sla_hours); return 0

if __name__=="__main__": raise SystemExit(main())
