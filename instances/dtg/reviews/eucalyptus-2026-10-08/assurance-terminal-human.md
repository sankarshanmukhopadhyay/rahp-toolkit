# RAHP assurance conclusion — DTG-VTC-EUCALYPTUS-2026-10-08

- Assessment: `rahp:f1df8dcef625798eacf5`
- Subject type: `portfolio-composition`
- Outcome: **INDETERMINATE**
- Reason: `eucalyptus-composition-evidence-required`
- Controller state: `TERMINAL_INDETERMINATE_EVIDENCE_REQUIRED`
- process_state: `complete`
- assurance_state: `indeterminate`
- evidence_maturity: `source-only`
- Boundedness: Conclusion applies only to the configured subject, immutable pins and evidence classes represented in this run.
- Confidence: bounded by named evidence and assessor result

## Source pins

- `OpenVTC/verifiable-trust-infrastructure@49f5f1beb61adc34bdf7cf0bd3eb10f594415b80`
- `OpenVTC/openvtc@2a4fa2b3c8e831dbe3184a1119c4c87b6f197220`
- `affinidi/affinidi-tdk-rs@a1611baa011620a6ca62649b105c2b8c898f2653`
- `affinidi/affinidi-webvh-service@1686668623e0bba0e18880074d82794cb929a7fc`
- `affinidi/affinidi-trust-registry-rs@c77052f9bffe8bb7b4a3f357d9ef54cf632950f0`
- `trustoverip/dtgwg-trust-tasks-tf@7b6bb488ffd838bef058310c909207d4a7b77125`
- `OpenVTC/verifiable-git-infrastructure@92f32dd4c107545bd42b009ca55fc1ed4759309d`
- `OpenVTC/vta-browser-plugin@d6df67971688fd927cd5b095424fa4093d4264df`
- `decentralized-identity/didwebvh-rs@155eb4e71c9d45db57c6f7329f286bbd753e0138`
- `OpenVTC/dtg-credentials@fc9954d8d529d312ebac7ec1d413179857474c96`
- `OpenVTC/predicate-credential-system@4be4598563f422b9a3a4e37032d22487836d322c`
- `OpenVTC/vta-agent-memory@85db98a8a9c6d25b673a38a9e7e60d3435f3fcc5`
- `affinidi/affinidi-tsp-go@d32ca7cdde208e93509c1f140ad7ee04d52ca7cc`
- `affinidi/affinidi-tsp-dart@a64814c8043d6af0955a3ce01bfc6033d8daeb78`
- `OpenVTC/vti-push-gateway@44342121e161ccb12e43013f33ce80abb2486acb`
- `OpenVTC/rp-sdk-js@8594c2acba4014232e842fe7613e8a7cdc0e2b0f`
- `OpenVTC/vti-didcomm-js@afd11e1f5dab611118253d2ebaffd1cfee29962a`
- `OpenVTC/vta-mobile-agent-ios@863a1e912042b28908ec2cf3675677ad9c151e0e`
- `sankarshanmukhopadhyay/trust-protocol-interop-lab@895e1af0f441995cada90dad2a429e56885bd394`
- `sankarshanmukhopadhyay/dtg-privacy-implementation-profile@991c92bad6ccb61dbc2511162bf11a9eb59679e2`

## Assurance inference

20 consequential propositions lack accepted deployed-composition/specialist evidence. Component results and configuration exceptions are bounded observations, not certification.

## Human-harm traceability

- **requester / Forged or sender-mismatched task enters an authenticated transport** → unauthorized actuation → `Task proofs are bound to the actual sender across all consuming doors` → document proof plus transport-sender binding → EUC-01, EUC-02, EUC-03, EUC-04, EUC-05, EUC-06, EUC-07, EUC-08, EUC-09, EUC-10, EUC-11, EUC-12, EUC-13, EUC-14, EUC-15, EUC-16, EUC-17, EUC-18, EUC-19, EUC-20 → INDETERMINATE
- **principal / Valid VAC/VDC with expired or absent mandate reaches consequential execution** → unauthorized delegated action → `Credential validity, delegation and authority remain non-substitutable` → joint authority/delegation/current-state checks → EUC-01, EUC-02, EUC-03, EUC-04, EUC-05, EUC-06, EUC-07, EUC-08, EUC-09, EUC-10, EUC-11, EUC-12, EUC-13, EUC-14, EUC-15, EUC-16, EUC-17, EUC-18, EUC-19, EUC-20 → INDETERMINATE
- **community administrator / One principal attempts widening its own ACL entry** → self-escalation → `Self-edit restrictions and exception boundaries are enforced at each transport` → ceiling-bound ACL updates and explicit exceptions → EUC-01, EUC-02, EUC-03, EUC-04, EUC-05, EUC-06, EUC-07, EUC-08, EUC-09, EUC-10, EUC-11, EUC-12, EUC-13, EUC-14, EUC-15, EUC-16, EUC-17, EUC-18, EUC-19, EUC-20 → INDETERMINATE
- **approver / Duplicate, stale or correlated approvals accumulate toward a threshold** → false independence and unauthorized action → `N approvals provide the declared independent authorization under actual host policy` → operation-bound approvals plus eligibility and deduplication → EUC-01, EUC-02, EUC-03, EUC-04, EUC-05, EUC-06, EUC-07, EUC-08, EUC-09, EUC-10, EUC-11, EUC-12, EUC-13, EUC-14, EUC-15, EUC-16, EUC-17, EUC-18, EUC-19, EUC-20 → INDETERMINATE
- **service operator / A task is replayed across transport change and restart** → duplicate or stale consequential effect → `Replay and restart cannot create a second authorization path` → freshness, durable replay state and idempotency → EUC-01, EUC-02, EUC-03, EUC-04, EUC-05, EUC-06, EUC-07, EUC-08, EUC-09, EUC-10, EUC-11, EUC-12, EUC-13, EUC-14, EUC-15, EUC-16, EUC-17, EUC-18, EUC-19, EUC-20 → INDETERMINATE
- **agent owner / Rev 2 client contacts Rev 3 service and relationship state changes** → downgrade or lost relationship authority → `Transport compatibility does not weaken authentication or relationship semantics` → version-bound codecs and fail-closed state transitions → EUC-01, EUC-02, EUC-03, EUC-04, EUC-05, EUC-06, EUC-07, EUC-08, EUC-09, EUC-10, EUC-11, EUC-12, EUC-13, EUC-14, EUC-15, EUC-16, EUC-17, EUC-18, EUC-19, EUC-20 → INDETERMINATE
- **room member / Removed member attempts access after MLS epoch rotation or succession** → confidentiality loss or custody lockout → `Room removal and custody succession preserve confidentiality and recoverability` → epoch rekey and explicit custodian succession → EUC-01, EUC-02, EUC-03, EUC-04, EUC-05, EUC-06, EUC-07, EUC-08, EUC-09, EUC-10, EUC-11, EUC-12, EUC-13, EUC-14, EUC-15, EUC-16, EUC-17, EUC-18, EUC-19, EUC-20 → INDETERMINATE
- **applicant / Hidden vetting is replayed or uses correlated attestations** → false admission or disclosure of vetters → `Hidden vetting enforces its declared threshold without excess disclosure` → distinct-attestation predicate and binding → EUC-01, EUC-02, EUC-03, EUC-04, EUC-05, EUC-06, EUC-07, EUC-08, EUC-09, EUC-10, EUC-11, EUC-12, EUC-13, EUC-14, EUC-15, EUC-16, EUC-17, EUC-18, EUC-19, EUC-20 → INDETERMINATE
- **holder / Faces are reused, composed or retired across communities** → cross-context correlation and disclosure → `Persona and face boundaries survive composed credential/task/UI use` → context boundaries and lifecycle checks → EUC-01, EUC-02, EUC-03, EUC-04, EUC-05, EUC-06, EUC-07, EUC-08, EUC-09, EUC-10, EUC-11, EUC-12, EUC-13, EUC-14, EUC-15, EUC-16, EUC-17, EUC-18, EUC-19, EUC-20 → INDETERMINATE
- **repository contributor / Unauthorized push, unapproved PR or stale membership reaches forge** → unauthorized merge or misattributed code → `Forge enforcement preserves current authority through PR, approval and merge` → forge gate plus current authorization and protected signing → EUC-01, EUC-02, EUC-03, EUC-04, EUC-05, EUC-06, EUC-07, EUC-08, EUC-09, EUC-10, EUC-11, EUC-12, EUC-13, EUC-14, EUC-15, EUC-16, EUC-17, EUC-18, EUC-19, EUC-20 → INDETERMINATE
- **mediator operator / Queue purge or runtime configuration mutation occurs without authority** → message loss or unsafe routing → `Mediator administration stays authorized and auditable` → signed management and least privilege → EUC-01, EUC-02, EUC-03, EUC-04, EUC-05, EUC-06, EUC-07, EUC-08, EUC-09, EUC-10, EUC-11, EUC-12, EUC-13, EUC-14, EUC-15, EUC-16, EUC-17, EUC-18, EUC-19, EUC-20 → INDETERMINATE
- **relying party / Resolution follows a private address, redirect or rebound DNS** → SSRF and confidential data exposure → `Network guards hold across actual resolver and transport composition` → egress guard and DNS vetting → EUC-01, EUC-02, EUC-03, EUC-04, EUC-05, EUC-06, EUC-07, EUC-08, EUC-09, EUC-10, EUC-11, EUC-12, EUC-13, EUC-14, EUC-15, EUC-16, EUC-17, EUC-18, EUC-19, EUC-20 → INDETERMINATE
- **auditor / Evidence is truncated, rolled back or moved after key rotation** → undetectable tampering or failed redress → `Audit and retained task evidence support challenge without silent tampering` → hash-chain verification and durable attributable receipts → EUC-01, EUC-02, EUC-03, EUC-04, EUC-05, EUC-06, EUC-07, EUC-08, EUC-09, EUC-10, EUC-11, EUC-12, EUC-13, EUC-14, EUC-15, EUC-16, EUC-17, EUC-18, EUC-19, EUC-20 → INDETERMINATE
- **key custodian / Hybrid proof set omits one proof or signs under wrong algorithm** → algorithm downgrade or custody compromise → `Post-quantum and hybrid processing reject omitted or incompatible proofs` → algorithm-bound keys and proof-set verification → EUC-01, EUC-02, EUC-03, EUC-04, EUC-05, EUC-06, EUC-07, EUC-08, EUC-09, EUC-10, EUC-11, EUC-12, EUC-13, EUC-14, EUC-15, EUC-16, EUC-17, EUC-18, EUC-19, EUC-20 → INDETERMINATE
- **trust-registry administrator / Wrong sender mutates registry or stale signed answer is consumed** → illegitimate recognition or stale authority → `Registry mutations and reliance preserve authority and temporal meaning` → authenticated bound writes and signed responses → EUC-01, EUC-02, EUC-03, EUC-04, EUC-05, EUC-06, EUC-07, EUC-08, EUC-09, EUC-10, EUC-11, EUC-12, EUC-13, EUC-14, EUC-15, EUC-16, EUC-17, EUC-18, EUC-19, EUC-20 → INDETERMINATE
- **mobile approver / Pairing or push causes unattended approval** → owner consent bypass → `Mobile approval binds owner intent, displayed action and current authority` → device-bound key and deliberate approval gate → EUC-01, EUC-02, EUC-03, EUC-04, EUC-05, EUC-06, EUC-07, EUC-08, EUC-09, EUC-10, EUC-11, EUC-12, EUC-13, EUC-14, EUC-15, EUC-16, EUC-17, EUC-18, EUC-19, EUC-20 → INDETERMINATE
- **agent operator / Recalled memory carries executable instructions or excessive data** → prompt injection and secret exposure → `Agent memory cannot silently acquire instruction authority` → untrusted-data fence and bounded storage → EUC-01, EUC-02, EUC-03, EUC-04, EUC-05, EUC-06, EUC-07, EUC-08, EUC-09, EUC-10, EUC-11, EUC-12, EUC-13, EUC-14, EUC-15, EUC-16, EUC-17, EUC-18, EUC-19, EUC-20 → INDETERMINATE
- **relying party / Expired token, wrong audience or malicious canonicalization reaches session** → session substitution or denial of service → `RP sessions are bound to audience, challenge, time and valid proof` → expiry/audience/challenge checks and bounded canonicalization → EUC-01, EUC-02, EUC-03, EUC-04, EUC-05, EUC-06, EUC-07, EUC-08, EUC-09, EUC-10, EUC-11, EUC-12, EUC-13, EUC-14, EUC-15, EUC-16, EUC-17, EUC-18, EUC-19, EUC-20 → INDETERMINATE
- **new adopter / Coordinated tags are treated as a guarantee of dependency compatibility** → false assurance or unreproducible build → `Actual build inputs and cross-project consumption match the claimed baseline` → exact lockfiles and producer-consumer version skew tests → EUC-01, EUC-02, EUC-03, EUC-04, EUC-05, EUC-06, EUC-07, EUC-08, EUC-09, EUC-10, EUC-11, EUC-12, EUC-13, EUC-14, EUC-15, EUC-16, EUC-17, EUC-18, EUC-19, EUC-20 → INDETERMINATE
- **excluded participant / Participant cannot complete gesture or challenge an adverse decision** → exclusion, loss of autonomy or unreviewable denial → `Consent and redress remain usable for affected people` → accessible alternative journey and durable redress → EUC-01, EUC-02, EUC-03, EUC-04, EUC-05, EUC-06, EUC-07, EUC-08, EUC-09, EUC-10, EUC-11, EUC-12, EUC-13, EUC-14, EUC-15, EUC-16, EUC-17, EUC-18, EUC-19, EUC-20 → INDETERMINATE

## Residuals

- Source inspection and bounded component checks do not establish this consequential composition. Attributable positive, negative and adversarial traces from the pinned consuming composition, including configuration, policy, clock, participants, expected/observed outcomes and effects; specialist return where privacy or human independence is asserted.
- Source inspection and bounded component checks do not establish this consequential composition. Attributable positive, negative and adversarial traces from the pinned consuming composition, including configuration, policy, clock, participants, expected/observed outcomes and effects; specialist return where privacy or human independence is asserted.
- Source inspection and bounded component checks do not establish this consequential composition. Attributable positive, negative and adversarial traces from the pinned consuming composition, including configuration, policy, clock, participants, expected/observed outcomes and effects; specialist return where privacy or human independence is asserted.
- Source inspection and bounded component checks do not establish this consequential composition. Attributable positive, negative and adversarial traces from the pinned consuming composition, including configuration, policy, clock, participants, expected/observed outcomes and effects; specialist return where privacy or human independence is asserted.
- Source inspection and bounded component checks do not establish this consequential composition. Attributable positive, negative and adversarial traces from the pinned consuming composition, including configuration, policy, clock, participants, expected/observed outcomes and effects; specialist return where privacy or human independence is asserted.
- Source inspection and bounded component checks do not establish this consequential composition. Attributable positive, negative and adversarial traces from the pinned consuming composition, including configuration, policy, clock, participants, expected/observed outcomes and effects; specialist return where privacy or human independence is asserted.
- Source inspection and bounded component checks do not establish this consequential composition. Attributable positive, negative and adversarial traces from the pinned consuming composition, including configuration, policy, clock, participants, expected/observed outcomes and effects; specialist return where privacy or human independence is asserted.
- Source inspection and bounded component checks do not establish this consequential composition. Attributable positive, negative and adversarial traces from the pinned consuming composition, including configuration, policy, clock, participants, expected/observed outcomes and effects; specialist return where privacy or human independence is asserted.
- Source inspection and bounded component checks do not establish this consequential composition. Attributable positive, negative and adversarial traces from the pinned consuming composition, including configuration, policy, clock, participants, expected/observed outcomes and effects; specialist return where privacy or human independence is asserted.
- Source inspection and bounded component checks do not establish this consequential composition. Attributable positive, negative and adversarial traces from the pinned consuming composition, including configuration, policy, clock, participants, expected/observed outcomes and effects; specialist return where privacy or human independence is asserted.
- Source inspection and bounded component checks do not establish this consequential composition. Attributable positive, negative and adversarial traces from the pinned consuming composition, including configuration, policy, clock, participants, expected/observed outcomes and effects; specialist return where privacy or human independence is asserted.
- Source inspection and bounded component checks do not establish this consequential composition. Attributable positive, negative and adversarial traces from the pinned consuming composition, including configuration, policy, clock, participants, expected/observed outcomes and effects; specialist return where privacy or human independence is asserted.
- Source inspection and bounded component checks do not establish this consequential composition. Attributable positive, negative and adversarial traces from the pinned consuming composition, including configuration, policy, clock, participants, expected/observed outcomes and effects; specialist return where privacy or human independence is asserted.
- Source inspection and bounded component checks do not establish this consequential composition. Attributable positive, negative and adversarial traces from the pinned consuming composition, including configuration, policy, clock, participants, expected/observed outcomes and effects; specialist return where privacy or human independence is asserted.
- Source inspection and bounded component checks do not establish this consequential composition. Attributable positive, negative and adversarial traces from the pinned consuming composition, including configuration, policy, clock, participants, expected/observed outcomes and effects; specialist return where privacy or human independence is asserted.
- Source inspection and bounded component checks do not establish this consequential composition. Attributable positive, negative and adversarial traces from the pinned consuming composition, including configuration, policy, clock, participants, expected/observed outcomes and effects; specialist return where privacy or human independence is asserted.
- Source inspection and bounded component checks do not establish this consequential composition. Attributable positive, negative and adversarial traces from the pinned consuming composition, including configuration, policy, clock, participants, expected/observed outcomes and effects; specialist return where privacy or human independence is asserted.
- Source inspection and bounded component checks do not establish this consequential composition. Attributable positive, negative and adversarial traces from the pinned consuming composition, including configuration, policy, clock, participants, expected/observed outcomes and effects; specialist return where privacy or human independence is asserted.
- Source inspection and bounded component checks do not establish this consequential composition. Attributable positive, negative and adversarial traces from the pinned consuming composition, including configuration, policy, clock, participants, expected/observed outcomes and effects; specialist return where privacy or human independence is asserted.
- Source inspection and bounded component checks do not establish this consequential composition. Attributable positive, negative and adversarial traces from the pinned consuming composition, including configuration, policy, clock, participants, expected/observed outcomes and effects; specialist return where privacy or human independence is asserted.

