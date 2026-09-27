# Candidate Atomic Skills — DeepSeek Harness case only

> Status: **provisional Atomic candidates**, supported by one real DeepSeek Harness realization. These are semantic candidates, not patch names, file recipes, or Workflow/Pattern registrations. A second independent realization or held-out transfer is required before `reviewed` promotion.

## AC-derive-residual-pressure-budget

### Identity

- **id:** `AC-derive-residual-pressure-budget`
- **name:** `derive-residual-pressure-budget`
- **version:** `0.1.0`
- **title:** Derive proactive pressure from residual message capacity
- **confidence:** provisional / medium; one direct realization with strong unit and replay oracles

### Discovery

- **description:** Derives a proactive pressure threshold and retained-tail budget when a mandatory downstream output reservation and explicit safety headroom consume the same finite capacity as upstream messages. Use when a pressure gate is based on nominal capacity and can fire after the provider's admissible message budget has already been exhausted.
- **problem_signature:** threshold uses nominal capacity while output reservation and pressure headroom are charged to that capacity.
- **observable_cues:**
  - A model window has a request output cap charged to the same context window.
  - The provider rejects prompts near `W - O`, while the current pressure threshold is derived from `W`.
  - A compaction policy has a configurable threshold ratio and a retained-tail budget.
  - The implementation has no explicit residual-budget invariant.

### Boundary

- **preconditions:**
  - One finite capacity `W` is shared by message input, mandatory routed output reservation `O`, and pressure headroom `B`.
  - The pressure policy has a threshold ratio `r` and either ratio or explicit retention.
  - The implementation can obtain `W`, `O`, and `B` at the policy-resolution seam.
- **exclusions:**
  - Physically isolated capacity pools.
  - Preemptible or advisory output reservations that are not part of the provider admission invariant.
  - Provider-confirmed overflow recovery when no proactive pressure policy is being repaired.
  - A case where retention itself is defined against a different capacity pool.
- **non_goals:**
  - Choosing a provider or model.
  - Designing the compaction transaction or summary format.
  - Silently clamping invalid configurations.

### Problem mechanism and semantic roles

- **problem_mechanism:** A nominal-capacity threshold admits upstream history that competes with a mandatory downstream reservation. The provider can reject the request before the proactive gate is reached.
- **semantic_roles:**
  - `W`: nominal shared capacity.
  - `O`: mandatory routed output reservation.
  - `M`: message budget after reservation, `W - O`.
  - `B`: additional pressure headroom.
  - `P`: residual pressure budget, `M - B`.
  - `r`: nominal pressure ratio.
  - `T`: proactive threshold.

### Contract

- **required_inputs:** `W`, `O`, `B`, `r`, retention policy, target identity for errors.
- **produced_outputs:** immutable derived spec containing `T`, resolved retained tokens, and the target; a target-specific configuration error for invalid boundaries.
- **parameter_slots:** `capacity`, `mandatory_reservation`, `pressure_headroom`, `threshold_ratio`, `retention_form`, `target_key`.
- **variation_points:** whether `O` comes from a durable request envelope or an adapter default; whether retention is ratio or explicit; numeric types and rounding policy.

### Solution principle

Derive policy from the capacity available to messages, not from nominal capacity alone. For this realization:

1. Compute `M = W - O`.
2. Require `M > 0`.
3. Compute `P = M - B` and require `P > 0`.
4. Set `T = floor(min(W * r, P))`.
5. For ratio retention, use `floor(M * retainRatio)`; preserve explicit `retainTokens` as explicit.
6. Require the resolved retained budget to be strictly below `T`.

The headroom is a pressure safety margin; it is not silently substituted for the retained-tail budget.

### Invariants

- `O >= 0` and is an integer.
- `M = W - O`.
- `P = W - O - B`.
- `T <= P`.
- Ratio retention is derived from `M`, not from `W`.
- `retainTokens < T`.
- Invalid `M <= 0` or `P <= 0` is an actionable target-specific failure, not silent disablement.

