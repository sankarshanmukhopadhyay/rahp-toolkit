# Eucalyptus supplemental native evidence — 8 October 2026

The native evidence packet is complete and retained; overall assurance remains **INDETERMINATE**. This follow-up closes substantial native-execution sub-obligations while keeping all 20 consequential proposition judgments evidence-required. It does not replace the [initial sealed campaign](../eucalyptus-2026-10-08/report.md).

## Evidence and provenance

The [native CI run](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/actions/runs/37733481776) executed the exact source contract with assessor revision [fdbbff0](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/commit/fdbbff0e4f7b34f49305452dea3f0b9dccb59384). [PR #962](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/pull/962) merged the collector after validation, documentation, workflow governance and clean-room workflows passed.

The retained [native-evidence.zip](native-evidence.zip) is byte-for-byte the downloaded Actions artifact, not a reconstructed substitute. SHA256: `972cc23ed99bc3e5cac0c4559941fa6ddb242bc622b3590a211a6a6a3217eebe`; 830,225 bytes. Its inner seal root is `9894628403748b1a884071746a9da4f48a52779c938201d710715a12753e92ad`. Both archive digest and inner integrity were independently verified after download. The archive includes commands, version output, revisions, execution timestamps, assessor source snapshot, stdout/stderr, build inputs, prerequisite logs and the original machine summary.

See [attempts.json](attempts.json), [run-contract.json](run-contract.json), [summary.json](summary.json), [integrity.json](integrity.json) and the [supplemental disposition](disposition.json). These readable records are exact copies from the archive except the separately authored disposition. They preserve the measured observation rather than rewriting nonzero attempts after diagnosis.

## What executed

There were **26 attempts: 19 EXECUTED_PASS, four EXECUTED_NONZERO and three ATTEMPTED_UNAVAILABLE**. Aggregate counts are **11,528 passing, 14 failing and 89 skipped test events**. Counts span overlapping suites and include 1,286 passing events from nonzero attempts; they are neither unique tests nor independent assurance claims. Passing attempts account for 10,242 passing events. Skips are not passes.

| Attempt | Execution state | Passing events | Failed events |
|---|---|---:|---:|
| rust-openvtc | EXECUTED_NONZERO | 957 | 1 |
| rust-verifiable-trust-infrastructure | ATTEMPTED_UNAVAILABLE | 0 | 0 |
| rust-affinidi-tdk-rs | EXECUTED_PASS | 3905 | 0 |
| rust-affinidi-webvh-service | EXECUTED_PASS | 1220 | 0 |
| rust-affinidi-trust-registry-rs | EXECUTED_NONZERO | 290 | 9 |
| rust-dtgwg-trust-tasks-tf | EXECUTED_PASS | 1459 | 0 |
| rust-verifiable-git-infrastructure | EXECUTED_PASS | 820 | 0 |
| rust-didwebvh-rs | EXECUTED_PASS | 523 | 0 |
| rust-dtg-credentials | EXECUTED_PASS | 213 | 0 |
| rust-predicate-credential-system | EXECUTED_PASS | 446 | 0 |
| rust-vta-agent-memory | EXECUTED_PASS | 119 | 0 |
| rust-vti-push-gateway | EXECUTED_PASS | 141 | 0 |
| go-tsp | EXECUTED_PASS | 782 | 0 |
| dart-tsp | EXECUTED_NONZERO | 39 | 4 |
| dart-tsp-package | EXECUTED_PASS | 83 | 0 |
| ios-approval | EXECUTED_NONZERO | 0 | 0 |
| lab-room-handoff | ATTEMPTED_UNAVAILABLE | 0 | 0 |
| lab-privacy-handoff | ATTEMPTED_UNAVAILABLE | 0 | 0 |
| vtc-sender | EXECUTED_PASS | 5 | 0 |
| vtc-self-edit | EXECUTED_PASS | 11 | 0 |
| vtc-consent | EXECUTED_PASS | 31 | 0 |
| vta-freshness | EXECUTED_PASS | 3 | 0 |
| vta-refresh | EXECUTED_PASS | 5 | 0 |
| rooms-native | EXECUTED_PASS | 198 | 0 |
| vetting-native | EXECUTED_PASS | 7 | 0 |
| e2e-native | EXECUTED_PASS | 271 | 0 |

Eight focused VTI consuming-path fixture attempts passed: sender binding (5), self-edit (11), unrestricted administrator consent (31), freshness (3), refresh (5), rooms (198), vetting (7), and E2E (271). These provide new attributable native fixture observations. Their success is separate from the full VTI workspace attempt, which timed out. Fixture mediation and identities still do not establish every deployed door, independent people or observer surfaces.

Go produced 782 passing events with uncached `go test -count=1 -json ./...`. Dart produced 83 passing events when the unchanged tagged tests ran from their package directory. The original root invocation remains a separate failed attempt; four errors concern package-relative fixture paths. Rust native component execution is now established for TDK, WebVH service, Trust Tasks, VGI, DIDWebVH, credentials, PCS, agent memory and push gateway.

Credentials and Dart used preserved fresh dependency resolutions, not release locks. A coordinated source tag does not imply each consumer resolves every coordinated component revision. The recorded input files support further dependency comparison; they do not settle the cross-version proposition.

## Nonzero and unavailable results

* **OpenVTC:** 957 passes and one failed assertion in `state_handler::vetting_actions::tests::no_ticket_is_issued_for_requests_that_cannot_be_attested`, at tagged `openvtc/src/state_handler/vetting_actions.rs:7280`. The observed message concerns drawing three token windows before issuing a ticket. This is an actual test-level failure requiring target-specific diagnosis and a reproducible focused retest. This packet does not label it a vulnerability or silently credit the whole suite as PASS.
* **Trust registry:** 290 passes and nine integration failures. All nine fail at `trust-registry/tests/didcomm_integration_test.rs:60` because `CLIENT_DID` is absent from `.env.test`. This run lacks the configured live integration prerequisites. Authority enforcement cannot be inferred from those unexecuted integration paths.
* **Dart original invocation:** 39 passes and four fixture-path errors. The separately recorded package-directory run supplies the bounded 83-pass retest without erasing this diagnostic.
* **iOS:** Swift execution reached a build failure because the supplied `VtaMobileCore.xcframework` has no Linux library. No Apple journey or native iOS test PASS was obtained.
* **Full VTI workspace:** exceeded the recorded 900-second bound before reporting native test events. Focused suites later passed, but they do not retroactively make this full attempt successful.
* **Lab room and privacy handoffs:** reject the Eucalyptus VTI revision because their pinned producers require older revisions (`56cd6e5...` and `72bf579...`). This is a source-compatibility boundary. Historical probe PASS cannot be borrowed for Eucalyptus. A producer change and new evidence require their own review.

Exact diagnostic text is retained under `native-evidence/logs/` in the archive. No target test was edited, disabled or weakened, and no upstream defect was filed.

## Remaining closure contracts

The following rows retain the original exact retest obligations and proposed responsibility surfaces. They do not assign upstream maintainers. Every row remains evidence-required; related native observations support only the bounded sub-obligations listed in the disposition.

| Proposition | Responsibility surface | Remaining retest |
|---|---|---|
| EUC-01 | VTI / Trust Tasks | Execute signed/unsigned, wrong-sender and nested-transport requests through VTA, VTC, mediator and push doors; verify zero forbidden effects. |
| EUC-02 | DTG Credentials / VTI | Exercise both substitution directions and revoke authority between verification and commit. |
| EUC-03 | VTI / deployment operator | Execute label-only, widening, narrowing, sole-admin and multiple-person configurations across HTTPS/DIDComm/TSP; assert audit-before-effect. |
| EUC-04 | VTI / community governance | Exercise repeated approver, requester approval, stale approval, role reduction, threshold change, cancellation, cooling-off and real single-person/multi-person policy. |
| EUC-05 | VTI / mediator | Capture and replay identical task, changed payload under same ID, expired consent and post-restart retries; inspect effects and durable state. |
| EUC-06 | TDK / Go / Dart / browser | Execute independent byte vectors and old/new endpoint pairs, nested mediator sends, restart and forged relationship transitions. |
| EUC-07 | VTI Rooms / deployment operator | Run host, native and browser participants; remove member, rekey, rotate custodian, replay old epoch and corrupt Merkle record. |
| EUC-08 | PCS / DPIP specialist / VTI | Execute duplicate-vetter, wrong-context, withdrawn-vetter, nonce replay and public/hidden A-B journeys with observable transcripts. |
| EUC-09 | DPIP specialist / OpenVTC / VTA | Compare two contexts through issuance, presentation, status discovery, task retention and retirement; measure stable joins and required disclosures. |
| EUC-10 | VGI / VTC / forge operator | Run GitHub and Forgejo adapters against sandbox forges; bypass PR gate, revoke member after approval, replay webhook, exercise break-glass and inspect signer attribution. |
| EUC-11 | TDK / mediator operator | Run unauthorized and authorized inspect/purge/patch/reload tasks; verify sender proof, ACL, restart and audit on every transport. |
| EUC-12 | TDK / DID hosting / browser | Execute private/IP-encoding/redirect/rebinding vectors through real resolver, mediator client and DID hosting rather than the URL predicate alone. |
| EUC-13 | VTA / VTC / governance operator | Tamper, truncate, roll back and rotate keys; independently verify chains and reconstruct a contested action after agent replacement. |
| EUC-14 | VTI / TSP PQ | Exercise mixed algorithms, absent hybrid member, wrong key type, malformed signature and downgraded peer; pin actual crypto packages. |
| EUC-15 | Trust registry / relying-party operator | Run unauthorized write, replay, key rotation, stale status and cross-context recognition; verify policy version, effective time and audit. |
| EUC-16 | Mobile / push / VTA | Exercise unsolicited pairing, forged push, altered display/action digest, decline, expiry and revoked device through physical approval journey. |
| EUC-17 | Agent memory / VTA operator | Feed delimiter escape, command injection, excessive record and cross-owner recall through actual MCP consumer; observe decisions and stored bytes. |
| EUC-18 | RP SDK / browser operator | Run wrong recipient, stale token, reused challenge, deeply nested payload and modified signed token through actual relying service. |
| EUC-19 | All component maintainers / RAHP | Build locked consumers; compare resolved package identities to coordinated sources and execute old/new request-schema and lifecycle pairs. |
| EUC-20 | Community governance / client maintainers | Run assistive-technology and unavailable-device journeys; document supported alternatives and verify a challenged decision can be corrected without bypassing authority. |

For each proposition, closure requires the pinned consuming configuration, policy, clock/state, participants and attributable expected/observed effects across positive, negative and adversarial cases. Privacy assertions also need actual observer captures and a portable specialist judgment. Participant independence needs real governance observations; physical approval and accessibility need supported participant/device journeys. None can be inferred from a fixture count.

The practical next evidence boundaries are: diagnose the OpenVTC assertion; provision the trust-registry integration prerequisites; complete the full VTI workspace within a justified bound; produce source-compatible Lab probes; then execute the deployment, privacy, governance, Apple and resilience journeys. These are concrete outstanding obligations, not hidden work claimed as complete.

## Reproduction and preservation

Extract the archive to a new directory and run:

```bash
sha256sum native-evidence.zip
unzip native-evidence.zip -d native-packet
python tools/eucalyptus_campaign.py --verify-package native-packet/native-evidence
```

The initial assessment remains sealed and unchanged. The follow-up collector rejects reuse of an existing output without altering its seal, and future attempts preserve build inputs under individual attempt directories. These preservation fixes do not change or reinterpret this recorded run.

Contributor: Codex (AI-assisted implementation, orchestration, evidence review and prose). Publication is not human risk acceptance, a conformance grant or closure of issue #960.
