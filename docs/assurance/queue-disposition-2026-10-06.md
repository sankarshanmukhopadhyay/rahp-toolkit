# DTG assessment queue disposition, 2026-10-06

Controllers: #903, #904, #906. Bounded security owner: #121.

## Disposition

The three controller epochs contain **42 unique qualifying finding identities**. Every identity has an explicit scoped judgment or durable successor. The controllers can close after this record is integrated and the transfers are journaled. Their closure does not discharge the remediation and evidence obligations owned elsewhere.

Machine-readable ledger: [queue-disposition-2026-10-06.json](queue-disposition-2026-10-06.json). It retains every original epoch membership, source evidence reference, original route, revised route, owner and evidence/lifecycle boundary. Original snapshot digests are never rewritten after routing-policy changes.

| Controller | Exact digest | Qualifying findings | Previously UNMAPPED |
|---|---|---:|---:|
| #903 | `424871d7c9b3dc0e591d7d24d8903aa3d52757905f2c189462b1dce68117ed60` | 38 | 12 |
| #904 | `3cd6ab51728fe8b0f4bd4be64650673acc65cc8aa1f759322f5e2263c652dae8` | 34 | 12 |
| #906 | `d0a3ba5d06239fb73e2bc71def7b299e936350b95330cc289ed93e8eadfc5d8c` | 33 | 12 |

