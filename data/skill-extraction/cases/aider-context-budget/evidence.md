# Evidence: Aider budget-aware summarization and fallback

## Scope and provenance

Repository: `/home/chenyujia/tritonToLlvm/aider-agent`.

Verified commits:

- `e61857ef09db263ee8de89ac2cb16e1bb3ffa36e` — summarize as many messages as fit into summarizer context
- `64470955d4799b92a4b8174856e8699b5ba41568` — pass `max_chat_history_tokens` into `ChatSummary`
- `ff41f9bd9a29585176c16445d2064f426864ec7c` — adjust history budget from `max_input_tokens`
- `5c866c67b507c6508012e7d7fbdec0e358556a4e` — graceful fallback on summarizer failure

## Observed mechanisms

Aider derives a summarizer/history budget from the summarizer or main model input capability, selects as many older messages as fit while retaining recent messages, and passes the resolved history budget into the summary component. If summarization fails, it preserves the original messages and emits a warning instead of silently dropping context or crashing.

## Alignment decision

Aider is a neighboring family: budget-aware context summarization. It is not direct evidence for downstream output reservation because the reviewed changes concern summarizer input capacity and graceful fallback, not a provider-enforced output reservation charged against the same window.

## Case Actions

- `CA1`: derive history budget from model input capability and safety margin.
- `CA2`: select a maximal fitting history prefix while preserving the recent tail.
- `CA3`: propagate resolved history budget into the summary component.
- `CA4`: preserve original context and warn when summarization fails.

## Reusable candidate boundaries

The likely Atomics are `select-history-prefix-by-available-summarizer-budget`, `derive-history-budget-from-model-input-capability`, and `preserve-original-context-on-summary-failure`. They should not be merged into residual-output reservation without a shared-capacity/output-cap oracle.
