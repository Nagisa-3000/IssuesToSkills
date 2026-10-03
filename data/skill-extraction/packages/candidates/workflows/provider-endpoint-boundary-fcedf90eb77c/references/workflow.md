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
