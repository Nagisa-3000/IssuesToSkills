# Validation and promotion gates

## Validation ladder

1. Focused contract checks: test provider selection and precedence using explicit, fallback, partial, absent, malformed, and confusable inputs relevant to the selected identity signal.
2. Focused boundary checks: directly inspect the canonical resolver result, component constructor contract, SDK constructor options, or emitted request fields and verify exact preservation and omission rules.
3. Integration checks: exercise the real consumer-to-boundary path, such as session resume, application configuration through construction, SDK creation, or multi-turn HTTP request conversion.
4. Regression checks: run existing tests for unaffected providers, ordinary requests, legacy persisted data, endpoint ownership, provider healing, established constructor options, and caller-authored field preservation.
5. Environment-complete verification: execute the focused repository test suite in an intact checkout with required dependencies; do not substitute static inspection for successful runtime validation.

## Known failure modes

### Provider identity is inferred from a model name or unsafe hostname substring.

- Detection: A similarly named, suffix-confusable, or unrelated endpoint selects the specialized path.
- Mitigation: Use declared interface mode, authoritative persisted route data, or parsed canonical hostname boundaries with explicit negative cases.

### A fallback overrides an explicit or fresher value.

- Detection: Tests with both explicit and fallback sources select the fallback, or stale metadata replaces a newer nested route.
- Mitigation: Encode precedence explicitly and use fallbacks only to fill missing fields.

### The adaptation broadens to unaffected providers or ordinary requests.

- Detection: Optional fields appear when unconfigured, unrelated hosts select the adapter, or established request snapshots change.
- Mitigation: Gate the adaptation on the established provider contract and assert negative and absence cases.

### A caller-authored value is mistaken for a synthesized compatibility value.

- Detection: Distinct explicit fields are removed or persisted source history is mutated.
- Mitigation: Require an evidence-backed invariant that identifies the synthesized value and transform only the outbound copy at its owning boundary.

### An endpoint and provider-mode combination becomes inconsistent.

- Detection: The external constructor receives an endpoint associated with one interface and a mode associated with another.
- Mitigation: Derive both from the same established interface contract while preserving any valid explicit mode.

### Static inspection is reported as completed runtime validation.

- Detection: Focused tests were unavailable, dependencies were missing, or the checkout was incomplete.
- Mitigation: Record the execution gap and keep the pattern pending until an untouched holdout repair and environment-complete test run succeed.

## Exclusions

- Credential acquisition or credential-precedence changes.
- Provider integrations requiring a different request or response protocol.
- Prompting, edit-format, retry-policy, or response-processing redesign.
- Raw credential persistence or restoration as part of route reconciliation.
- Global removal of a shared compatibility field accepted or required by other endpoints.
- Remote plaintext HTTP enablement for compatibility.
- Repository-specific endpoint guards, resume repairs, constructor changes, or request fields unless their stated conditions apply.

## Current package gate

- package status: `candidate`
- promotion status: `candidate_pending_independent_holdouts`
- repository-disjoint holdout: `True`
- oracle qualified: `True`
- paired agent evaluation: `pass_directional`
- retrieval evaluation: `recorded`

Retrieval success and a discriminating oracle do not promote this Skill. Promotion requires a leakage-audited paired agent run and independent weighted evaluation.
