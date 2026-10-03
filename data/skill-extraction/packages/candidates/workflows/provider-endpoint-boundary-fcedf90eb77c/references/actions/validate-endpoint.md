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
