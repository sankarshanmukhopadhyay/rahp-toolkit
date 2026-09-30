# LPC pre-demo scope manifest — OpenVTC credential migration

Campaign: RAHP #851  
Child assessment: RAHP #868  
Scope input: upstream-supplied **OpenVTC Credential Migration**, dated 2026-09-30  
Freeze mode: **authoritative flow topology + current-main implementation pins**

## Scope statement

The LPC-oriented assurance subject is the coordinated migration of the OpenVTC/VTI credential flows from the pre-WD02 credential shapes to the current DTG credential, VSC and VAC semantics described by the upstream migration document.

The source document is authoritative for the migration flow topology and intended semantic changes. It did not provide immutable revisions for every implementation repository. The implementation boundary below is therefore frozen independently from current `main` for reproducibility.

This is a coordinated cut-over assessment, not a system-wide assurance claim.

## Actors and components

- VTC service (`vtc-service`)
- applicant/member running OpenVTC + VTA
- vetter/peer running OpenVTC + VTA
- witness/member or VTA
- DTG Credential Specification
- DTG VSC Predicate Registry
- `dtg-credentials` implementation crate
- VTI / `vta-sdk`
- OpenVTC
- Trust Tasks

## Ordered credential flow

| Flow | Interaction | Before | Target |
|---|---|---|---|
| 1 | VTC → OpenVTC invitation | VIC | VIC on DTG context v1 + `issuerScope` |
| 2 | VTC → member membership grant | community-issued VMC | VMC + public `issuerScope` |
| 3 | member → VTC membership acknowledgement | member-issued VMC | VMC + issuer-declared scope |
| 4 | VTC → member role grant | VEC / `CommunityRole` | VAC with authority scope/actions |
| 5a | applicant ↔ vetter vetting card | signed VDS | unchanged VDS |
| 5b | vetter → applicant vetting statement | VEC / identity-vetting endorsement | VSC `vetted/1` |
| 5c | applicant → VTC admission presentation | VP of VECs | VP of `vetted/1` VSCs |
| 6 | OpenVTC ↔ OpenVTC; publish to VTC | VRC | VRC + `issuerScope` |
| 7 | OpenVTC → VTC persona annotation | VPC | VPC + `issuerScope` |
| 8a | witness → member witnessed edge | VWC | VSC `witnessed/1` |
| 8b | member → VTC personhood/join presentation | VP with VWC | VP with `witnessed/1` |
| 9 | VTC → member → VTC policy identity verification | VEC / `IdentityVerification` | plain non-DTG W3C IDVC |
| 10 | VTC admin → VTC policy statement vocabulary | free `typeUri` list | predicate accept list |

## Frozen source baseline

Observed on 2026-09-30.

| Repository | Revision | Role in subject |
|---|---|---|
| `trustoverip/dtgwg-cred-spec` | `44d5084926ad06ca6395d754c91d8494a7c38c22` | current credential semantics, context and `issuerScope`; `vetted/1` example alignment |
| `trustoverip/dtgwg-vsc-registry` | `7c5ba6c8114dc64cdfe8356992f46850a0d8ead1` | VSC predicate registry; `vetted/1` and `presented/1` draft entries; commit/digest pin model |
| `OpenVTC/dtg-credentials` | `1d49eaf17a5002817370426554d312db2ed19b09` | pre-migration 0.11.0 credential implementation baseline |
| `OpenVTC/verifiable-trust-infrastructure` | `32ddd2f231474104535830ab05a52a66527c61ac` | VTA/VTC implementation baseline |
| `OpenVTC/openvtc` | `e49816c5f6c49d2d2d2f656d8e20507133e00c01` | OpenVTC client/member implementation baseline |
| `trustoverip/dtgwg-trust-tasks-tf` | `9a104be3b9b7302cab64adf779079ab5be69c4c2` | Trust Tasks implementation/specification baseline |

### Baseline interpretation

The specification/registry side has already advanced beyond the timestamped upstream snapshot:

- `vetted/1` and `presented/1` are present in the registry as draft;
- cred-spec has aligned the identity-vetting worked example to `vetted/1` and camelCase values.

