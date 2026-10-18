# Portfolio no-action precedence correction — 2026-10-18

**Scope:** RAHP semantic materiality routing, specifically historical controller snapshots #1028, #1040, #1042, #1043, #1045, #1046 and #1047. Upstream source authority remains with the originating OpenVTC repositories. This record corrects an observed **routing judgment**, not a runtime conformance verdict.

## Finding

The archived controller routing artifacts place source finding `aa28149c7babc678e9e7` (`OpenVTC/verifiable-trust-infrastructure` [PR #1997](https://github.com/OpenVTC/verifiable-trust-infrastructure/pull/1997), [commit `2a7c8ce`](https://github.com/OpenVTC/verifiable-trust-infrastructure/commit/2a7c8ce3ffaba9ddad25ff61ae94f58c369addcf)) in `no-action / routine-release-or-plan`.

This is a **breaking behavioral** VTA SDK wallet sign-in change: signed `auth/oob` grants, UV key enrollment and advertised TrustTaskHTTPS/SignInPortal. It was normalized simultaneously to `change_kind: [behavior-change, release-change]`, `dimensions: [security, lifecycle, release]`, and `concerns: [authorization, aggregation]`.

The semantic router selected the first matching `release + aggregation` no-action rule before reaching the later `openvtc-security-combined` rule. Therefore a genuine behavioral assurance question was silently suppressed because the same observation also had a release metadata dimension. This **violates the intent** of the no-action rationale, which is explicitly bounded to release markers and editorial plans, not functionality.

## Bounded remedy

- Add declarative `unless: {change_kind: [behavior-change]}` veto semantics to `semantic_match()` for supported list fields. A veto only affects rules explicitly opting in; existing positive match semantics remain unchanged.
- Apply that veto to both `routine-release-or-plan` and `openvtc-routine-alignment`; neither may downgrade a dual-classified functionality change to no-action.
- Regression `tests/test_routing_noaction_precedence.py` constructs the exact archived wallet-sign-in finding, expects `combined / openvtc-security-combined`, and verifies an ordinary `vta-sdk-v0.65.0` release marker remains `no-action`. Unknown veto fields fail closed.

## Disposition and owner

- `aa28149c7babc678e9e7` is transferred for **Scope A trigger-link and consent-path review** to [RAHP #994](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/994). This is an **assurance review transfer**, not an assertion of PASS or a new unscoped engine requirement.
- The seven historical controller snapshots remain immutable. Their earlier `no-action` judgment for this finding is **superseded** by this record; there is no need to falsify old artefacts or release a new historical snapshot.
- Controller closure must still account for every `combined`, `covered`, `no-action`, UNMAPPED and DPIP child. Correcting one false negative is **not** an authorization to close controllers.
- Releases and packaging-only changes may remain `no-action` when there is truly no simultaneously detected behavior change; individual version labels are not themselves evidence of semantic preservation.

## Reproduce

```bash
python3 -m unittest tests.test_routing_noaction_precedence -v
python3 tools/validate_dtg_instance_routing.py
```

Evidence basis: downloaded original workflow `dtg-portfolio-routing-*` artifacts for 14–17 October, including `routing.json`, recorded finding/normalization/decision and `combined-result.json`. No external deployed VTA execution has been inferred.
