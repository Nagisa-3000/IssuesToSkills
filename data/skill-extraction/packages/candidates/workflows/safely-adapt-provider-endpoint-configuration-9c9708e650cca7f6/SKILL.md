---
name: safely-adapt-provider-endpoint-configuration-9c9708e650cca7f6
description: "A partial-order workflow for honoring explicit and environment-supplied endpoint overrides while preserving provider identity, transport safety, and existing client behavior. Use when A client supports multiple provider interfaces selected by an authentication or backend mode.; Callers need endpoint overrides through both an explicit configuration field and provider-specific environment variables.; The external SDK accepts endpoint and provider-mode options that must remain mutually consistent."
metadata:
  skill-id: "workflow:a1416952c048b7d5"
  level: workflow
  status: candidate
  version: 1
  category: "provider-interface-adaptation"
---

# Safely route custom endpoints through a multi-provider SDK boundary

## Purpose

Construct the external provider client with the intended custom endpoint and matching provider mode, while rejecting malformed or insecure remote overrides before any request can use them.

## When to use

- A client supports multiple provider interfaces selected by an authentication or backend mode.
- Callers need endpoint overrides through both an explicit configuration field and provider-specific environment variables.
- The external SDK accepts endpoint and provider-mode options that must remain mutually consistent.

## Do not use / Anti-goals

- Do not change authentication credential precedence or introduce new credential requirements.
- Do not apply these endpoint environment variables to unrelated authentication paths or alternate client implementations.
- Do not permit remote plaintext HTTP merely to maximize compatibility.
- Do not let an environment endpoint override a caller-supplied explicit endpoint.

Exclusions:
- The integration has only one provider interface and no competing endpoint sources.
- Endpoint selection and validation are already owned and guaranteed by a lower-level SDK contract.
- The target path does not construct the SDK client that consumes the custom endpoint.

## Applicability probes

- Does the current task satisfy this signal: A client supports multiple provider interfaces selected by an authentication or backend mode.
- Does the current task satisfy this signal: Callers need endpoint overrides through both an explicit configuration field and provider-specific environment variables.
- Does the current task satisfy this signal: The external SDK accepts endpoint and provider-mode options that must remain mutually consistent.
- Can the current checkout establish this entry state: The client-construction boundary knows the declared authentication type, but provider-specific endpoint environment variables are ignored, custom endpoints are not transport-validated, and SDK provider mode may be absent.
- Can a focused oracle observe the Action postconditions at their owning boundary?

## Preconditions

The client-construction boundary knows the declared authentication type, but provider-specific endpoint environment variables are ignored, custom endpoints are not transport-validated, and SDK provider mode may be absent.

Required runtime inputs:
- declared authentication/provider type
- optional explicit endpoint
- provider-specific environment endpoint values
- optional explicit SDK provider-mode value
- external SDK constructor contract

Map semantic owners and parameter slots to the current checkout before editing.

## Workflow

### Action 1 — Resolve a provider-specific endpoint with explicit configuration precedence

- Atomic ID: `semantic-action:0615b3d0c1425572`; [action contract](references/actions/770d8d94a05cc926.md).
- Owner: provider client option resolver.
- Object: declared_authentication_type, explicit_endpoint, primary_provider_environment_endpoint, cloud_provider_environment_endpoint.
- Operation: Select the endpoint candidate at the provider-client boundary: retain an explicit runtime endpoint when present; otherwise read the environment slot associated with the declared authentication interface.
- Preserve: At most one endpoint candidate is selected; explicit configuration wins, and an environment fallback is chosen according to the declared authentication type rather than inferred credentials.
- Required: true; condition: Run when constructing a provider SDK client for a supported direct-provider authentication branch..
- Depends on: no prior Action.
- Verify: Constructor-focused tests demonstrate provider-directed environment lookup, explicit precedence, and selection based on declared authentication type even without inferred credentials.

### Action 2 — Reject malformed or insecure remote custom endpoints

- Atomic ID: `semantic-action:6b88c49d9fea9d8b`; [action contract](references/actions/7284adaa9f1dfe4f.md).
- Owner: outbound endpoint policy guard.
- Object: selected_endpoint, allowed_loopback_hostnames, required_remote_protocol.
- Operation: Parse any selected custom endpoint and enforce encrypted transport for remote hosts while retaining an HTTP exception for local loopback development.
- Preserve: The endpoint is admitted only if it is parseable and uses HTTPS, except that named and numeric loopback hosts may use HTTP; rejected values fail before SDK construction.
- Required: true; condition: Run only when endpoint resolution yields a non-empty custom endpoint..
- Depends on: resolve-provider-endpoint-precedence.
- Verify: Unit tests prove loopback HTTP acceptance and rejection of malformed or remote HTTP values.

