---
layout: default
title: "Roadmap"
nav_order: 6
has_toc: true
parent: Reference
---
# RAHP Toolkit Roadmap

This roadmap records the current portable RAHP direction. Historical pre-v1.2 roadmap material is preserved under `archive/pre-v1.2/` and is not current authority.

## v1.8.0 — Semantically Governed Assurance Pipeline (stable release)

Status: **stable public release — Common Map (*Cyrestis thyodamas*)**.

v1.8 strengthens RAHP's operating assurance pipeline without changing the stable v1 compatibility boundary. It improves how material work is selected, how deterministic evidence advances, where human judgment is required, and how specialist privacy examination is integrated.

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
   - adversarial false-independence concerns are classified across Sybil, sock-puppet, false-diversity, trust-laundering, collusion, quorum-capture and selective-evidence classes;
   - these registers remain continuing work and are not misrepresented as completed threat coverage.

### Retained portable capability contracts

v1.8 preserves the previously qualified portable capability set:

- **Durable assessment and finding lineage**
- **Governed remediation and retest**
- **Assurance graph and impact analysis**
- **Evidence provenance, freshness and delta**
- **Executable authority and policy gates**
- **Portfolio and deployment presentation**
- **Release qualification**

These remain executable, documented, deployment-independent capability surfaces. v1.8 extends the operational assurance pipeline around them rather than replacing their contracts.

### Baseline policy

A toolkit release does not automatically requalify maintained external targets. Historical records remain immutable lineage evidence, and open evidence registers remain open unless their own acceptance criteria are satisfied.

## v1.7.0 — Assurance Operations and Cross-Spec Execution

v1.7 qualified monitor-driven assessment queueing, explicit review modes, live current-head assurance regeneration, full DTG cross-spec execution coverage and release-grade regression evidence.

See [v1.7.0 release notes](docs/releases/v1.7.0.md).

## v1.5.0 — Continuous Governed Assurance

v1.5 turned evidence-driven point-in-time assessment into durable, continuously governed assurance while preserving deployment independence. It delivered the retained capability contracts above plus machine-verifiable v1.5 release qualification.

The v1.5 lifecycle remains part of v1.6:

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

v1.8.0 is additive within that boundary. Existing normalized results remain valid.

See [v1.8.0 release notes](docs/releases/v1.8.0.md) and the [v1.8 qualification contract](method/v1.8-release-qualification.yaml).

## v1.2.0 — Evidence-Driven Assurance

v1.2 established typed assurance conclusions, first-class control credit, evidence classification, explicit zero-finding semantics, governed remediation/retest records, DRARM mappings, and Python/TypeScript conformance.

See [v1.2.0 release notes](docs/releases/v1.2.0.md).

## Future work

Subsequent v1.x releases may refine implementation, adoption, corpus coverage and operational tooling without breaking the stable v1 contracts. Each v1.5.0-and-later release receives its own randomly selected West Bengal butterfly release name at release time.

A v2 release is required for breaking changes to the stable method or normalized-result compatibility boundary.

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
