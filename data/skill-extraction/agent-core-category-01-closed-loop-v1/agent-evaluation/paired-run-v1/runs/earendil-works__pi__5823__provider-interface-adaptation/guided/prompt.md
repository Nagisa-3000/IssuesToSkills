You are solving a held-out implementation task in repository earendil-works/pi.
The workspace is a synthetic snapshot based on the pre-change parent and has no future Git history. The original solution commit is not available. Work only in this workspace; do not search external services or other repositories. Do not edit the visible regression tests. Inspect the current code, implement the behavior, and run focused tests before finishing.

# Problem family
provider interface adaptation

# Issue/task
--model provider/model ignores provider when model ID exists on multiple providers

## Description

When the same model ID (e.g. `gemma-4-12b`) is configured on multiple providers, `--model provider-b/gemma-4-12b` ignores the explicit provider and uses the default provider instead.

## Steps to reproduce

1. Configure two providers in `auth.json` with the same model ID available on both
2. Set one as the default provider
3. Run `pi --model provider-b/model-name -p "test"`
4. Observe that provider-a (the default) is used instead of provider-b

## Expected behavior

`--model provider/model` should honor the provider part of the specification, even when the model ID exists on the default provider.

## Workaround

Give each provider a unique model ID (e.g. `gemma-4-12b-200k` vs `gemma-4-12b-128k`).

## Impact

Breaks fleet setups where the same model runs on different hardware with different context sizes. The orchestrator and subagents need different providers but share a model name.

# Visible regression tests retained for this evaluation
- packages/coding-agent/test/model-resolver-provider-precedence.holdout.test.ts

# Validation commands
- `env PATH=/home/chenyujia/.local/node22/bin:/usr/bin:/bin npm --prefix packages/coding-agent test -- 'test/model-resolver-provider-precedence.holdout.test.ts'`
- `git diff --check HEAD`

# Arm
guided

# Retrieved Skill Graph guidance
The following are hypotheses retrieved only from the training repositories using lexical/vector retrieval, optional HNSW, and typed graph expansion. Verify every step against the current code and tests; do not copy repository-specific names blindly.

## Retrieved node 1: pattern — Define the provider contract before adapting its boundary
id: pattern:5895d079305884e4
repository: -
score: 0.097228
sources: {"graph": 0.06545014339961053, "lexical": 0.015384615384615385, "lexical_raw": 2.014966340901896, "vector": 0.01639344262295082, "vector_raw": 0.25005194925736013}

When a compatible provider path fails because configuration, persisted routing, client construction, or request shape disagrees with the actual provider interface, first establish an evidence-backed identity, precedence, and field-preservation contract. Then adapt only the boundary that violates that contract, adding transport or request-routing behavior only when the selected interface requires it.

facets:
{"problem_class": "provider-interface-adaptation", "promotion_status": "candidate_pending_holdout"}