## Actionable remediation

### evidence-test

VTI / Trust Tasks: Execute signed/unsigned, wrong-sender and nested-transport requests through VTA, VTC, mediator and push doors; verify zero forbidden effects.

**Acceptance criterion:** Attributable positive, negative and adversarial traces from the pinned consuming composition, including configuration, policy, clock, participants, expected/observed outcomes and effects; specialist return where privacy or human independence is asserted.

### evidence-test

DTG Credentials / VTI: Exercise both substitution directions and revoke authority between verification and commit.

**Acceptance criterion:** Attributable positive, negative and adversarial traces from the pinned consuming composition, including configuration, policy, clock, participants, expected/observed outcomes and effects; specialist return where privacy or human independence is asserted.

### evidence-test

VTI / deployment operator: Execute label-only, widening, narrowing, sole-admin and multiple-person configurations across HTTPS/DIDComm/TSP; assert audit-before-effect.

**Acceptance criterion:** Attributable positive, negative and adversarial traces from the pinned consuming composition, including configuration, policy, clock, participants, expected/observed outcomes and effects; specialist return where privacy or human independence is asserted.

### evidence-test

VTI / community governance: Exercise repeated approver, requester approval, stale approval, role reduction, threshold change, cancellation, cooling-off and real single-person/multi-person policy.

**Acceptance criterion:** Attributable positive, negative and adversarial traces from the pinned consuming composition, including configuration, policy, clock, participants, expected/observed outcomes and effects; specialist return where privacy or human independence is asserted.

### evidence-test

VTI / mediator: Capture and replay identical task, changed payload under same ID, expired consent and post-restart retries; inspect effects and durable state.

**Acceptance criterion:** Attributable positive, negative and adversarial traces from the pinned consuming composition, including configuration, policy, clock, participants, expected/observed outcomes and effects; specialist return where privacy or human independence is asserted.

### evidence-test

TDK / Go / Dart / browser: Execute independent byte vectors and old/new endpoint pairs, nested mediator sends, restart and forged relationship transitions.

**Acceptance criterion:** Attributable positive, negative and adversarial traces from the pinned consuming composition, including configuration, policy, clock, participants, expected/observed outcomes and effects; specialist return where privacy or human independence is asserted.

### evidence-test

VTI Rooms / deployment operator: Run host, native and browser participants; remove member, rekey, rotate custodian, replay old epoch and corrupt Merkle record.

**Acceptance criterion:** Attributable positive, negative and adversarial traces from the pinned consuming composition, including configuration, policy, clock, participants, expected/observed outcomes and effects; specialist return where privacy or human independence is asserted.

### evidence-test

PCS / DPIP specialist / VTI: Execute duplicate-vetter, wrong-context, withdrawn-vetter, nonce replay and public/hidden A-B journeys with observable transcripts.

**Acceptance criterion:** Attributable positive, negative and adversarial traces from the pinned consuming composition, including configuration, policy, clock, participants, expected/observed outcomes and effects; specialist return where privacy or human independence is asserted.

### evidence-test

DPIP specialist / OpenVTC / VTA: Compare two contexts through issuance, presentation, status discovery, task retention and retirement; measure stable joins and required disclosures.

**Acceptance criterion:** Attributable positive, negative and adversarial traces from the pinned consuming composition, including configuration, policy, clock, participants, expected/observed outcomes and effects; specialist return where privacy or human independence is asserted.

### evidence-test

VGI / VTC / forge operator: Run GitHub and Forgejo adapters against sandbox forges; bypass PR gate, revoke member after approval, replay webhook, exercise break-glass and inspect signer attribution.

**Acceptance criterion:** Attributable positive, negative and adversarial traces from the pinned consuming composition, including configuration, policy, clock, participants, expected/observed outcomes and effects; specialist return where privacy or human independence is asserted.

### evidence-test

TDK / mediator operator: Run unauthorized and authorized inspect/purge/patch/reload tasks; verify sender proof, ACL, restart and audit on every transport.

**Acceptance criterion:** Attributable positive, negative and adversarial traces from the pinned consuming composition, including configuration, policy, clock, participants, expected/observed outcomes and effects; specialist return where privacy or human independence is asserted.

### evidence-test

TDK / DID hosting / browser: Execute private/IP-encoding/redirect/rebinding vectors through real resolver, mediator client and DID hosting rather than the URL predicate alone.

**Acceptance criterion:** Attributable positive, negative and adversarial traces from the pinned consuming composition, including configuration, policy, clock, participants, expected/observed outcomes and effects; specialist return where privacy or human independence is asserted.

### evidence-test

VTA / VTC / governance operator: Tamper, truncate, roll back and rotate keys; independently verify chains and reconstruct a contested action after agent replacement.

**Acceptance criterion:** Attributable positive, negative and adversarial traces from the pinned consuming composition, including configuration, policy, clock, participants, expected/observed outcomes and effects; specialist return where privacy or human independence is asserted.

### evidence-test

VTI / TSP PQ: Exercise mixed algorithms, absent hybrid member, wrong key type, malformed signature and downgraded peer; pin actual crypto packages.

**Acceptance criterion:** Attributable positive, negative and adversarial traces from the pinned consuming composition, including configuration, policy, clock, participants, expected/observed outcomes and effects; specialist return where privacy or human independence is asserted.

### evidence-test

Trust registry / relying-party operator: Run unauthorized write, replay, key rotation, stale status and cross-context recognition; verify policy version, effective time and audit.

**Acceptance criterion:** Attributable positive, negative and adversarial traces from the pinned consuming composition, including configuration, policy, clock, participants, expected/observed outcomes and effects; specialist return where privacy or human independence is asserted.

### evidence-test

Mobile / push / VTA: Exercise unsolicited pairing, forged push, altered display/action digest, decline, expiry and revoked device through physical approval journey.

**Acceptance criterion:** Attributable positive, negative and adversarial traces from the pinned consuming composition, including configuration, policy, clock, participants, expected/observed outcomes and effects; specialist return where privacy or human independence is asserted.

### evidence-test

Agent memory / VTA operator: Feed delimiter escape, command injection, excessive record and cross-owner recall through actual MCP consumer; observe decisions and stored bytes.

**Acceptance criterion:** Attributable positive, negative and adversarial traces from the pinned consuming composition, including configuration, policy, clock, participants, expected/observed outcomes and effects; specialist return where privacy or human independence is asserted.

### evidence-test

RP SDK / browser operator: Run wrong recipient, stale token, reused challenge, deeply nested payload and modified signed token through actual relying service.

**Acceptance criterion:** Attributable positive, negative and adversarial traces from the pinned consuming composition, including configuration, policy, clock, participants, expected/observed outcomes and effects; specialist return where privacy or human independence is asserted.

### evidence-test

All component maintainers / RAHP: Build locked consumers; compare resolved package identities to coordinated sources and execute old/new request-schema and lifecycle pairs.

**Acceptance criterion:** Attributable positive, negative and adversarial traces from the pinned consuming composition, including configuration, policy, clock, participants, expected/observed outcomes and effects; specialist return where privacy or human independence is asserted.

### evidence-test

Community governance / client maintainers: Run assistive-technology and unavailable-device journeys; document supported alternatives and verify a challenged decision can be corrected without bypassing authority.

**Acceptance criterion:** Attributable positive, negative and adversarial traces from the pinned consuming composition, including configuration, policy, clock, participants, expected/observed outcomes and effects; specialist return where privacy or human independence is asserted.


## Machine-readable record

