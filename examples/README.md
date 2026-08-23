# RAHP worked examples

Worked examples demonstrate the portable RAHP method against independently governed targets. They are evidence and regression assets; they do not define portable RAHP semantics.

## Canonical maintained-example policy

From RAHP v1.5.0 onward, a **canonical maintained example** is expected to run on the current stable RAHP release.

The invariant is:

```text
canonical maintained example -> current stable RAHP v1.5.x
historical/versioned evidence -> original RAHP version preserved
```

For maintained pressure tests, the canonical `pressure-test.yaml` therefore records the current RAHP baseline directly. Older assessment provenance is not silently rewritten or discarded: each migrated example has a `history/pre-v1.5.yaml` pointer that records the original RAHP version and exact Git blob SHA, while Git history retains the full prior content.

`examples/current-baselines.yaml` is the machine-readable index for the current maintained pressure-test set. It records:

- the stable RAHP release used by canonical examples;
- target and companion revision pins;
- evidence freshness;
- normalized residual posture;
- prior assessment baseline;
- assurance delta and finding lineage.

The registry **indexes and validates current examples; it is not a substitute for updating them**.

## Baseline lifecycle

```text
historical assessment
  -> preserve exact prior blob identity
  -> evidence freshness evaluation
  -> v1.5 reassessment/revalidation
  -> canonical current pressure-test.yaml
  -> explicit assurance delta + finding lineage
  -> current residual posture + policy gate
  -> governed disposition or further review
```

A finding may remain unchanged across toolkit releases. Rebaselining does not imply remediation. Likewise, zero findings does not imply `assured`; unresolved evidence gaps or review obligations remain visible in current posture.

## Maintained examples on v1.5.0

The canonical v1.5 pressure-test examples currently include:

- CAWG/C2PA portfolio composition;
- DTG Trust Tasks × Credential Specification;
- DTG Credential Specification × ZKP;
- DTG Trust Tasks × ZKP.

Each canonical record directly declares `reviewed_against.rahp_version: v1.5.0` and includes v1.5 evidence-lineage and assurance-posture fields.

## Exploratory cross-spec examples

Exploratory examples can apply the same portable RAHP method before they have the source pinning, maintainer disposition and regression obligations required for the canonical maintained-example registry.

- [`cross-spec/guardianship-fiduciary/`](./cross-spec/guardianship-fiduciary/) pressure-tests guardianship, fiduciary and other constrained-authority relationships across credential, transaction, privacy/proof and governance surfaces. It uses DTG as a worked instance, starts from explicit discussion hypotheses, and keeps downstream issue creation gated on source-pinned evidence and maintainer disposition.

Exploratory examples are intentionally **not** added to `current-baselines.yaml` merely because they exist. Promotion requires the evidence and maintenance commitments described by the canonical policy above.

## Maintainer-feedback resilience exemplar

`examples/resilience/openvtc-cypress/` is maintained as a different kind of example: it demonstrates how DRARM evidence is dispositioned after a target maintainer supplies counter-evidence, sharper implementation evidence, ownership information, and remediation records.

Its machine-readable `maintainer-disposition.yaml` intentionally includes multiple transition types:

- a finding weakened and narrowed;
- a detector-backed finding weakened to `review-required` after a credible architectural rationale;
- findings strengthened by maintainer investigation;
- a review gap promoted when stronger evidence appears;
- a distinct review gap retained rather than incorrectly merged into another failure mode.

The example also demonstrates a critical method rule: a documented rationale may justify additional review, but **does not itself produce `controlled` or `assured`**. Executable evidence remains necessary.

ARPA remains in the reassessment queue where refreshed target/runtime evidence is required before a current executable assessment can be asserted safely.

## Validation

The validation boundary checks that:

- the registry declares RAHP v1.5.0 as current;
- every canonical maintained pressure-test example exists and itself declares RAHP v1.5.0;
- every canonical maintained pressure-test example carries explicit lineage and current assurance posture;
- historical provenance pointers exist for migrated pre-v1.5 examples;
- normalized residual states are valid;
- prior-baseline lineage and assurance deltas are explicit;
- rendered sibling README blocks remain synchronized with canonical YAML;
- the OpenVTC resilience exemplar retains its machine-readable maintainer-feedback transitions and review-only queue override;
- deployment-specific example semantics remain outside the portable method and engine contract.

Run:

```bash
python3 tools/validate_v15_release.py
python3 tools/validate_current_examples.py
python3 tools/validate_resilience.py
python3 tools/validate_pressure_tests.py
```
