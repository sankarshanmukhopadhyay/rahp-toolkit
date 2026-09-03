# Trust Architecture Assurance Stack

## Reference Architecture and Adoption Playbook

**Status:** Architecture Proposal / Adoption Playbook  
**Implementation impact:** None  
**Initial worked realization:** Decentralized Trust Graph (DTG) + OpenVTC  
**Primary orchestration reference:** RAHP Toolkit  
**Document authority:** Informative portfolio architecture, with normative requirements applying only to implementations that explicitly claim conformance with this playbook  
**Change control:** Repository issue/PR process  

---

## Abstract

This document defines a reference architecture for continuously assuring concrete realizations of trust architectures against their normative baseline, implementation state, deployment configuration, dependencies, and observed behaviour.

The architecture is motivated by a separation that is common in mature technical ecosystems but is often left implicit in early trust infrastructure: the separation between a specification that states what a system is expected to mean, an implementation that realizes those statements in software, a deployment that introduces operational configuration and environmental dependencies, and an assurance process that determines what conclusions are justified by the available evidence.

The initial worked realization uses the Decentralized Trust Graph (DTG) specifications as the normative substrate and OpenVTC as a concrete implementation substrate. RAHP, the DTG Privacy Implementation Profile (DPIP), the Trust Protocol Interop Lab, and portfolio-monitoring capabilities are aligned as assurance-side components. This alignment is descriptive and prospective. Publication of this document does not alter the behaviour, authority, conformance status, or roadmap of any referenced project.

The central proposition of the stack is:

> **A concrete realization of a trust architecture is assured against an identified normative baseline, an identified implementation state, an identified deployment configuration, an identified dependency state, and a bounded body of observed evidence.**

The resulting assurance state is evidence-bound and time-bound. It is not equivalent to certification, accreditation, legal conformity, endorsement, production authorization, or standards-body approval unless an independently governed scheme explicitly consumes the evidence and makes such a decision.

---

## 1. Purpose

The purpose of the Trust Architecture Assurance Stack, abbreviated **TAAS** in this document, is to provide a coherent model for answering the following question:

> Given a normative trust architecture and one concrete implementation or deployment of that architecture, what assurance conclusions are justified by the evidence currently available?

The architecture is intended to support development-time assurance, release qualification, interoperability and composition evaluation, deployment-time assurance, continuous reassessment, and evidence production for external governance processes.

TAAS is not intended to replace the authority of specification-owning bodies, implementation maintainers, operators, auditors, regulators, conformity-assessment bodies, or certification schemes. It provides an evidence and assurance architecture that such actors MAY use.

The architecture is deliberately documentation-first. It identifies concepts, roles, interfaces, and evidence obligations before requiring schemas, APIs, workflows, or repository changes.

---

## 2. Scope

This document defines:

1. the assurance subject;
2. the distinction between normative, implementation, deployment, dependency, and observation state;
3. assurance-side architectural principles;
4. the role and authority boundary of each aligned component;
5. development-time and production-time assurance lifecycles;
6. specialist-assessor routing and evidence return;
7. executable/falsification evidence;
8. assurance-state reconciliation;
9. invalidation and reassessment semantics;
10. the relationship between assurance and certification;
11. conceptual evidence contracts;
12. an initial DTG + OpenVTC reference realization;
13. current-state alignment and gaps;
14. a staged adoption roadmap.

This document does not define a protocol wire format, API, certification scheme, legal compliance regime, trust mark, accreditation regime, or mandatory implementation roadmap.

---

## 3. Conventions and normative language

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **MAY**, and **OPTIONAL** in this document are to be interpreted as described by RFC 2119 and RFC 8174 when, and only when, they appear in all capitals.

Because this document is an architecture proposal rather than an adopted standard, those terms describe conformance with this playbook. They do not impose requirements on DTG, OpenVTC, RAHP, DPIP, the Trust Protocol Interop Lab, or any other referenced project unless that project independently adopts the requirement.

The words **implemented**, **tested**, **observed**, **inferred**, **indeterminate**, **evidence-required**, **model-gap**, and **deferred** are used as evidence-status terms. They MUST NOT be treated as interchangeable.

---

## 4. Design objective

TAAS is designed to separate four propositions that are frequently collapsed:

1. **Normative proposition:** a specification says that a property, behaviour, constraint, or relationship is required or expected.
2. **Implementation proposition:** a software implementation claims or appears to implement that normative proposition.
3. **Operational proposition:** a deployed instance is configured and operated in a way that preserves the intended property.
4. **Assurance proposition:** available evidence justifies a bounded conclusion about the preceding propositions.

A conforming assurance process MUST NOT infer proposition 4 solely from propositions 1, 2, or 3.

A specification statement MUST NOT, by itself, be treated as evidence of implementation correctness.

A successful implementation test MUST NOT, by itself, be treated as evidence of production behaviour.

A successful production observation MUST NOT, by itself, be generalized beyond the identified deployment, evidence window, and conditions under which the observation was made.

---

## 5. Architectural principles

### 5.1 Evidence before conclusion

An assurance conclusion MUST be traceable to evidence or to an explicitly declared inference rule.

Absence of required evidence MUST NOT be converted into PASS.

Where evidence is unavailable but the assurance question remains material, the result SHOULD be `evidence-required` or `indeterminate`, depending on whether the missing evidence can be identified.

### 5.2 Bounded claims

Every assurance conclusion MUST identify the subject, scope, evidence basis, and temporal boundary to which it applies.

A conclusion about one implementation version MUST NOT automatically apply to another implementation version.

A conclusion about a test environment MUST NOT automatically apply to a production deployment.

A component-level PASS MUST NOT automatically imply a composition-level PASS.

### 5.3 Provenance

Evidence used in an assurance decision SHOULD be attributable to a source, collection mechanism, version, timestamp or evidence window, and integrity reference where practical.

Where provenance cannot be established to the level required by the assurance question, the conclusion MUST reflect that limitation.

### 5.4 Explicit authority boundaries

A component MUST NOT issue a claim that depends on authority it does not possess.

Examples include:

- a portfolio observer MUST NOT declare a system safe merely because no upstream repository changed;
- an implementation maintainer MUST NOT declare independent conformity solely on the basis of self-authored tests;
- a specialist privacy assessor MUST NOT claim general system assurance;
- an assurance orchestrator MUST NOT convert an evidence-backed assessment into certification unless a separately governed certification scheme grants it that authority;
- an interoperability laboratory MUST NOT convert bounded executable success into an unqualified production-readiness claim.