### Validation oracle

- Numeric unit: `W=1,048,576`, `O=256,000`, `r=.8`, `B=65,536`, `retainRatio=.16` yields `T=634,060` and `retainTokens=126,812`.
- Compatibility unit: `W=1,000`, `O=0`, `r=.8`, `B=0` yields `T=800` and `retainTokens=160`.
- Boundary unit: reject negative/non-integer `O`, `O >= W`, `W-O-B <= 0`, and `retainTokens >= T`.
- Behavioral unit: the same measured history remains below the nominal threshold without a reservation but triggers after the durable output reservation lowers `T`.
- Evidence: `EU-RESIDUAL-FORMULA`, `EU-BOUNDARY-GUARDS`, `EU-UNIT-ORACLE`, realized by `CA3` and `CA5`.

### Failure modes

- Retaining the old `floor(W * r)` threshold.
- Subtracting `B` from ratio retention when the contract defines retention against message budget `M`.
- Double-subtracting a reservation that was already removed upstream.
- Treating `O > W` as zero available capacity and continuing.
- Clamping `P <= 0` to a small threshold without surfacing the route and configuration.
- Returning a mutable or stale budget when the route/capacity changes.

### Realization mapping

- **Case:** `deepseek-compaction-reservation`.
- **Case actions:** `CA1` diagnosis, `CA3` residual transformation, `CA5` boundary validation.
- **Code:** `/home/chenyujia/tritonToLlvm/deepseek-harness/packages/compaction/compaction-basic/src/config.ts:141-216`.
- **Tests:** `/home/chenyujia/tritonToLlvm/deepseek-harness/packages/compaction/compaction-basic/tests/compaction-basic.spec.ts:308-445, 627-680`.
- **Supporting commits:** `0fadb08fbdd3316c4605fc4e6be96cb9990b56c6`, `555b664b08db05e1cf8eeebb7eb00960ddf785b7`, `9b016b642503ff798faec65c860e948cc14f99cc`.

### Abstraction assessment and delivery

- **abstraction_assessment:** Strongly semantic for shared-capacity pressure, but the “ratio retention uses `M` while pressure uses `P`” detail is a realization-specific contract until another system confirms it.
- **counterexamples to hold out:** isolated input/output pools; soft output caps not counted by admission; a policy whose threshold is already defined on residual capacity.
- **routing_view:** trigger on shared-capacity pressure, nominal-window thresholds, provider rejection before compaction, or residual-budget terminology.
- **execution_view:** load capacity/reservation/headroom facts, derive `M/P/T`, validate boundaries, then check numeric and dynamic oracles.
- **reference_files:** `evidence.md`, `case.json`; no script proposed from this single case.

---

## AC-bind-effective-output-reservation

### Identity

- **id:** `AC-bind-effective-output-reservation`
- **name:** `bind-effective-output-reservation`
- **version:** `0.1.0`
- **title:** Bind a capacity policy to the effective routed output reservation
- **confidence:** provisional / medium; one direct call-point realization with explicit-header and adapter-default tests

### Discovery

- **description:** Binds a shared-capacity policy calculation to the output reservation of the actual routed request, including the configured-envelope and adapter-default fallback chain. Use when the pressure resolver sees model capacity but not the effective request output cap, or when provider/model switching can make a cached reservation stale.
- **problem_signature:** capacity metadata and request-envelope output cap exist in separate services or records, and the policy seam accepts only nominal capacity.
- **observable_cues:**
  - A durable request header records provider/model and may record `maxTokens`.
  - Model metadata exposes `contextWindow` and `defaultMaxTokens`.
  - The wire serializer uses an output-cap precedence chain.
  - Tests distinguish explicit request cap from adapter fallback.

### Boundary

- **preconditions:**
  - A durable routed target identifies the provider/model whose capacity is being measured.
  - The provider/adapter can resolve capacity and a default output cap.
  - The policy function can accept the effective reservation as an explicit input.
