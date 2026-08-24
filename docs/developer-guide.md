---
layout: default
title: "Developer guide"
nav_order: 8
has_toc: true
parent: Learn RAHP
---
# Developer guide

This page collects the repository-facing workflow that previously competed for space in the root README. It is an orientation layer: detailed contracts remain in their dedicated documentation and machine-readable sources.

## Development invariants

RAHP separates the portable method from deployment-specific state. Changes to core schemas, normalized results, engine behavior or portable catalogues must remain usable by an unrelated adopter without inheriting DTG, CAWG/C2PA or another deployment's semantics.

The stable v1 compatibility boundaries are:

```text
rahp-engine-contract-v1
normalized result schema version 1
rahp-evidence-retention-v1
```

See [Engine contract](engine-contract.md), [Portability](portability.md), and `method/versioning.yaml` before changing one of these boundaries.

## Core validation

For ordinary changes, start with:

```bash
python3 tools/validate.py
```

The repository CI also exercises specialized validators. When changing the corresponding surfaces, run the relevant checks locally:

```bash
python3 tools/validate_catalogue.py
python3 tools/validate_glossary.py
python3 tools/validate_assurance_lineage.py
python3 tools/validate_remediation_retest_lineage.py
python3 tools/validate_assurance_graph.py
python3 tools/validate_evidence_freshness_delta.py
python3 tools/validate_authority_policy_gates.py
python3 tools/validate_capability_documentation.py
python3 tools/validate_engine_contract.py
python3 tools/validate_scenario_corpora.py
python3 tools/validate_pressure_tests.py
python3 tools/build.py
python3 tools/validate_reference_links.py
```

See [Performance and execution efficiency](performance.md) for the versioned benchmark profiles used to measure full and cross-specification execution paths.

## Release qualification

`method/release.yaml` is the single current-release declaration. It records the semantic version, tag, presentation name, release notes, compatibility boundary, and the release-specific qualification manifest and validator.

Use the generic release CLI rather than invoking a version-specific release validator from automation:

```bash
python3 tools/release.py metadata
python3 tools/release.py verify
python3 tools/release.py qualify
```

`verify` checks synchronization across package/workspace metadata, `PROJECT-STATUS.yaml`, `method/versioning.yaml`, human-facing release surfaces and the declared release evidence paths. `qualify` first performs that generic verification and then invokes the version-specific qualification validator declared by `method/release.yaml`.

A new release therefore receives a new immutable qualification manifest/validator when its evidence boundary changes, while the release orchestration itself remains stable. Historical qualification contracts are evidence and must not be repurposed for a later release.

## Generated content

Generated views are checked into the repository when they are durable publication/evidence surfaces. Do not hand-edit them.

Important examples include:

- `build/` outputs generated from canonical structured data;
- rendered pressure-test sections generated from `pressure-test.yaml`;
- rendered catalogue/glossary documentation;
- scenario-corpus reader projections where applicable.

If CI reports a generated view as stale, update the canonical source first and run the named renderer. A clean build should produce no uncommitted generated delta.

## Pressure-test records

`examples/**/pressure-test.yaml` is the canonical machine-readable assessment record. The corresponding README contains a generated human-readable projection.

After changing a pressure-test record:

```bash
python3 tools/render_pressure_tests.py
python3 tools/validate_pressure_tests.py
```

Preserve the prior assessment under the example's `history/` directory when the change represents a substantive reassessment rather than an editorial correction. See [Assurance lineage](assurance-lineage.md) and [Review evidence and retention](evidence-retention.md).

## Scenario corpora

Corpora under `corpora/` are adapters from source-specific scenarios to portable RAHP stress patterns. They are not normative forks of the source specifications.

When expanding or re-baselining a corpus:

1. pin an immutable reviewed source revision;
2. preserve source-owned meaning and identifiers;
3. add scenarios because a pressure dimension is missing, not to increase a count;
4. update the machine-readable coverage map;
5. recompose dependent corpora;
6. rerun affected assessments when the semantic or coverage change is material; and
7. validate with `tools/validate_scenario_corpora.py` and `tools/corpus_status.py --offline`.

See [Scenario corpora](scenario-corpora.md) and [Corpus synchronization and provenance](corpus-synchronization.md).

## TypeScript reference implementation

The TypeScript packages are a reference implementation of stable schemas/core/graph/CLI behavior, not a separate source of method semantics.

```bash
npm ci
npm run build:ts
npm run test:ts
```

CI also checks Python/TypeScript conformance so language-specific behavior does not silently diverge.

## Documentation synchronization

`method/capability-documentation.yaml` binds implemented capabilities to implementation, tests and primary documentation. `tools/validate_capability_documentation.py` makes drift testable.

Documentation should follow a layered information architecture:

- **README:** project landing page and routing;
- **hub pages:** getting started, continuous assurance, developer workflow;
- **topic pages:** authoritative explanation of one method/capability;
- **structured method files:** machine-readable contracts;
- **generated views:** publication projections.

Avoid copying detailed topic material back into the README or multiple hub pages. Link to the authoritative page instead.

## Pull-request discipline

Before merging a substantive change:

- confirm canonical structured files validate;
- regenerate durable views;
- inspect the affected assessment/retest impact;
- run the full validation workflow;
- run the documentation/Pages workflow; and
- merge only when both are green.

For contribution conventions, see [How to contribute](how-to-contribute.md) and [CONTRIBUTING.md](../CONTRIBUTING.md).
