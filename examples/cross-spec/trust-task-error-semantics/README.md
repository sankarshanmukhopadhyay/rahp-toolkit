# Trust Task error-semantic assurance

Issue #691 records an assurance gap exposed by upstream Trust Tasks TF #575: a task implementation can return a generic failure while losing the specification-declared error distinction, and ordinary build/conformance gates may still remain green.

## Assurance boundary

This work does not define new Trust Task error codes and does not make generated bindings authoritative. The governing specification remains authoritative.

The downstream assurance proposition is narrower:

> If a declared extended error changes lifecycle interpretation, retryability, redress, or a relying component's next action, the observed implementation outcome must preserve that declared semantic distinction.

## Evidence model

The fixture covers four distinct states:

- SEMANTIC_MATCH: observed extended code and retryability match the declaration;
- SEMANTIC_LOSS: a declared distinction is collapsed or retryability changes;
- UNKNOWN_SPEC: the Type URI is not known, so an empty declaration cannot be inferred;
- NOT_APPLICABLE: the Type URI is known and the governing specification declares no extended codes.

This distinction prevents "unknown task" from being treated as "known task with no extended errors."

## Running

Use:

python tools/validate_trust_task_error_semantics.py

The regression suite also imports the evaluator directly.

## Relationship to contestability

Exact error semantics can be part of adverse-decision reconstruction, but an error message is not itself redress. RAHP #610 retains the cross-boundary contestability proposition. This fixture only ensures that a consuming system is not deprived of a distinction the governing task specification actually declared.

## External dependency

Upstream Trust Tasks TF #575 is still an external implementation dependency. If it changes or does not merge, the assurance proposition remains valid while the particular binding mechanism may change. A downstream PASS must come from observed semantic fidelity, not from the existence of generated constants.
