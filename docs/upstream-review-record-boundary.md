# Upstream RAHP review-record interoperability boundary

Tracking: ToIP RAHP Task Force convergence issue #17, Increment 6.

## Authoritative inputs

Accepted upstream RAHP revision: `448e2ff4ca7f747ca899e0e845adfe45f750f094`. Canonical schema: `review/spec-review.schema.json` (`rahp-spec-review/v1`); canonical validator: `review/validate_spec_review.py`; vocabulary authority: `method/vocabularies.yaml`. The accepted TRQP and VRC baseline/reassessed YAML reviews are the examined input cases.

Downstream RAHP Toolkit revision at preparation: `5bbe4ad3bddc692f582eccf92689eba69604e1d7`. Downstream's `tools/review.py` pressure-test, security and combined-review records are *different* record families; downstream assurance-controller terminal statuses are not equivalent to upstream finding statuses. No automatic translation or method/schema migration is authorized by this experiment.

## Executable claim and challenges

In CI, the existing validation workflow obtains the immutable upstream checkout and runs:

```sh
python3 -m unittest discover -s tests -p 'test_upstream_review_boundary.py' -v
python3 tools/upstream_review_boundary.py --upstream upstream-review-compat --output report.json
```

For each of the retained TRQP, VRC baseline and VRC reassessment reviews, the test requires original acceptance, and rejection of five mutations:

- mutable target revision replacing the 40-character Git pin;
- unknown risk reference (using the selected upstream risk corpus);
- duplicate finding identifier;
- downstream-style `PASS` substituted for upstream finding status;
- added ungoverned `evidence` member to a finding.

All altered records are written to a temporary file; upstream fixtures remain intact. The executable result is bounded **schema/vocabulary/reference validation evidence**, not evidence sufficiency or assurance of the examined specification.

## Semantic crosswalk and non-mappings

| Concern | Upstream RAHP | Downstream Toolkit | Disposition |
| --- | --- | --- | --- |
| Review target identity | `target.repository`, immutable 40-char `target.revision` | Review initiation includes target repository/version/commit | Conceptually alignable; no general conversion proven |
| Finding identity | `F-nnn`, unique per review | Pressure-test and other assessment findings have own records | Related purpose, **not** ID equivalence |
| Risk link | `RK-*` resolved against explicitly selected corpus | Generic and instance/catalogue reference families coexist | Requires explicit mapping and authority; **not** automatic |
| Finding status | `open`, `in_progress`, `resolved`, `risk_accepted`, `out_of_scope`, `superseded` | Independent review modes and terminal controller outcomes | Distinct lifecycle/decision semantics; never map `PASS` to upstream review status |
| Evidence | TRQP/VRC example-local sidecars, reviewed interpretation separate | Producer/assessor results, provenance and terminal reconciliation | No shared evidence schema established |
| Reassessment | VRC `SR-201` and `SR-202` bound to distinct immutable revisions; prior findings retained | Broader materiality/freshness/invalidation mechanisms | Historical correspondence, **not** controller-state parity |

## Limitations and architectural disposition

This tranche **does not** perform a lossless conversion into downstream pressure-test/combined review formats, nor verify generic downstream evidence consumers. Conflating those contracts would produce an unjustified assurance claim. A later Increment 6 slice should examine an explicit, reviewed mapping proposal (if actual consumer needs exist) and separate reassessment/evidence lineage behavior. Existing upstream examples are accepted method instances; their example-local sidecars have not been promoted to a normative envelope.

The comparison is deterministic, the validator itself owns acceptance, and CI retains the machine-readable case matrix. Missing upstream fixtures fail closed. Source identities are Git pins, not claims of external source authenticity. AI-assisted preparation; independent reviewability APPLICABLE, with reproducible commands, boundaries, negative tests and limitations recorded.
