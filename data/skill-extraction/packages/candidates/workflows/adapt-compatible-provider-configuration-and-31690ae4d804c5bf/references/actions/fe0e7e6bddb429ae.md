# Remove provider credentials from domain-component construction

Atomic ID: `semantic-action:d803e48cee271d14`

Semantic owner: domain component construction boundary

Operation: reconcile

Object / parameter slots:
- domain component factory
- application entry-point call site
- direct test call sites

## Preconditions

Every direct component construction requires an API key and optionally a base URL, and construction mutates the global provider client.

## Action

Make domain-component creation independent of provider initialization after configuration ownership moves to the application boundary, then reconcile all direct construction call sites.

## Invariant

The component constructor requires only its domain inputs and no longer mutates provider configuration; direct call sites conform to that contract.

## Direct validation

Instantiate the component through the updated production and test call sites without provider credential arguments and run the existing constructor-dependent regression tests.

Step oracle: Verify production and direct test call sites construct the component without credential or endpoint arguments and retain existing behavior.

## Regression validation

- Static diff check: confirm the supported interface fields map to provider-client attributes and the domain constructor no longer owns provider initialization.
- Constructor regression check: run existing domain, command, and editing tests through the simplified construction contract.
- Request-unit check: mock the provider request method and assert routing-key presence and absence for configured and unconfigured cases.
- Configuration-path check: exercise command-line and configuration-file inputs to confirm equivalent normalized client state.
- Integration check: issue a minimal request against a configured compatible provider endpoint and confirm successful routing.

## Failure modes

Defer if the owner, precondition, or oracle differs. Classify a failed postcondition as action_failure; an unavailable oracle as missing_oracle.

## Not applicable when

- The provider is not compatible with the existing client and request/response protocol.
- The required adaptation changes authentication or transport semantics beyond client attributes and request keyword mapping.
- Provider configuration is intentionally isolated per component or per request and cannot safely use the shared client state evidenced here.

## Evidence

- [E5](../evidence/ef099fcece6eeca3.md)
- [E6](../evidence/b073b98568c2ff91.md)
- [E9](../evidence/2032ea400f77275b.md)
