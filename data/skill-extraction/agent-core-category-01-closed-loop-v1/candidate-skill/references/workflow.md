# Workflow for Define the provider contract before adapting its boundary

Portable roles are bound to real graph Actions in each training realization. The ids are evidence, not repository-independent patch recipes.

## Portable roles

### 1. Establish provider identity and precedence

- role_id: `establish-interface-contract`
- required: `true`
- condition: Use when multiple endpoint, provider, persisted-route, or configuration sources can influence the path, or when the affected endpoint must be distinguished from compatible alternatives.
- purpose: Define which observable signal selects the provider interface, which representation or configuration source is authoritative, and how explicit, current, legacy, and fallback values compose.
- validation: Exercise positive selection, competing-source precedence, absent and partial inputs, malformed inputs where applicable, and negative cases that must retain the existing provider path.

### 2. Adapt the boundary that owns the mismatch

- role_id: `adapt-contract-owner`
- required: `true`
- condition: Run after the provider identity and precedence contract is established and a specific consumer, constructor, or outbound adapter is shown to violate it.
- purpose: Make the consuming or construction boundary honor the established contract while preserving its local safety behavior and the behavior of unaffected paths.
- validation: Observe the boundary's output directly and prove that authoritative values are used, explicit or caller-authored values are preserved, and unrelated behavior remains unchanged.

### 3. Validate a selected custom endpoint

- role_id: `guard-selected-endpoint`
- required: `false`
- condition: Use only when this boundary accepts custom endpoint values and no lower layer already guarantees their parsing and transport policy.
- purpose: Reject malformed or insecure remote endpoint overrides before external client construction while preserving an evidence-backed local-development exception.
- validation: Prove acceptance of permitted secure and loopback forms and rejection of malformed or disallowed remote plaintext forms before SDK construction.

### 4. Translate provider routing at dispatch

- role_id: `translate-request-routing`
- required: `false`
- condition: Use only when successful dispatch requires per-request routing fields not represented by the common request shape.
- purpose: Map configured provider routing identifiers to the exact request keywords expected by the provider without changing requests when those identifiers are absent.
- validation: Capture the provider request call and assert exact key translation for configured identifiers and exact absence for unconfigured identifiers.

## Ordering constraints

- `establish-interface-contract` before `adapt-contract-owner`: Always establish identity, precedence, and preservation rules before changing the consuming boundary.
- `establish-interface-contract` before `guard-selected-endpoint`: Validate only the endpoint selected under the established precedence contract.
- `guard-selected-endpoint` before `adapt-contract-owner`: When the contract owner constructs an external client from a custom endpoint, admit or reject the endpoint before forwarding it to that client.
- `establish-interface-contract` before `translate-request-routing`: Add request routing fields only after their configuration ownership and provider applicability are established.

## Decision points

### What observable signal authoritatively identifies the provider interface?

- The boundary has an explicit declared authentication or provider mode. -> `establish-interface-contract`
- A configured endpoint has a stable canonical hostname and provider identity must be distinguished from compatible alternatives. -> `establish-interface-contract`
- The operation restores an existing session and an authoritative persisted runtime route can be identified. -> `establish-interface-contract`
- No evidence-backed interface signal is available. -> no additional role

### Which boundary owns the demonstrated mismatch?

- A consumer independently interprets persisted or layered route metadata. -> `adapt-contract-owner`
- Application or domain construction owns provider configuration that belongs at the composition boundary. -> `adapt-contract-owner`
- The external SDK constructor receives incomplete or inconsistent endpoint and provider-mode options. -> `adapt-contract-owner`
- The selected endpoint rejects a recognizable field synthesized by shared request construction. -> `adapt-contract-owner`

### Does the selected interface require additional conditional enforcement?

- A non-empty custom endpoint reaches this boundary and its transport safety is not already guaranteed. -> `guard-selected-endpoint`
- The provider requires deployment, engine, or equivalent routing identifiers on each request. -> `translate-request-routing`
- Neither custom-endpoint admission nor additional per-request routing is required. -> no additional role

## Concrete graph realizations

### NousResearch/hermes-agent — Align a resume interface with the authoritative persisted runtime route

- workflow_id: `workflow:7feccf0ac8bb22b3`
- `establish-interface-contract` -> `semantic-action:2d7c1bbc5fa9d6fa`
- `adapt-contract-owner` -> `semantic-action:743621ceda02ecdb`

### google-gemini/gemini-cli — Safely route custom endpoints through a multi-provider SDK boundary

- workflow_id: `workflow:a1416952c048b7d5`
- `establish-interface-contract` -> `semantic-action:0615b3d0c1425572`
- `guard-selected-endpoint` -> `semantic-action:6b88c49d9fea9d8b`
- `adapt-contract-owner` -> `semantic-action:4ebd6851e9c5c71f`

### Aider-AI/aider — Adapt a compatible provider across configuration, construction, and request boundaries

- workflow_id: `workflow:b5dccd8edcc90ddd`
- `establish-interface-contract` -> `semantic-action:f739bb2c7c9a9da7`
- `adapt-contract-owner` -> `semantic-action:d803e48cee271d14`
- `translate-request-routing` -> `semantic-action:00aaec027a328c3f`

### QwenLM/qwen-code — Adapt a shared request shape for a stricter compatible endpoint

- workflow_id: `workflow:da462de34604fc60`
- `establish-interface-contract` -> `semantic-action:4a8c6ad7fc7800b2`
- `adapt-contract-owner` -> `semantic-action:db94712551fe490e`
