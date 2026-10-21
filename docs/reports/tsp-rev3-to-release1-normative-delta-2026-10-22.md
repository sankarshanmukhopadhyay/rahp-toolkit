# TSP Rev 3 to Release 1.0: normative delta and assurance retest register

**Issue:** #1103 · **PR:** #1104 · **Date:** 2026-10-22.

## Reproducible comparison

- **Rev 3:** `trustoverip/tswg-tsp-specification@f5b8668952aabe8e541b535fcbdf589484ffc4f4`; header: `Experimental Implementor's Draft Rev 3`; merge #63 explicitly proposed Rev 3 as candidate for R1.
- **Release 1.0 source candidate:** `trustoverip/tswg-tsp-specification@ccda6b33159d860f05c328eb436dabe83548b705`; header: `Release 1.0`; merge #86 explicitly says “Clarify appraisal requirements citing standards, make VID_sndr always on, set version to 1.0”.
- **Comparison:** [GitHub compare](https://github.com/trustoverip/tswg-tsp-specification/compare/f5b8668952aabe8e541b535fcbdf589484ffc4f4...ccda6b33159d860f05c328eb436dabe83548b705): 19 intervening commits, 1 modified file (`spec/spec.md`), 342 additions, 199 deletions. These counts describe the full intervening history, not only merge #86.
- **Publication provenance:** source status does not prove the currently served GitHub Pages rendering or formal governance approval.

## Verified substantive normative changes in merge #86

| ID | Rev 3 / pre-#86 | Release 1.0 candidate | Assurance consequence |
|---|---|---|---|
| DELTA-01 | Header described Experimental Implementor's Draft Rev 3 with errata | Header says Release 1.0 | Distinguish source designation from ratification and live deployment |
| DELTA-02 | Wire version `YTSP-AAC` (0.2) | Wire version `YTSP-BAA` (1.0) | **Rev 3 test vectors and exact-byte expectations cannot be treated as Release 1.0 vectors** |
| DELTA-03 | HPKE-Base confidential payload sender VID could be NULL by default | All PKAE confidential payloads MUST carry sender VID; receiver MUST compare with envelope sender | Add rejection of NULL sender, mismatch, omitted sender; check pack/open and mixed-version interop |
| DELTA-04 | ESSR explanation allowed HPKE sender binding via AAD without embedded sender VID | Embedded sender identity plus AAD required for HPKE-Base | Update security claims and threat analysis; confirm actual implementation |
| DELTA-05 | Verifiability phrasing did not explicitly distinguish computation and appraisal | Cryptographic verification and policy-based appraisal distinguished with RFC9334/TCG-AF references | Add VID appraisal-policy, freshness, provenance and governance tests; cryptographic PASS cannot imply appraisal PASS |
| DELTA-06 | Encodings allowed `VID_sndr | 4BAA` in some examples | `VID_sndr` shown as mandatory in updated application and nested payload encodings | Update parser/serialization conformance and cross-layer identity binding cases |

The source diff also retains the rule that a **non-confidential** payload sender field MAY be NULL; if non-NULL, it must match the envelope sender. Do not misread the “always on” commit title as requiring a non-NULL sender in every payload mode.

## Required retest plan

| Test family | Target / expected evidence | Priority | Status |
|---|---|---|---|
| Protocol version negotiation | `YTSP-BAA` acceptance; explicit `YTSP-AAC` backward compatibility policy | P0 | NOT EXECUTED |
| HPKE confidential sender binding | Non-NULL sender VID in payload, matches envelope; reject missing/NULL/mismatch | P0 | NOT EXECUTED |
| Sealed box sender binding | Retain ESSR sender binding checks; no regression | P0 | NOT EXECUTED |
| Non-confidential sender semantics | Allow NULL where permitted; reject non-NULL mismatch | P0 | NOT EXECUTED |
| Revised test vectors | Generate/verify Release 1.0 canonical vectors and exact-byte encodings | P0 | NOT EXECUTED |
| VID appraisal | Appraisal is policy-governed; demonstrate verification does not imply authorization/trust | P0 | NOT EXECUTED |
| Composition | Verify resolver/support-system → VID appraisal → sender binding → relying application authorization | P0 | NOT EXECUTED |
| Negative regressions | Recheck eight Rev 3 historical failures under Release 1.0 source and pinned implementations | P1 | NOT EXECUTED |
| DRARM | Retry/reconnect, routed/nested fan-out, resolver cache and overload/queue boundaries | P1 | NOT EXECUTED |
| Human harms | Wrong-person attribution, improper relationship acceptance, redress and revocation lag | P1 | NOT EXECUTED |

## Conformance admission decision

The OpenVTC suite pinned to Rev 3 (`YTSP-AAC`) is a **historical comparator**, not Release 1.0 conformance evidence. Its 1672 passes, 8 failures and 250 skips remain historically attributable; none are promoted to Release 1.0 PASS. New Release 1.0 test cases must explicitly cover the new version tag and non-NULL confidential sender VID requirement.

## Residual uncertainties

The full 19-commit diff may contain other normative changes beyond the inspected merge #86. A complete clause-by-clause delta, current publication/deployment verification, formal approval record, pinned implementation builds and executable four-lens RAHP results remain outstanding.

**Terminal four-lens disposition: INDETERMINATE.**
