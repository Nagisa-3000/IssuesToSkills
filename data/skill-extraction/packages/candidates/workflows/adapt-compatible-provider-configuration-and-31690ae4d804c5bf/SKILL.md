---
name: adapt-compatible-provider-configuration-and-31690ae4d804c5bf
description: "A partial-order workflow for adding provider-specific client settings and request-routing fields while keeping domain construction independent of credentials and preserving the default request path. Use when A provider uses an otherwise compatible client library but requires additional endpoint metadata or routing identifiers.; Provider configuration is currently split into or coupled with a domain-component constructor.; The provider request method accepts routing fields that are not represented in the application's common request construction."
metadata:
  skill-id: "workflow:b5dccd8edcc90ddd"
  level: workflow
  status: candidate
  version: 1
  category: "provider-interface-adaptation"
---

# Adapt a compatible provider across configuration, construction, and request boundaries

## Purpose

Accept the compatible provider's required settings at the application boundary and translate them into the client and request interfaces needed to dispatch a chat completion successfully.

## When to use

- A provider uses an otherwise compatible client library but requires additional endpoint metadata or routing identifiers.
- Provider configuration is currently split into or coupled with a domain-component constructor.
- The provider request method accepts routing fields that are not represented in the application's common request construction.

## Do not use / Anti-goals

- Do not redesign model prompting, edit formats, retry policy, or response processing.
- Do not force provider-specific optional values into requests when the user did not configure them.
- Do not retain credentials in unrelated domain constructor signatures merely to initialize a shared provider client.
- Do not claim end-to-end provider connectivity without a request-level or integration oracle.

Exclusions:
- The provider is not compatible with the existing client and request/response protocol.
- The required adaptation changes authentication or transport semantics beyond client attributes and request keyword mapping.
- Provider configuration is intentionally isolated per component or per request and cannot safely use the shared client state evidenced here.

## Applicability probes

- Does the current task satisfy this signal: A provider uses an otherwise compatible client library but requires additional endpoint metadata or routing identifiers.
- Does the current task satisfy this signal: Provider configuration is currently split into or coupled with a domain-component constructor.
- Does the current task satisfy this signal: The provider request method accepts routing fields that are not represented in the application's common request construction.
- Can the current checkout establish this entry state: The application can configure a key and base endpoint, but additional provider settings cannot flow through the interface; provider initialization is coupled to domain construction; and request dispatch omits provider-specific routing fields.
- Can a focused oracle observe the Action postconditions at their owning boundary?

## Preconditions

The application can configure a key and base endpoint, but additional provider settings cannot flow through the interface; provider initialization is coupled to domain construction; and request dispatch omits provider-specific routing fields.

Required runtime inputs:
- provider client's supported configuration attributes
- provider request method's expected routing argument names
- application argument or configuration-file surface
- domain-component construction call sites
- request-dispatch call site
- regression and request-mocking test harness

Map semantic owners and parameter slots to the current checkout before editing.

## Workflow

### Action 1 — Configure the provider client at application startup

- Atomic ID: `semantic-action:f739bb2c7c9a9da7`; [action contract](references/actions/0141bdec2f411dc2.md).
- Owner: application composition and provider-client configuration boundary.
- Object: credential, endpoint base, provider API type, provider API version, deployment identifier, engine identifier, provider client module.
- Operation: Expose the provider's optional connection and routing settings at the application boundary and apply only supplied values to the shared client before downstream components are created.
- Preserve: The application boundary accepts the supported optional provider settings and initializes the shared provider client before constructing downstream components; omitted optional settings are not overwritten.
- Required: true; condition: The compatible provider exposes additional client-level configuration values..
- Depends on: no prior Action.
- Verify: Verify each supplied interface value maps to the correct client attribute before component creation and that omitted optional values are not assigned.

### Action 2 — Remove provider credentials from domain-component construction

