# Executable evidence producer result contract

RAHP accepts executable evidence as an **observation-bearing input to assurance**, not as an assurance decision.

The target-neutral producer return is `rahp-evidence-producer-result/v1`, defined by `schemas/rahp-evidence-producer-result-v1.schema.json`.

## Ownership boundary

The contract separates three responsibilities:

1. **Evidence producer** — executes a source-pinned experiment or observation and returns attributable artifacts, observations, execution metadata, freshness/invalidation keys and an explicit claim boundary.
2. **Specialist/profile** — interprets domain-specific meaning where required. Privacy observer/correlation semantics, for example, remain DPIP-owned.
3. **RAHP** — routes obligations/evidence, validates generic provenance and freshness, reconciles specialist returns and owns terminal assurance state.

A producer result therefore MUST NOT encode terminal RAHP or portfolio assurance outcomes. `workflow green != assurance green` and `missing evidence != PASS` remain invariants.

## Required surfaces

A producer result identifies:

- the registered producer implementation and immutable producer revision;
- the assurance proposition/evidence contract and evidence requirement IDs being served;
- immutable normative/implementation/deployment/runtime/configuration source pins as applicable;
- execution identity, runner, time, determinism and local execution status;
- evidence status/class, integrity-bearing artifacts and raw/bounded observations;
- a claim boundary describing supported propositions, unsupported inference, limitations and residual uncertainty;
- the source pins against which the result is fresh plus machine-readable invalidation keys.

## Fail-closed states

`execution.status` and `evidence.status` are deliberately separate. A process may execute successfully while producing `not-tested` or `evidence-incomplete` evidence. Conversely, a failed or unavailable execution does not become assurance failure automatically; it becomes evidence for the relevant specialist/RAHP reconciliation path.

The portable evidence states are:

- `observed`
- `not-tested`
- `evidence-incomplete`
- `failed`

Observed evidence requires integrity-bearing artifacts with producer provenance. Source-pin mismatch makes the evidence stale for a requested target revision.

## Domain-specific observations

The `observations` array is intentionally structurally open. RAHP validates the generic envelope and attribution boundary but does not interpret target- or specialist-specific observation fields. Producers and specialist contracts may define nested observation schemas independently.

This allows, for example, an Interop Lab producer to emit DPIP-defined privacy observations without RAHP learning `observer`, `surfaces`, OpenVTC, VDC/VAC or other target vocabulary.

## Migration and compatibility

The existing registered Interop producer currently emits `interop-evidence-bundle/v1`. That path remains supported until a producer has been migrated to `rahp-evidence-producer-result/v1` with characterization/equivalence evidence.

Migration should proceed one producer at a time:

```text
characterize current bundle + failure semantics
        ↓
emit portable RAHP envelope around the same bounded observations
        ↓
validate producer identity / pins / artifacts / claim boundary
        ↓
compare specialist interpretation and reconciliation
        ↓
only then retire the compatibility path
```

The contract is portable only if its generic meaning remains unchanged when the implementation target or specialist changes.
