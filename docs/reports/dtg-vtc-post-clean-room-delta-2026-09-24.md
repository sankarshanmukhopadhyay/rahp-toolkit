---
layout: default
title: "DTG/VTC post-clean-room assurance delta — 2026-09-24"
nav_exclude: true
---
# DTG/VTC Post-Clean-Room Assurance Delta Report — 2026-09-24

**Purpose:** upstream-facing reconciliation of clean-room campaign #772 after current execution evidence (#783), materiality-driven RAHP execution (#785/#787), and the current-pin cross-specification rebaseline (#782).

## Executive conclusion

A second full #772-style campaign is not warranted. The current rebaseline confirms that the original clean-room result should evolve through proposition-scoped evidence and current-pin reconciliation rather than another wholesale execution epoch.

The current cross-specification posture remains **AMBER / INDETERMINATE** across all eight maintained seams. This is not a regression. Current Credential, Trust Tasks and ZKP text materially strengthens authority separation, task/outcome binding, replay resistance, audience/context binding, lifecycle semantics and privacy framing. Fresh Interop evidence under #783 also establishes bounded execution for Trust Task to credential integration, replay convergence, VAC use-time authority and several A/B privacy surfaces.

What remains is narrower: live status/policy freshness, target-attributable privacy evidence, demonstrated ZKP integration, and current executable closure for VDS and Agent Names composition seams.

**No historical RAHP finding is promoted by this rebaseline into a newly proven upstream defect.**

## Severity and priority

Severity measures consequence if a finding is true. Priority measures how urgently the next action should occur.

| Severity | Meaning |
|---|---|
| S0 Critical | Unauthorized consequential action, systemic authority failure, severe privacy/security compromise, or invalid assurance. |
| S1 High | Material weakness in authorization, lifecycle, proof/replay, privacy or interoperability across a composition boundary. |
| S2 Medium | Bounded semantic, operational, provenance or assurance weakness with credible but limited impact. |
| S3 Low | Clarity, diagnostics or low-impact consistency issue without demonstrated material failure. |

| Priority | Meaning |
|---|---|
| P0 Immediate | Blocks defensible current assurance or leaves a high-risk authority/interoperability ambiguity. |
| P1 Near-term | Material gap for the next active specification/implementation tranche. |
| P2 Planned | Bounded issue suitable for scheduled maintenance. |
| P3 Monitor | Evidence insufficient for action, externally blocked, or informative only. |

Priority is not mechanically derived from severity.

## Current authority baseline

| Surface | Current pin | Role |
|---|---|---|
| Credential Specification | 1152a523c85febfb6b9b0b597a0783b6cdab884a | specification |
| Trust Tasks | fe099568c278edceb93bcca8249c349be4184148 | specification/framework |
| ZKP Task Force | a42bf8c06875cde7c2c9b578279c1be2c682f8ba | requirements, discussion and requests |
| ZKP Specification | cfd94063e5cfee7ba6df4dcfd28c10399a0ffd0a | specification and conformance apparatus |
| VDS | 99eacacedd1729d20528a2ec65ff5288d103ec5e | specification source |
| Agent Names | 962591709e260616aba066bf08865962f6851bf3 | specification source |

The ZKP authority transition is explicit: the Task Force repository remains requirements/discussion lineage, while dtgwg-zkp-spec owns the current specification and conformance apparatus.

## Delta from #772

#772 ended with two verified portfolio propositions and eight evidence-required propositions. #783 has since produced current-epoch evidence for bounded Trust Task to credential integration, replay/duplicate-effect resistance, VAC use-time authority, presenter/subject/action/scope binding, status A/B observation, policy-discovery A/B observation and retained-task/evidence A/B observation.

That evidence narrows several #772 uncertainties but does not justify synthetic aggregate PASS:

- #609 still owns live VAC revocation/status, policy lookup and freshness/propagation.
- #310 still owns target-attributable credential/proof identifier correlation evidence.
- ZKP's current integration text still describes Trust Tasks binding as an integration target, not demonstrated interoperability.
- VDS and Agent Names have not moved in ways that provide fresh executable composition closure.

## Current composition dispositions

