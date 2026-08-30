# RAHP release codename governance

From v1.5.0 onward, RAHP uses butterfly names derived from Wikipedia's **List of butterflies of West Bengal** as human-readable release codenames. Semantic version/tag identity remains authoritative.

## Repository-local authority

The naming mechanism is owned by this repository. The shared cross-repository pattern does not make another repository authoritative over RAHP releases.

Machine-readable state:

- `config/release-codenames.txt` — reviewed eligible common names;
- `config/release-codename-policy.json` — provenance and selection rules;
- `config/release-codename-history.json` — immutable/persisted version→codename bindings;
- `tools/release_codenames.py` — policy validator and future-name selector;
- `method/release.yaml` — authoritative current release declaration consumed by the existing qualification/publication workflow.

## Release lifecycle

```text
coherent RAHP capability boundary
  ↓
semantic candidate version
  ↓
select unused codename from pinned pool
  ↓
persist candidate version→codename binding
  ↓
update current release declaration and qualification evidence
  ↓
review / pressure tests / human release decision
  ↓
Actions requalifies current state
  ↓
annotated tag + GitHub Release
```

A future candidate name can be previewed with:

```bash
python3 tools/release_codenames.py select --version vX.Y.Z
```

The selected candidate must then be persisted in `config/release-codename-history.json` in the same reviewed release-candidate change that updates `method/release.yaml`. `python3 tools/release.py verify` and `qualify` enforce that the current declaration matches the persisted binding.

## Invariants

1. Wikipedia is provenance, not a release-time runtime dependency.
2. Pool entries are unique case-insensitively and source-attributed.
3. Previously used names are excluded while unused names remain.
4. Reuse is forbidden unless the reviewed policy explicitly changes.
5. Existing semantic-version bindings cannot silently change names.
6. Candidate identity is known before human release acceptance.
7. Release publication remains idempotent and cannot rewrite an existing GitHub Release.
8. Green workflow execution is necessary but does not replace the human release judgment embodied by the reviewed release declaration/qualification state.

## Historical alias

`v1.8.0 — Common Map` remains immutable historical release metadata. The current source page labels *Cyrestis thyodamas* as `map butterfly`; the repository policy therefore records `Common Map` as a grandfathered historical alias. This preserves the published judgment trail rather than rewriting history to track later source wording.
