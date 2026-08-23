# Guardianship and fiduciary authority — source-pinned evidence review

Date: 2026-08-23

This review converts the initial guardianship/fiduciary pressure-test hypotheses into a source-pinned evidence assessment. It deliberately distinguishes three evidence classes:

1. **upstream DTG specification text** — evidence of what the shared DTG work currently says;
2. **companion-fork design/conformance guidance** — evidence that a control has been designed or exercised in the ZKP fork, but not evidence that upstream DTG has adopted it;
3. **absence / unresolved composition** — a remaining question, not proof that a specification is defective.

The review does not create downstream DTG issues. Its purpose is to determine which hypotheses survive contact with current source material.

## Source pins

| Surface | Revision reviewed |
| --- | --- |
| DTG General | `trustoverip/dtgwg-general@fa15044225ff447ad6564983a5ce0732b80cbdc1` |
| Credential Specification | `trustoverip/dtgwg-cred-spec@b89f389abbdae77ba60b673c0836c781c2b54169` |
| Trust Tasks | `trustoverip/dtgwg-trust-tasks-tf@4937c70df95e56ed6404b8c004106ecb121a23cf` |
| upstream ZKP TF | `trustoverip/dtgwg-zkp-tf@a58569308fcec70e014835555a1f1d8c15f09852` |
| companion ZKP fork | `sankarshanmukhopadhyay/dtgwg-zkp-tf@6064c3428ca88471b5ec8271ec03e318c26d2a13` |

## Material controls already present

The evidence pass found controls that materially narrow the initial hypotheses:

- The Credential Specification includes `validFrom`/`validUntil`, optional `taskContext`, verifier validity enforcement, issuer-authorization checks, and an explicit warning that a cryptographically valid credential is not necessarily an authorized credential.
- Trust Tasks separates proof of producer identity/integrity from authorization. Its ACL tasks support roles, scopes, expiry, revocation, scope reduction, consumer policy checks, and evidentiary persistence.
- Trust Tasks audience-binds proof-carrying documents to the intended recipient and distinguishes exchange correlation from normative authorization semantics.
- The companion ZKP fork explicitly states that task context is not authority, evaluates privacy over composed presentations/evidence closure, rejects deterministic/low-entropy hashes as hiding mechanisms for enumerable inputs, and separates cryptographic assurance from governance-backed assurance.
- The companion ZKP fork also records governance rules for external evidence and does not automatically grant conformance credit to unverified sources.

These controls mean the pressure test should not claim that DTG lacks authority, lifecycle, replay or privacy primitives in general. The residual issue is narrower: whether those primitives compose into a sufficient guardianship/fiduciary decision model.

## Finding-by-finding delta

| Finding | Evidence-pass classification | What changed |
| --- | --- | --- |
| F01 — appointment validity over-read as permission | **Refined** | Upstream already distinguishes cryptographic identity/proof from authorization, and Trust Tasks makes the consumer's policy decision authoritative. The remaining question is whether a guardianship/fiduciary appointment, its scope, duties and a particular transaction permission are represented as separate interoperable propositions. |
| F02 — stale authority across artifacts | **Refined** | Expiry, revocation and scope reduction primitives exist. The open problem is cross-artifact propagation of suspension/supersession/restoration and the transaction-time rule for selecting the authoritative current state. |
| F03 — replay outside transaction context | **Weakened** | Trust Tasks provides unique document IDs, audience binding, thread/citation rules and task-context machinery. Generic replay is therefore not an unmitigated framework gap. A narrower question remains for domain approvals: which transaction fields and authority state must an approval commit to, and what freshness rule applies? |
| F04 — privacy leakage from co-approval/relationship proof | **Refined / partially controlled** | The companion ZKP fork already requires composed-presentation privacy analysis. The unresolved point is an upstream cross-spec contract exposing the required authority/co-approval predicates without forcing durable relationship correlators or unnecessary ancestry/status disclosure. |
| F05 — enumerable confidential digests | **Weakened / construction guardrail** | The companion ZKP fork already rejects deterministic/low-entropy hashing as a privacy mechanism for enumerable values. The Credential Specification's VWC digest is described as an integrity binding, not a confidentiality construction. This finding is retained as a guardrail for future hidden-status constructions, not as a claim that current VWC digest semantics are confidential. |
| F06 — emergency authority persists | **Insufficient evidence / profile-level** | Generic expiry and revocation primitives exist, but the reviewed sources do not establish a guardianship-specific emergency-authority profile with activation/deactivation/restoration semantics. The evidence supports a profile/governance question, not a generic framework defect. |
| F07 — proof validity confused with fiduciary propriety | **Refined / partially controlled** | Upstream Credential and Trust Tasks text already rejects the inference that proof validity equals authorization. The companion ZKP fork further separates proof assurance from governance assurance. The residual fiduciary question concerns duties, conflicts, best-interest/least-restrictive rules and other propriety predicates that authorization alone does not establish. |
| F08 — proof over weakly governed source assertions | **Weakened** | Upstream requires proof/source authorization checks at important boundaries, while the companion fork has explicit external-evidence governance. The residual gap is profile-specific: how an authoritative guardianship/fiduciary source is discovered, governed and lifecycle-checked before its predicates receive conformance credit. |
| F09 — retained agency/restoration invisible | **Insufficient evidence / governance-heavy** | The reviewed primitives can revoke, expire and change authority, but they do not by themselves establish a normative retained-agency or supported-decision model. This remains a governance/profile requirement unless DTG chooses to standardize machine-verifiable retained-agency predicates. |
| F10 — jurisdictional semantic flattening | **Insufficient evidence / governance-heavy** | No evidence supports treating current DTG identifiers as a cross-jurisdiction equivalence mechanism for guardianship/fiduciary law. The risk is real as an interoperability design constraint, but a concrete DTG defect requires a future profile/mapping proposal to test. |