### 5.5 Reassessment on material change

Assurance is not permanent.

A material change to the normative baseline, implementation, deployment configuration, dependencies, operating policy, runtime behaviour, evidence body, or threat model SHOULD trigger a materiality determination.

Where the change affects a claim previously relied upon, the previous assurance state MUST be treated as stale, superseded, conditionally valid, or requiring reassessment.

### 5.6 Generic assurance core, profile-specific evidence

The assurance orchestration model SHOULD remain independent of any single trust architecture.

Architecture-specific semantics SHOULD be expressed through profiles, data, assessor logic, evidence requirements, and composition cases rather than hard-coded into the generic orchestration core.

DTG is the first worked realization in this document. DTG-specific examples are not requirements that all TAAS adopters use DTG.

### 5.7 Falsifiability

Where a material assurance proposition can be expressed as observable behaviour, the assurance process SHOULD seek evidence capable of falsifying the proposition rather than only evidence capable of confirming an expected success path.

Negative tests, boundary conditions, failure injection, replay conditions, state-transition tests, and composition tests are therefore first-class assurance evidence.

### 5.8 Distinguish current capability from target architecture

A reference architecture MUST distinguish between:

- capability that exists and is implemented;
- capability that has been tested;
- behaviour that has been observed;
- architecture that is inferred from existing components;
- evidence that is still required;
- model gaps;
- deliberately deferred work.

Architectural aspiration MUST NOT be represented as current implementation capability.

---

## 6. Assurance subject

### 6.1 General model

The **assurance subject** is the concrete realization to which an assurance conclusion applies.

An assurance subject SHOULD be modelled as the tuple:

`S = (N, I, D, X, P, E, T)`

where:

- `N` = normative baseline;
- `I` = implementation identity;
- `D` = deployment configuration;
- `X` = dependency state;
- `P` = operating policy and governance state;
- `E` = evidence body;
- `T` = evidence window and temporal context.

Not every assurance activity requires every element. A specification-only assessment MAY omit deployment and runtime state. A production assurance activity SHOULD identify all material elements.

### 6.2 Normative baseline

The normative baseline identifies the specification state against which a realization is interpreted.

It SHOULD include, where applicable:

- specification repository and authoritative location;
- release, working-draft identifier, tag, or commit SHA;
- referenced companion specifications;
- declared profiles;
- normative dependencies;
- known open decisions relevant to the assessed property.

The normative baseline MUST be precise enough to determine whether a later specification change could invalidate the conclusion.

### 6.3 Implementation identity

The implementation identity identifies the software realization.

It SHOULD include:

- implementation name;
- release or version;
- source commit where available;
- build provenance where material;
- enabled features;
- implementation-specific profile declarations;
- implementation dependencies that affect the assurance proposition.

For the initial worked realization, OpenVTC is treated as an implementation substrate, not as the only possible DTG implementation.

### 6.4 Deployment configuration

The deployment configuration identifies the operational realization of the implementation.

It MAY include:

- environment designation;
- configuration digest;
- service topology;
- enabled endpoints;
- DID methods;
- credential formats;
- trust registry endpoints;
- mediators;
- key-management arrangement;
- persistence configuration;
- logging and retention settings;
- policy configuration;
- network boundaries;
- administrative domains;
- high-availability or recovery configuration.

The level of detail SHOULD be proportionate to the claims being assured.

### 6.5 Dependency state

Dependency state captures external or subordinate components whose behaviour may affect the assurance conclusion.

This MAY include:

- libraries;
- databases;
- identity providers;
- trust registries;
- mediators;
- HSM or KMS services;
- external policy engines;
- cloud services;
- network services;
- operating system/runtime versions;
- third-party protocol components.

Dependency identity SHOULD be captured when changes in that dependency could invalidate a relied-upon assurance claim.

### 6.6 Policy and governance state

Trust systems frequently depend on rules that are not reducible to source code.

The assurance subject SHOULD therefore identify relevant policy and governance state where such state influences permitted actions or trust conclusions.

Examples include:

- authorization policy;
- role or delegation policy;
- revocation policy;
- retention policy;
- operator duty;
- escalation or redress policy;
- trust-registry governance;
- issuance policy;
- verifier policy.

### 6.7 Evidence body

The evidence body is the set of observations, artifacts, test results, traces, assertions, and specialist findings used to support the assurance conclusion.

Evidence MAY be static, executable, observed, derived, or attested.

The evidence body SHOULD identify evidence quality and provenance.

### 6.8 Evidence window

The evidence window identifies when the observations were valid or collected.

A production assurance record SHOULD state the period over which runtime observations apply.

A record MUST NOT imply continued observation outside its evidence window unless the collection mechanism is demonstrably continuous and that fact is itself represented in the record.

---

## 7. Assurance levels of analysis

TAAS distinguishes the following levels of analysis.

### 7.1 Specification assurance

**Object:** normative specification or composition of specifications.

Typical questions include:

- Are requirements internally coherent?
- Do two specifications compose without an identified ambiguity?
- Does a normative design create a privacy, security, authority, lifecycle, or governance risk?
- Is an asserted property actually specified?

Specification assurance does not establish that an implementation correctly realizes the specification.

### 7.2 Implementation assurance

**Object:** identified software implementation.

Typical questions include:

- Does the implementation behave consistently with the normative baseline?
- Are required failure modes present?
- Are state transitions enforced?
- Are implementation-specific deviations declared?
- Are security and privacy controls actually realized?

Implementation assurance does not, by itself, establish production deployment assurance.

### 7.3 Composition assurance

**Object:** interaction among two or more components, protocols, profiles, or roles.

Typical questions include:

- Does individually correct behaviour remain correct when components interact?
- Do identity, authorization, lifecycle, privacy, and policy assumptions remain consistent across boundaries?
- Does one component expose information another component did not expect to become linkable?
- Can a sequence of valid local actions create an invalid global state?

Composition assurance SHOULD include executable or otherwise falsifiable evidence where practical.

### 7.4 Deployment assurance

**Object:** identified operational deployment.

Typical questions include:

- Does configuration preserve the properties established at implementation level?
- Are operator controls consistent with the intended trust model?
- Do runtime observations support the expected behaviour?
- Have changes occurred since the prior assurance record?
- Are required dependencies in the expected state?

