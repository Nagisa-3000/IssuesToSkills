---
name: adapt-provider-interface-boundaries
description: Diagnose and repair compatible-provider routing or request-shape failures by establishing provider identity and precedence before changing only the owning boundary.
metadata:
  short-description: Establish a provider contract, then repair only its owning boundary
  status: candidate
---

# Define the provider contract before adapting its boundary

When a compatible provider path fails because configuration, persisted routing, client construction, or request shape disagrees with the actual provider interface, first establish an evidence-backed identity, precedence, and field-preservation contract. Then adapt only the boundary that violates that contract, adding transport or request-routing behavior only when the selected interface requires it.

**Lifecycle:** `candidate_pending_independent_holdouts`. This package is a candidate. Retrieval and the holdout oracle are recorded, but paired agent validation is still pending; do not install it as a validated global Skill yet.

## Use this skill when

- A provider-compatible path reaches the wrong endpoint, restores stale routing metadata, omits required routing arguments, or emits a field rejected by the selected endpoint.
- Multiple representations or configuration sources can identify the provider route, and their precedence is currently implicit or inconsistent.
- A shared implementation mostly satisfies the provider protocol, but a narrow client-construction, resume, or outbound-request boundary has a documented mismatch.
- The affected interface can be identified from observable configuration, persisted route data, or parsed endpoint identity rather than model-name guesses.

## Do not use this skill when

### Anti-goals

- Do not redesign authentication, prompting, response processing, retry behavior, or unrelated provider paths.
- Do not infer provider identity from model-family names when endpoint, authentication mode, or persisted route evidence is available.
- Do not overwrite explicit configuration with defaults, environment values, historical metadata, or synthesized fields.
- Do not add absent optional settings or provider-specific request fields to the ordinary request path.
- Do not mutate caller-owned or persisted conversation data merely to change the outbound wire representation.
- Do not treat distinct Actions as interchangeable merely because they occupy the same workflow role.

### Not applicable

- The target provider is not compatible with the existing request and response protocol.
- There is no evidence-backed way to identify the selected provider interface or determine precedence among competing route sources.
- The failure belongs to credential acquisition, initial provider discovery, response interpretation, or another subsystem rather than an interface boundary.
- Different consumers intentionally implement different routing semantics rather than alternate paths to the same provider contract.
- A lower-level SDK already owns and guarantees endpoint selection, validation, and request adaptation for the affected path.

## Required inputs

- Runtime task context: repository slug, absolute checkout, optional base ref, and target scope.
- The observed provider symptom and the narrowest reproducible request, resume, or construction path.
- Observable interface signals such as explicit provider mode, canonical endpoint identity, or an
  authoritative persisted route.
- Competing configuration sources and their evidenced precedence.
- A focused oracle plus regression commands for unaffected provider paths.

Do not create a persistent project-binding layer. Locate semantic roles in the supplied checkout
and keep that mapping only in the run record.

## Workflow

### 1. Establish provider identity and precedence

- Role id: `establish-interface-contract`
- Status: required
- Use when: Use when multiple endpoint, provider, persisted-route, or configuration sources can influence the path, or when the affected endpoint must be distinguished from compatible alternatives.
- Action: Define which observable signal selects the provider interface, which representation or configuration source is authoritative, and how explicit, current, legacy, and fallback values compose.
- Check: Exercise positive selection, competing-source precedence, absent and partial inputs, malformed inputs where applicable, and negative cases that must retain the existing provider path.

### 2. Adapt the boundary that owns the mismatch

- Role id: `adapt-contract-owner`
- Status: required
- Use when: Run after the provider identity and precedence contract is established and a specific consumer, constructor, or outbound adapter is shown to violate it.
- Action: Make the consuming or construction boundary honor the established contract while preserving its local safety behavior and the behavior of unaffected paths.
- Check: Observe the boundary's output directly and prove that authoritative values are used, explicit or caller-authored values are preserved, and unrelated behavior remains unchanged.

### 3. Validate a selected custom endpoint

- Role id: `guard-selected-endpoint`
- Status: conditional
- Use when: Use only when this boundary accepts custom endpoint values and no lower layer already guarantees their parsing and transport policy.
- Action: Reject malformed or insecure remote endpoint overrides before external client construction while preserving an evidence-backed local-development exception.
- Check: Prove acceptance of permitted secure and loopback forms and rejection of malformed or disallowed remote plaintext forms before SDK construction.

### 4. Translate provider routing at dispatch

- Role id: `translate-request-routing`
- Status: conditional
- Use when: Use only when successful dispatch requires per-request routing fields not represented by the common request shape.
- Action: Map configured provider routing identifiers to the exact request keywords expected by the provider without changing requests when those identifiers are absent.
- Check: Capture the provider request call and assert exact key translation for configured identifiers and exact absence for unconfigured identifiers.

Establish all required roles before a conditional role. Role ids express portable intent; they do
not authorize copying a training-repository implementation. Read
[the Workflow reference](references/workflow.md) for ordering and decision points, and
[the Action contracts](references/action-contracts.md) for real graph bindings.

## Validation

1. Focused contract checks: test provider selection and precedence using explicit, fallback, partial, absent, malformed, and confusable inputs relevant to the selected identity signal.
2. Focused boundary checks: directly inspect the canonical resolver result, component constructor contract, SDK constructor options, or emitted request fields and verify exact preservation and omission rules.
3. Integration checks: exercise the real consumer-to-boundary path, such as session resume, application configuration through construction, SDK creation, or multi-turn HTTP request conversion.
4. Regression checks: run existing tests for unaffected providers, ordinary requests, legacy persisted data, endpoint ownership, provider healing, established constructor options, and caller-authored field preservation.
5. Environment-complete verification: execute the focused repository test suite in an intact checkout with required dependencies; do not substitute static inspection for successful runtime validation.

Static inspection is not runtime validation. Run the focused oracle, the affected integration path,
and regressions for unchanged providers in the current checkout.

## Stop, ask, or defer

- Stop and reassess if provider identity is inferred from a model name or unsafe hostname substring. Detection signal: A similarly named, suffix-confusable, or unrelated endpoint selects the specialized path.
- Stop and reassess if a fallback overrides an explicit or fresher value. Detection signal: Tests with both explicit and fallback sources select the fallback, or stale metadata replaces a newer nested route.
- Stop and reassess if the adaptation broadens to unaffected providers or ordinary requests. Detection signal: Optional fields appear when unconfigured, unrelated hosts select the adapter, or established request snapshots change.
- Stop and reassess if a caller-authored value is mistaken for a synthesized compatibility value. Detection signal: Distinct explicit fields are removed or persisted source history is mutated.
- Stop and reassess if an endpoint and provider-mode combination becomes inconsistent. Detection signal: The external constructor receives an endpoint associated with one interface and a mode associated with another.
- Stop and reassess if static inspection is reported as completed runtime validation. Detection signal: Focused tests were unavailable, dependencies were missing, or the checkout was incomplete.

Also stop when no evidence-backed provider identity or precedence rule is available. Ask for the
missing contract instead of guessing from a model name or a broad hostname substring.

## Supporting references

- [Workflow roles, ordering, and concrete realizations](references/workflow.md)
- [Bound Action contracts](references/action-contracts.md)
- [Validation ladder and failure modes](references/validation.md)
- [Observed holdout feedback and lifecycle decision](references/feedback.md)
- [Provenance and promotion status](references/provenance.yaml)