payload:
{"action_template": [{"condition": "Use when multiple endpoint, provider, persisted-route, or configuration sources can influence the path, or when the affected endpoint must be distinguished from compatible alternatives.", "purpose": "Define which observable signal selects the provider interface, which representation or configuration source is authoritative, and how explicit, current, legacy, and fallback values compose.", "required": true, "role_id": "establish-interface-contract", "title": "Establish provider identity and precedence", "validation": "Exercise positive selection, competing-source precedence, absent and partial inputs, malformed inputs where applicable, and negative cases that must retain the existing provider path."}, {"condition": "Run after the provider identity and precedence contract is established and a specific consumer, constructor, or outbound adapter is shown to violate it.", "purpose": "Make the consuming or construction boundary honor the established contract while preserving its local safety behavior and the behavior of unaffected paths.", "required": true, "role_id": "adapt-contract-owner", "title": "Adapt the boundary that owns the mismatch", "validation": "Observe the boundary's output directly and prove that authoritative values are used, explicit or caller-authored values are preserved, and unrelated behavior remains unchanged."}, {"condition": "Use only when this boundary accepts custom endpoint values and no lower layer already guarantees their parsing and transport policy.", "purpose": "Reject malformed or insecure remote endpoint overrides before external client construction while preserving an evidence-backed local-development exception.", "required": false, "role_id": "guard-selected-endpoint", "title": "Validate a selected custom endpoint", "validation": "Prove acceptance of permitted secure and loopback forms and rejection of malformed or disallowed remote plaintext forms before SDK construction."}, {"condition": "Use only when successful dispatch requires per-request routing fields not represented by the common request shape.", "purpose": "Map configured provider routing identifiers to the exact request keywords expected by the provider without changing requests when those identifiers are absent.", "required": false, "role_id": "translate-request-routing", "title": "Translate provider routing at dispatch", "validation": "Capture the provider request call and assert exact key translation for configured identifiers and exact absence for unconfigured identifiers."}], "anti_goals": ["Do not redesign authentication, prompting, response processing, retry behavior, or unrelated provider paths.", "Do not infer provider identity from model-family names when endpoint, authentication mode, or persisted route evidence is available.", "Do not overwrite explicit configuration with defaults, environment values, historical metadata, or synthesized fields.", "Do not add absent optional settings or provider-specific request fields to the ordinary request path.", "Do not mutate caller-owned or persisted conversation data merely to change the outbound wire representation.", "Do not treat distinct Actions as interchangeable merely because they occupy the same workflow role."], "decision_points": [{"branches": [{"action_role_ids": ["establish-interface-contract"], "condition": "The boundary has an explicit declared authentication or provider mode."}, {"action_role_ids": ["establish-interface-contract"], "condition": "A configured endpoint has a stable canonical hostname and provider identity must be distinguished from compatible alternatives."}, {"action_role_ids": ["establish-interface-contract"], "condition": "The operation restores an existing session and an authoritative persisted runtime route can be identified."}, {"action_role_ids": [], "condition": "No evidence-backed interface signal is available."}], "question": "What observable signal authoritatively identifies the provider interface?"}, {"branches": [{"action_role_ids": ["adapt-contract-owner"], "condition": "A consumer independently interprets persisted or layered route metadata."}, {"action_role_ids": ["adapt-contract-owner"], "condition": "Application or domain construction owns provider configuration that belongs at the composition boundary."}, {"action_role_ids": ["adapt-contract-owner"], "condition": "The external SDK constructor receives incomplete or inconsistent endpoint and provider-mode options."}, {"action_role_ids": ["adapt-contract-owner"], "condition": "The selected endpoint rejects a recognizable field synthesized by shared request construction."}], "question": "Which boundary owns the demonstrated mismatch?"}, {"branches": [{"action_role_ids": ["guard-selected-endpoint"], "condition": "A non-empty custom endpoint reaches this boundary and its transport safety is not already guaranteed."}, {"action_role_ids": ["translate-request-routing"], "condition": "The provider requires deployment, engine, or equivalent routing identifiers on each request."}, {"action_role_ids": [], "condition": "Neither custom-endpoint admission nor additional per-request routing is required."}], "question": "Does the selected interface require additional conditional enforcement?"}], "exclusions": ["Credential acquisition or credential-precedence changes.", "Provider integrations requiring a different request or response protocol.", "Prompting, edit-format, retry-policy, or response-processing redesign.", "Raw credential persistence or restoration as part of route reconciliation.", "Global removal of a shared compatibility field accepted or required by other endpoints.", "Remote plaintext HTTP enablement for compatibility.", "Repository-specific endpoint guards, resume repairs, constructor changes, or request fields unless their stated conditions apply."], "invariants": ["Explicit current configuration takes precedence over fallback environment or historical values unless the established interface contract says otherwise.", "A fallback fills only information that is absent; it does not replace a newer, more specific, or explicitly supplied value.", "Provider identity is derived from the strongest available interface signal, such as declared authentication mode, canonical parsed hostname, or the authoritative persisted route.", "Adaptation occurs at the narrowest boundary that owns the mismatched representation.", "Unconfigured optional values remain absent from client options and outbound requests.", "Unaffected providers, endpoints, consumers, and request shapes retain their existing behavior.", "Each realization preserves the pre-state, post-state, and validation oracle of its bound Action."], "known_failure_modes": [{"detection": "A similarly named, suffix-confusable, or unrelated endpoint selects the specialized path.", "failure": "Provider identity is inferred from a model name or unsafe hostname substring.", "mitigation": "Use declared interface mode, authoritative persisted route data, or parsed canonical hostname boundaries with explicit negative cases."}, {"detection": "Tests with both explicit and fallback sources select the fallback, or stale metadata replaces a newer nested route.", "failure": "A fallback overrides an explicit or fresher value.", "mitigation": "Encode precedence explicitly and use fallbacks only to fill missing fields."}, {"detection": "Optional fields appear when unconfigured, unrelated hosts select the adapter, or established request snapshots change.", "failure": "The adaptation broadens to unaffected providers or ordinary requests.", "mitigation": "Gate the adaptation on the established provider contract and assert negative and absence cases."}, {"detection": "Distinct explicit fields are removed or persisted source history is mutated.", "failure": "A caller-authored value is mistaken for a synthesized compatibility value.", "mitigation": "Require an evidence-backed invariant that identifies the synthesized value and transform only the outbound copy at its owning boundary."}, {"detection": "The external constructor receives an endpoint associated with one interface and a mode associated with another.", "failure": "An endpoint and provider-mode combination becomes inconsistent.", "mitigation": "Derive both from the same established interface contract while preserving any valid explicit mode."}, {"detection": "Focused tests were unavailable, dependencies were missing, or the checkout was incomplete.", "failure": "Static inspection is reported as completed runtime validation.", "mitigation": "Record the execution gap and keep the pattern pending until an untouched holdout repair and environment-complete test run succeed."}], "missing_probes": ["Apply the required role sequence to a separate untouched repository repair and verify that the role boundaries can be instantiated without reusing or weakening any training Action contract.", "Execute focused and regression tests in dependency-complete, intact checkouts for training workflows whose tests were only inspected.", "Confirm in the holdout that negative provider-selection and optional-field-absence cases remain unchanged after the adaptation."], "not_applicable_when": ["The target provider is not compatible with the existing request and response protocol.", "There is no evidence-backed way to identify the selected provider interface or determine precedence among competing route sources.", "The failure belongs to credential acquisition, initial provider discovery, response interpretation, or another subsystem rather than an interface boundary.", "Different consumers intentionally implement different routing semantics rather than alternate paths to the same provider contract.", "A lower-level SDK already owns and guarantees endpoint selection, validation, and request adaptation for the affected path."], "ordering_constraints": [{"after_role_id": "adapt-contract-owner", "before_role_id": "establish-interface-contract", "condition": "Always establish identity, precedence, and preservation rules before changing the consuming boundary."}, {"after_role_id": "guard-selected-endpoint", "before_role_id": "establish-interface-contract", "condition": "Validate only the endpoint selected under the established precedence contract."}, {"after_role_id": "adapt-contract-owner", "before_role_id": "guard-selected-endpoint", "condition": "When the contract owner constructs an external client from a custom endpoint, admit or reject the endpoint before forwarding it to that client."}, {"after_role_id": "translate-request-routing", "before_role_id": "establish-interface-contract", "condition": "Add request routing fields only after their configuration ownership and provider applicability are established."}], "supporting_workflows": ["workflow:7feccf0ac8bb22b3", "workflow:a1416952c048b7d5", "workflow:b5dccd8edcc90ddd", "workflow:da462de34604fc60"], "validation_ladder": ["Focused contract checks: test provider selection and precedence using explicit, fallback, partial, absent, malformed, and confusable inputs relevant to the selected identity signal.", "Focused boundary checks: directly inspect the canonical resolver result, component constructor contract, SDK constructor options, or emitted request fields and verify exact preservation and omission rules.", "Integration checks: exercise the real consumer-to-boundary path, such as session resume, application configuration through construction, SDK creation, or multi-turn HTTP request conversion.", "Regression checks: run existing tests for unaffected providers, ordinary requests, legacy persisted data, endpoint ownership, provider healing, established constructor options, and caller-authored field preservation.", "Environment-complete verification: execute the focused repository test suite in an intact checkout with required dependencies; do not substitute static inspection for successful runtime validation."], "when_to_use": ["A provider-compatible path reaches the wrong endpoint, restores stale routing metadata, omits required routing arguments, or emits a field rejected by the selected endpoint.", "Multiple representations or configuration sources can identify the provider route, and their precedence is currently implicit or inconsistent.", "A shared implementation mostly satisfies the provider protocol, but a narrow client-construction, resume, or outbound-request boundary has a documented mismatch.", "The affected interface can be identified from observable configuration, persisted route data, or parsed endpoint identity rather than model-name guesses."], "workflow_realizations": [{"evidence_ids": ["E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9", "E10", "E11", "E12"], "repository": "NousResearch/hermes-agent", "role_bindings": [{"action_ids": ["semantic-action:2d7c1bbc5fa9d6fa"], "role_id": "establish-interface-contract"}, {"action_ids": ["semantic-action:743621ceda02ecdb"], "role_id": "adapt-contract-owner"}], "workflow_id": "workflow:7feccf0ac8bb22b3"}, {"evidence_ids": ["ev-before-01", "ev-diff-01", "ev-impl-01", "ev-call-01", "ev-impl-02", "ev-test-01", "ev-test-02", "ev-test-03", "ev-test-04", "ev-test-05"], "repository": "google-gemini/gemini-cli", "role_bindings": [{"action_ids": ["semantic-action:0615b3d0c1425572"], "role_id": "establish-interface-contract"}, {"action_ids": ["semantic-action:6b88c49d9fea9d8b"], "role_id": "guard-selected-endpoint"}, {"action_ids": ["semantic-action:4ebd6851e9c5c71f"], "role_id": "adapt-contract-owner"}], "workflow_id": "workflow:a1416952c048b7d5"}, {"evidence_ids": ["E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9", "E10", "E11"], "repository": "Aider-AI/aider", "role_bindings": [{"action_ids": ["semantic-action:f739bb2c7c9a9da7"], "role_id": "establish-interface-contract"}, {"action_ids": ["semantic-action:d803e48cee271d14"], "role_id": "adapt-contract-owner"}, {"action_ids": ["semantic-action:00aaec027a328c3f"], "role_id": "translate-request-routing"}], "workflow_id": "workflow:b5dccd8edcc90ddd"}, {"evidence_ids": ["E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9"], "repository": "QwenLM/qwen-code", "role_bindings": [{"action_ids": ["semantic-action:4a8c6ad7fc7800b2"], "role_id": "establish-interface-contract"}, {"action_ids": ["semantic-action:db94712551fe490e"], "role_id": "adapt-contract-owner"}], "workflow_id": "workflow:da462de34604fc60"}]}

