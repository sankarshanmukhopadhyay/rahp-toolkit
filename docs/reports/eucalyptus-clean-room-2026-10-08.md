---
layout: default
title: "Eucalyptus clean-room campaign"
parent: Reference
nav_order: 12
has_toc: true
---
# Eucalyptus clean-room RAHP campaign — 2026-10-08

Campaign tracker: [#960](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/960).

**Campaign execution completes independently of its assurance outcome. Eucalyptus remains INDETERMINATE.** This is an AI-assisted, source-pinned assessment proposal, not a human risk-acceptance decision, independently conducted audit or VTI conformance grant.

The [campaign contract](../../profiles/dtg/eucalyptus/campaign.json) covers all 18 coordinated `VTI-Eucalyptus` repositories, pinned to full commit and annotated-tag object identities. The Interop Lab and DPIP are separately pinned auxiliary producers, outside the coordinated release. Fresh source collection, current test attempts, explicit human-harm coverage and producer admission are separated from historical assessment outcomes.

## Run the delivered flow

Use Python 3.11 or later, Git and Node 24. Install RAHP dependencies:

```bash
python3 -m pip install -r requirements.txt
python3 tools/eucalyptus_campaign.py --workspace /tmp/eucalyptus-fresh-960
python3 tools/eucalyptus_campaign.py --verify-package /tmp/eucalyptus-fresh-960/output
```

The workspace must not already contain assessment output. Each source tag and commit is verified before evidence collection; unexpected source modification stops execution. `--reuse-sources` is only for a freshly precollected, clean, exact-pinned source set; it never imports prior verdicts or prior evidence output.

The existing **Clean-room assurance executor** workflow accepts `run_mode=eucalyptus`. This extends the governed executor without adding another workflow. The command attempts locked JavaScript dependency acquisition, each registered component suite, Lab room/privacy handoffs and DPIP's portable incomplete-evidence interpretation; it writes attributable attempts even when runtimes, external hosts or source-compatible producers are unavailable. An acquisition/orchestration error returns nonzero with `execution-failure.json`; a completed INDETERMINATE assessment is a valid result and returns zero.

Rust, Go, Dart and Apple platform prerequisites are not synthesized. To broaden native coverage, provision the exact versions required by the pinned manifests before triggering the same command. Each registered suite has a bounded timeout; changing that budget changes the campaign contract and identity. Installing a newer compiler or matching a coordinated date is not evidence of dependency or composition compatibility.

## What the package contains

The durable assessment is under [the Eucalyptus review directory](../../instances/dtg/reviews/eucalyptus-2026-10-08/summary.json). Its evidence archive preserves the complete generated output, including full logs, source and assessor provenance, lockfile package inventory, environment diagnostics, source observations, proposition matrix, portable specialist return, terminal records and integrity manifest.

To inspect and verify the archive:

```bash
python3 -m zipfile -e instances/dtg/reviews/eucalyptus-2026-10-08/evidence.zip /tmp/eucalyptus-evidence-960
python3 tools/eucalyptus_campaign.py --verify-package /tmp/eucalyptus-evidence-960
```

The integrity manifest detects changed, deleted and injected evidence against its stored root. It is not a digital signature or independent attestation. Exact code hashes accompany the assessor base commit because this initial execution used the tested campaign implementation before its publication commit existed. Reproduction must match both source pins and implementation hashes; the eventual GitHub merge identity is not falsely substituted into the original execution.

## Measured execution

- 18 coordinated source repositories and 2 separately pinned auxiliary producers.
- 20 consequential propositions, all INDETERMINATE; zero composition PASS.
- 65 registered attempts: 43 EXECUTED_PASS, 4 EXECUTED_NONZERO, 18 ATTEMPTED_UNAVAILABLE.
- 295 passing standalone Node test checks, plus successful browser workspace tests and static Trust Task binding/ceremony/package checks. These are not an aggregate conformance grant.
- 574 RAHP repository tests passed, including 16 campaign tests covering real end-to-end replay, commit/tag pin mismatches, dirty sources, path escape, output reuse, missing tools, timeout, zero-test success, evidence tampering and component-to-composition inference boundaries.

The four nonzero attempts are preserved: mediator-auth SSRF positive control, external live-DID resolution, deployment PID-command matching and the RP SDK JCS fixture precondition. Their diagnostics are recorded separately; none is declared an independently confirmed Eucalyptus vulnerability.

## Inference boundaries established by fresh inspection

1. **Second-party consent is configuration-dependent.** The tagged `vtc-service/src/acl/single_admin.rs` documents a host-configured single-administrator mode that can waive consent even when multiple administrator identifiers exist. `vtc-service/src/config.rs` defaults the mode to false. The node cannot determine whether multiple identifiers represent distinct people. This qualifies the release headline; it does not demonstrate an exploit or establish independent people from key cardinality.
2. **Coordinated tags do not establish consumed dependency provenance.** Lockfile identities and checksums are inventoried separately from the tagged repositories. No claim that every consumer used those exact coordinated source trees is inferred from shared release naming.
3. **Older producer contracts reject this release.** The pinned Lab room and Track-A A/B adapters were invoked with the Eucalyptus checkout. Their target guards reject older fixed revisions instead of generating a misleading fresh PASS. No pin was patched out.
4. **DPIP's return does not invent an observation.** The declared privacy input says `executed=false`, `signal=not-tested` and explicitly prohibits interpreting `effective_join=false` as an observed no-join result. DPIP produces a portable INDETERMINATE return. Native context, status, policy, transcript, retained-evidence and hidden-vetting observer captures remain required.
5. **A failing test is diagnosed at its actual failure boundary.** The RP SDK's original deep-array test overflows in `JSON.stringify` before calling the canonicalizer. A separate direct probe checks the tagged canonicalizer at 5,000 levels, the permitted depth and one level beyond; it does not edit or waive the original test. SSRF positive-control failures are read alongside actual DNS diagnostics; live-DID tests need their external host; PID matching is read alongside the actual process/procfs view.

## Coverage and unresolved evidence

Twenty explicit persona/scenario/harm/control propositions cover sender binding, authority/delegation, ACL exceptions, approval independence, replay/restart, transport compatibility, rooms/custody, hidden vetting, personas, forge control/signing, mediator administration, SSRF/resolution, audit/redress, hybrid proofs, registry reliance, mobile approval, memory injection, RP sessions, consumed dependencies and accessibility/exclusion.

The machine record keeps **RAHP, security, composition, DRARM and specialist** lens dispositions explicit. Passing component vectors remain bounded evidence. Deployment-native multi-service traces, induced-failure/recovery evidence, observer captures, native device journeys and human governance evidence are not replaced with synthetic fixtures.

No Eucalyptus-wide PASS, independently confirmed vulnerability or historical finding closure is asserted. Each unresolved proposition has a named owner, pressure cases, required evidence and retest condition in the campaign contract and generated matrix. The owner fields identify proposed technical responsibility; they do not assign work to upstream maintainers or claim their acceptance.

## Post-seal historical reconciliation

The historical September campaigns are preserved, including the [September 24 handoff](../../reports/dtg-vtc-clean-room-assurance-2026-09-24.md) and its later [delta assessment](dtg-vtc-post-clean-room-delta-2026-09-24.md). They were read for reconciliation after the first fresh Eucalyptus result was sealed, and are not executable inputs to this campaign.

| Earlier evidence family | Fresh Eucalyptus disposition |
|---|---|
| Bounded VDC/VAC non-substitution PASS | Not inherited. Current native credential/task consuming evidence is required under EUC-02. |
| Historical VDC scope/acceptance divergence | Not reasserted from old string searches. Current source tests are identified; adopted-specification conformance needs its own exact normative/implementation closure. |
| Actuation, replay and use-time binding | New exact target and tests recorded under EUC-01/02/05. Old native adapters reject the new target; older PASS cannot transfer. |
| Status, policy, retained evidence and correlation | Fresh missing-observation declaration and DPIP return under EUC-08/09/12/13. No aggregate privacy PASS inherited. |
| Normative/realization separation | Still an assessment boundary; it does not certify Eucalyptus conformance to unpinned external specifications. |
| ZKP, VDS and Agent Names compositions | Outside this coordinated-release subject unless their actual consumed dependencies and normative obligations are independently bound. PCS is not silently equated with those earlier specifications. |

The enlarged release scope and changed source identities prevent defensible closure of earlier residuals by analogy. This campaign establishes a new assessment baseline and precise evidence obligations; it does not erase older issues or count their conclusions as current observations.
