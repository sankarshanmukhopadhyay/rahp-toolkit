# LPC pre-demo assurance record — OpenVTC credential migration

Campaign: RAHP #851  
Migration composition owner: RAHP #868  
Fresh differential owner: RAHP #870  
Assessment date: 2026-09-30  
Scope manifest: `docs/lpc-pre-demo-scope-manifest.md`  
Evidence templates: `docs/lpc-pre-demo-evidence-templates.md`

## Executive disposition

**Overall result: INDETERMINATE / target migration not yet realized at the frozen implementation pins.**

This is not a finding that the current OpenVTC/VTI stack is unsafe merely because it still implements the pre-migration credential model. It means the upstream-declared LPC credential-migration target cannot yet receive a runtime PASS/FAIL judgment because the implementation revisions frozen for this campaign do not implement that target.

The campaign nevertheless produced a useful and bounded assurance result:

- the authoritative migration flow has been captured;
- the current pre-migration implementation and current specification/registry revisions are source-pinned;
- applicable historical RAHP regressions and known residuals have been reconciled;
- every migration seam M1–M8 has a current disposition;
- a clean-room differential identified one additional material Trust Tasks semantic-convergence issue (#870);
- target-native runtime evidence requirements are defined and ready to instantiate;
- no system-wide or migration-complete assurance claim is made.

## Assessed subject

The upstream-supplied **OpenVTC Credential Migration** describes a coordinated cut-over across ten flows:

1. VIC invitation;
2. community-issued VMC;
3. member-issued reciprocal VMC;
4. role VEC → VAC;
5. identity-vetting VEC → VSC `vetted/1`;
6. VRC + `issuerScope`;
7. VPC + `issuerScope`;
8. VWC → VSC `witnessed/1`;
9. `IdentityVerification` VEC → plain W3C IDVC;
10. free endorsement-type registry → predicate accept list.

The upstream source explicitly prefers coordinated cut-over over indefinite dual acceptance.

## Frozen evidence boundary

| Repository | Frozen revision | Current role |
|---|---|---|
| `trustoverip/dtgwg-cred-spec` | `44d5084926ad06ca6395d754c91d8494a7c38c22` | current credential semantics; context v1; required `issuerScope`; `vetted/1` example alignment |
| `trustoverip/dtgwg-vsc-registry` | `7c5ba6c8114dc64cdfe8356992f46850a0d8ead1` | VSC predicate registry; `endorses/1`, `witnessed/1`, `vetted/1`, `presented/1` present as draft |
| `OpenVTC/dtg-credentials` | `1d49eaf17a5002817370426554d312db2ed19b09` | pre-migration 0.11.0 credential implementation |
| `OpenVTC/verifiable-trust-infrastructure` | `32ddd2f231474104535830ab05a52a66527c61ac` | pre-migration VTA/VTC implementation |
| `OpenVTC/openvtc` | `e49816c5f6c49d2d2d2f656d8e20507133e00c01` | pre-migration OpenVTC client implementation |
| `trustoverip/dtgwg-trust-tasks-tf` | `9a104be3b9b7302cab64adf779079ab5be69c4c2` | current Trust Tasks line, still carrying several old credential/role semantics |

## Baseline observations

At the frozen pins:

- cred-spec already requires `issuerScope`;
- the VSC registry already contains `vetted/1`, `witnessed/1`, `presented/1` and `endorses/1` as draft predicates;
- `dtg-credentials` does **not** yet contain `issuerScope` or `StatementCredential`;
- VTI still uses `IDENTITY_VETTING_ENDORSEMENT_TYPE`, VEC `CommunityRole`, free endorsement-type registration and endorsement-based vetting requirements;
- OpenVTC still maps role credentials to `EndorsementCredential`;
- Trust Tasks still describes vetting statements as endorsement credentials and vetter eligibility as possession of a `CommunityRole` endorsement.

The specification/registry and implementation surfaces are therefore temporarily on different sides of the migration boundary.

## Proposition-level results

| Area | Proposition | Evidence | Result | Residual |
|---|---|---|---|---|
| M1 coordinated cut-over | Old/new credential semantics cannot coexist ambiguously across a partial deployment. | Upstream migration ordering; frozen repo pins; implementation remains pre-cut-over. | **INDETERMINATE** | No migrated target exists to test atomicity, rollback or mixed-version refusal. Must re-pin migrated revisions before runtime assurance. |
| M2 `issuerScope` | Every DTG credential carries a valid truthful correlation-scope declaration and consumers enforce it. | cred-spec `44d5084` requires `issuerScope`; no implementation support found in `dtg-credentials`/OpenVTC frozen pins. | **INDETERMINATE** | Runtime enforcement and truthful scope selection untested. Privacy conclusion routes to DPIP; declaration alone is not unlinkability evidence. |
| M3 VEC→VAC authority | Role authority is expressed and consumed as bounded VAC scope/actions, not retired endorsement semantics. | `dtg-credentials` already supplies VAC constructor/authority-chain machinery; VTI consumers remain `CommunityRole` VEC based. | **INDETERMINATE / transition not implemented** | Exact role→scope/actions mapping and consumer migration missing. Live status/policy freshness remains #609. Registry action vocabulary remains open (#17). |
| M4 vetting/witness VSC | `vetted/1` and `witnessed/1` preserve intended claims, task binding and subject/issuer semantics without widening. | Registry profiles exist; `dtg-credentials` lacks VSC implementation; VTI still uses VEC/VWC paths. | **INDETERMINATE** | Target-native VSC issue/present/verify evidence absent. Digest/task-citation privacy residuals cred-spec #38/#58 remain explicit. |
| M5 IDVC boundary | Identity verification is a plain W3C credential, not misclassified as DTG/VSC/VAC, with live status and exact policy consumption. | Current VTI already treats `IdentityVerification` conceptually as non-DTG identity-proofing evidence, but upstream migration leaves final type/context open. | **INDETERMINATE / design input missing** | Exact type/context and migrated policy contract must be pinned. |
| M6 predicate accept list | Free endorsement type strings no longer confer statement semantics; unknown/unadmitted predicates fail closed. | Current VTI still implements endorsement-type registration and validation. Registry predicates exist but migration is not implemented. | **INDETERMINATE** | Predicate accept-list runtime, unknown-predicate refusal and draft-predicate policy not yet evidenced. |
| M7 Trust Tasks convergence | Task schemas, bindings and credential semantics move coherently to VSC/VAC/current DTG types. | Current Trust Tasks still carries endorsement-based vetting and `CommunityRole` eligibility; canonical VMC path exists but some historical names remain in surfaces/examples. Fresh finding #870 owns the semantic migration. | **FAIL against target semantics at the frozen pin / expected pre-migration baseline** | Must not be interpreted as a defect in the declared pre-migration stack. It proves the target cut-over is not complete and identifies #870 as the durable semantic-convergence owner. |
| M8 non-inference/evidence integrity | Membership, role authority, vetting, personhood/ID evidence, relationship and delivery/outcome remain distinct propositions. | Historical RAHP #781/#798/#833 plus current source inspection. | **INDETERMINATE for migrated target; historical controls retained** | Fresh migrated runtime evidence required. No component artifact may be promoted into a stronger claim by migration convenience. |

## Historical regression reconciliation

| RAHP anchor | Current LPC disposition |
|---|---|
| #767 proof-required task vs bearer/session equivalence | **IN-SCOPE / RETEST REQUIRED** once migrated signed credential-delivery/admission paths exist |
| #795/#799 operation-bound step-up | **N/A** to the supplied migration subject unless privileged step-up is added to the demo |
| #820 proofPurpose/key-role binding | **IN-SCOPE / historical strengthened; migrated regression evidence still required** |
| #833 acceptance-window semantics | **CONDITIONAL** on asynchronous discovery/delivery in the actual run |
| #798 admission lifecycle | **IN-SCOPE / historical strengthened; migrated regression evidence required** |
| #781 Trust Tasks × Credential Spec | **IN-SCOPE / known cross-spec residual discipline applies** |
| #780 Trust Tasks × ZKP | **CONDITIONAL** on ZKP/personhood/hidden-vetter proof path |
| #225/#228 source-pinned composition/evidence sufficiency | **IN-SCOPE / satisfied as campaign method** |
| #609 live VAC revocation/policy freshness | **KNOWN RESIDUAL** when VAC authority becomes active |
| #826/#837 step-up residuals | **N/A** unless step-up is demonstrated |
| #836 recipient-advertised acceptance windows | **CONDITIONAL** |
| #310/#338/#339 privacy/correlation | **IN-SCOPE where correlation claims are made; DPIP owns conclusion** |
| #849 hidden-vetter PCS | **N/A unless `vetting-pcs` is enabled** |

## Clean-room differential

### Fresh ∩ known

The independent source pass reproduced known high-value assurance concerns:

- action-time authority and revocation freshness;
- proof/authentication must not become authorization;
- admission lifecycle and current vetter authority;
- cross-component non-inference;
- task/proof freshness and replay;
- privacy/correlation requiring attributable runtime evidence.

### Fresh − known

**#870 — Trust Tasks vetting predicate / vetter-eligibility semantic migration.**

The upstream plan says to replace the vetting statement type URI with the VSC predicate IRI, but the current Trust Tasks contract embeds the old model structurally and semantically:

- statement body described as `credentialSubject.endorsement`;
- `statementType` defined as an endorsement type;
- vetter eligibility defined by `CommunityRole` endorsement possession.

The migration therefore requires schema, generated-binding and authority-consumer convergence, not only URI substitution.

### Known − fresh

Step-up-specific residuals #826/#837 did not arise from the supplied migration flow and remain outside the campaign unless the actual demo adds those operations.

## Evidence-template dispositions

| Family | Current disposition |
|---|---|
| A — authority at effect time | **READY / NOT RUN**: target VAC consumer not yet landed |
| B — proof/authentication vs authorization | **READY / NOT RUN**: migrated signed task paths not yet landed |
| C — exact operation-bound step-up | **N/A** on supplied scope |
| D — proofPurpose/key-role binding | **READY / NOT RUN** against migrated path |
| E — freshness/replay/acceptance | **READY / NOT RUN**; acceptance-window subcases conditional |
| F — cross-component non-inference | **READY / source-assessed; runtime NOT RUN** |
| G — fail-closed consequential boundary | **READY / NOT RUN** against target migration |
| H — outcome/evidence integrity | **READY / NOT RUN** against target migration |
| P — privacy/correlation | **READY / requires target-attributable A/B evidence and DPIP** |

`NOT RUN` here is an evidence statement, not a negative test result.

## Known design dependencies

The upstream source and current repositories leave at least these decisions open:

1. exact type/context for the plain W3C identity-verification credential;
2. mapping of old role names to VAC `authority.scope/actions`, including whether registry #17 supplies a shared action vocabulary;
3. whether invitation role scopes remain or authority is exclusively issued at admission;
4. treatment of draft VSC predicates in the LPC/demo profile;
5. cred-spec #38/#58 binder/citation privacy work.

No RAHP conclusion fills these decisions by inference.

## LPC-facing conclusion

A defensible statement at this freeze is:

> RAHP has reviewed the upstream-declared OpenVTC credential-migration path, pinned the current specification, registry and implementation state, reconciled the path against historical assurance findings, and performed a fresh cross-component review. The migration target is not yet implemented at the frozen OpenVTC/VTI revisions, so target-native end-to-end runtime assurance remains INDETERMINATE rather than PASS. The assessment has identified the required regression/negative tests and one additional Trust Tasks semantic-convergence issue (#870). Existing residuals, including live VAC revocation/policy freshness and privacy/correlation evidence, remain explicit.

Statements that are **not** supported:

- “the LPC credential migration is RAHP PASS”;
- “the current implementation has completed the credential migration”;
- “`issuerScope` proves unlinkability/privacy”;
- “VSC registry admission proves runtime statement semantics”;
- “VAC issuance alone proves current role authorization”;
- “all DTG/VTC risks are covered.”

## Retest trigger

A comparable target run is warranted as soon as migrated implementation revisions exist.

The retest must:

1. append a second immutable target pin set rather than replacing the pre-migration baseline;
2. instantiate the selected evidence cases;
3. include old-shape rejection/mixed-version negative cases;
4. include VAC action widening/revocation/freshness cases;
5. include VSC predicate/task-binding cases;
6. include fail-closed unknown-predicate and missing/invalid-`issuerScope` cases;
7. route privacy evidence to DPIP;
8. reconcile #870 before any migration-complete conclusion.

## Campaign closure rationale

The campaign can close at this point as a **completed pre-demo assurance examination with an INDETERMINATE target result** because:

- authoritative scope is captured;
- current source boundary is frozen;
- historical regressions are dispositioned;
- targeted runtime evidence gaps are explicitly recorded rather than promoted to PASS;
- the clean-room differential is reconciled;
- the new material finding has a durable owner (#870);
- specialist/known residuals retain their existing owners;
- this Assurance Record distinguishes demonstrated evidence from missing target evidence.

A later migrated implementation does not mutate this record. It triggers a new comparable source-pinned run under the durable owners above.
