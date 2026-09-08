# Capability coverage packs

Capability coverage is a portable RAHP mechanism for expressing assurance propositions about a bounded subject without adding that subject's vocabulary to RAHP core.

## Contract

A coverage record identifies a subject, assessment maturity, and propositions. Each proposition selects a generic assurance pattern, an evidence provider, required evidence, evidence references, and a scoped judgment.

Supported maturity levels are `architectural`, `specification`, `implementation`, `runtime`, and `deployment`. Maturity and judgment are independent: evidence that satisfies a proposition at one maturity does not satisfy the same proposition at a later maturity.

Judgments are `SATISFIED`, `UNSATISFIED`, `INDETERMINATE`, `EVIDENCE_REQUIRED`, and `NOT_APPLICABLE`. Missing required evidence cannot produce `SATISFIED`.

Providers identify the source/owner of evidence, not the final assurance authority: `rahp`, `dpip`, `interop-lab`, `external`, or `human-judgment`.

## Generic patterns

The registry covers context isolation, positive disclosure, provenance preservation, atomic resolution integrity, authority non-composition, capability attenuation and chain integrity, lifecycle/current-authority integrity, confidentiality boundaries, unlinkability/correlation, rollback/freshness integrity, operator independence, untrusted agent input, human handling of untrusted content, and cross-context aggregation/non-inference.

`atomic-resolution-integrity` applies when a multi-reference resolution or projection must fail as a unit rather than silently emit a misleading partial result. It is intentionally generic: subject-specific concepts such as Persona profiles or credential bundles belong in coverage packs, not in the core pattern name.

Subject-specific vocabulary belongs in instance or profile coverage packs, not in this registry.

## Example

```yaml
coverage:
  id: example-capability
  subject: example
  maturity: implementation
  propositions:
    - id: P-EX-001
      pattern: context-isolation
      provider: rahp
      judgment: SATISFIED
      assessed_at_maturity: implementation
      evidence_required:
        - negative access evidence
      evidence:
        - source: example-implementation
          revision: abc123
```

Evidence references should retain source identity and revision. RAHP's existing freshness/reconciliation machinery remains authoritative for determining whether a source change makes evidence stale or requires retest; coverage does not introduce a competing freshness state machine.

## Subject-specific packs

The DTG deployment profile stores subject-specific coverage under `profiles/dtg/coverage/`.

`profiles/dtg/coverage/persona.yaml` binds DTG Persona propositions to generic RAHP patterns and pins both the Trust Tasks normative revision and the OpenVTC implementation revision used as evidence. The pack deliberately leaves correlation, cross-context aggregation, composed agent authority, broader version integrity, provenance and unresolved atomicity evidence as `EVIDENCE_REQUIRED` where the pinned evidence does not directly establish the claim.

`profiles/dtg/coverage/data-rooms.yaml` is the canonical architectural-stage Data Rooms proposition catalogue. It defines `P-ROOM-001` through `P-ROOM-016`, including each proposition's title, generic pattern, evidence provider, scoped statement, required evidence, current architectural judgment and residual where applicable. Issue [#481](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/481) uses those identifiers only as references while tracking later implementation/runtime/deployment evidence maturity; it is not a competing proposition definition.

The Data Rooms pack exercises the same generic registry across authorization, capability chains, lifecycle, confidentiality, privacy, freshness, operator independence, recovery, migration, agent-input safety, recall provenance and human-content handling. It also records five materially different scenario families rather than treating “Data Rooms” as one generic operating context.

The Data Rooms pack is intentionally maturity-separated. A design proposition can be `SATISFIED` at `architectural` maturity while the corresponding implementation, runtime-privacy or composition posture remains `EVIDENCE_REQUIRED`. Partial OpenVTC implementation observed at the pinned source state does not automatically upgrade the architectural baseline. In particular, architectural host confidentiality does not imply runtime membership unlinkability, and cryptographic or service distinctness does not establish operator independence.

### Current Data Rooms evidence maturity

The 2026-09-08 execution tranche under #481 exercised the currently obtainable public OpenVTC Data Rooms implementation through the Interop Lab rather than promoting architectural evidence by inspection. At the source-pinned implementation boundary, `P-ROOM-005` and `P-ROOM-012` advanced to bounded satisfaction, `P-ROOM-002` gained stronger mixed-principal/same-subject implementation evidence, and `P-ROOM-013` advanced partially. The remaining `P-ROOM-*` residuals stay explicit where private-room ZK execution, witnessed anchoring/freshness, operator-control evidence, full migration behavior, or composed agent/human runtime surfaces are absent.

This later evidence does **not** rewrite the architectural judgments in `data-rooms.yaml`. The pack remains the immutable architectural baseline; #481 is the durable evidence-maturity/reconciliation owner. Where private-room privacy evidence is required, DPIP owns the specialist evidence contract; where executable composition/runtime evidence is required, the Interop Lab may produce attributable evidence; RAHP retains terminal reconciliation authority.

This is the intended usage model: a subject pack may expose a reusable assurance pattern missing from the registry, but any registry extension must remain subject-neutral. It must not add `Persona`, `Room`, `MLS`, `VAC`, `VMC`, or other consumer-specific semantics to RAHP core. The Data Rooms exercise required no new core pattern, which provides a second independent consumer check on the generic registry introduced by #463.

## Validation and reporting

Run:

```bash
python3 tools/capability_coverage.py path/to/coverage.yaml --summary
```

For the DTG Persona baseline:

```bash
python3 tools/capability_coverage.py profiles/dtg/coverage/persona.yaml --summary
```

For the DTG Data Rooms architectural baseline:

```bash
python3 tools/capability_coverage.py profiles/dtg/coverage/data-rooms.yaml --summary
```

The summary reports propositions defined and assessed, plus counts for each judgment. Validation rejects duplicate/missing proposition identifiers, unknown maturity/provider/judgment/pattern values, satisfaction without required evidence, and implicit maturity promotion.

## Claim boundary

A coverage pack supports only the maturity and evidence actually recorded. Architectural evidence is not implementation evidence; implementation evidence is not runtime or deployment evidence. `EVIDENCE_REQUIRED` is an explicit assurance outcome and never aliases PASS.
