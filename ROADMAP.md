---
layout: default
title: "Roadmap"
nav_order: 6
has_toc: true
parent: Reference
---
# RAHP Toolkit Roadmap

## v2.0.0 — Portable Assurance Engine Stabilization (stable release)

Status: **stable public release candidate — Blue Mormon (*Papilio polymnestor*)**.

v2.0 marks the product-level architecture boundary where RAHP core becomes deliberately boring: new portfolio findings should normally change instance data, profiles, evidence, or conclusions rather than generic engine code.

### Delivered workstreams

1. **Normalized finding model**
   - portfolio-neutral finding schema;
   - source text retained as provenance;
   - semantic-first routing;
   - unknown qualified concepts become `UNMAPPED`.

2. **Declarative instance profiles**
   - DTG-specific extraction and routing semantics live under `instances/dtg/`;
   - generic finding logic no longer owns target vocabulary.

3. **Portable specialist assessor contract**
   - finite PASS / FAIL / INDETERMINATE / NOT_APPLICABLE results;
   - required reason code, evidence use, residual risk and action;
   - malformed returns invalidate provenance instead of contributing GREEN.

4. **Finite lifecycle controller**
   - explicit DISCOVERED → QUALIFIED → ROUTED → ASSESSMENT_REQUIRED → EVIDENCE_REQUIRED → EVIDENCE_READY → ASSESSED → TERMINAL transitions;
   - plugin error cannot become PASS.

5. **First-class clean-room mode**
   - engine-owned unique lineage;
   - historical state/evidence exclusion;
   - coalescing forbidden;
   - fresh specialist lineage required.

6. **Black-box portability acceptance**
   - frozen DTG snapshots for 28, 29 and 30 Aug execute through one unchanged stabilized core;
   - non-DTG/CAWG validation remains part of the suite;
   - final DTG target failures were discovered without further RAHP-core modification.

### Compatibility

The product major version does not invalidate the stable portable compatibility authorities:

```text
rahp-engine-contract-v1 revision 1.3
normalized result schema version 1
rahp-evidence-retention-v1
```

Historical v1.x results and evidence remain valid.


This roadmap records the current portable RAHP direction. Historical pre-v1.2 roadmap material is preserved under `archive/pre-v1.2/` and is not current authority.

## v1.9.0 — Portable Clean-Room Assurance (stable release)

Status: **stable public release — Lesser Mime (*Papilio epycides*)**.

v1.9 qualifies clean-room assurance as a reusable portable capability without changing the stable v1 compatibility boundary.

### Delivered workstreams

1. **Generic declarative clean-room execution**
   - one canonical `clean-room-assessment.yml` executor;
   - target, resource, adapter and evidence-producer semantics supplied through a run specification;
   - immutable source pins and explicit fresh lineage.

2. **Attributable evidence production**
   - evidence requirements carry explicit producer and attempt state;
   - target-native and composition evidence remain separately attributed;
   - missing or unexercised evidence remains missing rather than being promoted to PASS.

3. **Experiment-role semantics**
   - same-relationship runs can be declared as positive controls with `must-detect` semantics;
   - materially context-distinct target-native runs can be declared as unlinkability pressure cases with `must-not-emerge` semantics;
   - a detected positive-control join is detector-sensitivity evidence, not target privacy failure.

4. **Fresh specialist lineage**
   - clean-room evidence feeds a fresh semantic RAHP review;
   - privacy materiality can create a new DPIP examination;
   - DPIP `INDETERMINATE` remains non-green;
   - historical RAHP and DPIP records remain immutable.

5. **Workflow governance**
   - obsolete target-specific clean-room workflows are removed;
   - an executable governance check prevents their reintroduction;
   - distinct lifecycle/state-machine workflows remain separate where their semantic ownership differs.

6. **Target-adapter portability acceptance**
   - Interop Lab #71/#72 adds a target-native context-distinct Dogwood pressure adapter;
   - the existing positive control remains unchanged;
   - generic RAHP clean-room execution and generic Interop A/B classification/export logic require no VTI/Dogwood-specific branch.

### Baseline policy

A toolkit release does not automatically requalify every maintained external target. Historical records remain immutable lineage evidence. A bounded favourable pressure observation does not become a global target privacy PASS.

## v1.8.0 — Semantically Governed Assurance Pipeline

Status: **historical stable release — Common Map (*Cyrestis thyodamas*)**.

v1.8 strengthened RAHP's operating assurance pipeline without changing the stable v1 compatibility boundary. It improved how material work is selected, how deterministic evidence advances, where human judgment is required, and how specialist privacy examination is integrated.

### Delivered workstreams

