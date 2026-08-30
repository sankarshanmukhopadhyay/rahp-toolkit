# Upstream routing ledger — RAHP #293

Run: `dtg-canonical-clean-room-293-faed4f07`

This ledger records the **action owner** for every material non-PASS proposition. It is intentionally separate from the assurance judgment: routing a finding upstream does not change the finding, and inability to create an external issue does not erase the action.

## U-01 — OpenVTC DTG Credentials VWC digest interoperability

- RAHP finding: `DTG-COMP-005`
- Result: **FAIL**
- Owner: **OpenVTC/reference-implementation**
- Target: `OpenVTC/dtg-credentials`
- Pinned revision: `fcae96171d95b4bae55a2e1ead22c52413da2a57`
- Type: implementation/specification alignment
- External issue creation from the connected integration: **blocked by GitHub 403 / Resource not accessible by integration**

### Proposition

The current library should produce and verify Witness Credential digests compatible with DTG Core Credentials Working Draft 01 when it claims that profile.

### Evidence

The pinned README explicitly warns that its VWC `digest` encoding diverges from Working Draft 01 and that VWCs produced by the library will not interoperate with spec-conformant implementations in either direction.

### Minimum acceptable resolution

Either align generation/verification with the current normative algorithm, or explicitly version the incompatible implementation profile and prevent callers from mistaking it for current-spec VWC support. Add independent positive/negative conformance vectors and a cross-implementation round-trip test.

### Counter-case / non-defect boundary

The normative DTG Core Credentials specification is not failed by this finding. An implementation that follows the current digest algorithm is outside the defect.

### Falsification condition

A pinned implementation revision passes current-spec vectors in both generation and verification, including rejection of the legacy incompatible encoding where required.

---

## U-02 — Member-issued VMC withdrawal/status discovery

- RAHP finding: `DTG-COMP-004`
- Result: **INDETERMINATE**
- Owner: **DTG-spec-upstream**
- Primary target: `trustoverip/dtgwg-cred-spec`
- Composition partner: Trust Tasks / status-discovery work
- Pinned revision: `2b403b607aaec9d84f78189a55337c677f3cd2ed`
- Type: normative composition dependency
- External issue creation from the connected integration: **blocked by GitHub 403 / Resource not accessible by integration**

### Proposition

A verifier relying on the two-sided VMC membership edge needs a member-controlled way to establish that the member-issued acknowledgement remains current and has not been withdrawn.

### Evidence

The current spec explicitly defers withdrawal/revocation/re-issuance and status discovery for the member-issued VMC. It states that until this mechanism exists a verifier can match the acknowledgement to the grant but cannot learn that it has since been withdrawn.

### Minimum acceptable resolution

Define or normatively bind a member-controlled status/currentness mechanism, unavailable/stale failure semantics, re-issuance behaviour, and privacy constraints for the lookup path. Provide conformance cases for withdrawn, stale, unavailable and re-issued acknowledgements.

### Counter-case / non-defect boundary

A deployment using short validity windows may bound exposure, but that does not create a general status/currentness mechanism.

### Falsification condition

A current normative composition provides a member-controlled status path and a verifier can deterministically distinguish current, withdrawn, stale and unavailable states without depending on the community to withdraw the member's own acknowledgement.

---

## U-03 — Fresh cross-transport Trust Task conformance

- RAHP finding: `DTG-COMP-003`
- Result: **INDETERMINATE**
- Owner: **OpenVTC/reference-implementation + Trust Tasks binding maintainers**
- Targets: `OpenVTC/verifiable-trust-infrastructure`, `trustoverip/dtgwg-trust-tasks-tf`
- Type: evidence-production / interoperability

### Proposition

The same consequential Trust Task semantics should survive the supported transport choices, including lifecycle state, failure, continuation, task consent and stale-policy behaviour.

### Evidence

