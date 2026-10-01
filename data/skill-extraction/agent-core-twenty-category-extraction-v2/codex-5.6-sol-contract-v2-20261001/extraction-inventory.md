# Agent-core twenty-category extraction inventory

This index combines the completed 01–07 and 08–20 extraction runs without duplicating their case artifacts.

## Scope

- Included: Issue/PR → ChangeEpisode → candidate Atomic → actionable Workflow.
- Deferred: Pattern construction, graph storage/retrieval, skill-guided holdout execution, feedback, and lifecycle evaluation.
- Holdout rule: four training cases plus one untouched different-repository holdout per category.

## Totals

- Categories: 20
- Training cases / admitted episodes: 80 / 80
- Candidate Atomics / Workflows: 218 / 83
- Manual / JSON Schema validation passes: 80 / 80
- Untouched holdouts / detected leaks: 20 / 0

## Component runs

- 01–07: `data/skill-extraction/agent-core-seven-category-extraction-v2/codex-5.6-sol-contract-v2-20261001/extraction-inventory.json`
- 08–20: `data/skill-extraction/agent-core-thirteen-category-extraction-v2/codex-5.6-sol-contract-v2-20261001/extraction-inventory.json`

## Categories

| # | Category | Episodes | Atomic | Workflow | Holdout |
| ---: | --- | ---: | ---: | ---: | --- |
| 01 | provider-interface-adaptation | 4 | 10 | 4 | earendil-works/pi #5823 |
| 02 | credential-resolution-and-authentication | 4 | 12 | 4 | Aider-AI/aider #750 |
| 03 | context-budget-and-compaction | 4 | 9 | 4 | NousResearch/hermes-agent #43547 |
| 04 | state-continuity-and-resume | 4 | 11 | 5 | openai/codex #47761 |
| 05 | structured-tool-contract-integrity | 4 | 11 | 4 | google-gemini/gemini-cli #29308 |
| 06 | effect-control-and-isolation | 4 | 11 | 4 | QwenLM/qwen-code #10859 |
| 07 | failure-recovery-and-streaming | 4 | 11 | 4 | earendil-works/pi #9735 |
| 08 | model-catalog-and-capability-metadata | 4 | 12 | 4 | Aider-AI/aider #4114 |
| 09 | provider-error-payload-normalization | 4 | 6 | 4 | QwenLM/qwen-code #7010 |
| 10 | subprocess-and-pty-lifecycle | 4 | 11 | 4 | QwenLM/qwen-code #1780 |
| 11 | permission-policy-enforcement | 4 | 14 | 4 | google-gemini/gemini-cli #17353 |
| 12 | path-root-and-worktree-resolution | 4 | 9 | 4 | openai/codex #810 |
| 13 | diff-rendering-and-review-navigation | 4 | 11 | 4 | earendil-works/pi #7903 |
| 14 | key-event-normalization-and-shortcuts | 4 | 7 | 4 | NousResearch/hermes-agent #91611 |
| 15 | unicode-width-and-terminal-rendering | 4 | 13 | 4 | openai/codex #46266 |
| 16 | extension-lifecycle-and-reload | 4 | 13 | 5 | openai/codex #47679 |
| 17 | link-integrity-and-browser-handoff | 4 | 8 | 4 | QwenLM/qwen-code #9069 |
| 18 | cross-platform-release-packaging | 4 | 12 | 4 | QwenLM/qwen-code #12649 |
| 19 | sensitive-data-redaction-in-diagnostics | 4 | 10 | 4 | Aider-AI/aider #94 |
| 20 | persistent-state-and-schema-consistency | 4 | 17 | 5 | QwenLM/qwen-code #9426 |

## Sample kinds

- `exact_table_row`: 7
- `verified_implementation_pull_request`: 52
- `verified_substitute`: 21

## Validation

- Validation errors: 0
- Holdout URL leaks: 0
- Deterministic corpus audit: `extraction-validation.json`
