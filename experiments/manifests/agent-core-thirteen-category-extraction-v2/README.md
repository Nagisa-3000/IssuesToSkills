# Agent-core thirteen-category extraction v2

This extraction-only set extends the first seven classes to twenty common agent-harness problem classes.

- Training cases: 52 (13 categories × 4 repositories).
- Untouched holdouts: 13 (one different repository per category).
- Training cases with a changed test/spec file: 35.
- Every training artifact resolves to a pinned local implementation commit.
- `selection-audit.json` is provenance only and must never be passed to an extraction or holdout agent.
- `excluded-candidates.json` records keyword-near candidates rejected after implementation review.
- `holdouts.json` must not enter Episode, Atomic, Workflow, Pattern, graph, or retrieval construction.

## Categories

- `model-catalog-and-capability-metadata` — model catalog freshness and capability metadata
- `provider-error-payload-normalization` — preserve and normalize provider error payloads
- `subprocess-and-pty-lifecycle` — subprocess and pseudo-terminal lifecycle finalization
- `permission-policy-enforcement` — permission policy consistency and bypass prevention
- `path-root-and-worktree-resolution` — canonical path resolution against the intended repository or worktree root
- `diff-rendering-and-review-navigation` — bounded diff presentation and review navigation
- `key-event-normalization-and-shortcuts` — portable key-event normalization and conflict-free shortcuts
- `unicode-width-and-terminal-rendering` — Unicode-safe width calculation, wrapping, and terminal rendering
- `extension-lifecycle-and-reload` — extension loading, identity, uninstall, and reload lifecycle
- `link-integrity-and-browser-handoff` — preserve link targets and route browser handoff through the correct host
- `cross-platform-release-packaging` — cross-platform release asset completeness and packaging
- `sensitive-data-redaction-in-diagnostics` — redact secrets and sensitive payloads at logging and diagnostics boundaries
- `persistent-state-and-schema-consistency` — persistent cache and state schema consistency

## Scope boundary

The current phase ends at schema-validated Issue/PR → ChangeEpisode → candidate Atomic → actionable Workflow extraction. Pattern construction, graph storage, retrieval, graph expansion, LLM use, feedback, lifecycle updates, and holdout agent evaluation remain deferred.

All runs use the v2 contract with plain-language titles, `when_to_use`, `anti_goals`, `not_applicable_when`, runtime inputs, Atomic-linked steps, dependencies, conditions, validation oracles, validation ladders, and stop conditions.
