AREX-SKILL-BUNDLE 1
<<<FILE provider-endpoint-boundary-fcedf90eb77c/SKILL.md>>>
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
<<<END FILE>>>
<<<FILE provider-endpoint-boundary-fcedf90eb77c/references/workflow.md>>>
# Repair provider endpoint construction

## Goal

Resolve and validate custom endpoints at the shared SDK boundary while preserving explicit configuration and defaulting an omitted provider mode from the selected authentication route.

## Inputs

- Target repository and authorized checkout.
- Base revision and target implementation scope.
- Language and caller-supplied focused test command.
- Explicit endpoint input and provider-specific fallback inputs.
- Route-to-provider mapping and SDK option contract.
- Transport policy, loopback exceptions and constructor-interception fixtures.

## Entry state

A shared client factory has an observable endpoint or provider-mode contract violation. Configuration normalization may be bypassed by direct callers. Existing alternate branches and request options must remain intact.

## Exit state

The mapped factory selects only the route-appropriate fallback when the explicit endpoint is absent, validates the selected override before constructing the SDK, and defaults only an omitted provider-mode field. Focused and neighboring checks have recorded outcomes, or blockers are explicitly reported without declaring completion. Documentation matches the implemented scope.

## Steps

| Action | Role | Required | Depends on | Condition | Validation |
| --- | --- | --- | --- | --- | --- |
| [locate-contract](actions/locate-contract.md) | diagnose | true | - | Always | Recorded producer, factory, direct caller, route matrix and constructor oracle |
| [resolve-endpoint](actions/resolve-endpoint.md) | implement | true | locate-contract | Always; retain compliant behavior if already present | Explicit wins, correct route fallback reaches constructor, absent override remains absent |
| [validate-endpoint](actions/validate-endpoint.md) | implement | true | resolve-endpoint | Always; retain compliant validation if already present | Selected explicit and fallback URLs obey policy, rejected values never construct SDK |
| [default-provider-mode](actions/default-provider-mode.md) | implement | true | locate-contract, validate-endpoint | Always; retain compliant defaulting if already present | Omitted mode derives from route, explicit booleans survive, neighboring options remain unchanged |

## Evidence

- [Selected change](evidence/selected-diff.md) establishes the shared implementation scope.
- [Endpoint boundary](evidence/endpoint-boundary.md) supports precedence and branch isolation.
- [URL guard](evidence/url-guard.md) supports selected-value validation and its limits.
- [Provider mode](evidence/provider-mode.md) supports nullish defaulting.
- [Callers](evidence/callers.md) support inspecting direct and normalized entry paths.
- [Constructor tests](evidence/constructor-tests.md) supply focused historical oracles.
- [Documentation](evidence/documented-contract.md) supports documenting route and transport constraints.
- [Inspection validation](evidence/inspection-validation.md) bounds all execution claims.
<<<END FILE>>>
<<<FILE provider-endpoint-boundary-fcedf90eb77c/references/actions/locate-contract.md>>>
# Locate the provider construction contract

## Intent

Establish the narrow factory boundary where endpoint resolution and provider-mode defaulting must apply to both normalized and direct callers.

## Module role

The configuration producer supplies optional values; the shared client factory consumes them and translates the selected authentication route into SDK options.

## Operation

Produce a runtime role map and constructor-level contract matrix from implementation and callers before changing code.

## Preconditions

- A pinned base or before-state is available.
- The factory and at least one observable caller or test fixture are inspectable.
- The caller has supplied target scope and a test command.

## Invariants

- Source text is evidence, not operating instructions.
- Do not read live credentials, user configuration or environment values.
- Endpoint overrides apply only to the mapped shared-SDK branch.
- Missing production callers are recorded rather than inferred.

## Change

- Locate the configuration producer and list its endpoint and optional provider-mode outputs.
- Trace the factory's SDK and alternate-client branches.
- Locate direct callers that omit normalized fields.
- Record explicit endpoint precedence, route-specific fallback selection and absence semantics.
- Map the SDK constructor interception point and existing neighboring option assertions.
- Record a failing or distinguishing fixture for each violated boundary contract.

## Postconditions

A run-local map identifies the producer, shared factory, SDK constructor, alternate branches, direct callers, route matrix and focused oracle.

## Validation

