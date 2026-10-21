# TSP Release 1.0 source baseline and publication reconciliation

**Assessment:** RAHP #1103; draft PR #1104. **Verified on:** 2026-10-22.

## Directly inspected upstream evidence

1. `trustoverip/tswg-tsp-specification`, commit `ccda6b33159d860f05c328eb436dabe83548b705`, file `spec/spec.md`: document header reads **Specification Status: Release 1.0**. The source contains normative RFC 2119/8174 keywords and protocol definitions.
2. At the same commit, `specs.json` declares `spec_directory: ./spec`, `markdown_paths: [spec.md]`, `output_path: ./docs`. This establishes the source-to-render *configuration*, **not** that a particular deployed page was generated from this commit.
3. The upstream repo's `docs/index.html` was not accessible at the inspected commit or current main via the GitHub contents API. No byte-level comparison to the live GitHub Pages HTML was achieved.
4. `OpenVTC/tsp-conformance` at commit `b89e62869c686841fc98a4386f3b297babad0194` explicitly tests **Rev 3** (`YTSP-AAC`, abbreviated upstream commit `f5b8668`), not the Release 1.0 source pin. Its September report is historical supporting evidence, not Release 1.0 conformance certification.
5. A previously inspected live rendering was described as **Experimental Implementor's Draft Rev 2**. This description has not been reconciled with the source's Release 1.0 status and must not be silently overwritten.

## Evidence-driven decision

**Primary assessment source candidate:** immutable `spec/spec.md@ccda6b33159d860f05c328eb436dabe83548b705`, identified by its own header as Release 1.0.

**Publication equivalence:** **UNVERIFIED**. Do not assert that `https://trustoverip.github.io/tswg-tsp-specification/` serves Release 1.0 until its actual displayed status and provenance can be confirmed.

**Approval / ratification:** **NOT ESTABLISHED**. A source header stating Release 1.0 does not itself establish formal ToIP approval, publication date, or ratification status.

**Rev 3 suite evidence:** **CONDITIONALLY ADMITTED** only for claims demonstrably stable across the Rev 3 source and the selected Release 1.0 source. Preserve its eight historical negative-test failures as implementation/version-specific observations.

## Required reconciliation before terminal assessment

- [ ] Obtain live page HTML or deployed `gh-pages` artifact, inspect displayed status, revision, publication metadata and deploy commit.
- [ ] Resolve abbreviated `f5b8668` to a full SHA, compare Rev 3 normative provisions and vectors against the pinned Release 1.0 source.
- [ ] Determine formal publication/approval status from upstream governance or release record; do not infer from version label.
- [ ] Re-run the relevant conformance and negative cases against explicitly pinned implementations and the chosen normative target.
- [ ] Update both reports to name **Release 1.0 source candidate**, with the published-render discrepancy explicitly open.

**Current four-lens assurance disposition: INDETERMINATE.**
