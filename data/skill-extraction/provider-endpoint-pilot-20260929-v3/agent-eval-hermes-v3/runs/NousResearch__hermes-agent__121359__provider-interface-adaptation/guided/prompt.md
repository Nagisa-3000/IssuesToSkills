You are solving a held-out implementation task in repository NousResearch/hermes-agent.
The workspace is a synthetic snapshot based on the pre-change parent and has no future Git history. The original solution commit is not available. Work only in this workspace; do not search external services or other repositories. Do not edit the visible regression tests. Inspect the current code, implement the behavior, and run focused tests before finishing.

# Problem family
provider interface adaptation

# Issue/task
fallback provider base_url is ignored

Held-out cross-project task in the provider interface adaptation family. Implement the behavior required by the visible regression tests while preserving existing compatibility and error semantics. The original implementation commit is intentionally absent from this snapshot.

# Visible regression tests retained for this evaluation
- tests/tools/test_base_environment.py
- tests/tools/test_tool_result_storage.py
- tests/hermes_cli/test_model_validation.py
- tests/tui_gateway/test_ws_orphan_races.py
- tests/agent/test_fallback_entry_base_url.py
- apps/desktop/src/store/composer-queue.test.ts
- tests/tools/test_file_ops_single_roundtrip.py
- tests/hermes_cli/test_models_relay_base_url.py
- tests/hermes_cli/test_runtime_provider_resolution.py
- apps/desktop/src/app/chat/sidebar/project-filter.test.ts
- tests/agent/test_turn_finalizer_interrupt_alternation.py
- apps/desktop/src/app/contrib/hooks/use-background-sync.test.ts

# Arm
guided

# Retrieved Skill Graph guidance
The following are hypotheses retrieved only from the training repositories using lexical/vector retrieval, optional HNSW, and typed graph expansion. Verify every step against the current code and tests; do not copy repository-specific names blindly.

## Retrieved node 1: pattern — isolate-provider-contract-divergence-at-integration-boundaries
id: pattern:isolate-provider-contract-divergence-at-integration-boundaries
repository: -
score: 0.062223
sources: {"graph": 0.03495061727477184, "lexical": 0.014285714285714285, "lexical_raw": 3.0088251798194157e-06, "vector": 0.012987012987012988, "vector_raw": 0.0}

Preserve the shared client model while adapting provider-specific endpoint differences at a narrow integration boundary: centralize endpoint configuration or classification, apply only the required routing or wire-format translation, and validate the affected end-to-end request path.

facets:
{"exclusions": [], "failure_modes": [], "level": "pattern", "preconditions": []}

payload:
{"routing_terms": ["pattern"]}

retrieval trace:
- Aider-AI__aider__88@549a1a76403e309890410f9538bda2fc4f901758:workflow:adapt-a-client-to-provider-specific-endpoint-contracts --contains/in--> pattern:isolate-provider-contract-divergence-at-integration-boundaries
- QwenLM/qwen-code#11657@3ba01990e13e9e8e14e147b60add50e0f972431a:workflow:adapt-generic-compatible-requests-to-a-stricter-endpoint-contract --contains/in--> pattern:isolate-provider-contract-divergence-at-integration-boundaries

## Retrieved node 2: workflow — adapt-a-client-to-provider-specific-endpoint-contracts
id: Aider-AI__aider__88@549a1a76403e309890410f9538bda2fc4f901758:workflow:adapt-a-client-to-provider-specific-endpoint-contracts
repository: -
score: 0.104519
sources: {"graph": 0.07566933308626857, "lexical": 0.015151515151515152, "lexical_raw": 3.282065550052863e-06, "vector": 0.0136986301369863, "vector_raw": 0.0}

Extend a provider-compatible client by centralizing endpoint configuration, reconciling consumer construction, and translating optional routing values only at the invocation boundary.

facets:
{"exclusions": [], "failure_modes": [], "level": "workflow", "preconditions": []}

payload:
{"routing_terms": ["workflow"]}