- **exclusions:**
  - Using a global model catalog as a substitute for the durable route's effective metadata.
  - Treating auxiliary compaction-summary `maxTokens` as the routed request reservation.
  - A workflow that has no request envelope and no provider default to bind.
- **non_goals:**
  - Defining the residual-budget arithmetic itself.
  - Rewriting provider serialization precedence.
  - Falling back to agent options when a durable route is intentionally required.

### Problem mechanism and semantic roles

- **problem_mechanism:** The reservation exists at the request boundary but is omitted from the capacity-policy boundary. A correct residual calculation cannot be performed if the call site passes only `contextWindow`.
- **semantic_roles:**
  - `durable_route`: provider/model used for the latest request.
  - `effective_envelope_cap`: request-specific output cap.
  - `adapter_default_cap`: provider/model default when the envelope omits a cap.
  - `effective_reservation`: the value passed to the policy resolver.
  - `capacity_metadata`: current route's context capacity and default cap.

### Contract

- **required_inputs:** durable request header, route-specific model metadata, provider serializer precedence.
- **produced_outputs:** one effective reservation value and one route-specific capacity binding passed explicitly to the policy seam.
- **parameter_slots:** `route_selector`, `envelope_cap_field`, `adapter_default_field`, `missing_cap_value`, `capacity_lookup`.
- **variation_points:** whether the fallback is zero or a provider-defined default; whether route changes are represented as a new durable header; whether metadata is synchronous or asynchronous.

### Solution principle

At the pressure call point, resolve the current durable route and current model metadata, then apply the same precedence that the request path uses:

1. `effective_reservation = durable_header.maxTokens` when present.
2. Otherwise use `modelInfo.defaultMaxTokens`.
3. Otherwise use the repository-defined no-reservation value (`0` in this realization).
4. Pass the value explicitly to residual-budget resolution.
5. Re-resolve for every current route; do not cache by model id alone.

If no durable routed target exists, follow the host contract for “no pressure target” rather than inventing a different route from agent options.

### Invariants

- The reservation used by pressure matches the cap that the provider will use for that routed request.
- Explicit envelope cap wins over adapter default.
- Adapter default wins over missing-cap zero fallback.
- Provider/model identity and capacity are resolved together.
- A provider switch with the same model id cannot reuse stale capacity/reservation facts.
- The auxiliary summary cap remains a distinct semantic field.

### Validation oracle

- Explicit-header test: a history below the nominal `W*r` threshold compacts after a durable header with a smaller `maxTokens` lowers the threshold.
- Adapter-default test: omit the header cap and return a lower `defaultMaxTokens`; compaction still triggers.
- Provider-switch test: same model id on large then small provider re-resolves capacity.
- Serialization cross-check: model metadata and wire serializer show the same output-cap precedence family.
- Evidence: `EU-RESERVATION-BINDING`, `EU-UNIT-ORACLE`, `EU-INTEGRATION-ORACLE`, realized by `CA2`.

### Failure modes

- Passing `contextWindow` alone to the resolver.
- Using `ResolvedTargetPolicy.maxTokens` as the routed request reservation; in this case it is the summarization cap.
- Reading a model-discovery catalog instead of the durable routed request metadata.
- Using a previous provider's capacity when provider changes but model id stays the same.
- Giving agent options precedence over the durable request header when the host contract requires the durable route.
- Treating “missing cap” as an unbounded reservation instead of the provider's defined fallback.

### Realization mapping

- **Case:** `deepseek-compaction-reservation`.
- **Case action:** `CA2`.
- **Code:** `/home/chenyujia/tritonToLlvm/deepseek-harness/packages/compaction/compaction-basic/src/index.ts:48-68, 289-319`.
- **Provider facts:** `/home/chenyujia/tritonToLlvm/deepseek-harness/packages/llm/llm-deepseek/src/model-info.ts:61-78` and `packages/llm/llm-deepseek/src/serialize.ts:140-143`.
- **Supporting commits:** `0fadb08fbdd3316c4605fc4e6be96cb9990b56c6`, `9b016b642503ff798faec65c860e948cc14f99cc`.

