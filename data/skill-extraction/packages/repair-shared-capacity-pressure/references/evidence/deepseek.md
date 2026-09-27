# Evidence: DeepSeek Harness compaction pressure / output reservation

## Scope and evidence boundary

- **Repository:** `/home/chenyujia/tritonToLlvm/deepseek-harness`
- **Case family:** compaction pressure / output reservation with a shared finite context capacity and residual budget.
- **Extraction boundary:** this is a single DeepSeek Harness case. No Hermes result was read, imported, compared, or used. No cross-repository Workflow or Pattern claim is made here.
- **Design source read first:** `/home/chenyujia/tritonToLlvm/arex-skill-graph/design/agent-skill-aligned-hierarchy-v2.md` (v2.1.0, 2026-09-26). The artifacts below keep provenance in the Case layer and keep candidate Atomic skills implementation-independent.

## Git provenance: PR #4530 was verified from local objects

The local repository contains the merge commit and both parents as real commit objects. `git cat-file -p` and ancestry checks establish:

- **Merge commit:** `bc45bd821a63619c39a4cf0686d94743093cd990`
- **First parent (pre-PR master):** `0fa88d48756a0a05ab6ffc55de0e18faa8a3144f`
- **Second parent (tip of PR branch):** `ec7030afd3643773a96198f9d1c8e9c7fc5e3da1`
- **Merge title:** `Merge pull request #4530 from deepseek-harness/fix/compaction-threshold-reserves-completion`
- `0fa88d...` is an ancestor of the merge and `ec7030...` is also an ancestor of the merge.
- The second-parent chain was independently enumerated with `git rev-list --reverse --ancestry-path 0fa88...` and contains exactly the six commits below; the supplied abbreviated hashes were verified rather than assumed.

| order on PR branch | full commit | parent | commit date (+08:00) | observed semantic contribution |
|---:|---|---|---|---|
| 1 | `0fadb08fbdd3316c4605fc4e6be96cb9990b56c6` | `0fa88d48756a0a05ab6ffc55de0e18faa8a3144f` | 2026-09-18 14:59:36 | Change proactive pressure from nominal window to the message budget after routed output reservation; add unit coverage and make the headless harness expose a coherent capacity/cap pair. |
| 2 | `a1cebebd4086836fe487006dca87ea18afbe57f4` | `0fadb08fbdd3316c4605fc4e6be96cb9990b56c6` | 2026-09-18 15:28:46 | Remove an unused `reservedCompletionTokens` field from the resolved output shape while retaining the reservation as an input to budget derivation; explicitly distinguish routed request cap from summarization `maxTokens`. |
| 3 | `b02b20d7135ebd0f3d1848ef3af5b25aef852e27` | `a1cebebd4086836fe487006dca87ea18afbe57f4` | 2026-09-18 16:04:41 | Add explicit pressure headroom, preserve actionable degenerate-cap errors, pin real-model caps, and add the deterministic `compaction-output-reserve` replay fixture. |
| 4 | `555b664b08db05e1cf8eeebb7eb00960ddf785b7` | `b02b20d7135ebd0f3d1848ef3af5b25aef852e27` | 2026-09-18 17:38:59 | Make `headroomTokens` configurable and target-overridable; cap pressure by residual capacity after output reservation plus headroom; use the setting as the default summary cap; update unit, loader, loop-regression, and e2e fixtures. |
| 5 | `9b016b642503ff798faec65c860e948cc14f99cc` | `555b664b08db05e1cf8eeebb7eb00960ddf785b7` | 2026-09-18 17:45:37 | Make the output reservation argument explicit at the budget-resolution seam and remove the old no-reservation unit expectation. |
| 6 | `ec7030afd3643773a96198f9d1c8e9c7fc5e3da1` | `9b016b642503ff798faec65c860e948cc14f99cc` | 2026-09-19 12:18:15 | Default summarization output cap to resolved headroom, preserve explicit caps, reject zero-cap inheritance, and add deterministic `compaction-summary-headroom` replay evidence. |

The PR is therefore treated as one Case realization, not as six independent skills and not as a chronological Workflow.

## Parent-before state and failure mechanism

At first parent `0fa88d48756a0a05ab6ffc55de0e18faa8a3144f`:

1. `packages/compaction/compaction-basic/src/config.ts` exposed `resolveCompactSpec(policy, contextWindow)`.
2. It calculated `thresholdTokens = floor(contextWindow * thresholdRatio)` and, for ratio retention, `retainTokens = floor(contextWindow * retainRatio)`.
3. `packages/compaction/compaction-basic/src/index.ts` called `resolveModelInfo(...).context`, then passed only `context.contextWindow` into the resolver. The pressure path had no request-output reservation at the policy seam.
4. The routed provider's request output cap is charged against the same model context window. The PR's first commit records the observed failure: with `W = 1,048,576` and `O = 256,000`, the message budget is `792,576`, but the old 0.8 gate is `838,860`; observed requests around `792,850`, `797,639`, and `793,352` were rejected before proactive pressure compaction could run. This is the motivating oracle recorded in commit `0fadb08...`, not an inference from the commit title.
5. The old configuration also gave summarization `maxTokens` a fixed default of `8192`, independent of the newly introduced pressure headroom.

The failure mechanism is a shared-capacity accounting mismatch: a policy threshold consumes nominal capacity while a later mandatory output reservation consumes the same capacity at request time. The threshold can therefore sit above the provider's admissible prompt region.

## After state: implementation facts and call points

### Effective reservation is bound at the pressure call site

- `/home/chenyujia/tritonToLlvm/deepseek-harness/packages/compaction/compaction-basic/src/index.ts:48-68` reads the latest durable `request/header`. `reservedCompletionTokens(agent, defaultMaxTokens)` chooses `header.config.maxTokens`, otherwise the adapter's `defaultMaxTokens`, otherwise `0`.
- `/home/chenyujia/tritonToLlvm/deepseek-harness/packages/compaction/compaction-basic/src/index.ts:289-319` keeps overflow recovery separate, resolves model metadata for pressure, and calls `resolveCompactSpec(policy, info.context.contextWindow, reservedCompletionTokens(...))`.
- A missing durable routed provider/model returns `null` rather than using `AgentOptions` as a substitute for the pressure target. Pressure requires adapter context metadata; overflow is a distinct trigger and bypasses this normal pressure threshold path.
- `/home/chenyujia/tritonToLlvm/deepseek-harness/packages/llm/llm-deepseek/src/model-info.ts:61-78` provides `context.contextWindow` and `defaultMaxTokens = configured model maxTokens ?? connection maxTokens`.
- `/home/chenyujia/tritonToLlvm/deepseek-harness/packages/llm/llm-deepseek/src/serialize.ts:140-143` confirms the request wire cap is `options.maxTokens ?? model.maxTokens ?? connection.maxTokens`, which is the same fallback family that the pressure path models.

### Residual budget calculation

At `/home/chenyujia/tritonToLlvm/deepseek-harness/packages/compaction/compaction-basic/src/config.ts:141-216`:

- `W = contextWindow`.
- `O = reservedCompletionTokens` from the effective routed request envelope or adapter default.
- `M = W - O` is the message budget.
- `B = policy.headroomTokens` is additional pressure headroom.
- `P = M - B = W - O - B` is the residual pressure budget.
- `T = floor(min(W * thresholdRatio, P))` is the proactive pressure threshold.
- Ratio retention is `floor(M * retainRatio)`. Explicit `retainTokens` remains explicit and is checked against `T`; retention is not silently rewritten to use `P`.
- The resolver returns an immutable spec without storing a separate `reservedCompletionTokens` field. The reservation is consumed in the derived budgets, avoiding a second exported meaning that could be confused with the summarization `maxTokens` field.

### Configuration and propagation

- `headroomTokens` is accepted in the top-level policy and exact provider/model policies (`config.ts:25-50`), validated as a non-negative integer, and defaults to `65_536` (`config.ts:75-109`).
- The effective summary `maxTokens` defaults to resolved headroom, while an explicit global or exact-target cap wins. A zero headroom therefore requires an explicit positive summary cap (`config.ts:75-95`; tests at `compaction-basic.spec.ts:325-350`).
- `resolveTargetPolicy` carries `headroomTokens` through exact-target merging (`config.ts:118-138`). The per-model fallback preserves explicit per-model `maxTokens` over inherited values and uses a per-model headroom as its default only when the global cap is absent.
- This is an intentional distinction: `ResolvedTargetPolicy.maxTokens` is the auxiliary summarization output cap; the routed request output reservation is the separate `O` input derived from the durable request header / adapter metadata.

### Boundary guards

`resolveCompactSpec` rejects:

- non-positive or non-integer `W`;
- negative or non-integer `O`;
- `M <= 0` (the request reserve consumes the whole window);
- `P <= 0` (output reserve plus pressure headroom leave no pressure budget);
- resolved `retainTokens >= T`.

Errors are `TargetPressureConfigError` keyed by the exact `provider/model`, so the runtime can treat a route-specific configuration problem as a target-specific warning rather than silently disabling pressure globally.

## Validation oracles in the repository

The validation evidence is behavioral and spans unit, loader, regression, deterministic session, and live-provider smoke surfaces. No test was changed by this extraction task.

### Numeric and boundary unit oracle

`/home/chenyujia/tritonToLlvm/deepseek-harness/packages/compaction/compaction-basic/tests/compaction-basic.spec.ts:308-445` asserts:

- defaults resolve to `thresholdRatio: 0.8`, `headroomTokens: 65_536`, and summary `maxTokens: 65_536`;
- `headroomTokens` defaults the summary cap, while explicit global and per-model caps win;
- zero headroom without a positive explicit cap fails;
- with `W = 1_048_576`, `O = 256_000`, ratio `0.8`, and retain ratio `0.16`, the expected values are `T = 634_060` and `retainTokens = 126_812`;
- with `W = 1_000`, `O = 0`, the compatibility values are `T = 800` and `retainTokens = 160`;
- `O = W`, `O > W`, `O < 0`, and non-integer `O` produce target-specific errors;
- headroom exhaustion and retention-at-threshold are rejected.

### Dynamic pressure-gating oracle

`compaction-basic.spec.ts:620-680` proves the call-point binding, not only the arithmetic:

- a measured history below 80% of the whole `W = 1,000` remains un-compacted without a reserve;
- appending a durable `request/header` with a smaller effective `maxTokens` lowers the threshold and causes proactive compaction;
- when the durable header omits `maxTokens`, a mocked adapter `defaultMaxTokens` supplies the reserve and also causes compaction;
- the same-model-id provider switch is re-resolved so capacity is not cached across routes (`compaction-basic.spec.ts:627-649`).

### Integration and replay oracle

- `/home/chenyujia/tritonToLlvm/deepseek-harness/packages/compaction/compaction-basic/tests/loader-composition.spec.ts:60-95` verifies real loader normalization, global headroom, exact-target headroom override, explicit target summary cap, and plugin composition.
- `/home/chenyujia/tritonToLlvm/deepseek-harness/apps/cli/tests/profiles/headless/tests/compaction.e2e.ts:28-50` uses `modelContextWindow: 15_000`, `modelMaxTokens: 7_000`, and `headroomTokens: 4_000`; the intended message budget is 8,000 and the explicit summary cap is 1,024.
- `snapshots/session/compaction-output-reserve/cordis.yml` and its JSONL fixture pin `W = 10,300`, request `O = 1,000`, pressure `B = 1,800`, retained tokens `20`, and auxiliary summary `maxTokens = 32`. The replay includes `compaction/start`, `compaction/summary`, a replacement checkpoint, `compaction/end`, and a next-step request that continues with `PROACTIVE COMPACTION COMPLETE`.
- `snapshots/session/compaction-summary-headroom/cordis.yml` and its JSONL fixture use the same bounded capacity and request reserve but omit an explicit summary cap from the plugin config. The `compaction/summary` event records `maxTokens = 1,800`, proving that resolved headroom becomes the auxiliary generation cap.
- The authored snapshot metadata (`snapshot.yml`) pins both deterministic scenarios and keeps their input/session evidence separate from the live-provider smoke.

### Live-provider / harness oracle

`apps/cli/tests/profiles/headless/real-model.patch.yml` pins `maxTokens: 8192` for the real DeepSeek models. This prevents live-model output-cap drift from changing the message budget unexpectedly. The e2e test remains guarded by `DEEPSEEK_API_KEY`; the deterministic session fixtures do not require an external API key.

## Limits of this evidence

- This case supports provisional Atomic candidates only. It does not support a reviewed Atomic, a Workflow candidate across cases, or a Pattern candidate.
- The evidence demonstrates one implementation's distinction between routed request reservation and summarization output cap. It does not establish that all providers charge output against context capacity, nor that `B` must equal a summary cap when an explicit cap is supplied.
- The deterministic fixtures validate the session event oracle and configuration binding; they do not replace the live-provider smoke test.