retrieval trace:
- Aider-AI__aider__88@549a1a76403e309890410f9538bda2fc4f901758:atomic:reconcile-consumer-construction-interface --contains/in--> Aider-AI__aider__88@549a1a76403e309890410f9538bda2fc4f901758:workflow:adapt-a-client-to-provider-specific-endpoint-contracts
- Aider-AI__aider__88@549a1a76403e309890410f9538bda2fc4f901758:atomic:centralize-provider-sdk-configuration --contains/in--> Aider-AI__aider__88@549a1a76403e309890410f9538bda2fc4f901758:workflow:adapt-a-client-to-provider-specific-endpoint-contracts
- Aider-AI__aider__88@549a1a76403e309890410f9538bda2fc4f901758:atomic:forward-optional-provider-routing-fields --contains/in--> Aider-AI__aider__88@549a1a76403e309890410f9538bda2fc4f901758:workflow:adapt-a-client-to-provider-specific-endpoint-contracts
- pattern:isolate-provider-contract-divergence-at-integration-boundaries --contains/out--> Aider-AI__aider__88@549a1a76403e309890410f9538bda2fc4f901758:workflow:adapt-a-client-to-provider-specific-endpoint-contracts

## Retrieved node 3: workflow — surface-hidden-http-error-details-at-provider-boundaries
id: earendil-works/pi#5832@6fbeba51af98a37a0695ec8b53308dde81d9ab46:workflow:surface-hidden-http-error-details-at-provider-boundaries
repository: -
score: 0.098561
sources: {"graph": 0.0687033673039785, "lexical": 0.014705882352941176, "lexical_raw": 3.1739762148199973e-06, "vector": 0.015151515151515152, "vector_raw": 0.10865549034627574}

Establish one bounded error contract, compose it without duplication, adopt it at affected provider boundaries while preserving local behavior, and verify both utility semantics and representative catch paths.

facets:
{"exclusions": [], "failure_modes": [], "level": "workflow", "preconditions": []}

payload:
{"routing_terms": ["workflow"]}

retrieval trace:
- earendil-works/pi#5832@6fbeba51af98a37a0695ec8b53308dde81d9ab46:atomic:normalize-heterogeneous-provider-failures --contains/in--> earendil-works/pi#5832@6fbeba51af98a37a0695ec8b53308dde81d9ab46:workflow:surface-hidden-http-error-details-at-provider-boundaries
- earendil-works/pi#5832@6fbeba51af98a37a0695ec8b53308dde81d9ab46:atomic:validate-provider-diagnostic-contract --contains/in--> earendil-works/pi#5832@6fbeba51af98a37a0695ec8b53308dde81d9ab46:workflow:surface-hidden-http-error-details-at-provider-boundaries
- earendil-works/pi#5832@6fbeba51af98a37a0695ec8b53308dde81d9ab46:atomic:adapt-provider-catch-boundaries --contains/in--> earendil-works/pi#5832@6fbeba51af98a37a0695ec8b53308dde81d9ab46:workflow:surface-hidden-http-error-details-at-provider-boundaries
- earendil-works/pi#5832@6fbeba51af98a37a0695ec8b53308dde81d9ab46:atomic:compose-nonduplicating-provider-diagnostic --contains/in--> earendil-works/pi#5832@6fbeba51af98a37a0695ec8b53308dde81d9ab46:workflow:surface-hidden-http-error-details-at-provider-boundaries

## Retrieved node 4: workflow — adapt-generic-compatible-requests-to-a-stricter-endpoint-contract
id: QwenLM/qwen-code#11657@3ba01990e13e9e8e14e147b60add50e0f972431a:workflow:adapt-generic-compatible-requests-to-a-stricter-endpoint-contract
repository: -
score: 0.097402
sources: {"graph": 0.06914303332324669, "lexical": 0.013333333333333334, "lexical_raw": 2.3582423733557238e-06, "vector": 0.014925373134328358, "vector_raw": 0.10798189975257515}

