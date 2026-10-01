You are solving a held-out implementation task in repository earendil-works/pi.
The workspace is a synthetic snapshot based on the pre-change parent and has no future Git history. The original solution commit is not available. Work only in this workspace; do not search external services or other repositories. Do not edit the visible regression tests. Inspect the current code, implement the behavior, and run focused tests before finishing.

# Problem family
provider interface adaptation

# Issue/task
fix(ai): openai-completions - throw error on missing finish-reason

Held-out cross-project task in the provider interface adaptation family. Implement the behavior required by the visible regression tests while preserving existing compatibility and error semantics. The original implementation commit is intentionally absent from this snapshot.

# Visible regression tests retained for this evaluation
- packages/ai/test/openai-completions-tool-choice.test.ts
- packages/agent/test/harness/skills.test.ts
- packages/agent/test/harness/session.test.ts
- packages/agent/test/harness/storage.test.ts
- packages/agent/test/harness/compaction.test.ts
- packages/agent/test/harness/nodejs-env.test.ts

# Arm
guided

# Retrieved Skill Graph guidance
The following are hypotheses retrieved only from the training repositories using lexical/vector retrieval, optional HNSW, and typed graph expansion. Verify every step against the current code and tests; do not copy repository-specific names blindly.

## Retrieved node 1: pattern — Resolve provider interface adaptation through a contract-first, evidence-validated change chain.
id: pattern:5895d079305884e4
repository: -
score: 0.039552
sources: {"graph": 0.007774406670035633, "lexical": 0.015384615384615385, "lexical_raw": 5.320363272787868e-06, "vector": 0.01639344262295082, "vector_raw": 0.4135423805446677}

Resolve provider interface adaptation through a contract-first, evidence-validated change chain.

facets:
{"problem_class": "provider-interface-adaptation", "promotion_status": "insufficient-structural-support"}

payload:
{"decision_points": []}

retrieval trace:
- workflow:db028c1199198681 --supported_by/in--> pattern:5895d079305884e4
- workflow:ab57da6fa585a2b5 --supported_by/in--> pattern:5895d079305884e4
- workflow:39fa8a7327fff902 --supported_by/in--> pattern:5895d079305884e4
- workflow:4b61c655f3f3c32e --supported_by/in--> pattern:5895d079305884e4

## Retrieved node 2: workflow — surface-hidden-http-error-details-at-provider-boundaries
id: workflow:db028c1199198681
repository: earendil-works/pi
score: 0.065741
sources: {"graph": 0.033474703383615814, "lexical": 0.01639344262295082, "lexical_raw": 2.7665243781009865, "vector": 0.015873015873015872, "vector_raw": 0.20942001007230504}

Establish one bounded error contract, compose it without duplication, adopt it at affected provider boundaries while preserving local behavior, and verify both utility semantics and representative catch paths.

facets:
{"entry_state": "Multiple provider adapters own incompatible catch formatting, and gateway or proxy failures can expose only an opaque SDK message even though the thrown object retains a status and body.", "exit_state": "Affected adapters expose a bounded status/body diagnostic without double-printing existing content and without losing adapter-specific prefixes, categories, hints, stop reasons, or supplemental metadata.", "problem_class": "provider-interface-adaptation"}

payload:
{"entry_state": "Multiple provider adapters own incompatible catch formatting, and gateway or proxy failures can expose only an opaque SDK message even though the thrown object retains a status and body.", "exit_state": "Affected adapters expose a bounded status/body diagnostic without double-printing existing content and without losing adapter-specific prefixes, categories, hints, stop reasons, or supplemental metadata.", "goal": "Return actionable provider HTTP failure details when an SDK exposes the status and response body outside its opaque Error.message.", "steps": [{"action_id": "semantic-action:9cbf99d39f855621", "optional": false, "role": "establish-contract", "step_id": "step-1"}, {"action_id": "semantic-action:d6f919dc5f5f465a", "optional": false, "role": "reconcile", "step_id": "step-2"}, {"action_id": "semantic-action:8ce6b0f7e8c07846", "optional": false, "role": "implement", "step_id": "step-3"}, {"action_id": "semantic-action:5f86bf02fd2a0ba6", "optional": false, "role": "validate", "step_id": "step-4"}]}

