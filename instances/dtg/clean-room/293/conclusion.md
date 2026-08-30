# Canonical DTG portfolio clean-room conclusion — RAHP #293

**Run:** `dtg-canonical-clean-room-293-faed4f07`  
**Portfolio registry:** `sankarshanmukhopadhyay/dtg-portfolio-monitor@faed4f076b647dde16b016cf14a74aed72497f72`  
**Overall portfolio state:** **AMBER**

## Executive conclusion

A technically competent implementer **can build a coherent DTG composite from the current canonical specifications and reference implementations**, but should not treat the portfolio as a uniformly finished, plug-compatible or fully privacy-proven stack.

The strongest current result is architectural: the canonical Trust Tasks, Credentials and ZKP work now contain several important boundaries that prevent common over-claims. Task lifecycle is explicit; cryptographic validity is separated from authorization; PHC qualification is governance-owned; scoped uniqueness is not global uniqueness; relationship completion is not equated with a single published VRC; and the VTI reference implementation contains concrete lifecycle and exact-task-consent protections.

The portfolio is nevertheless **AMBER** because material composition obligations remain unresolved or unproven:

1. the current OpenVTC DTG Credentials library has a documented VWC digest incompatibility with Working Draft 01;
2. current member-issued VMC withdrawal/status discovery remains a normative composition dependency;
3. fresh #293 runtime privacy evidence is absent, so DPIP correctly returned `INDETERMINATE / evidence-required`;
4. cross-transport equivalence is not freshly demonstrated and TSP remains experimental in the pinned VTI source;
5. some named portfolio workstreams are not yet mature normative deliverables;
6. no single current cross-portfolio correction/redress contract was established.

These are **bounded, typed obligations**, not reasons to modify RAHP core.

## What an implementer may rely on today

### Strongest current specification-level foundations

- **Trust Tasks:** use the canonical framework for task identity, request/response/error/continuation semantics, duplicate handling, lifecycle state and evidence citation. Do not substitute transport acknowledgements or silence for task state.
- **DTG Core Credentials:** treat proof validity, validity windows, issuer authorization, digest/context binding and governance authority as separate checks.
- **Personhood:** treat PHC as a governance-qualified claim. A credential type, VP or ZK proof alone does not establish global personhood or uniqueness.
- **ZKP:** use scoped/contextual uniqueness only for the exact action/scope/epoch it proves. Do not promote a nullifier result into global one-person assurance.
- **VTI relationship graph:** a single VRC is a half-edge. Mutual/in-force relationship state depends on reciprocal current halves and lifecycle precedence.
- **Task consent:** where the VTI DTTE mechanism is used, approval is bound to the exact act and rechecked against current policy/enrolment/state before execution.

## What must not be assumed

- multiplicity of DIDs, issuers, credentials, witnesses or evidence paths means independence;
- ZKP verification means the biometric/personhood determination was correct;
- scoped nullifier uniqueness means one natural person globally;
- a valid credential means the issuer is currently authorized or the credential/current consent is still in force;
- a matching two-sided VMC pair proves the member acknowledgement has not since been withdrawn;
- a single published VRC is a mutual current relationship;
- Trust Task schema validity means the enclosing composition is safe;
- a successful HTTP/DIDComm/TSP exchange means equivalent semantic task state;
- source-code privacy intentions mean runtime unlinkability;
- CI/workflow green means assurance green.

## Critical implementation warning

If the composite uses `OpenVTC/dtg-credentials@fcae96171d95b4bae55a2e1ead22c52413da2a57` for Witness Credentials, the pinned library itself says its VWC digest encoding is incompatible with current spec-conformant implementations.

**Do not ship a current-spec interoperability claim on that VWC path without fixing or replacing it.**

This is a bounded implementation FAIL. It does not invalidate the canonical DTG Core Credentials specification, but it is a real blocker for the affected reference-implementation path.

## Privacy conclusion

Privacy is **INDETERMINATE**, not FAIL and not PASS.

DPIP #146 examined the fresh #293 lineage and returned `INDETERMINATE / evidence-required`. The clean-room run produced no new attributable runtime A/B observations for relationship identifiers, status/policy discovery, retained Trust Task evidence or verifier transcripts. The current sources also expose personhood deduplication and nullifier/context state whose privacy impact depends on actual runtime scoping and retention.

An implementer claiming composed unlinkability must produce deployment evidence; specification prose and successful cryptographic proof are insufficient.

## Normative composition gap: current member consent

The current credentials draft explicitly records that the member-issued VMC acknowledgement lacks a completed member-controlled withdrawal/status-discovery mechanism. Until that composition contract exists, a verifier can establish that an acknowledgement matches a grant but cannot generally establish that the member has not subsequently withdrawn it.

Use short validity windows only as a bounded interim control, not as proof that the normative gap is solved.

## Transport posture

Trust Tasks has a strong transport-neutral semantic model. The pinned VTI source, however, states that TSP is experimental/off by default and requires live-mediator validation before production.

A production implementer should therefore:
- select an explicitly supported transport profile;
- record the binding version;
- run semantic conformance, not merely connectivity tests;
- avoid claiming DIDComm/HTTPS/TSP equivalence without evidence.

## Optional / immature layers

The current VDS and Agent Names repositories do not yet provide mature normative deliverables in this pinned run, and HTX is not a normative technical conformance source. Treat these as optional/planned/experimental layers in an implementation profile rather than pretending every named portfolio repository is at the same maturity.

## Portfolio state interpretation

### Specification portfolio: AMBER

The core specifications are coherent enough to implement, but material currentness, privacy, transport and composition obligations remain.

### Pinned reference stack: AMBER with a bounded FAIL

The reference stack contains useful executable semantics but includes the explicit VWC interoperability defect. Any deployment using that path must remediate it before claiming current-spec interoperability.

### Why not RED overall?

The demonstrated VWC defect belongs to a non-normative implementation and can be fixed/replaced without contradicting the canonical specification. No fresh evidence establishes that the canonical core composition is fundamentally impossible or internally contradictory.

### What would move the portfolio toward GREEN?

1. resolve or explicitly profile the VWC digest implementation mismatch;
2. close the member-issued VMC status/currentness composition contract;
3. produce fresh pinned DPIP runtime evidence for the composed privacy surfaces;
4. produce cross-transport semantic conformance evidence for each claimed production transport;
5. publish/qualify the maturity of optional VDS/Agent Names/HTX layers;
6. publish a composition-level failure/correction/redress matrix.

## RAHP stability conclusion

This run did **not** require a DTG-specific RAHP-core modification.

Every non-PASS result could be represented as one of:
- implementation defect;
- normative composition dependency;
- specialist privacy referral;
- runtime evidence requirement;
- maturity/scope limitation; or
- composition/governance requirement.

That is the behaviour expected from a generic assurance engine.