The October 5 snapshots were recovered from Portfolio Monitor commits `5d194c462bb3f5a6fe8ef86721b517e367cc51e5` (#903) and `a99277a717aab9795b7a0d545dade82fc8c9a268` (#904), at `data/findings/2026/10/05.json`. Canonical SHA-256 recomputation matches both recorded digests. The consumed October 6 content likewise matches #906. The ledger freezes its finding memberships even if the date-path is subsequently republished.

Nine #903 findings are absent from #906. #904 has one absent finding, already among those nine. These are retained below; disappearance from a later snapshot is not disposition.

| Finding | Scoped disposition / owner |
|---|---|
| `85c10c447fe2bf69052a` | Acceptance-window advertisement: #833's receiver assessment; producer-side residual #836 remains open. |
| `9b878baa95c8420e8f4f` | Document-size declaration: no separate assessment; no claim of complete resource protection. |
| `e5af88bcba73c7130754` | Trust Tasks Rust 0.24.4: already assessed in #272's October 5 closeout. |
| `d0b4877d8f5fc4d042e7` | DTG context: #474 historical convergence, #901 current migration record. |
| `443903313fccfb3b9ce1` | Maximum document-size metadata: bounded no-action. Also present in #904. |
| `d11cec7798af5427c356` | Discovery 0.3 framework: historical framework coverage; #836 retains producer-window divergence. |
| `4a78b036a20513c8730a` | issuerScope privacy: #835/#880 specialist lineage, non-terminal obligation #338. |
| `36667a59ec26933c6b5d` | VTA service release aggregation: inherits constituent dispositions. |
| `d3caae6859705301f7c9` | Late collection: #833 receiver/freshness evidence; #836 producer-window residual. |

## Fresh #121 bounded source review

Frozen sources:

- VTI: `4b5618f30372d7479a18f379e67fc00411de38da`.
- Trust Tasks: `7b6bb488ffd838bef058310c909207d4a7b77125`.
- VTI specification: `6a3041e88650126e0ca47869ac03dc069d026636`.

### Qualified git capabilities: source-supported preservation

Finding `18828d1335ff069040c5` moves git rights into `resourceGrants` on live ACL entries. `vtc-service/src/acl/resource_grant.rs` keeps repository grades distinct: namespace creation does not confer management over existing repositories; maintain does not confer ownership. Grants retain granter, expiry and resource qualifiers. The observed authority model is more coherent than a parallel rights store; it does not establish timely external forge convergence by itself. #797 retains projection/normative alignment, and #609 retains applicable live authority/status freshness.

### Signed administrative reads: source-supported strengthening

Finding `6746383deb0d6dae2e0b` is supported by `git_ns/tasks.rs` and `git_ns/admin_reads.rs`: declared proof requirements are enforced by the dispatch spine, the actor is a verified signer rather than a payload identity, and current capability/namespace standing governs disclosure. Repository-native tests in `git_ns/tests.rs` exercise unsigned namespace/repository/view reads and a namespace administrator asking outside its scope. These are inspected tests, not newly executed Rust results.

### Retirement of member-facing REST: source-supported preservation

Finding `c5ae0ee9c8cc64e6b2b8` is supported by the actual route table in `routes/mod.rs`, the member/surface Trust Task handlers and `tests/it/surface_verbs_spine.rs`. Renewal, DID rotation, personhood and relationship operations use explicit signed-document paths and operation-specific authority gates. This does not turn transport authentication into universal permission, nor close #691's structured-error contract or #836's recipient-window residual.

### Administrative consent topology: explicit exception, not independent-person proof

The five previously UNMAPPED authority findings are already assessed in closed #897. VTI-APV-022 now explicitly permits a host-configured single-administrator mode whether or not several administrator identifiers exist. `acl/admin_consent.rs` implements that declared waiver. `config_store.rs` excludes the mode from remote patch/import; the action-list response reports it; `tests/it/single_admin_mode.rs` explicitly tests that a second identifier does not restore consent. The host assertion that all administrator identifiers represent one person is an external governance assumption, not cryptographic evidence of independence.

`tests/it/acl_self_edit.rs` separately tests label-only self-edit, refusal of label-plus-authority changes, and mode/step-up restrictions. `admin_actions/mod.rs` rechecks current authority and state pins before executing stored decisions. Pending reductions have real effective suspension semantics: `tests/it/cooling_off_suspension.rs` and `action_list_a2.rs` establish the intended first-to-act behaviour, cancellation restoration, restart reconciliation, typed immediate removal and offline-write acknowledgement. Offline acknowledgement is retrospective visibility, not prior authorization. #610 retains cross-boundary contestability, and #837 retains its exact expiry/intervening-authority evidence requirements.

**Fresh adverse finding: #908.** Mandatory Critical audit emission fails open when `audit_writer` is absent. `acl/single_admin.rs::write` returns success without a writer; `authorize_self_edit` and `admin_actions/mod.rs::spend_waiver` likewise authorize after conditional audit writes. This contradicts VTI-APV-022 item 4 and the source comments asserting that unrecorded waivers cannot land. Present-writer write errors are propagated; writer absence is the distinct branch. This is a source-contract FAIL, not a claim of an executed exploit. #908 owns target-native absence/write-failure tests and remediation.

**#121 disposition:** bounded assessment complete, with source-supported strengthening/preservation and an explicit FAIL transferred to #908. Historical #897 remains immutable; no blanket authority PASS is asserted.

## Previously UNMAPPED ownership

| Group | Finding identities | Assessment / residual owners |
|---|---|---|
| Community identity/predicate migration | `8489f5ccddf1ae91ca45`, `81050504f25c51f89236`, `b3bbc613f0e4c0d0f231`, `5f600796a207a69d9b4a` | #870 and integrated #901 migration record; runtime privacy is separate. |
| Administrative lifecycle | `8d5718ce13e794725aab`, `f4cdc35d8f2c782f247c`, `09ccb1d242fb33d91c00`, `8d8326aa785c31620f36`, `adde5ccf990f1abb1fdd` | #897 historical assessment; #121 current review; #908 fresh audit FAIL; #837/#610/#609 scoped residuals. |
| Approved-join redelivery | `7dd4cece89d11aac5a8a` | #898: historical-removed member resend remains FAIL at current source. |
| Signing-key replacement | `ec101912064707597281` | #899: revoke-old then enrol-new remains non-atomic at current source. |
| Published PCS dependency | `f5ad8aa1399207519fb6` | #849 completed assessment; #889 attributable runtime privacy evidence remains required. |

PCS is off by default and explicitly feature-gated. Current manifests/lockfile resolve `predicate-credential-system 0.1.0` with registry checksum `ca56c675955e5b667c886572087f32f61687e51ec62843b3f32b296b87f472d8`. Publication does not establish unlinkability. Current documentation and #849/#888 preserve the retained composition/privacy boundary; no duplicate specialist referral is needed without new comparable evidence.

## State and routing corrections

- #902 was reviewed and merged as `d1584326bea9b748da029fe171b77a0e7c1419d1`; its observed validation, TypeScript conformance, impact and build checks passed. #901's artifact integration gate is satisfied.
- #272's October 5 disposition explicitly covers all three release identities in the controller union; it can close without a new assessment.
- #338 was closed despite a current `evidence-acquirable` body and #905/DPIP #295 INDETERMINATE transfer. It is reopened as the same durable semantic obligation; specialist history is unchanged.
- SDK finding `a775c9693b223f68a751` was incorrectly routed as release/no-action. Preserving rejection code/details changes observable failure semantics. The classification is corrected to #691 ownership.
- The instance normalization/routing repair maps all twelve recurring UNMAPPED findings. Administrator changes remain combined reviews under #121's existing stable key; known remediation/evidence coverage does not imply PASS. Unclassified material semantics still route UNMAPPED.

## Evidence and completion boundary

The new routing regressions exercise the twelve actual observations, error-versus-release precedence, durable owner preservation, repeated administrative observation identity, unrelated repositories and unseen predicate semantics. Baseline classification is twelve UNMAPPED plus one erroneous no-action; the repaired fixture is eight covered plus five combined reviews.

No Rust toolchain is available here. External target-native tests were inspected and their paths recorded; no new target-runtime PASS or feature-enabled Rust execution is claimed. Local validation passed: 457 unittest cases, full artifact/schema validation, DTG routing validation and git diff whitespace checks. CI must also pass before integration. These checks establish the routing change, not upstream runtime remediation.

Close the controller epochs only after the ledger is on main and the exact snapshot obligations are journaled on their owners. #908/#898/#899 remediation, #338/#889/#531 privacy evidence, and the remaining scoped external obligations stay open.