1. **Gatherer-native end-to-end assurance**
   - material repository changes retain immutable revision and gatherer lineage;
   - published assessment IDs advance directly without read-after-create discovery races;
   - portfolio GREEN/AMBER/RED remains evidence-dependent rather than CI-dependent.

2. **Bounded evidence-backed disposition**
   - deterministic evidence may close a review only under explicit evidence-sufficiency rules;
   - semantic uncertainty escalates to `judgment-required`;
   - workflow success is not converted into assurance success.

3. **Polarity-aware evidence**
   - strengthening/prevention evidence is distinguished from weakening/introduction evidence;
   - ambiguous lexical signals do not manufacture a PASS or adverse finding.

4. **RAHP → DPIP lifecycle**
   - privacy examination is invoked only when warranted;
   - handoff contracts, source pins, return lineage and DPIP applicability are explicit;
   - `INDETERMINATE` remains non-green.

5. **Semantic materiality**
   - normative, security-sensitive, implementation-semantic and genuine dependency changes remain assessment-worthy;
   - generated/codegen convergence is triaged rather than automatically promoted to broad review;
   - bounded release-only propagation is informational;
   - low-weight release fan-out cannot mask one high-significance semantic change.

6. **Structured continuing evidence programmes**
   - VTI composition candidates are indexed as pre-specification evidence;
   - adversarial false-independence concerns are classified across Sybil, sock-puppet, false-diversity, trust-laundering, collusion, quorum-capture and selective-evidence classes.

The final bullet above records the **v1.8.0 release boundary** and remains historically correct.

### Post-release evidence

After v1.8.0 was cut, issue [#193](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/193) completed the seven-row adversarial false-independence evidence corpus. That completion does not retroactively extend the v1.8.0 qualification claim; it is later evidence preserved in current lineage.

### Retained portable capability contracts

v1.9 preserves the previously qualified portable capability set:

- **Durable assessment and finding lineage**
- **Governed remediation and retest**
- **Assurance graph and impact analysis**
- **Evidence provenance, freshness and delta**
- **Executable authority and policy gates**
- **Portfolio and deployment presentation**
- **Release qualification**

## v1.7.0 — Assurance Operations and Cross-Spec Execution

Status: **historical stable release — Common Palmfly (*Elymnias hypermnestra*)**.

v1.7 qualified monitor-driven assessment queueing, explicit review modes, live current-head assurance regeneration, full DTG cross-spec execution coverage and release-grade regression evidence.

See [v1.7.0 release notes](docs/releases/v1.7.0.md).

## v1.5.0 — Continuous Governed Assurance

v1.5 turned evidence-driven point-in-time assessment into durable, continuously governed assurance while preserving deployment independence.

The retained lifecycle is:

```text
material target change
        ↓
impact selection
        ↓
freshness evaluation
        ↓
evidence retained / weakened / invalidated
        ↓
assessment or retest
        ↓
assurance delta
        ↓
residual obligation + remediation
        ↓
policy gate: PASS | FAIL | INDETERMINATE
        ↓
independent authority verification
        ↓
governed disposition/publication
        ↓
portable assurance posture
```

See [v1.5.0 release notes](docs/releases/v1.5.0.md) and [Continuous assurance](docs/continuous-assurance.md).

## Compatibility

The stable v1 compatibility boundaries remain:

```text
rahp-engine-contract-v1
normalized result schema version 1
rahp-evidence-retention-v1
```

v1.9.0 is additive within that boundary. Existing normalized results remain valid.

See [v1.9.0 release notes](docs/releases/v1.9.0.md) and the [v1.9 qualification contract](method/v1.9-release-qualification.yaml).

## v1.2.0 — Evidence-Driven Assurance

v1.2 established typed assurance conclusions, first-class control credit, evidence classification, explicit zero-finding semantics, governed remediation/retest records, DRARM mappings, and Python/TypeScript conformance.

See [v1.2.0 release notes](docs/releases/v1.2.0.md).

## Future work

Subsequent releases may refine implementation, adoption, corpus coverage and operational tooling while preserving or explicitly versioning the stable portable contracts. Each v1.5.0-and-later release receives its own randomly selected name from the governed pinned West Bengal butterfly pool.

Product semantic version and engine/result/evidence contract identifiers are related but distinct compatibility authorities. A breaking contract change still requires a new contract/schema identity even when the product major version has already advanced.

## Explicit non-goals

RAHP does not make these default behaviours:

- automatic filing into arbitrary upstream repositories;
- treating repository permissions as governance authority;
- treating a policy-gate PASS as delegation, publication authority or risk acceptance;
- equating detector absence with assurance;
- coupling portable core to a maintained deployment;
- using a universal assurance score to hide materially different states.

## Historical roadmap

The full pre-v1.2 roadmap is retained at `archive/pre-v1.2/ROADMAP-pre-v1.2.txt`.