Deployment assurance is the primary focus for production use.

### 7.5 Operational assurance

**Object:** deployment behaviour over time.

Operational assurance evaluates whether the deployed system continues to satisfy relied-upon properties during a bounded evidence window.

Operational assurance MAY be continuous, periodic, event-driven, or hybrid.

### 7.6 Conformity assessment and certification

Conformity assessment and certification are governance processes, not automatic consequences of the preceding assurance levels.

A certification scheme MAY consume TAAS evidence. TAAS itself does not confer certification authority.

---

## 8. Component model and authority alignment

### 8.1 Overview

The initial DTG realization aligns existing projects according to the following model.

| Component | Primary role | Principal inputs | Principal outputs | MUST NOT imply |
|---|---|---|---|---|
| DTG specifications | Normative architecture | WG decisions, specification text | requirements, protocol semantics, normative constraints | implementation correctness, production assurance |
| OpenVTC | Concrete implementation | DTG specifications, implementation design | executable software, implementation behaviour, runtime artifacts | ecosystem-wide assurance, independent certification |
| DTG Portfolio Monitor | Upstream dependency observation | repositories, releases, commits, issue/PR state where relevant | change evidence, pinned source state, dependency observations | safety, conformance, production readiness |
| RAHP | Assurance orchestration and reconciliation | subject model, findings, evidence, specialist returns | bounded assurance state, residual questions, reassessment triggers | certification authority, legal conformity |
| DPIP | Specialist privacy assessment | privacy propositions, implementation/runtime evidence | privacy finding, evidence requirements, model gaps | general system assurance |
| Trust Protocol Interop Lab | Executable composition and falsification evidence | implementations, configurations, cases, invariants | reproducible execution evidence | production certification, universal interoperability |
| Production operator | Operational realization and evidence source | implementation, configuration, policies, dependencies | runtime state, operational evidence, incident/change records | independent conformity merely by self-assertion |
| External conformity/certification scheme | Governance decision | criteria, evidence, assessor authority | conformity decision, certificate/attestation where applicable | authority outside its scheme scope |

### 8.2 DTG specifications

DTG provides the normative baseline for the initial realization.

The assurance stack MUST treat DTG sources as authoritative only to the extent that the relevant DTG project declares them authoritative.

TAAS MUST NOT silently override unresolved upstream semantics.

Where an upstream decision remains open, the assurance state SHOULD record the uncertainty or pin the assessment to a stated interpretation.

### 8.3 OpenVTC

OpenVTC is treated as a concrete implementation capable of producing implementation and runtime evidence relevant to DTG propositions.

OpenVTC MAY serve as:

- a reference implementation target;
- an executable subject in Interop Lab cases;
- a source of runtime traces;
- a source of state-transition evidence;
- a reproducible implementation for qualification runs;
- a basis for deployment-specific assurance.

OpenVTC MUST NOT be treated as synonymous with DTG. The specification and implementation authority planes remain distinct.

### 8.4 DTG Portfolio Monitor

The DTG Portfolio Monitor is modelled as an **upstream dependency observer**.

Its core question is:

> Has the normative or repository baseline changed in a way that may affect an existing assurance conclusion?

The monitor is particularly useful for development, maintenance, release qualification, and assurance invalidation.

It is not the centre of production assurance.

In production, the monitor SHOULD be treated as one evidence source among several, alongside implementation releases, configuration changes, dependency changes, runtime observations, operator policy changes, and specialist evidence.

### 8.5 RAHP

RAHP is modelled as the **assurance orchestration and reconciliation plane**.

Its responsibilities MAY include:

- accepting or constructing the assurance subject;
- determining materiality;
- identifying assurance questions;
- routing questions to specialist assessors;
- receiving durable specialist returns;
- distinguishing evidence gaps from model gaps;
- reconciling component and composition findings;
- determining residual assurance state;
- recording reassessment conditions;
- maintaining assurance lineage.

RAHP SHOULD remain generic. DTG-specific propositions SHOULD enter through configuration, data, profiles, findings, and specialist logic rather than target-specific core behaviour.

RAHP MUST NOT elevate its own orchestration role into certification authority.

### 8.6 DPIP

DPIP is modelled as the first specialist assurance service in the stack.

Its authority is bounded to privacy questions within its declared scope.

A privacy assessment SHOULD identify:

- privacy proposition;
- required evidence;
- available evidence;
- observed or inferred behaviour;
- unresolved evidence gaps;
- model gaps;
- bounded conclusion.

Where runtime evidence is required but unavailable, DPIP SHOULD return an evidence-bound state rather than infer a universal PASS from specification intent.

### 8.7 Trust Protocol Interop Lab

The Trust Protocol Interop Lab is modelled as the **executable composition and falsification evidence plane**.

Its purpose is not merely to demonstrate successful interoperability. It is to make consequential propositions executable, observable, and falsifiable under bounded conditions.

A Lab case SHOULD identify:

- proposition under test;
- implementation(s) under test;
- configuration;
- prerequisites;
- expected invariants;
- positive path;
- negative path;
- failure conditions;
- observable outputs;
- evidence capture;
- limitations;
- claims that MUST NOT be inferred.

Lab results SHOULD be consumable as evidence by RAHP or specialist assessors.

### 8.8 Production operator

A production operator controls material facts that neither DTG nor OpenVTC alone can determine.

Examples include:

- actual deployment topology;
- administrative separation;
- key custody;
- logging and retention;
- trust registry selection;
- network access;
- incident handling;
- policy configuration;
- backup and recovery;
- operator privileges;
- rollout strategy.

Production assurance therefore requires operator-originated evidence or independently observable evidence concerning these facts.

---

## 9. Reference assurance lifecycle

### 9.1 General lifecycle

A conforming TAAS lifecycle SHOULD support the following stages:

1. **Observe**
2. **Identify subject**
3. **Qualify evidence**
4. **Determine materiality**
5. **Form assurance questions**
6. **Route specialist examination**
7. **Gather or execute evidence**
8. **Receive specialist returns**
9. **Reconcile findings**
10. **Determine residual state**
11. **Record assurance outcome**
12. **Monitor invalidation conditions**
13. **Reassess when required**

### 9.2 Observe

Observation MAY be triggered by:

