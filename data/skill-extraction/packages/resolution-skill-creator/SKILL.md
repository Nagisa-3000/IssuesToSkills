---
name: resolution-skill-creator
description: Compile evidence-validated Workflow records and semantically accepted Pattern candidates into portable Agent Skill Packages; validate Action/evidence references and eval definitions before candidate admission, with holdout gates reserved for promotion.
metadata:
  short-description: Compile governed Resolution Graph records into an Agent Skill package
---

# Resolution Skill Creator

Compile an evidence-validated AREX Resolution Graph record into a portable Agent Skill
package. This skill is a **compiler and evaluator**, not an issue miner, patch
author, semantic deduplicator, or automatic Pattern promoter.

## Use this skill when

- a grounded Workflow or semantically accepted Pattern must become a candidate
  `SKILL.md` package;
- a Workflow or Pattern needs a human-readable `when_to_use`, `anti_goals`,
  `not_applicable_when`, explicit Action sequence, and validation ladder;
- an existing Skill package needs a versioned, evidence-preserving update;
- activation and functional evals must be created for a Skill before promotion.

## Do not use this skill when

- the source is only an Issue title, commit subject, filename, or embedding
  match without implementation evidence;
- the source Workflow or Pattern has unresolved required semantics;
- a Pattern was deferred/rejected by the semantic judge, or lacks independent
  multi-Workflow/repository support;
- the request is to directly modify the target repository rather than compile a
  Skill package;
- the package would hard-code a repository path, symbol, provider name, or
  solution ref as the reusable identity.

## Source-level policy

- **Atomic/Action:** compile to an Action reference by default. Create a
  standalone Skill only when the Action is a complete, user-facing operation
  with its own oracle.
- **Workflow:** compile to a task-oriented Skill when it has explicit action
  ids, ordering/branch conditions, `when_to_use`, `anti_goals`, and a
  validation ladder.
- **Pattern:** compile an accepted cross-project candidate after semantic
  adjudication and training leakage checks. Keep `status: candidate` while the
  holdout is pending. Holdout success is required for promotion; structural
  candidates and deferred/rejected records never supply serving guidance.

## Required human-readable contract

Every compiled Workflow or Pattern must expose, in plain language:

1. `when_to_use`: observable task/problem signals and required preconditions;
2. `anti_goals`: things the Agent must not optimize for or change;
3. `not_applicable_when`: explicit exclusions and missing prerequisites;
4. `inputs`: task context, repository, checkout/ref, and available oracles;
5. `actions`: real graph `action_id` references with role, required/optional
   status, conditions, and dependencies;
6. `validation_ladder`: focused, integration, and regression oracles;
7. `stop_conditions`: when to ask, defer, or refuse rather than guess;
8. provenance: source Workflow/Pattern ids and evidence ids in references,
   not in the user-facing title.

Use a human title for discovery and keep the machine category/id as metadata.
Do not expose generic titles such as “resolve bounded resource control through
an evidence-validated change chain” as the only Skill description.

## Runtime project context

Do not create a persistent `ProjectBinding` knowledge layer solely to store
repository paths. The caller supplies a `task_context` at runtime:

```yaml
task_context:
  repository: <repository slug>
  checkout: <absolute checkout>
  base_ref: <optional ref>
  language: <optional language>
  test_command: <optional command>
  target_scope: <optional scope>
```

A compiled Skill may ask a deterministic locator/probe to map semantic roles to
this checkout. Store that mapping in the run record, not in the reusable Skill
identity.

## Compilation procedure

1. Load the source record, supporting Workflows/Actions, evidence ids,
   validation results, and lifecycle status.
2. Run evidence and package gates in `references/promotion-gates.md`. Missing
   required semantics means an explicit defer record. A structurally valid
   package is a candidate; empirical promotion is a separate decision.
3. Humanize the title and summary. Preserve the universal invariant; remove
   repository paths, issue numbers, commit ids, and product-specific names from
   the reusable identity.
4. Normalize each Workflow step to a real `action_id`. Reject dangling ids,
   missing required steps, cycles that contradict the declared workflow, or
   validation steps without an oracle.
5. Write a concise `SKILL.md`. Put detailed evidence, examples, schemas, and
   mode-specific procedures in `references/`; use `scripts/` only for
   deterministic repeatable operations.
6. Generate activation evals covering direct, indirect, contextual,
   incomplete, negative, and edge requests. Generate a functional rubric that
   checks action coverage, anti-goal violations, tests, unrelated edits, and
   leakage.
7. Run structural validation. Mark generated activation/applicability/functional
   eval definitions `not_executed` until they actually run. Record model,
   prompt version, hydrated source ids, tokens, latency, and grader results.
8. Publish only a versioned artifact whose gates pass. Keep rejected/deferred
   source records and historical versions; never silently overwrite them.

## Package layout

```text
<skill-name>/
├── SKILL.md
├── agents/openai.yaml             # optional UI/dependency metadata
├── references/
│   ├── workflow.md
│   ├── actions/*.md
│   ├── evidence/*.md
│   └── provenance.json
├── scripts/verify_package.py       # optional, standalone deterministic verifier
├── assets/                        # optional templates/fixtures
└── evals/
    ├── activation-cases.json
    ├── applicability-cases.json
    └── functional-cases.json
```

`src/arex_skill_graph/skill_packages.py` implements the deterministic Workflow
compiler. `experiments/materialize_candidate_skills.py` provides selected-case
batch compilation and `--check`. Output is idempotent, content hashed, and
refuses manual-edit conflicts. The canonical package root is
`data/skill-extraction/packages/`; Workflow candidates use
`candidates/workflows/`. Legacy Pattern compiler packages retain their v1
layout for audit and compatibility; do not count them as v2 packages or use
them through v2 serving hydration without migration.

Read only the references needed for the current source level. Use
`references/agent-skill-contract.md` for package compatibility and
`references/promotion-gates.md` for the graph-specific gates.

## Failure handling

Return a structured `deferred` result when evidence, action references,
validation, or holdout support is insufficient. Explain the missing evidence and
identify the next safe probe. Never fill missing semantics from title,
similarity, or repository convention.