retrieval trace:
- pattern:5895d079305884e4 --supported_by/out--> workflow:db028c1199198681
- workflow-step:07df949874c4724a977e6444 --has_step/in--> workflow:db028c1199198681
- workflow-step:521acd9dbdb89d8b31c29406 --has_step/in--> workflow:db028c1199198681
- workflow-step:29940af7c04894a8ee60a6ca --has_step/in--> workflow:db028c1199198681
- workflow-step:c5fb77d2b15ab0e189b7a1b1 --has_step/in--> workflow:db028c1199198681

## Retrieved node 3: workflow — adapt-generic-compatible-requests-to-a-stricter-endpoint-contract
id: workflow:ab57da6fa585a2b5
repository: QwenLM/qwen-code
score: 0.053453
sources: {"graph": 0.02683281000212007, "lexical": 0.011235955056179775, "lexical_raw": 2.7986149223977467e-06, "vector": 0.015384615384615385, "vector_raw": 0.14553096750905498}

Introduce a narrowly routed outbound adapter when a nominally compatible endpoint rejects a generic provider transformation, preserving shared semantics and verifying the complete continuation path.

facets:
{"entry_state": "A generic compatible-provider transformation derives an extra message field from preserved history, and the actual endpoint rejects that field during multi-turn continuation.", "exit_state": "The affected endpoint is safely identified, only the derived incompatible field is removed from an outbound copy, other endpoint behavior is unchanged, and a strict HTTP oracle accepts the continuation wire shape.", "problem_class": "provider-interface-adaptation"}

payload:
{"entry_state": "A generic compatible-provider transformation derives an extra message field from preserved history, and the actual endpoint rejects that field during multi-turn continuation.", "exit_state": "The affected endpoint is safely identified, only the derived incompatible field is removed from an outbound copy, other endpoint behavior is unchanged, and a strict HTTP oracle accepts the continuation wire shape.", "goal": "Allow thinking-history and tool-call continuations to satisfy the stricter endpoint schema without weakening behavior for other compatible endpoints or deleting supported replay data.", "steps": [{"action_id": "semantic-action:30d94e268da81e3a", "optional": false, "role": "establish-contract", "step_id": "step-1"}, {"action_id": "semantic-action:d0e6aa7cfadb55f2", "optional": false, "role": "reconcile", "step_id": "step-2"}, {"action_id": "semantic-action:78dd7c430a0fc63d", "optional": false, "role": "validate", "step_id": "step-3"}]}

retrieval trace:
- pattern:5895d079305884e4 --supported_by/out--> workflow:ab57da6fa585a2b5
- workflow-step:3e518f3b47d2951658aab8c7 --has_step/in--> workflow:ab57da6fa585a2b5
- workflow-step:029639794ba1b68d0f6727c2 --has_step/in--> workflow:ab57da6fa585a2b5
- workflow-step:ee2eeebab78d2395ab04f672 --has_step/in--> workflow:ab57da6fa585a2b5

## Retrieved node 4: workflow — adapt-a-client-to-provider-specific-endpoint-contracts
id: workflow:4b61c655f3f3c32e
repository: Aider-AI/aider
score: 0.050475
sources: {"graph": 0.02676532196243553, "lexical": 0.012345679012345678, "lexical_raw": 3.565215777546965e-06, "vector": 0.011363636363636364, "vector_raw": 0.0}

Extend a provider-compatible client by centralizing endpoint configuration, reconciling consumer construction, and translating optional routing values only at the invocation boundary.

facets:
{"entry_state": "The client supports a generic key/base configuration, configuration mutation occurs inside a downstream factory, and provider-specific routing values cannot reach the request call.", "exit_state": "Application startup initializes all supplied provider settings, the consumer factory is configuration-independent, known callers use its revised interface, and configured request-routing identifiers are forwarded conditionally.", "problem_class": "provider-interface-adaptation"}

