---
name: resolution-skill-creator
description: Compile an evidence-grounded Workflow or promoted cross-project Pattern into a human-readable Agent Skill package with when-to-use rules, anti-goals, explicit action references, validation, provenance, and activation tests.
metadata:
  short-description: Compile governed Resolution Graph records into an Agent Skill package
---

# Resolution Skill Creator

Compile an admitted AREX Resolution Graph record into a portable Agent Skill
package. This skill is a **compiler and evaluator**, not an issue miner, patch
author, semantic deduplicator, or automatic Pattern promoter.

## Use this skill when

- a validated Atomic, Workflow, or promoted Pattern must become a reusable
  `SKILL.md` package;
- a Workflow or Pattern needs a human-readable `when_to_use`, `anti_goals`,
  `not_applicable_when`, explicit Action sequence, and validation ladder;
- an existing Skill package needs a versioned, evidence-preserving update;
- activation and functional evals must be created for a Skill before promotion.

## Do not use this skill when

- the source is only an Issue title, commit subject, filename, or embedding
  match without implementation evidence;
- the source Workflow or Pattern has unresolved required semantics;
- a Pattern has not passed its multi-Workflow/repository and holdout gates;
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
- **Pattern:** compile to a cross-project Skill only after semantic
  adjudication and a leakage-audited holdout result. A structural candidate is
  never published as a promoted Skill.

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
2. Run the promotion gates in `references/promotion-gates.md`. If a gate fails,
   emit a `candidate` or `deferred` artifact instead of a discoverable Skill.
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
7. Run structural validation and the activation/functional evals. Record model,
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
│   ├── action-contracts.md
│   ├── validation.md
│   └── provenance.yaml
├── scripts/                       # optional deterministic helpers
├── assets/                        # optional templates/fixtures
└── evals/
    ├── prompts.jsonl
    ├── rubric.schema.json
    └── expected.jsonl
```

Read only the references needed for the current source level. Use
`references/agent-skill-contract.md` for package compatibility and
`references/promotion-gates.md` for the graph-specific gates.

## Failure handling

Return a structured `deferred` result when evidence, action references,
validation, or holdout support is insufficient. Explain the missing evidence and
identify the next safe probe. Never fill missing semantics from title,
similarity, or repository convention.
