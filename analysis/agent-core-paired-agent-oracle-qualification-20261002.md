# Paired-agent oracle qualification — 2026-10-02

## Scope

This stage prepares executable holdouts for the next no-skill versus Skill-guided coding-agent comparison. Holdouts remain evaluation-only: `extraction_forbidden: true`, their solution refs are hidden from prompts, and neither holdout may enter Action, Workflow, or Pattern induction.

The public task input is the GitHub issue title and body only. The preparer now preserves those fields verbatim rather than replacing the body with generic synthetic wording.

## Qualified cases

| Case | Reference status | Base | Candidate | Decision |
| --- | --- | ---: | ---: | --- |
| NousResearch/hermes-agent #43547 — context budget and compaction | Merged PR head `623b21b`; merge commit retained only as evaluator metadata | focused pytest fails | focused pytest passes | Qualified |
| earendil-works/pi #9735 — failure recovery and streaming | Closed, unmerged PR head `df3d408`; non-authoritative candidate | retry-classifier regression fails | classifier and harness regressions pass | Qualified as an executable candidate oracle only |

Hermes uses `tests/agent/test_context_compressor.py`. Pi uses both `packages/ai/test/retry.test.ts` and `packages/coding-agent/test/suite/regressions/9735-proxy-truncated-stream-retry.test.ts`.

## Environment controls

- Hermes invokes `/home/chenyujia/.local/bin/uv` explicitly so qualification does not depend on an interactive login PATH.
- Pi installs the locked workspace dependencies, restores the repository's generated provider model-data fixture, and transpiles only the missing `pi-ai/utils/uuid` package subpath needed by the harness test. These steps are applied identically to parent and candidate snapshots.
- The causal gate requires setup and patch application to succeed, at least one functional test to run, the parent to fail, and the candidate to pass.
- `git diff --check` remains a hygiene check and is excluded from the causal success denominator.

## Guidance safety change

The paired-agent runner now removes Patterns whose semantic decision is `defer`, `deferred_by_semantic_judge`, `reject`, or `rejected_by_semantic_judge` before the LLM applicability judge and before prompt rendering. Candidate-pending-holdout Patterns and independently retrieved Workflows remain judgeable. Exclusions are written to `excluded_guidance_hits` for audit.

## Artifacts

- Candidate source manifest: `experiments/manifests/agent-core-seven-category-extraction-v2/paired-agent-oracle-candidates.json`
- Prepared executable cases: `data/skill-extraction/agent-core-seven-category-extraction-v2/paired-agent-oracle-candidates-20261002/`
- Final qualification and filtered case manifest: `data/skill-extraction/agent-core-seven-category-extraction-v2/paired-agent-qualification-20261002/`

Only the two rows in `qualified-case-manifest.json` are eligible for the next paired agent run. Pi's candidate must continue to be reported as unmerged and non-authoritative even if it succeeds in the agent experiment.