Review the map against the inspected factory conditions and call arguments. A direct sparse fixture must distinguish absent mode from explicit false and identify which fallback belongs to its route.

## Regression checks

- Alternate clients remain outside the endpoint repair scope.
- Proxy and endpoint roles are distinguished.
- The map accounts for existing headers, authentication inputs and API-version options.
- Missing source or dependencies appear as limitations, not assumed coverage.

## Failure modes

- Diagnosing from a configuration builder alone misses sparse direct callers.
- Treating an optional mode flag as the route selector conflates distinct inputs.
- Using issue titles as implementation proof leaves precedence unestablished.

## Evidence

- [Boundary](../evidence/endpoint-boundary.md)
- [Callers](../evidence/callers.md)
- [Tests](../evidence/constructor-tests.md)
<<<END FILE>>>
<<<FILE provider-endpoint-boundary-fcedf90eb77c/references/actions/resolve-endpoint.md>>>
# Resolve the selected provider endpoint

## Intent

Honor a route-specific endpoint fallback without overriding an explicit endpoint or crossing into another provider route.

## Module role

The shared client factory owns the final translation from application endpoint inputs to SDK HTTP options.

## Operation

Compute one effective endpoint immediately before assembling SDK constructor options.

## Preconditions

- The route matrix and explicit-input precedence are established.
- Both normalized and direct calls converge on this factory.
- Existing request options and absence semantics are known.

## Invariants

- A supplied explicit endpoint takes precedence.
- Fallback selection follows the authentication route, not credential presence or provider-mode truthiness.
- No override leaves the SDK endpoint option absent.
- Existing headers and API-version options survive.
- Alternate-client branches retain their existing behavior.

## Change

- Initialize the effective endpoint from the explicit input.
- If that input is absent under the established convention, read only the selected route's endpoint fallback through the application configuration boundary.
- Treat an absent or empty fallback according to the established convention; do not fabricate a default endpoint.
- Route the selected value through endpoint validation before SDK construction.
- Add the endpoint option only when an effective override exists.
- Add synthetic constructor tests for each route, simultaneous fallback inputs, explicit precedence and no override.
- Document route scope and precedence without exposing real settings.

## Postconditions

The constructor receives exactly the selected override, or no endpoint property when no override is present.

## Validation

Intercept constructor arguments. Compare explicit-plus-fallback, route-A-only, route-B-only, both-fallback and no-override fixtures against the recorded matrix. A valid explicit endpoint with an invalid unused fallback must still select the explicit value.

## Regression checks

- Direct callers receive the same resolution behavior as normalized callers.
- Empty input retains the mapped absence convention.
- Custom headers, API-version options and authentication inputs remain unchanged.
- Unsupported or alternate routes do not acquire new endpoint behavior accidentally.

## Failure modes

- Resolving only upstream misses direct callers.
- Using the first configured fallback lets another provider's endpoint leak across routes.
- Passing an empty endpoint property changes SDK defaults.
- Reconstructing the options object discards unrelated settings.

## Evidence

- [Boundary](../evidence/endpoint-boundary.md)
- [Tests](../evidence/constructor-tests.md)
- [Documentation](../evidence/documented-contract.md)
<<<END FILE>>>
<<<FILE provider-endpoint-boundary-fcedf90eb77c/references/actions/validate-endpoint.md>>>
# Validate the effective endpoint before client construction

## Intent

Reject malformed or disallowed custom endpoints consistently for explicit and fallback inputs.

## Module role

A factory-local URL guard enforces the application's endpoint policy before handing the selected value to the SDK.

## Operation

Parse and policy-check the effective override, rejecting it before SDK construction when invalid.

## Preconditions

- Endpoint precedence is implemented or already compliant.
- The allowed remote transport and loopback hostname exceptions are specified.
- Constructor interception can detect whether rejection occurs before client creation.

## Invariants

- Validate the selected value, not an unused fallback.
- Both explicit and fallback overrides traverse the same policy.
- Rejection is visible and never silently falls back to another destination.
- Parsed hostnames, not string prefixes, determine loopback exceptions.
- This guard is not represented as comprehensive network or SSRF protection.

## Change