### Abstraction assessment and delivery

- **abstraction_assessment:** The precedence-and-route-binding mechanism is independently reusable, but the missing-cap fallback value is provider/host-specific and must remain a parameter slot.
- **counterexamples to hold out:** no durable request route; a provider that does not charge output to the same capacity; a system where a central allocator already emits residual capacity.
- **routing_view:** trigger on missing output-cap propagation, stale capacity after route switching, or a pressure resolver that accepts only `contextWindow`.
- **execution_view:** trace the wire cap precedence, bind durable route plus metadata, pass explicit reservation, and validate explicit/default/switch partitions.
- **reference_files:** `evidence.md`, `case.json`; no script proposed from this single case.

---

## AC-default-summary-cap-to-headroom

### Identity

- **id:** `AC-default-summary-cap-to-headroom`
- **name:** `default-summary-cap-to-headroom`
- **version:** `0.1.0`
- **title:** Default auxiliary summary output to the configured pressure headroom
- **confidence:** provisional / medium-low; one case contains direct config tests and deterministic replay evidence

### Discovery

- **description:** Aligns an auxiliary compaction-summary generation cap with an explicit pressure-headroom budget when no summary cap is configured, while preserving explicit global and target-specific caps. Use when adding residual pressure headroom would otherwise leave summary generation on an unrelated legacy default.
- **problem_signature:** pressure headroom is configurable or newly introduced, but auxiliary summary output still uses an independent fixed default.
- **observable_cues:**
  - A policy has `headroomTokens` and a separate summarization `maxTokens`.
  - The old summary default is unrelated to the new headroom.
  - Provider reasoning/output tokens can consume the summary cap.
  - Replay metadata records the actual summary `maxTokens`.

### Boundary

- **preconditions:**
  - The compaction policy distinguishes pressure headroom from auxiliary summary output cap.
  - Headroom is a validated non-negative integer.
  - Explicit global and exact-target summary caps have defined precedence.
- **exclusions:**
  - Using headroom as the routed request reservation; those are different semantic roles.
  - Overriding an explicit summary cap merely because it differs from headroom.
  - Treating zero headroom as a valid positive summary cap without an explicit override.
- **non_goals:**
  - Choosing the pressure threshold formula.
  - Proving provider-specific context accounting.
  - Making every output cap in the system equal to headroom.

### Problem mechanism and semantic roles

- **problem_mechanism:** A new safety budget is introduced for pressure, but a separate auxiliary LLM call retains an unrelated output cap. This can make the supposedly protected budget meaningless or cause summary generation to exceed the intended bounded allowance.
- **semantic_roles:**
  - `headroomTokens`: pressure safety budget `B`.
  - `summary_maxTokens`: cap for the auxiliary compaction summary call.
  - `explicit_override`: user-selected summary cap that must win.
  - `request_reservation`: separate routed request cap `O`, never inferred from this candidate.

### Contract

- **required_inputs:** validated headroom, optional global summary cap, optional exact-target summary cap, explicit-cap precedence rules.
- **produced_outputs:** resolved positive summary output cap and an error if the inherited default would be zero or otherwise invalid.
- **parameter_slots:** `headroom_default`, `summary_cap_field`, `global_override`, `target_override`, `zero-headroom_policy`.
- **variation_points:** whether the default is equality to headroom or another bounded function; whether target overrides inherit global or policy-local headroom.

### Solution principle

Use the resolved headroom as the summary output cap only when no explicit summary cap exists. Preserve explicit global and exact-target caps. Validate the resulting cap as positive; if headroom is zero, require an explicit positive summary cap rather than silently creating a zero-cap request.

