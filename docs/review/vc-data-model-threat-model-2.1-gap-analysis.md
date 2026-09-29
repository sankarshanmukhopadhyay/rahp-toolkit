# VC Data Model Threat Model v2.1 — RAHP privacy gap analysis

## Purpose

This note records the judgment behind RAHP issue #843. It uses the W3C **Verifiable Credentials Data Model Threat Model v2.1** as research provenance to pressure-test the reusable RAHP risk catalogue.

Source: https://www.w3.org/TR/vc-data-model-threat-model/

At the time of this review the W3C document is a Group Note Draft / work in progress. It is not treated as authority for RAHP classifications.

## Judgment

The existing RAHP harm catalogue does not need VC-specific additions. Its privacy harms already cover unnecessary disclosure, correlation, inference, persistent surveillance and secondary use/context collapse.

The material gap is at the **risk mechanism** layer. Several credential-system failures can occur while authenticity, signature verification and ordinary lifecycle checks succeed:

- proof or securing metadata itself becomes a correlator;
- the act of querying status exposes presentation activity or relationship context;
- legitimately disclosed information is used after the original relying purpose has ended;
- a legitimate issuer/operator configures issuance or proof metadata so an intended unlinkability property is defeated;
- retained verification artefacts accumulate into a durable correlation and inference surface.

These mechanisms are represented as RKP-PRV-05 through RKP-PRV-09.

## Deliberate non-imports

The W3C threat list is not copied wholesale.

Credential tampering, context misuse, stable identifiers and disclosure aggregation already map to existing RAHP risks. Code injection and device compromise belong primarily to implementation/end-point security rather than this reusable trust-risk tranche. Cryptographic suite obsolescence is better handled through dependency/security lifecycle assurance unless a concrete trust proposition requires a more specific RAHP pattern.

## Important distinctions

### Status response disclosure vs status-query observability

RKP-PRV-03 covers information revealed **in a failure, diagnostic or status response**.

RKP-PRV-06 covers information revealed because **the status lookup happened at all**, including its timing, credential-specific target, relying context or observable relationship.

A response can therefore be perfectly minimal while the lookup pattern remains privacy-significant.

### Stable identifiers vs proof-mechanism correlation

RKP-PRV-01 covers explicit persistent identifiers.

RKP-PRV-05 covers otherwise privacy-preserving payloads that become linkable through proof values, verification-method references, timestamps or other securing metadata.

### Initial disclosure vs downstream processing

RKP-CRD-04 concerns forwarding, presenting or reusing a credential outside its intended audience or purpose.

RKP-PRV-07 begins after an initially legitimate disclosure and asks whether subsequent retention, transfer, profiling or reuse still has an adequate purpose and governance basis.

## Assurance implication

A cryptographically valid transaction is not automatically a privacy-safe transaction. Privacy claims require evidence about the complete observable and retained interaction, including proof machinery, status resolution, post-disclosure processing and artefact retention.

This note preserves source provenance and the reasoning for the catalogue extension; the catalogue records remain technology-neutral.
