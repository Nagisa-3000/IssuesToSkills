---
name: universal-resolution-distiller
description: Extract implementation-bearing Issue/PR evidence into validated candidate Agent Skill Packages with explicit Actions, provenance and eval cases; preserve JSON as intermediate records and holdouts for evaluation.
---

# Universal Resolution Distiller

Distill a real implementation-bearing Issue/PR into reusable resolution
knowledge. This is an **evidence-bound extraction meta-skill**. It does not patch
the target repository, treat similarity as truth, or publish an unvalidated
Pattern as a user-facing Skill.

## Use this skill when

- an Issue/PR/commit and its checkout can be inspected;
- the task is to extract reusable resolution knowledge from a completed change;
- the caller needs an evidence-backed Action, Workflow, or cross-project Pattern
  candidate;
- a training/holdout split and leakage audit are available.
- a category-scale corpus needs four or more cross-project training episodes
  while preserving a repository-disjoint untouched holdout.

## Do not use this skill when

- only an Issue title, label, commit subject, or embedding hit is available;
- the checkout cannot establish a before/after implementation and test oracle;
- the change is documentation-only, release noise, formatting-only, or an
  ungrounded merge/sync event;
- the target solution or holdout test is reserved for evaluation;
- the request is to modify the repository rather than extract knowledge.

## Evidence boundary

Start with one bounded `ChangeEpisode` containing:

- repository and issue/PR identity;
- pinned implementation ref and parent/base state;
- precise before, after, and diff summary;
- implementation, call-site, test, validation, and commit evidence;
- unresolved questions and known limitations.

Every semantic claim must cite stable evidence ids. If the before state, after
state, implementation boundary, or validation oracle is unknown, emit a
`deferred` or `rejected` record instead of guessing.

## Universal problem-class rule

Use a project-independent capability or invariant as the routing class. Good
classes describe boundaries such as bounded resource control, state continuity,
effect isolation, failure recovery, structured contract integrity, provider
adaptation, or lifecycle ownership. Do not use a repository path, UI surface,
release name, provider name, or keyboard shortcut as the reusable identity.

The class is a routing hypothesis only. Evidence may revise or reject it.

## Required operating order

```text
anchor issue and linked resolution
  -> verify checkout, parent, implementation, call sites, and tests
  -> create canonical ChangeEpisode
  -> extract semantic Actions / Atomics
  -> build an Issue Workflow DAG
  -> compile every grounded Workflow into a candidate Skill Package
  -> validate package, Action/evidence closure, hashes, and eval cases
  -> admit package-backed candidate records
  -> retrieve same-level peers
  -> LLM semantic dedup/adjudication
  -> induce Pattern candidates from multiple Workflows
  -> semantic Pattern adjudication
  -> compile only semantically accepted Pattern candidates
  -> validate on untouched holdout before promotion
```

Never induce a Pattern from one Issue or one Workflow. Never load a holdout
solution ref, target-only test, descendant commit, target repository solution
node, or previous agent transcript into training extraction or Pattern support.

For a multi-case category run, read
[`references/category-extraction-protocol.md`](references/category-extraction-protocol.md)
before selecting cases or launching extraction processes. Freeze the split
before any holdout solution inspection, isolate parallel case outputs, and run
`scripts/validate_extraction_inventory.py` before declaring the extraction
IR stage valid. Package materialization and validation are mandatory even when
the caller requests extraction only. Do not proceed into Pattern induction or agent evaluation when
the caller requested extraction only.

## Action / Atomic contract

An Action is one independently testable semantic operation, not a filename or
commit fragment. It must answer:

```yaml
semantic_action:
  title: <human-readable operation>
  intent: <observable capability or failure removed>
  module_role: <semantic owner, not a path or symbol>
  operation: <finite verb: normalize|guard|adapt|reconcile|map|validate|...>
  pre_state: <evidence-backed state predicate>
  post_state: <evidence-backed invariant>
  validation: <oracle and what it proves>
  parameters: <runtime entities/slots>
  evidence_ids: []
```

Split Actions when they have different semantic owners, validation oracles,
optional branches, or preconditions. Merge only when the evidence shows one
operation and one inseparable oracle.

## Workflow contract

A Workflow is a human-readable playbook for one problem scenario. It is not a
renamed Action list or a commit chronology. It must include:

```yaml
issue_workflow:
  title: <plain-language task title>
  goal: <observable target>
  when_to_use:
    - <problem signal or required precondition>
  anti_goals:
    - <what the agent must not change or optimize for>
  not_applicable_when:
    - <explicit exclusion or missing prerequisite>
  inputs: []
  steps:
    - action_ref: <real extraction-local action_name or materialized action_id>
      role: diagnose|establish-contract|implement|reconcile|validate|repair
      required: true
      depends_on: []
      condition: <optional branch predicate>
  edges:
    - from: <step id>
      to: <step id>
      type: requires|enables|validates|repairs
  exit_state: <completion invariant>
  validation_ladder: []
  stop_conditions: []
  unresolved_or_deferred: []
  evidence_ids: []
```

