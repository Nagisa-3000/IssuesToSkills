# Adapt a compatible provider across configuration, construction, and request boundaries

Workflow ID: `workflow:b5dccd8edcc90ddd`

Episode ID: `Aider-AI__aider__88__549a1a76`

Historical repository: Aider-AI/aider

Entry: The application can configure a key and base endpoint, but additional provider settings cannot flow through the interface; provider initialization is coupled to domain construction; and request dispatch omits provider-specific routing fields.

Exit: Supplied provider settings are applied before domain construction, the domain constructor is provider-independent, and request dispatch conditionally carries the provider's expected routing identifiers without changing the ordinary request path.

1. [centralize-provider-client-configuration](actions/0141bdec2f411dc2.md) (`semantic-action:f739bb2c7c9a9da7`); dependencies: none; condition: The compatible provider exposes additional client-level configuration values.; oracle: Verify each supplied interface value maps to the correct client attribute before component creation and that omitted optional values are not assigned.

2. [decouple-domain-construction-from-provider-credentials](actions/fe0e7e6bddb429ae.md) (`semantic-action:d803e48cee271d14`); dependencies: centralize-provider-client-configuration; condition: Provider initialization previously occurred inside the domain-component factory or constructor.; oracle: Verify production and direct test call sites construct the component without credential or endpoint arguments and retain existing behavior.

3. [adapt-provider-routing-at-request-dispatch](actions/ed4e15f2318b7422.md) (`semantic-action:00aaec027a328c3f`); dependencies: centralize-provider-client-configuration; condition: The provider requires deployment or engine routing fields on each request.; oracle: Capture the provider request call and verify configured routing fields are translated to deployment_id and engine, while absent fields remain absent.

Typed edges (validates/repairs may be feedback, not ordering):
- step-1 -> step-2: enables
- step-1 -> step-3: enables
- step-2 -> step-3: requires
