# Credential renewal relationship-lifecycle coverage reconciliation

**Tracking:** #1106  
**Status:** downstream bounded reconciliation  
**Source basis:** DTG HTX Discussion #22 as cited by #1106; existing downstream #1031 and #1089; current portable `method/catalogue/`; current bundled DTG `data/`.

## Authority boundary

HTX owns human-experience recommendations. Trust Tasks and credential profiles own lifecycle and successor semantics. Portable `method/` owns reusable RAHP method concepts. Root `data/` is the bundled DTG exemplar, not portable authority. Upstream `trustoverip/dtgwg-rahp-tf` remains authoritative for its own corpus.

The HTX discussion is exploratory. Its straw-person requirements and labels are treated as hypotheses, not adopted conformance rules.

## Existing coverage inventory

Portable coverage already includes lifecycle continuation (`ATP-AUTH-03`), current authority (`RKP-AUTH-02`, `CTP-AUTH-02`, `GRP-AUTH-02`), lifecycle composition (`RKP-COMP-02`, `CTP-COMP-02`, `GRP-COMP-02`), privacy/status observability (`RKP-PRV-06`, `RKP-COMP-03`, `GRP-PRV-02`, `ATP-PRV-01`), coercion/choice/withdrawal harms (`HRM-AUT-02`, `HRM-AUT-03`, `HRM-AUT-05`) and inclusion burden (`RKP-EXC-02`, `HRM-ACC-02`, `CTP-EXC-01`).

Bundled DTG records include `RK-CR02` (stale credential / expiry without renewal path), `RK-HX04` (unsupported decision-making exclusion), `RK-HX05` (LPA/guardianship architecture gap) and `RK-HX06` (credential lifecycle abandonment on capacity loss or death). These remain DTG exemplar records and are not imported into the portable method.

## Five-hypothesis disposition

| Hypothesis | Affected actors/interests | Existing coverage | Added evidence case | Disposition |
|---|---|---|---|---|
| automation maintains inactive relationship without current authority | holder, relying party; agency, security | `ATP-AUTH-03`, `RKP-AUTH-02`, `GRP-AUTH-02`; existing CRA-001..004 | retained existing negative vectors | **existing coverage** |
| coerced/concealed holder ending treated as free choice | holder; autonomy, exit | `HRM-AUT-02`, `HRM-AUT-03`, `HRM-AUT-05` | `CRA-006` + accessible contrast `CRA-009` | **bounded refinement**; no new portable risk needed |
| demand-driven renewal exposes intent/relationship/timing | holder; privacy, contextual integrity | `RKP-PRV-06`, `RKP-COMP-03`, `GRP-PRV-02`, `ATP-PRV-01` | `CRA-007` | **bounded refinement** |
| requested assurance uplift imposes unjustified proofing burden | holder/relying party; equality, access, autonomy | `RKP-EXC-02`, `HRM-ACC-02`, `CTP-EXC-01` | `CRA-008` | **bounded refinement**; control trade-off delegated to #1089 |
| expiration misclassified as closure, withdrawal or continuation | holder, issuer, relying party; agency, continuity | `RKP-COMP-02`, `CTP-COMP-02`, `GRP-COMP-02` | `CRA-005` | **bounded refinement** |

No hypothesis establishes a distinct reusable failure mechanism that justifies a new portable ID at this time.

## Control-induced consequence evidence for #1089

`CRA-008` deliberately records both sides of one control proposition: increasing assurance can reduce relying-party uncertainty while increasing holder proofing burden or exclusion risk. Missing proportionality or alternative-path evidence remains `INDETERMINATE`. This is concrete evidence for #1089's general method question, not a credential-renewal-specific method extension.

## Failure behavior established by the fixture

- expiry without other evidence is not holder closure, issuer withdrawal or current continuation authority;
- a missing privacy/proportionality/alternative-path fact remains non-PASS;
- a closure request can deny continuation while the human-experience disposition remains indeterminate under contradictory coercion evidence;
- support does not establish authority merely because a prompt or helper exists; the positive contrast requires explicit representative authorization and accessible participation;
- historical evidence is preserved but does not become current authority.

## Upstream convergence disposition

**No new upstream RAHP catalogue record is proposed from #1106.** Current portable patterns are sufficient when combined with the expanded negative/boundary examples. The useful upstream feedback is methodological and example-level:

1. preserve separation of expiry, holder closure and issuer withdrawal;
2. retain renewal/status timing privacy as an assessable evidence question;
3. make coercion/accessibility evidence visible when lifecycle actions are human-mediated;
4. assess third-party assurance uplift for participant burden and proportionality.

The generalized rule for control-induced/redistributed harms belongs to downstream #1089 first. Any upstream convergence should follow validated #1089 evidence rather than treating this issue as upstream authority.

## Compatibility and non-goals

The change is additive to an existing example and test module. It does not change catalogue schemas, IDs, method semantics, APIs or DTG lifecycle rules. It does not assert observed real-world harms.
