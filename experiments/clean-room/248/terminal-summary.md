# True clean-room Dogwood assessment #248 — terminal conclusion

## Bottom line

**AMBER — INDETERMINATE.** The new clean-room lineage successfully took pinned Dogwood RC-1 through fresh intake, real evidence production, semantic RAHP review, privacy materiality, a fresh DPIP examination, DPIP return, and RAHP reconciliation. The run did not justify GREEN because a bounded security/accountability residual remains and the Dogwood-native privacy experiment is semantically misclassified. It did not justify RED because the fresh evidence did not establish target-created cross-context correlation or a whole-target security/privacy failure.

## What was assessed

- Target: `OpenVTC/verifiable-trust-infrastructure`
- Release: `VTI-Dogwood-RC-1`
- Immutable commit: `cb01d0a758863fb3a02f9f4eef2c4f15f56c4c3b`
- Fresh lineage: `dogwood-clean-room-248-33296944093`
- Fresh workflow run: `33296944093`
- No historical Dogwood assessment evidence or conclusions were used as inputs.

## What evidence was actually produced

All four required runtime observations were attempted and satisfied in the fresh lineage:

- `ER-REL-DID-AB` — Dogwood-native, `EXECUTED / SATISFIED`.
- `ER-VERIFIER-AB` — Dogwood-native, `EXECUTED / SATISFIED`.
- `ER-STATUS-AB` — Interop composition, `EXECUTED / SATISFIED`.
- `ER-TASK-AB` — Interop composition, `EXECUTED / SATISFIED`.

Artifact: `dogwood-true-clean-room-248-33296944093`, ID `9727752013`, digest `sha256:de6418c317c934f10b64036288fd7462af822a85c4f45fe8c172f8af86d761e5`.

The composition pressure suite behaved coherently: its positive control detected a seeded join, its context-distinct pressure case detected no join, and its falsification vector detected a deliberately introduced status-handle join. Those status/policy and Trust Task observations remain explicitly composition-attributed.

## What we found

The pinned target itself documents partial durable-audit coverage. Several high-value state-mutating operations are not written to the durable audit trail, and audit-write failures can be silently swallowed. That is a bounded security/accountability concern, not proof that the whole target is insecure.

Privacy is independently material because the target architecture makes privacy a gating constraint and relies on selective disclosure and unlinkability behaviour.

The fresh Dogwood-native A/B evidence then exposed a test-producer semantics defect: the manifest deliberately reuses the same client DID across A and B to anchor the same underlying relationship, but the emitted capture labels the run as an unlinkability-pressure case where a join must not emerge and records the identical binder origin as unknown. A deliberately reused same-relationship identifier cannot simultaneously be treated as an unexpected target-created correlator.

Fresh DPIP #135 therefore completed as **INDETERMINATE / evidence-classification-required**. This is not an evidence-production failure: the observations exist. The unresolved issue is how the native experiment is typed and attributed.

## Why AMBER

**Not GREEN:** the target has a documented audit residual, and the Dogwood-native privacy evidence cannot support a target-level PASS until the experiment role/correlator origin is corrected.

**Not RED:** the fresh run did not demonstrate target-created cross-context correlation. The context-distinct composition pressure case was favourable, and the documented audit gap is bounded rather than a whole-target failure.

## What remains unknown

The main unresolved question is whether a correctly constructed **Dogwood-native context-distinct** A/B experiment produces an unintended stable correlator. The current native package cannot answer that because its same-DID control is mis-typed.

## References

- RAHP #248: https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/248
- Fresh run: https://github.com/sankarshanmukhopadhyay/rahp-toolkit/actions/runs/33296944093
- Fresh DPIP #135: https://github.com/sankarshanmukhopadhyay/dtg-privacy-implementation-profile/issues/135
- Producer defect Interop #69: https://github.com/sankarshanmukhopadhyay/trust-protocol-interop-lab/issues/69
- Dogwood RC-1: https://github.com/OpenVTC/verifiable-trust-infrastructure/releases/tag/VTI-Dogwood-RC-1

## Recommended next step

Fix **Interop Lab #69** so the Dogwood-native same-relationship run is explicitly a positive control with fixture-supplied correlator origin, and add a separate context-distinct native pressure case if supported. Then create a **new** pinned Dogwood privacy examination. Do not mutate this completed clean-room assessment or DPIP #135.