- normative repository change;
- implementation release;
- configuration change;
- dependency update;
- policy change;
- runtime anomaly;
- incident;
- scheduled assurance cycle;
- new evidence becoming available;
- previously missing evidence being supplied.

### 9.3 Identify subject

The process MUST identify the subject precisely enough that evidence and conclusions cannot be accidentally applied to a different realization.

### 9.4 Qualify evidence

Evidence SHOULD be checked for provenance, relevance, recency, completeness, and integrity appropriate to the assurance question.

### 9.5 Determine materiality

Not every change requires complete reassessment.

Materiality determines whether the observed change may alter a relied-upon proposition.

A materiality determination SHOULD be explicit and reproducible where practical.

### 9.6 Form assurance questions

Material change SHOULD be converted into one or more explicit assurance questions.

Example:

> Does the new identifier-correlation-scope model preserve the no-unintended-cross-context-correlation property in the assessed OpenVTC deployment?

### 9.7 Route specialist examination

Questions requiring domain-specific reasoning SHOULD be routed to an appropriate specialist assessor.

Routing MUST NOT imply that the specialist is authoritative outside its declared scope.

### 9.8 Gather or execute evidence

Evidence MAY be gathered through:

- repository inspection;
- implementation tests;
- conformance tests;
- Interop Lab execution;
- runtime telemetry;
- configuration inspection;
- policy inspection;
- traces;
- cryptographic evidence;
- operator attestations;
- external assessment;
- incident records.

### 9.9 Receive specialist returns

Specialist returns SHOULD be durable and attributable.

A conceptual specialist return SHOULD include:

- subject identifier;
- assessor identity/type;
- question identifier;
- evidence references;
- finding;
- confidence or limitation where applicable;
- missing evidence;
- model gaps;
- timestamp/evidence window;
- conditions for reassessment.

### 9.10 Reconcile findings

RAHP or an equivalent orchestrator SHOULD reconcile specialist and non-specialist findings without collapsing uncertainty.

Conflicting evidence MUST remain visible until reconciled or explicitly accepted as residual disagreement.

### 9.11 Determine residual state

Residual state SHOULD answer:

- what is supported;
- what failed;
- what remains unknown;
- what evidence is missing;
- what model is missing;
- what change would invalidate the result;
- what action, if any, is required.

### 9.12 Record outcome

The assurance record SHOULD be immutable or append-only at the level necessary to preserve lineage.

New assessments SHOULD supersede or relate to prior assessments rather than silently rewriting history.

---

## 10. Assurance states

TAAS does not mandate a single universal status vocabulary, but a conforming implementation SHOULD preserve at least the following semantic distinctions.

### 10.1 PASS

Available evidence supports the assessed proposition within the declared subject and scope.

PASS MUST NOT imply universal safety, certification, or applicability outside the evidence boundary.

### 10.2 FAIL

Available evidence contradicts a required proposition or demonstrates a material violation within the assessed scope.

### 10.3 INDETERMINATE

Available evidence is insufficient to justify PASS or FAIL, and the insufficiency cannot be reduced to one immediately resolvable evidence request.

### 10.4 EVIDENCE-REQUIRED

The assurance question is understood and the missing evidence required to resolve it can be identified.

### 10.5 MODEL-GAP

The assurance system lacks a model, rule, proposition, or interpretation required to evaluate the question responsibly.

A model gap MUST NOT be converted to PASS merely because no known rule rejects the subject.

### 10.6 DEFERRED

The question is intentionally postponed and is not part of the current assurance conclusion.

### 10.7 STALE or SUPERSEDED

A previously issued conclusion no longer applies without qualification because the subject or relied-upon evidence has materially changed.

---

## 11. Development-time assurance

### 11.1 Purpose

Development-time assurance helps specification authors and implementers identify contradictions, missing semantics, implementation defects, composition failures, and evidence requirements before deployment.

### 11.2 Typical flow

A development-time flow MAY be:

1. Portfolio Monitor observes a material DTG change.
2. RAHP determines that the change affects one or more assurance propositions.
3. RAHP routes privacy questions to DPIP.
4. Interop Lab executes bounded cases against an OpenVTC build.
5. OpenVTC test/runtime artifacts are captured.
6. DPIP or other specialists evaluate the evidence.
7. RAHP reconciles the evidence.
8. Findings feed back to DTG, OpenVTC, DPIP, Lab cases, or documentation.

### 11.3 Expected outputs

Development-time outputs MAY include:

- specification clarification request;
- implementation defect;
- test-case addition;
- specialist evidence requirement;
- composition finding;
- accepted residual risk;
- no material impact;
- deferred question.

### 11.4 Non-goal

A development-time PASS MUST NOT automatically be represented as production assurance.

---

## 12. Production assurance

### 12.1 Primary object

In production, the primary assurance object is the concrete deployment, not the specification repository.

The production question is therefore:

> What assurance conclusions are justified for this deployment, against this normative baseline and implementation version, under this configuration, policy, dependency state, and evidence window?

### 12.2 Evidence sources

Production assurance SHOULD consider, where material:

- normative baseline changes;
- implementation release changes;
- deployment configuration;
- dependency state;
- runtime telemetry;
- policy state;
- security events;
- privacy observations;
- key-management evidence;
- operator control evidence;
- Interop Lab reproduction against equivalent configuration;
- specialist-assessor returns.

### 12.3 Production twin or equivalent reproducible environment

Where destructive, adversarial, or disruptive tests are inappropriate against production, an operator SHOULD consider a reproducible environment that reflects the production implementation and relevant configuration.

Such an environment MAY be used by the Interop Lab or equivalent test plane.

Evidence from a reproduction environment MUST identify the extent to which production equivalence has been established.

### 12.4 Runtime evidence

Runtime evidence is particularly important for properties that depend on actual disclosure, retention, correlation, authorization, policy evaluation, failure handling, or operator behaviour.

A specification statement or unit test SHOULD NOT substitute for runtime evidence where the property can materially differ under deployment configuration.

### 12.5 Continuous or event-driven reassessment

Production assurance MAY operate continuously or through event-driven reassessment.

Relevant events include:

- upstream specification change;
- implementation upgrade;
- configuration drift;
- policy change;
- dependency update;
- incident;
- new threat intelligence;
- unexpected runtime observation;
- assurance evidence expiration.

---

## 13. The role of upstream portfolio monitoring in production

The DTG Portfolio Monitor remains useful in production, but its role changes.

