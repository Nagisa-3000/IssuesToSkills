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