retrieval trace:
- pattern-step:7ba496512e7154ba35269fe2 --declares_step/in--> pattern:5895d079305884e4
- pattern-step:c330478719afed1e40edb9fc --declares_step/in--> pattern:5895d079305884e4
- pattern-step:44d984675ad90d2d42394568 --declares_step/in--> pattern:5895d079305884e4
- workflow:a1416952c048b7d5 --instantiates/out--> pattern:5895d079305884e4
- workflow:a1416952c048b7d5 --supported_by/in--> pattern:5895d079305884e4
- workflow:7feccf0ac8bb22b3 --instantiates/out--> pattern:5895d079305884e4
- workflow:7feccf0ac8bb22b3 --supported_by/in--> pattern:5895d079305884e4
- pattern-step:2d7dbe2bd44671512a8d628d --declares_step/in--> pattern:5895d079305884e4
- workflow:b5dccd8edcc90ddd --instantiates/out--> pattern:5895d079305884e4
- workflow:b5dccd8edcc90ddd --supported_by/in--> pattern:5895d079305884e4
- workflow:da462de34604fc60 --instantiates/out--> pattern:5895d079305884e4
- workflow:da462de34604fc60 --supported_by/in--> pattern:5895d079305884e4

## Retrieved node 2: workflow — safely-adapt-provider-endpoint-configuration
id: workflow:a1416952c048b7d5
repository: google-gemini/gemini-cli
score: 0.056854
sources: {"graph": 0.0285302925943558, "lexical": 0.012195121951219513, "lexical_raw": 5.270595697591347e-06, "vector": 0.016129032258064516, "vector_raw": 0.2485146922229839}

A partial-order workflow for honoring explicit and environment-supplied endpoint overrides while preserving provider identity, transport safety, and existing client behavior.