Introduce a narrowly routed outbound adapter when a nominally compatible endpoint rejects a generic provider transformation, preserving shared semantics and verifying the complete continuation path.

facets:
{"exclusions": [], "failure_modes": [], "level": "workflow", "preconditions": []}

payload:
{"routing_terms": ["workflow"]}

retrieval trace:
- QwenLM/qwen-code#11657@3ba01990e13e9e8e14e147b60add50e0f972431a:atomic:validate-strict-endpoint-multiturn-continuation --contains/in--> QwenLM/qwen-code#11657@3ba01990e13e9e8e14e147b60add50e0f972431a:workflow:adapt-generic-compatible-requests-to-a-stricter-endpoint-contract
- pattern:isolate-provider-contract-divergence-at-integration-boundaries --contains/out--> QwenLM/qwen-code#11657@3ba01990e13e9e8e14e147b60add50e0f972431a:workflow:adapt-generic-compatible-requests-to-a-stricter-endpoint-contract
- QwenLM/qwen-code#11657@3ba01990e13e9e8e14e147b60add50e0f972431a:atomic:classify-compatible-endpoint-by-canonical-hostname --contains/in--> QwenLM/qwen-code#11657@3ba01990e13e9e8e14e147b60add50e0f972431a:workflow:adapt-generic-compatible-requests-to-a-stricter-endpoint-contract
- QwenLM/qwen-code#11657@3ba01990e13e9e8e14e147b60add50e0f972431a:atomic:remove-only-derived-incompatible-wire-field --contains/in--> QwenLM/qwen-code#11657@3ba01990e13e9e8e14e147b60add50e0f972431a:workflow:adapt-generic-compatible-requests-to-a-stricter-endpoint-contract

## Retrieved node 5: workflow — adapt-session-resume-to-a-versioned-provider-route
id: NousResearch/hermes-agent#125942@33c6ab002d1fac653d7e772025ef7aaab7c83480:workflow:adapt-session-resume-to-a-versioned-provider-route
repository: -
score: 0.066699
sources: {"graph": 0.036937455027880976, "lexical": 0.015873015873015872, "lexical_raw": 2.1111886085851297, "vector": 0.013888888888888888, "vector_raw": 0.06878517589774806}

Establish one precedence-aware interpretation of persisted provider-interface state, then make each resume consumer delegate route extraction to it and validate conflicts between new and legacy representations.

facets:
{"exclusions": [], "failure_modes": [], "level": "workflow", "preconditions": []}

payload:
{"routing_terms": ["workflow"]}

retrieval trace:
- NousResearch/hermes-agent#125942@33c6ab002d1fac653d7e772025ef7aaab7c83480:atomic:resolve-persisted-route-by-freshness --contains/in--> NousResearch/hermes-agent#125942@33c6ab002d1fac653d7e772025ef7aaab7c83480:workflow:adapt-session-resume-to-a-versioned-provider-route
- NousResearch/hermes-agent#125942@33c6ab002d1fac653d7e772025ef7aaab7c83480:atomic:delegate-resume-consumer-to-canonical-route-reader --contains/in--> NousResearch/hermes-agent#125942@33c6ab002d1fac653d7e772025ef7aaab7c83480:workflow:adapt-session-resume-to-a-versioned-provider-route

## Retrieved node 6: atomic — reconcile-consumer-construction-interface
id: Aider-AI__aider__88@549a1a76403e309890410f9538bda2fc4f901758:atomic:reconcile-consumer-construction-interface
repository: -
score: 0.050953
sources: {"graph": 0.01869489414694894, "lexical": 0.016129032258064516, "lexical_raw": 2.6708942835002483, "vector": 0.016129032258064516, "vector_raw": 0.14281517665678226}

Remove provider credentials from the consumer factory contract and migrate production and test callers to the configuration-independent constructor.

facets:
{"exclusions": [], "failure_modes": [], "level": "atomic", "preconditions": []}

