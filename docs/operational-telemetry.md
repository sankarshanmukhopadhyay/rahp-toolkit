---
layout: default
title: Operational telemetry and observability
parent: Operate assurance
nav_order: 8
---
# Operational telemetry and observability

RAHP emits **operational telemetry**, not a second assurance result.

The telemetry contract exists to answer questions such as: what ran, how much scope was selected, how long it took, what remained blocked, and whether materiality-bounded execution is actually reducing unnecessary work over time. It must never answer the target assurance question by itself.

## Contract

Operational events use `rahp-execution-telemetry/v1`.

A telemetry event contains:

- operation and run identity;
- elapsed execution time;
- an explicitly whitelisted low-sensitivity context such as profile, plan or source revision;
- scalar operational metrics such as available/selected/skipped counts;
- an explicit authority boundary declaring that the event is not assurance evidence and may not set an assurance outcome.

Arbitrary nested payloads are rejected so credentials, findings, evidence bodies, secrets or user content are not accidentally copied into telemetry.

## Assurance boundary

Telemetry can establish that a controller executed a path, selected a scope, encountered a blocker or consumed time. It cannot establish that the assessed system is safe, conformant, private, authorized or otherwise deserving of PASS.

The following remain invalid inferences:

- workflow success -> assurance PASS;
- fast execution -> assurance quality;
- zero operational errors -> no assurance residuals;
- selected scope -> complete coverage unless the materiality model itself supports that conclusion;
- missing telemetry -> target assurance failure.

Operational telemetry failure should be diagnosed as an observability problem. It must not silently rewrite a valid assurance result.

## Materiality-bounded selection

The cross-specification planner can write a telemetry sidecar containing the count of runnable compositions, selected compositions and skipped compositions for the chosen plan. This makes selection behavior inspectable without changing the selected set or its assurance semantics.

## Lifecycle diagnostics

The telemetry helper can summarize an assessment lifecycle into transition count, terminal/non-terminal state, explicit terminal outcome when one actually exists, blocking reason code and resilience disposition. It deliberately refuses to infer a terminal outcome from an intermediate state.

## Privacy and minimization

Only an approved context field set is recordable. Do not add raw evidence, credentials, prompts, policy bodies, repository tokens, personal identifiers or arbitrary operator text to telemetry. If a future operational metric requires richer data, define a new versioned low-sensitivity field rather than bypassing the contract.

## Performance relationship

Benchmark output embeds the same authority boundary. Performance evidence is useful for engineering and capacity planning; it is not assurance evidence about the subject under assessment.

See [Performance and execution efficiency](performance.md).
