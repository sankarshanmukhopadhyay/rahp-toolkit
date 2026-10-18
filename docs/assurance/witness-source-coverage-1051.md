# VTA witness: attributable source-test inventory and evidence limits

**Owner:** [#1051](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1051). **Source:** [OpenVTC VTI PR #2123](https://github.com/OpenVTC/verifiable-trust-infrastructure/pull/2123), exact revision `e9c5f9342e97ebc0a15ab53170d9692f5d2ad768`. Machine-readable source test inventory: [witness-source-coverage-1051.json](../../data/assurance/witness-source-coverage-1051.json).

## Executable, bounded source validation

```bash
python3 -m unittest tests.test_witness_source_coverage -v
python3 tools/validate_witness_source_coverage.py
python3 tools/validate_witness_source_coverage.py --fetch-source
```

The first two commands are deterministic offline regressions for source declarations and evidence status. The last one independently retrieves both VTI `witness_tests.rs` and its parent module at the exact git revision, checks all ten expected async-test declarations and verifies the Rust module includes `#[path = "witness_tests.rs"] mod tests;`. Retrieval failure or source drift is a nonzero result. Without `--fetch-source`, the manifest-only check is **not evidence that the remote source was independently acquired**.

At [VTI CI run 38756165903](https://github.com/OpenVTC/verifiable-trust-infrastructure/actions/runs/38756165903), workspace nextest job 116495482783 reported **6,063 passed, 23 skipped**. That aggregate run, even coupled with the source-module linkage, does not enumerate execution of these exact ten test functions individually. Consequently the attached machine-readable evidence state is `source-assertions-only`, deliberately not `PASS`. Individual attribution requires a separately captured list and test run from the pinned source:

```bash
cargo nextest list -p vta-service --lib
cargo nextest run -p vta-service -E 'test(trust_tasks::witness::tests)'
```

Record the actual toolchain/features/test identities and timestamps; these commands are **reproduction instructions**, not a claimed execution result.

## Original propositions and negative cases

The ten source test names distinguish the accepted open–present–accept relationship flow; a relationship DID named in membership; repeated present/used challenge; wrong-session witness answer; other-session VWC; unknown context/state indistinguishable errors; cross-context key ownership; `WitnessRequest` versus generic `Sign`; refused missing or mismatched credentials before disclosure; and a credential altered between open and present. The exact names and descriptions are in the JSON manifest. They are implementation-unit assertions, not yet independently exercised client-carrier and deployed-audit proof.

## Residual gates

**Still INDETERMINATE:** external client forwarding of the generated documents without origin-confusion or substitution, real deployment revocation/rollback, retained identifiers and event/audit content, cross-context linkability and any warranted DPIP privacy referral. No new RAHP protocol semantic is proposed. The next validation should compose an actual caller, VTA and witness and retain source-pinned traces, or transfer that obligation to a precisely scoped runtime owner; do not treat a passing schema or source test as conformance.
