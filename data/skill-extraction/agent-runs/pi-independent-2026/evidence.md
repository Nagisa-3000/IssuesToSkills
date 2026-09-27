# Independent evidence: Pi compaction/context-pressure analysis

## Scope and independence

- Repository inspected: `/home/chenyujia/tritonToLlvm/pi-agent`
- Git remote observed locally: `https://github.com/earendil-works/pi.git`
- Repository revision at inspection: `d5629e20`
- Extraction date: `2026-09-26`
- This run used the Pi working tree, its local Git history, before/after diffs, call sites, and tests only. No other agent output was used as semantic evidence.
- Commit titles and keyword hits were used only to discover candidates. Acceptance/rejection below is based on implementation data flow and behavioral tests.

## Family test used for comparison

The comparison target is the Hermes/DeepSeek residual-budget/shared-capacity family: a pressure policy should make the capacity actually available to the next operation explicit, reserve downstream/output headroom, apply the same policy at the request seam, and preserve the invariant across reconfiguration/retry. This definition is the comparison criterion, not evidence that Pi implements it.

## Evidence ledger

### EU-PI-THRESHOLD — explicit compaction threshold

**Observed evidence:** `packages/coding-agent/src/core/compaction/compaction.ts:289-292` implements `shouldCompact(contextTokens, contextWindow, settings)` as `contextTokens > contextWindow - settings.reserveTokens` when enabled. `packages/coding-agent/src/core/compaction/compaction.ts:919-920` uses the projected context estimate and `keepRecentTokens` during preparation.

**Commit evidence:** `46bde88a` introduced model-aware settings resolution; its before/after diff changes the call from `getCompactionSettings()` to `getCompactionSettings(model)` in `AgentSession` and adds exact provider/model overrides.

**What this proves:** Pi has a residual-threshold-shaped compaction rule and a configurable reserve.

**What it does not prove:** the reserve is the same semantic downstream/output reservation used by a provider request-capacity calculation. No shared formula or direct data dependency from `shouldCompact` to provider `maxTokens` was found.

### EU-PI-POLICY — model-specific policy resolution and validation

**Observed evidence:** `packages/coding-agent/src/core/settings-manager.ts:13-28,859-905` defines `CompactionModelOverride`, exact `provider/modelId` lookup, precedence `model override -> ordinary setting -> built-in default`, and non-negative safe-integer validation. Invalid base settings are rejected even when an override is valid.

