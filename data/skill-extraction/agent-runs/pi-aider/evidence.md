# Evidence: Pi/Aider bounded-context pressure and recovery

## Scope and method

This run compares the local checkouts `/home/chenyujia/tritonToLlvm/pi-agent` and `/home/chenyujia/tritonToLlvm/aider-agent`. It treats commit subjects and issue numbers as provenance pointers only; the semantic claims below come from reading the implementation, its callers, and test oracles. The output deliberately distinguishes **Case Action** (a repository-specific change instance) from an **Atomic candidate** (a reusable mechanism).

No token counts, model identity, LLM output, or runtime benchmark result is inferred unless a checked-in test explicitly asserts it. Aider’s local commit metadata does not carry issue/PR numbers for the four commits below; no issue/PR number is invented.

## Provenance and inspected code

| family | real provenance | implementation and call points | test oracle |
|---|---|---|---|
| Pi policy | `46bde88a1cd752966aa2a357d292e83aff98b132`, `feat(coding-agent): support per-model compaction token budgets`, closes Pi issue `#8133` | `packages/coding-agent/src/core/settings-manager.ts`: `SettingsManager.getCompactionTokenSetting`, `getCompactionSettings`; callers in `packages/coding-agent/src/core/agent-session.ts`: `_compactBeforeNextAssistantResponse`, `compact`, `_checkCompaction`, `_runAutoCompaction` | `packages/coding-agent/test/settings-manager-compaction.test.ts`; `packages/coding-agent/test/suite/agent-session-compaction-model-overrides.test.ts` assert exact override/fallback/validation and use of the active model across manual, threshold, overflow, and post-run paths |
| Pi request boundary | `56700d42ed65a94a80af7376adb19a9298065164`, `fix(coding-agent): compact before post-tool model requests (#8782)`, closes `#6879` | `packages/agent/src/agent-loop.ts`: `runLoop` invokes `prepareNextTurn` only after a completed turn when the loop will continue; `packages/coding-agent/src/core/agent-session.ts` supplies compaction preparation | `packages/coding-agent/test/suite/agent-session-compaction.test.ts`: the “does not compact after a terminating tool result” case requires no compaction entry/event, while continuation cases require `compaction` before `provider` |
| Pi oversized-tail boundary | `8bdcd4498a925301bcd8b9053386797727eae3b0`, `fix(coding-agent): compact oversized trailing tool results`, closes `#9740` | `packages/coding-agent/src/core/compaction/compaction.ts`: `findCutPoint` chooses the first valid cut point at/after pressure, or the latest valid cut point when a trailing tool result is itself oversized; `prepareCompaction` consumes that boundary | `packages/coding-agent/test/compaction.test.ts` regression for `#9740` asserts `firstKeptEntryIndex`, `turnStartIndex`, `firstKeptEntryId`, summarized messages, and retained turn prefix |
| Pi complete accounting | `a6f720e6caf1cf429e382011156c015fa204c512`, `fix(coding-agent): count custom messages in compaction budget`, closes `#6326` | `packages/coding-agent/src/core/compaction/compaction.ts`: `findCutPoint` counts context-visible entries, including custom messages, before selecting a safe boundary | `packages/coding-agent/test/compaction.test.ts` “should budget context-visible custom message entries” checks that a custom entry changes the cut point and split-turn result |
| Aider fit selection | `e61857ef09db263ee8de89ac2cb16e1bb3ffa36e`, `summarize as many messages as will fit into the summarizer context`; local metadata contains no issue/PR marker | `aider/history.py`: `ChatSummary.summarize_real` tokenizes messages, reserves a safety buffer from `models[0].info["max_input_tokens"]`, builds a fitting `keep` prefix, summarizes it, and recursively rechecks summary+tail; `aider/coders/base_coder.py`: `Coder.summarize_start` starts the worker when `too_big` | `tests/basic/test_history.py`: `test_summarize` requires a smaller result; `test_too_big` checks the budget gate; `test_tokenize` checks the accounting input |
| Aider budget propagation | `64470955d4799b92a4b8174856e8699b5ba41568`, `pass max_chat_history_tokens into ChatSummary`; `ff41f9bd9a29585176c16445d2064f426864ec7c`, `refactor: adjust max_chat_history_tokens calculation based on max_input_tokens`; neither local commit has an issue/PR marker | `aider/coders/base_coder.py`: `Coder.create` passes explicit `max_chat_history_tokens` or `main_model.max_chat_history_tokens` to `ChatSummary`; `aider/models.py`: `Model.__init__` derives `max_chat_history_tokens` from `max_input_tokens`, clamped to 1/16th with 1k/8k bounds | `tests/basic/test_history.py` constructs `ChatSummary` with an explicit limit; checked-in fixture/search-replace tests exercise coder construction and the resolved field. The code establishes propagation; it does not establish a shared provider output reservation |
| Aider failure recovery | `5c866c67b507c6508012e7d7fbdec0e358556a4e`, `fix: Handle summarizer failure gracefully with fallback and warning`; local metadata contains no issue/PR marker | `aider/coders/base_coder.py`: `Coder.create` catches `ValueError` from `from_coder.summarizer.summarize_all`, keeps `done_messages`, and calls `io.tool_warning`; `summarize_worker` also catches `ValueError` and warns | `tests/basic/test_history.py`: `test_fallback_to_second_model` verifies a later summarizer model can recover. The fallback-on-coder-switch path is directly visible in implementation; no checked-in test was found that injects that exact `ValueError` and asserts the warning |

## Causal reading

### Pi direct family

The three Pi changes form a semantic chain rather than a commit timeline:

1. `46bde88` makes the active provider/model part of compaction-policy resolution and routes the resolved settings through every compaction entry point.
2. `56700d42` moves preparation to the boundary where a real next assistant/provider request is about to happen, and suppresses it when a tool terminates the turn.
3. `8bdcd449` repairs the boundary selector for the case where a trailing tool result alone exceeds the retained budget, preserving the latest safe assistant/tool-call boundary.

`a6f720e` is a supporting accounting action: it prevents visible custom entries from being omitted before the boundary is selected. These actions have a real causal dependency: an active-model policy is only useful if evaluated at the actual next-request boundary, and that boundary is only usable if the cut-point algorithm can return a safe result for oversized tails.

### Aider related family

The Aider sequence is also semantically coherent, but at a different seam:

1. `ff41f9bd` derives a bounded history budget from model input capacity.
2. `64470955` passes an explicit caller budget into `ChatSummary` instead of silently re-deriving it from the weak model.
3. `e61857ef` uses that budget to select a maximal fitting older prefix while retaining a recent tail.
4. `5c866c67` preserves the original history and warns when a cross-coder summarization call fails.

This is genuine budget propagation plus non-destructive recovery. It is **adjacent**, not proof of Pi’s request-boundary mechanism: Aider’s code manages a summarizer/history input budget, and the reviewed changes do not demonstrate a provider request boundary with an output reservation charged against the same capacity.

## Explicit non-claims

- The Aider formula `max_input_tokens / 16`, the `512` safety subtraction, and the 1k/8k clamps are implementation facts, not a generalized residual-capacity law.
- Pi `reserveTokens` and `keepRecentTokens` are compaction settings; the reviewed evidence does not prove that they equal a provider-enforced output reservation formula.
- A commit with `Closes #...` is issue provenance, not evidence that the issue text was read. The semantic evidence here is the diff, call path, and test oracle.
- No cross-repository equivalence is claimed merely because both families use words such as “context”, “budget”, “summary”, or “overflow”.
