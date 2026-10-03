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
