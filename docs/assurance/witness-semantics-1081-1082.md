# Witness role, identity and lifecycle assurance

**Owners:** [#1081](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1081) and [#1082](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1082).  
**Machine-readable contract:** [`witness-semantics-1081-1082.json`](../../data/assurance/witness-semantics-1081-1082.json).

This is a downstream RAHP assurance record. It assesses pinned DTG witness semantics; it does **not** define DTG witness authority, relying-party policy, or privacy conclusions.

## Pinned authoritative sources

| Source | Revision | Role in this assessment |
|---|---|---|
| [`trustoverip/dtgwg-vsc-registry`](https://github.com/trustoverip/dtgwg-vsc-registry) | `7b30c7567581686ce77243856088a865b465cfe3` | Normative `witnessed/1` predicate and profile. |
| [`trustoverip/dtgwg-trust-tasks-tf`](https://github.com/trustoverip/dtgwg-trust-tasks-tf) | `696783ede3e8aa74abb361b16465b7cad1b90ba3` | `witness/session/0.2` and `witness/session/submit/0.2` ceremony and outcome-evidence contract. |
| [`trustoverip/dtgwg-cred-spec`](https://github.com/trustoverip/dtgwg-cred-spec) | `2e3c5beffb6de1a90c3e8dd3eae472d90afd336c` | Credential model and governance boundary for VWC/predicate handling. |

The registry profile states that a VWC is bound to a specific trust-task exchange, that the witness issuer scope is `directed` at minimum, and that the VWC does not establish that the referenced credential is currently valid or unrevoked. The Trust Tasks 0.2 session/submit pair makes the witness the session recipient, requires proof on the witness response, and describes the verifier pairing rule between response issuer and VWC issuer. Those source constraints are the basis for the mechanical cases below.

The discussion-derived refinements in #1081 and #1082 are treated as assurance propositions. Where those discussions go beyond the currently pinned normative sources, this record preserves the result as contextual, policy-dependent, or `INDETERMINATE` rather than manufacturing downstream DTG semantics.

## Executable validation

```bash
python3 -m unittest tests.test_witness_semantics -v
python3 tools/validate_witness_semantics.py
```

The validator evaluates 24 source-pinned positive, negative and indeterminate cases. Its output is evidence that the downstream case contract is internally coherent. It is **not** runtime conformance evidence for a particular witness deployment.

## #1081 role and identity propositions

### WIT-ROLE-001: non-participation is not organizational independence

The harness fails a witness that is itself a party to the witnessed event. It does not fail a community-governed witness merely because it is affiliated with the community. If relying policy additionally requires organizational independence, the decision becomes evidence-dependent.

This preserves the visible judgment from #1081:

> “Witness is not a party to the event” is an assurance invariant. “Witness is independent enough for this relying decision” is a contextual trust-policy conclusion.

### WIT-ROLE-002: independence is not self-proving

A self-description such as `independent` never satisfies a policy that requires external independence evidence. Without external evidence, the result remains `INDETERMINATE`.

### WIT-ID-001: ceremony identity continuity

Where the pinned task/profile contract requires continuity, the VWC issuer, session recipient and response signer must identify the same witness. Divergence is `FAIL`; a missing identity leg is `INDETERMINATE`.

### WIT-ID-002: continuity is not cross-role identity collapse

The harness separately records whether the witnessing identity is reused as an unrelated durable operational identifier. A continuous ceremony identity does not establish organizational independence. Identifier reuse and correlation remain a separate control surface.

Privacy conclusions about mediator choice, DID-log hosting, membership gating, retained attestation records, status-query traffic or cross-role correlation remain owned by [#338](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/338)/DPIP.

## #1082 temporal and lifecycle propositions

### WIT-TIME-001: VRC and VWC state do not cascade implicitly

Two explicit regression vectors are included:

- **N1:** a VRC is valid when witnessed and later revoked; the historical VWC is not automatically mutated solely because the VRC changes.
- **N2:** a VWC is revoked or withdrawn while the VRC remains otherwise valid; the VRC is not silently revoked by the VWC state.

Applying an implicit cascade is a mechanical `FAIL`.

### WIT-REV-001: revocation reason semantics remain bounded

When the available status representation distinguishes attestation invalidation from reliance withdrawal, the harness checks that the interpretation matches that reason. When the representation is undifferentiated, an attempt to infer that the historical event was false remains `INDETERMINATE`.

### WIT-KEY-001: historical authorization is not non-compromise proof

A key authorized at issuance time plus a later-discovered compromise with unknown onset remains `INDETERMINATE`. The harness deliberately prevents historical DID/key authorization from being promoted to proof that the key was uncompromised at issuance.

### WIT-AVAIL-001: unavailable is not VALID or REVOKED

Temporary outage and witness retirement are represented as distinct witness states, but unavailable status evidence produces `INDETERMINATE` in both cases. The validator never maps absence of status evidence to VALID, REVOKED or PASS.

### WIT-SUCC-001: hosting succession is not mutation authority

A successor may host frozen evidence without acquiring authority to mutate predecessor status. An attempted mutation with explicitly absent authority is `FAIL`; unknown authority remains `INDETERMINATE`.

### WIT-RET-001: minimal retention is an evidence boundary

The pinned Trust Tasks source requires discarding inbound presentations after their function is discharged. The assurance case therefore treats a retained digest/attestation record as insufficient to reconstruct a discarded original presentation. Claiming reconstruction from the digest alone is `FAIL`.

## Short-validity versus online-status strategies

The machine-readable record compares two lifecycle strategies without declaring them assurance-equivalent:

| Strategy | Immediate withdrawal | Availability dependency | Important limitation |
|---|---|---|---|
| Short validity, no online status | No | Clock/expiry evidence | Risk is time-bounded but cannot be withdrawn immediately. |
| Online status | Yes, when available and authorized | Status evidence availability | Adds availability and status-query surfaces; privacy conclusions route to #338/DPIP. |

This comparison is descriptive. RAHP does not choose a universal strategy for DTG.

## Evidence limits and retest conditions

This tranche establishes **mechanically reviewable, source-pinned cases**, not deployment conformance. Runtime/operator control, effective organizational independence, compromise onset, successor authority and actual status availability remain evidence-dependent.

Re-run or revise this record when any of the following materially changes:

1. `witnessed/1` predicate/profile semantics;
2. `witness/session` or `witness/session/submit` beyond the pinned 0.2 contract;
3. DTG credential status/revocation semantics relevant to VWCs;
4. upstream clarification of witness independence, revocation reason semantics, witness retirement, or successor authority;
5. #338/DPIP produces privacy evidence that changes the correlation boundary.

## Independent reviewability

**APPLICABLE.** A reviewer can inspect the exact source commits, run the two commands above, examine every positive/negative/indeterminate vector in the JSON contract, and challenge the evaluator rules without privileged maintainer context.

The remaining limitation is explicit: this is a downstream assurance harness over upstream semantics. It does not claim to be upstream authority or a substitute for deployment evidence.