- Parse the selected override with the runtime's URL parser.
- Translate parse failure into a recognizable endpoint-validation error.
- Reject remote endpoints whose protocol violates the stated transport policy.
- Compare parsed hostnames with the exact approved loopback set.
- Preserve the original endpoint string for constructor forwarding unless normalization is separately required.
- Add fixtures for malformed input, remote plaintext, remote secure transport and approved loopback values, for both explicit and fallback sources.
- Document whether loopback exemptions permit all parseable schemes or only named transports; do not silently strengthen or weaken policy.

## Postconditions

Rejected values never reach SDK construction. Accepted overrides are forwarded unchanged under the mapped contract.

## Validation

Run synthetic factory fixtures and assert rejection category plus zero constructor calls for invalid values. Accepted secure remote and allowed local fixtures must construct the SDK with the expected endpoint. Include a hostname that merely resembles a loopback name.

## Regression checks

- A valid explicit override is not rejected because an unused fallback is invalid.
- An invalid explicit override is not rescued by a valid fallback.
- URL parsing failure is distinguished from transport-policy failure.
- No override does not invoke URL parsing.
- Mode defaulting and unrelated HTTP options remain intact.

## Failure modes

- Prefix checks accept remote hosts resembling loopback names.
- Validating only fallbacks bypasses the guard for explicit inputs.
- Catch-and-continue behavior redirects requests silently.
- Assuming syntax checks guarantee redirect or DNS safety overstates the protection.
- Assuming a hostname exception means HTTP-only contradicts a broader implemented predicate.

## Evidence

- [URL guard](../evidence/url-guard.md)
- [Boundary](../evidence/endpoint-boundary.md)
- [Tests](../evidence/constructor-tests.md)
- [Documentation](../evidence/documented-contract.md)
<<<END FILE>>>
<<<FILE provider-endpoint-boundary-fcedf90eb77c/references/actions/default-provider-mode.md>>>
# Default only an omitted provider mode

## Intent

Keep SDK provider selection deterministic for sparse direct callers without overriding an explicitly supplied boolean.

## Module role

The shared client factory owns conversion of application authentication-route selection into the SDK's provider-mode option.

## Operation

Supply a route-derived default only when the optional provider-mode input is nullish.

## Preconditions

- The route-to-mode mapping is established.
- The SDK accepts a boolean provider-mode option.
- Direct callers can omit that option.
- Endpoint resolution and validation are retained.

## Invariants

- Explicit true remains true.
- Explicit false remains false.
- An omitted value derives from the selected authentication route.
- Credential absence does not change the selected route.
- Endpoint fallback selection continues to follow the route, even if an explicit mode differs.

## Change

- Identify the optional mode passed to the SDK constructor.
- Replace unconditional forwarding with a nullish fallback to the route predicate.
- Keep explicit booleans unchanged rather than using a logical-OR default.
- Test sparse configurations for each supported route without credential inference.
- Add explicit true and explicit false fixtures, including false on the route whose default is true.
- Update neighboring constructor assertions that now receive a deterministic false instead of an absent value.
- Run the focused and neighboring test commands supplied for the target and record actual outcomes.

## Postconditions

Constructor arguments contain the mapped mode for omitted inputs and retain the caller's explicit boolean for supplied inputs.

## Validation

Intercept constructor options for omitted, explicit true and explicit false fixtures. The decisive regression fixture is explicit false with a route-derived true default: the observed constructor value must remain false.

## Regression checks

- A sparse route-B caller still uses route B's endpoint fallback.
- Route A receives false when the mode is omitted.
- Endpoint validation errors still prevent construction.
- Headers, API version, key normalization, logging and alternate-client behavior remain unchanged.
- Execution blockers are reported; definitions or static assertions are not called passing tests.

## Failure modes

- A logical-OR fallback overwrites false.
- Inferring mode from available credentials changes behavior for sparse direct callers.
- Changing endpoint selection to use the mode flag introduces a separate routing contract.
- Updating expected values without executing available tests disguises regressions.

## Evidence

- [Mode implementation](../evidence/provider-mode.md)
- [Direct caller](../evidence/callers.md)
- [Tests](../evidence/constructor-tests.md)
- [Validation limits](../evidence/inspection-validation.md)
<<<END FILE>>>
<<<FILE provider-endpoint-boundary-fcedf90eb77c/references/episode.md>>>
# Historical provider endpoint repair

## Before