payload:
{"routing_terms": ["atomic"]}

retrieval trace:
- Aider-AI__aider__88@549a1a76403e309890410f9538bda2fc4f901758:workflow:adapt-a-client-to-provider-specific-endpoint-contracts --contains/out--> Aider-AI__aider__88@549a1a76403e309890410f9538bda2fc4f901758:atomic:reconcile-consumer-construction-interface

## Retrieved node 7: atomic — centralize-provider-sdk-configuration
id: Aider-AI__aider__88@549a1a76403e309890410f9538bda2fc4f901758:atomic:centralize-provider-sdk-configuration
repository: -
score: 0.050193
sources: {"graph": 0.01869489414694894, "lexical": 0.015625, "lexical_raw": 3.5993165313968383e-06, "vector": 0.015873015873015872, "vector_raw": 0.13120142815993086}

Accept endpoint-specific provider settings at the application boundary and apply only supplied values to the shared provider client before constructing downstream consumers.

facets:
{"exclusions": [], "failure_modes": [], "level": "atomic", "preconditions": []}

payload:
{"routing_terms": ["atomic"]}

retrieval trace:
- Aider-AI__aider__88@549a1a76403e309890410f9538bda2fc4f901758:workflow:adapt-a-client-to-provider-specific-endpoint-contracts --contains/out--> Aider-AI__aider__88@549a1a76403e309890410f9538bda2fc4f901758:atomic:centralize-provider-sdk-configuration

## Retrieved node 8: atomic — resolve-persisted-route-by-freshness
id: NousResearch/hermes-agent#125942@33c6ab002d1fac653d7e772025ef7aaab7c83480:atomic:resolve-persisted-route-by-freshness
repository: -
score: 0.049764
sources: {"graph": 0.019285714285714285, "lexical": 0.014084507042253521, "lexical_raw": 2.9430667132378626e-06, "vector": 0.01639344262295082, "vector_raw": 0.1965457197631288}

Normalize multiple persisted route representations into one provider/endpoint/wire tuple using explicit freshness precedence: the latest nested runtime route first, then legacy top-level fields, with a routable billing identity only filling a missing provider.

facets:
{"exclusions": [], "failure_modes": [], "level": "atomic", "preconditions": []}

payload:
{"routing_terms": ["atomic"]}

retrieval trace:
- NousResearch/hermes-agent#125942@33c6ab002d1fac653d7e772025ef7aaab7c83480:workflow:adapt-session-resume-to-a-versioned-provider-route --contains/out--> NousResearch/hermes-agent#125942@33c6ab002d1fac653d7e772025ef7aaab7c83480:atomic:resolve-persisted-route-by-freshness

# Applicability judgment
{
  "selected_skill_id": "Aider-AI__aider__88@549a1a76403e309890410f9538bda2fc4f901758:atomic:centralize-provider-sdk-configuration",
  "applicable": true,
  "confidence": 0.78,
  "rationale": "The reported failure is that an endpoint-specific setting, the fallback provider entry's base_url, is ignored. The selected atomic skill directly addresses propagating supplied provider endpoint configuration into the provider client before downstream use while leaving unspecified values and existing defaults unchanged. This is a closer causal match than workflows about wire-format adaptation, persisted session routes, error diagnostics, or constructor credential removal. Applicability depends on the defect occurring at the fallback client construction/configuration boundary rather than in later provider-entry selection or URL normalization.",
  "missing_preconditions": [
    "Confirm that the resolved fallback provider entry exposes base_url to the client-construction boundary.",
    "Confirm that the fallback provider uses a client or SDK whose endpoint can be configured per resolved provider entry.",
    "Confirm that compatibility requires applying only an explicitly supplied fallback base_url while retaining the existing default endpoint when it is absent.",
    "The supplied context contains no before/after implementation or call-site evidence proving where the value is dropped."
  ]
}

Use the guidance to localize the problem and choose a safe implementation, but rely on the visible tests and current code as the oracle.