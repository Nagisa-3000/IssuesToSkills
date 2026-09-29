You are solving a held-out implementation task in repository Aider-AI/aider.
The workspace is a synthetic snapshot based on the pre-change parent and has no future Git history. The original solution commit is not available. Work only in this workspace; do not search external services or other repositories. Do not edit the visible regression tests. Inspect the current code, implement the behavior, and run focused tests before finishing.

# Problem family
provider interface adaptation

# Issue/task
Openrouter compatibility

Held-out cross-project task in the provider interface adaptation family. Implement the behavior required by the visible regression tests while preserving existing compatibility and error semantics. The original implementation commit is intentionally absent from this snapshot.

# Visible regression tests retained for this evaluation
- tests/test_models.py

# Arm
guided

# Retrieved Skill Graph guidance
The following are hypotheses retrieved only from the training repositories using lexical/vector retrieval, optional HNSW, and typed graph expansion. Verify every step against the current code and tests; do not copy repository-specific names blindly.

## Retrieved node 1: pattern — isolate-provider-contract-divergence-at-integration-boundaries
id: pattern:isolate-provider-contract-divergence-at-integration-boundaries
repository: -
score: 0.065553
sources: {"graph": 0.03631663026682665, "lexical": 0.014084507042253521, "lexical_raw": 1.5044125899097079e-06, "vector": 0.015151515151515152, "vector_raw": 0.0}

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
score: 0.103647
sources: {"graph": 0.07333662351121015, "lexical": 0.014925373134328358, "lexical_raw": 1.6410327750264315e-06, "vector": 0.015384615384615385, "vector_raw": 0.0}

Extend a provider-compatible client by centralizing endpoint configuration, reconciling consumer construction, and translating optional routing values only at the invocation boundary.

facets:
{"exclusions": [], "failure_modes": [], "level": "workflow", "preconditions": []}

payload:
{"routing_terms": ["workflow"]}

retrieval trace:
- Aider-AI__aider__88@549a1a76403e309890410f9538bda2fc4f901758:atomic:reconcile-consumer-construction-interface --contains/in--> Aider-AI__aider__88@549a1a76403e309890410f9538bda2fc4f901758:workflow:adapt-a-client-to-provider-specific-endpoint-contracts
- Aider-AI__aider__88@549a1a76403e309890410f9538bda2fc4f901758:atomic:forward-optional-provider-routing-fields --contains/in--> Aider-AI__aider__88@549a1a76403e309890410f9538bda2fc4f901758:workflow:adapt-a-client-to-provider-specific-endpoint-contracts
- Aider-AI__aider__88@549a1a76403e309890410f9538bda2fc4f901758:atomic:centralize-provider-sdk-configuration --contains/in--> Aider-AI__aider__88@549a1a76403e309890410f9538bda2fc4f901758:workflow:adapt-a-client-to-provider-specific-endpoint-contracts
- pattern:isolate-provider-contract-divergence-at-integration-boundaries --contains/out--> Aider-AI__aider__88@549a1a76403e309890410f9538bda2fc4f901758:workflow:adapt-a-client-to-provider-specific-endpoint-contracts

## Retrieved node 3: workflow — adapt-generic-compatible-requests-to-a-stricter-endpoint-contract
id: QwenLM/qwen-code#11657@3ba01990e13e9e8e14e147b60add50e0f972431a:workflow:adapt-generic-compatible-requests-to-a-stricter-endpoint-contract
repository: -
score: 0.101130
sources: {"graph": 0.07209920930225366, "lexical": 0.013157894736842105, "lexical_raw": 1.1791211866778619e-06, "vector": 0.015873015873015872, "vector_raw": 0.07999610686192105}

Introduce a narrowly routed outbound adapter when a nominally compatible endpoint rejects a generic provider transformation, preserving shared semantics and verifying the complete continuation path.

facets:
{"exclusions": [], "failure_modes": [], "level": "workflow", "preconditions": []}

payload:
{"routing_terms": ["workflow"]}

