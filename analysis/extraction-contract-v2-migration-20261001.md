# Extraction contract v2 migration

The first seven-category extraction run is a valid v1 evidence corpus, but its
Workflow schema predates the current human-readable Skill contract. In
particular, the archived Workflows contain goals, entry/exit states, action
names, and graph edges, but do not uniformly contain:

- `when_to_use`;
- `anti_goals`;
- `not_applicable_when`;
- runtime inputs;
- required/optional Action status and dependencies;
- step-level validation;
- a validation ladder;
- stop conditions;
- a separate plain-language title.

The extractor now defaults to
`schemas/codex-change-episode-v2.schema.json`. The runner rejects dangling
Action references and incomplete Workflow contracts rather than inventing
them downstream. The graph builder preserves the new fields and remains
backward-readable for archived v1 artifacts.

## Compatibility boundary

- `data/skill-extraction/agent-core-seven-category-extraction-v2/codex-5.6-sol-20261001/`
  remains immutable v1 provenance.
- New runs must use v2 and record the schema path in `codex-command.json`.
- v1 Workflows may support migration prompts, but they are not considered
  publishable v2 Workflow or Pattern contracts until the missing fields have
  been evidence-grounded by re-extraction or explicit semantic review.
- Holdout Issues remain untouched during migration.

## Verified implementation changes

- v2 JSON Schema added;
- extraction prompt now requests human wording, when-to-use rules, anti-goals,
  exclusions, action-linked steps, validation, and stop conditions;
- runtime validation checks Action linkage and mandatory contract fields;
- graph materialization preserves the v2 Workflow fields;
- regression tests cover schema acceptance, dangling Action rejection, and
  missing when-to-use/anti-goal rejection.
