#!/usr/bin/env python3
"""Unified RAHP review entry point.

RAHP supports three review modes:
  rahp      risks-and-harms pressure testing
  security  adversarial security-hardening review
  combined  both lenses plus a generated cross-lens synthesis

This tool scaffolds and orchestrates reviews. It does not infer findings from a
target document. A reviewer (human or AI-assisted) must inspect the target and
populate the canonical YAML records.
"""
from __future__ import annotations
import argparse, datetime as dt, pathlib, re, shutil, subprocess, sys
from typing import Any

try:
    import yaml
except ImportError:
    sys.exit("review.py requires PyYAML: pip install -r requirements.txt")

ROOT=pathlib.Path(__file__).resolve().parent.parent

def dump(path: pathlib.Path, data: dict[str,Any]) -> None:
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(yaml.safe_dump(data,sort_keys=False,allow_unicode=True,width=110),encoding="utf-8")

def load(path: pathlib.Path) -> dict[str,Any]:
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}

def slug_ok(s:str)->bool:
    return bool(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*",s))

def run_tool(name:str,*args:str)->int:
    cmd=[sys.executable,str(ROOT/"tools"/name),*args]
    return subprocess.run(cmd,cwd=ROOT).returncode

def rahp_paths(slug:str, storage:str="exemplar"):
    if storage=="working":
        d=ROOT/".rahp"/"reviews"/slug
        return d/"pressure-test.yaml",d/"README.md"
    d=ROOT/"examples"/slug
    return d/"pressure-test.yaml",d/"README.md"

def security_paths(slug:str, storage:str="exemplar"):
    if storage=="working":
        d=ROOT/".rahp"/"reviews"/slug
        return d/"security-findings.yaml",d/"SECURITY_REVIEW.md"
    d=ROOT/"examples"/"security-hardening"/slug
    return d/"findings.yaml",d/"SECURITY_REVIEW.md"

def combined_paths(slug:str, storage:str="exemplar"):
    if storage=="working":
        d=ROOT/".rahp"/"reviews"/slug
        return d/"combined-review.yaml",d/"COMBINED_REVIEW.md"
    d=ROOT/"examples"/"combined"/slug
    return d/"combined-review.yaml",d/"COMBINED_REVIEW.md"

def base_target(a):
    t={"repository":a.repository,"version":a.version,"commit":a.commit,"source_paths":a.source_path or []}
    if getattr(a,"document",None): t["document"]=a.document
    return t

def init_rahp(a):
    y,readme=rahp_paths(a.slug,a.storage)
    if y.exists() and not a.force: raise SystemExit(f"{y.relative_to(ROOT)} already exists; use --force to replace")
    target=base_target(a)
    data={"review":{
        "id":a.rahp_id or "SR-DRAFT","status":"in-progress","title":f"{a.title} RAHP pressure test",
        "reviewed_on":a.reviewed_on,"target":target,
        "reviewed_against":{"repository":a.rahp_repository,"rahp_version":a.rahp_version,"corpus_date":a.reviewed_on,
                            "engine_contract":"rahp-engine-contract-v1"},
        "scope":{"included":[],"excluded":[]},"method":{"workflow":"docs/pressure-testing-a-spec.md"},
        "summary":{"finding_count":0,"open_count":0},"findings":[]}}
    dump(y,data)
    if not readme.exists() or a.force:
        readme.write_text(f"# {a.title} — RAHP pressure test\n\nHuman-authored interpretation may be added outside the generated block.\n",encoding="utf-8")
    print(f"[init] {y.relative_to(ROOT)}")

def init_security(a):
    y,_=security_paths(a.slug,a.storage)
    if y.exists() and not a.force: raise SystemExit(f"{y.relative_to(ROOT)} already exists; use --force to replace")
    target=base_target(a)
    target.pop("document",None)
    data={"review":{
        "id":a.security_id or "SEC-X-000","status":"in-progress","title":f"{a.title} security-hardening review",
        "reviewed_on":a.reviewed_on,"target":target,
        "reviewed_against":{"repository":a.rahp_repository,"rahp_version":a.rahp_version,
                            "engine_contract":"rahp-engine-contract-v1"},
        "summary":{"finding_count":0,"open_count":0,"overall_assessment":"Review in progress."},
        "findings":[]}}
    dump(y,data); print(f"[init] {y.relative_to(ROOT)}")

def init_combined(a):
    init_rahp(a); init_security(a)
    y,_=combined_paths(a.slug,a.storage)
    data={"review":{
        "id":a.combined_id or "COMB-DRAFT","status":"in-progress","title":f"{a.title} combined RAHP + security review",
        "reviewed_on":a.reviewed_on,
        "target":{"repository":a.repository,"version":a.version,"commit":a.commit},
        "rahp_review":("pressure-test.yaml" if a.storage=="working" else f"../../{a.slug}/pressure-test.yaml"),
        "security_review":("security-findings.yaml" if a.storage=="working" else f"../../security-hardening/{a.slug}/findings.yaml"),
        "summary":"Generated cross-lens synthesis. Add reviewer interpretation in notes when useful.",
        "reviewed_against":{"repository":a.rahp_repository,"rahp_version":a.rahp_version,"engine_contract":"rahp-engine-contract-v1"},
        "notes":[]}}
    dump(y,data); print(f"[init] {y.relative_to(ROOT)}")

def cmd_init(a):
    if not slug_ok(a.slug): raise SystemExit("--slug must use lowercase letters, digits and single hyphens")
    if not re.fullmatch(r"[0-9a-fA-F]{40}",a.commit): raise SystemExit("--commit must be a full 40-character SHA")
    if a.mode=="rahp": init_rahp(a)
    elif a.mode=="security": init_security(a)
    else: init_combined(a)
    print("\nReview scaffold created. Populate canonical YAML findings after examining the target.")
    if a.storage=="working":
        print("Working review is under .rahp/ and is intentionally ignored by Git.")
        print("Promote only a deliberately curated worked example with `review.py promote --mode %s --slug %s`." % (a.mode,a.slug))
    else:
        print("Run `python3 tools/review.py render --mode %s%s` to render the human-readable view." %
              (a.mode, f" --slug {a.slug}" if a.mode=="combined" else ""))

def cmd_render(a):
    rc=0
    if a.mode in ("rahp","combined"): rc=max(rc,run_tool("render_pressure_tests.py"))
    if a.mode in ("security","combined"): rc=max(rc,run_tool("render_security_reviews.py"))
    if a.mode=="combined": rc=max(rc,run_tool("render_combined_reviews.py",*(["--slug",a.slug] if a.slug else [])))
    raise SystemExit(rc)

def cmd_validate(a):
    rc=0
    if a.mode in ("rahp","combined"): rc=max(rc,run_tool("validate_pressure_tests.py"))
    if a.mode in ("security","combined"): rc=max(rc,run_tool("validate_security_reviews.py"))
    if a.mode=="combined": rc=max(rc,run_tool("validate_combined_reviews.py"))
    raise SystemExit(rc)

def cmd_run(a):
    # Render first, then validate. This is orchestration, not automated analysis.
    class X: pass
    x=X(); x.mode=a.mode; x.slug=a.slug
    try: cmd_render(x)
    except SystemExit as e:
        if e.code: raise
    cmd_validate(x)

def cmd_promote(a):
    if not slug_ok(a.slug): raise SystemExit("--slug must use lowercase letters, digits and single hyphens")
    src=ROOT/".rahp"/"reviews"/a.slug
    if not src.exists(): raise SystemExit(f"working review not found: {src.relative_to(ROOT)}")
    pairs=[]
    if a.mode in ("rahp","combined"):
        pairs += [(src/"pressure-test.yaml", rahp_paths(a.slug,"exemplar")[0]), (src/"README.md", rahp_paths(a.slug,"exemplar")[1])]
    if a.mode in ("security","combined"):
        pairs += [(src/"security-findings.yaml", security_paths(a.slug,"exemplar")[0]), (src/"SECURITY_REVIEW.md", security_paths(a.slug,"exemplar")[1])]
    if a.mode=="combined":
        pairs += [(src/"combined-review.yaml", combined_paths(a.slug,"exemplar")[0])]
    for source,dest in pairs:
        if not source.exists(): raise SystemExit(f"missing working review file: {source.relative_to(ROOT)}")
        if dest.exists() and not a.force: raise SystemExit(f"{dest.relative_to(ROOT)} exists; use --force")
        dest.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(source,dest); print(f"[promote] {dest.relative_to(ROOT)}")
    print("Promotion creates a curated exemplar. Deployment dispositions should instead use compact instance review records and evidence manifests.")

def cmd_status(a):
    rows=[]; represented_rahp=set(); represented_security=set()
    for cy in sorted(ROOT.glob("examples/combined/**/combined-review.yaml")):
        c=(load(cy).get("review") or {}); slug=cy.parent.name
        rp=(cy.parent/str(c.get("rahp_review") or "")).resolve(); sp=(cy.parent/str(c.get("security_review") or "")).resolve()
        def state(p):
            if not p.exists(): return "missing"
            r=load(p).get("review") or {}; return f"{r.get('status','?')} / {len(r.get('findings') or [])} finding(s)"
        represented_rahp.add(rp); represented_security.add(sp)
        rows.append((slug,state(rp),state(sp),str(c.get("status") or "?")))
    for py in sorted(ROOT.glob("examples/**/pressure-test.yaml")):
        if py.resolve() not in represented_rahp:
            r=load(py).get("review") or {}; rows.append((py.parent.name,f"{r.get('status','?')} / {len(r.get('findings') or [])} finding(s)","—","—"))
    for sy in sorted(ROOT.glob("examples/security-hardening/**/findings.yaml")):
        if sy.resolve() not in represented_security:
            r=load(sy).get("review") or {}; rows.append((sy.parent.name,"—",f"{r.get('status','?')} / {len(r.get('findings') or [])} finding(s)","—"))
    print("Review inventory")
    print("="*92)
    print(f"{'target':28} {'RAHP':24} {'security':24} {'combined':12}")
    for r in sorted(rows): print(f"{r[0]:28} {r[1]:24} {r[2]:24} {r[3]:12}")

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    sub=ap.add_subparsers(dest="command",required=True)
    ip=sub.add_parser("init",help="scaffold a new review")
    ip.add_argument("--mode",choices=["rahp","security","combined"],required=True)
    ip.add_argument("--slug",required=True); ip.add_argument("--title",required=True)
    ip.add_argument("--repository",required=True); ip.add_argument("--version",required=True)
    ip.add_argument("--commit",required=True); ip.add_argument("--document")
    ip.add_argument("--source-path",action="append",default=[])
    ip.add_argument("--reviewed-on",default=dt.date.today().isoformat())
    ip.add_argument("--rahp-repository",default="sankarshanmukhopadhyay/rahp-toolkit")
    ip.add_argument("--rahp-version",default="v0.9.0")
    ip.add_argument("--rahp-id"); ip.add_argument("--security-id"); ip.add_argument("--combined-id")
    ip.add_argument("--storage",choices=["working","exemplar"],default="working",help="working keeps run artefacts under ignored .rahp/; exemplar writes to examples/")
    ip.add_argument("--force",action="store_true"); ip.set_defaults(func=cmd_init)

    for name,func in [("render",cmd_render),("validate",cmd_validate),("run",cmd_run)]:
        p=sub.add_parser(name,help=f"{name} review outputs")
        p.add_argument("--mode",choices=["rahp","security","combined"],required=True)
        p.add_argument("--slug",help="limit combined rendering to one target slug")
        p.set_defaults(func=func)
    pr=sub.add_parser("promote",help="promote a working review into the curated examples corpus")
    pr.add_argument("--mode",choices=["rahp","security","combined"],required=True); pr.add_argument("--slug",required=True); pr.add_argument("--force",action="store_true"); pr.set_defaults(func=cmd_promote)
    st=sub.add_parser("status",help="show discovered committed exemplar review records"); st.set_defaults(func=cmd_status)
    a=ap.parse_args(); a.func(a)

if __name__=="__main__": main()