```yaml
schema: rahp-assurance-run-state/v1
assessment_id: rahp:f1df8dcef625798eacf5
correlation_key: 06bc77950b572bf0154bf01dea9cd6f839856e2ce668b5784fef834f1076a30e
subject:
  type: portfolio-composition
  id: DTG-VTC-EUCALYPTUS-2026-10-08
  components:
  - OpenVTC/openvtc
  - OpenVTC/verifiable-trust-infrastructure
  - affinidi/affinidi-tdk-rs
  - affinidi/affinidi-webvh-service
  - affinidi/affinidi-trust-registry-rs
  - trustoverip/dtgwg-trust-tasks-tf
  - OpenVTC/verifiable-git-infrastructure
  - OpenVTC/vta-browser-plugin
  - decentralized-identity/didwebvh-rs
  - OpenVTC/dtg-credentials
  - OpenVTC/predicate-credential-system
  - OpenVTC/vta-agent-memory
  - affinidi/affinidi-tsp-go
  - affinidi/affinidi-tsp-dart
  - OpenVTC/vti-push-gateway
  - OpenVTC/rp-sdk-js
  - OpenVTC/vti-didcomm-js
  - OpenVTC/vta-mobile-agent-ios
source_pins:
- repository: OpenVTC/verifiable-trust-infrastructure
  revision: 49f5f1beb61adc34bdf7cf0bd3eb10f594415b80
- repository: OpenVTC/openvtc
  revision: 2a4fa2b3c8e831dbe3184a1119c4c87b6f197220
- repository: affinidi/affinidi-tdk-rs
  revision: a1611baa011620a6ca62649b105c2b8c898f2653
- repository: affinidi/affinidi-webvh-service
  revision: 1686668623e0bba0e18880074d82794cb929a7fc
- repository: affinidi/affinidi-trust-registry-rs
  revision: c77052f9bffe8bb7b4a3f357d9ef54cf632950f0
- repository: trustoverip/dtgwg-trust-tasks-tf
  revision: 7b6bb488ffd838bef058310c909207d4a7b77125
- repository: OpenVTC/verifiable-git-infrastructure
  revision: 92f32dd4c107545bd42b009ca55fc1ed4759309d
- repository: OpenVTC/vta-browser-plugin
  revision: d6df67971688fd927cd5b095424fa4093d4264df
- repository: decentralized-identity/didwebvh-rs
  revision: 155eb4e71c9d45db57c6f7329f286bbd753e0138
- repository: OpenVTC/dtg-credentials
  revision: fc9954d8d529d312ebac7ec1d413179857474c96
- repository: OpenVTC/predicate-credential-system
  revision: 4be4598563f422b9a3a4e37032d22487836d322c
- repository: OpenVTC/vta-agent-memory
  revision: 85db98a8a9c6d25b673a38a9e7e60d3435f3fcc5
- repository: affinidi/affinidi-tsp-go
  revision: d32ca7cdde208e93509c1f140ad7ee04d52ca7cc
- repository: affinidi/affinidi-tsp-dart
  revision: a64814c8043d6af0955a3ce01bfc6033d8daeb78
- repository: OpenVTC/vti-push-gateway
  revision: 44342121e161ccb12e43013f33ce80abb2486acb
- repository: OpenVTC/rp-sdk-js
  revision: 8594c2acba4014232e842fe7613e8a7cdc0e2b0f
- repository: OpenVTC/vti-didcomm-js
  revision: afd11e1f5dab611118253d2ebaffd1cfee29962a
- repository: OpenVTC/vta-mobile-agent-ios
  revision: 863a1e912042b28908ec2cf3675677ad9c151e0e
- repository: sankarshanmukhopadhyay/trust-protocol-interop-lab
  revision: 895e1af0f441995cada90dad2a429e56885bd394
- repository: sankarshanmukhopadhyay/dtg-privacy-implementation-profile
  revision: 991c92bad6ccb61dbc2511162bf11a9eb59679e2
scope: Fresh source-pinned RAHP examination of all 18 VTI-Eucalyptus coordinated repositories,
  component test attempts and 20 consequential composition/human-harm propositions.
non_scope: Production certification; independent security or cryptographic audit;
  human risk acceptance; unpinned normative specifications; exhaustive path/feature
  coverage; native device, enclave and hosted-forge deployment claims. Full campaign
  scope does not mean every implementation path was executed.
personas:
- agent operator
- agent owner
- applicant
- approver
- auditor
- community administrator
- excluded participant
- holder
- key custodian
- mediator operator
- mobile approver
- new adopter
- principal
- relying party
- repository contributor
- requester
- room member
- service operator
- trust-registry administrator
scenarios:
- Forged or sender-mismatched task enters an authenticated transport
- Valid VAC/VDC with expired or absent mandate reaches consequential execution
- One principal attempts widening its own ACL entry
- Duplicate, stale or correlated approvals accumulate toward a threshold
- A task is replayed across transport change and restart
- Rev 2 client contacts Rev 3 service and relationship state changes
- Removed member attempts access after MLS epoch rotation or succession
- Hidden vetting is replayed or uses correlated attestations
- Faces are reused, composed or retired across communities
- Unauthorized push, unapproved PR or stale membership reaches forge
- Queue purge or runtime configuration mutation occurs without authority
- Resolution follows a private address, redirect or rebound DNS
- Evidence is truncated, rolled back or moved after key rotation
- Hybrid proof set omits one proof or signs under wrong algorithm
- Wrong sender mutates registry or stale signed answer is consumed
- Pairing or push causes unattended approval
- Recalled memory carries executable instructions or excessive data
- Expired token, wrong audience or malicious canonicalization reaches session
- Coordinated tags are treated as a guarantee of dependency compatibility
- Participant cannot complete gesture or challenge an adverse decision
risks: []
harms:
- unauthorized actuation
- unauthorized delegated action
- self-escalation
- false independence and unauthorized action
- duplicate or stale consequential effect
- downgrade or lost relationship authority
- confidentiality loss or custody lockout
- false admission or disclosure of vetters
- cross-context correlation and disclosure
- unauthorized merge or misattributed code
- message loss or unsafe routing
- SSRF and confidential data exposure
- undetectable tampering or failed redress
- algorithm downgrade or custody compromise
- illegitimate recognition or stale authority
- owner consent bypass
- prompt injection and secret exposure
- session substitution or denial of service
- false assurance or unreproducible build
- exclusion, loss of autonomy or unreviewable denial
assurance_propositions:
- Task proofs are bound to the actual sender across all consuming doors
- Credential validity, delegation and authority remain non-substitutable
- Self-edit restrictions and exception boundaries are enforced at each transport
- N approvals provide the declared independent authorization under actual host policy
- Replay and restart cannot create a second authorization path
- Transport compatibility does not weaken authentication or relationship semantics
- Room removal and custody succession preserve confidentiality and recoverability
- Hidden vetting enforces its declared threshold without excess disclosure
- Persona and face boundaries survive composed credential/task/UI use
- Forge enforcement preserves current authority through PR, approval and merge
- Mediator administration stays authorized and auditable
- Network guards hold across actual resolver and transport composition
- Audit and retained task evidence support challenge without silent tampering
- Post-quantum and hybrid processing reject omitted or incompatible proofs
- Registry mutations and reliance preserve authority and temporal meaning
- Mobile approval binds owner intent, displayed action and current authority
- Agent memory cannot silently acquire instruction authority
- RP sessions are bound to audience, challenge, time and valid proof
- Actual build inputs and cross-project consumption match the claimed baseline
- Consent and redress remain usable for affected people
requirements_examined:
- EUC-01
- EUC-02
- EUC-03
- EUC-04
- EUC-05
- EUC-06
- EUC-07
- EUC-08
- EUC-09
- EUC-10
- EUC-11
- EUC-12
- EUC-13
- EUC-14
- EUC-15
- EUC-16
- EUC-17
- EUC-18
- EUC-19
- EUC-20
cross_spec_assumptions: []
evidence:
- requirement_id: EUC-01
  class: model/evidence-contract-definition
  result: NOT_EVIDENCED
  attempt_state: NO_APPLICABLE_PRODUCER
  surface_classifications: []
  provenance:
    producer: null
    producer_revision: null
    attribution: VTI / Trust Tasks
    evidence_file: null
- requirement_id: EUC-02
  class: model/evidence-contract-definition
  result: NOT_EVIDENCED
  attempt_state: NO_APPLICABLE_PRODUCER
  surface_classifications: []
  provenance:
    producer: null
    producer_revision: null
    attribution: DTG Credentials / VTI
    evidence_file: null
- requirement_id: EUC-03
  class: model/evidence-contract-definition
  result: NOT_EVIDENCED
  attempt_state: NO_APPLICABLE_PRODUCER
  surface_classifications: []
  provenance:
    producer: null
    producer_revision: null
    attribution: VTI / deployment operator
    evidence_file: null
- requirement_id: EUC-04
  class: model/evidence-contract-definition
  result: NOT_EVIDENCED
  attempt_state: NO_APPLICABLE_PRODUCER
  surface_classifications: []
  provenance:
    producer: null
    producer_revision: null
    attribution: VTI / community governance
    evidence_file: null
- requirement_id: EUC-05
  class: model/evidence-contract-definition
  result: NOT_EVIDENCED
  attempt_state: NO_APPLICABLE_PRODUCER
  surface_classifications: []
  provenance:
    producer: null
    producer_revision: null
    attribution: VTI / mediator
    evidence_file: null
- requirement_id: EUC-06
  class: model/evidence-contract-definition
  result: NOT_EVIDENCED
  attempt_state: NO_APPLICABLE_PRODUCER
  surface_classifications: []
  provenance:
    producer: null
    producer_revision: null
    attribution: TDK / Go / Dart / browser
    evidence_file: null
- requirement_id: EUC-07
  class: model/evidence-contract-definition
  result: NOT_EVIDENCED
  attempt_state: ATTEMPTED_UNAVAILABLE
  surface_classifications: []
  provenance:
    producer: null
    producer_revision: null
    attribution: VTI Rooms / deployment operator
    evidence_file: null
- requirement_id: EUC-08
  class: model/evidence-contract-definition
  result: NOT_EVIDENCED
  attempt_state: ATTEMPTED_UNAVAILABLE
  surface_classifications: []
  provenance:
    producer: null
    producer_revision: null
    attribution: PCS / DPIP specialist / VTI
    evidence_file: null
- requirement_id: EUC-09
  class: model/evidence-contract-definition
  result: NOT_EVIDENCED
  attempt_state: ATTEMPTED_UNAVAILABLE
  surface_classifications: []
  provenance:
    producer: null
    producer_revision: null
    attribution: DPIP specialist / OpenVTC / VTA
    evidence_file: null
- requirement_id: EUC-10
  class: model/evidence-contract-definition
  result: NOT_EVIDENCED
  attempt_state: NO_APPLICABLE_PRODUCER
  surface_classifications: []
  provenance:
    producer: null
    producer_revision: null
    attribution: VGI / VTC / forge operator
    evidence_file: null
- requirement_id: EUC-11
  class: model/evidence-contract-definition
  result: NOT_EVIDENCED
  attempt_state: NO_APPLICABLE_PRODUCER
  surface_classifications: []
  provenance:
    producer: null
    producer_revision: null
    attribution: TDK / mediator operator
    evidence_file: null
- requirement_id: EUC-12
  class: model/evidence-contract-definition
  result: NOT_EVIDENCED
  attempt_state: ATTEMPTED_UNAVAILABLE
  surface_classifications: []
  provenance:
    producer: null
    producer_revision: null
    attribution: TDK / DID hosting / browser
    evidence_file: null
- requirement_id: EUC-13
  class: model/evidence-contract-definition
  result: NOT_EVIDENCED
  attempt_state: ATTEMPTED_UNAVAILABLE
  surface_classifications: []
  provenance:
    producer: null
    producer_revision: null
    attribution: VTA / VTC / governance operator
    evidence_file: null
- requirement_id: EUC-14
  class: model/evidence-contract-definition
  result: NOT_EVIDENCED
  attempt_state: NO_APPLICABLE_PRODUCER
  surface_classifications: []
  provenance:
    producer: null
    producer_revision: null
    attribution: VTI / TSP PQ
    evidence_file: null
- requirement_id: EUC-15
  class: model/evidence-contract-definition
  result: NOT_EVIDENCED
  attempt_state: NO_APPLICABLE_PRODUCER
  surface_classifications: []
  provenance:
    producer: null
    producer_revision: null
    attribution: Trust registry / relying-party operator
    evidence_file: null
- requirement_id: EUC-16
  class: model/evidence-contract-definition
  result: NOT_EVIDENCED
  attempt_state: NO_APPLICABLE_PRODUCER
  surface_classifications: []
  provenance:
    producer: null
    producer_revision: null
    attribution: Mobile / push / VTA
    evidence_file: null
- requirement_id: EUC-17
  class: model/evidence-contract-definition
  result: NOT_EVIDENCED
  attempt_state: NO_APPLICABLE_PRODUCER
  surface_classifications: []
  provenance:
    producer: null
    producer_revision: null
    attribution: Agent memory / VTA operator
    evidence_file: null
- requirement_id: EUC-18
  class: model/evidence-contract-definition
  result: NOT_EVIDENCED
  attempt_state: NO_APPLICABLE_PRODUCER
  surface_classifications: []
  provenance:
    producer: null
    producer_revision: null
    attribution: RP SDK / browser operator
    evidence_file: null
- requirement_id: EUC-19
  class: model/evidence-contract-definition
  result: NOT_EVIDENCED
  attempt_state: NO_APPLICABLE_PRODUCER
  surface_classifications: []
  provenance:
    producer: null
    producer_revision: null
    attribution: All component maintainers / RAHP
    evidence_file: null
- requirement_id: EUC-20
  class: model/evidence-contract-definition
  result: NOT_EVIDENCED
  attempt_state: NO_APPLICABLE_PRODUCER
  surface_classifications: []
  provenance:
    producer: null
    producer_revision: null
    attribution: Community governance / client maintainers
    evidence_file: null
- class: model/evidence-contract-definition
  result: EXECUTED_PASS
  provenance:
    id: dependencies-dtgwg-trust-tasks-tf
    source: dtgwg-trust-tasks-tf
    command:
    - npm
    - ci
    - --ignore-scripts
    - --fetch-retries=0
    - --fetch-timeout=10000
    - --audit=false
    - --fund=false
    purpose: Attempt locked JavaScript dependency acquisition; success alone carries
      no behavioral assurance.
    evidence_class: model/evidence-contract-definition
    timeout_seconds: 25
    class: model/evidence-contract-definition
    started_at: '2026-10-08T04:32:08.937939+00:00'
    returncode: 0
    state: EXECUTED_PASS
    reason: Pinned command completed; assurance limited to its declared purpose.
    duration_seconds: 1.094
    stdout:
      path: logs/dependencies-dtgwg-trust-tasks-tf.stdout.txt
      sha256: 49273be1aaed0170ae0157f99ba5297e134e11a6e6cc03c34aca5393b9ff358e
    stderr:
      path: logs/dependencies-dtgwg-trust-tasks-tf.stderr.txt
      sha256: 7125f194612fcff2f454c05d848e7cb71facc1967b4d5017e25b34fdee3ba74f
    repository: trustoverip/dtgwg-trust-tasks-tf
    revision: 7b6bb488ffd838bef058310c909207d4a7b77125
- class: model/evidence-contract-definition
  result: EXECUTED_PASS
  provenance:
    id: dependencies-vta-browser-plugin
    source: vta-browser-plugin
    command:
    - npm
    - ci
    - --ignore-scripts
    - --fetch-retries=0
    - --fetch-timeout=10000
    - --audit=false
    - --fund=false
    purpose: Attempt locked JavaScript dependency acquisition; success alone carries
      no behavioral assurance.
    evidence_class: model/evidence-contract-definition
    timeout_seconds: 25
    class: model/evidence-contract-definition
    started_at: '2026-10-08T04:32:10.032542+00:00'
    returncode: 0
    state: EXECUTED_PASS
    reason: Pinned command completed; assurance limited to its declared purpose.
    duration_seconds: 16.493
    stdout:
      path: logs/dependencies-vta-browser-plugin.stdout.txt
      sha256: 8d995fdd74298fbc6459c7fe175ce53de3c473f5bc0d35a645eca1118da90b5e
    stderr:
      path: logs/dependencies-vta-browser-plugin.stderr.txt
      sha256: 233a44148c19e2f8a5eadbaf1e2afc52adff40795eb386965ebfd3040c25295f
    repository: OpenVTC/vta-browser-plugin
    revision: d6df67971688fd927cd5b095424fa4093d4264df
- class: model/evidence-contract-definition
  result: EXECUTED_PASS
  provenance:
    id: dependencies-rp-sdk-js
    source: rp-sdk-js
    command:
    - npm
    - ci
    - --ignore-scripts
    - --fetch-retries=0
    - --fetch-timeout=10000
    - --audit=false
    - --fund=false
    purpose: Attempt locked JavaScript dependency acquisition; success alone carries
      no behavioral assurance.
    evidence_class: model/evidence-contract-definition
    timeout_seconds: 25
    class: model/evidence-contract-definition
    started_at: '2026-10-08T04:32:26.526031+00:00'
    returncode: 0
    state: EXECUTED_PASS
    reason: Pinned command completed; assurance limited to its declared purpose.
    duration_seconds: 1.114
    stdout:
      path: logs/dependencies-rp-sdk-js.stdout.txt
      sha256: c780b24e0cf1ad2fefc6665e7a16a029fef8d280296a159e51b08b8e7b079a3e
    stderr:
      path: logs/dependencies-rp-sdk-js.stderr.txt
      sha256: 7125f194612fcff2f454c05d848e7cb71facc1967b4d5017e25b34fdee3ba74f
    repository: OpenVTC/rp-sdk-js
    revision: 8594c2acba4014232e842fe7613e8a7cdc0e2b0f
- class: model/evidence-contract-definition
  result: EXECUTED_PASS
  provenance:
    id: dependencies-vti-didcomm-js
    source: vti-didcomm-js
    command:
    - npm
    - ci
    - --ignore-scripts
    - --fetch-retries=0
    - --fetch-timeout=10000
    - --audit=false
    - --fund=false
    purpose: Attempt locked JavaScript dependency acquisition; success alone carries
      no behavioral assurance.
    evidence_class: model/evidence-contract-definition
    timeout_seconds: 25
    class: model/evidence-contract-definition
    started_at: '2026-10-08T04:32:27.641139+00:00'
    returncode: 0
    state: EXECUTED_PASS
    reason: Pinned command completed; assurance limited to its declared purpose.
    duration_seconds: 0.908
    stdout:
      path: logs/dependencies-vti-didcomm-js.stdout.txt
      sha256: bc5d8a5c79e25fbcf51bae826061b65483f1baab7606e00c42d2c9c469a178e7
    stderr:
      path: logs/dependencies-vti-didcomm-js.stderr.txt
      sha256: 7125f194612fcff2f454c05d848e7cb71facc1967b4d5017e25b34fdee3ba74f
    repository: OpenVTC/vti-didcomm-js
    revision: afd11e1f5dab611118253d2ebaffd1cfee29962a
- class: runtime-observation
  result: EXECUTED_PASS
  provenance:
    id: didcomm-a256cbc-hs512
    source: vti-didcomm-js
    command:
    - node
    - --test
    - --test-reporter=tap
    - test/a256cbc-hs512.test.js
    purpose: Shipped JavaScript component vectors; no service-composition proof.
    timeout_seconds: 45
    class: runtime-observation
    started_at: '2026-10-08T04:32:28.549430+00:00'
    returncode: 0
    state: EXECUTED_PASS
    tests: 6
    passed: 6
    reason: Pinned component test vectors passed; no cross-service inference.
    duration_seconds: 0.203
    stdout:
      path: logs/didcomm-a256cbc-hs512.stdout.txt
      sha256: 1ab5c7887f4be0691513d5de525b2cf394d8ab66a3b81f34bea2ad23e80f699a
    stderr:
      path: logs/didcomm-a256cbc-hs512.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: OpenVTC/vti-didcomm-js
    revision: afd11e1f5dab611118253d2ebaffd1cfee29962a
- class: runtime-observation
  result: EXECUTED_PASS
  provenance:
    id: didcomm-aes
    source: vti-didcomm-js
    command:
    - node
    - --test
    - --test-reporter=tap
    - test/aes.test.js
    purpose: Shipped JavaScript component vectors; no service-composition proof.
    timeout_seconds: 45
    class: runtime-observation
    started_at: '2026-10-08T04:32:28.753110+00:00'
    returncode: 0
    state: EXECUTED_PASS
    tests: 4
    passed: 4
    reason: Pinned component test vectors passed; no cross-service inference.
    duration_seconds: 0.193
    stdout:
      path: logs/didcomm-aes.stdout.txt
      sha256: 77c881e1ab10e47ae2eed8dd301530e9bd36e241a1e17130d30b066cd58e8391
    stderr:
      path: logs/didcomm-aes.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: OpenVTC/vti-didcomm-js
    revision: afd11e1f5dab611118253d2ebaffd1cfee29962a
- class: runtime-observation
  result: EXECUTED_PASS
  provenance:
    id: didcomm-anoncrypt
    source: vti-didcomm-js
    command:
    - node
    - --test
    - --test-reporter=tap
    - test/anoncrypt.test.js
    purpose: Shipped JavaScript component vectors; no service-composition proof.
    timeout_seconds: 45
    class: runtime-observation
    started_at: '2026-10-08T04:32:28.947050+00:00'
    returncode: 0
    state: EXECUTED_PASS
    tests: 5
    passed: 3
    reason: Pinned component test vectors passed; no cross-service inference.
    duration_seconds: 0.287
    stdout:
      path: logs/didcomm-anoncrypt.stdout.txt
      sha256: 9b7fdad306dd4560f7f02ac738b1ab6dbc094872ff985f1239705c245ffa9bf8
    stderr:
      path: logs/didcomm-anoncrypt.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: OpenVTC/vti-didcomm-js
    revision: afd11e1f5dab611118253d2ebaffd1cfee29962a
- class: runtime-observation
  result: EXECUTED_PASS
  provenance:
    id: didcomm-base64url
    source: vti-didcomm-js
    command:
    - node
    - --test
    - --test-reporter=tap
    - test/base64url.test.js
    purpose: Shipped JavaScript component vectors; no service-composition proof.
    timeout_seconds: 45
    class: runtime-observation
    started_at: '2026-10-08T04:32:29.235505+00:00'
    returncode: 0
    state: EXECUTED_PASS
    tests: 19
    passed: 19
    reason: Pinned component test vectors passed; no cross-service inference.
    duration_seconds: 0.186
    stdout:
      path: logs/didcomm-base64url.stdout.txt
      sha256: ddb2b69ae333191e3c6055b9e9e575adedea435907f00b107c233cc92cc0b5c4
    stderr:
      path: logs/didcomm-base64url.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: OpenVTC/vti-didcomm-js
    revision: afd11e1f5dab611118253d2ebaffd1cfee29962a
- class: runtime-observation
  result: EXECUTED_PASS
  provenance:
    id: didcomm-concat-kdf
    source: vti-didcomm-js
    command:
    - node
    - --test
    - --test-reporter=tap
    - test/concat-kdf.test.js
    purpose: Shipped JavaScript component vectors; no service-composition proof.
    timeout_seconds: 45
    class: runtime-observation
    started_at: '2026-10-08T04:32:29.422580+00:00'
    returncode: 0
    state: EXECUTED_PASS
    tests: 13
    passed: 13
    reason: Pinned component test vectors passed; no cross-service inference.
    duration_seconds: 0.197
    stdout:
      path: logs/didcomm-concat-kdf.stdout.txt
      sha256: 2bfd9509e3a7a5c856ccb2be899e7b51f201655ecea1c9b7987570fd6fb2eb53
    stderr:
      path: logs/didcomm-concat-kdf.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: OpenVTC/vti-didcomm-js
    revision: afd11e1f5dab611118253d2ebaffd1cfee29962a
- class: runtime-observation
  result: EXECUTED_PASS
  provenance:
    id: didcomm-did-key
    source: vti-didcomm-js
    command:
    - node
    - --test
    - --test-reporter=tap
    - test/did-key.test.js
    purpose: Shipped JavaScript component vectors; no service-composition proof.
    timeout_seconds: 45
    class: runtime-observation
    started_at: '2026-10-08T04:32:29.620329+00:00'
    returncode: 0
    state: EXECUTED_PASS
    tests: 13
    passed: 13
    reason: Pinned component test vectors passed; no cross-service inference.
    duration_seconds: 0.326
    stdout:
      path: logs/didcomm-did-key.stdout.txt
      sha256: 48651ce0f4373f43a9449442828a17d6f7aee22b2d363af66c9c5f71719d4d38
    stderr:
      path: logs/didcomm-did-key.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: OpenVTC/vti-didcomm-js
    revision: afd11e1f5dab611118253d2ebaffd1cfee29962a
- class: runtime-observation
  result: EXECUTED_PASS
  provenance:
    id: didcomm-did-peer
    source: vti-didcomm-js
    command:
    - node
    - --test
    - --test-reporter=tap
    - test/did-peer.test.js
    purpose: Shipped JavaScript component vectors; no service-composition proof.
    timeout_seconds: 45
    class: runtime-observation
    started_at: '2026-10-08T04:32:29.947636+00:00'
    returncode: 0
    state: EXECUTED_PASS
    tests: 8
    passed: 8
    reason: Pinned component test vectors passed; no cross-service inference.
    duration_seconds: 0.281
    stdout:
      path: logs/didcomm-did-peer.stdout.txt
      sha256: e6f4b547436a3b93297d7294935ae814e3ed1e4443547b61983aa8fea9a390fe
    stderr:
      path: logs/didcomm-did-peer.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: OpenVTC/vti-didcomm-js
    revision: afd11e1f5dab611118253d2ebaffd1cfee29962a
- class: runtime-observation
  result: EXECUTED_PASS
  provenance:
    id: didcomm-did-webvh-ssrf
    source: vti-didcomm-js
    command:
    - node
    - --test
    - --test-reporter=tap
    - test/did-webvh-ssrf.test.js
    purpose: Shipped JavaScript component vectors; no service-composition proof.
    timeout_seconds: 45
    class: runtime-observation
    started_at: '2026-10-08T04:32:30.229285+00:00'
    returncode: 0
    state: EXECUTED_PASS
    tests: 13
    passed: 13
    reason: Pinned component test vectors passed; no cross-service inference.
    duration_seconds: 0.376
    stdout:
      path: logs/didcomm-did-webvh-ssrf.stdout.txt
      sha256: 861ab5e8ba915fd76fa3cccfa7eed2d1faa0a94237432ddf647bd942696f1b01
    stderr:
      path: logs/didcomm-did-webvh-ssrf.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: OpenVTC/vti-didcomm-js
    revision: afd11e1f5dab611118253d2ebaffd1cfee29962a
- class: runtime-observation
  result: EXECUTED_PASS
  provenance:
    id: didcomm-did-webvh
    source: vti-didcomm-js
    command:
    - node
    - --test
    - --test-reporter=tap
    - test/did-webvh.test.js
    purpose: Shipped JavaScript component vectors; no service-composition proof.
    timeout_seconds: 45
    class: runtime-observation
    started_at: '2026-10-08T04:32:30.606468+00:00'
    returncode: 0
    state: EXECUTED_PASS
    tests: 8
    passed: 4
    reason: Pinned component test vectors passed; no cross-service inference.
    duration_seconds: 0.206
    stdout:
      path: logs/didcomm-did-webvh.stdout.txt
      sha256: fb1e79aa8f329824cc1f8a52b83aa79f9a564fd32df467e7788b1d705c9786aa
    stderr:
      path: logs/didcomm-did-webvh.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: OpenVTC/vti-didcomm-js
    revision: afd11e1f5dab611118253d2ebaffd1cfee29962a
- class: runtime-observation
  result: EXECUTED_PASS
  provenance:
    id: didcomm-dns-rebinding
    source: vti-didcomm-js
    command:
    - node
    - --test
    - --test-reporter=tap
    - test/dns-rebinding.test.js
    purpose: Shipped JavaScript component vectors; no service-composition proof.
    timeout_seconds: 45
    class: runtime-observation
    started_at: '2026-10-08T04:32:30.813145+00:00'
    returncode: 0
    state: EXECUTED_PASS
    tests: 3
    passed: 3
    reason: Pinned component test vectors passed; no cross-service inference.
    duration_seconds: 0.319
    stdout:
      path: logs/didcomm-dns-rebinding.stdout.txt
      sha256: 421bf1d423c1627960c3b1a8cedcedad2593419f5eeda1016956f23c86e602e7
    stderr:
      path: logs/didcomm-dns-rebinding.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: OpenVTC/vti-didcomm-js
    revision: afd11e1f5dab611118253d2ebaffd1cfee29962a
- class: runtime-observation
  result: EXECUTED_PASS
  provenance:
    id: didcomm-ecdh-1pu
    source: vti-didcomm-js
    command:
    - node
    - --test
    - --test-reporter=tap
    - test/ecdh-1pu.test.js
    purpose: Shipped JavaScript component vectors; no service-composition proof.
    timeout_seconds: 45
    class: runtime-observation
    started_at: '2026-10-08T04:32:31.132778+00:00'
    returncode: 0
    state: EXECUTED_PASS
    tests: 3
    passed: 3
    reason: Pinned component test vectors passed; no cross-service inference.
    duration_seconds: 0.255
    stdout:
      path: logs/didcomm-ecdh-1pu.stdout.txt
      sha256: 2763a48f67e1239e1b9a7a250d1b7abe3be90bf6e8a08081b3046472c7d23a3c
    stderr:
      path: logs/didcomm-ecdh-1pu.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: OpenVTC/vti-didcomm-js
    revision: afd11e1f5dab611118253d2ebaffd1cfee29962a
- class: runtime-observation
  result: EXECUTED_PASS
  provenance:
    id: didcomm-ecdh-es
    source: vti-didcomm-js
    command:
    - node
    - --test
    - --test-reporter=tap
    - test/ecdh-es.test.js
    purpose: Shipped JavaScript component vectors; no service-composition proof.
    timeout_seconds: 45
    class: runtime-observation
    started_at: '2026-10-08T04:32:31.388874+00:00'
    returncode: 0
    state: EXECUTED_PASS
    tests: 4
    passed: 4
    reason: Pinned component test vectors passed; no cross-service inference.
    duration_seconds: 0.259
    stdout:
      path: logs/didcomm-ecdh-es.stdout.txt
      sha256: 8118ae64377a1e16cd0b5d217d14a56f9a9e8c8caff014dc92e20a9bc00ff8d0
    stderr:
      path: logs/didcomm-ecdh-es.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: OpenVTC/vti-didcomm-js
    revision: afd11e1f5dab611118253d2ebaffd1cfee29962a
- class: runtime-observation
  result: EXECUTED_PASS
  provenance:
    id: didcomm-ecdh-p256
    source: vti-didcomm-js
    command:
    - node
    - --test
    - --test-reporter=tap
    - test/ecdh-p256.test.js
    purpose: Shipped JavaScript component vectors; no service-composition proof.
    timeout_seconds: 45
    class: runtime-observation
    started_at: '2026-10-08T04:32:31.648435+00:00'
    returncode: 0
    state: EXECUTED_PASS
    tests: 3
    passed: 3
    reason: Pinned component test vectors passed; no cross-service inference.
    duration_seconds: 0.309
    stdout:
      path: logs/didcomm-ecdh-p256.stdout.txt
      sha256: ae35c1aeaef3a3b0001b37e800344c8273306472d7167d4e1842d76cbef047a6
    stderr:
      path: logs/didcomm-ecdh-p256.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: OpenVTC/vti-didcomm-js
    revision: afd11e1f5dab611118253d2ebaffd1cfee29962a
- class: runtime-observation
  result: EXECUTED_PASS
  provenance:
    id: didcomm-forward
    source: vti-didcomm-js
    command:
    - node
    - --test
    - --test-reporter=tap
    - test/forward.test.js
    purpose: Shipped JavaScript component vectors; no service-composition proof.
    timeout_seconds: 45
    class: runtime-observation
    started_at: '2026-10-08T04:32:31.958677+00:00'
    returncode: 0
    state: EXECUTED_PASS
    tests: 4
    passed: 3
    reason: Pinned component test vectors passed; no cross-service inference.
    duration_seconds: 0.234
    stdout:
      path: logs/didcomm-forward.stdout.txt
      sha256: 1570388a8318c29798b8a9f8775b2757ae0864f7eef3b4dc5067bed52dc5a371
    stderr:
      path: logs/didcomm-forward.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: OpenVTC/vti-didcomm-js
    revision: afd11e1f5dab611118253d2ebaffd1cfee29962a
- class: runtime-observation
  result: EXECUTED_PASS
  provenance:
    id: didcomm-jwk
    source: vti-didcomm-js
    command:
    - node
    - --test
    - --test-reporter=tap
    - test/jwk.test.js
    purpose: Shipped JavaScript component vectors; no service-composition proof.
    timeout_seconds: 45
    class: runtime-observation
    started_at: '2026-10-08T04:32:32.193596+00:00'
    returncode: 0
    state: EXECUTED_PASS
    tests: 15
    passed: 15
    reason: Pinned component test vectors passed; no cross-service inference.
    duration_seconds: 0.323
    stdout:
      path: logs/didcomm-jwk.stdout.txt
      sha256: 80db7ff25442399e80b0481161b2e94e5f8153623423497e9207956466761e15
    stderr:
      path: logs/didcomm-jwk.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: OpenVTC/vti-didcomm-js
    revision: afd11e1f5dab611118253d2ebaffd1cfee29962a
- class: runtime-observation
  result: EXECUTED_PASS
  provenance:
    id: didcomm-key-agreement
    source: vti-didcomm-js
    command:
    - node
    - --test
    - --test-reporter=tap
    - test/key-agreement.test.js
    purpose: Shipped JavaScript component vectors; no service-composition proof.
    timeout_seconds: 45
    class: runtime-observation
    started_at: '2026-10-08T04:32:32.517621+00:00'
    returncode: 0
    state: EXECUTED_PASS
    tests: 6
    passed: 6
    reason: Pinned component test vectors passed; no cross-service inference.
    duration_seconds: 0.321
    stdout:
      path: logs/didcomm-key-agreement.stdout.txt
      sha256: 71f91bacec2556ed53acb84131f2f94c062ac4251abf92438a54f1b96604da1e
    stderr:
      path: logs/didcomm-key-agreement.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: OpenVTC/vti-didcomm-js
    revision: afd11e1f5dab611118253d2ebaffd1cfee29962a
- class: runtime-observation
  result: EXECUTED_NONZERO
  provenance:
    id: didcomm-mediator-auth-ssrf
    source: vti-didcomm-js
    command:
    - node
    - --test
    - --test-reporter=tap
    - test/mediator-auth-ssrf.test.js
    purpose: Shipped JavaScript component vectors; no service-composition proof.
    timeout_seconds: 45
    class: runtime-observation
    started_at: '2026-10-08T04:32:32.840034+00:00'
    returncode: 1
    state: EXECUTED_NONZERO
    reason: Nonzero execution requires diagnosis; neither automatic defect finding
      nor PASS.
    duration_seconds: 10.804
    stdout:
      path: logs/didcomm-mediator-auth-ssrf.stdout.txt
      sha256: cbbb618167ec6b0e5c2d469eebce723bfac8514c591f3e6a51838e39557d0b39
    stderr:
      path: logs/didcomm-mediator-auth-ssrf.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: OpenVTC/vti-didcomm-js
    revision: afd11e1f5dab611118253d2ebaffd1cfee29962a
- class: runtime-observation
  result: EXECUTED_PASS
  provenance:
    id: didcomm-mediator-auth
    source: vti-didcomm-js
    command:
    - node
    - --test
    - --test-reporter=tap
    - test/mediator-auth.test.js
    purpose: Shipped JavaScript component vectors; no service-composition proof.
    timeout_seconds: 45
    class: runtime-observation
    started_at: '2026-10-08T04:32:43.644852+00:00'
    returncode: 0
    state: EXECUTED_PASS
    tests: 9
    passed: 7
    reason: Pinned component test vectors passed; no cross-service inference.
    duration_seconds: 0.301
    stdout:
      path: logs/didcomm-mediator-auth.stdout.txt
      sha256: aad0ae2304a741ad83168ad8f836b674f6f530a66e66de438205b73c207b012f
    stderr:
      path: logs/didcomm-mediator-auth.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: OpenVTC/vti-didcomm-js
    revision: afd11e1f5dab611118253d2ebaffd1cfee29962a
- class: runtime-observation
  result: EXECUTED_PASS
  provenance:
    id: didcomm-mediator-transport
    source: vti-didcomm-js
    command:
    - node
    - --test
    - --test-reporter=tap
    - test/mediator-transport.test.js
    purpose: Shipped JavaScript component vectors; no service-composition proof.
    timeout_seconds: 45
    class: runtime-observation
    started_at: '2026-10-08T04:32:43.946669+00:00'
    returncode: 0
    state: EXECUTED_PASS
    tests: 36
    passed: 36
    reason: Pinned component test vectors passed; no cross-service inference.
    duration_seconds: 1.671
    stdout:
      path: logs/didcomm-mediator-transport.stdout.txt
      sha256: 98c19de657c094e541d12770e97bf105752ac67d2496a1ae9cb27defc3057416
    stderr:
      path: logs/didcomm-mediator-transport.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: OpenVTC/vti-didcomm-js
    revision: afd11e1f5dab611118253d2ebaffd1cfee29962a
- class: runtime-observation
  result: EXECUTED_PASS
  provenance:
    id: didcomm-migration-fallback
    source: vti-didcomm-js
    command:
    - node
    - --test
    - --test-reporter=tap
    - test/migration-fallback.test.js
    purpose: Shipped JavaScript component vectors; no service-composition proof.
    timeout_seconds: 45
    class: runtime-observation
    started_at: '2026-10-08T04:32:45.618599+00:00'
    returncode: 0
    state: EXECUTED_PASS
    tests: 3
    passed: 3
    reason: Pinned component test vectors passed; no cross-service inference.
    duration_seconds: 0.294
    stdout:
      path: logs/didcomm-migration-fallback.stdout.txt
      sha256: b2b7241061d77aaec6942fa79c1f6c4e63995a7e6d2107b5ed8c50ce7510464d
    stderr:
      path: logs/didcomm-migration-fallback.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: OpenVTC/vti-didcomm-js
    revision: afd11e1f5dab611118253d2ebaffd1cfee29962a
- class: runtime-observation
  result: EXECUTED_PASS
  provenance:
    id: didcomm-multibase
    source: vti-didcomm-js
    command:
    - node
    - --test
    - --test-reporter=tap
    - test/multibase.test.js
    purpose: Shipped JavaScript component vectors; no service-composition proof.
    timeout_seconds: 45
    class: runtime-observation
    started_at: '2026-10-08T04:32:45.913220+00:00'
    returncode: 0
    state: EXECUTED_PASS
    tests: 14
    passed: 14
    reason: Pinned component test vectors passed; no cross-service inference.
    duration_seconds: 0.185
    stdout:
      path: logs/didcomm-multibase.stdout.txt
      sha256: 7fc7d80f9bea5d2cb96881a851b67ad75fc56fbc5a0693b7b863a3519c77eca7
    stderr:
      path: logs/didcomm-multibase.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: OpenVTC/vti-didcomm-js
    revision: afd11e1f5dab611118253d2ebaffd1cfee29962a
- class: runtime-observation
  result: EXECUTED_PASS
  provenance:
    id: didcomm-net-guard-node
    source: vti-didcomm-js
    command:
    - node
    - --test
    - --test-reporter=tap
    - test/net-guard-node.test.js
    purpose: Shipped JavaScript component vectors; no service-composition proof.
    timeout_seconds: 45
    class: runtime-observation
    started_at: '2026-10-08T04:32:46.099731+00:00'
    returncode: 0
    state: EXECUTED_PASS
    tests: 4
    passed: 4
    reason: Pinned component test vectors passed; no cross-service inference.
    duration_seconds: 0.201
    stdout:
      path: logs/didcomm-net-guard-node.stdout.txt
      sha256: 8a6c6a7369ee8bd8ba9ec92ddaf728a300773abc3e7750c053f88cd2835e2c7e
    stderr:
      path: logs/didcomm-net-guard-node.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: OpenVTC/vti-didcomm-js
    revision: afd11e1f5dab611118253d2ebaffd1cfee29962a
- class: runtime-observation
  result: EXECUTED_PASS
  provenance:
    id: didcomm-net-guard
    source: vti-didcomm-js
    command:
    - node
    - --test
    - --test-reporter=tap
    - test/net-guard.test.js
    purpose: Shipped JavaScript component vectors; no service-composition proof.
    timeout_seconds: 45
    class: runtime-observation
    started_at: '2026-10-08T04:32:46.301149+00:00'
    returncode: 0
    state: EXECUTED_PASS
    tests: 20
    passed: 20
    reason: Pinned component test vectors passed; no cross-service inference.
    duration_seconds: 0.246
    stdout:
      path: logs/didcomm-net-guard.stdout.txt
      sha256: 51443a4a5b954f0ddd2935561bb5fa6461a787e9b121fabfae4f47d6989bba4b
    stderr:
      path: logs/didcomm-net-guard.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: OpenVTC/vti-didcomm-js
    revision: afd11e1f5dab611118253d2ebaffd1cfee29962a
- class: runtime-observation
  result: EXECUTED_PASS
  provenance:
    id: didcomm-p256
    source: vti-didcomm-js
    command:
    - node
    - --test
    - --test-reporter=tap
    - test/p256.test.js
    purpose: Shipped JavaScript component vectors; no service-composition proof.
    timeout_seconds: 45
    class: runtime-observation
    started_at: '2026-10-08T04:32:46.548697+00:00'
    returncode: 0
    state: EXECUTED_PASS
    tests: 7
    passed: 7
    reason: Pinned component test vectors passed; no cross-service inference.
    duration_seconds: 0.336
    stdout:
      path: logs/didcomm-p256.stdout.txt
      sha256: 40f4bf29c0cdc48dcfee0a0e3d27f142fed0550926a76b10dac50be56f426467
    stderr:
      path: logs/didcomm-p256.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: OpenVTC/vti-didcomm-js
    revision: afd11e1f5dab611118253d2ebaffd1cfee29962a
- class: runtime-observation
  result: EXECUTED_PASS
  provenance:
    id: didcomm-pack-unpack-p256
    source: vti-didcomm-js
    command:
    - node
    - --test
    - --test-reporter=tap
    - test/pack-unpack-p256.test.js
    purpose: Shipped JavaScript component vectors; no service-composition proof.
    timeout_seconds: 45
    class: runtime-observation
    started_at: '2026-10-08T04:32:46.886707+00:00'
    returncode: 0
    state: EXECUTED_PASS
    tests: 6
    passed: 6
    reason: Pinned component test vectors passed; no cross-service inference.
    duration_seconds: 0.76
    stdout:
      path: logs/didcomm-pack-unpack-p256.stdout.txt
      sha256: 5ab06fd68d5b35e323d21622792ae32149093c1614d3ed62b77e09ab8a46e2ec
    stderr:
      path: logs/didcomm-pack-unpack-p256.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: OpenVTC/vti-didcomm-js
    revision: afd11e1f5dab611118253d2ebaffd1cfee29962a
- class: runtime-observation
  result: EXECUTED_PASS
  provenance:
    id: didcomm-pack-unpack
    source: vti-didcomm-js
    command:
    - node
    - --test
    - --test-reporter=tap
    - test/pack-unpack.test.js
    purpose: Shipped JavaScript component vectors; no service-composition proof.
    timeout_seconds: 45
    class: runtime-observation
    started_at: '2026-10-08T04:32:47.647933+00:00'
    returncode: 0
    state: EXECUTED_PASS
    tests: 8
    passed: 8
    reason: Pinned component test vectors passed; no cross-service inference.
    duration_seconds: 0.344
    stdout:
      path: logs/didcomm-pack-unpack.stdout.txt
      sha256: c5c33e56279a1d76440fa8e4d4d1edad7f08aa3ab1d3f3cbfec31ec26c10aec2
    stderr:
      path: logs/didcomm-pack-unpack.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: OpenVTC/vti-didcomm-js
    revision: afd11e1f5dab611118253d2ebaffd1cfee29962a
- class: runtime-observation
  result: EXECUTED_PASS
  provenance:
    id: didcomm-resolver
    source: vti-didcomm-js
    command:
    - node
    - --test
    - --test-reporter=tap
    - test/resolver.test.js
    purpose: Shipped JavaScript component vectors; no service-composition proof.
    timeout_seconds: 45
    class: runtime-observation
    started_at: '2026-10-08T04:32:47.993216+00:00'
    returncode: 0
    state: EXECUTED_PASS
    tests: 19
    passed: 19
    reason: Pinned component test vectors passed; no cross-service inference.
    duration_seconds: 0.247
    stdout:
      path: logs/didcomm-resolver.stdout.txt
      sha256: 18f0a54a6a3dc40ca87dc81e646fd9639a94d06b4d95ef229c30d37b139b7d82
    stderr:
      path: logs/didcomm-resolver.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: OpenVTC/vti-didcomm-js
    revision: afd11e1f5dab611118253d2ebaffd1cfee29962a
- class: model/evidence-contract-definition
  result: ATTEMPTED_UNAVAILABLE
  provenance:
    id: didcomm-roundtrip-rust
    source: vti-didcomm-js
    command:
    - node
    - --test
    - --test-reporter=tap
    - test/roundtrip-rust.test.js
    purpose: Shipped JavaScript component vectors; no service-composition proof.
    timeout_seconds: 45
    class: runtime-observation
    started_at: '2026-10-08T04:32:48.241419+00:00'
    returncode: 0
    state: ATTEMPTED_UNAVAILABLE
    reason: zero or unverified executed test count
    duration_seconds: 0.208
    stdout:
      path: logs/didcomm-roundtrip-rust.stdout.txt
      sha256: ddc3c1549bf9aebeea27ced78ca1d70cc28d6314358752591ce483937ece7bd3
    stderr:
      path: logs/didcomm-roundtrip-rust.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: OpenVTC/vti-didcomm-js
    revision: afd11e1f5dab611118253d2ebaffd1cfee29962a
- class: runtime-observation
  result: EXECUTED_PASS
  provenance:
    id: didcomm-sender-binding
    source: vti-didcomm-js
    command:
    - node
    - --test
    - --test-reporter=tap
    - test/sender-binding.test.js
    purpose: Shipped JavaScript component vectors; no service-composition proof.
    timeout_seconds: 45
    class: runtime-observation
    started_at: '2026-10-08T04:32:48.450127+00:00'
    returncode: 0
    state: EXECUTED_PASS
    tests: 12
    passed: 12
    reason: Pinned component test vectors passed; no cross-service inference.
    duration_seconds: 0.478
    stdout:
      path: logs/didcomm-sender-binding.stdout.txt
      sha256: d4124e2a419199ccb618bcbc9501b76176d4d4c697a49e8f5d365743e50ee4a4
    stderr:
      path: logs/didcomm-sender-binding.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: OpenVTC/vti-didcomm-js
    revision: afd11e1f5dab611118253d2ebaffd1cfee29962a
- class: runtime-observation
  result: EXECUTED_PASS
  provenance:
    id: didcomm-tsp-frame
    source: vti-didcomm-js
    command:
    - node
    - --test
    - --test-reporter=tap
    - test/tsp-frame.test.js
    purpose: Shipped JavaScript component vectors; no service-composition proof.
    timeout_seconds: 45
    class: runtime-observation
    started_at: '2026-10-08T04:32:48.929352+00:00'
    returncode: 0
    state: EXECUTED_PASS
    tests: 7
    passed: 7
    reason: Pinned component test vectors passed; no cross-service inference.
    duration_seconds: 0.183
    stdout:
      path: logs/didcomm-tsp-frame.stdout.txt
      sha256: 5bf623d720e175f2bdb5b8944976a5f2174d8c00fdd120d302467802860130dd
    stderr:
      path: logs/didcomm-tsp-frame.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: OpenVTC/vti-didcomm-js
    revision: afd11e1f5dab611118253d2ebaffd1cfee29962a
- class: runtime-observation
  result: EXECUTED_NONZERO
  provenance:
    id: didcomm-vta-didcomm
    source: vti-didcomm-js
    command:
    - node
    - --test
    - --test-reporter=tap
    - test/vta-didcomm.test.js
    purpose: Shipped JavaScript component vectors; no service-composition proof.
    timeout_seconds: 45
    class: runtime-observation
    started_at: '2026-10-08T04:32:49.112879+00:00'
    returncode: 1
    state: EXECUTED_NONZERO
    reason: Nonzero execution requires diagnosis; neither automatic defect finding
      nor PASS.
    duration_seconds: 9.945
    stdout:
      path: logs/didcomm-vta-didcomm.stdout.txt
      sha256: b23430488dee11fd7e9ba6f2c6378722ec17c09f76b8e6eb2d1808dc1f838e3a
    stderr:
      path: logs/didcomm-vta-didcomm.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: OpenVTC/vti-didcomm-js
    revision: afd11e1f5dab611118253d2ebaffd1cfee29962a
- class: runtime-observation
  result: EXECUTED_PASS
  provenance:
    id: didcomm-vta-rest-auth
    source: vti-didcomm-js
    command:
    - node
    - --test
    - --test-reporter=tap
    - test/vta-rest-auth.test.js
    purpose: Shipped JavaScript component vectors; no service-composition proof.
    timeout_seconds: 45
    class: runtime-observation
    started_at: '2026-10-08T04:32:59.059506+00:00'
    returncode: 0
    state: EXECUTED_PASS
    tests: 13
    passed: 13
    reason: Pinned component test vectors passed; no cross-service inference.
    duration_seconds: 0.311
    stdout:
      path: logs/didcomm-vta-rest-auth.stdout.txt
      sha256: 36504e79dc80da37daa8629deac5b9a6054af2101888780cca6e9dcf06f0a320
    stderr:
      path: logs/didcomm-vta-rest-auth.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: OpenVTC/vti-didcomm-js
    revision: afd11e1f5dab611118253d2ebaffd1cfee29962a
- class: runtime-observation
  result: EXECUTED_PASS
  provenance:
    id: didcomm-x25519
    source: vti-didcomm-js
    command:
    - node
    - --test
    - --test-reporter=tap
    - test/x25519.test.js
    purpose: Shipped JavaScript component vectors; no service-composition proof.
    timeout_seconds: 45
    class: runtime-observation
    started_at: '2026-10-08T04:32:59.371675+00:00'
    returncode: 0
    state: EXECUTED_PASS
    tests: 4
    passed: 4
    reason: Pinned component test vectors passed; no cross-service inference.
    duration_seconds: 0.245
    stdout:
      path: logs/didcomm-x25519.stdout.txt
      sha256: 1f051134899796c411393faa3f8addd7fcd27c8e4ff1d1351875e59702123782
    stderr:
      path: logs/didcomm-x25519.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: OpenVTC/vti-didcomm-js
    revision: afd11e1f5dab611118253d2ebaffd1cfee29962a
- class: runtime-observation
  result: EXECUTED_NONZERO
  provenance:
    id: vti-deploy-helper
    source: verifiable-trust-infrastructure
    command:
    - bash
    - deploy/nitro/deploy-common.test.sh
    purpose: Pinned deployment helper regression tests; no enclave certification.
    timeout_seconds: 45
    class: runtime-observation
    started_at: '2026-10-08T04:32:59.619729+00:00'
    returncode: 1
    state: EXECUTED_NONZERO
    reason: Nonzero execution requires diagnosis; neither automatic defect finding
      nor PASS.
    duration_seconds: 0.036
    stdout:
      path: logs/vti-deploy-helper.stdout.txt
      sha256: 84af7f123a48c1cc2035f0aa8b7ae17fa696545f95d6d5dec2af9eea2c36575b
    stderr:
      path: logs/vti-deploy-helper.stderr.txt
      sha256: 78c9942f3de21de1fa2e472f6ace7efe0e626c9bbc40df2e3d1a4d57dc14ee2a
    repository: OpenVTC/verifiable-trust-infrastructure
    revision: 49f5f1beb61adc34bdf7cf0bd3eb10f594415b80
- class: model/evidence-contract-definition
  result: ATTEMPTED_UNAVAILABLE
  provenance:
    id: rust-openvtc
    source: openvtc
    command:
    - cargo
    - test
    - --locked
    - --workspace
    purpose: Shipped Rust workspace tests; runtime prerequisites may be unavailable.
    timeout_seconds: 120
    class: runtime-observation
    started_at: '2026-10-08T04:32:59.656638+00:00'
    state: ATTEMPTED_UNAVAILABLE
    reason: 'executable unavailable: cargo'
    returncode: null
    duration_seconds: 0.0
    stdout:
      path: logs/rust-openvtc.stdout.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    stderr:
      path: logs/rust-openvtc.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: OpenVTC/openvtc
    revision: 2a4fa2b3c8e831dbe3184a1119c4c87b6f197220
- class: model/evidence-contract-definition
  result: ATTEMPTED_UNAVAILABLE
  provenance:
    id: rust-verifiable-trust-infrastructure
    source: verifiable-trust-infrastructure
    command:
    - cargo
    - test
    - --locked
    - --workspace
    purpose: Shipped Rust workspace tests; runtime prerequisites may be unavailable.
    timeout_seconds: 120
    class: runtime-observation
    started_at: '2026-10-08T04:32:59.657190+00:00'
    state: ATTEMPTED_UNAVAILABLE
    reason: 'executable unavailable: cargo'
    returncode: null
    duration_seconds: 0.0
    stdout:
      path: logs/rust-verifiable-trust-infrastructure.stdout.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    stderr:
      path: logs/rust-verifiable-trust-infrastructure.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: OpenVTC/verifiable-trust-infrastructure
    revision: 49f5f1beb61adc34bdf7cf0bd3eb10f594415b80
- class: model/evidence-contract-definition
  result: ATTEMPTED_UNAVAILABLE
  provenance:
    id: rust-affinidi-tdk-rs
    source: affinidi-tdk-rs
    command:
    - cargo
    - test
    - --locked
    - --workspace
    purpose: Shipped Rust workspace tests; runtime prerequisites may be unavailable.
    timeout_seconds: 120
    class: runtime-observation
    started_at: '2026-10-08T04:32:59.657642+00:00'
    state: ATTEMPTED_UNAVAILABLE
    reason: 'executable unavailable: cargo'
    returncode: null
    duration_seconds: 0.0
    stdout:
      path: logs/rust-affinidi-tdk-rs.stdout.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    stderr:
      path: logs/rust-affinidi-tdk-rs.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: affinidi/affinidi-tdk-rs
    revision: a1611baa011620a6ca62649b105c2b8c898f2653
- class: model/evidence-contract-definition
  result: ATTEMPTED_UNAVAILABLE
  provenance:
    id: rust-affinidi-webvh-service
    source: affinidi-webvh-service
    command:
    - cargo
    - test
    - --locked
    - --workspace
    purpose: Shipped Rust workspace tests; runtime prerequisites may be unavailable.
    timeout_seconds: 120
    class: runtime-observation
    started_at: '2026-10-08T04:32:59.658132+00:00'
    state: ATTEMPTED_UNAVAILABLE
    reason: 'executable unavailable: cargo'
    returncode: null
    duration_seconds: 0.0
    stdout:
      path: logs/rust-affinidi-webvh-service.stdout.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    stderr:
      path: logs/rust-affinidi-webvh-service.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: affinidi/affinidi-webvh-service
    revision: 1686668623e0bba0e18880074d82794cb929a7fc
- class: model/evidence-contract-definition
  result: ATTEMPTED_UNAVAILABLE
  provenance:
    id: rust-affinidi-trust-registry-rs
    source: affinidi-trust-registry-rs
    command:
    - cargo
    - test
    - --locked
    - --workspace
    purpose: Shipped Rust workspace tests; runtime prerequisites may be unavailable.
    timeout_seconds: 120
    class: runtime-observation
    started_at: '2026-10-08T04:32:59.658520+00:00'
    state: ATTEMPTED_UNAVAILABLE
    reason: 'executable unavailable: cargo'
    returncode: null
    duration_seconds: 0.0
    stdout:
      path: logs/rust-affinidi-trust-registry-rs.stdout.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    stderr:
      path: logs/rust-affinidi-trust-registry-rs.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: affinidi/affinidi-trust-registry-rs
    revision: c77052f9bffe8bb7b4a3f357d9ef54cf632950f0
- class: model/evidence-contract-definition
  result: ATTEMPTED_UNAVAILABLE
  provenance:
    id: rust-dtgwg-trust-tasks-tf
    source: dtgwg-trust-tasks-tf
    command:
    - cargo
    - test
    - --locked
    - --workspace
    purpose: Shipped Rust workspace tests; runtime prerequisites may be unavailable.
    timeout_seconds: 120
    class: runtime-observation
    started_at: '2026-10-08T04:32:59.659376+00:00'
    state: ATTEMPTED_UNAVAILABLE
    reason: 'executable unavailable: cargo'
    returncode: null
    duration_seconds: 0.0
    stdout:
      path: logs/rust-dtgwg-trust-tasks-tf.stdout.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    stderr:
      path: logs/rust-dtgwg-trust-tasks-tf.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: trustoverip/dtgwg-trust-tasks-tf
    revision: 7b6bb488ffd838bef058310c909207d4a7b77125
- class: model/evidence-contract-definition
  result: ATTEMPTED_UNAVAILABLE
  provenance:
    id: rust-verifiable-git-infrastructure
    source: verifiable-git-infrastructure
    command:
    - cargo
    - test
    - --locked
    - --workspace
    purpose: Shipped Rust workspace tests; runtime prerequisites may be unavailable.
    timeout_seconds: 120
    class: runtime-observation
    started_at: '2026-10-08T04:32:59.659911+00:00'
    state: ATTEMPTED_UNAVAILABLE
    reason: 'executable unavailable: cargo'
    returncode: null
    duration_seconds: 0.0
    stdout:
      path: logs/rust-verifiable-git-infrastructure.stdout.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    stderr:
      path: logs/rust-verifiable-git-infrastructure.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: OpenVTC/verifiable-git-infrastructure
    revision: 92f32dd4c107545bd42b009ca55fc1ed4759309d
- class: model/evidence-contract-definition
  result: ATTEMPTED_UNAVAILABLE
  provenance:
    id: rust-didwebvh-rs
    source: didwebvh-rs
    command:
    - cargo
    - test
    - --locked
    - --workspace
    purpose: Shipped Rust workspace tests; runtime prerequisites may be unavailable.
    timeout_seconds: 120
    class: runtime-observation
    started_at: '2026-10-08T04:32:59.660421+00:00'
    state: ATTEMPTED_UNAVAILABLE
    reason: 'executable unavailable: cargo'
    returncode: null
    duration_seconds: 0.0
    stdout:
      path: logs/rust-didwebvh-rs.stdout.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    stderr:
      path: logs/rust-didwebvh-rs.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: decentralized-identity/didwebvh-rs
    revision: 155eb4e71c9d45db57c6f7329f286bbd753e0138
- class: model/evidence-contract-definition
  result: ATTEMPTED_UNAVAILABLE
  provenance:
    id: rust-dtg-credentials
    source: dtg-credentials
    command:
    - cargo
    - test
    - --locked
    - --workspace
    purpose: Shipped Rust workspace tests; runtime prerequisites may be unavailable.
    timeout_seconds: 120
    class: runtime-observation
    started_at: '2026-10-08T04:32:59.660858+00:00'
    state: ATTEMPTED_UNAVAILABLE
    reason: 'executable unavailable: cargo'
    returncode: null
    duration_seconds: 0.0
    stdout:
      path: logs/rust-dtg-credentials.stdout.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    stderr:
      path: logs/rust-dtg-credentials.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: OpenVTC/dtg-credentials
    revision: fc9954d8d529d312ebac7ec1d413179857474c96
- class: model/evidence-contract-definition
  result: ATTEMPTED_UNAVAILABLE
  provenance:
    id: rust-predicate-credential-system
    source: predicate-credential-system
    command:
    - cargo
    - test
    - --locked
    - --workspace
    purpose: Shipped Rust workspace tests; runtime prerequisites may be unavailable.
    timeout_seconds: 120
    class: runtime-observation
    started_at: '2026-10-08T04:32:59.661263+00:00'
    state: ATTEMPTED_UNAVAILABLE
    reason: 'executable unavailable: cargo'
    returncode: null
    duration_seconds: 0.0
    stdout:
      path: logs/rust-predicate-credential-system.stdout.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    stderr:
      path: logs/rust-predicate-credential-system.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: OpenVTC/predicate-credential-system
    revision: 4be4598563f422b9a3a4e37032d22487836d322c
- class: model/evidence-contract-definition
  result: ATTEMPTED_UNAVAILABLE
  provenance:
    id: rust-vta-agent-memory
    source: vta-agent-memory
    command:
    - cargo
    - test
    - --locked
    - --workspace
    purpose: Shipped Rust workspace tests; runtime prerequisites may be unavailable.
    timeout_seconds: 120
    class: runtime-observation
    started_at: '2026-10-08T04:32:59.661657+00:00'
    state: ATTEMPTED_UNAVAILABLE
    reason: 'executable unavailable: cargo'
    returncode: null
    duration_seconds: 0.0
    stdout:
      path: logs/rust-vta-agent-memory.stdout.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    stderr:
      path: logs/rust-vta-agent-memory.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: OpenVTC/vta-agent-memory
    revision: 85db98a8a9c6d25b673a38a9e7e60d3435f3fcc5
- class: model/evidence-contract-definition
  result: ATTEMPTED_UNAVAILABLE
  provenance:
    id: rust-vti-push-gateway
    source: vti-push-gateway
    command:
    - cargo
    - test
    - --locked
    - --workspace
    purpose: Shipped Rust workspace tests; runtime prerequisites may be unavailable.
    timeout_seconds: 120
    class: runtime-observation
    started_at: '2026-10-08T04:32:59.662088+00:00'
    state: ATTEMPTED_UNAVAILABLE
    reason: 'executable unavailable: cargo'
    returncode: null
    duration_seconds: 0.0
    stdout:
      path: logs/rust-vti-push-gateway.stdout.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    stderr:
      path: logs/rust-vti-push-gateway.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: OpenVTC/vti-push-gateway
    revision: 44342121e161ccb12e43013f33ce80abb2486acb
- class: model/evidence-contract-definition
  result: ATTEMPTED_UNAVAILABLE
  provenance:
    id: go-tsp
    source: affinidi-tsp-go
    command:
    - go
    - test
    - ./...
    purpose: Independent Go TSP implementation vectors.
    timeout_seconds: 120
    class: runtime-observation
    started_at: '2026-10-08T04:32:59.662529+00:00'
    state: ATTEMPTED_UNAVAILABLE
    reason: 'executable unavailable: go'
    returncode: null
    duration_seconds: 0.0
    stdout:
      path: logs/go-tsp.stdout.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    stderr:
      path: logs/go-tsp.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: affinidi/affinidi-tsp-go
    revision: d32ca7cdde208e93509c1f140ad7ee04d52ca7cc
- class: model/evidence-contract-definition
  result: ATTEMPTED_UNAVAILABLE
  provenance:
    id: dart-tsp
    source: affinidi-tsp-dart
    command:
    - dart
    - test
    - packages/affinidi_tsp/test
    purpose: Dart vectors; package runtime setup is separately required.
    timeout_seconds: 90
    class: runtime-observation
    started_at: '2026-10-08T04:32:59.663100+00:00'
    state: ATTEMPTED_UNAVAILABLE
    reason: 'executable unavailable: dart'
    returncode: null
    duration_seconds: 0.0
    stdout:
      path: logs/dart-tsp.stdout.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    stderr:
      path: logs/dart-tsp.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: affinidi/affinidi-tsp-dart
    revision: a64814c8043d6af0955a3ce01bfc6033d8daeb78
- class: model/evidence-contract-definition
  result: ATTEMPTED_UNAVAILABLE
  provenance:
    id: ios-approval
    source: vta-mobile-agent-ios
    command:
    - swift
    - test
    purpose: Swift owner approval component tests; Apple platform prerequisites apply.
    timeout_seconds: 90
    class: runtime-observation
    started_at: '2026-10-08T04:32:59.664023+00:00'
    state: ATTEMPTED_UNAVAILABLE
    reason: 'executable unavailable: swift'
    returncode: null
    duration_seconds: 0.0
    stdout:
      path: logs/ios-approval.stdout.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    stderr:
      path: logs/ios-approval.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: OpenVTC/vta-mobile-agent-ios
    revision: 863a1e912042b28908ec2cf3675677ad9c151e0e
- class: runtime-observation
  result: EXECUTED_NONZERO
  provenance:
    id: npm-rp-sdk-js
    source: rp-sdk-js
    command:
    - npm
    - test
    purpose: Declared package tests; missing dependencies remain explicit.
    timeout_seconds: 60
    class: runtime-observation
    started_at: '2026-10-08T04:32:59.664595+00:00'
    returncode: 1
    state: EXECUTED_NONZERO
    reason: Nonzero execution requires diagnosis; neither automatic defect finding
      nor PASS.
    duration_seconds: 1.23
    stdout:
      path: logs/npm-rp-sdk-js.stdout.txt
      sha256: 196b69aaadef8f174e1341ffc9139ba1763be2348c47f9b9a724270f6f58fbe5
    stderr:
      path: logs/npm-rp-sdk-js.stderr.txt
      sha256: 87807c3f435058bbcf7ad3fcaded5adf2b7b50fca51f0c3d54f7708ed1e86305
    repository: OpenVTC/rp-sdk-js
    revision: 8594c2acba4014232e842fe7613e8a7cdc0e2b0f
- class: runtime-observation
  result: EXECUTED_PASS
  provenance:
    id: npm-vta-browser-plugin
    source: vta-browser-plugin
    command:
    - npm
    - test
    purpose: Declared package tests; missing dependencies remain explicit.
    timeout_seconds: 60
    class: runtime-observation
    started_at: '2026-10-08T04:33:00.896249+00:00'
    returncode: 0
    state: EXECUTED_PASS
    reason: Pinned command completed; assurance limited to its declared purpose.
    duration_seconds: 37.814
    stdout:
      path: logs/npm-vta-browser-plugin.stdout.txt
      sha256: 467cac78a47aca7bf1d6f07cbdca2846cfe9e8238c1649a23019a60beaaaef2b
    stderr:
      path: logs/npm-vta-browser-plugin.stderr.txt
      sha256: d829d0b399a760edea60c001d051836938a28d8fb33b019376efae7483db3eda
    repository: OpenVTC/vta-browser-plugin
    revision: d6df67971688fd927cd5b095424fa4093d4264df
- class: static-specification-analysis
  result: EXECUTED_PASS
  provenance:
    id: tt-check-bindings-conformance
    source: dtgwg-trust-tasks-tf
    command:
    - node
    - scripts/check-bindings-conformance.mjs
    purpose: Shipped static registry/bindings/ceremony validation, not deployed runtime.
    timeout_seconds: 90
    evidence_class: static-specification-analysis
    class: static-specification-analysis
    started_at: '2026-10-08T04:33:38.712110+00:00'
    returncode: 0
    state: EXECUTED_PASS
    reason: Pinned command completed; assurance limited to its declared purpose.
    duration_seconds: 3.346
    stdout:
      path: logs/tt-check-bindings-conformance.stdout.txt
      sha256: 64197e12a1e9ad709bf5a17bd28c3cae5c58727c7fe1cd2783de47978f921a7d
    stderr:
      path: logs/tt-check-bindings-conformance.stderr.txt
      sha256: 6f9b5bdc5480854ee0c147d4a5d8539442cf307c7408b39c9f5b40131229ae3f
    repository: trustoverip/dtgwg-trust-tasks-tf
    revision: 7b6bb488ffd838bef058310c909207d4a7b77125
- class: static-specification-analysis
  result: EXECUTED_PASS
  provenance:
    id: tt-validate-ceremonies
    source: dtgwg-trust-tasks-tf
    command:
    - node
    - scripts/validate-ceremonies.mjs
    purpose: Shipped static registry/bindings/ceremony validation, not deployed runtime.
    timeout_seconds: 90
    evidence_class: static-specification-analysis
    class: static-specification-analysis
    started_at: '2026-10-08T04:33:42.058519+00:00'
    returncode: 0
    state: EXECUTED_PASS
    reason: Pinned command completed; assurance limited to its declared purpose.
    duration_seconds: 0.213
    stdout:
      path: logs/tt-validate-ceremonies.stdout.txt
      sha256: 5c77f74fe8d216bc6dcfc21eb786329d186c6fc3d323e28994b32a8f58b01b60
    stderr:
      path: logs/tt-validate-ceremonies.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: trustoverip/dtgwg-trust-tasks-tf
    revision: 7b6bb488ffd838bef058310c909207d4a7b77125
- class: static-specification-analysis
  result: EXECUTED_PASS
  provenance:
    id: tt-check-dart-packages
    source: dtgwg-trust-tasks-tf
    command:
    - node
    - scripts/check-dart-packages.mjs
    purpose: Shipped static registry/bindings/ceremony validation, not deployed runtime.
    timeout_seconds: 90
    evidence_class: static-specification-analysis
    class: static-specification-analysis
    started_at: '2026-10-08T04:33:42.271530+00:00'
    returncode: 0
    state: EXECUTED_PASS
    reason: Pinned command completed; assurance limited to its declared purpose.
    duration_seconds: 0.165
    stdout:
      path: logs/tt-check-dart-packages.stdout.txt
      sha256: 3b11d88def951e27f77a0cc17a50f04ce3684063785f23de77f35ab4af4ed4b3
    stderr:
      path: logs/tt-check-dart-packages.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: trustoverip/dtgwg-trust-tasks-tf
    revision: 7b6bb488ffd838bef058310c909207d4a7b77125
- class: runtime-observation
  result: EXECUTED_PASS
  provenance:
    id: browser-demo-cors
    source: vta-browser-plugin
    command:
    - node
    - --test
    - --test-reporter=tap
    - packages/demo-rp/tests/cors.test.mjs
    purpose: Shipped demo security vectors; no whole-browser assurance.
    timeout_seconds: 45
    class: runtime-observation
    started_at: '2026-10-08T04:33:42.437003+00:00'
    returncode: 0
    state: EXECUTED_PASS
    tests: 6
    passed: 6
    reason: Pinned component test vectors passed; no cross-service inference.
    duration_seconds: 0.346
    stdout:
      path: logs/browser-demo-cors.stdout.txt
      sha256: 15164b1b04f661e51f6d0490dc15de85fb849510a7e1051f05768487b54e5de4
    stderr:
      path: logs/browser-demo-cors.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: OpenVTC/vta-browser-plugin
    revision: d6df67971688fd927cd5b095424fa4093d4264df
- class: runtime-observation
  result: EXECUTED_PASS
  provenance:
    id: browser-demo-grant-parser
    source: vta-browser-plugin
    command:
    - node
    - --test
    - --test-reporter=tap
    - packages/reviewer-demo/tests/parse-grant-command.test.mjs
    purpose: Shipped demo security vectors; no whole-browser assurance.
    timeout_seconds: 45
    class: runtime-observation
    started_at: '2026-10-08T04:33:42.783307+00:00'
    returncode: 0
    state: EXECUTED_PASS
    tests: 9
    passed: 9
    reason: Pinned component test vectors passed; no cross-service inference.
    duration_seconds: 0.232
    stdout:
      path: logs/browser-demo-grant-parser.stdout.txt
      sha256: 23b321475caeb3de755113232c387153e98e5f2b52e0a91dc9f51d2fecbf6d02
    stderr:
      path: logs/browser-demo-grant-parser.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: OpenVTC/vta-browser-plugin
    revision: d6df67971688fd927cd5b095424fa4093d4264df
- class: model/evidence-contract-definition
  result: ATTEMPTED_UNAVAILABLE
  provenance:
    id: lab-room-handoff
    source: trust-protocol-interop-lab
    command:
    - python3
    - experiments/dtg-data-room-runtime/run_current_openvtc.py
    - --target
    - ../verifiable-trust-infrastructure
    - --output
    - ../../output/lab-room.json
    purpose: Actual producer admission against the Eucalyptus pin; older hardcoded
      target must fail closed.
    timeout_seconds: 30
    class: runtime-observation
    started_at: '2026-10-08T04:33:43.016129+00:00'
    returncode: 1
    state: ATTEMPTED_UNAVAILABLE
    reason: dependency or network prerequisite unavailable; see full logs
    duration_seconds: 0.051
    stdout:
      path: logs/lab-room-handoff.stdout.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    stderr:
      path: logs/lab-room-handoff.stderr.txt
      sha256: 43f1bce60547ae1d3a1bae6289e2855d8134b3d4c6b881e1d5d07ca47c46f62b
    repository: sankarshanmukhopadhyay/trust-protocol-interop-lab
    revision: 895e1af0f441995cada90dad2a429e56885bd394
- class: model/evidence-contract-definition
  result: ATTEMPTED_UNAVAILABLE
  provenance:
    id: lab-privacy-handoff
    source: trust-protocol-interop-lab
    command:
    - python3
    - experiments/dtg-protected-access/current_openvtc_context.py
    - --checkout
    - ../verifiable-trust-infrastructure
    - --context
    - A
    - --verifier
    - https://verifier.example.invalid
    - --purpose
    - eucalyptus-cleanroom
    - --challenge
    - eucalyptus-960
    - --client-seed
    - '1'
    purpose: Actual source-compatible privacy probe attempt; incompatible source pins
      cannot become new runtime evidence.
    timeout_seconds: 30
    class: runtime-observation
    started_at: '2026-10-08T04:33:43.067059+00:00'
    returncode: 2
    state: ATTEMPTED_UNAVAILABLE
    reason: dependency or network prerequisite unavailable; see full logs
    duration_seconds: 0.047
    stdout:
      path: logs/lab-privacy-handoff.stdout.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    stderr:
      path: logs/lab-privacy-handoff.stderr.txt
      sha256: 732dbf45a20aba302215b40fd30e31e142793d51f75e181d44abd85b4eaa39e0
    repository: sankarshanmukhopadhyay/trust-protocol-interop-lab
    revision: 895e1af0f441995cada90dad2a429e56885bd394
- class: model/evidence-contract-definition
  result: EXECUTED_PASS
  provenance:
    id: dpip-incomplete-return
    source: dtg-privacy-implementation-profile
    command:
    - python3
    - scripts/evaluate_privacy_observability.py
    - ../../output/privacy-observability-input.json
    - --output
    - ../../output/dpip-specialist.json
    purpose: DPIP portable return for explicitly unavailable A/B observations; not
      a runtime privacy experiment.
    evidence_class: model/evidence-contract-definition
    timeout_seconds: 30
    class: model/evidence-contract-definition
    started_at: '2026-10-08T04:33:43.113980+00:00'
    returncode: 0
    state: EXECUTED_PASS
    reason: Pinned command completed; assurance limited to its declared purpose.
    duration_seconds: 0.121
    stdout:
      path: logs/dpip-incomplete-return.stdout.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    stderr:
      path: logs/dpip-incomplete-return.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: sankarshanmukhopadhyay/dtg-privacy-implementation-profile
    revision: 991c92bad6ccb61dbc2511162bf11a9eb59679e2
- class: runtime-observation
  result: EXECUTED_PASS
  provenance:
    id: rp-jcs-direct-boundary
    source: rp-sdk-js
    command:
    - node
    - --experimental-transform-types
    - --input-type=module
    - -e
    - 'import assert from "node:assert/strict"; import {jcsCanonicalize,JcsLimitExceededError,JCS_MAX_DEPTH}
      from "./src/jcs.ts"; let deep=0; for(let i=0;i<5000;i++) deep=[deep]; assert.throws(()=>jcsCanonicalize(deep),e=>e
      instanceof JcsLimitExceededError && e.limit==="depth"); let bounded=0; for(let
      i=0;i<JCS_MAX_DEPTH;i++) bounded=[bounded]; assert.doesNotThrow(()=>jcsCanonicalize(bounded));
      assert.throws(()=>jcsCanonicalize([bounded]),JcsLimitExceededError); console.log("PASS
      actual JCS depth-bound vectors: 5000 levels, exact boundary, boundary+1");'
    purpose: Direct execution of tagged canonicalizer at 5000 levels, maximum permitted
      depth and depth+1; avoids the failing JSON.stringify precondition without changing
      target tests.
    timeout_seconds: 30
    class: runtime-observation
    started_at: '2026-10-08T04:33:43.235649+00:00'
    returncode: 0
    state: EXECUTED_PASS
    reason: Pinned command completed; assurance limited to its declared purpose.
    duration_seconds: 0.143
    stdout:
      path: logs/rp-jcs-direct-boundary.stdout.txt
      sha256: bec47b67d0f21cc1e687b7d0beb64fb0cc84e7ef5bfbddbcbe1c3474b626f1cd
    stderr:
      path: logs/rp-jcs-direct-boundary.stderr.txt
      sha256: 769f0c1b188c5dcd3a206ebd2af6bb6289e6d6c7a7b6e05acd58501898bcf538
    repository: OpenVTC/rp-sdk-js
    revision: 8594c2acba4014232e842fe7613e8a7cdc0e2b0f
- class: runtime-observation
  result: EXECUTED_PASS
  provenance:
    id: local-dns-diagnostic
    source: vti-didcomm-js
    command:
    - node
    - --input-type=module
    - -e
    - import {lookup} from "node:dns/promises"; for(const host of ["localhost","localhost.","mediator.localhost","mediator.localhost.","127.0.0.1."]){try
      { console.log(host,JSON.stringify(await lookup(host)));}catch(e){console.log(host,e.code)}}
    purpose: Environment-only diagnostic for the failing SSRF positive control; never
      proof that the guard holds.
    timeout_seconds: 30
    class: runtime-observation
    started_at: '2026-10-08T04:33:43.378759+00:00'
    returncode: 0
    state: EXECUTED_PASS
    reason: Pinned command completed; assurance limited to its declared purpose.
    duration_seconds: 0.078
    stdout:
      path: logs/local-dns-diagnostic.stdout.txt
      sha256: 80407d1d4b9f1271b2a21f202aa6dc903328d8fe8f27f212f5579b2218c0f5a5
    stderr:
      path: logs/local-dns-diagnostic.stderr.txt
      sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    repository: OpenVTC/vti-didcomm-js
    revision: afd11e1f5dab611118253d2ebaffd1cfee29962a
- class: model/evidence-contract-definition
  result: INDETERMINATE
  provenance:
    source_pins:
    - repository: sankarshanmukhopadhyay/trust-protocol-interop-lab
      revision: 895e1af0f441995cada90dad2a429e56885bd394
      tag_object: 895e1af0f441995cada90dad2a429e56885bd394
      release: HEAD
      path: sources/trust-protocol-interop-lab
      role: evidence-producer/specialist snapshot; outside coordinated release
    - repository: sankarshanmukhopadhyay/dtg-privacy-implementation-profile
      revision: 991c92bad6ccb61dbc2511162bf11a9eb59679e2
      tag_object: 991c92bad6ccb61dbc2511162bf11a9eb59679e2
      release: HEAD
      path: sources/dtg-privacy-implementation-profile
      role: evidence-producer/specialist snapshot; outside coordinated release
    artifact: dpip-specialist.json
    sha256: 7c24ce9385e0bddad5fa7744b1494bdf211bffe44b518d810e8939690e33a5b9
    scope: Explicitly missing privacy observations; no native experiment executed.
tests:
- dependencies-dtgwg-trust-tasks-tf
- dependencies-vta-browser-plugin
- dependencies-rp-sdk-js
- dependencies-vti-didcomm-js
- didcomm-a256cbc-hs512
- didcomm-aes
- didcomm-anoncrypt
- didcomm-base64url
- didcomm-concat-kdf
- didcomm-did-key
- didcomm-did-peer
- didcomm-did-webvh-ssrf
- didcomm-did-webvh
- didcomm-dns-rebinding
- didcomm-ecdh-1pu
- didcomm-ecdh-es
- didcomm-ecdh-p256
- didcomm-forward
- didcomm-jwk
- didcomm-key-agreement
- didcomm-mediator-auth-ssrf
- didcomm-mediator-auth
- didcomm-mediator-transport
- didcomm-migration-fallback
- didcomm-multibase
- didcomm-net-guard-node
- didcomm-net-guard
- didcomm-p256
- didcomm-pack-unpack-p256
- didcomm-pack-unpack
- didcomm-resolver
- didcomm-roundtrip-rust
- didcomm-sender-binding
- didcomm-tsp-frame
- didcomm-vta-didcomm
- didcomm-vta-rest-auth
- didcomm-x25519
- vti-deploy-helper
- rust-openvtc
- rust-verifiable-trust-infrastructure
- rust-affinidi-tdk-rs
- rust-affinidi-webvh-service
- rust-affinidi-trust-registry-rs
- rust-dtgwg-trust-tasks-tf
- rust-verifiable-git-infrastructure
- rust-didwebvh-rs
- rust-dtg-credentials
- rust-predicate-credential-system
- rust-vta-agent-memory
- rust-vti-push-gateway
- go-tsp
- dart-tsp
- ios-approval
- npm-rp-sdk-js
- npm-vta-browser-plugin
- tt-check-bindings-conformance
- tt-validate-ceremonies
- tt-check-dart-packages
- browser-demo-cors
- browser-demo-grant-parser
- lab-room-handoff
- lab-privacy-handoff
- dpip-incomplete-return
- rp-jcs-direct-boundary
- local-dns-diagnostic
inference: 20 consequential propositions lack accepted deployed-composition/specialist
  evidence. Component results and configuration exceptions are bounded observations,
  not certification.
confidence: bounded by named evidence and assessor result
boundedness: Conclusion applies only to the configured subject, immutable pins and
  evidence classes represented in this run.
state: TERMINAL_INDETERMINATE_EVIDENCE_REQUIRED
terminal: true
outcome: INDETERMINATE
reason_code: eucalyptus-composition-evidence-required
residuals:
- id: EUC-01
  summary: Source inspection and bounded component checks do not establish this consequential
    composition. Attributable positive, negative and adversarial traces from the pinned
    consuming composition, including configuration, policy, clock, participants, expected/observed
    outcomes and effects; specialist return where privacy or human independence is
    asserted.
- id: EUC-02
  summary: Source inspection and bounded component checks do not establish this consequential
    composition. Attributable positive, negative and adversarial traces from the pinned
    consuming composition, including configuration, policy, clock, participants, expected/observed
    outcomes and effects; specialist return where privacy or human independence is
    asserted.
- id: EUC-03
  summary: Source inspection and bounded component checks do not establish this consequential
    composition. Attributable positive, negative and adversarial traces from the pinned
    consuming composition, including configuration, policy, clock, participants, expected/observed
    outcomes and effects; specialist return where privacy or human independence is
    asserted.
- id: EUC-04
  summary: Source inspection and bounded component checks do not establish this consequential
    composition. Attributable positive, negative and adversarial traces from the pinned
    consuming composition, including configuration, policy, clock, participants, expected/observed
    outcomes and effects; specialist return where privacy or human independence is
    asserted.
- id: EUC-05
  summary: Source inspection and bounded component checks do not establish this consequential
    composition. Attributable positive, negative and adversarial traces from the pinned
    consuming composition, including configuration, policy, clock, participants, expected/observed
    outcomes and effects; specialist return where privacy or human independence is
    asserted.
- id: EUC-06
  summary: Source inspection and bounded component checks do not establish this consequential
    composition. Attributable positive, negative and adversarial traces from the pinned
    consuming composition, including configuration, policy, clock, participants, expected/observed
    outcomes and effects; specialist return where privacy or human independence is
    asserted.
- id: EUC-07
  summary: Source inspection and bounded component checks do not establish this consequential
    composition. Attributable positive, negative and adversarial traces from the pinned
    consuming composition, including configuration, policy, clock, participants, expected/observed
    outcomes and effects; specialist return where privacy or human independence is
    asserted.
- id: EUC-08
  summary: Source inspection and bounded component checks do not establish this consequential
    composition. Attributable positive, negative and adversarial traces from the pinned
    consuming composition, including configuration, policy, clock, participants, expected/observed
    outcomes and effects; specialist return where privacy or human independence is
    asserted.
- id: EUC-09
  summary: Source inspection and bounded component checks do not establish this consequential
    composition. Attributable positive, negative and adversarial traces from the pinned
    consuming composition, including configuration, policy, clock, participants, expected/observed
    outcomes and effects; specialist return where privacy or human independence is
    asserted.
- id: EUC-10
  summary: Source inspection and bounded component checks do not establish this consequential
    composition. Attributable positive, negative and adversarial traces from the pinned
    consuming composition, including configuration, policy, clock, participants, expected/observed
    outcomes and effects; specialist return where privacy or human independence is
    asserted.
- id: EUC-11
  summary: Source inspection and bounded component checks do not establish this consequential
    composition. Attributable positive, negative and adversarial traces from the pinned
    consuming composition, including configuration, policy, clock, participants, expected/observed
    outcomes and effects; specialist return where privacy or human independence is
    asserted.
- id: EUC-12
  summary: Source inspection and bounded component checks do not establish this consequential
    composition. Attributable positive, negative and adversarial traces from the pinned
    consuming composition, including configuration, policy, clock, participants, expected/observed
    outcomes and effects; specialist return where privacy or human independence is
    asserted.
- id: EUC-13
  summary: Source inspection and bounded component checks do not establish this consequential
    composition. Attributable positive, negative and adversarial traces from the pinned
    consuming composition, including configuration, policy, clock, participants, expected/observed
    outcomes and effects; specialist return where privacy or human independence is
    asserted.
- id: EUC-14
  summary: Source inspection and bounded component checks do not establish this consequential
    composition. Attributable positive, negative and adversarial traces from the pinned
    consuming composition, including configuration, policy, clock, participants, expected/observed
    outcomes and effects; specialist return where privacy or human independence is
    asserted.
- id: EUC-15
  summary: Source inspection and bounded component checks do not establish this consequential
    composition. Attributable positive, negative and adversarial traces from the pinned
    consuming composition, including configuration, policy, clock, participants, expected/observed
    outcomes and effects; specialist return where privacy or human independence is
    asserted.
- id: EUC-16
  summary: Source inspection and bounded component checks do not establish this consequential
    composition. Attributable positive, negative and adversarial traces from the pinned
    consuming composition, including configuration, policy, clock, participants, expected/observed
    outcomes and effects; specialist return where privacy or human independence is
    asserted.
- id: EUC-17
  summary: Source inspection and bounded component checks do not establish this consequential
    composition. Attributable positive, negative and adversarial traces from the pinned
    consuming composition, including configuration, policy, clock, participants, expected/observed
    outcomes and effects; specialist return where privacy or human independence is
    asserted.
- id: EUC-18
  summary: Source inspection and bounded component checks do not establish this consequential
    composition. Attributable positive, negative and adversarial traces from the pinned
    consuming composition, including configuration, policy, clock, participants, expected/observed
    outcomes and effects; specialist return where privacy or human independence is
    asserted.
- id: EUC-19
  summary: Source inspection and bounded component checks do not establish this consequential
    composition. Attributable positive, negative and adversarial traces from the pinned
    consuming composition, including configuration, policy, clock, participants, expected/observed
    outcomes and effects; specialist return where privacy or human independence is
    asserted.
- id: EUC-20
  summary: Source inspection and bounded component checks do not establish this consequential
    composition. Attributable positive, negative and adversarial traces from the pinned
    consuming composition, including configuration, policy, clock, participants, expected/observed
    outcomes and effects; specialist return where privacy or human independence is
    asserted.
actions:
- surface: evidence-test
  action: 'VTI / Trust Tasks: Execute signed/unsigned, wrong-sender and nested-transport
    requests through VTA, VTC, mediator and push doors; verify zero forbidden effects.'
  acceptance_criterion: Attributable positive, negative and adversarial traces from
    the pinned consuming composition, including configuration, policy, clock, participants,
    expected/observed outcomes and effects; specialist return where privacy or human
    independence is asserted.
- surface: evidence-test
  action: 'DTG Credentials / VTI: Exercise both substitution directions and revoke
    authority between verification and commit.'
  acceptance_criterion: Attributable positive, negative and adversarial traces from
    the pinned consuming composition, including configuration, policy, clock, participants,
    expected/observed outcomes and effects; specialist return where privacy or human
    independence is asserted.
- surface: evidence-test
  action: 'VTI / deployment operator: Execute label-only, widening, narrowing, sole-admin
    and multiple-person configurations across HTTPS/DIDComm/TSP; assert audit-before-effect.'
  acceptance_criterion: Attributable positive, negative and adversarial traces from
    the pinned consuming composition, including configuration, policy, clock, participants,
    expected/observed outcomes and effects; specialist return where privacy or human
    independence is asserted.
- surface: evidence-test
  action: 'VTI / community governance: Exercise repeated approver, requester approval,
    stale approval, role reduction, threshold change, cancellation, cooling-off and
    real single-person/multi-person policy.'
  acceptance_criterion: Attributable positive, negative and adversarial traces from
    the pinned consuming composition, including configuration, policy, clock, participants,
    expected/observed outcomes and effects; specialist return where privacy or human
    independence is asserted.
- surface: evidence-test
  action: 'VTI / mediator: Capture and replay identical task, changed payload under
    same ID, expired consent and post-restart retries; inspect effects and durable
    state.'
  acceptance_criterion: Attributable positive, negative and adversarial traces from
    the pinned consuming composition, including configuration, policy, clock, participants,
    expected/observed outcomes and effects; specialist return where privacy or human
    independence is asserted.
- surface: evidence-test
  action: 'TDK / Go / Dart / browser: Execute independent byte vectors and old/new
    endpoint pairs, nested mediator sends, restart and forged relationship transitions.'
  acceptance_criterion: Attributable positive, negative and adversarial traces from
    the pinned consuming composition, including configuration, policy, clock, participants,
    expected/observed outcomes and effects; specialist return where privacy or human
    independence is asserted.
- surface: evidence-test
  action: 'VTI Rooms / deployment operator: Run host, native and browser participants;
    remove member, rekey, rotate custodian, replay old epoch and corrupt Merkle record.'
  acceptance_criterion: Attributable positive, negative and adversarial traces from
    the pinned consuming composition, including configuration, policy, clock, participants,
    expected/observed outcomes and effects; specialist return where privacy or human
    independence is asserted.
- surface: evidence-test
  action: 'PCS / DPIP specialist / VTI: Execute duplicate-vetter, wrong-context, withdrawn-vetter,
    nonce replay and public/hidden A-B journeys with observable transcripts.'
  acceptance_criterion: Attributable positive, negative and adversarial traces from
    the pinned consuming composition, including configuration, policy, clock, participants,
    expected/observed outcomes and effects; specialist return where privacy or human
    independence is asserted.
- surface: evidence-test
  action: 'DPIP specialist / OpenVTC / VTA: Compare two contexts through issuance,
    presentation, status discovery, task retention and retirement; measure stable
    joins and required disclosures.'
  acceptance_criterion: Attributable positive, negative and adversarial traces from
    the pinned consuming composition, including configuration, policy, clock, participants,
    expected/observed outcomes and effects; specialist return where privacy or human
    independence is asserted.
- surface: evidence-test
  action: 'VGI / VTC / forge operator: Run GitHub and Forgejo adapters against sandbox
    forges; bypass PR gate, revoke member after approval, replay webhook, exercise
    break-glass and inspect signer attribution.'
  acceptance_criterion: Attributable positive, negative and adversarial traces from
    the pinned consuming composition, including configuration, policy, clock, participants,
    expected/observed outcomes and effects; specialist return where privacy or human
    independence is asserted.
- surface: evidence-test
  action: 'TDK / mediator operator: Run unauthorized and authorized inspect/purge/patch/reload
    tasks; verify sender proof, ACL, restart and audit on every transport.'
  acceptance_criterion: Attributable positive, negative and adversarial traces from
    the pinned consuming composition, including configuration, policy, clock, participants,
    expected/observed outcomes and effects; specialist return where privacy or human
    independence is asserted.
- surface: evidence-test
  action: 'TDK / DID hosting / browser: Execute private/IP-encoding/redirect/rebinding
    vectors through real resolver, mediator client and DID hosting rather than the
    URL predicate alone.'
  acceptance_criterion: Attributable positive, negative and adversarial traces from
    the pinned consuming composition, including configuration, policy, clock, participants,
    expected/observed outcomes and effects; specialist return where privacy or human
    independence is asserted.
- surface: evidence-test
  action: 'VTA / VTC / governance operator: Tamper, truncate, roll back and rotate
    keys; independently verify chains and reconstruct a contested action after agent
    replacement.'
  acceptance_criterion: Attributable positive, negative and adversarial traces from
    the pinned consuming composition, including configuration, policy, clock, participants,
    expected/observed outcomes and effects; specialist return where privacy or human
    independence is asserted.
- surface: evidence-test
  action: 'VTI / TSP PQ: Exercise mixed algorithms, absent hybrid member, wrong key
    type, malformed signature and downgraded peer; pin actual crypto packages.'
  acceptance_criterion: Attributable positive, negative and adversarial traces from
    the pinned consuming composition, including configuration, policy, clock, participants,
    expected/observed outcomes and effects; specialist return where privacy or human
    independence is asserted.
- surface: evidence-test
  action: 'Trust registry / relying-party operator: Run unauthorized write, replay,
    key rotation, stale status and cross-context recognition; verify policy version,
    effective time and audit.'
  acceptance_criterion: Attributable positive, negative and adversarial traces from
    the pinned consuming composition, including configuration, policy, clock, participants,
    expected/observed outcomes and effects; specialist return where privacy or human
    independence is asserted.
- surface: evidence-test
  action: 'Mobile / push / VTA: Exercise unsolicited pairing, forged push, altered
    display/action digest, decline, expiry and revoked device through physical approval
    journey.'
  acceptance_criterion: Attributable positive, negative and adversarial traces from
    the pinned consuming composition, including configuration, policy, clock, participants,
    expected/observed outcomes and effects; specialist return where privacy or human
    independence is asserted.
- surface: evidence-test
  action: 'Agent memory / VTA operator: Feed delimiter escape, command injection,
    excessive record and cross-owner recall through actual MCP consumer; observe decisions
    and stored bytes.'
  acceptance_criterion: Attributable positive, negative and adversarial traces from
    the pinned consuming composition, including configuration, policy, clock, participants,
    expected/observed outcomes and effects; specialist return where privacy or human
    independence is asserted.
- surface: evidence-test
  action: 'RP SDK / browser operator: Run wrong recipient, stale token, reused challenge,
    deeply nested payload and modified signed token through actual relying service.'
  acceptance_criterion: Attributable positive, negative and adversarial traces from
    the pinned consuming composition, including configuration, policy, clock, participants,
    expected/observed outcomes and effects; specialist return where privacy or human
    independence is asserted.
- surface: evidence-test
  action: 'All component maintainers / RAHP: Build locked consumers; compare resolved
    package identities to coordinated sources and execute old/new request-schema and
    lifecycle pairs.'
  acceptance_criterion: Attributable positive, negative and adversarial traces from
    the pinned consuming composition, including configuration, policy, clock, participants,
    expected/observed outcomes and effects; specialist return where privacy or human
    independence is asserted.
- surface: evidence-test
  action: 'Community governance / client maintainers: Run assistive-technology and
    unavailable-device journeys; document supported alternatives and verify a challenged
    decision can be corrected without bypassing authority.'
  acceptance_criterion: Attributable positive, negative and adversarial traces from
    the pinned consuming composition, including configuration, policy, clock, participants,
    expected/observed outcomes and effects; specialist return where privacy or human
    independence is asserted.
harm_traceability:
- persona: requester
  scenario: Forged or sender-mismatched task enters an authenticated transport
  harm: unauthorized actuation
  proposition: Task proofs are bound to the actual sender across all consuming doors
  control: document proof plus transport-sender binding
  conclusion: INDETERMINATE
  evidence: EUC-01, EUC-02, EUC-03, EUC-04, EUC-05, EUC-06, EUC-07, EUC-08, EUC-09,
    EUC-10, EUC-11, EUC-12, EUC-13, EUC-14, EUC-15, EUC-16, EUC-17, EUC-18, EUC-19,
    EUC-20
- persona: principal
  scenario: Valid VAC/VDC with expired or absent mandate reaches consequential execution
  harm: unauthorized delegated action
  proposition: Credential validity, delegation and authority remain non-substitutable
  control: joint authority/delegation/current-state checks
  conclusion: INDETERMINATE
  evidence: EUC-01, EUC-02, EUC-03, EUC-04, EUC-05, EUC-06, EUC-07, EUC-08, EUC-09,
    EUC-10, EUC-11, EUC-12, EUC-13, EUC-14, EUC-15, EUC-16, EUC-17, EUC-18, EUC-19,
    EUC-20
- persona: community administrator
  scenario: One principal attempts widening its own ACL entry
  harm: self-escalation
  proposition: Self-edit restrictions and exception boundaries are enforced at each
    transport
  control: ceiling-bound ACL updates and explicit exceptions
  conclusion: INDETERMINATE
  evidence: EUC-01, EUC-02, EUC-03, EUC-04, EUC-05, EUC-06, EUC-07, EUC-08, EUC-09,
    EUC-10, EUC-11, EUC-12, EUC-13, EUC-14, EUC-15, EUC-16, EUC-17, EUC-18, EUC-19,
    EUC-20
- persona: approver
  scenario: Duplicate, stale or correlated approvals accumulate toward a threshold
  harm: false independence and unauthorized action
  proposition: N approvals provide the declared independent authorization under actual
    host policy
  control: operation-bound approvals plus eligibility and deduplication
  conclusion: INDETERMINATE
  evidence: EUC-01, EUC-02, EUC-03, EUC-04, EUC-05, EUC-06, EUC-07, EUC-08, EUC-09,
    EUC-10, EUC-11, EUC-12, EUC-13, EUC-14, EUC-15, EUC-16, EUC-17, EUC-18, EUC-19,
    EUC-20
- persona: service operator
  scenario: A task is replayed across transport change and restart
  harm: duplicate or stale consequential effect
  proposition: Replay and restart cannot create a second authorization path
  control: freshness, durable replay state and idempotency
  conclusion: INDETERMINATE
  evidence: EUC-01, EUC-02, EUC-03, EUC-04, EUC-05, EUC-06, EUC-07, EUC-08, EUC-09,
    EUC-10, EUC-11, EUC-12, EUC-13, EUC-14, EUC-15, EUC-16, EUC-17, EUC-18, EUC-19,
    EUC-20
- persona: agent owner
  scenario: Rev 2 client contacts Rev 3 service and relationship state changes
  harm: downgrade or lost relationship authority
  proposition: Transport compatibility does not weaken authentication or relationship
    semantics
  control: version-bound codecs and fail-closed state transitions
  conclusion: INDETERMINATE
  evidence: EUC-01, EUC-02, EUC-03, EUC-04, EUC-05, EUC-06, EUC-07, EUC-08, EUC-09,
    EUC-10, EUC-11, EUC-12, EUC-13, EUC-14, EUC-15, EUC-16, EUC-17, EUC-18, EUC-19,
    EUC-20
- persona: room member
  scenario: Removed member attempts access after MLS epoch rotation or succession
  harm: confidentiality loss or custody lockout
  proposition: Room removal and custody succession preserve confidentiality and recoverability
  control: epoch rekey and explicit custodian succession
  conclusion: INDETERMINATE
  evidence: EUC-01, EUC-02, EUC-03, EUC-04, EUC-05, EUC-06, EUC-07, EUC-08, EUC-09,
    EUC-10, EUC-11, EUC-12, EUC-13, EUC-14, EUC-15, EUC-16, EUC-17, EUC-18, EUC-19,
    EUC-20
- persona: applicant
  scenario: Hidden vetting is replayed or uses correlated attestations
  harm: false admission or disclosure of vetters
  proposition: Hidden vetting enforces its declared threshold without excess disclosure
  control: distinct-attestation predicate and binding
  conclusion: INDETERMINATE
  evidence: EUC-01, EUC-02, EUC-03, EUC-04, EUC-05, EUC-06, EUC-07, EUC-08, EUC-09,
    EUC-10, EUC-11, EUC-12, EUC-13, EUC-14, EUC-15, EUC-16, EUC-17, EUC-18, EUC-19,
    EUC-20
- persona: holder
  scenario: Faces are reused, composed or retired across communities
  harm: cross-context correlation and disclosure
  proposition: Persona and face boundaries survive composed credential/task/UI use
  control: context boundaries and lifecycle checks
  conclusion: INDETERMINATE
  evidence: EUC-01, EUC-02, EUC-03, EUC-04, EUC-05, EUC-06, EUC-07, EUC-08, EUC-09,
    EUC-10, EUC-11, EUC-12, EUC-13, EUC-14, EUC-15, EUC-16, EUC-17, EUC-18, EUC-19,
    EUC-20
- persona: repository contributor
  scenario: Unauthorized push, unapproved PR or stale membership reaches forge
  harm: unauthorized merge or misattributed code
  proposition: Forge enforcement preserves current authority through PR, approval
    and merge
  control: forge gate plus current authorization and protected signing
  conclusion: INDETERMINATE
  evidence: EUC-01, EUC-02, EUC-03, EUC-04, EUC-05, EUC-06, EUC-07, EUC-08, EUC-09,
    EUC-10, EUC-11, EUC-12, EUC-13, EUC-14, EUC-15, EUC-16, EUC-17, EUC-18, EUC-19,
    EUC-20
- persona: mediator operator
  scenario: Queue purge or runtime configuration mutation occurs without authority
  harm: message loss or unsafe routing
  proposition: Mediator administration stays authorized and auditable
  control: signed management and least privilege
  conclusion: INDETERMINATE
  evidence: EUC-01, EUC-02, EUC-03, EUC-04, EUC-05, EUC-06, EUC-07, EUC-08, EUC-09,
    EUC-10, EUC-11, EUC-12, EUC-13, EUC-14, EUC-15, EUC-16, EUC-17, EUC-18, EUC-19,
    EUC-20
- persona: relying party
  scenario: Resolution follows a private address, redirect or rebound DNS
  harm: SSRF and confidential data exposure
  proposition: Network guards hold across actual resolver and transport composition
  control: egress guard and DNS vetting
  conclusion: INDETERMINATE
  evidence: EUC-01, EUC-02, EUC-03, EUC-04, EUC-05, EUC-06, EUC-07, EUC-08, EUC-09,
    EUC-10, EUC-11, EUC-12, EUC-13, EUC-14, EUC-15, EUC-16, EUC-17, EUC-18, EUC-19,
    EUC-20
- persona: auditor
  scenario: Evidence is truncated, rolled back or moved after key rotation
  harm: undetectable tampering or failed redress
  proposition: Audit and retained task evidence support challenge without silent tampering
  control: hash-chain verification and durable attributable receipts
  conclusion: INDETERMINATE
  evidence: EUC-01, EUC-02, EUC-03, EUC-04, EUC-05, EUC-06, EUC-07, EUC-08, EUC-09,
    EUC-10, EUC-11, EUC-12, EUC-13, EUC-14, EUC-15, EUC-16, EUC-17, EUC-18, EUC-19,
    EUC-20
- persona: key custodian
  scenario: Hybrid proof set omits one proof or signs under wrong algorithm
  harm: algorithm downgrade or custody compromise
  proposition: Post-quantum and hybrid processing reject omitted or incompatible proofs
  control: algorithm-bound keys and proof-set verification
  conclusion: INDETERMINATE
  evidence: EUC-01, EUC-02, EUC-03, EUC-04, EUC-05, EUC-06, EUC-07, EUC-08, EUC-09,
    EUC-10, EUC-11, EUC-12, EUC-13, EUC-14, EUC-15, EUC-16, EUC-17, EUC-18, EUC-19,
    EUC-20
- persona: trust-registry administrator
  scenario: Wrong sender mutates registry or stale signed answer is consumed
  harm: illegitimate recognition or stale authority
  proposition: Registry mutations and reliance preserve authority and temporal meaning
  control: authenticated bound writes and signed responses
  conclusion: INDETERMINATE
  evidence: EUC-01, EUC-02, EUC-03, EUC-04, EUC-05, EUC-06, EUC-07, EUC-08, EUC-09,
    EUC-10, EUC-11, EUC-12, EUC-13, EUC-14, EUC-15, EUC-16, EUC-17, EUC-18, EUC-19,
    EUC-20
- persona: mobile approver
  scenario: Pairing or push causes unattended approval
  harm: owner consent bypass
  proposition: Mobile approval binds owner intent, displayed action and current authority
  control: device-bound key and deliberate approval gate
  conclusion: INDETERMINATE
  evidence: EUC-01, EUC-02, EUC-03, EUC-04, EUC-05, EUC-06, EUC-07, EUC-08, EUC-09,
    EUC-10, EUC-11, EUC-12, EUC-13, EUC-14, EUC-15, EUC-16, EUC-17, EUC-18, EUC-19,
    EUC-20
- persona: agent operator
  scenario: Recalled memory carries executable instructions or excessive data
  harm: prompt injection and secret exposure
  proposition: Agent memory cannot silently acquire instruction authority
  control: untrusted-data fence and bounded storage
  conclusion: INDETERMINATE
  evidence: EUC-01, EUC-02, EUC-03, EUC-04, EUC-05, EUC-06, EUC-07, EUC-08, EUC-09,
    EUC-10, EUC-11, EUC-12, EUC-13, EUC-14, EUC-15, EUC-16, EUC-17, EUC-18, EUC-19,
    EUC-20
- persona: relying party
  scenario: Expired token, wrong audience or malicious canonicalization reaches session
  harm: session substitution or denial of service
  proposition: RP sessions are bound to audience, challenge, time and valid proof
  control: expiry/audience/challenge checks and bounded canonicalization
  conclusion: INDETERMINATE
  evidence: EUC-01, EUC-02, EUC-03, EUC-04, EUC-05, EUC-06, EUC-07, EUC-08, EUC-09,
    EUC-10, EUC-11, EUC-12, EUC-13, EUC-14, EUC-15, EUC-16, EUC-17, EUC-18, EUC-19,
    EUC-20
- persona: new adopter
  scenario: Coordinated tags are treated as a guarantee of dependency compatibility
  harm: false assurance or unreproducible build
  proposition: Actual build inputs and cross-project consumption match the claimed
    baseline
  control: exact lockfiles and producer-consumer version skew tests
  conclusion: INDETERMINATE
  evidence: EUC-01, EUC-02, EUC-03, EUC-04, EUC-05, EUC-06, EUC-07, EUC-08, EUC-09,
    EUC-10, EUC-11, EUC-12, EUC-13, EUC-14, EUC-15, EUC-16, EUC-17, EUC-18, EUC-19,
    EUC-20
- persona: excluded participant
  scenario: Participant cannot complete gesture or challenge an adverse decision
  harm: exclusion, loss of autonomy or unreviewable denial
  proposition: Consent and redress remain usable for affected people
  control: accessible alternative journey and durable redress
  conclusion: INDETERMINATE
  evidence: EUC-01, EUC-02, EUC-03, EUC-04, EUC-05, EUC-06, EUC-07, EUC-08, EUC-09,
    EUC-10, EUC-11, EUC-12, EUC-13, EUC-14, EUC-15, EUC-16, EUC-17, EUC-18, EUC-19,
    EUC-20
lineage:
  clean_room: true
  historical_inputs_used: false
  run:
    lineage_prefix: 06bc77950b572bf0154bf01dea9cd6f839856e2ce668b5784fef834f1076a30e
    instance: dtg
    snapshot: VTI-Eucalyptus
  campaign_identity: 06bc77950b572bf0154bf01dea9cd6f839856e2ce668b5784fef834f1076a30e
process_state: complete
assurance_state: indeterminate
evidence_maturity: source-only
lenses:
  rahp:
    materiality: applicable
    execution: executed
    result: INDETERMINATE
    evidence_maturity: source-only
    reason: Fresh scenario/harm/proposition source examination completed; broader
      required evidence remains absent.
  security:
    materiality: applicable
    execution: executed
    result: INDETERMINATE
    evidence_maturity: automated-conformance
    reason: Bounded target JavaScript positive/negative vectors executed; Rust/native
      security and service-composition coverage remain incomplete.
  composition:
    materiality: applicable
    execution: required-but-not-executed
    result: INDETERMINATE
    evidence_maturity: source-only
    reason: Lab handoffs attempted; historical native adapters reject this new pin.
      No full deployed-composition trace accepted.
  drarm:
    materiality: applicable
    execution: required-but-not-executed
    result: INDETERMINATE
    evidence_maturity: source-only
    reason: Restart, crash, partition, stale authority, room custody and recovery
      require target-native induced-failure evidence.
  specialist:
    materiality: applicable
    execution: executed
    result: INDETERMINATE
    evidence_maturity: modeled
    reason: DPIP incomplete-evidence interpretation is separate from unexecuted native
      observer experiments; human-independence/exclusion evidence also remains required.
```
