#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import argparse, sys, yaml
ROOT=Path(__file__).resolve().parent.parent

def load(path: Path):
    d=yaml.safe_load(path.read_text(encoding='utf-8')) or {}
    if d.get('deprecated') and d.get('canonical_registry'):
        return load(ROOT/d['canonical_registry'])
    return d

def validate_composition(c: dict, p: str, errors: list[str]) -> None:
    parts=c.get('components',[])
    if not isinstance(parts,list) or len(parts)!=2: errors.append(f'{p}.components must contain exactly two repositories')
    for part in parts:
        if '/' not in str(part.get('repository','')): errors.append(f'{p} has invalid repository')
        if not part.get('corpus_id'): errors.append(f'{p} component corpus_id is required')
    if c.get('runnable'):
        for key in ('corpus_id','assessment','evidence_grade'):
            if not c.get(key): errors.append(f'{p}.{key} required when runnable')
        if c.get('assessment') and not (ROOT/c['assessment']).exists(): errors.append(f"{p}.assessment does not exist: {c['assessment']}")

def main()->int:
    ap=argparse.ArgumentParser(description='Validate an ecosystem/profile-owned cross-specification registry.')
    ap.add_argument('--registry', type=Path, required=True, help='Registry path, e.g. profiles/dtg/cross-spec-tests.yaml')
    ap.add_argument('--composition', help='Validate only the selected composition details while retaining registry-level identity/uniqueness checks')
    args=ap.parse_args(); path=args.registry if args.registry.is_absolute() else ROOT/args.registry
    d=load(path); errors=[]; seen=set(); profile=d.get('profile') or {}
    if not profile.get('id'): errors.append('profile.id is required')
    comps=d.get('compositions',[])
    if not isinstance(comps,list) or not comps: errors.append('compositions must be a non-empty list'); comps=[]

    selected=None
    for i,c in enumerate(comps):
        cid=c.get('id'); p=f'compositions[{i}]'
        if not cid or cid in seen: errors.append(f'{p}.id must be present and unique')
        seen.add(cid)
        if args.composition and cid == args.composition:
            selected=(i,c)
        if not args.composition:
            validate_composition(c,p,errors)

    if args.composition:
        if selected is None:
            errors.append(f'composition is unknown: {args.composition}')
        else:
            i,c=selected
            if not c.get('runnable'): errors.append(f'compositions[{i}] is not runnable: {args.composition}')
            validate_composition(c,f'compositions[{i}]',errors)

    if errors:
        print('\n'.join(f'ERROR: {e}' for e in errors),file=sys.stderr); return 1
    if args.composition:
        print(f"cross-spec registry selected composition valid: profile={profile.get('id')} composition={args.composition}")
    else:
        print(f"cross-spec registry valid: profile={profile.get('id')} {len(comps)} declared, {sum(bool(c.get('runnable')) for c in comps)} runnable")
    return 0
if __name__=='__main__': raise SystemExit(main())
