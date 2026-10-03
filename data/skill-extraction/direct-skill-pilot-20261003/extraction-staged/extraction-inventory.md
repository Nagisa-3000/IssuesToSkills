# Agent-core common-category extraction: actionable Workflow contract

## Summary

- Training cases: 1
- Evidence-validated ChangeEpisodes (legacy admitted count): 1
- Materialized candidate Skill Packages: 1
- Package-backed admitted candidate Episodes: 1
- Candidate Atomics: 4
- Candidate Workflows: 1
- Legacy schema-valid responses: 0
- Direct package extractions: 1
- Holdout leaks: 0

| Category | Episodes | Atomic | Workflow | Exact | Substitute | Holdout |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| provider-interface-adaptation | 1 | 4 | 1 | 0 | 1 | earendil-works/pi #5823 |

## Cases

### google-gemini/gemini-cli #25357

- Category: `provider-interface-adaptation`
- Episode: Historical provider endpoint repair
- Atomics: Default only an omitted provider mode; Locate the provider construction contract; Resolve the selected provider endpoint; Validate the effective endpoint before client construction
- Workflows: Repair provider endpoint construction
- When to use: A provider-specific endpoint setting exists but does not reach the SDK constructor.; Explicit configuration and provider-specific fallback settings compete at a shared client factory.; Direct factory callers omit a provider-mode flag and the selected authentication route must supply its default.; Constructor-level tests can observe the endpoint, mode and preserved request options.
- Anti-goals: Do not redesign authentication, acquire credentials, or inspect live user settings.; Do not replace proxy configuration with endpoint configuration.; Do not change SDK internals, retry behavior, model selection or response processing.; Do not infer a cross-repository Pattern from this single implementation.
