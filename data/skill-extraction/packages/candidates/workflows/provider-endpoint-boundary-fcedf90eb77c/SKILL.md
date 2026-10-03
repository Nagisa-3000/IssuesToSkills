---
name: provider-endpoint-boundary-fcedf90eb77c
description: "Repair a provider SDK construction boundary when provider-specific endpoint overrides are ignored, explicit endpoints lose precedence, or an omitted SDK mode disagrees with the selected authentication route."
---

# Adapt the provider endpoint boundary

## Purpose

Make a shared provider-client factory consistently resolve custom endpoints, validate the selected endpoint, and supply a deterministic provider mode without changing unrelated authentication routes.

## When to use

- A provider-specific endpoint setting exists but does not reach the SDK constructor.
- Explicit configuration and provider-specific fallback settings compete at a shared client factory.
- Direct factory callers omit a provider-mode flag and the selected authentication route must supply its default.
- Constructor-level tests can observe the endpoint, mode and preserved request options.

## Do not use / Anti-goals

- Do not redesign authentication, acquire credentials, or inspect live user settings.
- Do not replace proxy configuration with endpoint configuration.
- Do not change SDK internals, retry behavior, model selection or response processing.
- Do not infer a cross-repository Pattern from this single implementation.

## Not applicable when

- The failing request uses a separate client implementation outside the shared SDK branch.
- The endpoint already reaches the constructor and the failure is remote connectivity or service behavior.
- The application has no ownership over SDK construction or no observable constructor oracle.
- The requested security policy requires DNS resolution, redirect controls or comprehensive SSRF protection.

## Applicability probes

- Map the configuration producer, shared factory, SDK constructor and alternate authentication branches in the caller-supplied checkout.
- Locate both normalized and direct factory callers; establish whether the provider-mode field can be absent.
- Identify explicit endpoint input, provider-specific fallback inputs and the existing absence convention.
- Locate tests that intercept SDK construction without network calls or real credentials.
- Confirm the intended transport policy and loopback exceptions rather than assuming every custom URL is acceptable.

## Preconditions

- The caller supplies repository, checkout, base revision, implementation scope, language and test command.
- Source and tests establish which route selects which endpoint fallback.
- The SDK exposes endpoint and provider-mode constructor options.
- Test fixtures use synthetic values and restore their configuration stubs.
- Changes and execution occur only in an authorized writable target checkout; this historical source checkout remains untouched.

## Workflow

Follow [Workflow](references/workflow.md). Map roles with [locate-contract](references/actions/locate-contract.md), implement [resolve-endpoint](references/actions/resolve-endpoint.md), enforce [validate-endpoint](references/actions/validate-endpoint.md), and complete [default-provider-mode](references/actions/default-provider-mode.md). Execute the validation ladder after all required Actions.

## Validation ladder

- First record the role mapping, route matrix, precedence rule and focused constructor oracle.
- Test explicit-versus-fallback resolution, provider isolation, absent endpoints and direct callers.
- Test malformed URLs, remote plaintext URLs and allowed loopback fixtures; rejection must occur before SDK construction.
- Test absent, explicit true and explicit false provider-mode values.
- Run neighboring constructor tests for headers, API version, authentication inputs and alternate branches.
- Run the caller-supplied focused command, then broader checks if available; record actual outcomes and execution blockers.
- Inspect documentation against the implemented scope and security limitations.

## Failure modes

- Resolving endpoints only in a configuration builder misses direct factory callers.
- Falling back by credential presence selects the wrong route for sparse configurations.
- A truthiness default overwrites an explicit false provider-mode value.
- Validating fallback values but not explicit values leaves an inconsistent trust boundary.
- Catching validation errors and continuing silently changes the intended destination.
- Rebuilding request options drops existing headers or API-version settings.

## Stop conditions

- Stop and request evidence if route ownership or constructor behavior cannot be established.
- Stop if the intended endpoint precedence or transport policy is ambiguous.
- Stop before editing excluded authentication branches or inspecting credentials.
- Report blocked or unexecuted tests explicitly; do not label static inspection as runtime success.
- Do not claim package validation, index admission or transfer success before the corresponding host or evaluation step.

## Evidence and provenance

The historical implementation is documented in [Episode](references/episode.md), with [boundary evidence](references/evidence/endpoint-boundary.md), [mode evidence](references/evidence/provider-mode.md) and [validation limits](references/evidence/inspection-validation.md). Identity and frozen split are recorded in [Provenance](references/provenance.json).

## Known limitations

- Historical tests were inspected, not executed; authored eval definitions also remain unexecuted.
- Historical tests and authored definitions do not establish transfer success.
- The inspected checkout is sparse; an available test-harness caller does not establish complete production call-site coverage.
- The historical URL guard accepts any parseable scheme for its exact loopback hostname allowlist; it is not an HTTP-only scheme guard.
- URL syntax and hostname checks do not establish redirect, DNS, certificate or remote-service safety.
- Preserve project-specific branch behavior only after mapping it; do not assume all authentication routes share endpoint semantics.