## Hypothesis delta

### H-GF-01 — shared cross-spec constrained-authority semantics

**Result: refined, still supported.**

DTG already has reusable authorization, scope, lifecycle and evidence primitives. The evidence does not support inventing a monolithic guardianship credential. The stronger formulation is that a constrained-authority profile needs an explicit **composition contract**: which existing primitives establish appointment, current scope and source authority, and which additional predicates are needed for duties, conflicts, retained agency, oversight and transaction permission.

### H-GF-02 — bounded authority in credential semantics

**Result: refined.**

The Credential Specification already carries validity and task-context concepts and explicitly requires issuer authorization. A future guardianship/fiduciary profile should reuse those primitives. New credential semantics are justified only for predicates that cannot already be represented or referenced safely.

### H-GF-03 — transaction-bound evidence in Trust Tasks

**Result: weakened but still relevant.**

Trust Tasks already has strong identity, audience, correlation, proof and ACL authorization machinery. The remaining question is domain-specific composition: a fiduciary approval must identify the decision-relevant transaction semantics and current authority state that make the approval meaningful. This should be tested as a profile before proposing framework-level changes.

### H-GF-04 — privacy-preserving composed predicates

**Result: confirmed at the architectural level, partially controlled in the companion fork.**

The companion ZKP work already expresses the core privacy rule: assess the whole composed presentation/evidence closure and do not treat low-entropy hashes as hiding. The next gap is not to restate that rule, but to identify concrete guardianship/fiduciary predicates and determine whether upstream credential/task interfaces expose sufficient proof inputs without requiring a durable correlator.

### H-GF-05 — governance/assurance beyond cryptographic validity

**Result: confirmed but narrowed.**

The evidence strongly supports the non-inference boundary: proof integrity, identity and authorization do not establish fiduciary propriety. DTG already recognizes part of this distinction. The remaining work is to identify which propriety questions belong to governance/profile rules and which require machine-verifiable evidence hooks.

## Revised residual problem

After the evidence pass, the central gap is no longer well described as “DTG lacks guardianship/fiduciary support.” A more accurate statement is:

> DTG has many of the necessary primitives for scoped authority, lifecycle, evidence binding and privacy assurance, but there is not yet an evidence-backed constrained-authority composition profile showing how those primitives establish a guardianship/fiduciary decision without over-disclosure or semantic overreach.

That is a materially smaller and more actionable problem.

## Recommended next gate

Before any downstream DTG issue is opened:

1. define two or three concrete constrained-authority transactions (for example, routine act, threshold/co-approval act, and restoration/supersession case);
2. construct the evidence closure for each using current Credential and Trust Task primitives;
3. identify only the predicates that cannot be represented or privately proven with the current interfaces;
4. classify each remaining gap as specification, profile, governance or assurance/conformance;
5. take that evidence-backed delta to maintainers for disposition.

This keeps the improvement loop evidence-driven and avoids asking DTG specifications to solve policy questions that belong in governance profiles.
