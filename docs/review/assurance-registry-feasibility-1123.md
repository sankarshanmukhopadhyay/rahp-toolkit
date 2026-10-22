# Assurance registry feasibility evaluation — #1123

**Status:** implementation evidence available; final issue disposition pending PR validation  
**Issue:** #1123  
**Implementation:** PR #1124  
**Authority boundary:** `method/catalogue/` remains authoritative for portable assurance semantics.

## Question

Can a future RAHP assessment reuse registered assurance knowledge rather than reconstructing equivalent reasoning from prose, while preserving the evidence and authority boundaries necessary to independently evaluate the assessment?

## Repository evidence discovered

The feasibility investigation found that RAHP already had the substantive reusable assurance model before #1123:

- six portable object families under `method/catalogue/`: harms, risks, controls, guardrails, assurance patterns and evidence patterns;
- stable `HRM-*`, `RKP-*`, `CTP-*`, `GRP-*`, `ATP-*` and `EVP-*` identifiers;
- `method/schema/catalogue.schema.json` for catalogue record structure;
- `tools/validate_catalogue.py` for catalogue graph validation;
- `tools/portable_catalogue.py` for resolving assessment `portable_assurance` mappings;
- generated human-readable catalogue documentation;
- maintained assessments that already reference portable IDs while retaining assessment-specific evidence.

This means a second registry ontology, new identifier namespace, or duplicate lifecycle model would add authority ambiguity rather than useful capability.

## Implemented experiment

PR #1124 adds a derived registry index builder over the existing catalogue.

The index exposes:

- stable portable ID;
- object type;
- name and concise semantic summary;
- canonical source file;
- typed relationships to adjacent portable objects.

It deliberately does not copy deployment findings, assessment evidence, dispositions or upstream authority.

The builder fails closed on:

- duplicate portable IDs;
- unresolved portable references;
- inconsistent catalogue versions;
- malformed relationship lists.

## Real consumption path

The maintained Trust Tasks pressure test at
`examples/trust-tasks-spec/pressure-test.yaml` already references the portable
catalogue through `portable_assurance`.

The registry test resolves those existing references through the derived index
and verifies that each reference returns:

1. a known registry entry;
2. the expected object type; and
3. the canonical `method/catalogue/` source location.

The assessment is not rewritten to contain registry metadata. Its source-pinned
observations, findings, harms, recommendations and dispositions remain local
assessment evidence.

A concrete path is Trust Tasks finding `F-003`, which references
`RKP-AUTH-02` and `ATP-AUTH-02`. The registry resolves these as a risk pattern
and assurance pattern respectively, while the finding retains the evidence for
why those patterns apply to the reviewed Trust Tasks revision.

## Feasibility findings

### 1. Did the registry replace duplicated assurance reasoning?

**Partially, but mainly at the discovery boundary.**

The portable catalogue had already eliminated much semantic duplication.
The registry does not replace that catalogue. It makes existing reusable
semantics easier for tools to enumerate and resolve without understanding six
separate catalogue files.

### 2. Can an assessment reuse objects without reading their originating assessment?

**Yes.**

Portable IDs resolve to method-level definitions and relationships under
`method/catalogue/`. They do not depend on the assessment that first motivated
or used them.

### 3. Are provenance and authority clear?

**Yes, if the registry remains derived.**

The registry records the canonical source path and declares itself derived.
Assessment evidence remains assessment-local. The registry does not become an
independent semantic authority.

### 4. Can references be validated mechanically?

**Yes.**

Existing RAHP validation already validates `portable_assurance` references
directly against the canonical catalogue. The new registry tests additionally
prove that those same references are resolvable as typed discovery records.

This is intentionally not a second semantic validator.

### 5. Does the registry improve traceability?

**Yes, in a bounded way.**

A consumer can move from an assessment ID reference to its object type,
canonical source and adjacent relationships through one deterministic index.

### 6. Does it simplify assessment execution?

**Not materially.**

Current RAHP assessment validation already works without the registry. The
registry should therefore not become a mandatory execution dependency.

### 7. Are new object classes needed?

**No evidence currently justifies them.**

The original #1123 hypotheses included questions, scenarios, personas,
evidence requirements and templates. Existing repository evidence shows that
the six portable catalogue families already cover the reusable assurance
semantics relevant to this experiment. Personas, scenarios and assessment
records have separate existing authority and lifecycle boundaries.

### 8. Does the experiment justify expansion?

**It justifies retaining a lightweight derived index, not creating a new
registry subsystem or repository.**

The demonstrated value is machine discovery, typed resolution and navigation.
There is no current evidence that RAHP needs a registry API, a second lifecycle,
new identifiers, or independently governed registry releases.

## Decision recommendation

Choose **B: continue within RAHP**, narrowly.

Retain the derived registry builder and documentation as an optional discovery
surface over the portable catalogue.

Do not:

- create a separate registry repository;
- mint replacement identifiers;
- duplicate catalogue validation;
- make registry availability a prerequisite for assessment execution;
- expand into personas/templates/scenarios until a concrete consumer requires it.

Future expansion should require evidence of an external or cross-project
consumer that cannot use the current catalogue/index surfaces cleanly.

## Acceptance interpretation

Several original #1123 acceptance criteria were hypotheses that repository
inspection showed to be already satisfied or superseded:

- object taxonomy: existing six-family portable catalogue;
- schema: existing catalogue schema;
- identifier semantics: existing stable catalogue identifiers;
- initial corpus: existing maintained catalogue, substantially larger than the
  proposed 10–20 object experiment;
- human-readable catalogue: existing generated portable catalogue view;
- assessment integration: existing `portable_assurance` mappings, now exercised
  through the derived registry index.

The remaining completion evidence is successful PR validation after the real
consumption test is added.

## Required repository gate

Before merge, the ready-for-review head must satisfy the repository-required
`DCO`, `validate` and `TypeScript conformance` checks. These checks are
merge-gating evidence for repository integration; they do not change the
assurance authority of the derived registry.

## Residual limitation

This experiment demonstrates repository-internal consumption. It does not
establish independent external adoption, cross-project interoperability, or a
need for separately versioned registry governance.
