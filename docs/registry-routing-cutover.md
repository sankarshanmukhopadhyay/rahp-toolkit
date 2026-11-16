# Registry routing preflight

The DTG materiality workflow produces three different work types: controller, combined review and DPIP referral. The controller and DPIP workflows depend on RAHP-local issue identity; the combined review worker similarly consumes local issues. These **cannot yet be retargeted** to a passive registry without a compatible execution and return path.

`tools/registry_route_gate.py` audits the actual post-journal event files before the existing publisher executes. It emits a JSON report naming missing source pins, external owner or consumer compatibility. It is strictly read-only. Its CI test suite attempts to falsify readiness through current event formats, wrong pins, duplicate identities and missing producer contracts.

The preflight does **not** authorize cutover, create registry issues, or suppress the present publisher. The `live_cutover_authorized` value is always false, including for an empty event set. For a future cutover gate `--require-ready` makes unsatisfied dependencies fail closed; do not enable that option in the current workflow until controller/DPIP/Lab transport and credential compatibility is demonstrated.

[Registry issue #2](https://github.com/sankarshanmukhopadhyay/rahp-assessment-registry/issues/2) is the canonical cutover gate. Source findings must continue to remain observable, and an unavailable external token must never be reported as a successful handoff.