This candidate deliberately does **not** say that summary cap equals routed request reservation. The latter remains the input to residual-capacity pressure calculation.

### Invariants

- An explicit exact-target summary cap overrides an inherited global cap.
- An explicit global summary cap overrides the default derived from headroom.
- An omitted summary cap resolves to the applicable headroom in this realization.
- The final summary cap is positive.
- `summary_maxTokens` is not reused as `request_reservation` unless a separate provider contract explicitly proves that equivalence.

### Validation oracle

- Default-resolution unit: `resolveConfig({headroomTokens: 16_384}).maxTokens` is `16_384`.
- Explicit-precedence unit: explicit global/per-target summary caps remain unchanged even when headroom differs.
- Degenerate unit: `headroomTokens: 0` without a positive explicit summary cap fails.
- Loader oracle: global headroom and target-level `headroomTokens: 0, maxTokens: 32` survive real loader normalization.
- Replay oracle: `compaction-summary-headroom/session.v3.jsonl` records summary `maxTokens: 1,800` when the composition omits an explicit summary cap; `compaction-output-reserve/session.v3.jsonl` records explicit summary `maxTokens: 32`.
- Evidence: `EU-HEADROOM-CONFIG`, `EU-INTEGRATION-ORACLE`, `EU-REPLAY-SUMMARY-HEADROOM`, realized by `CA4` and `CA6`.

### Failure modes

- Keeping the legacy fixed default while claiming headroom is the safety budget.
- Using `headroomTokens: 0` as a zero-cap auxiliary request.
- Letting a global cap override a more specific target cap.
- Conflating `summary_maxTokens` with the routed request reservation used for pressure.
- Applying headroom to overflow recovery or other output paths without a separate contract.

### Realization mapping

- **Case:** `deepseek-compaction-reservation`.
- **Case actions:** `CA4` and `CA6`.
- **Code:** `/home/chenyujia/tritonToLlvm/deepseek-harness/packages/compaction/compaction-basic/src/config.ts:75-109, 118-138`; `/home/chenyujia/tritonToLlvm/deepseek-harness/packages/compaction/compaction-basic/src/types.ts:8-28`.
- **Tests and fixtures:** `/home/chenyujia/tritonToLlvm/deepseek-harness/packages/compaction/compaction-basic/tests/compaction-basic.spec.ts:325-350`; `loader-composition.spec.ts:70-95`; `snapshots/session/compaction-summary-headroom`.
- **Supporting commits:** `555b664b08db05e1cf8eeebb7eb00960ddf785b7`, `ec7030afd3643773a96198f9d1c8e9c7fc5e3da1`.

### Abstraction assessment and delivery

- **abstraction_assessment:** This is a narrower Atomic than the residual-budget candidate. It is reusable only where the same policy owns both pressure headroom and auxiliary summary output defaults; explicit override precedence and zero-headroom behavior are part of the contract.
- **counterexamples to hold out:** systems where summary output is charged to a separate pool; policies where headroom is not intended to bound summary generation; explicit provider-level summary caps that must always win.
- **routing_view:** trigger on “headroom added but summary cap still uses legacy default,” “summary generation can consume the reserved safety budget,” or zero-headroom configuration failures.
- **execution_view:** resolve defaults and target overrides, validate positive cap, then replay/inspect actual summary event metadata.
- **reference_files:** `evidence.md`, `case.json`; no script proposed from this single case.

## Promotion decision

- **Candidate Atomic status:** all three remain `provisional`.
- **Why not Workflow/Pattern:** the case has a semantic DAG realization, but there is only one Case Workflow and no cross-case or held-out evidence. Per the design document, that is insufficient to promote a Workflow or Pattern.
- **Why not reviewed Atomic:** each candidate has one realization. The direct unit/replay oracles establish correctness for this case, but not independent transfer.
- **Recommended next evidence:** one independent repository or held-out synthetic case with the same shared-capacity mechanism, plus a negative case with isolated pools to test routing exclusions.