facets:
{"entry_state": "The client-construction boundary knows the declared authentication type, but provider-specific endpoint environment variables are ignored, custom endpoints are not transport-validated, and SDK provider mode may be absent.", "exit_state": "The SDK receives the highest-precedence endpoint associated with the declared provider and a consistent concrete provider mode; malformed and insecure remote endpoints fail before client construction.", "problem_class": "provider-interface-adaptation"}

payload:
{"anti_goals": ["Do not change authentication credential precedence or introduce new credential requirements.", "Do not apply these endpoint environment variables to unrelated authentication paths or alternate client implementations.", "Do not permit remote plaintext HTTP merely to maximize compatibility.", "Do not let an environment endpoint override a caller-supplied explicit endpoint."], "entry_state": "The client-construction boundary knows the declared authentication type, but provider-specific endpoint environment variables are ignored, custom endpoints are not transport-validated, and SDK provider mode may be absent.", "exit_state": "The SDK receives the highest-precedence endpoint associated with the declared provider and a consistent concrete provider mode; malformed and insecure remote endpoints fail before client construction.", "goal": "Construct the external provider client with the intended custom endpoint and matching provider mode, while rejecting malformed or insecure remote overrides before any request can use them.", "not_applicable_when": ["The integration has only one provider interface and no competing endpoint sources.", "Endpoint selection and validation are already owned and guaranteed by a lower-level SDK contract.", "The target path does not construct the SDK client that consumes the custom endpoint."], "steps": [{"action_id": "semantic-action:0615b3d0c1425572", "action_name": "resolve-provider-endpoint-precedence", "condition": "Run when constructing a provider SDK client for a supported direct-provider authentication branch.", "depends_on": [], "optional": false, "required": true, "role": "establish-contract", "step_id": "step-1", "validation": "Constructor-focused tests demonstrate provider-directed environment lookup, explicit precedence, and selection based on declared authentication type even without inferred credentials."}, {"action_id": "semantic-action:6b88c49d9fea9d8b", "action_name": "guard-custom-endpoint-transport", "condition": "Run only when endpoint resolution yields a non-empty custom endpoint.", "depends_on": ["resolve-provider-endpoint-precedence"], "optional": false, "required": true, "role": "implement", "step_id": "step-2", "validation": "Unit tests prove loopback HTTP acceptance and rejection of malformed or remote HTTP values."}, {"action_id": "semantic-action:4ebd6851e9c5c71f", "action_name": "adapt-provider-sdk-options", "condition": "Run after an endpoint is admitted, or directly with no endpoint when resolution yields none; preserve an explicit provider-mode value when supplied.", "depends_on": ["resolve-provider-endpoint-precedence", "guard-custom-endpoint-transport"], "optional": false, "required": true, "role": "reconcile", "step_id": "step-3", "validation": "Mocked constructor assertions prove accepted endpoint forwarding and concrete provider-mode reconciliation for both provider branches and existing non-cloud cases."}], "stop_conditions": ["Stop and defer if the declared provider cannot be determined at the client-construction boundary.", "Stop if no direct test seam can observe the external SDK constructor options or rejection behavior.", "Stop rather than broadening scope if endpoint support would require changing credential acquisition or unrelated authentication paths.", "Do not claim runtime validation success until the focused tests execute in an intact checkout."], "validation_ladder": ["Static diff check: confirm endpoint lookup is inside the intended SDK-construction branch and keyed by the declared authentication type.", "Focused unit checks: verify each provider environment endpoint is forwarded with the matching provider mode.", "Precedence check: set explicit and environment endpoints and verify the explicit value wins.", "Safety checks: verify loopback HTTP succeeds while malformed and remote HTTP endpoints fail before SDK construction.", "Regression checks: retain established constructor-option assertions, now with concrete non-cloud provider mode.", "Repository test execution: run the focused content-generator test file in an intact checkout; this remained deferred in the supplied staged-deletion worktree."], "when_to_use": ["A client supports multiple provider interfaces selected by an authentication or backend mode.", "Callers need endpoint overrides through both an explicit configuration field and provider-specific environment variables.", "The external SDK accepts endpoint and provider-mode options that must remain mutually consistent."]}

retrieval trace:
- pattern:5895d079305884e4 --supported_by/out--> workflow:a1416952c048b7d5
- pattern:5895d079305884e4 --instantiates/in--> workflow:a1416952c048b7d5
- workflow-step:92607eeb6df21e6401017d40 --has_step/in--> workflow:a1416952c048b7d5
- workflow-step:b82af4a10b019ca343ce0b7d --has_step/in--> workflow:a1416952c048b7d5
- workflow-step:960da6c035cadc27deb58eb3 --has_step/in--> workflow:a1416952c048b7d5

## Retrieved node 3: workflow — adapt-compatible-provider-configuration-and-routing
id: workflow:b5dccd8edcc90ddd
repository: Aider-AI/aider
score: 0.054142
sources: {"graph": 0.028308899769891153, "lexical": 0.0125, "lexical_raw": 5.568198011474891e-06, "vector": 0.013333333333333334, "vector_raw": 0.0814151937995504}

A partial-order workflow for adding provider-specific client settings and request-routing fields while keeping domain construction independent of credentials and preserving the default request path.

facets:
{"entry_state": "The application can configure a key and base endpoint, but additional provider settings cannot flow through the interface; provider initialization is coupled to domain construction; and request dispatch omits provider-specific routing fields.", "exit_state": "Supplied provider settings are applied before domain construction, the domain constructor is provider-independent, and request dispatch conditionally carries the provider's expected routing identifiers without changing the ordinary request path.", "problem_class": "provider-interface-adaptation"}

