---
layout: default
title: "Using RAHP with external agents"
parent: Learn RAHP
nav_order: 4
has_toc: true
permalink: /docs/reasoning-integration/
---
# Integrating RAHP with an external agentic system

RAHP is **agent-independent**, not agent-incompatible. An external agent may orchestrate an existing RAHP examination, but it does not thereby become the authority for an assurance conclusion.

This is a **tool invocation pattern**, not a claim of a shipped universal agent protocol, SDK, or tested integration with every agent framework.

## Minimum integration contract

| Boundary | Caller provides or performs | RAHP/evidence consumer must verify |
| --- | --- | --- |
| Subject and scope | Explicit proposition, assessment target, version/source pins | Subject matches the permitted assessment scope |
| Evidence | Source/evidence references, provenance, freshness where applicable | Evidence is available, attributable, relevant, and sufficient for the bounded proposition |
| Invocation | Executes a maintained RAHP entry point; captures exit status and output | Execution success is recorded separately from assurance state |
| Assessment result | Preserves output bytes and references; no fabricated PASS | Validate [portable assessor-result v1](assessor-result-contract.md) when a specialist result is produced |
| Explanation | May attach [optional reasoning trace](reasoning-trace.md) | Explicitly validate the trace; do not confuse structural validity with truth |
| Terminalization | Submits eligible results to a compatible controller | Only the controller applies terminal-state rules |
| Governance | Routes unresolved issues to authorized reviewer | Reviewer authority, correction and supersession remain explicit |

**Do not** transform an agent's confidence score, a green tool result, or a schema-valid artifact into a terminal PASS.

## Same examination, two callers

### Human or CI

From a checkout with dependencies installed:

```bash
python3 examples/standalone-trqp/replay.py --check
python3 -m unittest tests.test_trqp_reasoning_trace -v
```

This verifies the retained source replay and its bounded trace fixture. It is **not** a complete deployed-system assurance assessment.

### External agent

A compatible agent may invoke **the same commands** as a subprocess/tool action, capture the exit code and unmodified outputs, and attach the pinned artifacts to its task record. A tool adapter must set working directory, execution permissions, timeouts and resource limits according to the host's security policy. The following is *illustrative pseudocode*, not a new RAHP agent API:

```text
task = receive_authorized_task()
assert task.scope permits "TRQP source-example replay"
execution = run_approved_tool("python3 examples/standalone-trqp/replay.py --check")
record(execution.exit_status, execution.stdout, execution.stderr, source_pins)
if execution.exit_status != 0:
    return "execution failed / evidence unavailable; no assurance PASS"
trace = load_retained("examples/standalone-trqp/reasoning-trace-f002.json")
validate_trace(trace, bounded_assessor_result)
return evidence_and_bounded_finding_for_review
```

The pseudocode's `bounded_assessor_result` represents a compatible, separately produced assessment record. **The standalone replay does not itself emit a portable specialist result or terminal controller disposition.** A production adapter must not invent either artifact.

## Failure and adversarial cases

- **Missing evidence:** mark it unavailable or indeterminate; do not invent observations.
- **Conflicting evidence:** preserve both observations and route to review; do not silently choose a favorable one.
- **Stale evidence:** require freshness evaluation for the relevant subject; the optional trace profile does not implement freshness enforcement.
- **Untrusted tool output or prompt injection:** treat retrieved text as data, not instructions changing authority or policy.
- **Agent replacement or retries:** retain source pins, execution evidence, assessor result, and review history independently of agent memory.
- **Reviewer disagreement:** preserve the disagreement and its authority basis; the current optional trace profile does not implement adjudication or supersession.

## Integration acceptance checks

1. A standalone run works with no agent or LLM dependency.
2. An external caller can invoke the same replay without changing its meaning.
3. A nonzero exit status cannot be presented as successful assurance.
4. The portable assessor result is validated separately from any optional trace.
5. A reviewer can distinguish source observation, bounded inference, controller disposition, and authorized governance decision.

See [reasoning architecture](reasoning-architecture.md) for code ownership and [the TRQP worked example](../examples/standalone-trqp/README.md) for executable evidence.