### Action 3 — Reconcile provider identity and forward accepted options to the SDK

- Atomic ID: `semantic-action:4ebd6851e9c5c71f`; [action contract](references/actions/dc41ebb06392566f.md).
- Owner: external provider SDK adapter.
- Object: accepted_endpoint, explicit_provider_mode, declared_authentication_type, sdk_http_options, sdk_provider_mode.
- Operation: Construct the provider SDK options with the validated endpoint and a concrete provider-mode flag, deriving the mode from the declared authentication interface when upstream credential inference left it unset.
- Preserve: The SDK receives the accepted endpoint in its HTTP options and a concrete provider-mode value that preserves an explicit setting or otherwise reflects the declared authentication interface.
- Required: true; condition: Run after an endpoint is admitted, or directly with no endpoint when resolution yields none; preserve an explicit provider-mode value when supplied..
- Depends on: resolve-provider-endpoint-precedence, guard-custom-endpoint-transport.
- Verify: Mocked constructor assertions prove accepted endpoint forwarding and concrete provider-mode reconciliation for both provider branches and existing non-cloud cases.

Completion invariant: The SDK receives the highest-precedence endpoint associated with the declared provider and a consistent concrete provider mode; malformed and insecure remote endpoints fail before client construction.

## Validation ladder

- Static diff check: confirm endpoint lookup is inside the intended SDK-construction branch and keyed by the declared authentication type.
- Focused unit checks: verify each provider environment endpoint is forwarded with the matching provider mode.
- Precedence check: set explicit and environment endpoints and verify the explicit value wins.
- Safety checks: verify loopback HTTP succeeds while malformed and remote HTTP endpoints fail before SDK construction.
- Regression checks: retain established constructor-option assertions, now with concrete non-cloud provider mode.
- Repository test execution: run the focused content-generator test file in an intact checkout; this remained deferred in the supplied staged-deletion worktree.

Report static/source, focused unit, regression, integration/request-boundary, and environment/backend results separately. Mark an unavailable level unverified; do not count an inspected test as an executed test.

## Failure modes

- retrieval_failure: selected package describes a different failure boundary.
- applicability_failure: entry state or exclusions disagree with the current task.
- composition_failure: Action dependencies or owner boundaries cannot be satisfied.
- action_failure: the direct oracle disproves an Action postcondition.
- stale_environment: the current implementation or SDK contract differs from evidence.
- missing_oracle: source inspection is available but executable validation is absent.

## Stop conditions

- Stop and defer if the declared provider cannot be determined at the client-construction boundary.
- Stop if no direct test seam can observe the external SDK constructor options or rejection behavior.
- Stop rather than broadening scope if endpoint support would require changing credential acquisition or unrelated authentication paths.
- Do not claim runtime validation success until the focused tests execute in an intact checkout.

## Evidence and provenance

Read [the workflow](references/workflow.md) for ordering and source identity. Read [provenance](references/provenance.json) and linked evidence cards only when inspecting historical support.

## Known limitations

- No PR body, review discussion, or status-check results were available in the GitHub evidence bundle.
- Focused tests were inspected but not executed because the supplied worktree contains staged deletions of all tracked files.
- The implementation includes [::1] in the hostname allowlist; WHATWG URL.hostname behavior for bracketed IPv6 was not separately exercised by the added tests.
- No cross-repository pattern is proposed from this single workflow.
- Did CI execute and pass the focused content-generator tests for cb289e0724b46ce867b6d3fe4bd0ac6ed890dc45? The evidence bundle omits status checks.
- Should the loopback policy include additional loopback representations or subdomains? The observed implementation and tests only establish localhost, 127.0.0.1, and an untested [::1] allowlist entry.
- The supplied checkout worktree is entirely staged as deleted; extraction therefore relied on immutable Git objects and did not alter or restore user state.
- Candidate package: compilation and structural validation do not prove cross-project transfer.
- Training oracles are recorded instructions; compilation does not execute them.
- Integration and environment/backend validation must be established in the current task.