During specification development, it may be a primary trigger for assurance work.

During production operation, it is one upstream sensor in a broader assurance graph.

A production assurance architecture SHOULD therefore consider at least the following classes of trigger:

```
Normative changes ───────┐
Implementation changes ─┤
Configuration changes ──┤
Dependency changes ─────┤
Policy changes ──────────┤──> materiality -> reassessment
Runtime observations ───┤
Incidents ───────────────┤
New evidence ────────────┘
```

A lack of normative change does not establish that a production deployment remains assured.

Likewise, a production anomaly may require reassessment even where DTG and OpenVTC are unchanged.

---

## 14. Specialist assurance model

### 14.1 Purpose

Specialist assurance prevents the orchestration layer from embedding every domain model into a monolithic core.

### 14.2 Specialist categories

Potential categories MAY include:

- privacy;
- security;
- authority and delegation;
- lifecycle and revocation;
- governance and policy;
- resilience;
- composition;
- accessibility;
- regulatory mapping.

This document does not require creation of any additional specialist project.

### 14.3 Routing requirements

A routing decision SHOULD identify:

- assurance question;
- specialist scope;
- evidence supplied;
- evidence requested;
- expected result contract;
- failure/retry semantics;
- subject identity.

### 14.4 Specialist return requirements

A specialist return MUST NOT be interpreted outside its declared scope.

Where a specialist cannot evaluate the question because the required model is absent, it SHOULD return `model-gap` rather than invent a local interpretation without attribution.

---

## 15. Executable assurance and falsification

### 15.1 Why execution matters

Trust architectures often contain propositions that appear coherent at specification level but fail in composition, state transition, or runtime disclosure.

Executable cases are therefore a preferred evidence source where behaviour can be reproduced.

### 15.2 Case structure

A useful assurance case SHOULD define:

1. claim under test;
2. subject implementation(s);
3. normative reference;
4. configuration;
5. initial state;
6. stimulus;
7. expected behaviour;
8. forbidden behaviour;
9. observation mechanism;
10. evidence artifact;
11. result;
12. limitations.

### 15.3 Negative cases

Negative cases SHOULD be treated as first-class.

Examples include:

- expired authority;
- revoked relationship;
- duplicate/replayed message;
- cross-context identifier correlation;
- missing evidence;
- stale status information;
- dependency outage;
- malformed or ambiguous policy;
- partial implementation support;
- recovery after interrupted delivery.

### 15.4 Production claim boundary

A successful Lab execution supports only the case and environment actually exercised.

It MUST NOT be represented as independent proof that every production deployment behaves identically.

---

## 16. Conceptual evidence contracts

This section identifies information that a mature implementation of TAAS is likely to require. It does not define schemas.

### 16.1 Assurance subject descriptor

A future subject descriptor MAY include:

```yaml
subject:
  normative_baseline:
    source: <repository-or-authoritative-reference>
    version: <tag-working-draft-or-sha>
  implementation:
    name: <implementation>
    version: <release-or-sha>
  deployment:
    instance: <deployment-identifier>
    configuration_digest: <digest>
  dependencies:
    - name: <dependency>
      version: <version-or-state>
  policy:
    digest: <policy-reference>
  evidence_window:
    from: <timestamp>
    to: <timestamp>
```

### 16.2 Evidence descriptor

A future evidence descriptor MAY include:

```yaml
evidence:
  id: <stable-id>
  subject: <subject-id>
  type: <test-trace-config-attestation-observation>
  producer: <producer>
  collected_at: <timestamp>
  integrity: <digest-or-reference>
  scope: <scope>
  location: <artifact-reference>
```

### 16.3 Specialist assessment return

A future specialist return MAY include:

```yaml
assessment:
  subject: <subject-id>
  question: <question-id>
  assessor: <assessor-id-or-type>
  outcome: PASS | FAIL | INDETERMINATE | EVIDENCE_REQUIRED | MODEL_GAP
  evidence:
    - <evidence-ref>
  missing_evidence:
    - <requirement>
  limitations:
    - <limitation>
  reassess_if:
    - <condition>
```

### 16.4 Assurance record

A future assurance record MAY include:

```yaml
assurance_record:
  subject: <subject-id>
  normative_baseline: <reference>
  implementation: <reference>
  deployment: <reference>
  evidence_window: <window>
  findings:
    - <finding-ref>
  specialist_returns:
    - <assessment-ref>
  overall_state: <bounded-state>
  supported_claims:
    - <claim>
  unresolved:
    - <question>
  residual_risk:
    - <risk>
  invalidation_conditions:
    - <condition>
  issued_at: <timestamp>
```

The examples are illustrative. No implementation requirement follows from their publication.

---

## 17. Invalidation and assurance lineage

### 17.1 General rule

An assurance conclusion remains meaningful only while the subject and relied-upon evidence remain materially equivalent to the assessed state.

### 17.2 Potential invalidation events

Examples include:

- normative requirement changes;
- reinterpretation of a normative requirement;
- implementation release;
- implementation commit change;
- feature flag change;
- configuration change;
- dependency upgrade;
- key-management change;
- policy change;
- trust-registry change;
- evidence expiration;
- incident;
- vulnerability discovery;
- new contradictory runtime observation;
- specialist model change.

### 17.3 Materiality before full reassessment

An invalidation event does not necessarily require complete reassessment.

The system SHOULD first determine whether the event can affect a relied-upon proposition.

### 17.4 Lineage

A new assurance record SHOULD identify the prior record it supersedes, updates, or depends upon.

Historical records SHOULD remain available for audit and reasoning where practical.

---

## 18. Certification and conformity boundary

### 18.1 Assurance is not certification

TAAS produces attributable evidence, findings, and bounded assurance states.

TAAS does not, by itself, confer:

- certification;
- accreditation;
- legal conformity;
- regulatory approval;
- standards-body endorsement;
- authorization to operate;
- trust marks;
- product approval;
- procurement eligibility.

### 18.2 When assurance may support certification

A separately governed conformity or certification scheme MAY define criteria that consume TAAS evidence.

For example:

```
TAAS evidence and findings
          |
          v
Authorized evaluator / conformity process
          |
          v
Governed decision
          |
          v
Certificate, attestation, or conformity statement
```

The authority for the final decision derives from the scheme, not from TAAS.

### 18.3 Certification-enabling infrastructure