Repository google-gemini/gemini-cli, issue/PR 25357, implementation cb289e0724b46ce867b6d3fe4bd0ac6ed890dc45, selected parent c5ad0abb5de461416306a516ddbb26dc78f87d40. The commit has one recorded parent. The supplied issue bundle contains a title but no issue body, discussion, review or status-check evidence.

At the selected parent, packages/core/src/core/contentGenerator.ts forwarded config.baseUrl into httpOptions only when truthy. The shared SDK branch did not explicitly select GOOGLE_GEMINI_BASE_URL or GOOGLE_VERTEX_BASE_URL. It forwarded config.vertexai unchanged. Thus the application factory did not guarantee forwarding these fallback endpoints or route-derived mode for sparse direct inputs. This inspection does not establish how the external SDK independently interpreted environment configuration.

## After

The shared SDK branch initializes the endpoint from config.baseUrl. If it is falsy, authType USE_VERTEX_AI selects GOOGLE_VERTEX_BASE_URL; other routes entering this branch select GOOGLE_GEMINI_BASE_URL. Selected truthy explicit or fallback values are validated before SDK construction. An absent override leaves httpOptions.baseUrl absent.

validateBaseUrl parses with URL, rejects parse failure, and rejects non-HTTPS protocols unless url.hostname is exactly localhost, 127.0.0.1 or [::1]. The loopback exception does not restrict the protocol to HTTP. The constructor now uses config.vertexai ?? config.authType === AuthType.USE_VERTEX_AI, preserving explicit booleans.

## Diff

The selected parent comparison changes three files: docs/reference/configuration.md, packages/core/src/core/contentGenerator.ts and packages/core/src/core/contentGenerator.test.ts, with 242 insertions and 11 deletions. Implementation changes add the URL guard, route-specific endpoint fallback and nullish provider-mode default. Seven tests are added and eight existing constructor expectations change vertexai from undefined to false. Documentation adds the two endpoint settings and their transport constraints.

The repaired shared branch includes USE_GEMINI, USE_VERTEX_AI and GATEWAY. Consequently GATEWAY receives the Gemini fallback under the implementation's non-Vertex branch, although the added documentation describes Gemini API-key and Vertex authentication. LOGIN_WITH_GOOGLE and COMPUTE_ADC use the separate code-assist constructor; fake-response handling also exits earlier.

## Call sites

- packages/core/src/core/contentGenerator.ts:119-175: createContentGeneratorConfig stores authType, baseUrl and customHeaders; credential-dependent branches may populate vertexai, leaving it absent otherwise.
- packages/core/src/core/contentGenerator.test.ts:657-661 and 690-694: added tests exercise configuration-builder-to-factory calls.
- packages/core/src/core/contentGenerator.test.ts:719-727: a direct sparse Vertex factory call omits vertexai and credentials while both fallback endpoint fixtures are present.
- packages/cli/src/test-utils/AppRig.tsx:307-324: the authentication-refresh test harness builds a direct factory input with authType, proxy and a synthetic/default API key but no vertexai or baseUrl.
- Available searches found no additional non-test callers beyond this harness and the function declarations. Production configuration and client source files were unavailable in the sparse checkout; exhaustive production call-site coverage is not claimed.

## Tests

- packages/core/src/core/contentGenerator.test.ts:642-705 asserts provider-specific fallback forwarding through normalized configuration for Gemini and Vertex.
- packages/core/src/core/contentGenerator.test.ts:707-738 asserts Vertex endpoint selection and vertexai true for a sparse direct caller with both fallback settings.
- packages/core/src/core/contentGenerator.test.ts:740-770 asserts explicit endpoint precedence over the Gemini fallback.
- packages/core/src/core/contentGenerator.test.ts:772-801 asserts forwarding http://127.0.0.1:8080.
- packages/core/src/core/contentGenerator.test.ts:803-827 asserts malformed explicit URL and remote HTTP rejection.
- packages/core/src/core/contentGenerator.test.ts:23-27 mocks the SDK and credential loader; 38-46 clears mock state and restores stubbed settings.
- Existing tests inspected around constructor expectations cover headers, API version and alternate generator paths; the selected diff changes eight undefined mode expectations to false.
- Observed validation: HEAD resolved to the pinned implementation, the selected parent resolved to c5ad0abb5de461416306a516ddbb26dc78f87d40, git status --short emitted no changes, and git diff --check for the selected comparison exited 0 without diagnostics.
- Not run: unit tests, integration tests, network requests, build, lint and type checks. node_modules and packages/core/package.json were absent; no dependencies were installed.
- packages/core/vitest.config.ts:9-23 defines the historical test runner, setup file, JUnit output and enabled coverage. This read-only extraction did not invoke that runner.
- All packaged evaluation cases are new definitions with status not_executed, not evidence of transfer success.