payload:
{"anti_goals": ["Do not redesign model prompting, edit formats, retry policy, or response processing.", "Do not force provider-specific optional values into requests when the user did not configure them.", "Do not retain credentials in unrelated domain constructor signatures merely to initialize a shared provider client.", "Do not claim end-to-end provider connectivity without a request-level or integration oracle."], "entry_state": "The application can configure a key and base endpoint, but additional provider settings cannot flow through the interface; provider initialization is coupled to domain construction; and request dispatch omits provider-specific routing fields.", "exit_state": "Supplied provider settings are applied before domain construction, the domain constructor is provider-independent, and request dispatch conditionally carries the provider's expected routing identifiers without changing the ordinary request path.", "goal": "Accept the compatible provider's required settings at the application boundary and translate them into the client and request interfaces needed to dispatch a chat completion successfully.", "not_applicable_when": ["The provider is not compatible with the existing client and request/response protocol.", "The required adaptation changes authentication or transport semantics beyond client attributes and request keyword mapping.", "Provider configuration is intentionally isolated per component or per request and cannot safely use the shared client state evidenced here."], "steps": [{"action_id": "semantic-action:f739bb2c7c9a9da7", "action_name": "centralize-provider-client-configuration", "condition": "The compatible provider exposes additional client-level configuration values.", "depends_on": [], "optional": false, "required": true, "role": "establish-contract", "step_id": "step-1", "validation": "Verify each supplied interface value maps to the correct client attribute before component creation and that omitted optional values are not assigned."}, {"action_id": "semantic-action:d803e48cee271d14", "action_name": "decouple-domain-construction-from-provider-credentials", "condition": "Provider initialization previously occurred inside the domain-component factory or constructor.", "depends_on": ["centralize-provider-client-configuration"], "optional": false, "required": true, "role": "reconcile", "step_id": "step-2", "validation": "Verify production and direct test call sites construct the component without credential or endpoint arguments and retain existing behavior."}, {"action_id": "semantic-action:00aaec027a328c3f", "action_name": "adapt-provider-routing-at-request-dispatch", "condition": "The provider requires deployment or engine routing fields on each request.", "depends_on": ["centralize-provider-client-configuration"], "optional": false, "required": true, "role": "implement", "step_id": "step-3", "validation": "Capture the provider request call and verify configured routing fields are translated to deployment_id and engine, while absent fields remain absent."}], "stop_conditions": ["Stop if the provider client does not support the proposed client attributes or request arguments.", "Stop if configuration ownership cannot be moved without introducing conflicting shared-client state.", "Stop if existing direct construction call sites cannot be reconciled to the provider-independent contract.", "Defer completion if no oracle can verify the emitted request arguments or a real compatible-provider request."], "validation_ladder": ["Static diff check: confirm the supported interface fields map to provider-client attributes and the domain constructor no longer owns provider initialization.", "Constructor regression check: run existing domain, command, and editing tests through the simplified construction contract.", "Request-unit check: mock the provider request method and assert routing-key presence and absence for configured and unconfigured cases.", "Configuration-path check: exercise command-line and configuration-file inputs to confirm equivalent normalized client state.", "Integration check: issue a minimal request against a configured compatible provider endpoint and confirm successful routing."], "when_to_use": ["A provider uses an otherwise compatible client library but requires additional endpoint metadata or routing identifiers.", "Provider configuration is currently split into or coupled with a domain-component constructor.", "The provider request method accepts routing fields that are not represented in the application's common request construction."]}

retrieval trace:
- pattern:5895d079305884e4 --supported_by/out--> workflow:b5dccd8edcc90ddd
- pattern:5895d079305884e4 --instantiates/in--> workflow:b5dccd8edcc90ddd
- workflow-step:4ef41cfb317d195f2a16236a --has_step/in--> workflow:b5dccd8edcc90ddd
- workflow-step:430e1e4cfb42c3eb5d570b1b --has_step/in--> workflow:b5dccd8edcc90ddd
- workflow-step:109a80c79da2ce46de0d5754 --has_step/in--> workflow:b5dccd8edcc90ddd

## Retrieved node 4: workflow — align-resume-interface-with-persisted-runtime-route
id: workflow:7feccf0ac8bb22b3
repository: NousResearch/hermes-agent
score: 0.048573
sources: {"graph": 0.02179312689477587, "lexical": 0.011627906976744186, "lexical_raw": 4.395955673489258e-06, "vector": 0.015151515151515152, "vector_raw": 0.2097849588101521}

Resolve cross-interface resume failures by identifying the metadata actually updated by the producer, defining a single precedence contract for legacy and current representations, and routing the inconsistent consumer through that contract while preserving its local safety behavior.

facets:
{"entry_state": "At least one resume interface can read a stale provider, endpoint, or API mode because its local metadata interpretation differs from the writer and from another resume consumer.", "exit_state": "All examined resume interfaces consume the same canonical route precedence, the latest nested route wins over stale representations, partial legacy metadata remains compatible, and unsafe fallback identities remain filtered.", "problem_class": "provider-interface-adaptation"}