A long-term role for TAAS MAY be to provide high-quality, reproducible, machine-readable evidence to certification or conformity processes while remaining independent of the authority to issue the final certification decision.

This separation is RECOMMENDED because it preserves the distinction between evidence production and governance authority.

---

## 19. DTG + OpenVTC reference realization

### 19.1 Purpose

The DTG + OpenVTC realization demonstrates how the generic model can be applied using projects that already provide normative and implementation substrate.

### 19.2 Reference flow

```
DTG normative baseline
        |
        v
OpenVTC implementation
        |
        v
Concrete deployment or reproducible instance
        |
        +-----------------------------+
        |                             |
        v                             v
runtime/config evidence       Interop Lab execution
        |                             |
        +---------------+-------------+
                        |
                        v
                  specialist assessors
                     e.g. DPIP
                        |
                        v
                       RAHP
                        |
                        v
                bounded assurance record
```

The DTG Portfolio Monitor observes the normative side of this flow and supplies change/provenance evidence when relevant.

### 19.3 Example: correlation-scope change

Consider a normative DTG change that alters how correlation scope is declared or interpreted.

A possible assurance flow is:

1. The Portfolio Monitor observes the normative change and pins the affected source state.
2. RAHP determines that the change may affect privacy and composition propositions.
3. The assurance subject identifies the relevant DTG baseline and OpenVTC version.
4. DPIP identifies runtime evidence needed to determine whether an identifier is unintentionally linkable across contexts.
5. Interop Lab executes a case against the relevant OpenVTC build and configuration.
6. Runtime traces identify what identifiers, status references, or relationship artifacts are exposed.
7. DPIP assesses the evidence.
8. RAHP reconciles the privacy return with other findings.
9. The assurance record states what is supported and what remains unresolved.
10. If the OpenVTC version or deployment configuration later changes, materiality is reevaluated.

### 19.4 Example assurance record in prose

A production-oriented assurance statement might read:

> Against DTG baseline N, OpenVTC release I, deployment configuration digest C, dependency state X, and runtime evidence collected during evidence window T, propositions A, B, and C are supported. Proposition D remains evidence-required because verifier-side retention evidence was not available. The result does not establish certification, legal conformity, or behaviour outside the identified deployment and evidence window. Reassessment is required if the DTG correlation-scope semantics, OpenVTC release, deployment configuration, verifier policy, or relevant runtime evidence changes materially.

This is the intended shape of a TAAS conclusion.

---

## 20. Current portfolio alignment

This section describes the current portfolio at an architectural level. It is not a claim that all proposed TAAS capabilities are already implemented.

### 20.1 RAHP

**Current alignment:** strong.

RAHP already contains substantial machinery for observation intake, materiality, bounded assessment, specialist routing, durable specialist return, reconciliation, evidence-state handling, and assurance lineage.

**Architecture interpretation:** implemented or partially implemented assurance orchestration plane.

**Remaining question:** whether all production-oriented subject identity, deployment-state, and invalidation concepts are represented with sufficient explicitness for external adopters.

### 20.2 DPIP

**Current alignment:** strong for specialist privacy assessment.

DPIP already operates as a bounded privacy assessor and can distinguish missing runtime evidence from supported conclusions.

**Architecture interpretation:** implemented specialist-assessment pattern.

**Remaining question:** broader availability of real runtime evidence and independent consumption outside the current DTG assurance flow.

### 20.3 Trust Protocol Interop Lab

**Current alignment:** strong for executable, bounded, evidence-producing cases.

The Lab already emphasizes executable governance propositions, falsifiability, bounded claim semantics, and evidence-gated maturity.

**Architecture interpretation:** implemented or partially implemented execution/falsification plane.

**Remaining question:** standardized evidence exchange with assurance orchestrators and reproducibility against externally operated implementations or production-equivalent configurations.

### 20.4 DTG Portfolio Monitor

**Current alignment:** strong for upstream observation.

**Architecture interpretation:** implemented upstream dependency observer.

**Remaining question:** whether production assurance should consume its outputs directly or through a more general observation/event contract.

### 20.5 OpenVTC

**Current alignment:** external implementation substrate.

OpenVTC provides concrete software behaviour against which DTG propositions can be exercised.

**Architecture interpretation:** implementation target and potential evidence producer.

**Remaining question:** what stable implementation/deployment metadata and runtime evidence can be consumed without coupling TAAS to OpenVTC internals.

---

## 21. Gap classification

The architecture intentionally records gaps without immediately converting them into implementation work.

### 21.1 Implemented

Use where code or durable repository behaviour exists and performs the described capability.

### 21.2 Tested

Use where the capability has falsification-oriented or reproducible test evidence.

### 21.3 Observed

Use where behaviour has been seen in a concrete run, deployment, or artifact.

### 21.4 Inferred

Use where the architecture appears to be represented by existing components but has not been explicitly declared or independently tested as such.

### 21.5 Evidence-required

Use where the concept is understood but empirical evidence is missing.

### 21.6 Model-gap

Use where no adequate rule, model, or interpretation currently exists.

### 21.7 Deferred

Use where implementation is intentionally postponed pending adoption, upstream stability, or additional evidence.

---

## 22. Adoption playbook

### 22.1 Stage 0 — Architecture publication

**Objective:** establish a shared vocabulary and component boundary model.

Activities:

- publish this document;
- review authority boundaries;
- review terminology;
- verify that the architecture describes existing projects accurately;
- collect objections and mismatches;
- avoid code changes.

Exit criterion:

> The architecture is considered a useful description of the intended assurance model even if implementation gaps remain.

### 22.2 Stage 1 — Portfolio alignment

**Objective:** align documentation across existing repositories.

Possible activities:

- add references from RAHP, DPIP, Interop Lab, and relevant monitor documentation;
- identify repository-local ownership of any discovered gaps;
- ensure README claims remain bounded;
- document which component owns each output.

No new cross-repository runtime dependency is required at this stage.

### 22.3 Stage 2 — Contract discovery

**Objective:** determine whether conceptual contracts need formal representation.

Candidate contracts include:

- assurance subject descriptor;
- observation/change event;
- specialist assessment request;
- specialist assessment return;
- executable evidence artifact;
- assurance record;
- invalidation event.

Contracts SHOULD be introduced only where more than one component has a demonstrated need to exchange the information.

### 22.4 Stage 3 — Implementation qualification

