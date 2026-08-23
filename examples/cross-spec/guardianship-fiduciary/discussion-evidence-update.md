# Discussion update: first source-pinned evidence pass

The first source-pinned evidence pass materially **narrows** the opening hypothesis.

The initial question was whether DTG lacked enough machinery to represent and verify constrained representative authority. Current source text shows that this is too broad. DTG already contains several important primitives that control parts of the risk.

## What the evidence changed

### Credential-side controls already present

Current Credential Specification work already requires or supports several controls relevant to the case:

- credential validity periods;
- task-context binding;
- revocation/status checking through the applicable trust registry/governance framework;
- issuer-authorization evaluation; and
- an explicit distinction between cryptographic validity and authorization.

In particular, the current text states that a cryptographically valid credential is not necessarily an authorized one and requires the verifier to evaluate issuer authorization under the applicable governance framework.

That weakens any finding framed simply as “a valid credential may be treated as authority.” The residual question is narrower: **which constrained-authority predicates must be present, current and composed for the particular decision being made?**

### Trust Task controls already present

Current Trust Task work also provides significant building blocks:

- audience binding for proof-bearing documents;
- authenticated issuer/recipient semantics;
- task/exchange correlation;
- scoped and expiring grants;
- scope reduction and revocation;
- explicit consumer authorization checks; and
- a clear statement that proof establishes who asked, not whether that party is authorized to act.

The ACL grant/revoke examples are particularly useful evidence because they demonstrate that current Trust Task machinery is already capable of representing scoped, time-bounded authority and reducing or terminating that scope.

This materially weakens the premise that Trust Tasks need an entirely new authority mechanism.

The remaining question is whether those primitives can be composed for **transaction-specific constrained authority** involving approval thresholds, co-approval, conflicts, fiduciary duties, emergency activation, retained agency and restoration.

### Privacy / ZKP controls already present in the companion fork

The companion ZKP work also controls several risks that appeared open in the original hypothesis set. It already treats privacy as a composed-presentation property, separates task context from authority, warns against deterministic low-entropy hashes being mistaken for hiding commitments, and distinguishes cryptographic proof integrity/privacy from governance-backed assurance.

Those controls should therefore not be reported as absent.

However, they remain **companion-fork evidence**, not proof of upstream adoption. The remaining question is whether the relevant cross-spec interfaces and predicates can be made concrete enough to become interoperable/conformance evidence.

## Finding delta

The initial ten findings now have the following direction:

| Finding | Evidence-pass result | Residual question |
| --- | --- | --- |
| F01 Appointment validity can be over-read as permission | **Refined** | Existing specs distinguish proof/authorization, but constrained-authority composition remains to be demonstrated. |
| F02 Authority lifecycle can become stale | **Refined** | Validity, expiry and revocation exist; cross-artifact suspension/supersession/restoration propagation remains unproven. |
| F03 Approval replay | **Weakened** | Audience/task binding controls part of replay risk; transaction-semantic binding still needs a concrete case. |
| F04 Co-approval / relationship privacy leakage | **Refined / partially controlled** | Companion ZKP work covers composed privacy in principle; quorum/co-approval construction remains to be demonstrated. |
| F05 Enumerable confidential digests | **Weakened to construction guardrail** | Companion ZKP requirements already reject low-entropy deterministic hiding claims; apply this when constructions are selected. |
| F06 Emergency authority persistence | **Insufficient evidence / governance-heavy** | No basis yet for claiming a missing primitive; needs a concrete activation/deactivation case. |
| F07 Proof validity confused with fiduciary propriety | **Refined / partially controlled** | Existing specs separate proof and authorization; substantive fiduciary propriety remains governance/assurance, not crypto validity. |
| F08 Proof over weak source assertions | **Weakened** | Current credential/Trust Task text already requires issuer/source authorization and authenticated evidence; full evidence closure still matters. |
| F09 Retained agency/restoration invisible | **Insufficient evidence / governance-heavy** | Needs a concrete restoration/precedence construction before treating it as a normative gap. |
| F10 Cross-jurisdiction equivalence flattening | **Insufficient evidence / governance-heavy** | Needs actual profile/jurisdiction mapping evidence before proposing interoperability work. |

## Revised conclusion

The evidence therefore does **not** support the broad conclusion that DTG lacks the primitives needed for guardianship or fiduciary authority.

A more defensible statement is:

> DTG already contains meaningful primitives for scoped authority, validity, revocation, task context, authorization separation, authenticated evidence and privacy-preserving composition. What has not yet been demonstrated is a constrained-authority composition profile showing how appointment, current scope, transaction permission, duties/conflicts, retained principal agency and privacy-preserving proof inputs compose into an evidence-closed decision.

That distinction matters because it changes the next step from “open specification gaps” to **construct and test complete evidence closures using the primitives that already exist**.

## Next evidence-closure cases

The next phase will construct three concrete cases:

### Case A — Routine bounded-authority act

A representative performs an ordinary action that is clearly within an active, scoped authority.

The test is whether existing Credential + Trust Task + governance evidence is sufficient to establish:

- current appointment/authority;
- relevant scope;
- transaction context;
- current status;
- authoritative source; and
- the permitted verifier conclusion without inferring incapacity or broader authority.

### Case B — Threshold / co-approval act

A representative attempts an action that requires a threshold condition or additional approval.

The test is whether the system can prove:

- current authority;
- transaction amount/class;
- applicable threshold;
- required co-approval or quorum;
- freshness/non-replay; and
- satisfaction of the approval predicate without unnecessarily exposing every representative or sensitive relationship detail.

### Case C — Suspension / restoration act

Authority changes while previously issued credentials or task evidence remain available.

The test is whether relying parties can correctly determine:

- which authority state is current;
- whether stale approvals remain usable;
- how supersession or suspension propagates;
- how partial/full restoration of principal agency is represented; and
- which decision path takes precedence when representative and principal evidence coexist.

## Disposition rule

Each case will end with one of these outcomes:

- **Existing primitives sufficient**
- **Profile / composition clarification required**
- **Missing normative primitive demonstrated**
- **Governance-only / outside cryptographic specification**
- **Insufficient evidence**

Only a demonstrated residual gap should become a candidate downstream DTG issue or focused Discussion.

No downstream issue is being created as part of this update.