**Commit/diff:** `46bde88a1cd752966aa2a357d292e83aff98b132` (`feat(coding-agent): support per-model compaction token budgets`, closes #8133) changed the API to accept a model and added validation and model-override tests.

**Test evidence:** `packages/coding-agent/test/settings-manager-compaction.test.ts:115-190` covers invalid override/base values, malformed entries, zero values, and fallback; `packages/coding-agent/test/suite/agent-session-compaction-model-overrides.test.ts:36-103` covers manual, pre-prompt, post-run, and overflow paths.

### EU-PI-REPLAY — the resolved policy is replayed through runtime paths

**Observed evidence:** current call sites in `packages/coding-agent/src/core/agent-session.ts:587-605,2413-2429,2599-2605,2747-2750` resolve settings with the active model for pre-request threshold checks, manual compaction, `_checkCompaction`, and automatic compaction. `packages/coding-agent/src/core/agent-session.ts:608-633` rebuilds provider-visible context from the canonical session projection before the request.

**Test evidence:** the model-override suite asserts the same resolved `reserveTokens`/`keepRecentTokens` in manual, threshold, post-run, and overflow compaction and checks the extension preparation settings.

**What this proves:** Pi propagates model-scoped compaction policy across several entry points rather than reading one global snapshot.

**Inference:** this is a reusable policy-replay mechanism and is the closest Pi analogue to the family’s reconfiguration invariant. It remains an inference about reuse; the tests do not establish Hermes/DeepSeek’s shared-capacity arithmetic.

### EU-PI-BOUNDARY — pressure check before the next real request

**Commit/diff:** `56700d42ed65a94a80af7376adb19a9298065164` (`fix(coding-agent): compact before post-tool model requests (#8782)`) changes `packages/agent/src/agent-loop.ts` so `prepareNextTurn` is deferred until a next turn is actually needed. `AgentSession._compactBeforeNextAssistantResponse()` invokes threshold compaction before the next assistant response.

**Current call sites:** `packages/agent/src/agent-loop.ts:182-241` prepares the next turn and request immediately before streaming the next assistant response; `packages/coding-agent/src/core/agent-session.ts:587-605` evaluates the projected context and compacts before that request.

**Test evidence:** `packages/coding-agent/test/suite/agent-session-compaction.test.ts` covers post-tool compaction, queued steering during compaction, and no compaction after a terminating tool result. The commit also changed the agent-loop test to assert the new ordering.

**What this proves:** Pi fixed a request-boundary timing bug and prevents unnecessary compaction after a terminal tool result.

**Why it is not the target family by itself:** this is scheduling/control-flow placement, not derivation of a shared input/output capacity budget.

### EU-PI-CONTEXT — canonical context accounting and safe retention

**Commit/diff:** `a6f720e6caf1cf429e382011156c015fa204c512` (`fix(coding-agent): count custom messages in compaction budget`, closes #6326) replaced ad-hoc entry conversion with `sessionEntryToContextMessages` and made context-visible custom entries participate in token/cut-point accounting. Its test adds `packages/coding-agent/test/compaction.test.ts:358-375` for a custom message changing the cut point.

**Commit/diff:** `8bdcd4498a925301bcd8b9053386797727eae3b0` (`fix(coding-agent): compact oversized trailing tool results`, closes #9740) changes `findCutPoint` to prefer the latest safe cut point when trailing tool results alone exceed `keepRecentTokens`; its regression test uses an 8000-character tool result and asserts compaction before the resumed provider request while retaining the tool result.

**Current implementation:** `packages/coding-agent/src/core/compaction/compaction.ts:218-283,919-935` estimates from the latest valid usage plus trailing message estimates, invalidates stale usage after context edits/compaction, and uses the projection for `tokensBefore` and cut points.

**What this proves:** budget measurement is increasingly based on the canonical provider-visible projection, including custom and trailing artifacts, and compaction preserves a safe conversational boundary.

**Why it is adjacent:** complete-context accounting protects the pressure invariant but does not make the pressure budget a shared provider input/output-capacity calculation.

### EU-PI-NO-USAGE — missing/zero provider usage recovery (reviewed but not promoted as a case action)

**Commit/diff:** `4495469a5e8466eb67e3f26969922d3e7b208de2` (`fix(coding-agent): compact without provider usage`, closes #8328) changes `_checkCompaction` to use message-size estimation when usage is absent or all-zero. `packages/coding-agent/test/suite/regressions/8328-zero-usage-auto-compaction.test.ts:39-80` checks both trigger and non-trigger cases.

**Classification:** useful adjacent robustness evidence for context accounting; not a distinct Case Action in this extraction because it is a fallback data-source repair, not the family’s shared-capacity mechanism.

## False-positive candidates explicitly rejected

- `6d474f8c` (`fix(ai): cap context-sized default output budgets`) caps a provider default `maxTokens` at 32000 when the model advertises a context-sized output limit. It has no compaction call-site or shared residual budget with the input context; reject as same-mechanism evidence.
- `22a9c484` (`fix(ai): respect model output token limits`) is provider option plumbing; reject as same-mechanism evidence.
- `e98f287e` (`fix(ai): retry Azure peak-load capacity errors`) is retry classification for a provider overload/capacity error, not context pressure; reject.
- `97fa14e3` (`fix(coding-agent): reject truncated compaction summaries`) validates summary completeness; reject as a capacity-policy realization.

## Bottom line

Pi contains real compaction/context-pressure mechanisms, including a `contextWindow - reserveTokens` threshold and model-scoped policy propagation, but the reviewed code does not establish the Hermes/DeepSeek shared-capacity invariant at the same semantic seam. The defensible result is **partial alignment**: policy resolution/replay overlaps; request-boundary timing and complete-context accounting are adjacent mechanisms. The cross-repository Pattern remains **provisional** and Pi must not be promoted as a direct realization from this evidence.

## Verification note

The tests were read as repository evidence. They were not executed in this workspace because the Pi checkout has no `node_modules` directory; no runtime result is claimed here.