**Objective:** demonstrate repeatable assurance against an implementation such as OpenVTC.

Activities MAY include:

- pin implementation versions;
- run clean-room qualification;
- execute bounded Lab cases;
- collect specialist evidence;
- reproduce assessment identities;
- exercise failure and replay semantics.

### 22.5 Stage 4 — Deployment-oriented assurance

**Objective:** extend the subject from implementation to concrete deployment.

Activities MAY include:

- configuration identity;
- operator evidence;
- runtime evidence;
- dependency state;
- production-equivalent reproduction;
- invalidation triggers;
- evidence-window semantics.

### 22.6 Stage 5 — Externalization

**Objective:** prove that the stack is not only self-consistent within one portfolio.

High-value externalization evidence includes:

- an independent implementation used as an assurance subject;
- an external specialist implementing the assessment-return contract;
- an independent operator reproducing an Interop Lab case;
- an external consumer reading and acting on an assurance record;
- an upstream specification issue changed in response to an assurance finding.

### 22.7 Stage 6 — Conformity/certification integration, if desired

**Objective:** allow a separately governed conformity process to consume TAAS evidence.

This stage SHOULD occur only when there is an actual governance body, scheme owner, relying-party need, or regulatory requirement.

TAAS SHOULD NOT create a certification regime merely to complete its own architecture.

---

## 23. Maturity model

A TAAS realization MAY be described using the following maturity dimensions.

| Dimension | Early | Developing | Advanced | Operational |
|---|---|---|---|---|
| Subject identity | informal | version-pinned | deployment-aware | continuously attributable |
| Evidence provenance | ad hoc | referenced | integrity-aware | automated and durable |
| Specialist assurance | manual | bounded assessor | portable returns | multiple independent assessors |
| Executable evidence | examples | repeatable cases | negative/composition coverage | production-linked reproduction |
| Reconciliation | narrative | structured | durable lineage | continuous reassessment |
| Invalidation | manual | release-based | materiality-driven | event-driven |
| External adoption | none | internal cross-repo | external reproduction | independent operators/assessors |
| Certification integration | none | conceptual | scheme mapping | governed external use |

Maturity SHOULD be reported dimensionally. A stack SHOULD NOT claim a single maturity label that obscures weak dimensions.

---

## 24. Security considerations

An assurance architecture can create false confidence if its evidence boundaries are unclear.

Implementers SHOULD consider at least the following risks:

- fabricated evidence;
- stale evidence;
- replayed evidence;
- subject/evidence mismatch;
- incomplete configuration capture;
- false independence between evidence producer and evaluator;
- missing negative cases;
- silent model gaps;
- overgeneralization from test to production;
- overgeneralization from one implementation to an ecosystem;
- compromise of evidence storage or lineage;
- assessor implementation defects;
- policy/configuration drift.

The assurance system SHOULD be designed so that failure of one evidence source does not silently manufacture support for a proposition.

---

## 25. Privacy considerations

The assurance process itself may collect sensitive operational evidence.

Evidence collection SHOULD follow data minimization and purpose limitation.

The system SHOULD avoid retaining production identifiers, relationship data, verifier transcripts, secrets, or user-level telemetry where the assurance question can be answered using less sensitive evidence.

Where sensitive evidence is required, access, retention, redaction, and provenance rules SHOULD be explicit.

Privacy evidence MAY itself become a correlation surface; this risk SHOULD be considered in DPIP and assurance-evidence design.

---

## 26. Governance considerations

TAAS separates evidence authority from governance authority.

A relying organization SHOULD identify:

- who may define assurance questions;
- who may supply evidence;
- who may operate specialist assessors;
- who may accept residual risk;
- who may declare an assurance record superseded;
- who may translate assurance into operational authorization;
- who, if anyone, may issue conformity or certification claims.

These authorities MAY be held by different organizations.

The architecture SHOULD NOT assume that technical control implies governance authority.

---

## 27. Interoperability considerations

Interoperability claims SHOULD distinguish:

- protocol compatibility;
- semantic compatibility;
- policy compatibility;
- state-transition compatibility;
- governance compatibility;
- privacy compatibility;
- operational compatibility.

A successful wire exchange establishes only what was actually exercised.

The Trust Protocol Interop Lab MAY be used to make broader composition claims testable, but each claim MUST remain bounded by the case and evidence.

---

## 28. Relationship to implementation and standards development

The intended feedback cycle is:

```
Normative specification
        |
        v
Implementation
        |
        v
Executable / runtime evidence
        |
        v
Specialist assessment
        |
        v
Assurance reconciliation
        |
        v
Finding
        |
        +----------------------------+
        |                            |
        v                            v
Specification clarification    Implementation remediation
```

A mature assurance stack therefore supports standards development rather than merely judging completed standards.

Findings MAY reveal:

- ambiguous normative text;
- unstated assumptions;
- insufficient failure semantics;
- missing privacy constraints;
- composition risks;
- implementation defects;
- operator-control dependencies;
- evidence requirements that the specification should make explicit.

---

## 29. Worked production scenario

### 29.1 Initial state

Assume:

- DTG baseline `N1`;
- OpenVTC release `I1`;
- production deployment `P1`;
- configuration digest `C1`;
- dependency set `X1`;
- policy digest `G1`;
- evidence window `T1`.

### 29.2 Evidence collection

The production assurance process collects:

- pinned DTG source references;
- OpenVTC release/build identity;
- configuration metadata;
- dependency versions;
- runtime traces for selected trust-task and credential flows;
- privacy-relevant disclosure observations;
- Interop Lab reproduction using `I1` and a configuration materially equivalent to `C1`;
- DPIP privacy assessment;
- RAHP risk/composition findings.

### 29.3 Reconciliation

RAHP determines:

- authority/lifecycle proposition A: PASS;
- delivery/replay proposition B: PASS within tested conditions;
- privacy proposition C: PASS for observed pairwise flow;
- privacy proposition D: EVIDENCE-REQUIRED because verifier retention behaviour is not observable;
- composition proposition E: INDETERMINATE because an upstream DTG semantic remains unresolved.

### 29.4 Assurance record

The record states that A-C are supported for subject `(N1, I1, P1, C1, X1, G1, T1)`; D and E remain unresolved; no certification claim is made.

### 29.5 Change event

OpenVTC is upgraded from `I1` to `I2`.

