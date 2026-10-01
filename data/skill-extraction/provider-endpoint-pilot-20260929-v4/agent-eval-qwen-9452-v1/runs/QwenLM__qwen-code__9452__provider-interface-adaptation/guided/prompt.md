You are solving a held-out implementation task in repository QwenLM/qwen-code.
The workspace is a synthetic snapshot based on the pre-change parent and has no future Git history. The original solution commit is not available. Work only in this workspace; do not search external services or other repositories. Do not edit the visible regression tests. Inspect the current code, implement the behavior, and run focused tests before finishing.

# Problem family
provider interface adaptation

# Issue/task
switching Responses models or endpoints breaks saved session

Held-out cross-project task in the provider interface adaptation family. Implement the behavior required by the visible regression tests while preserving existing compatibility and error semantics. The original implementation commit is intentionally absent from this snapshot.

# Visible regression tests retained for this evaluation
- packages/core/src/utils/thoughtUtils.test.ts
- packages/core/src/core/anthropicContentGenerator/converter.test.ts
- packages/core/src/core/llm-content-generator/llm-content-generator.test.ts

# Validation commands
- `env CI=1 QWEN_VITEST_GUARD_ROOT=/tmp/arex-qwen-targeted-vitest-root PATH=/home/chenyujia/.local/node22/bin:/home/chenyujia/.local/node22-global/node_modules/.bin:/usr/bin:/bin pnpm exec vitest run --config ./vitest.config.ts --coverage.enabled=false 'packages/core/src/utils/thoughtUtils.test.ts' 'packages/core/src/core/anthropicContentGenerator/converter.test.ts' 'packages/core/src/core/llm-content-generator/llm-content-generator.test.ts'`
- `git diff --check HEAD`

# Arm
guided

# Retrieved Skill Graph guidance
The following are hypotheses retrieved only from the training repositories using lexical/vector retrieval, optional HNSW, and typed graph expansion. Verify every step against the current code and tests; do not copy repository-specific names blindly.

## Retrieved node 1: workflow — adapt-generic-compatible-requests-to-a-stricter-endpoint-contract
id: workflow:ab57da6fa585a2b5
repository: QwenLM/qwen-code
score: 0.049489
sources: {"graph": 0.0267587271852363, "lexical": 0.011235955056179775, "lexical_raw": 2.7986149223977467e-06, "vector": 0.011494252873563218, "vector_raw": 0.0}

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

## Retrieved node 2: action — Apply a compatibility policy only to requests targeting the endpoint whose wire contract requires it, without misrouting other hosts that serve the same model family.
id: semantic-action:30d94e268da81e3a
repository: -
score: 0.037117
sources: {"selected_payload_relation": 0.03711670133623447}

Select an endpoint-specific compatibility adapter using parsed hostname boundaries rather than model-family names or substring matching.

facets:
{"grounded_semantics": true, "module_role": "provider selection boundary", "operation": "classify", "problem_class": "provider-interface-adaptation"}

retrieval trace:
- workflow:ab57da6fa585a2b5 --payload-reference--> semantic-action:30d94e268da81e3a

## Retrieved node 3: action — Demonstrate that replaying a prior thinking turn no longer produces a rejected continuation request.
id: semantic-action:78dd7c430a0fc63d
repository: -
score: 0.037117
sources: {"selected_payload_relation": 0.03711670133623447}

Exercise the complete history-conversion, provider-adaptation, and HTTP path against a strict contract oracle.

facets:
{"grounded_semantics": true, "module_role": "provider wire-contract validation", "operation": "validate", "problem_class": "provider-interface-adaptation"}

retrieval trace:
- workflow:ab57da6fa585a2b5 --payload-reference--> semantic-action:78dd7c430a0fc63d

## Retrieved node 4: action — Prevent strict-schema request rejection without discarding supported replay data, explicit caller intent, or shared history.
id: semantic-action:d0e6aa7cfadb55f2
repository: -
score: 0.037117
sources: {"selected_payload_relation": 0.03711670133623447}

At the outbound boundary, remove only a field recognizable as a derived mirror while retaining the endpoint-supported source field and distinct explicit values.

facets:
{"grounded_semantics": true, "module_role": "outbound provider request adapter", "operation": "reconcile", "problem_class": "provider-interface-adaptation"}

retrieval trace:
- workflow:ab57da6fa585a2b5 --payload-reference--> semantic-action:d0e6aa7cfadb55f2

# Applicability judgment
{
  "selected_skill_id": "workflow:ab57da6fa585a2b5",
  "applicable": true,
  "confidence": 0.93,
  "rationale": "The workflow is causally aligned with the regression contract: saved history contains provider-specific reasoning replay metadata in a shared field; after switching providers, generic conversion would send that metadata as a foreign native signature; the fix must recognize the incompatible payload and remove only that field from the outbound representation while preserving reasoning text, tool-call behavior, native signatures, and the caller-owned history for a possible switch back. Its emphasis on a narrowly routed outbound adapter, preserving shared semantics, and validating complete continuation paths directly matches the Anthropic and Gemini tests. The other workflows concern error formatting, startup endpoint configuration, or persisted route precedence rather than sanitizing provider-specific wire metadata.",
  "missing_preconditions": [
    "The implementation must have a reliable, non-throwing discriminator for the OpenAI Responses replay payload shape rather than treating every thought signature as foreign.",
    "The Anthropic and Gemini request paths must permit wire-only copying or transformation so persisted caller-owned history is not mutated."
  ]
}

Use the guidance to localize the problem and choose a safe implementation, but rely on the visible tests and current code as the oracle.