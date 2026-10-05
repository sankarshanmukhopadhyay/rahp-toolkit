# OpenVTC post-migration end-to-end RAHP assurance record

Campaign: #901  
Historical comparison: #851 / #868  
Assessment date: 2026-10-05

## Executive disposition

**Overall: PASS at the migrated semantic/source-composition layer, with bounded FAIL findings and explicit residual/evidence limits.**

The credential migration that was INDETERMINATE under #851 is now materially implemented across the current DTG Credentials, VSC Registry, Trust Tasks, VTI and OpenVTC sources. The central migration propositions are no longer waiting on implementation.

This result is deliberately narrower than a blanket system certification:

- current source and repository-native negative tests support the migrated wire/semantic contracts;
- the historical migration-convergence owner #870 is resolved;
- current concrete defects remain open under #898 and #899;
- live authority/status freshness remains a known residual under #609 where applicable;
- no claim is made that every optional/experimental path has been exercised end to end in one external runtime deployment.

## Frozen target pins

| Repository | Pin |
|---|---|
| trustoverip/dtgwg-cred-spec | `4088056a15f6e74847eb422e1c2bae33684272ea` |
| trustoverip/dtgwg-vsc-registry | `4a1a30337627e3d6f3f792db8430046977b17aaf` |
| OpenVTC/dtg-credentials | `fc9954d8d529d312ebac7ec1d413179857474c96` |
| OpenVTC/verifiable-trust-infrastructure | `ffd1a24d5d17202126b621696cbf41123c6d21e6` |
| OpenVTC/openvtc | `53696c9c709cabb3d15753b1bcc2ba2c66eb1b72` |
| trustoverip/dtgwg-trust-tasks-tf | `58fdbd5094ad36e4154d23a30038cb7bafeb517e` |

## Ten-flow disposition

| Flow | Current target | Result | Evidence / residual |
|---|---|---|---|
| 1. Invitation | VIC under DTG context v1 with `issuerScope: public` | **PASS (source)** | OpenVTC defines public invitation issuer scope; dtg-credentials refuses pre-v1 context/no-scope forms. |
| 2. Membership grant | community-issued VMC, public issuer scope | **PASS (source)** | dtg-credentials enforces public scope for community membership grant; OpenVTC current membership path uses conformant v1 VMC. |
| 3. Membership acknowledgement | reciprocal member-issued VMC | **PASS (source)** | OpenVTC acknowledgement constructor requires a conformant grant and member-declared issuer scope; old grant cannot be acknowledged. |
| 4. Role grant | community-issued VAC with `authority.scope` and `role:<name>` action | **PASS with known residual** | Trust Tasks and VTI use `roleVac`; retired CommunityRole VEC is a negative fixture. Live revocation/policy freshness remains #609 where authority is consumed outside locally authoritative state. |
| 5. Peer identity vetting | VDS card + `vetted/1` VSC + admission presentation | **PASS (source + negative tests)** | VTI signs/verifies StatementCredential, exact predicate, issuer, card/session binding, taskContext + taskDigestMultibase, validity and proofPurpose; legacy VEC is rejected. #870 closed. |
| 6. Relationship | VRC with truthful issuer scope | **PASS (source)** | OpenVTC VRC code declares scope explicitly and retires stored pre-v1 VRCs rather than ambiguously reinterpreting them. |
| 7. Persona annotation | VPC on v1 credential shape | **PASS (source)** | Current OpenVTC/dtg-credentials v1 constructors require issuerScope and one concrete subtype. No fresh material defect surfaced. |
| 8. Witness/personhood | `witnessed/1` VSC | **PASS (source)** | retired WitnessCredential is refused; current profile requires StatementCredential/predicate semantics and task binding. |
| 9. Community identity check | current canonical model: community-issued `vetted/1` VSC | **PASS against current canonical target; supplied guidance is stale** | Registry #24, current Trust Tasks and VTI now converge on community-issued `vetted/1`, not the earlier proposed plain IDVC. The older migration narrative should be refreshed. |
| 10. Statement admission | predicate accept list | **PASS (source + negative test)** | PredicateAcceptList is exact-match/fail-closed; unlisted predicate rejection is explicitly tested. |

