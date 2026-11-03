# Protection coverage from existing RAHP evidence: a bounded research pilot

**Issue:** [#1159](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1159)  
**State:** analyst-assembled research candidate; **NOT independently accepted**  
**Date:** 2026-11-03  
**RAHP record snapshot:** `sankarshanmukhopadhyay/rahp-toolkit@42df1e2660a0db8221fdf587c9222b628f95419e`  
**Method:** read-only projection over three existing canonical `pressure-test.yaml` records. This document does not add a method schema, amend a source finding, or reassess current upstream implementations.

## 1. Proposition, affected context, and intended answer

**Affected context:** a principal whose work, relationships, or rights may be affected when an agent or delegate purports to act for them; includes a relying party accepting the action. No actual person or deployment is identified.

**Threat:** a consumer interprets authenticated Trust Task producer identity or a valid agent membership credential as **current, scoped authority** to execute a consequential delegated action, without obtaining and checking the governing mandate and lifecycle evidence.

**Question:** At the exact historical revisions reviewed, which **specification-level separation or control** is evidenced, where is authority allocated, and what remains unresolved in the composed decision?

Portable concerns already present in the source records include `HRM-AUT-04`, `RKP-DEL-01`, `RKP-AUTH-02`, and `CTP-AUTH-02`. These pattern IDs are *RAHP interpretation aids*, not authoritative upstream requirements, demonstrated harms, or a mapping to a specific affected person.

The evidence examined is historical. Its normative observations must not be silently promoted to statements about upstream latest versions.

## 2. Canonical inputs and exact scope

The first two are specification-review records; the third is a later **composition** review of the same two families, not an independent third standard. The issue allows three or four relevant *specifications/artifacts*; the distinction matters.

| Record | Exact historical upstream target(s) as recorded | Canonical RAHP source | Assessment excerpt |
| --- | --- | --- | --- |
| Trust Tasks | `trustoverip/dtgwg-trust-tasks-tf@fbe196a8a17ba3f99d0657a64be5ac58621023a1` (Editor's Draft 0.3) | [Trust Tasks review](../../examples/trust-tasks-spec/pressure-test.yaml) | `SR-002 / F-003`: producer identity is not portable proof of authority/delegation. |
| DTG Credential Specification | `trustoverip/dtgwg-cred-spec@d19f7c9cac364fab8e50cf434513ef53fef80e37` (Working Draft 01) | [Credential review](../../examples/dtg-credential-spec/pressure-test.yaml) | `SR-001 / F-002`: agent VMC membership can be misread as authority/capability/accountability. |
| Trust Tasks × Credential Specification | Trust Tasks `134733ff934775db522522dc26cb79836da29256`; Credential Specification `2b403b607aaec9d84f78189a55337c677f3cd2ed` (RAHP v1.9 baseline) | [Composition review](../../examples/cross-spec/trust-tasks-credspec/v1.9-current-pressure-test.yaml) | `SR-XSP-001 / F-001`: current authority and lifecycle coherence remain a composition gap. |

The later composition record is a **different target epoch** from the first two records. It cannot be treated as simultaneous confirmation of an identical normative baseline. This pilot compares their *recorded interpretation boundaries* and does not recompute the changes between epochs.

## 3. Source-separated assessment packets

Each packet distinguishes **recorded source observation**, **RAHP analyst inference**, **architectural allocation**, and **qualification**. Every observed normative statement below is attributed to the existing RAHP source record; I did not independently re-run the historical upstream specification review.

### Packet A: Trust Tasks identity versus authority

- **Recorded source observation:** `SR-002 / F-003` cites `SPEC.md#72-consumer-requirements` for the proposition that ceremony membership does not itself confer task authority, and `SPEC.md#48-the-issuer-and-recipient-members` for issuer/proof binding to document origin. It cites `docs/design-notes/delegated-trust-task-execution.md#2-roles-and-trust` for the executor's policy boundary.
- **Bounded coverage statement:** the assessed draft **separates** proof of document origin/ceremony membership from authorization. This is evidence of an applicable *semantic boundary in the assessed specification*, not evidence that a particular consumer enforces it.
- **Unresolved requirement or allocation:** portable delegation/mandate semantics including principal, delegate, operation, scope, temporal validity, revocation, onward delegation and authoritative enforcement remain allocated to companion authorization profiles, governance and actual runtime policy.
- **Assessment status:** **PARTIAL/CONDITIONAL**. It would be misleading to label this specification `protected`: the recorded review itself identifies an open companion-profile gap.
- **Unsupported inference:** proof validity ≠ permission to execute; membership ≠ delegation; signed task ≠ currently effective authority.

### Packet B: Agent membership credential versus mandate

- **Recorded source observation:** `SR-001 / F-002` cites `spec/body.md#vmc-verifiable-membership-credential` for VMC subjects including agents and the membership semantics of that record. It cites `spec/body.md#security-considerations` for issuer authorization checks and identifies missing explicit non-inference language in the **assessed WD01**.
- **Bounded coverage statement:** the reviewed credential format can represent an agent's membership, **not** an agent's operation-specific permission, controller identity, delegated mandate or current authority.
- **Unresolved requirement or allocation:** the assessed source review recommends a normative non-inference rule and companion agent/delegation binding. The fact that this is recommended is **not evidence it was adopted** at WD01 or implemented by a consumer.
- **Assessment status:** **GAP IDENTIFIED IN HISTORICAL REVIEW**. This does not establish that the latest Credential Specification still has the gap; a current-source reassessment is required.
- **Unsupported inference:** valid membership credential ≠ operator accountability or permission; missing negative evidence ≠ explicit prohibition.

### Packet C: Composed authority at action time

- **Recorded source observation:** `SR-XSP-001 / F-001` (pinned to later Trust Tasks and Credential Specification revisions above) cites its own Trust Tasks reassessment, composed scenarios `XSP-002` and `XSP-013` through `XSP-020`, and `specs/acl/grant/0.1/spec.md`. It acknowledges scoped expiring ACL mechanics while retaining the cross-artifact authority and lifecycle residual.
- **Bounded coverage statement:** the composition record recognizes narrower authority/ACL primitives, but explicitly does **not** demonstrate synchronized credential/status/policy evaluation or effective mandate at consequential action time.
- **Unresolved requirement or allocation:** define and test the narrow cross-spec profile for effective authority, revocation and temporal precedence. Governing specification and governance owners must define obligations; implementation/deployment owners must enforce and produce runtime evidence.
- **Assessment status:** **UNRESOLVED COMPOSITION**, with the canonical `policy_gate: FAIL` retained at its historical review epoch. This is an assessment-policy disposition, **not** an observed deployed attack.
- **Unsupported inference:** passing both component validators ≠ composition PASS; an ACL grant ≠ current credential/mandate across every boundary.

## 4. Derived consumer-facing projection (not authoritative state)

This compact table is derived *only* from the three canonical records above. It is not a completeness matrix and has **no score**, Boolean protection flag, or implied certification.

| Concern × artifact | Specification-level result supported by the recorded review | What remains unestablished | Reader-facing status |
| --- | --- | --- | --- |
| Producer identity mistaken for mandate × Trust Tasks | Distinction between origin proof and authorization is explicitly recognized in assessed draft. | Cross-system portable delegation profile; implementation enforcement. | **Conditional treatment; governance/implementation evidence required** |
| Agent membership mistaken for mandate × Credential Specification | Membership semantics are separately described; WD01 review identifies missing explicit non-inference language. | Adoption of the proposed non-inference rule; current revision; consumer behavior. | **Historic gap identified; current status unassessed** |
| Valid components combined into stale delegation × composition | Scoped ACL mechanics exist in later source epoch; recorded composition finding remains open. | Action-time mandate, status/revocation and cross-spec lifecycle coherence. | **Unresolved composition; no runtime PASS** |

**Absent cells** mean **NOT_ASSESSED** unless a separately documented applicability decision exists. `NOT_APPLICABLE` would require affirmative scope reasoning; it cannot be inferred because a record is missing. `NO_RELEVANT_MATERIAL_FOUND` would require a separately specified search scope and negative search record, neither of which this pilot claims.

## 5. Freshness and accountable review

The provenance of each packet is its historical source pin and RAHP file, **not** the publication date of this derived page. A material change to any target specification, companion authority profile, governance rule, role/impact pattern, or evidence set triggers reassessment of the affected packet. The old findings remain citable as historic judgments.

The existing RAHP records already carry source target, finding, severity, evidence observation, harm hypothesis, control/disposition and retest trigger. This pilot does **not** demonstrate that an independent reader agrees with the judgments, nor that any current deployment satisfies their requirements.

**Reviewer challenge checklist:** verify cited upstream paragraphs at the historical commits; challenge the recorded non-inference interpretation; determine which later changes supersede the historic findings; check whether the purported delegate is actually authorized at action time; request target-native evidence before accepting implementation effectiveness. Record disagreements as disagreements, not automatic failures or PASS.

**Human acceptance:** `PENDING` (no independent reviewer named, no acceptance presumed). The document is an attributable *analyst candidate* for discussion under #1159; it cannot on its own satisfy the issue's independent reviewability acceptance criterion.

## 6. Research disposition

**Provisional finding:** a useful three-artifact protection-coverage **view can be expressed using existing RAHP review records**. These canonical records already contain enough narrative/source structure to distinguish limited semantic controls, specification gaps, allocation, unresolved composition and reassessment triggers. A new canonical protection matrix/schema is **NOT JUSTIFIED by this pilot**.

**Important limits:** the projection was assembled manually; historical reviews are not current-state checks; no independent review or usability study was performed; we did not attempt to generate this page automatically or establish portability beyond this one proposition. Therefore the strongest justified decision is **continue bounded research with independent challenge, not productise a dashboard**.

The next necessary observation is a cold-reader examination: can another reviewer independently reconstruct the three conclusions, distinguish the differing source epochs, and identify the missing action-time authority evidence without explanatory assistance? If not, repair the existing evidence/navigation first. Only consider a generator if the manual projection demonstrates repeatable reader value and evidence integrity.

**Release and compatibility impact:** none. This is a research projection; there are no changes to canonical assessments, RAHP schema, method or runtime evaluation.