The implementation side is still pre-cut-over at this freeze:

- `dtg-credentials` does not expose `issuerScope` or `StatementCredential`;
- VTI still contains `IDENTITY_VETTING_ENDORSEMENT_TYPE` and `CommunityRole` VEC semantics;
- OpenVTC still maps role credentials to `EndorsementCredential`;
- no `issuerScope` implementation was found in the current OpenVTC baseline.

Therefore this manifest is a **pre-migration control baseline**. Failure of current `main` to emit the target shapes is not itself a defect; target-conformance evidence must be collected against the implementation revisions that actually perform the migration.

## Upstream-declared unresolved inputs

The migration source explicitly leaves these open:

1. exact type name and context for the plain W3C identity-verification credential in flow 9;
2. role → VAC `authority.actions` vocabulary and whether registry #17 owns shared values;
3. whether VIC `scopes: role:<name>` remains or is replaced by authority issued at admission;
4. `vetted/1` remains draft while cred-spec #38 and #58 may still change digest/task-citation properties.

These remain design dependencies, not assumptions RAHP may fill in.

## Historical RAHP applicability

| Historical item | LPC migration scope |
|---|---|
| R-01 proof-required task vs bearer/session equivalence (#767) | IN-SCOPE / RETEST where signed credential-delivery/admission Trust Tasks are exercised |
| R-02 operation-bound step-up (#795/#799) | OUT-OF-SCOPE unless privileged admin/step-up enters actual run |
| R-03 proofPurpose/key-role binding (#820) | IN-SCOPE / RETEST |
| R-04 acceptance-window semantics (#833) | CONDITIONAL on async discovery/delivery |
| R-05 admission lifecycle (#798) | IN-SCOPE / RETEST |
| R-06 Trust Tasks × Credential Spec non-inference (#781) | IN-SCOPE / RETEST |
| R-07 Trust Tasks × ZKP (#780) | CONDITIONAL on ZKP/personhood/hidden-vetter path |
| R-08 source-pinned composition (#225/#228) | IN-SCOPE / mandatory |
| #609 live VAC status/policy freshness | IN-SCOPE / KNOWN-RESIDUAL when VAC authority is consumed |
| #837/#826 step-up residuals | OUT-OF-SCOPE unless step-up is demonstrated |
| #836 recipient-advertised windows | CONDITIONAL |
| #310/#338/#339 correlation/privacy | IN-SCOPE where `issuerScope` or presentation composition creates a privacy proposition; DPIP owns conclusion |
| #849 hidden-vetter PCS | OUT-OF-SCOPE unless `vetting-pcs` is enabled |

## Migration-specific assurance propositions

The detailed durable owner is #868. The campaign will test:

- atomic/coherent cut-over without ambiguous old/new acceptance;
- truthful and enforced `issuerScope`;
- VEC-role → VAC authority non-escalation;
- VSC `vetted/1` / `witnessed/1` semantic and task-citation preservation;
- correct non-DTG IDVC boundary;
- fail-closed predicate accept-list behavior;
- Trust Task schema/IRI/type convergence;
- non-inference across membership, authority, statements, personhood evidence and outcomes.

## Evidence-template selection

From `docs/lpc-pre-demo-evidence-templates.md`:

- Family A — selected for VAC/action-time authority and policy decisions.
- Family B — selected for signed credential delivery and admission.
- Family C — not selected unless step-up enters runtime scope.
- Family D — selected for signed Trust Task delivery/presentation.
- Family E — selected for replay/freshness/task citation; acceptance-window subcases conditional.
- Family F — selected.
- Family G — selected.
- Family H — selected.
- Family P — selected for `issuerScope`/cross-context claims; DPIP conclusion required.
- Hidden-vetter-specific P7 — not selected unless the feature is enabled.

## Freeze rule

When migration implementation revisions land, do **not** overwrite this baseline. Record a second target pin set and compare baseline → target.

The final LPC record must distinguish:

1. upstream-declared target semantics;
2. pre-migration baseline;
3. actual migrated implementation pins tested;
4. target-native runtime evidence;
5. remaining known residuals/design dependencies.