## Known limitations

The checkout is a sparse cached training source. The supplied issue bundle records missing discussion and review metadata. Real SDK/network behavior, credential flows and complete production callers were not verified. Historical tests do not cover all loopback names, arbitrary loopback schemes, malformed fallback settings, explicit false on a Vertex route, empty overrides or every alternate branch. Those gaps motivate proposed regression definitions rather than claims of observed execution. No holdouts, live credentials, user settings, environment values, prepared candidates or prior extraction transcripts were inspected. The source checkout was not modified.
<<<END FILE>>>
<<<FILE provider-endpoint-boundary-fcedf90eb77c/references/evidence/selected-diff.md>>>
# Selected implementation comparison

## Kind

diff

## Source

Local git comparison cb289e0724b46ce867b6d3fe4bd0ac6ed890dc45^1..cb289e0724b46ce867b6d3fe4bd0ac6ed890dc45; selected parent resolves to c5ad0abb5de461416306a516ddbb26dc78f87d40. Changed files: packages/core/src/core/contentGenerator.ts, packages/core/src/core/contentGenerator.test.ts and docs/reference/configuration.md.

## Observation

The inspected comparison adds the URL guard, route-selected fallback endpoint and nullish provider-mode default. It adds seven constructor tests and adjusts eight existing mode expectations. The three-file comparison contains 242 insertions and 11 deletions. There is one recorded parent, so no merge-parent separation was needed. This supports one coherent factory-boundary Workflow, not an independent cross-repository Pattern.
<<<END FILE>>>
<<<FILE provider-endpoint-boundary-fcedf90eb77c/references/evidence/endpoint-boundary.md>>>
# Shared factory endpoint precedence and branch scope

## Kind

implementation

## Source

Revision cb289e0724b46ce867b6d3fe4bd0ac6ed890dc45, packages/core/src/core/contentGenerator.ts:95-101, 119-175 and 258-320. Before-state: selected parent c5ad0abb5de461416306a516ddbb26dc78f87d40, same file:258-301.

## Observation

The configuration type exposes optional baseUrl and vertexai. The builder retains explicit baseUrl. The shared SDK branch includes Gemini, Vertex and Gateway routes; code-assist routes return through another constructor. At lines 291-311, config.baseUrl wins when truthy, otherwise authType selects one fallback setting; only a truthy result becomes httpOptions.baseUrl. Both selected explicit and fallback values invoke the guard. The SDK constructor retains headers and API version. The parent instead forwarded only config.baseUrl and did not explicitly select these fallback settings. Gateway follows the non-Vertex fallback branch; this is observed scope, not a universal provider policy.
<<<END FILE>>>
<<<FILE provider-endpoint-boundary-fcedf90eb77c/references/evidence/url-guard.md>>>
# URL parsing and transport guard

## Kind

implementation

## Source

Revision cb289e0724b46ce867b6d3fe4bd0ac6ed890dc45, packages/core/src/core/contentGenerator.ts:104-117 and 291-319.

## Observation

LOCAL_HOSTNAMES contains localhost, 127.0.0.1 and [::1]. validateBaseUrl constructs a URL and throws an invalid-custom-URL error on parse failure. It rejects when protocol is not https: and the parsed hostname is not in the exact allowlist. The selected override is guarded before GoogleGenAI construction. The predicate exempts any parseable protocol for the listed local hostnames; it does not guarantee HTTP-only loopback, DNS safety, redirect restrictions or service compatibility.
<<<END FILE>>>
<<<FILE provider-endpoint-boundary-fcedf90eb77c/references/evidence/provider-mode.md>>>
# Preserve explicit mode and default omitted mode

## Kind

implementation

## Source

Revision cb289e0724b46ce867b6d3fe4bd0ac6ed890dc45, packages/core/src/core/contentGenerator.ts:153-175 and 314-319; selected parent comparison at the SDK constructor.