retrieval trace:
- QwenLM/qwen-code#11657@3ba01990e13e9e8e14e147b60add50e0f972431a:atomic:classify-compatible-endpoint-by-canonical-hostname --contains/in--> QwenLM/qwen-code#11657@3ba01990e13e9e8e14e147b60add50e0f972431a:workflow:adapt-generic-compatible-requests-to-a-stricter-endpoint-contract
- QwenLM/qwen-code#11657@3ba01990e13e9e8e14e147b60add50e0f972431a:atomic:validate-strict-endpoint-multiturn-continuation --contains/in--> QwenLM/qwen-code#11657@3ba01990e13e9e8e14e147b60add50e0f972431a:workflow:adapt-generic-compatible-requests-to-a-stricter-endpoint-contract
- pattern:isolate-provider-contract-divergence-at-integration-boundaries --contains/out--> QwenLM/qwen-code#11657@3ba01990e13e9e8e14e147b60add50e0f972431a:workflow:adapt-generic-compatible-requests-to-a-stricter-endpoint-contract
- QwenLM/qwen-code#11657@3ba01990e13e9e8e14e147b60add50e0f972431a:atomic:remove-only-derived-incompatible-wire-field --contains/in--> QwenLM/qwen-code#11657@3ba01990e13e9e8e14e147b60add50e0f972431a:workflow:adapt-generic-compatible-requests-to-a-stricter-endpoint-contract

## Retrieved node 4: workflow — surface-hidden-http-error-details-at-provider-boundaries
id: earendil-works/pi#5832@6fbeba51af98a37a0695ec8b53308dde81d9ab46:workflow:surface-hidden-http-error-details-at-provider-boundaries
repository: -
score: 0.098166
sources: {"graph": 0.06754435349509783, "lexical": 0.014492753623188406, "lexical_raw": 1.5869881074099986e-06, "vector": 0.016129032258064516, "vector_raw": 0.08049512220836638}

Establish one bounded error contract, compose it without duplication, adopt it at affected provider boundaries while preserving local behavior, and verify both utility semantics and representative catch paths.

facets:
{"exclusions": [], "failure_modes": [], "level": "workflow", "preconditions": []}

payload:
{"routing_terms": ["workflow"]}

retrieval trace:
- earendil-works/pi#5832@6fbeba51af98a37a0695ec8b53308dde81d9ab46:atomic:normalize-heterogeneous-provider-failures --contains/in--> earendil-works/pi#5832@6fbeba51af98a37a0695ec8b53308dde81d9ab46:workflow:surface-hidden-http-error-details-at-provider-boundaries
- earendil-works/pi#5832@6fbeba51af98a37a0695ec8b53308dde81d9ab46:atomic:adapt-provider-catch-boundaries --contains/in--> earendil-works/pi#5832@6fbeba51af98a37a0695ec8b53308dde81d9ab46:workflow:surface-hidden-http-error-details-at-provider-boundaries
- earendil-works/pi#5832@6fbeba51af98a37a0695ec8b53308dde81d9ab46:atomic:compose-nonduplicating-provider-diagnostic --contains/in--> earendil-works/pi#5832@6fbeba51af98a37a0695ec8b53308dde81d9ab46:workflow:surface-hidden-http-error-details-at-provider-boundaries
- earendil-works/pi#5832@6fbeba51af98a37a0695ec8b53308dde81d9ab46:atomic:validate-provider-diagnostic-contract --contains/in--> earendil-works/pi#5832@6fbeba51af98a37a0695ec8b53308dde81d9ab46:workflow:surface-hidden-http-error-details-at-provider-boundaries

## Retrieved node 5: workflow — adapt-session-resume-to-a-versioned-provider-route
id: NousResearch/hermes-agent#125942@33c6ab002d1fac653d7e772025ef7aaab7c83480:workflow:adapt-session-resume-to-a-versioned-provider-route
repository: -
score: 0.067824
sources: {"graph": 0.03580535714285714, "lexical": 0.015625, "lexical_raw": 2.111187021597022, "vector": 0.01639344262295082, "vector_raw": 0.08627946668834321}

Establish one precedence-aware interpretation of persisted provider-interface state, then make each resume consumer delegate route extraction to it and validate conflicts between new and legacy representations.

facets:
{"exclusions": [], "failure_modes": [], "level": "workflow", "preconditions": []}

payload:
{"routing_terms": ["workflow"]}

retrieval trace:
- NousResearch/hermes-agent#125942@33c6ab002d1fac653d7e772025ef7aaab7c83480:atomic:resolve-persisted-route-by-freshness --contains/in--> NousResearch/hermes-agent#125942@33c6ab002d1fac653d7e772025ef7aaab7c83480:workflow:adapt-session-resume-to-a-versioned-provider-route
- NousResearch/hermes-agent#125942@33c6ab002d1fac653d7e772025ef7aaab7c83480:atomic:delegate-resume-consumer-to-canonical-route-reader --contains/in--> NousResearch/hermes-agent#125942@33c6ab002d1fac653d7e772025ef7aaab7c83480:workflow:adapt-session-resume-to-a-versioned-provider-route