payload:
{"anti_goals": ["Do not change provider selection for new sessions that have no usable persisted route.", "Do not treat accounting buckets as authoritative route identities when they are documented as frozen or non-routable.", "Do not remove interface-specific endpoint-ownership checks, stale-provider healing, reasoning settings, service-tier handling, or profile-following behavior.", "Do not persist or restore raw API credentials as part of route reconciliation."], "entry_state": "At least one resume interface can read a stale provider, endpoint, or API mode because its local metadata interpretation differs from the writer and from another resume consumer.", "exit_state": "All examined resume interfaces consume the same canonical route precedence, the latest nested route wins over stale representations, partial legacy metadata remains compatible, and unsafe fallback identities remain filtered.", "goal": "A session resumed through any supported interface uses the provider, endpoint, and protocol associated with its latest persisted runtime execution rather than combining its model with stale route metadata.", "not_applicable_when": ["There is no durable runtime-route representation or no evidence identifying which representation is freshest.", "The failure occurs during initial provider discovery rather than restoration of an existing session.", "The differing consumers intentionally implement distinct routing semantics rather than alternate interfaces to the same resumed session."], "steps": [{"action_id": "semantic-action:2d7c1bbc5fa9d6fa", "action_name": "reconcile-partial-persisted-route-fallback", "condition": "The persisted row has multiple current or legacy route representations whose precedence and fallback composition must be made explicit.", "depends_on": [], "optional": false, "required": true, "role": "establish-contract", "step_id": "step-1", "validation": "Canonical-reader tests prove nested precedence, legacy top-level support, routable fallback completion, bare-bucket rejection, and malformed-input tolerance."}, {"action_id": "semantic-action:743621ceda02ecdb", "action_name": "delegate-resume-route-selection-to-canonical-reader", "condition": "A resume consumer independently decodes route metadata instead of using the established canonical resolver.", "depends_on": ["reconcile-partial-persisted-route-fallback"], "optional": false, "required": true, "role": "implement", "step_id": "step-2", "validation": "Cross-interface regression tests prove the adapted consumer and the existing canonical consumer select the nested current route over stale billing and top-level values."}], "stop_conditions": ["Stop if the producer's authoritative or freshest representation cannot be established from code or tests.", "Stop if the proposed canonical precedence would discard a supported legacy route representation without a migration or compatibility oracle.", "Stop if the consumer has intentionally different routing semantics and therefore should not share the resolver.", "Do not claim runtime validation complete unless the focused tests execute successfully in a dependency-complete environment."], "validation_ladder": ["Inspect the writer to confirm which persisted representation is refreshed on each executed turn.", "Unit-test the canonical resolver across nested, top-level, partial, malformed, routable-fallback, and non-routable-fallback inputs.", "Run consumer-level regression tests with a stale first-call billing provider and a newer nested route.", "Run consumer-level regression tests with stale top-level endpoint/protocol keys and a newer nested route.", "Run existing resume compatibility tests for endpoint ownership, provider healing, legacy rows, profile-following exclusions, reasoning configuration, and service tier.", "Run repository diff validation and the focused test module in the supported project environment."], "when_to_use": ["A producer and one resume consumer use a nested or versioned runtime snapshot while another consumer reconstructs the same route from older top-level or accounting fields.", "A resumed model is sent to the wrong provider endpoint or protocol after the session changes providers.", "Multiple consumers interpret the same persisted route with different precedence rules."]}

retrieval trace:
- pattern:5895d079305884e4 --supported_by/out--> workflow:7feccf0ac8bb22b3
- pattern:5895d079305884e4 --instantiates/in--> workflow:7feccf0ac8bb22b3
- workflow-step:f173c2cfa6592de2f5e64680 --has_step/in--> workflow:7feccf0ac8bb22b3
- workflow-step:acdd9fe187de8b5faaf11b6a --has_step/in--> workflow:7feccf0ac8bb22b3

## Retrieved node 5: workflow — adapt_shared_request_shape_for_strict_endpoint
id: workflow:da462de34604fc60
repository: QwenLM/qwen-code
score: 0.046099
sources: {"graph": 0.02157741132332616, "lexical": 0.011363636363636364, "lexical_raw": 3.861632071702955e-06, "vector": 0.013157894736842105, "vector_raw": 0.07857108528510649}

Route only the affected endpoint to a narrow outbound adapter, then remove the provably derived incompatible field while preserving shared behavior and caller data.

facets:
{"entry_state": "A shared provider emits both a source field and its synthesized mirror during replay, and requests to one strict endpoint fail before continuation completes.", "exit_state": "Only requests routed to the affected endpoint omit the exact synthesized field at the outbound boundary; accepted fields and explicit distinct values survive, other endpoints retain prior behavior, and multi-turn continuation succeeds.", "problem_class": "provider-interface-adaptation"}