## Observation

The builder infers vertexai in credential-dependent branches, while direct factory inputs can omit it. The SDK constructor changes from forwarding config.vertexai to a nullish fallback using whether authType is USE_VERTEX_AI. Explicit false therefore survives even on the Vertex route; omitted mode becomes true for Vertex and false for other routes in the shared branch. This explicit-false preservation is established by the expression, not an executed historical test. Endpoint fallback selection separately follows authType.
<<<END FILE>>>
<<<FILE provider-endpoint-boundary-fcedf90eb77c/references/evidence/callers.md>>>
# Normalized and direct factory entry paths

## Kind

call_site

## Source

Revision cb289e0724b46ce867b6d3fe4bd0ac6ed890dc45, packages/cli/src/test-utils/AppRig.tsx:307-324; packages/core/src/core/contentGenerator.test.ts:657-661, 690-694 and 719-727.

## Observation

The harness's refresh-auth stub invokes the factory with authType, proxy and an API-key fixture, omitting vertexai and baseUrl. Added tests also invoke the configuration builder before the factory, while the sparse Vertex test calls the factory directly with only authType. These observed entry paths support locating final resolution at the convergent factory rather than only in the builder. The sparse checkout lacks production configuration/client files, so complete production coverage remains unknown.
<<<END FILE>>>
<<<FILE provider-endpoint-boundary-fcedf90eb77c/references/evidence/constructor-tests.md>>>
# Historical constructor argument oracles

## Kind

test

## Source

Revision cb289e0724b46ce867b6d3fe4bd0ac6ed890dc45, packages/core/src/core/contentGenerator.test.ts:23-46 and 642-827; selected parent diff for existing vertexai expectations.

## Observation

The SDK is mocked and settings stubs are restored after tests. Added assertions check Gemini and Vertex fallback endpoints, sparse Vertex route selection with both fallbacks, explicit-over-fallback precedence, local HTTP acceptance, malformed explicit URL rejection and remote HTTP rejection. Eight existing expectations now require vertexai false rather than undefined. These are inspected test definitions, not passing execution results. Rejection tests assert thrown errors but do not explicitly assert zero constructor calls; that stronger check is proposed in the packaged evals.
<<<END FILE>>>
<<<FILE provider-endpoint-boundary-fcedf90eb77c/references/evidence/documented-contract.md>>>
# Documented custom endpoint constraints

## Kind

diff

## Source

Revision cb289e0724b46ce867b6d3fe4bd0ac6ed890dc45, docs/reference/configuration.md:2151-2165; selected comparison with parent c5ad0abb5de461416306a516ddbb26dc78f87d40.

## Observation

The added configuration entries describe Gemini API-key and Vertex endpoint overrides, require valid URLs, and state HTTPS with exceptions for localhost, 127.0.0.1 and [::1]. Documentation does not enumerate Gateway behavior or establish full SSRF protection. Its transport wording must be read with the implementation predicate, which has a hostname-based exception broader than HTTP alone.
<<<END FILE>>>
<<<FILE provider-endpoint-boundary-fcedf90eb77c/references/evidence/inspection-validation.md>>>
# Observed extraction checks and execution limits

## Kind

validation

## Source

Read-only local inspection of revision cb289e0724b46ce867b6d3fe4bd0ac6ed890dc45 and parent c5ad0abb5de461416306a516ddbb26dc78f87d40 on October 3, 2026; packages/core/vitest.config.ts:9-23; supplied issue-bundle.json limitations.

## Observation