## Retrieved node 6: atomic — resolve-persisted-route-by-freshness
id: NousResearch/hermes-agent#125942@33c6ab002d1fac653d7e772025ef7aaab7c83480:atomic:resolve-persisted-route-by-freshness
repository: -
score: 0.050262
sources: {"graph": 0.020747950819672133, "lexical": 0.013888888888888888, "lexical_raw": 1.4715333566189313e-06, "vector": 0.015625, "vector_raw": 0.0728033699974309}

Normalize multiple persisted route representations into one provider/endpoint/wire tuple using explicit freshness precedence: the latest nested runtime route first, then legacy top-level fields, with a routable billing identity only filling a missing provider.

facets:
{"exclusions": [], "failure_modes": [], "level": "atomic", "preconditions": []}

payload:
{"routing_terms": ["atomic"]}

retrieval trace:
- NousResearch/hermes-agent#125942@33c6ab002d1fac653d7e772025ef7aaab7c83480:workflow:adapt-session-resume-to-a-versioned-provider-route --contains/out--> NousResearch/hermes-agent#125942@33c6ab002d1fac653d7e772025ef7aaab7c83480:atomic:resolve-persisted-route-by-freshness

## Retrieved node 7: atomic — delegate-resume-consumer-to-canonical-route-reader
id: NousResearch/hermes-agent#125942@33c6ab002d1fac653d7e772025ef7aaab7c83480:atomic:delegate-resume-consumer-to-canonical-route-reader
repository: -
score: 0.049740
sources: {"graph": 0.020747950819672133, "lexical": 0.014285714285714285, "lexical_raw": 1.564426290382473e-06, "vector": 0.014705882352941176, "vector_raw": -0.062162857189978354}

Replace a consumer-specific reconstruction of persisted provider metadata with the canonical session-route resolver before applying existing endpoint-safety and provider-healing logic.

facets:
{"exclusions": [], "failure_modes": [], "level": "atomic", "preconditions": []}

payload:
{"routing_terms": ["atomic"]}

retrieval trace:
- NousResearch/hermes-agent#125942@33c6ab002d1fac653d7e772025ef7aaab7c83480:workflow:adapt-session-resume-to-a-versioned-provider-route --contains/out--> NousResearch/hermes-agent#125942@33c6ab002d1fac653d7e772025ef7aaab7c83480:atomic:delegate-resume-consumer-to-canonical-route-reader

## Retrieved node 8: atomic — reconcile-consumer-construction-interface
id: Aider-AI__aider__88@549a1a76403e309890410f9538bda2fc4f901758:atomic:reconcile-consumer-construction-interface
repository: -
score: 0.049598
sources: {"graph": 0.019640872560275545, "lexical": 0.015873015873015872, "lexical_raw": 2.670892966526194, "vector": 0.014084507042253521, "vector_raw": -0.07333608310403039}

Remove provider credentials from the consumer factory contract and migrate production and test callers to the configuration-independent constructor.

facets:
{"exclusions": [], "failure_modes": [], "level": "atomic", "preconditions": []}

payload:
{"routing_terms": ["atomic"]}

retrieval trace:
- Aider-AI__aider__88@549a1a76403e309890410f9538bda2fc4f901758:workflow:adapt-a-client-to-provider-specific-endpoint-contracts --contains/out--> Aider-AI__aider__88@549a1a76403e309890410f9538bda2fc4f901758:atomic:reconcile-consumer-construction-interface

# Applicability judgment
{
  "selected_skill_id": null,
  "applicable": false,
  "confidence": 0.94,
  "rationale": "The supplied context identifies only a broad provider-interface-adaptation task and names OpenRouter, but provides no implementation, call-site, test assertions, or execution evidence showing the actual contract divergence. Consequently, it is not possible to establish that the change requires endpoint configuration, constructor reconciliation, optional routing fields, hostname-based classification, wire-field removal, error normalization, or persisted-route resolution. Selecting any candidate would rely on titles, repository identity, or retrieval scores rather than causal semantic evidence.",
  "missing_preconditions": [
    "Contents and assertions of tests/test_models.py",
    "Relevant provider/model implementation and call sites",
    "Observed failing behavior or provider contract mismatch",
    "Evidence identifying the required request, endpoint, construction, routing, or error-semantics adaptation"
  ]
}

Use the guidance to localize the problem and choose a safe implementation, but rely on the visible tests and current code as the oracle.