payload:
{"anti_goals": ["Do not remove the accepted source field needed to replay prior reasoning.", "Do not disable or change shared mirroring behavior for endpoints that accept or require it.", "Do not infer endpoint identity from a hosted model-family name.", "Do not mutate persisted or caller-owned conversation history.", "Do not discard a distinct explicit field merely because it has the same semantic category as the rejected derived field."], "entry_state": "A shared provider emits both a source field and its synthesized mirror during replay, and requests to one strict endpoint fail before continuation completes.", "exit_state": "Only requests routed to the affected endpoint omit the exact synthesized field at the outbound boundary; accepted fields and explicit distinct values survive, other endpoints retain prior behavior, and multi-turn continuation succeeds.", "goal": "Allow multi-turn replay through a strict OpenAI-compatible endpoint without sending a shared-layer compatibility field that the endpoint rejects.", "not_applicable_when": ["The endpoint itself requires the derived field or rejects the source field instead.", "The rejected value cannot be distinguished from a caller-authored value using an evidence-backed invariant.", "Provider identity cannot be established safely from available configuration.", "The failure is unrelated to outbound request shape or multi-turn replay."], "steps": [{"action_id": "semantic-action:4a8c6ad7fc7800b2", "action_name": "route_endpoint_by_canonical_hostname", "condition": "The endpoint has a stable canonical hostname and model names may be served by multiple providers.", "depends_on": [], "optional": false, "required": true, "role": "establish-contract", "step_id": "step-1", "validation": "Canonical and subdomain URLs select the adapter, while suffix-confusable and unrelated hosts follow their existing provider path."}, {"action_id": "semantic-action:db94712551fe490e", "action_name": "remove_only_derived_incompatible_field", "condition": "The selected endpoint rejects the derived field and the shared transformation makes the derived copy recognizable by exact equality with its source.", "depends_on": ["route_endpoint_by_canonical_hostname"], "optional": false, "required": true, "role": "reconcile", "step_id": "step-2", "validation": "Unit assertions prove selective removal and preservation; an HTTP integration test proves a replayed multi-turn request reaches the wire without the rejected field and receives a successful response."}], "stop_conditions": ["Stop if the endpoint rejection cannot be reproduced or tied to the synthesized field.", "Stop if safe provider identity requires a model-name heuristic shared by unrelated endpoints.", "Stop if the implementation cannot distinguish the derived copy from caller-authored data.", "Stop if removing the field breaks required replay information or changes unaffected endpoints."], "validation_ladder": ["Confirm the parent shared provider actually synthesizes the rejected field for the affected request class.", "Test provider routing for the exact hostname, supported subdomains, malformed or unrelated URLs, and hostname-confusion cases.", "Test transformation invariants: preserve the accepted source field, preserve distinct explicit values, remove only an equal string mirror, and leave source history unchanged.", "Exercise the real conversion, provider, and HTTP path with replayed multi-turn history against a strict endpoint stand-in that reproduces the rejection contract.", "Run the focused provider test suite in a materialized checkout with the repository's required Node runtime."], "when_to_use": ["A nominally compatible endpoint rejects a field synthesized by shared request construction rather than supplied independently by the caller.", "The failure occurs after prior structured assistant output is replayed, including continuations following thinking or tool-use turns.", "The endpoint can be identified from configuration using a canonical hostname boundary."]}

retrieval trace:
- pattern:5895d079305884e4 --supported_by/out--> workflow:da462de34604fc60
- pattern:5895d079305884e4 --instantiates/in--> workflow:da462de34604fc60
- workflow-step:2c58ddeb1f69c561232ae7b2 --has_step/in--> workflow:da462de34604fc60
- workflow-step:feec6ac8c947b69fececccd1 --has_step/in--> workflow:da462de34604fc60

## Retrieved node 6: action — Keep endpoint routing and SDK provider mode consistent at the external-provider interface even when optional configuration fields were not populated upstream.
id: semantic-action:4ebd6851e9c5c71f
repository: -
score: 0.086599
sources: {"graph": 0.05558946754703857, "lexical": 0.015625, "lexical_raw": 2.200788256486705, "mandatory_step_action": 0.08049728227944307, "validation_closure": 0.047852482233248346, "vector": 0.015384615384615385, "vector_raw": 0.21429238817943488}

Construct the provider SDK options with the validated endpoint and a concrete provider-mode flag, deriving the mode from the declared authentication interface when upstream credential inference left it unset.

facets:
{"grounded_semantics": true, "module_role": "external provider SDK adapter", "operation": "adapt", "problem_class": "provider-interface-adaptation"}

retrieval trace:
- semantic-action:0615b3d0c1425572 --enables/out--> semantic-action:4ebd6851e9c5c71f
- semantic-action:0615b3d0c1425572 --validates/in--> semantic-action:4ebd6851e9c5c71f
- pattern-step:44d984675ad90d2d42394568 --conforms_to/in--> semantic-action:4ebd6851e9c5c71f
- workflow-step:92607eeb6df21e6401017d40 --executed_by/out--> semantic-action:4ebd6851e9c5c71f
- semantic-action:6b88c49d9fea9d8b --requires/out--> semantic-action:4ebd6851e9c5c71f
- semantic-action:4ebd6851e9c5c71f --validates--> semantic-action:0615b3d0c1425572

## Retrieved node 7: action — Route chat requests through providers that require a deployment identifier or engine argument while preserving ordinary requests when those settings are absent.
id: semantic-action:00aaec027a328c3f
repository: -
score: 0.072921
sources: {"selected_payload_relation": 0.07292115105538255}

Translate configured routing identifiers into the keyword arguments expected by the provider's request method, without adding absent optional fields.

facets:
{"grounded_semantics": true, "module_role": "provider request adapter", "operation": "adapt", "problem_class": "provider-interface-adaptation"}

retrieval trace:
- pattern:5895d079305884e4 --payload-reference--> semantic-action:00aaec027a328c3f

## Retrieved node 8: action — Ensure custom requests target the endpoint belonging to the selected provider interface without allowing an environment default to override an explicit caller choice.
id: semantic-action:0615b3d0c1425572
repository: -
score: 0.072921
sources: {"selected_payload_relation": 0.07292115105538255}

Select the endpoint candidate at the provider-client boundary: retain an explicit runtime endpoint when present; otherwise read the environment slot associated with the declared authentication interface.

facets:
{"grounded_semantics": true, "module_role": "provider client option resolver", "operation": "resolve", "problem_class": "provider-interface-adaptation"}

retrieval trace:
- pattern:5895d079305884e4 --payload-reference--> semantic-action:0615b3d0c1425572

## Retrieved node 9: action — Produce one usable persisted runtime route from layered session metadata without replacing newer or more specific route fields with a stale or non-routable fallback identity.
id: semantic-action:2d7c1bbc5fa9d6fa
repository: -
score: 0.072921
sources: {"selected_payload_relation": 0.07292115105538255}

Normalize layered session metadata so the canonical reader preserves explicit top-level endpoint and wire fields while filling only a missing provider from a routable historical fallback.

