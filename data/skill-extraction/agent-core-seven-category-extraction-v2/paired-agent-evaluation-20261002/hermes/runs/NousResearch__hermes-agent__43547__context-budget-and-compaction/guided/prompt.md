You are solving a held-out implementation task in repository NousResearch/hermes-agent.
The workspace is a synthetic snapshot based on the pre-change parent and has no future Git history. The original solution commit is not available. Work only in this workspace; do not search external services or other repositories. Do not edit the visible regression tests. Inspect the current code, implement the behavior, and run focused tests before finishing.

# Problem family
context budget and compaction

# Issue/task
Context compaction trigger ignores the output-token reservation (custom-provider default max_tokens=65536 halves the usable input budget)

## Summary

The context-compaction trigger compares estimated input tokens against `context_length × compression.threshold`, but the request that actually goes to the provider reserves `max_tokens` **out of that same window**. When `max_tokens` is large, the *effective input budget* (`context_length − max_tokens`) can sit at or below the compaction trigger — so sessions hit a hard provider 400 before proactive compaction ever fires, and the recovery path can't save them.

This is not hypothetical with default settings: for `provider: custom` (vLLM / llama.cpp / LM Studio / Ollama-compatible endpoints), the provider profile defaults `max_tokens` to **65536** when the user hasn't set `model.max_tokens` (`plugins/model-providers/custom/__init__.py` — the deliberate floor added for Ollama's `num_predict=128`, #39281). Against a 131072-token model, that default silently halves the usable input budget.

## Real incident (2026-06-10, Hermes Agent v0.16.0 / upstream a72bb037)

Setup: vLLM 0.22 serving gemma4 with `--max-model-len 131072`; no `model.max_tokens` in config.yaml; `compression.threshold: 0.5`.

- Effective input budget: 131072 − 65536 (profile default) = **65,536 tokens**
- Compaction trigger: 0.5 × 131072 = est. **65,536 tokens** — i.e. *exactly at* the wall
- Aggravator: the rough estimator (`estimate_messages_tokens_rough`, ~chars/4) reported **~43K** when the provider tokenized the same prompt as **≥65,537** (system prompt + tool schemas + chat template + thinking history; ~1.5× undercount) — so by the estimator's reckoning the session was at 33% of the window when it was at 100% of the real input budget.

```
⚠️  API call failed (attempt 1/3): BadRequestError [HTTP 400]
   📝 Error: HTTP 400: This model's maximum context length is 131072 tokens. However, you
   requested 65536 output tokens and your prompt contains at least 65537 input tokens, for a
   total of at least 131073 tokens. Please reduce the length of the input prompt or the number
   of requested output tokens.
   ⏱️  Elapsed: 0.09s  Context: 28 msgs, ~43,089 tokens
⚠️  Context length exceeded, but provider did not report a max context length; keeping context_length at 131,072 tokens and compressing.
🗜️ Context too large (~43,089 tokens) — compressing (1/3)...
🗜️ Compressed 27 → 20 messages, retrying...
   [same 400 again — the retry still requests 65536 output tokens]
❌ Context length exceeded and cannot compress further.
```

The compression retries can't converge: each pass frees a small amount of input while the request keeps reserving the same 65,536 output tokens. (A second, narrower bug made this worse — `parse_available_output_tokens_from_error` doesn't recognize vLLM's token-based phrasing, so the output-cap repair path never engaged. That part is fixed separately in the linked PR.)

## Proposal

Make the input-budget math reservation-aware:

1. **Compaction trigger:** compare estimated input against `(context_length − resolved_output_cap) × threshold` instead of `context_length × threshold`, where `resolved_output_cap` is the same value the transport will put in the request (user `model.max_tokens`, else the provider profile's `default_max_tokens`, else 0).
2. **Pre-flight check:** same substitution anywhere the estimate is compared to `context_length`.
3. Possibly cap the custom-profile default at something like `min(65536, context_length // 4)` once a context length is known — the 65536 floor makes sense for Ollama's tiny `num_predict` default, but it shouldn't consume half of a 131K window.

(1) and (2) are mechanical; (3) is a design question for maintainers since it touches the #39281 fix. Happy to implement whichever shape you prefer — flagging the design first rather than dropping an opinionated PR.

---

I had Claude Fable 5 do this work - this issue was written by the model after it diagnosed the incident live on my own Hermes deployment (custom vLLM endpoint on local hardware). The numbers and logs above are from the real session. As with my previous PRs, my goal is to push Fable to be a useful open-source contributor - if the maintainers find the diagnosis sound, that's the signal I'm looking for.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


# Visible regression tests retained for this evaluation
- tests/agent/test_context_compressor.py

# Validation commands
- `./.venv/bin/pytest -q 'tests/agent/test_context_compressor.py'`
- `git diff --check HEAD`

# Arm
guided

# Retrieved Skill Graph guidance
The following are hypotheses retrieved only from the training repositories using lexical/vector retrieval, optional HNSW, and typed graph expansion. Verify every step against the current code and tests; do not copy repository-specific names blindly.

## Retrieved node 1: pattern — Repair budget decisions at their policy boundary
id: pattern:8105d8c0f3d9ec16
repository: -
score: 0.054540
sources: {"graph": 0.029504685531859445, "lexical": 0.012048192771084338, "lexical_raw": 11.160532013962648, "vector": 0.012987012987012988, "vector_raw": 0.09833129746035561}

When an existing context-related budget resolves to an unsafe value, correct the resolver or threshold provider that owns the decision, preserve stricter constraints and unrelated fallback behavior, and add focused tests that lock the intended precedence. The exact implementation remains conditional on whether the defect is an ordered capability classification or a dynamic-versus-configured limit calculation.

facets:
{"problem_class": "context-budget-and-compaction", "promotion_status": "candidate_pending_holdout"}

payload:
{"action_template": [{"condition": "Apply after tracing the incorrect runtime value to an ordered classifier, threshold provider, or equivalent stable policy boundary.", "purpose": "Change the existing resolver or threshold provider so the affected runtime path receives the evidence-backed budget while preserving stricter constraints and unrelated behavior.", "required": true, "role_id": "repair-budget-policy", "title": "Correct the owning budget policy", "validation": "Inspect or exercise the policy boundary to confirm the affected inputs select the intended value and that the existing consumer still obtains its budget through that boundary."}, {"condition": "Apply after the owning budget policy expresses the intended decision for every implicated dimension.", "purpose": "Encode exact examples for the corrected budget decision, its competing precedence branch, and representative unaffected behavior.", "required": true, "role_id": "lock-budget-contract", "title": "Lock budget precedence with focused checks", "validation": "Focused tests must fail under the prior policy and pass only when the corrected value, the opposite precedence branch, and neighboring fallback or configuration behavior are all preserved."}], "anti_goals": ["Do not globally raise defaults to repair one identifier, call site, or capacity condition.", "Do not broaden or reorder unrelated fallback rules without evidence that their behavior should change.", "Do not rewrite compaction, truncation, persistence, or file-spill mechanisms when their input budget is the defective boundary.", "Do not treat approximate unit conversions as exact tokenization.", "Do not validate only the newly expected value while leaving competing precedence branches and neighboring behavior unconstrained."], "decision_points": [{"branches": [{"action_role_ids": ["repair-budget-policy", "lock-budget-contract"], "condition": "A supported identifier falls through an ordered capability classifier to a broader or default budget."}, {"action_role_ids": ["repair-budget-policy", "lock-budget-contract"], "condition": "A static configured threshold ignores observable remaining capacity at evaluation time."}], "question": "What observable policy defect produces the incorrect budget?"}, {"branches": [{"action_role_ids": ["repair-budget-policy", "lock-budget-contract"], "condition": "Yes; authoritative capabilities or measurable capacity inputs identify the intended result and competing bound."}, {"action_role_ids": [], "condition": "No; the capability is disputed, required usage data is unavailable, or only an ungrounded proxy could be introduced."}], "question": "Can the intended budget and precedence be established from available evidence?"}, {"branches": [{"action_role_ids": ["repair-budget-policy", "lock-budget-contract"], "condition": "Input and output capabilities are maintained in separate ordered classifiers; update and validate each implicated classifier before broader fallbacks."}, {"action_role_ids": ["repair-budget-policy", "lock-budget-contract"], "condition": "The provider combines a configured ceiling with current remaining capacity; select the smaller bound and validate both winner branches."}], "question": "Which repository-specific implementation branch applies?"}], "exclusions": ["Bounded retry, cancellation, and retry-lifecycle observability for generated summaries are separate request-resilience contracts.", "Selecting an ordered summarizer prefix and reconciling a generated summary with a preserved tail are separate compaction-accounting contracts.", "The supporting Actions are not interchangeable: capability classification and remaining-capacity capping realize the same roles through distinct state transitions and validation oracles.", "No untouched holdout repair is present in the supplied graph, so the pattern is not promoted beyond candidate_pending_holdout."], "invariants": ["The repair occurs at the policy boundary that supplies the budget to existing consumers.", "Every independent budget dimension implicated by the defect is updated and validated; correcting only one dimension is insufficient when another can still fall through.", "A specific rule must take precedence over a broader fallback only when evidence supports the specific rule.", "A dynamic capacity-derived bound must not weaken an existing stricter configured ceiling.", "Focused checks must cover both the corrected result and at least one competing or neighboring branch.", "Repository-specific classifier ordering and capacity-conversion logic remain conditional implementations, not universal mandatory steps."], "known_failure_modes": [{"detection": "The affected input or output check passes while another capability lookup still returns a generic or default value.", "failure": "Only one independently resolved budget dimension is corrected.", "mitigation": "Enumerate all implicated dimensions before implementation and include exact focused assertions for each one."}, {"detection": "Representative neighboring identifiers or configurations resolve to new values despite lacking supporting evidence.", "failure": "A specific repair unintentionally changes broader fallback behavior.", "mitigation": "Keep the specific rule ahead of the broad fallback and retain adjacent regression examples for unaffected behavior."}, {"detection": "A controlled case with a smaller configured limit returns the larger capacity-derived value.", "failure": "A dynamic estimate overrides a stricter configured ceiling.", "mitigation": "Use the smaller applicable bound and test both precedence directions, including custom configuration."}, {"detection": "Static call-site inspection or an integration check shows the consumer still reads a constant, stale field, or different resolver.", "failure": "The policy is changed, but the runtime consumer bypasses it.", "mitigation": "Trace the repaired value through the existing consumer boundary and add an integration-level assertion where supported."}, {"detection": "The suite lacks cases for the opposite precedence branch or representative unaffected fallback behavior.", "failure": "Tests prove only the new happy path.", "mitigation": "Add focused branch tests and neighboring regressions before considering the repair complete."}], "missing_probes": ["Apply the two-role policy to a separate untouched repository repair involving an incorrect context-related budget decision.", "Verify in the holdout that the incorrect value is repaired at an existing policy boundary rather than through a downstream workaround.", "Verify in the holdout that focused contract checks, consumer integration checks, and neighboring regressions are all independently observable.", "Obtain successful test execution evidence where the supplied training workflows currently provide committed or static validation without captured local or CI results."], "not_applicable_when": ["No authoritative capability, configured ceiling, or observable current-capacity input exists from which to derive the intended budget.", "The runtime already resolves and consumes the intended budget, indicating that the failure belongs to another layer.", "The affected operation does not obtain its limit through a stable resolver or threshold provider.", "The failure is caused by transient request handling, summary selection, preserved-tail accounting, or another compaction contract rather than budget resolution."], "ordering_constraints": [{"after_role_id": "lock-budget-contract", "before_role_id": "repair-budget-policy", "condition": "The focused regression contract is finalized after the policy boundary expresses all intended dimensions and precedence rules."}], "supporting_workflows": ["workflow:0a319eebe6566d37", "workflow:a7d9ff2248556484"], "validation_ladder": ["Focused contract checks: exercise the repaired resolver or provider with controlled inputs and assert the exact expected budget for every implicated dimension or bound.", "Integration checks: verify the existing runtime configuration or guarded output path still consumes the repaired policy result without bypassing it or replacing the downstream mechanism.", "Regression checks: exercise the competing precedence branch and representative neighboring identifiers, fallback rules, default configuration, or custom configuration to detect unintended widening or weakening.", "Execution check: run the relevant focused test target and applicable package checks when the checkout is executable; otherwise record execution as deferred rather than claiming a pass."], "when_to_use": ["A runtime context, generation, or retained-output budget is demonstrably lower or otherwise different from the value implied by authoritative capability or current-capacity inputs.", "The incorrect value can be traced to a stable policy boundary such as an ordered capability resolver or a threshold provider.", "Multiple independent limits or classifier branches can compete, and the intended winner can be expressed as an observable contract.", "Downstream compaction or truncation behavior is already present and the demonstrated defect is the budget supplied to it rather than the downstream mechanism itself."], "workflow_realizations": [{"evidence_ids": ["E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E10"], "repository": "QwenLM/qwen-code", "role_bindings": [{"action_ids": ["semantic-action:2b8ef8d34d1e1b68"], "role_id": "repair-budget-policy"}, {"action_ids": ["semantic-action:0ccbb58662634c16"], "role_id": "lock-budget-contract"}], "workflow_id": "workflow:0a319eebe6566d37"}, {"evidence_ids": ["E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9", "E10", "E11"], "repository": "google-gemini/gemini-cli", "role_bindings": [{"action_ids": ["semantic-action:7ffb3d9a37cbb643"], "role_id": "repair-budget-policy"}, {"action_ids": ["semantic-action:efb1d3e4e77e58c6"], "role_id": "lock-budget-contract"}], "workflow_id": "workflow:a7d9ff2248556484"}]}

retrieval trace:
- workflow:a7d9ff2248556484 --instantiates/out--> pattern:8105d8c0f3d9ec16
- workflow:a7d9ff2248556484 --supported_by/in--> pattern:8105d8c0f3d9ec16
- pattern-step:3284a7a40a3425494e05682d --declares_step/in--> pattern:8105d8c0f3d9ec16
- pattern-step:0240d285ac6ecc07cd418aa2 --declares_step/in--> pattern:8105d8c0f3d9ec16
- workflow:0a319eebe6566d37 --instantiates/out--> pattern:8105d8c0f3d9ec16
- workflow:0a319eebe6566d37 --supported_by/in--> pattern:8105d8c0f3d9ec16

## Retrieved node 2: workflow — make-tool-output-budget-context-aware
id: workflow:a7d9ff2248556484
repository: google-gemini/gemini-cli
score: 0.042591
sources: {"graph": 0.014218884436673856, "lexical": 0.012987012987012988, "lexical_raw": 13.22149466298999, "vector": 0.015384615384615385, "vector_raw": 0.1728713476240491}

Adapt an existing tool-output truncation path so its budget responds to current context consumption without replacing its configured safety ceiling or its downstream truncation mechanism.

facets:
{"entry_state": "The scheduler already truncates eligible shell output using a configured threshold, but that threshold is independent of how much model context the latest prompt consumed.", "exit_state": "Eligible shell output is passed to the existing truncation mechanism with the smaller of the configured ceiling and the estimated remaining-context character budget, with focused tests covering precedence branches.", "problem_class": "context-budget-and-compaction"}

payload:
{"anti_goals": ["Do not replace or raise a stricter default or user-supplied truncation ceiling.", "Do not rewrite the downstream truncation, file-spill, line-retention, or telemetry behavior when the threshold provider is the missing policy boundary.", "Do not apply this policy to unrelated tool results when the established call site is scoped to successful string output from the shell tool.", "Do not present the four-characters-per-token estimate as exact tokenization."], "entry_state": "The scheduler already truncates eligible shell output using a configured threshold, but that threshold is independent of how much model context the latest prompt consumed.", "exit_state": "Eligible shell output is passed to the existing truncation mechanism with the smaller of the configured ceiling and the estimated remaining-context character budget, with focused tests covering precedence branches.", "goal": "Ensure retained shell output cannot exceed either the configured character ceiling or the estimated space remaining in the active model context.", "not_applicable_when": ["No reliable model context limit or current prompt-usage measurement is available.", "The consumer requires an exact tokenizer-derived byte or token bound rather than an approximate character threshold.", "Tool-output truncation is disabled or the output path does not consume the threshold provider."], "steps": [{"action_id": "semantic-action:7ffb3d9a37cbb643", "action_name": "cap-output-threshold-by-remaining-context", "condition": "Apply when model capacity and latest prompt usage can be read at threshold-evaluation time.", "depends_on": [], "optional": false, "required": true, "role": "implement", "step_id": "step-1", "validation": "Inspect the threshold provider and confirm it selects Math.min of the configured ceiling and four times remaining tokens; confirm the existing scheduler consumes the getter."}, {"action_id": "semantic-action:efb1d3e4e77e58c6", "action_name": "verify-context-aware-threshold-branches", "condition": "Run after the dynamic cap is implemented.", "depends_on": ["cap-output-threshold-by-remaining-context"], "optional": false, "required": true, "role": "validate", "step_id": "step-2", "validation": "The focused unit cases must prove remaining capacity wins when smaller and the default or custom configured ceiling wins when smaller."}], "stop_conditions": ["Stop if the model token limit or latest prompt token count cannot be obtained without introducing an ungrounded proxy.", "Stop if changing the threshold provider would affect consumers whose budget semantics differ from the inspected shell-output call site.", "Stop and repair if the dynamic calculation can exceed the configured ceiling or if custom threshold precedence fails.", "Do not claim runtime validation unless the relevant test command completes successfully."], "validation_ladder": ["Static diff check: the fixed getter is replaced by a minimum of the dynamic remaining-context estimate and configured ceiling.", "Call-site check: the guarded shell-output path still obtains the threshold through the changed provider and passes it to the existing truncation function.", "Focused unit check: verify the 124000 and 4000000 default-ceiling cases.", "Configuration compatibility check: verify both 24000 and 50000 custom-ceiling cases.", "Package check: run the core package's vitest suite when a materialized checkout and dependencies are available."], "when_to_use": ["A tool-output truncation path already accepts a character threshold, but that threshold is static while prompt usage varies.", "The runtime can identify the active model's token capacity and observe the latest prompt token count.", "Oversized tool output can consume context needed for the next model request."]}

retrieval trace:
- pattern:8105d8c0f3d9ec16 --supported_by/out--> workflow:a7d9ff2248556484
- pattern:8105d8c0f3d9ec16 --instantiates/in--> workflow:a7d9ff2248556484
- workflow-step:7182412e72a9c1282edb3c9c --has_step/in--> workflow:a7d9ff2248556484
- workflow-step:1a5a42a3aacd47ce3c8a4000 --has_step/in--> workflow:a7d9ff2248556484

## Retrieved node 3: workflow — repair-model-alias-budget-resolution
id: workflow:0a319eebe6566d37
repository: QwenLM/qwen-code
score: 0.034662
sources: {"graph": 0.018788756303937025, "lexical": 0.015873015873015872, "lexical_raw": 16.78562960994122}

A bounded workflow for correcting an official model name that falls through ordered capability tables and destabilizes long-session compaction, while preserving existing family fallbacks.

facets:
{"entry_state": "The endpoint-accepted alias misses at least one specific capability classifier and receives a generic or default budget inconsistent with its intended model tier.", "exit_state": "The alias resolves to the intended input and output budgets through specific rules ordered before broader fallbacks, and committed regression assertions cover both dimensions plus unaffected family behavior.", "problem_class": "context-budget-and-compaction"}

payload:
{"anti_goals": ["Do not globally raise default context or output limits to accommodate one alias.", "Do not reorder or broaden generic family rules in a way that upgrades older models without evidence.", "Do not change the compaction algorithm when the demonstrated defect is capability classification.", "Do not accept endpoint-incompatible spellings as a substitute for recognizing the endpoint's official identifier."], "entry_state": "The endpoint-accepted alias misses at least one specific capability classifier and receives a generic or default budget inconsistent with its intended model tier.", "exit_state": "The alias resolves to the intended input and output budgets through specific rules ordered before broader fallbacks, and committed regression assertions cover both dimensions plus unaffected family behavior.", "goal": "Ensure a supported official model identifier initializes configuration with its actual input-context and output-generation budgets instead of generic defaults, without changing unrelated model-family behavior.", "not_applicable_when": ["The model identifier is not supported by the target endpoint.", "The authoritative model capability is unknown or disputed.", "The failure persists when configuration already contains the correct input and output budgets.", "The repository does not derive runtime context or output budgets from model-name classification."], "steps": [{"action_id": "semantic-action:2b8ef8d34d1e1b68", "action_name": "align-official-alias-resource-budgets", "condition": "Apply when direct inspection proves that the official identifier falls through one or both ordered capability tables.", "depends_on": [], "optional": false, "required": true, "role": "implement", "step_id": "step-1", "validation": "Static inspection shows the alias is covered by the specific rule before the generic family rule in both input and output classifiers."}, {"action_id": "semantic-action:0ccbb58662634c16", "action_name": "lock-alias-budget-regression-contract", "condition": "Run after both classifier mappings express the intended capability contract.", "depends_on": ["align-official-alias-resource-budgets"], "optional": false, "required": true, "role": "validate", "step_id": "step-2", "validation": "The focused oracle asserts the exact input and output values, while adjacent family assertions constrain unintended widening."}], "stop_conditions": ["Stop if no authoritative input and output limits can be established for the alias.", "Stop if the identifier is rejected by the endpoint; classification changes cannot repair endpoint incompatibility.", "Stop and investigate another layer if the alias already resolves to the correct limits.", "Do not claim runtime validation when the committed test cannot be executed in the supplied checkout."], "validation_ladder": ["Inspect the pre-change ordered classifiers and calculate which specific, generic, or default branches the alias selects.", "Inspect the post-change classifiers to confirm both input and output dimensions recognize the alias before broader fallbacks.", "Run or evaluate the focused unit assertions for the alias's exact input and output limits.", "Run neighboring family assertions to detect unintended classifier widening.", "If the checkout is executable, run the package's focused token-limit test target; otherwise record execution as deferred rather than claiming a pass."], "when_to_use": ["A supported model alias is accepted by the endpoint but resolves to a generic or default token limit.", "Long sessions or compaction fail because the configured context or output budget is lower than the model capability associated with an equivalent versioned name.", "Input and output capabilities are maintained in separate ordered classifiers that can drift or fall through independently."]}

retrieval trace:
- workflow-step:00607e6f51604e1ade101d65 --has_step/in--> workflow:0a319eebe6566d37
- pattern:8105d8c0f3d9ec16 --supported_by/out--> workflow:0a319eebe6566d37
- pattern:8105d8c0f3d9ec16 --instantiates/in--> workflow:0a319eebe6566d37
- workflow-step:361fe1cb5b4b483db0d362ea --has_step/in--> workflow:0a319eebe6566d37

## Retrieved node 4: action — Make future classifier drift or one-sided input/output updates observable in the unit-test suite.
id: semantic-action:0ccbb58662634c16
repository: -
score: 0.040905
sources: {"selected_payload_relation": 0.04090491846746758}

Encode the corrected alias behavior in a focused test that checks both context-window and output-generation limits, with neighboring family tests guarding classifier precedence.

facets:
{"grounded_semantics": true, "module_role": "Model-capability mapping regression suite", "operation": "validate", "problem_class": "context-budget-and-compaction"}

retrieval trace:
- pattern:8105d8c0f3d9ec16 --payload-reference--> semantic-action:0ccbb58662634c16

## Retrieved node 5: action — Prevent a supported model alias from receiving undersized context and output budgets that can trigger premature or truncated long-session compaction.
id: semantic-action:2b8ef8d34d1e1b68
repository: -
score: 0.040905
sources: {"selected_payload_relation": 0.04090491846746758}

Extend the specific, ordered model classifiers so an official alias selects the same input-window and output-capacity tiers as its equivalent versioned family names, without altering older-family fallbacks.

facets:
{"grounded_semantics": true, "module_role": "Model-capability budget resolver used during runtime configuration initialization", "operation": "reconcile", "problem_class": "context-budget-and-compaction"}

retrieval trace:
- pattern:8105d8c0f3d9ec16 --payload-reference--> semantic-action:2b8ef8d34d1e1b68

## Retrieved node 6: action — Prevent a configured shell-output allowance from exceeding the estimated context capacity left after the latest prompt while preserving stricter configured limits.
id: semantic-action:7ffb3d9a37cbb643
repository: -
score: 0.040905
sources: {"selected_payload_relation": 0.04090491846746758}

Derive the output-character threshold from both the configured ceiling and an estimate of remaining model capacity, selecting the smaller value before the existing truncation call site consumes it.

facets:
{"grounded_semantics": true, "module_role": "runtime output-budget policy provider", "operation": "cap", "problem_class": "context-budget-and-compaction"}

retrieval trace:
- pattern:8105d8c0f3d9ec16 --payload-reference--> semantic-action:7ffb3d9a37cbb643

## Retrieved node 7: action — Establish a regression oracle for the precedence between dynamic remaining capacity and the pre-existing configured threshold.
id: semantic-action:efb1d3e4e77e58c6
repository: -
score: 0.040905
sources: {"selected_payload_relation": 0.04090491846746758}

Exercise the threshold policy with controlled capacity and usage values to prove that remaining context wins when smaller and the configured ceiling wins otherwise, including custom configuration.

facets:
{"grounded_semantics": true, "module_role": "output-budget policy test oracle", "operation": "validate", "problem_class": "context-budget-and-compaction"}

retrieval trace:
- pattern:8105d8c0f3d9ec16 --payload-reference--> semantic-action:efb1d3e4e77e58c6

# Applicability judgment
{
  "selected_skill_id": "pattern:8105d8c0f3d9ec16",
  "applicable": true,
  "confidence": 0.96,
  "rationale": "The defect is causally located at an existing budget-policy boundary: ContextCompressor computes its trigger from the raw context window even though the transport reserves max_tokens from that same window. The intended threshold is therefore derived from the observable effective input capacity, context_length minus the resolved output cap, rather than by changing downstream compaction behavior. The visible focused tests lock the corrected value, unchanged no-reservation behavior, degenerate-window fallback, and invalid-value coercion, matching the pattern's repair-at-policy-boundary and neighboring-regression requirements. The repository-specific workflow candidates concern different mechanisms, such as shell-output truncation or model-alias classification, so the cross-workflow budget-policy pattern is the applicable candidate.",
  "missing_preconditions": [
    "The hidden implementation and call sites must confirm that ContextCompressor receives the same resolved output cap the transport actually sends, including the custom provider's default_max_tokens when model.max_tokens is unset.",
    "No execution evidence is supplied showing that the focused pytest command and git diff check passed.",
    "The supplied material does not confirm whether every other pre-flight comparison against context_length was updated to use the same effective input budget."
  ]
}

Use the guidance to localize the problem and choose a safe implementation, but rely on the visible tests and current code as the oracle.