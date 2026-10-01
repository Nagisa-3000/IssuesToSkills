# Agent-core seven-category extraction v2

This manifest set is the extraction-only phase for seven common agent-harness
problem classes.

- train-all.json: 28 training cases (7 categories x 4 repositories).
- 01-*.json through 07-*.json: independent four-case category manifests,
  suitable for seven parallel runner processes.
- holdouts.json: seven untouched leave-one-repository-out cases. These must
  not enter ChangeEpisode, Atomic, Workflow, Pattern, or graph construction.
- excluded-seeds.json: the remaining exact table rows for which no verified
  implementation-bearing resolution was selected.

Every training case is explicitly classified as either exact_table_row or
verified_substitute. A substitute retains the original unresolved seed in
seed_issue, seed_issue_url, and provenance.seed; it is never reported as
completion of that exact table row.

The pinned commit, first parent, changed-file sample, Issue/PR URL, and
repository checkout are recorded for offline extraction. The intended model is
openai/gpt-5.6-sol through the RVNPU Responses endpoint. API credentials must
be supplied only as a process environment variable and must not be written into
this directory or extraction artifacts.

Current scope ends after schema-validated ChangeEpisode plus candidate Atomic
and Workflow extraction. Holdout agent evaluation, retrieval, graph expansion,
LLM judge/use, feedback, merge/retirement, and final evaluation are deferred.

The archived `codex-5.6-sol-20261001` run used the v1 extraction schema and is
kept immutable for provenance. New extraction runs use
`schemas/codex-change-episode-v2.schema.json`, which requires plain-language
titles, `when_to_use`, `anti_goals`, exclusions, inputs, action-linked steps,
step validation, a validation ladder, and stop conditions. Existing v1
episodes must be explicitly migrated or re-extracted before entering a v2
Workflow/Pattern catalog; consumers must not silently synthesize the missing
contract fields.
