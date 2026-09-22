#!/usr/bin/env python3
from __future__ import annotations
import argparse, pathlib, yaml
ROOT=pathlib.Path(__file__).resolve().parent.parent
FILES=[('Harm patterns','harm-patterns.yaml','definition'),('Risk patterns','risk-patterns.yaml','description'),('Control patterns','control-patterns.yaml','control_objective'),('Guardrail patterns','guardrail-patterns.yaml','prohibited_state'),('Assurance patterns','assurance-patterns.yaml','assertion'),('Evidence patterns','evidence-patterns.yaml','claim_supported')]
def render():
    out=['---','layout: default','title: "Portable assurance catalogue"','parent: Reference','nav_order: 2','has_toc: true','---','# Portable assurance catalogue','',
    'RAHP v1.1 provides a **method-level assurance knowledge model** that can be reused across deployments without importing deployment governance state. The canonical source is `method/catalogue/`.','',
    'The chain is `harm ← risk → control → guardrail / assurance → evidence`. See the [RAHP glossary](glossary.md) for simple-English definitions.','',
    '## Guardrail completeness','',
    'Each `RKP-*` record declares `guardrail_requirement.status`: `required`, `conditional`, or `control_sufficient`. Only a missing **required** guardrail is a catalogue defect. The current catalogue has **zero required guardrail gaps**. `RKP-PE-02` is conditional because a guardrail is needed only when materially affected parties lack meaningful choice, exit or remedy.','']
    for heading,fn,summary in FILES:
        d=yaml.safe_load((ROOT/'method/catalogue'/fn).read_text())
        out += [f'## {heading}','']
        for r in d['records']:
            out += [f"### {r['id']} — {r['name']}",'',str(r.get(summary) or ''),'']
            fields=[]
            if r.get('family'): fields.append(('Family',r['family']))
            if r.get('control_function'): fields.append(('Control function',r['control_function']))
            if r.get('protected_interest'): fields.append(('Protected interest',r['protected_interest']))
            if r.get('assurance_level'): fields.append(('Assurance level',r['assurance_level']))
            if r.get('guardrail_requirement'):
                gr=r['guardrail_requirement']; fields.append(('Guardrail requirement',gr['status'])); fields.append(('Why',gr['rationale']))
                if gr.get('condition'): fields.append(('Condition',gr['condition']))
            for key in ('harm_patterns','risk_patterns','control_patterns','guardrail_patterns','evidence_patterns'):
                if r.get(key): fields.append((key.replace('_',' ').title(),', '.join(f'`{x}`' for x in r[key])))
            if fields:
                out += ['| Field | Value |','|---|---|']+[f'| {k} | {v} |' for k,v in fields]+['']
    return '\n'.join(out)+'\n'
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--check',action='store_true'); a=ap.parse_args(); p=ROOT/'docs/portable-assurance-catalogue.md'; text=render()
    if a.check:
        if not p.exists() or p.read_text()!=text:
            print('Portable catalogue documentation is stale; run tools/render_portable_catalogue_docs.py'); return 1
        print('Portable catalogue documentation current.'); return 0
    p.write_text(text); print('Rendered',p.relative_to(ROOT)); return 0
if __name__=='__main__': raise SystemExit(main())
