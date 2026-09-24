#!/usr/bin/env python3
from pathlib import Path
import argparse, yaml
ROOT=Path(__file__).resolve().parent.parent
ap=argparse.ArgumentParser(); ap.add_argument('--registry',required=True); ap.add_argument('--composition',required=True); ap.add_argument('--github-output',type=Path)
a=ap.parse_args(); rp=Path(a.registry); rp=rp if rp.is_absolute() else ROOT/rp
d=yaml.safe_load(rp.read_text()) or {}
if d.get('deprecated') and d.get('canonical_registry'): d=yaml.safe_load((ROOT/d['canonical_registry']).read_text()) or {}
item=next((x for x in d.get('compositions',[]) if x.get('id')==a.composition),None)
if not item or not item.get('runnable'): raise SystemExit(f'Composition is unknown or not runnable: {a.composition}')
vals={'assessment':item['assessment'],'corpus_id':item['corpus_id'],'profile_id':(d.get('profile') or {}).get('id','external'),'execution_class':item['execution_class']}
for k,v in vals.items(): print(f'{k}={v}')
if a.github_output:
    with a.github_output.open('a',encoding='utf-8') as f:
        for k,v in vals.items(): f.write(f'{k}={v}\n')