git rev-parse HEAD returned the pinned revision. Parent resolution matched the supplied parent. git status --short emitted no changes. git diff --check on the selected comparison exited 0 without diagnostics. Existence checks found no node_modules and no packages/core/package.json. The runner configuration writes JUnit and coverage outputs, and the extraction environment is read-only. No tests, build, lint, type checks or network probes were run. The supplied bundle also states the sparse source has no installed dependencies or previously executed historical tests. These observations bound validation claims and do not establish package integrity or transfer success.
<<<END FILE>>>
<<<FILE provider-endpoint-boundary-fcedf90eb77c/references/provenance.json>>>
{
  "category": "provider-interface-adaptation",
  "holdout_used": false,
  "issue": 25357,
  "repository": "google-gemini/gemini-cli",
  "revision": "cb289e0724b46ce867b6d3fe4bd0ac6ed890dc45",
  "schema_version": "arex-direct-skill-provenance-v1",
  "source_episode_ids": [
    "github:google-gemini/gemini-cli#25357@cb289e0724b46ce867b6d3fe4bd0ac6ed890dc45"
  ],
  "source_key": "fcedf90eb77c",
  "split": "train_candidate",
  "source_workflow_id": "workflow:fcedf90eb77c:provider-endpoint-boundary-fcedf90eb77c",
  "package": {
    "name": "provider-endpoint-boundary-fcedf90eb77c",
    "skill_id": "workflow:fcedf90eb77c:provider-endpoint-boundary-fcedf90eb77c",
    "version": 1,
    "level": "workflow",
    "status": "candidate"
  }
}
<<<END FILE>>>
<<<FILE provider-endpoint-boundary-fcedf90eb77c/evals/activation-cases.json>>>
{
  "status": "not_executed",
  "cases": [
    {
      "id": "ignored-provider-fallback",
      "request": "Our shared model client factory ignores the selected provider's endpoint override. Explicit endpoints work, and we can inspect mocked SDK constructor arguments.",
      "expected": "activate",
      "rationale": "The endpoint translation boundary and a direct constructor oracle are identified."
    },
    {
      "id": "sparse-mode-default",
      "request": "A direct factory caller supplies a provider authentication route but omits the SDK mode flag. Normalized callers work. Repair the default without changing explicit false.",
      "expected": "activate",
      "rationale": "The sparse-input mode contract matches the factory adaptation procedure."
    },
    {
      "id": "ambiguous-proxy-report",
      "request": "The provider proxy is ignored. I do not know whether this means an HTTP proxy, custom API endpoint, or a separate login service.",
      "expected": "clarify",
      "rationale": "The semantic input and ownership boundary must be distinguished before activation."
    },
    {
      "id": "remote-outage",
      "request": "Constructor tracing shows the correct secure endpoint and mode, but the remote service returns unavailable errors. Add retries.",
      "expected": "do_not_activate",
      "rationale": "Remote availability and retry policy are outside this boundary repair."
    },
    {
      "id": "auth-rearchitecture",
      "request": "Replace all authentication methods with a new credential broker.",
      "expected": "do_not_activate",
      "rationale": "Authentication redesign is an explicit anti-goal."
    }
  ]
}
<<<END FILE>>>
<<<FILE provider-endpoint-boundary-fcedf90eb77c/evals/applicability-cases.json>>>
{
  "status": "not_executed",
  "cases": [
    {
      "id": "owned-convergent-factory",
      "request": "The checkout contains a shared SDK factory, normalized and direct callers, two route-specific fallback inputs, an explicit endpoint field, and a mocked-constructor test command. Explicit input must win and remote endpoints require secure transport.",
      "expected": "applicable",
      "rationale": "Ownership, precedence, route selection, transport policy and oracle are available."
    },
    {
      "id": "builder-only-evidence",
      "request": "Only the configuration-builder source and an issue title are available. The client factory, SDK options and tests are missing.",
      "expected": "insufficient",
      "rationale": "The actual consumption boundary and validation oracle cannot be established."
    },
    {
      "id": "unknown-loopback-policy",
      "request": "The factory and tests are available, but maintainers have not decided whether custom remote HTTP and non-HTTP loopback schemes are allowed.",
      "expected": "insufficient",
      "rationale": "Endpoint validation would invent a security policy without the required contract."
    },
    {
      "id": "separate-login-client",
      "request": "The failure occurs exclusively in the separate login-service client, which never enters the provider SDK factory.",
      "expected": "not_applicable",
      "rationale": "The owning implementation is outside the Workflow boundary."
    },
    {
      "id": "sdk-owned-endpoint-routing",
      "request": "The application cannot configure or intercept SDK construction; the vendor SDK alone owns endpoint resolution.",
      "expected": "not_applicable",
      "rationale": "The required editable boundary and constructor oracle are absent."
    },
    {
      "id": "dns-redirect-hardening",
      "request": "The endpoint already reaches the constructor. We need DNS rebinding prevention and validation after every redirect.",
      "expected": "not_applicable",
      "rationale": "The requested network-security policy exceeds the parse-and-transport guard supported here."
    }
  ]
}
<<<END FILE>>>
<<<FILE provider-endpoint-boundary-fcedf90eb77c/evals/functional-cases.json>>>
{
  "status": "not_executed",
  "cases": [
    {
      "id": "map-normalized-and-direct-paths",
      "action_id": "action:fcedf90eb77c:provider-endpoint-boundary-fcedf90eb77c:locate-contract",
      "setup": "Provide a synthetic repository with a configuration builder, shared SDK factory, separate login client, direct sparse caller and intercepted constructor. Supply base revision and focused test command.",
      "checks": [
        "The run-local map names the producer, shared factory, SDK constructor, alternate branch and direct caller using inspected source locators.",
        "The route matrix distinguishes explicit endpoint, route-specific fallback and absent override.",
        "The mode matrix distinguishes omitted mode from explicit false.",
        "No live settings, credentials or environment values are inspected.",
        "Missing production callers are recorded rather than fabricated."
      ]
    },
    {
      "id": "endpoint-precedence-and-isolation",
      "action_id": "action:fcedf90eb77c:provider-endpoint-boundary-fcedf90eb77c:resolve-endpoint",
      "setup": "In an authorized writable target, intercept the SDK constructor and use synthetic settings for route A and route B. Include normalized and direct inputs; restore all stubs after each case.",
      "checks": [
        "Run the caller-supplied focused command with explicit secure endpoint plus both fallbacks; constructor endpoint equals the explicit input.",
        "With no explicit endpoint and both fallbacks, each route forwards only its mapped endpoint.",
        "A sparse route-B input without credentials still selects route B's fallback.",
        "With no override, constructor HTTP options omit the endpoint property.",
        "A valid explicit endpoint with a malformed unused fallback still constructs using the explicit endpoint.",
        "Existing custom headers and API-version values are preserved.",
        "Separate login-client fixtures remain on their original constructor path."
      ]
    },
    {
      "id": "selected-url-policy",
      "action_id": "action:fcedf90eb77c:provider-endpoint-boundary-fcedf90eb77c:validate-endpoint",
      "setup": "Intercept construction and exercise explicit and fallback inputs under a declared remote-HTTPS policy with an exact loopback allowlist. Use only synthetic URLs. Declare separately whether local scheme exceptions are broad or HTTP-only.",
      "checks": [
        "Run focused fixtures for malformed selected explicit and fallback values; each reports a parse-validation error and zero SDK constructor calls.",
        "Remote plaintext endpoints fail transport validation before SDK construction.",
        "A secure remote endpoint is accepted and forwarded unchanged.",
        "Allowed local plaintext fixtures reach construction; test every declared loopback hostname.",
        "A remote hostname resembling a loopback name does not receive the exception.",
        "An invalid explicit endpoint is rejected even when the route fallback is valid.",
        "No override avoids URL parsing and preserves SDK defaults.",
        "For a historical-policy compatibility fixture, a parseable non-HTTPS URL on an allowlisted local hostname satisfies the guard; do not claim that the SDK supports its scheme.",
        "The result reports that DNS, redirect and remote-service safety were not established."
      ]
    },
    {
      "id": "nullish-mode-and-option-regressions",
      "action_id": "action:fcedf90eb77c:provider-endpoint-boundary-fcedf90eb77c:default-provider-mode",
      "setup": "Provide direct factory fixtures for routes whose omitted modes default to false and true, explicit booleans, synthetic endpoint overrides and neighboring option tests. Use a supplied runnable test command in the authorized target.",
      "checks": [
        "Omitted mode becomes false for the first route and true for the second route.",
        "Explicit false on the route with a true default remains false at construction.",
        "Explicit true remains true rather than being recomputed from the route.",
        "Endpoint fallback selection still follows the authentication route when explicit mode differs.",
        "Malformed selected endpoints still prevent constructor calls.",
        "Neighboring fixtures retain headers, API version, empty-key normalization and wrapper behavior.",
        "Run focused and neighboring commands when available and record actual outcomes; missing dependencies or source remain blockers, not passing results.",
        "No retry logic, credential acquisition or alternate authentication redesign is introduced."
      ]
    }
  ]
}
<<<END FILE>>>
AREX-SKILL-BUNDLE-END