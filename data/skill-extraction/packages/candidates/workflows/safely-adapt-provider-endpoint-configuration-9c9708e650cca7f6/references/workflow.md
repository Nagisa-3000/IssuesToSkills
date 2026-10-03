# Safely route custom endpoints through a multi-provider SDK boundary

Workflow ID: `workflow:a1416952c048b7d5`

Episode ID: `google-gemini__gemini-cli__25357__cb289e0`

Historical repository: google-gemini/gemini-cli

Entry: The client-construction boundary knows the declared authentication type, but provider-specific endpoint environment variables are ignored, custom endpoints are not transport-validated, and SDK provider mode may be absent.

Exit: The SDK receives the highest-precedence endpoint associated with the declared provider and a consistent concrete provider mode; malformed and insecure remote endpoints fail before client construction.

1. [resolve-provider-endpoint-precedence](actions/770d8d94a05cc926.md) (`semantic-action:0615b3d0c1425572`); dependencies: none; condition: Run when constructing a provider SDK client for a supported direct-provider authentication branch.; oracle: Constructor-focused tests demonstrate provider-directed environment lookup, explicit precedence, and selection based on declared authentication type even without inferred credentials.

2. [guard-custom-endpoint-transport](actions/7284adaa9f1dfe4f.md) (`semantic-action:6b88c49d9fea9d8b`); dependencies: resolve-provider-endpoint-precedence; condition: Run only when endpoint resolution yields a non-empty custom endpoint.; oracle: Unit tests prove loopback HTTP acceptance and rejection of malformed or remote HTTP values.

3. [adapt-provider-sdk-options](actions/dc41ebb06392566f.md) (`semantic-action:4ebd6851e9c5c71f`); dependencies: resolve-provider-endpoint-precedence, guard-custom-endpoint-transport; condition: Run after an endpoint is admitted, or directly with no endpoint when resolution yields none; preserve an explicit provider-mode value when supplied.; oracle: Mocked constructor assertions prove accepted endpoint forwarding and concrete provider-mode reconciliation for both provider branches and existing non-cloud cases.

Typed edges (validates/repairs may be feedback, not ordering):
- step-1 -> step-2: enables
- step-1 -> step-3: enables
- step-2 -> step-3: requires
- step-3 -> step-1: validates