The prior assurance record does not disappear, but its applicability to the current deployment becomes stale until materiality is determined.

If the change affects only an unrelated administrative interface, RAHP MAY determine no reassessment of A-E is required.

If the change affects identifier disclosure or message delivery, relevant propositions MUST be reassessed.

This demonstrates why assurance is tied to the concrete realization rather than to the product name alone.

---

## 30. Anti-patterns

The following patterns are explicitly discouraged.

### 30.1 “The spec says it, therefore it is assured”

Normative intent is not implementation evidence.

### 30.2 “The tests passed, therefore production is certified”

Test success is bounded evidence, not certification.

### 30.3 “OpenVTC is DTG”

Implementation and normative authority are distinct.

### 30.4 “No upstream changes means no assurance changes”

Configuration, dependencies, policy, and runtime behaviour can change independently.

### 30.5 “The specialist returned PASS, therefore the system passes”

Specialist conclusions are scoped and require reconciliation.

### 30.6 “Unknown means acceptable”

Missing evidence and model gaps MUST remain visible.

### 30.7 “The assurance engine owns the standard”

Assurance tooling MUST NOT silently replace upstream normative authority.

### 30.8 “The architecture document creates implementation obligations”

This playbook is not a hidden backlog. Implementation work requires explicit repository-local issues and acceptance criteria.

---

## 31. Recommended repository ownership model

If future implementation gaps are accepted, ownership SHOULD follow the capability boundary.

| Gap type | Presumptive owner |
|---|---|
| generic orchestration, reconciliation, assurance lineage | RAHP |
| DTG privacy semantics and privacy evidence | DPIP |
| executable cases, negative tests, reproducible compositions | Trust Protocol Interop Lab |
| DTG upstream observation and change provenance | DTG Portfolio Monitor |
| implementation behaviour or runtime instrumentation | OpenVTC or relevant implementation |
| normative ambiguity | owning DTG specification/task force |
| certification criteria | external scheme owner or authorized governance body |

This table does not authorize work in those repositories.

---

## 32. Review questions for standards and architecture discussion

Reviewers are encouraged to challenge the proposal using questions such as:

1. Is the assurance subject sufficiently precise to prevent accidental claim transfer?
2. Are normative authority and implementation authority adequately separated?
3. Does the model over-privilege OpenVTC as a reference implementation?
4. Is the Portfolio Monitor correctly positioned as an upstream observer rather than a production assurance controller?
5. Does RAHP have too much responsibility in the proposed orchestration model?
6. Are specialist-assessor boundaries sufficiently explicit?
7. Can the model represent contradictory evidence without collapsing it?
8. Are evidence-required and model-gap adequately distinguished?
9. Is the production deployment treated as a first-class assurance object?
10. Is the certification boundary sufficiently strong?
11. Can a non-DTG trust architecture adopt the model without changing the core concepts?
12. Does the architecture create any hidden assumption that one organization controls specification, implementation, operation, and assurance?
13. What evidence would be required before calling a TAAS realization independently validated?
14. Which conceptual contracts are actually needed, and which would be premature standardization?

---

## 33. Initial decisions proposed by this document

This document proposes the following architectural decisions for discussion:

1. The primary assurance object for production is the concrete deployment, not the specification repository.
2. The normative baseline remains a first-class part of the assurance subject.
3. OpenVTC is an implementation substrate and evidence producer, not a normative authority.
4. The DTG Portfolio Monitor is an upstream dependency observer, not the sole production assurance trigger.
5. RAHP is the assurance orchestration and reconciliation plane.
6. DPIP is a specialist privacy assessor.
7. The Trust Protocol Interop Lab is an executable composition and falsification evidence plane.
8. Assurance conclusions are bounded, attributable, version-sensitive, configuration-sensitive, and time-sensitive.
9. Material change can invalidate or trigger reassessment of prior assurance.
10. Missing evidence and missing models remain explicit terminal or intermediate states.
11. Certification is a separately governed decision that MAY consume TAAS evidence but is not produced automatically by TAAS.
12. The architecture SHOULD remain generic, with DTG + OpenVTC serving as the first worked realization.
13. Publication of this document creates no implementation obligation.

---

## 34. Next steps after adoption of the document

If this architecture is accepted as a useful model, the next activity SHOULD be an **alignment review**, not an implementation wave.

That review SHOULD compare each repository against this document and classify every relevant concept as:

- implemented;
- tested;
- observed;
- inferred;
- evidence-required;
- model-gap;
- deferred;
- not applicable.

Only after that review SHOULD repository-local implementation issues be considered.

The highest-value future work is expected to be work that increases external validity, such as independent implementation targets, independent specialist assessors, production-equivalent evidence, reproducible cases, and external consumers of assurance records.

---

## 35. Conclusion

A trust architecture becomes operationally meaningful through concrete implementations and deployments. The assurance question therefore cannot end at specification analysis.

The Trust Architecture Assurance Stack proposed here provides a disciplined path from normative intent to implementation identity, deployment state, observed evidence, specialist examination, executable falsification, reconciliation, and bounded assurance outcome.

Its governing principle is simple:

> **Assure concrete realizations of trust architectures against their normative baseline, implementation state, deployment configuration, dependency and policy state, and observed behaviour.**

The architecture intentionally stops short of certification. It creates an evidence infrastructure capable of supporting implementation improvement, standards refinement, production risk decisions, and—where an independently governed scheme exists—future conformity or certification processes.

The immediate objective is not to change code. It is to establish a common architecture precise enough that future implementation work can be judged against explicit ownership, evidence, and authority boundaries rather than emerging through repository-local improvisation.

---

## References

- RFC 2119, *Key words for use in RFCs to Indicate Requirement Levels*.
- RFC 8174, *Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words*.
- Trust over IP Decentralized Trust Graph work: https://github.com/trustoverip
- OpenVTC repositories: https://github.com/OpenVTC/openvtc
- RAHP Toolkit: https://github.com/sankarshanmukhopadhyay/rahp-toolkit
- DTG Privacy Implementation Profile: https://github.com/sankarshanmukhopadhyay/dtg-privacy-implementation-profile
- Trust Protocol Interop Lab: https://github.com/sankarshanmukhopadhyay/trust-protocol-interop-lab

> **Reference hygiene note:** project URLs and organizational ownership MAY change. An adopted revision SHOULD replace illustrative project references with the authoritative locations current at publication time.