| Composition | Execution class | Priority | Current result | Delta from historical assessment |
|---|---|---:|---|---|
| Trust Tasks × Credential | core | P0 | **INDETERMINATE** | All three findings narrowed; #609/#310 remain blockers. |
| Credential × ZKP | core | P0 | **INDETERMINATE** | Stronger proof/authority/context semantics; integration not demonstrated. |
| Credential × VDS | conditional | P0 | **INDETERMINATE** | Historical risks retained; VDS unchanged and no current execution evidence. |
| Trust Tasks × ZKP | conditional | P0 | **INDETERMINATE** | Authority/replay gap narrowed; Trust Tasks binding remains an integration target. |
| Trust Tasks × VDS | conditional | P1 | **INDETERMINATE** | Trust Tasks changed materially; persistent-state closure remains unevidenced. |
| ZKP × VDS | conditional | P1 | **INDETERMINATE** | ZKP stronger; VDS unchanged; no integrated proof/state evidence. |
| Agent Names × Trust Tasks | core | P1 | **INDETERMINATE** | Trust Tasks identity/authority semantics stronger; controller seam unevidenced. |
| Agent Names × Credential | conditional | P1 | **INDETERMINATE** | Credential semantics stronger; identity/control seam unevidenced. |

## Historical finding reconciliation

The historical cross-specification corpus contains 23 findings.

Current-pin reconciliation yields:

- **0 resolved to portfolio-wide PASS**
- **13 narrowed or retained-narrowed**
- **10 retained**
- **0 newly proven upstream defects**

The absence of a new FAIL is not a reason to close the residuals. It means the correct next work is focused evidence or specification-profile clarification rather than bulk issue filing.

## P0 upstream/reliance actions

### 1. Close live authority-currentness evidence

**Severity:** S1 High  
**Priority:** P0 Immediate  
**Owner:** implementation/evidence owners coordinated through RAHP #609

The bounded authority path verifies validity windows and exact action/scope checks, but current evidence does not establish live credentialStatus/revocation, separate live governance-policy/status lookup, or a bounded propagation/freshness contract.

**Closure evidence:** revoked authority, stale status, lookup failure and policy disagreement negative cases with attributable current traces.

### 2. Establish target-attributable correlation evidence

**Severity:** S1 High  
**Priority:** P0 Immediate  
**Owner:** original target implementation evidence owner, coordinated through RAHP #310

Interop A/B evidence exists, but it cannot be relabelled as target runtime evidence. Until original-target evidence exists, cross-context credential/proof identifier conclusions remain INDETERMINATE.

### 3. Turn ZKP integration targets into demonstrated profiles

**Severity:** S1 High  
**Priority:** P0 Immediate for Credential × ZKP; P1 for broader ZKP seams  
**Owner:** relevant specification/profile maintainers

The current ZKP specification has strong audience, purpose, challenge, freshness, status and authority-separation semantics, but explicitly records Trust Tasks binding as an integration target rather than demonstrated interoperability.

**Requested action:** pin compatible Credential/Trust Task revisions, define the profile and public signals, and supply wrong-audience, stale-status, replay and authority-substitution negative vectors.

## P1 actions

- Produce current VDS composition evidence for persistent state versus current authority, historical/current truth, provenance and auditability.
- Produce Agent Names integration evidence that distinguishes naming/control identity from current authorization and delegated execution.
- Complete privacy/contestability reconciliation for fixed task citation/digest and retained-evidence surfaces once #310 obtains target-attributable evidence.

## What changed in RAHP itself

Since #772, RAHP has made execution materiality-driven:

- core seams are routinely selected;
- conditional seams run only when materially implicated;
- reference evidence is retained without routine execution;
- full remains explicitly available for rebaseline or campaign use.

This rebaseline therefore establishes the comparison point needed for future selective execution. A future routine run does not need to repeat all eight seams merely to preserve confidence.

## Trigger for the next full clean-room campaign

Another full #772-style campaign should occur only when bounded reassessment cannot defend the portfolio conclusion, for example when:

- multiple core and conditional seams are simultaneously invalidated;
- authority/delegation semantics change across several specifications;
- canonical authority moves across major source repositories;
- the realization architecture materially changes across the full trust path;
- evidence freshness invalidates a substantial fraction of the retained graph;
- specialist evidence contradicts a portfolio conclusion;
- or RAHP terminal assurance semantics themselves change.

Elapsed time alone is not a trigger.

## Upstream handoff judgment

The actionable signal is now narrower than #772:

1. close live authority-currentness evidence (#609);
2. obtain target-attributable correlation evidence (#310);
3. turn ZKP integration targets into demonstrated, version-pinned profiles;
4. add VDS and Agent Names execution evidence only when their conditional seams are materially implicated.

No bulk upstream issue publication is justified from the historical 23 findings. File upstream only when a residual survives a current, source-pinned reassessment and has a concrete normative or implementation owner.

## Provenance

- Parent clean-room campaign: #772
- Current-pin rebaseline: #782
- Current execution-evidence tranche: #783
- Materiality-driven execution changes: #784 / #786, PRs #785 / #787
- Durable blockers: #310 and #609
- Machine-readable rebaseline: instances/dtg/reviews/2026-09-24-cross-spec-rebaseline.yaml