The canonical Trust Tasks framework requires each transport binding to map semantic lifecycle states. The pinned VTI TSP guide states TSP is experimental/off by default and its runtime message paths should be validated against a live mediator before production. No fresh #293 multi-transport runtime run exists.

### Minimum acceptable resolution

Produce one pinned conformance wave exercising an equivalent task over each claimed transport, including success, error, continuation/blocked state and at least one authorization/consent transition. Record semantic outputs, not just transport success.

### Counter-case / non-defect boundary

A deployment that uses only a single fully supported transport need not claim cross-transport equivalence.

### Falsification condition

Equivalent task fixtures produce contradictory semantic state or authorization results across transports under equivalent policy and inputs.

---

## U-04 — Privacy/correlation runtime evidence

- RAHP finding: `DTG-COMP-012`
- Result: **INDETERMINATE**
- Owner: **DPIP / evidence-production**
- Examination: `sankarshanmukhopadhyay/dtg-privacy-implementation-profile#146`
- Type: privacy specialist examination

### Proposition

Composing credentials, ZKP, Trust Tasks, relationship graph/status and verifier state must not silently expand correlation beyond the declared context.

### DPIP result

`INDETERMINATE / evidence-required`

Fresh #293 evidence statuses:
- `ER-REL-DID-AB`: `NOT_EVIDENCED`
- `ER-STATUS-AB`: `NOT_EVIDENCED`
- `ER-TASK-AB`: `NOT_EVIDENCED`
- `ER-VERIFIER-AB`: `NOT_EVIDENCED`

### Minimum acceptable resolution

Generate a new pinned runtime package within a new lineage using positive controls plus context-distinct unlinkability cases. Include relationship identifiers, status/policy lookup, retained task/outcome evidence, verifier transcript/challenge, and relevant personhood/nullifier/transport metadata.

### Counter-case / non-defect boundary

Stable identifiers deliberately reused inside one declared relationship/context are not by themselves a privacy violation. The adverse condition is unintended linkage beyond the declared scope.

### Falsification condition

A join appears across contexts where the declared policy requires `must-not-emerge`, and the correlator is target/composition-derived rather than deliberately fixture-supplied.

---

## U-05 — Cross-portfolio correction/redress contract

- RAHP finding: `DTG-COMP-014`
- Result: **INDETERMINATE**
- Owner: **composition-owner / future VTI specification**
- Type: composition/governance

### Proposition

A composite implementer needs deterministic handling for stale or contradictory evidence, unavailable authority/status, correction, challenge and remediation across credential, relationship, task and personhood decisions.

### Evidence

Trust Tasks provides strong task failure/lifecycle semantics and VTI implements several local correction/revocation/consent paths, but this clean-room run did not establish one normative cross-portfolio redress contract.

### Minimum acceptable resolution

Publish a composition-level matrix mapping material failure classes to responsible authority, retry/correction semantics, evidence update, revocation/supersession and user/operator remediation.

### Counter-case / non-defect boundary

A component-specific failure path can be correct locally without constituting a whole-portfolio redress model.

### Falsification condition

A current composition document unambiguously routes all material failure classes and has executable examples for contradictory, stale and unavailable-authority states.

---

## U-06 — Immature/optional portfolio layers

- RAHP finding: `DTG-COMP-015`
- Result: **FAIL_BOUNDED**
- Owners: VDS / Agent Names / HTX workstreams
- Type: maturity/scope

### Evidence

- VDS pinned README says the repository **will be** the home of DTG VDS V1.0.
- Agent Names pinned repository presents task-force framing without a normative deliverable found in this run.
- HTX is currently an artifact/workspace surface rather than a normative technical conformance source.

### Required disposition

Do not present these layers as uniformly implementation-ready normative dependencies. A composite profile should mark them optional/experimental/planned until a stable deliverable exists.

### Falsification condition

A pinned normative deliverable with versioned conformance requirements is present and explicitly included by the composite profile.
