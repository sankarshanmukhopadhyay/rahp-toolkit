# Reviewer architecture and trust boundaries

## Purpose

This note gives an independent reviewer a compact map of what RAHP owns, what it consumes, and where confidence must stop.

## Execution chain

```text
subject + immutable source identity
  -> gather / subject model
  -> materiality
  -> bounded proposition assessment
  -> evidence classification
  -> specialist routing where required
  -> specialist result / evidence return
  -> reconciliation
  -> residual + action
  -> terminal assurance record
```

The controller owns supported lifecycle state and terminalization. GitHub Actions, CLI completion and repository permissions do not own assurance state.

## Authority boundaries

**RAHP core owns:** portable lifecycle semantics; proposition/evidence contracts; evidence-conservative inference boundaries; normalized findings/results; reconciliation; source-pinned lineage; and terminal assurance semantics for supported flows.

**Deployment profiles own:** the subject configuration, deployment-specific corpora, local governance inputs, local evidence, and local dispositions. A bundled exemplar does not become a dependency of the portable core.

**Specialists own bounded specialist questions.** DPIP is the qualified privacy specialist used by current flows. A specialist result crosses the boundary through a versioned contract; RAHP must not silently reinterpret an unavailable or indeterminate specialist result into PASS.

**Evidence producers own observations, not conclusions.** The Trust Protocol Interop Lab can produce attributable execution/composition evidence. Its workflow success does not confer RAHP assurance and it is not folded into RAHP authority.

**External normative sources remain external authorities.** For example, VTI remains the normative/conformance authority for VTI. RAHP can assess evidence against a pinned VTI state; it does not become the source of VTI semantics.

**Governance authority is separate from evaluation.** A PASS policy result does not grant publication, closure, risk-acceptance or other governance authority.

## Evidence trust boundaries

RAHP distinguishes normative/static source evidence, synthetic/fixture evidence, executable conformance evidence, runtime observations and governance evidence. One class cannot silently satisfy a proposition requiring another.

Consequential evidence should identify provenance, source/revision, production mechanism, observation time, integrity where applicable, authority class and supported proposition. A manifest makes provenance inspectable; it does not prove sufficiency.

## Source and time boundaries

Assessments are pinned to an immutable revision or source identity. Replay against the same immutable state is expected to be idempotent. A materially new pin creates reassessment lineage. Freshness can become potentially-stale, stale, retest-required, superseded or indeterminate without asserting that the underlying system has failed.

## Composition boundary

Component validity is not composition validity. Composition assessment must separately examine cross-component assumptions, authority/lifecycle interaction, privacy/correlation, substitution, redress, weakest-link behaviour and evidence continuity.

## Critical non-equivalences

- workflow success != assurance success
- zero findings != PASS
- identity != authority
- discovery != recognition
- recognition != authorization
- component PASS != composition PASS
- protocol completion != semantic completion
- multiplicity != independence
- normative convergence != implementation conformance
- repository permission != governance authority

## High-value reviewer attack surfaces

The highest-value challenges are: missing or stale evidence promoted to PASS; wrong-subject or wrong-pin evidence accepted; duplicate sources treated as independent; malformed specialist returns; incomplete execution presented as terminal assurance; component evidence promoted to composition assurance; and external normative text silently reinterpreted by local machinery.