Every step reference must resolve to a real Action in the same extraction
record. The extraction contract may use `action_name`; graph materialization
must convert it to a stable `action_id` and reject dangling or ambiguous
references. Do not use a loose list of `atomic_names` as the only linkage.
Make optional branches and anti-goals explicit so an Agent can tell both what
to do and what not to do.

## Pattern contract

A Pattern is a cross-Workflow decision policy or invariant, not a generic class
label. Give it a human title and retain the machine category separately:

```yaml
resolution_pattern:
  title: <plain-language reusable principle>
  summary: <one-paragraph explanation>
  when_to_use: []
  anti_goals: []
  not_applicable_when: []
  invariants: []
  action_template:
    - role: <semantic action role>
      required: true
  decision_points: []
  ordering_constraints: []
  validation_ladder: []
  known_failure_modes: []
  exclusions: []
  supporting_workflow_ids: []
  supporting_repositories: []
  confidence: 0.0
  holdout_result: deferred|pass|fail|unavailable
```

Names such as `bounded-resource-budget-control` may remain routing keys, but
must not be the only user-facing description. Explain the invariant in plain
language, state when it applies, state anti-goals, and reference the concrete
Workflows and Actions that instantiate it.

Use structural alignment only to generate candidates. The semantic judge must
judge equivalence, applicability, optionality, exclusions, and human wording
from evidence-backed cards. Return `unknown` when evidence is insufficient.

## Retrieval and semantic boundary

BM25/FTS, dense vectors, HNSW, graph expansion, and structured filters only
produce bounded candidate pools. They do not decide:

- whether two Actions are duplicates;
- whether a Workflow applies;
- whether a Pattern is valid;
- whether a candidate should be promoted.

Record candidate ids, source repositories, graph traces, model, prompt version,
decision, rationale, evidence ids, latency, and tokens for every semantic
judge.

## Project context

Do not create repository paths or symbols as the reusable Skill identity. A
caller supplies a run-time `task_context`:

```yaml
task_context:
  repository: <repository slug>
  checkout: <absolute checkout>
  base_ref: <optional ref>
  language: <optional language>
  test_command: <optional command>
  target_scope: <optional scope>
```

A deterministic locator/probe may map semantic roles to the current checkout.
Store that mapping in the run record, not as a persistent ProjectBinding Skill
node.

## Promotion and stopping gates

Stop or defer when:

- no implementation-bearing resolution can be established;
- before/after state or validation oracle is missing;
- required Action/Workflow fields are unresolved;
- the evidence is target-only or belongs to a holdout split;
- the change is not a reusable behavioral resolution.

Promote a Pattern only when it has independent training Workflows from at least
two repositories, explicit `when_to_use` and anti-goals, a validation ladder,
no leakage, and a successful holdout/end-task result. Retrieval Recall alone is
not Pattern success.

## Mandatory completion contract

`resolution-skill-creator` is the reusable compiler component inside this
extraction, never an optional post-promotion step. The extractor returns JSON
under `schemas/codex-change-episode-v3.schema.json`; the runner compiles it into
the deliverable. Legacy v2 JSON may be migrated through the same compiler.

Each grounded Workflow must produce one self-contained package containing:

```text
<skill-name>/SKILL.md
<skill-name>/references/actions/*.md
<skill-name>/references/evidence/*.md
<skill-name>/references/workflow.md
<skill-name>/references/provenance.json
<skill-name>/evals/activation-cases.json
<skill-name>/evals/applicability-cases.json
<skill-name>/evals/functional-cases.json
```

Episode JSON is historical evidence. Atomic records become readable Action
references. Graph, SQLite and HNSW are storage/index projections. None of them
alone is an Agent Skill Package.

Use `experiments/materialize_candidate_skills.py` for selected validated
training responses, or the mandatory compiler in
`experiments/run_codex_issue_episode_extraction.py`. `--check` detects absent or
changed packages without writing. Never overwrite manual edits; create an
explicit new source/version when a revision is needed.

State progression is `structured -> evidence_validated -> skill_materialized
-> package_validated -> admitted_candidate`. JSON-only output is
`structured_only` or `materialization_pending`, with `extraction_success=false`.
Count real validated packages separately from candidate record counts.
Package structure and eval definitions do not mean functional evals ran.

The canonical root remains `data/skill-extraction/packages/`; generated
Workflow candidates live in `candidates/workflows/` below it. Do not duplicate
packages in a second independent root. Deferred/rejected Patterns stay as audit
IR and cannot provide serving guidance. A candidate package never becomes
promoted merely because its Markdown validates.