## Migration-native negative evidence

Current repository evidence establishes:

- pre-v1 DTG context/no-`issuerScope` credentials are refused;
- retired `EndorsementCredential` and `WitnessCredential` types are refused by dtg-credentials;
- VTI vetting tests carry a retired VEC fixture and require the new `vetted/1` StatementCredential shape;
- VTI eligibility tests include the retired `CommunityRole` endorsement shape as a negative case;
- OpenVTC retains the old role VEC only as a retired-shape fixture;
- unknown/unlisted predicates are rejected by PredicateAcceptList;
- vetting statements are bound to subject, card, session id and session digest;
- Trust Tasks generated/current contracts define `statementType` as the VSC predicate and `eligibleVetters.role` through exact VAC `role:<role>` semantics.

## Historical regression reconciliation

| Anchor | Disposition |
|---|---|
| #767 proof-required task vs bearer equivalence | **Preserved as cross-flow control; no fresh migration-specific regression found** |
| #820 proofPurpose/key-role binding | **Preserved in current vetting verification; current proof verification requires assertionMethod for the statement** |
| #798 admission lifecycle | **Broadly preserved; new redelivery edge case is separately FAIL under #898** |
| #781 cross-component non-inference | **Preserved: statement, authority, membership and outcome semantics are represented separately** |
| #609 live authority/status freshness | **KNOWN RESIDUAL** where live external VAC/status/policy state is required |
| #870 migration semantic convergence | **RESOLVED / CLOSED at current pins** |
| #898 join credential redelivery | **FAIL / remediation required** |
| #899 signing-key replacement atomicity | **FAIL / remediation required** |

## Clean-room differential

### Fresh ∩ known

The current source review reproduced the expected high-value boundaries:

- proof is not authority;
- role is authority, not endorsement;
- statement meaning is predicate-driven, not type-string driven;
- old/new wire forms are intentionally incompatible;
- task citation and evidence binding are explicit;
- unknown statement semantics fail closed;
- current-state lifecycle must gate consequential re-use.

### Fresh − known

No new migration-core security defect was found beyond the already-created current owners #898 and #899.

A documentation/provenance divergence was found: the supplied migration guidance still describes Flow 9 as a plain W3C identity-verification credential, while current canonical registry/Trust Tasks/VTI semantics now use a community-issued `vetted/1` VSC. This is not a runtime defect at the current pins, but the migration read-out should flag the guidance for refresh so implementers do not follow the superseded model.

### Known − fresh

The older #870 semantic-convergence gap no longer reproduces and is now closed. Step-up and broader live-authority residuals remain under their existing owners rather than being duplicated here.

## Current failures / remediation

### #898 — approved-join credential redelivery after Historical removal

Current VTI permits a historical removed member whose approved request and stored credential bodies remain to enter the redelivery path because the resend predicate does not check `member.is_removed()`.

**Result: FAIL / remediation required.**

### #899 — signing-key replacement is serialized but not failure-atomic

Current VTI revokes the old delegation before enrolling the replacement. A storage failure between the two writes can leave the old key revoked without the new key enrolled.

**Result: FAIL / remediation required.**

## Evidence limitation

GitHub commit-status APIs exposed no commit-status/workflow records for the frozen release/head commits during this assessment. The result therefore relies on source-pinned implementation and repository-native test evidence, not on a newly observed external CI run for every repository.

That limitation does not convert observed source defects into INDETERMINATE; it does bound positive claims to the evidence actually inspected.

## Final judgment

The original credential migration has crossed the important semantic threshold that #851 could not yet assess: current components agree on DTG context v1, required issuerScope, VSC predicates, VAC role authority and fail-closed predicate admission, and explicit negative fixtures defend the old wire forms.

The remaining upstream work is no longer “finish the migration.” It is narrower and more actionable:

1. fix #898 credential redelivery across removed/historical membership state;
2. fix #899 failure-atomic signing-key replacement;
3. retain #609 as the live authority/status freshness residual where applicable; and
4. refresh the migration guidance so Flow 9 reflects the current community-issued `vetted/1` model.

