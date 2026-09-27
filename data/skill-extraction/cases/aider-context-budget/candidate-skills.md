# Candidate Atomics: Aider context budget

## D1 — derive-history-budget-from-model-input-capability

Derive an explicit history budget from the summarizer/main model input limit and a safety margin. Validate that the budget is non-negative and make the source visible to downstream selection.

**Oracle:** changing `max_input_tokens` changes the selected history budget; invalid limits fail safely.

## D2 — select-history-prefix-by-available-summarizer-budget

Select as many older messages as fit into the summarizer budget while preserving the recent tail required for continuity.

**Oracle:** selected messages fit the budget, preserve required recent context, and vary monotonically with the available budget.

## D3 — preserve-original-context-on-summary-failure

If summary generation fails, retain the original context and issue a visible warning rather than losing information or crashing the session.

**Oracle:** injected summarizer failure returns original messages and an observable warning.

## Alignment boundary

These candidates address summarizer input fitting and failure recovery. They are adjacent to, but not part of, the residual-output-reservation Pattern.