facets:
{"grounded_semantics": true, "module_role": "canonical persisted-runtime route resolver", "operation": "reconcile", "problem_class": "provider-interface-adaptation"}

retrieval trace:
- pattern:5895d079305884e4 --payload-reference--> semantic-action:2d7c1bbc5fa9d6fa

## Retrieved node 10: action — Ensure requests reach the adapter that implements the actual endpoint contract while avoiding false routing for similarly named or hostile hosts.
id: semantic-action:4a8c6ad7fc7800b2
repository: -
score: 0.072921
sources: {"selected_payload_relation": 0.07292115105538255}

Recognize an endpoint using parsed hostname boundaries and route matching requests to its dedicated compatibility adapter without relying on model-family names or substring matches.

facets:
{"grounded_semantics": true, "module_role": "provider selection boundary", "operation": "route", "problem_class": "provider-interface-adaptation"}

retrieval trace:
- pattern:5895d079305884e4 --payload-reference--> semantic-action:4a8c6ad7fc7800b2

## Retrieved node 11: action — Prevent invalid or insecure remote endpoint overrides from reaching the provider SDK while preserving local development connectivity.
id: semantic-action:6b88c49d9fea9d8b
repository: -
score: 0.072921
sources: {"selected_payload_relation": 0.07292115105538255}

Parse any selected custom endpoint and enforce encrypted transport for remote hosts while retaining an HTTP exception for local loopback development.

facets:
{"grounded_semantics": true, "module_role": "outbound endpoint policy guard", "operation": "guard", "problem_class": "provider-interface-adaptation"}

retrieval trace:
- pattern:5895d079305884e4 --payload-reference--> semantic-action:6b88c49d9fea9d8b

## Retrieved node 12: action — Ensure every resume interface restores the provider, endpoint, and protocol belonging to the session's latest persisted runtime route.
id: semantic-action:743621ceda02ecdb
repository: -
score: 0.072921
sources: {"selected_payload_relation": 0.07292115105538255}

Adapt a resume interface that had its own incomplete metadata reader to consume the canonical route resolver, while leaving its interface-specific override construction and safety repairs intact.

facets:
{"grounded_semantics": true, "module_role": "client-session resume adapter", "operation": "adapt", "problem_class": "provider-interface-adaptation"}

retrieval trace:
- pattern:5895d079305884e4 --payload-reference--> semantic-action:743621ceda02ecdb

## Retrieved node 13: action — Prevent provider-specific credentials and endpoint defaults from leaking into the constructor contract of the component that manages editing behavior.
id: semantic-action:d803e48cee271d14
repository: -
score: 0.072921
sources: {"selected_payload_relation": 0.07292115105538255}

Make domain-component creation independent of provider initialization after configuration ownership moves to the application boundary, then reconcile all direct construction call sites.

facets:
{"grounded_semantics": true, "module_role": "domain component construction boundary", "operation": "reconcile", "problem_class": "provider-interface-adaptation"}

retrieval trace:
- pattern:5895d079305884e4 --payload-reference--> semantic-action:d803e48cee271d14

## Retrieved node 14: action — Prevent strict endpoints from rejecting replayed structured messages while retaining the information they accept and preserving caller-authored values.
id: semantic-action:db94712551fe490e
repository: -
score: 0.072921
sources: {"selected_payload_relation": 0.07292115105538255}

At the outbound boundary, recognize the exact compatibility field synthesized by shared request construction and remove that copy without altering source history or legitimate fields.

facets:
{"grounded_semantics": true, "module_role": "outbound request compatibility adapter", "operation": "reconcile", "problem_class": "provider-interface-adaptation"}

retrieval trace:
- pattern:5895d079305884e4 --payload-reference--> semantic-action:db94712551fe490e

## Retrieved node 15: action — Allow a compatible provider endpoint to receive its required client configuration without embedding that configuration in the domain component constructor.
id: semantic-action:f739bb2c7c9a9da7
repository: -
score: 0.072921
sources: {"selected_payload_relation": 0.07292115105538255}

Expose the provider's optional connection and routing settings at the application boundary and apply only supplied values to the shared client before downstream components are created.

facets:
{"grounded_semantics": true, "module_role": "application composition and provider-client configuration boundary", "operation": "normalize", "problem_class": "provider-interface-adaptation"}

retrieval trace:
- pattern:5895d079305884e4 --payload-reference--> semantic-action:f739bb2c7c9a9da7

# Applicability judgment
{
  "selected_skill_id": "pattern:5895d079305884e4",
  "applicable": true,
  "confidence": 0.93,
  "rationale": "The failure is a provider-selection precedence mismatch: the explicit CLI specification `provider/model` is the authoritative interface signal, but resolution can instead select a competing catalog entry whose model ID equals the entire input string. The holdout test makes this causal conflict explicit by placing `vercel-ai-gateway` model ID `zai/glm-5` before the intended `zai` provider model ID `glm-5`, then requiring `resolveCliModel` to honor the parsed provider and model components. The selected pattern directly applies because it requires establishing explicit provider identity and precedence, then adapting the narrow resolver boundary that violates that contract while preserving unaffected resolution paths. The repository-specific workflows and SDK-option action concern endpoint construction, persisted routes, or request translation and are therefore less applicable than the cross-workflow pattern.",
  "missing_preconditions": [
    "The hidden implementation and call sites must confirm that `resolveCliModel` is the boundary owning this precedence decision rather than a lower-level registry API.",
    "Regression evidence is still needed that bare model IDs, absent providers, unknown or malformed provider/model inputs, and unambiguous existing selections retain their prior behavior."
  ]
}

Use the guidance to localize the problem and choose a safe implementation, but rely on the visible tests and current code as the oracle.