# Atomic candidates: bounded context pressure and recovery

These are **candidates**, not repository-specific Case Actions. A candidate is promoted only when its mechanism survives an independent realization and held-out validation. This run has no held-out transfer result.

## A1 — resolve policy for the active model

- **Mechanism:** model/provider selection can change the applicable compaction policy; stale settings make later compaction paths inconsistent.
- **Operator:** validate ordinary settings and exact provider/model overrides, resolve one policy object, and pass it through manual, automatic, overflow, and model-switch paths.
- **Pi realization:** `ca:pi:resolve-policy`, `ca:pi:propagate-policy`; `SettingsManager.getCompactionTokenSetting/getCompactionSettings`; model override and settings tests.
- **Boundary:** does not imply Aider’s history budget or a downstream output-reservation formula.
- **Oracle:** exact fallback/invalid-value checks plus cross-entry-point/model-switch equivalence.
- **Status:** direct Pi candidate; cross-repository alignment is partial.

## A2 — gate pressure at the real next request

- **Mechanism:** compaction after a terminating tool result is wasted, while late compaction lets the next provider request see over-budget context.
- **Operator:** evaluate pressure in the continuation path immediately before a real next assistant/provider request; skip terminal outcomes.
- **Pi realization:** `runLoop`/`prepareNextTurn`, `AgentSession._compactBeforeNextAssistantResponse`, and the `#8782/#6879` continuation and terminating-tool tests.
- **Boundary:** Aider’s `summarize_start` is not equivalent; it starts a background history summarization job and has no reviewed termination-aware provider boundary.
- **Oracle:** compaction precedes provider on continuation and no compaction event/entry exists after termination.
- **Status:** direct Pi candidate; no Aider realization.

## A3 — preserve the latest safe boundary for an oversized tail

- **Mechanism:** a trailing tool result can exceed `keepRecentTokens` by itself, so the ordinary forward search may fail to produce a usable boundary.
- **Operator:** choose the nearest valid cut point at/after pressure; if none exists, use the latest valid cut point before the oversized tail and retain the active turn prefix.
- **Pi realization:** `findCutPoint` and `prepareCompaction`; `#9740` regression oracle asserts exact indices, entry id, summarized history, and prefix.
- **Boundary:** not the same as generic “truncate the oldest messages”; preserving a valid tool-call/result boundary is essential.
- **Status:** direct Pi candidate.

## A4 — account for context-visible input

- **Mechanism:** omitted custom/session entries undercount pressure and change cut-point selection.
- **Operator:** use one context-visible projection for accounting and boundary selection.
- **Pi realization:** custom-entry budget test for `findCutPoint` under `#6326`.
- **Related Aider behavior:** `ChatSummary.tokenize` measures messages, but the reviewed Aider path does not expose Pi’s session-entry projection or tool-boundary semantics.
- **Status:** direct Pi candidate; Aider is only adjacent.

## A5 — derive and propagate a history budget

- **Mechanism:** a summarizer can use an implicit or wrong capacity, causing unstable prefix selection or over-aggressive history loss.
- **Operator:** derive a bounded history budget from input capacity, permit an explicit caller budget, and pass it into prefix selection.
- **Aider realization:** `Model.__init__` → `max_chat_history_tokens`; `Coder.create` → `ChatSummary`; `ChatSummary.summarize_real` → fitting `keep` prefix plus retained tail.
- **Oracle:** `test_too_big`, `test_tokenize`, `test_summarize`, and explicit `ChatSummary(max_tokens=...)` construction.
- **Boundary:** the 1/16, 1k/8k, and 512 values are Aider policy parameters, not reusable universal constants.
- **Status:** direct Aider candidate; partial alignment with A1.

## A6 — preserve context on summary failure

- **Mechanism:** replacing usable history with a failed/empty summary is destructive and hard to recover from.
- **Operator:** catch the handled summarizer failure, retain original messages, warn visibly, and try a configured fallback model when available.
- **Aider realization:** `Coder.create` and `Coder.summarize_worker`; `ChatSummary.summarize_all`; fallback-to-second-model test.
- **Boundary:** the exact coder-switch warning path is not covered by a dedicated checked-in test in the reviewed files; record it as implementation evidence, not a stronger oracle.
- **Status:** direct Aider candidate; partial alignment with Pi recovery, not the same request-boundary mechanism.

## Candidate boundary summary

The strongest shared abstraction is **bounded-context pressure handling with an explicit safety boundary and non-destructive recovery**. It remains a workflow-level candidate, not a single proven cross-repository Atomic, because Pi’s safety boundary is a session/provider request boundary and Aider’s is a summarizer history-prefix boundary.
