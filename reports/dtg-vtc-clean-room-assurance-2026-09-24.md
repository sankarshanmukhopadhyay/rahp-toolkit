# DTG/VTC clean-room assurance handoff — 2026-09-24

Assessment epoch: **2026-09-24**  
Campaign: `DTG-VTC-FULL-CLEAN-ROOM-2026-09-24`  
Campaign issue: #772  
Evidence run: https://github.com/sankarshanmukhopadhyay/rahp-toolkit/actions/runs/35964821717  
Overall posture: **AMBER / INDETERMINATE**

> This is the durable repository summary of the campaign. The complete handoff is also generated as Markdown and HTML for external/upstream circulation.

## Severity

- **S0 Critical** — unauthorized consequential action, systemic authority failure, severe privacy/security compromise, or invalid assurance across the stack.
- **S1 High** — materially weakens authorization, lifecycle, proof/replay, privacy, or interoperability across a meaningful composition boundary.
- **S2 Medium** — bounded semantic, operational, provenance, redress, implementation-divergence, or assurance-process weakness.
- **S3 Low** — clarity, diagnostics, documentation, adoption, or low-impact consistency weakness.

## Priority

- **P0 Immediate** — blocks defensible assurance or creates a current high-risk interoperability/authority ambiguity.
- **P1 Near-term** — material gap for the next active specification/implementation tranche.
- **P2 Planned** — bounded scheduled maintenance/profile work.
- **P3 Monitor** — insufficient evidence, external blocker, or observation requiring future reassessment.

Priority is independent of severity.

## Current terminal result

The corrected source-pinned clean-room run returned:

- PASS: **2**
- FAIL: **0**
- INDETERMINATE: **8**
- NOT_APPLICABLE: **0**
- Portfolio posture: **AMBER**
- Terminal state: `TERMINAL_INDETERMINATE_EVIDENCE_REQUIRED`

The run terminated without stranding.

### Verified propositions

1. **P01 — delegation/current-authority non-substitution: PASS / verified.**
   Eight source-pinned Interop Lab negative vectors matched their expected deny/allow outcomes.
2. **P10 — normative/realization separation: PASS / verified.**
   RAHP preserves specification state separately from implementation realization state.

### Current actionable findings

| ID | Severity | Priority | Class | Disposition |
|---|---|---|---|---|
| CUR-01 | S1 High | P0 | implementation divergence | Current `OpenVTC/dtg-credentials` exposes a VDC constructor but the assessor does not observe adopted `delegation.scope` / `delegation.accepts` surfaces. Confirm supported baseline; implement conformance or explicitly scope non-support. |
| CUR-02 | S1 High | P0 | evidence gap | No current end-to-end credential → Trust Task actuation trace proves the authorization boundary. |
| CUR-03 | S1 High | P0 | evidence gap | No current cross-layer replay/idempotency trace proves retry/replay cannot create a second authorization/effect path. |
| CUR-04 | S1 High | P1 | evidence gap | Presenter/subject/controller/relationship binding is only partially verified across complete composed paths. |
| CUR-05 | S1 High | P1 | evidence gap | Effective correlation remains unresolved for status/policy discovery and retained task/evidence surfaces. |
| CUR-06 | S1 High | P1 | evidence gap | Capability/key/proof validity/current authority non-collapsibility is not yet proven at consequential actuation boundaries. |
| INT-01 | S2 Medium | P0 | assurance infrastructure | DTG cross-spec profiles still use `dtgwg-zkp-tf` while current ZKP specification work is present in `dtgwg-zkp-spec`; authority/currentness must be reconciled explicitly. |
| INT-02 | S2 Medium | P0 | assurance routing | #771 reports 30 qualifying 2026-09-24 material changes, 20 still UNMAPPED. Blanket reuse of earlier portfolio conclusions is not defensible. |

An evidence gap is **not** asserted as an upstream defect. It is a condition that blocks a defensible PASS.

## Cross-specification reconciliation

All eight maintained cross-spec review packages executed and validated during the campaign, producing durable issues #774–#781.

Their underlying assessments are dated **2026-08-19 through 2026-08-30**. The workflow proved the retained packages are internally valid; it did **not** prove that their historical findings remain current at 2026-09-24 pins.

The retained corpus contains **23 open historical residual findings**:
- eight historically Critical authority/lifecycle composition findings;
- the remainder historically High context/provenance/privacy/replay/scope findings.

They must not be bulk-filed upstream unchanged.

Material source movement confirms that current-pin reassessment is necessary:
- Trust Tasks is 285 commits ahead of the pin used by the 2026-08-30 Trust Tasks × Credential review;
- Credential Specification is 30 commits ahead of its corresponding pin;
- maintained `dtgwg-zkp-tf` is 6 commits ahead of the older ZKP baseline;
- current ZKP specification work is also present in the separate `dtgwg-zkp-spec` repository.

## Durable successor work

- #782 — current-pin rebaseline of all eight maintained cross-specification compositions, including explicit ZKP authority reconciliation.
- #783 — current runtime/composition evidence for P03–P09 using Interop Lab and DPIP where applicable.
- #771 — disposition the remaining unmapped 2026-09-24 Portfolio Monitor findings.

## Upstream handoff rule

File upstream only when a current-pin reassessment supports a concrete normative or implementation proposition and identifies the correct owner. Preserve the RAHP issue/evidence provenance and a falsifiable retest condition.

No fresh portfolio proposition in this campaign returned FAIL. **AMBER is not FAIL, but it is also not sufficient evidence for an end-to-end GREEN claim.**
