---
layout: default
title: "Adopting RAHP"
nav_order: 1
has_toc: true
parent: Adopt RAHP
---
# Adopting RAHP

RAHP is adopted through configuration. A Working Group, developer, standards project, assurance team, or independent reviewer can use the toolkit without inheriting a bundled deployment. DTG and CAWG/C2PA are examples of the same portable RAHP contracts, not parent environments that a new adopter must copy.

The current stable product boundary is described by `PROJECT-STATUS.yaml`, the engine/result/evidence contracts, and the v2.1 release qualification. Historical release notes remain evidence of earlier boundaries; they are not current adoption instructions.

## 1. Checkout and install

```bash
git clone <rahp-repository>
cd rahp-toolkit
pip install -r requirements.txt
```

## 2. Create `rahp.yaml`

Start from `examples/configurations/minimal.yaml` and replace the target metadata with your own repository or repositories.

```yaml
version: 1
profile:
  id: my-project
  title: My Project
assessment:
  default_mode: combined
repositories:
  - id: specification
    repository: my-org/my-spec
    branch: main
    context:
      title: My Specification
    scope:
      include: ["spec/**", "docs/**"]
    reviews: [rahp, security, combined]
```

## 3. Validate and inspect targets

```bash
python3 tools/rahp.py config-validate --config rahp.yaml
python3 tools/rahp.py targets --config rahp.yaml
```

## 4. Prepare source material

Either pin a full `commit`, provide a Git `local_path`, or let RAHP resolve the configured remote branch. To checkout configured remotes:

```bash
python3 tools/rahp.py prepare --config rahp.yaml --all
```

## 5. Select a review lens

```bash
python3 tools/rahp.py review --config rahp.yaml --target specification --mode rahp
python3 tools/rahp.py review --config rahp.yaml --target specification --mode security
python3 tools/rahp.py review --config rahp.yaml --target specification --mode combined
```

The configured review CLI resolves target provenance and scaffolds canonical review records under the ignored `.rahp/` working area. It does not make an evidence-backed finding merely because a command completed. Examine the target, record defensible findings, render and validate the resulting records, and deliberately promote only maintained exemplars or compact deployment dispositions.

This manual/configured review path is distinct from RAHP's qualified autonomous controller lifecycle. The controller owns assessment state, specialist routing, reconciliation and terminalization for supported automated assurance flows; a successful GitHub workflow or CLI invocation is not itself an assurance conclusion. See `docs/how-rahp-works.md`, `docs/review-modes.md` and `docs/evidence-retention.md`.

## What you do not inherit

A new deployment does not inherit another deployment's governance or assessment state. You do not need the DTG Portfolio Monitor, DTG scenario corpora, DTG governance queue, `RP-001`, canonical DTG `data/` records, CAWG `CRK-*` risks, or CAWG/C2PA monitoring state. Adopt only the method, contracts and capabilities your deployment needs.

This separation remains a core invariant: **shared portable contracts, independent deployment context**. Language-neutral execution/result boundaries are compatibility properties of the current engine contracts, not requirements to adopt any historical deployment shape.

## Optional richer use

Once a project needs recurring scenarios, governed risk/control catalogues, evidence contracts, specialist routing, source-drift monitoring or continuous reassessment, it can adopt those RAHP capabilities deliberately. They are not prerequisites for the first configured review.

See `docs/configuration.md` for the configuration model, `docs/portability.md` for the portability contract, and `docs/continuous-assurance.md` for the machine-owned lifecycle used after material change.

## Portable assurance catalogue

The reusable catalogue under `method/catalogue/` contains portable `HRM-*`, `RKP-*`, `CTP-*`, `GRP-*`, `ATP-*` and `EVP-*` patterns. Adopters may reference or specialize these patterns, but should keep deployment-specific risks, evidence, governance decisions and dispositions in their own deployment state. Do not copy the bundled DTG `data/` merely to obtain the portable catalogue.
