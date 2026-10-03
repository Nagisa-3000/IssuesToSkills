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
