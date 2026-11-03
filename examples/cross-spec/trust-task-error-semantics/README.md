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

## Source and implementation evidence (reconciled 2026-11-03)

- [Trust Tasks TF PR #575](https://github.com/trustoverip/dtgwg-trust-tasks-tf/pull/575) **merged on 2026-09-22** (`dc99f54b766df3264db8ed7489fc40d70ef12102`). Rust code generation can expose each specification's declared error codes; generated vocabulary alone is not observed semantic conformance.
- [OpenVTC/VTI #1600](https://github.com/OpenVTC/verifiable-trust-infrastructure/issues/1600) **closed on 2026-10-18**. Current VTI source contains derived error-code census modules at `vtc-service/src/trust_tasks/error_code_census.rs` and `vta-service/src/trust_tasks/error_code_census.rs`. These require witnessing tests for declared errors or an explicit, bounded *unwitnessed* baseline. A census with nonzero unwitnessed coverage is not proof that every error has an executable witness.
- **The RAHP fixture here remains synthetic and deliberately bounded.** Its positive example is illustrative, not an independently executed VTI response; the source/implementation changes above do not upgrade it to a runtime or composition PASS.

## What still needs independent assurance

For one assurance-relevant task and its **exact normative revision**, capture a real target-native rejected response and its structured extended code and retryability, tied to the target source/command/test. Compare this observation against the governing declaration, then mutate the observed code to `taskFailed` or reverse retryability and prove the qualification changes to `SEMANTIC_LOSS`. Preserve the source of the observation separately from the synthetic mutation.

If the native census already witnesses the precise case and the consumer contract is unambiguous, cite that test rather than introduce a redundant runtime harness. For cross-component fidelity, test the *actual consumer* instead; a producer witness does not prove that a relying component retains the distinction.

No additional code or expanded vocabulary is warranted until that case identifies a falsifiable coverage gap. Upstream source authority, downstream RAHP qualification and independent execution remain distinct.
