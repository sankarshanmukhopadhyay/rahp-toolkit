#!/usr/bin/env python3
"""Evaluate configured source-text assertions without making assurance judgments."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
from typing import Any
import yaml

def load(path: Path) -> dict[str,Any]:
    text=path.read_text(encoding='utf-8'); value=json.loads(text) if path.suffix=='.json' else yaml.safe_load(text)
    if not isinstance(value,dict): raise ValueError('config root must be a mapping')
    return value

def execute(config: dict[str,Any], root: Path) -> dict[str,Any]:
    out={'schema':'rahp-text-assertion-evidence/v1','requirements':{}}
    for req in config.get('requirements',[]):
        rid=str(req['id']); surfaces={}; paths=[]
        for pattern in req.get('paths',[]): paths.extend(p for p in root.glob(pattern) if p.is_file())
        for index, assertion in enumerate(req.get('assertions',[])):
            regex=re.compile(str(assertion['pattern']),re.I|re.M|re.S)
            matches=[]
            for path in sorted(set(paths)):
                try: text=path.read_text(encoding='utf-8')
                except UnicodeDecodeError: continue
                if regex.search(text): matches.append(str(path.relative_to(root)))
            expected=bool(assertion.get('expected_present',True)); observed=bool(matches)
            satisfied=(observed==expected)
            surfaces[str(assertion.get('id') or f'a{index+1}')]={'classification':'satisfied' if satisfied else 'absent','expected_present':expected,'observed_present':observed,'matched_paths':matches}
        if not surfaces: surfaces['configuration']={'classification':'not-evidenced','reason':'no assertions configured'}
        out['requirements'][rid]={'surfaces':surfaces,'root':str(root),'paths':req.get('paths',[])}
    return out

def self_test()->int:
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        root=Path(d); (root/'spec.md').write_text('Clients MUST use context-bound tokens.\n')
        cfg={'requirements':[{'id':'ER-1','paths':['*.md'],'assertions':[{'id':'bounded','pattern':'MUST use context-bound tokens','expected_present':True},{'id':'forbidden','pattern':'global reusable identifier','expected_present':False}]}]}
        result=execute(cfg,root); classes={x['classification'] for x in result['requirements']['ER-1']['surfaces'].values()}; assert classes=={'satisfied'}
    print('PASS text_assertion_probe self-test'); return 0

def main()->int:
    p=argparse.ArgumentParser(); p.add_argument('--self-test',action='store_true'); p.add_argument('--config',type=Path); p.add_argument('--root',type=Path); p.add_argument('--output',type=Path); a=p.parse_args()
    if a.self_test:return self_test()
    if not a.config or not a.root or not a.output:p.error('--config --root --output required')
    result=execute(load(a.config),a.root); a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(yaml.safe_dump(result,sort_keys=False),encoding='utf-8'); return 0
if __name__=='__main__': raise SystemExit(main())