- Atomic ID: `semantic-action:d803e48cee271d14`; [action contract](references/actions/fe0e7e6bddb429ae.md).
- Owner: domain component construction boundary.
- Object: domain component factory, application entry-point call site, direct test call sites.
- Operation: Make domain-component creation independent of provider initialization after configuration ownership moves to the application boundary, then reconcile all direct construction call sites.
- Preserve: The component constructor requires only its domain inputs and no longer mutates provider configuration; direct call sites conform to that contract.
- Required: true; condition: Provider initialization previously occurred inside the domain-component factory or constructor..
- Depends on: centralize-provider-client-configuration.
- Verify: Verify production and direct test call sites construct the component without credential or endpoint arguments and retain existing behavior.

### Action 3 — Forward provider-specific routing fields at request dispatch

- Atomic ID: `semantic-action:00aaec027a328c3f`; [action contract](references/actions/ed4e15f2318b7422.md).
- Owner: provider request adapter.
- Object: provider client module, chat-completion request keyword map, deployment identifier, engine identifier.
- Operation: Translate configured routing identifiers into the keyword arguments expected by the provider's request method, without adding absent optional fields.
- Preserve: Each request includes deployment_id and/or engine exactly when the corresponding configured client attributes exist, and otherwise retains the common request shape.
- Required: true; condition: The provider requires deployment or engine routing fields on each request..
- Depends on: centralize-provider-client-configuration.
- Verify: Capture the provider request call and verify configured routing fields are translated to deployment_id and engine, while absent fields remain absent.

Completion invariant: Supplied provider settings are applied before domain construction, the domain constructor is provider-independent, and request dispatch conditionally carries the provider's expected routing identifiers without changing the ordinary request path.

## Validation ladder

- Static diff check: confirm the supported interface fields map to provider-client attributes and the domain constructor no longer owns provider initialization.
- Constructor regression check: run existing domain, command, and editing tests through the simplified construction contract.
- Request-unit check: mock the provider request method and assert routing-key presence and absence for configured and unconfigured cases.
- Configuration-path check: exercise command-line and configuration-file inputs to confirm equivalent normalized client state.
- Integration check: issue a minimal request against a configured compatible provider endpoint and confirm successful routing.

Report static/source, focused unit, regression, integration/request-boundary, and environment/backend results separately. Mark an unavailable level unverified; do not count an inspected test as an executed test.

## Failure modes

- retrieval_failure: selected package describes a different failure boundary.
- applicability_failure: entry state or exclusions disagree with the current task.
- composition_failure: Action dependencies or owner boundaries cannot be satisfied.
- action_failure: the direct oracle disproves an Action postcondition.
- stale_environment: the current implementation or SDK contract differs from evidence.
- missing_oracle: source inspection is available but executable validation is absent.

## Stop conditions

- Stop if the provider client does not support the proposed client attributes or request arguments.
- Stop if configuration ownership cannot be moved without introducing conflicting shared-client state.
- Stop if existing direct construction call sites cannot be reconciled to the provider-independent contract.
- Defer completion if no oracle can verify the emitted request arguments or a real compatible-provider request.

## Evidence and provenance

Read [the workflow](references/workflow.md) for ordering and source identity. Read [provenance](references/provenance.json) and linked evidence cards only when inspecting historical support.

## Known limitations

- The pinned change contains no direct automated assertion for client-attribute assignment or deployment_id/engine forwarding.
- The changed regression tests could not be executed in the supplied environment because pytest is not installed.
- Successful live connectivity to the documented compatible provider is not established by the checkout or evidence bundle.
- The shared mutable provider-module state may affect multiple component instances; the pinned change does not test isolation or reset behavior.
- Did pull request 88 pass its historical CI suite? The supplied GitHub bundle omits status checks, and the local environment cannot run pytest.
- Does the target client version accept both deployment_id and engine simultaneously, or are they alternative routing modes? The implementation forwards both when both attributes exist, but no test or discussion resolves the intended precedence.
- Are environment-variable forms for the newly added options expected to be part of the supported contract through configargparse's automatic prefix behavior? The implementation makes that plausible, but the pinned change does not document or test those names.
- Candidate package: compilation and structural validation do not prove cross-project transfer.
- Training oracles are recorded instructions; compilation does not execute them.
- Integration and environment/backend validation must be established in the current task.
