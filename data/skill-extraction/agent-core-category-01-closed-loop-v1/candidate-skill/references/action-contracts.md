# Bound Action contracts

Locate each Action's semantic owner in the target checkout. Do not search for these ids or copy repository symbols into an unrelated project.

## adapt-provider-routing-at-request-dispatch

- action_id: `semantic-action:00aaec027a328c3f`
- role_ids: `translate-request-routing`
- workflow_ids: `workflow:b5dccd8edcc90ddd`
- supporting repositories: Aider-AI/aider
- module role: provider request adapter
- operation: `adapt`

**Pre-state:** Request dispatch sends the common chat-completion fields but cannot express provider-specific deployment or engine routing.

**Post-state:** Each request includes deployment_id and/or engine exactly when the corresponding configured client attributes exist, and otherwise retains the common request shape.

**Validation oracle:** Mock the provider request method and assert configured routing attributes appear under the provider's expected request keys, with separate assertions that absent attributes produce no extra keys.

**Parameters:**

- provider client module
- chat-completion request keyword map
- deployment identifier
- engine identifier

**Evidence ids:** `E7`, `E8`

## resolve-provider-endpoint-precedence

- action_id: `semantic-action:0615b3d0c1425572`
- role_ids: `establish-interface-contract`
- workflow_ids: `workflow:a1416952c048b7d5`
- supporting repositories: google-gemini/gemini-cli
- module role: provider client option resolver
- operation: `resolve`

**Pre-state:** Client configuration may contain an explicit endpoint, either provider-specific environment endpoint may be present, and the declared authentication type identifies the active interface.

**Post-state:** At most one endpoint candidate is selected; explicit configuration wins, and an environment fallback is chosen according to the declared authentication type rather than inferred credentials.

**Validation oracle:** Mock the external SDK constructor and assert both provider environment branches, both-environment disambiguation under an explicit authentication type, and explicit-over-environment precedence.

**Parameters:**

- declared_authentication_type
- explicit_endpoint
- primary_provider_environment_endpoint
- cloud_provider_environment_endpoint

**Evidence ids:** `ev-impl-01`, `ev-test-01`, `ev-test-02`, `ev-test-03`

## reconcile-partial-persisted-route-fallback

- action_id: `semantic-action:2d7c1bbc5fa9d6fa`
- role_ids: `establish-interface-contract`
- workflow_ids: `workflow:7feccf0ac8bb22b3`
- supporting repositories: NousResearch/hermes-agent
- module role: canonical persisted-runtime route resolver
- operation: `reconcile`

**Pre-state:** A session row may contain a provider-bearing nested runtime snapshot, partial top-level route fields, a routable billing provider, a bare non-routable billing bucket, malformed configuration, or combinations of these states.

**Post-state:** A provider-bearing nested runtime route wins; otherwise top-level route fields are retained and a routable billing provider fills only an absent provider; bare billing buckets and malformed metadata do not create a provider override.

**Validation oracle:** Exercise nested precedence, partial top-level fallback, malformed metadata, routable billing fallback, bare-bucket rejection, and explicit-provider precedence through the canonical reader tests.

**Parameters:**

- session metadata row
- nested runtime route
- top-level provider
- top-level endpoint
- top-level API mode
- billing provider
- set of non-routable billing buckets

**Evidence ids:** `E3`, `E4`, `E10`, `E11`

## route_endpoint_by_canonical_hostname

- action_id: `semantic-action:4a8c6ad7fc7800b2`
- role_ids: `establish-interface-contract`
- workflow_ids: `workflow:da462de34604fc60`
- supporting repositories: QwenLM/qwen-code
- module role: provider selection boundary
- operation: `route`

**Pre-state:** A configured OpenAI-compatible base URL would otherwise fall through to the generic provider, and the served model name is not sufficient evidence of the endpoint implementation.

**Post-state:** The canonical endpoint hostname and its subdomains select the dedicated adapter; unrelated, malformed, and suffix-confusable hosts do not.

**Validation oracle:** Exercise canonical-host, subdomain, hostile-suffix, and unrelated-host cases and assert the resulting request behavior identifies the selected provider path.

**Parameters:**

- configured base URL
- canonical endpoint hostname
- provider configuration
- generic-provider fallback

**Evidence ids:** `E4`, `E5`, `E8`

## adapt-provider-sdk-options

- action_id: `semantic-action:4ebd6851e9c5c71f`
- role_ids: `adapt-contract-owner`
- workflow_ids: `workflow:a1416952c048b7d5`
- supporting repositories: google-gemini/gemini-cli
- module role: external provider SDK adapter
- operation: `adapt`

**Pre-state:** Endpoint resolution and admission have completed, while the SDK provider-mode field may be explicitly set or absent despite a declared authentication type.

**Post-state:** The SDK receives the accepted endpoint in its HTTP options and a concrete provider-mode value that preserves an explicit setting or otherwise reflects the declared authentication interface.

**Validation oracle:** Inspect the mocked SDK constructor for endpoint forwarding and correct true/false provider-mode values, including the branch with declared cloud authentication but no inferred credentials and established non-cloud scenarios.

