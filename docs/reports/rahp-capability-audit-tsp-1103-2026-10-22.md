# RAHP capability audit after the TSP Release 1.0 assessment

**Tracking:** #1103  
**Assessment source:** completed four-lens TSP Release 1.0 campaign #1105.  
**Purpose:** distinguish demonstrated generic RAHP gaps from target-specific convenience work before changing the toolkit.

## Authority and decision rule

This audit treats `method/` as portable method authority, `tools/` as reusable execution support, `instances/` as deployment-owned state, and `examples/` as maintained/explanatory evidence. A TSP-specific inconvenience is not by itself evidence for a portable feature. Missing evidence remains non-PASS, and a generic change is justified only where the completed campaign demonstrates repeated or authority-boundary value.

## Capability disposition

| Deferred question from #1103 | Inspected support | Disposition | Change |
|---|---|---|---|
| source-pinned normative delta comparison | pressure tests require full commit pins; source review records and ordinary Git/source comparisons preserve changed-clause provenance | **not a demonstrated portable gap** | no generic normative-delta engine added; target-specific delta analysis may remain campaign evidence |
| RAHP + security + composition + DRARM orchestration | `tools/review.py`, `docs/review-modes.md`, `docs/full-stack-assurance-orchestration.md`, lens ledgers and DRARM adapter already distinguish execution, evidence maturity and assurance state | **already supported** | no new orchestrator |
| evidence export and reproducibility | DRARM emits JSON, Markdown and assessment-event JSON; review records are canonical YAML; evidence-retention and reproduction contracts already exist | **already supported** | no new export format |
| issue-first / durable public assessment record | assessment events and `publish_assessment_issues.py` support durable issue ownership; #1105 also demonstrated issue-hosted final reports without target-specific CI/tooling | **already supported / governance-gated** | no publication bypass or automatic upstream mutation added |
| missing reusable TSP negative cases | #1105 identified concrete implementation regression vectors, but no new generic RAHP failure mechanism was required for the bounded specification assessment | **not justified as portable catalogue work** | retain target/runtime vectors with implementation-conformance work |
| deployment-local catalogue references in rendered pressure tests | canonical validator resolves `instances/*/data/`, but renderer previously manufactured DTG catalogue links for local records with no explicit deployment link | **confirmed portability defect** | renderer now preserves explicit local links and otherwise renders titled code; regression tests added |

## Concrete defect: deployment-local reference rendering

### Reproduction before the fix

A temporary deployment-local `ZRK-01` risk under `instances/zz1103/data/risks.yaml` was referenced by a valid pressure test.

- `validate_pressure_tests.py --file ...` accepted the record and reported all references resolved.
- `render_pressure_tests.py` emitted `../../build/site/catalogue.html#ZRK-01`.
- `validate_reference_links.py` rejected the generated README because `ZRK-01` is not a bundled DTG catalogue ID.

The canonical validator was correct. The generated link violated the deployment authority boundary.

### Correct behavior

- bundled `data/` records without an explicit link continue to deep-link to the DTG catalogue;
- deployment-local records with an explicit `link` preserve that deployment-owned link;
- deployment-local records without a link render as titled code, not a false DTG-catalogue link.

This keeps portability without requiring every deployment catalogue to be merged into DTG or the global build.

## Source-delta decision

The TSP campaign used a one-off normative-delta helper on an abandoned TSP-specific branch. The completed campaign did not demonstrate that changed-hunk semantic classification is a stable portable RAHP engine responsibility. RAHP already requires immutable target pins and reviewer-authored evidence; normal repository comparison can establish the source delta. A generic semantic-delta tool would need broader cross-target evidence before entering `tools/`.

**Disposition:** no portable normative-delta tool in this tranche.

## Orchestration and evidence decision

The full-stack orchestration contract already requires explicit RAHP, security, composition, DRARM and specialist dispositions; it separates `process_state`, `assurance_state` and `evidence_maturity`, and permits completed campaigns to remain `INDETERMINATE`. DRARM already exports normalized JSON, Markdown and issue-event JSON. These are the capabilities #1105 needed.

The TSP campaign exposed workflow learning, not a missing engine/schema contract. Documentation already states that `review.py` scaffolds/renders/validates but does not infer findings.

**Disposition:** no new orchestrator or evidence schema.

## Negative-case decision

The TSP assessment produced useful Release 1.0 regression obligations for canonical CESR, trailing bytes, sender binding and key-state behavior. These are protocol/implementation test vectors. They did not establish a missing reusable harm/risk/control mechanism in the portable RAHP catalogue.

**Disposition:** no speculative catalogue additions from TSP.

## Compatibility and follow-up

The renderer fix changes only invalid fallback-link behavior for deployment-local records lacking their own links. It does not change canonical IDs, schemas, review semantics, portable catalogue authority, or valid explicit deployment links.

If future assessments demonstrate a recurring need for semantic source-delta classification across unrelated specifications, that should be opened as a separately evidenced capability proposal rather than resurrecting TSP-specific tooling.