payload:
{"entry_state": "The client supports a generic key/base configuration, configuration mutation occurs inside a downstream factory, and provider-specific routing values cannot reach the request call.", "exit_state": "Application startup initializes all supplied provider settings, the consumer factory is configuration-independent, known callers use its revised interface, and configured request-routing identifiers are forwarded conditionally.", "goal": "Permit the same application to invoke a compatible provider endpoint whose SDK and request contracts require optional endpoint metadata, without forcing provider configuration through the consumer factory.", "steps": [{"action_id": "semantic-action:7d6b49a1ecedb342", "optional": false, "role": "establish-contract", "step_id": "step-1"}, {"action_id": "semantic-action:2d6a7a39e552adce", "optional": false, "role": "reconcile", "step_id": "step-2"}, {"action_id": "semantic-action:db6b4ad8c741d3ab", "optional": false, "role": "implement", "step_id": "step-3"}]}

retrieval trace:
- pattern:5895d079305884e4 --supported_by/out--> workflow:4b61c655f3f3c32e
- workflow-step:65874e2762aa4d07800157cc --has_step/in--> workflow:4b61c655f3f3c32e
- workflow-step:b1b00041f6eee4a0865fa0f7 --has_step/in--> workflow:4b61c655f3f3c32e
- workflow-step:d85505948898595489906eef --has_step/in--> workflow:4b61c655f3f3c32e

## Retrieved node 5: workflow — adapt-session-resume-to-a-versioned-provider-route
id: workflow:39fa8a7327fff902
repository: NousResearch/hermes-agent
score: 0.045314
sources: {"graph": 0.01993241828993552, "lexical": 0.012048192771084338, "lexical_raw": 3.352610518709152e-06, "vector": 0.013333333333333334, "vector_raw": 0.022873608236374382}

Establish one precedence-aware interpretation of persisted provider-interface state, then make each resume consumer delegate route extraction to it and validate conflicts between new and legacy representations.

facets:
{"entry_state": "A producer persists the latest route in a nested runtime object, but at least one consumer independently reconstructs the route from older top-level fields and a potentially stale billing identity.", "exit_state": "Persisted route precedence is centralized and all relevant resume consumers use it; conflicting-representation tests select the latest nested route and legacy endpoint-safety coverage remains intact.", "problem_class": "provider-interface-adaptation"}

payload:
{"entry_state": "A producer persists the latest route in a nested runtime object, but at least one consumer independently reconstructs the route from older top-level fields and a potentially stale billing identity.", "exit_state": "Persisted route precedence is centralized and all relevant resume consumers use it; conflicting-representation tests select the latest nested route and legacy endpoint-safety coverage remains intact.", "goal": "Resume a session using its latest persisted provider, endpoint, and wire protocol without regressing compatible legacy rows or existing endpoint-safety rules.", "steps": [{"action_id": "semantic-action:dd484e564659b2bd", "optional": false, "role": "establish-contract", "step_id": "step-1"}, {"action_id": "semantic-action:dd2d4348a148e6cd", "optional": false, "role": "implement", "step_id": "step-2"}]}

retrieval trace:
- pattern:5895d079305884e4 --supported_by/out--> workflow:39fa8a7327fff902
- workflow-step:8c3351aed27cd54ae8ff938e --has_step/in--> workflow:39fa8a7327fff902
- workflow-step:d12e9d27e35c526fe2457a3e --has_step/in--> workflow:39fa8a7327fff902

## Retrieved node 6: action — Keep separate resume surfaces from interpreting the same persisted provider interface differently.
id: semantic-action:dd2d4348a148e6cd
repository: -
score: 0.068668
sources: {"graph": 0.040222144338745436, "lexical": 0.01282051282051282, "lexical_raw": 4.11859323472184e-06, "validation_closure": 0.03868531958212477, "vector": 0.015625, "vector_raw": 0.15232268704610685}

Replace a consumer-specific reconstruction of persisted provider metadata with the canonical session-route resolver before applying existing endpoint-safety and provider-healing logic.