**Parameters:**

- accepted_endpoint
- explicit_provider_mode
- declared_authentication_type
- sdk_http_options
- sdk_provider_mode

**Evidence ids:** `ev-call-01`, `ev-impl-02`, `ev-test-01`, `ev-test-02`, `ev-test-05`

## guard-custom-endpoint-transport

- action_id: `semantic-action:6b88c49d9fea9d8b`
- role_ids: `guard-selected-endpoint`
- workflow_ids: `workflow:a1416952c048b7d5`
- supporting repositories: google-gemini/gemini-cli
- module role: outbound endpoint policy guard
- operation: `guard`

**Pre-state:** A non-empty explicit or environment-derived custom endpoint has been selected but has not yet been admitted to outbound client options.

**Post-state:** The endpoint is admitted only if it is parseable and uses HTTPS, except that named and numeric loopback hosts may use HTTP; rejected values fail before SDK construction.

**Validation oracle:** Assert acceptance of an HTTP loopback URL and rejection of both an unparsable string and an HTTP remote URL with the expected error classes/messages.

**Parameters:**

- selected_endpoint
- allowed_loopback_hostnames
- required_remote_protocol

**Evidence ids:** `ev-diff-01`, `ev-test-04`

## delegate-resume-route-selection-to-canonical-reader

- action_id: `semantic-action:743621ceda02ecdb`
- role_ids: `adapt-contract-owner`
- workflow_ids: `workflow:7feccf0ac8bb22b3`
- supporting repositories: NousResearch/hermes-agent
- module role: client-session resume adapter
- operation: `adapt`

**Pre-state:** The resume adapter independently reads only top-level route fields and billing metadata, while another execution path persists the latest route in a nested runtime snapshot and another resume consumer already uses the canonical resolver.

**Post-state:** The resume adapter obtains provider, endpoint, and API mode through the canonical resolver, then applies its existing endpoint-ownership checks, provider healing, and override construction.

**Validation oracle:** Assert that resume selects nested runtime data over a stale first-call billing provider and over stale top-level route keys, and compare the restored route with the existing CLI resume consumer.

**Parameters:**

- session metadata row
- canonical route resolver
- resumed model
- provider override
- endpoint override
- API-mode override

**Evidence ids:** `E2`, `E5`, `E6`, `E7`, `E8`, `E9`

## decouple-domain-construction-from-provider-credentials

- action_id: `semantic-action:d803e48cee271d14`
- role_ids: `adapt-contract-owner`
- workflow_ids: `workflow:b5dccd8edcc90ddd`
- supporting repositories: Aider-AI/aider
- module role: domain component construction boundary
- operation: `reconcile`

**Pre-state:** Every direct component construction requires an API key and optionally a base URL, and construction mutates the global provider client.

**Post-state:** The component constructor requires only its domain inputs and no longer mutates provider configuration; direct call sites conform to that contract.

**Validation oracle:** Instantiate the component through the updated production and test call sites without provider credential arguments and run the existing constructor-dependent regression tests.

**Parameters:**

- domain component factory
- application entry-point call site
- direct test call sites

**Evidence ids:** `E5`, `E6`, `E9`

## remove_only_derived_incompatible_field

- action_id: `semantic-action:db94712551fe490e`
- role_ids: `adapt-contract-owner`
- workflow_ids: `workflow:da462de34604fc60`
- supporting repositories: QwenLM/qwen-code
- module role: outbound request compatibility adapter
- operation: `reconcile`

**Pre-state:** Shared request construction has produced assistant messages where a derived field may equal its source field, but the selected endpoint rejects the derived field during multi-turn replay.

**Post-state:** Outbound assistant messages omit the derived field only when it is the recognizable string copy of the source field; the source field, distinct explicit values, non-assistant messages, and original history remain intact.

**Validation oracle:** Assert field-level behavior for equal and distinct values and run a multi-turn generator request against a strict endpoint that rejects the incompatible field, inspecting the accepted wire body.

**Parameters:**

- provider-built request
- assistant message role
- source reasoning field
- derived reasoning field
- endpoint field contract

**Evidence ids:** `E2`, `E3`, `E6`, `E7`, `E8`, `E9`

## centralize-provider-client-configuration

- action_id: `semantic-action:f739bb2c7c9a9da7`
- role_ids: `establish-interface-contract`
- workflow_ids: `workflow:b5dccd8edcc90ddd`
- supporting repositories: Aider-AI/aider
- module role: application composition and provider-client configuration boundary
- operation: `normalize`

**Pre-state:** The application accepts only key and base settings, while the domain component constructor owns provider-module initialization and forces a default base value.

**Post-state:** The application boundary accepts the supported optional provider settings and initializes the shared provider client before constructing downstream components; omitted optional settings are not overwritten.

**Validation oracle:** Parse representative provider arguments or configuration fields and verify the corresponding provider-client attributes are set before domain-component construction, while omitted values remain untouched.

**Parameters:**

- credential
- endpoint base
- provider API type
- provider API version
- deployment identifier
- engine identifier
- provider client module

**Evidence ids:** `E2`, `E3`, `E4`, `E5`, `E10`