facets:
{"grounded_semantics": true, "module_role": "session-resume runtime adapter", "operation": "adapt", "problem_class": "provider-interface-adaptation"}

retrieval trace:
- semantic-action:dd484e564659b2bd --enables/out--> semantic-action:dd2d4348a148e6cd
- semantic-action:dd484e564659b2bd --validates/in--> semantic-action:dd2d4348a148e6cd
- workflow-step:8c3351aed27cd54ae8ff938e --executed_by/out--> semantic-action:dd2d4348a148e6cd
- semantic-action:dd2d4348a148e6cd --validates--> semantic-action:dd484e564659b2bd

## Retrieved node 7: action — Make provider-facing text, response, streaming, and image entry points consistently return actionable HTTP failure details.
id: semantic-action:8ce6b0f7e8c07846
repository: -
score: 0.063798
sources: {"graph": 0.033680095160376906, "lexical": 0.015625, "lexical_raw": 1.7163190502037906, "validation_closure": 0.032725156567575374, "vector": 0.014492753623188406, "vector_raw": 0.10050378152592121}

Replace adapter-local message-only formatting with the shared diagnostic contract while retaining adapter-specific semantics such as category prefixes, hints, and supplemental metadata.

facets:
{"grounded_semantics": true, "module_role": "provider adapter error boundary", "operation": "adapt", "problem_class": "provider-interface-adaptation"}

retrieval trace:
- workflow-step:07df949874c4724a977e6444 --executed_by/out--> semantic-action:8ce6b0f7e8c07846
- semantic-action:d6f919dc5f5f465a --enables/out--> semantic-action:8ce6b0f7e8c07846
- semantic-action:5f86bf02fd2a0ba6 --validates/in--> semantic-action:8ce6b0f7e8c07846
- semantic-action:8ce6b0f7e8c07846 --validates--> semantic-action:5f86bf02fd2a0ba6

## Retrieved node 8: action — Keep provider initialization at the application boundary while preserving construction of the request consumer across all known callers.
id: semantic-action:2d6a7a39e552adce
repository: -
score: 0.063081
sources: {"graph": 0.03542986259180289, "lexical": 0.0125, "lexical_raw": 3.7343179639006616e-06, "validation_closure": 0.03911510524415957, "vector": 0.015151515151515152, "vector_raw": 0.13689333631303308}

Remove provider credentials from the consumer factory contract and migrate production and test callers to the configuration-independent constructor.

facets:
{"grounded_semantics": true, "module_role": "consumer factory interface and its call sites", "operation": "reconcile", "problem_class": "provider-interface-adaptation"}

retrieval trace:
- workflow-step:65874e2762aa4d07800157cc --executed_by/out--> semantic-action:2d6a7a39e552adce
- semantic-action:7d6b49a1ecedb342 --enables/out--> semantic-action:2d6a7a39e552adce
- semantic-action:7d6b49a1ecedb342 --validates/in--> semantic-action:2d6a7a39e552adce
- semantic-action:2d6a7a39e552adce --validates--> semantic-action:7d6b49a1ecedb342

# Applicability judgment
{
  "selected_skill_id": null,
  "applicable": false,
  "confidence": 0.96,
  "rationale": "No candidate is supported by causal implementation or test evidence. The specific workflows and actions address HTTP error-detail formatting, outbound request adaptation, endpoint configuration, or persisted session routing; none establishes semantics for validating a completion response whose finish reason is absent. The generic provider-interface pattern cannot be selected solely from the task category and issue title, especially because the supplied snapshot omits the implementation, call sites, test contents, and behavioral evidence needed to determine equivalence.",
  "missing_preconditions": [
    "The current OpenAI completions response parsing and continuation control flow",
    "The visible regression test assertions for an absent finish reason",
    "The required error type, message, and propagation behavior",
    "Evidence showing where compatibility behavior must be preserved and whether streaming and non-streaming paths are both affected"
  ]
}

Use the guidance to localize the problem and choose a safe implementation, but rely on the visible tests and current code as the oracle.