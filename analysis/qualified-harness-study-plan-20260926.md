# Qualified Harness Study Execution Plan

Date: 2026-09-26
Repository: `arex-skill-graph`

## Objective

Build an auditable, leakage-controlled evaluation of evidence-grounded Skill
retrieval and cross-repository transfer on real agent-harness changes. The
study must separate retrieval effects from model-runtime effects and must not
promote an unverified episode into the strict catalog.

## Frozen experiment arms

For each held-out closed-Issue end task, run the same pre-merge base and hidden
regression tests under:

1. `no_skill` — task prompt only;
2. `raw_episode` — nearest verified raw change episode, without abstraction;
3. `flat_skill` — lexical/vector ranked Skill Cards, no graph expansion;
4. `graph_skill` — bounded typed graph expansion plus prerequisite/validation closure;
5. `cross_repository_graph_skill` — graph Skill plus Patterns whose evidence
   comes from repositories other than the target repository.

No arm may see the target PR, target post-merge commits, target hidden tests,
solution patch, or descendants created after the target merge.

## Work packages and gates

### WP0 — protocol and inventory (this turn)

- Freeze schemas for review labels, Workflow, Pattern, end task, hidden tests,
  runtime metrics, and leakage audit.
- Inventory current candidate manifests, local repositories, existing catalog,
  and runtime availability.
- Gate: every later artifact records source revision, cutoff, and provenance.

### WP1 — candidate review

- Review 8–12 high-quality candidates per repository across four repositories:
  Hermes, DeepSeek Harness, Pi, and Aider.
- Review labels must record verdict, domain, cross-repository potential, split
  decision, retained commits, dropped commits, and reason.
- Exclude docs-only, release-only, CI-only, reverts, merge noise, and changes
  without enough implementation/test evidence.
- Gate: 32–48 reviewed candidates; strict usable count and issue-grounded count
  reported separately.

### WP2 — strict Workflow catalog

- Build one or more Workflows only from `usable` or `usable_after_filter`
  labels, preserving split groups and retained commit IDs.
- Keep Commit/Hunk evidence and Validation nodes, but exclude evidence leaves
  from normal solve-mode hydration unless explicitly requested.
- Gate: 20–30 strict Workflows, at least three repositories represented, and no
  local-only episode silently promoted as issue-grounded.

### WP3 — Pattern candidates

- Induce 5–10 Pattern candidates only when supported by at least two Workflows
  from at least two repositories.
- Preserve supporting Workflow IDs, PatternStep order, predicates, evidence,
  and rejected/ambiguous mappings.
- Gate: every Pattern is traceable to source Workflows and has no repository-
  specific filename as its only abstraction.

### WP4 — real end tasks

- Select 8–12 closed-Issue/merged-PR chains with a clean pre-merge base,
  implementation plus regression evidence, and independently constructible
  hidden tests.
- Qualify base-fails/solution-passes before any model run.
- Gate: leakage audit passes and each task has a reproducible checkout.

### WP5 — hidden regression and leakage

- Hidden tests are generated or selected independently from the task prompt and
  are absent from the retrieval catalog.
- Audit target Issue, PR, commits, files, solution patch, descendant history,
  and target tests against every arm's context.
- Gate: zero target artifacts in retrieval context; missing oracle is reported,
  not counted as a retrieval failure.

### WP6 — runtime experiment

- Use an authenticated, version-pinned model runtime.
- Record model/version, prompt hash, input/output tokens, tool calls, retrieval
  latency, wall time, retries, cost, hidden-test result, and context node IDs.
- Run each arm with the same task order and at least two repetitions where
  possible.
- Analyze same-repository temporal holdout, held-out episodes, new Issues, and
  leave-one-repository-out transfer.

## Current status at freeze

- HNSW optional backend: implemented and tested; exact remains the default.
- Existing first review packet: 24 candidates, 6 per repository.
- Existing reviewed Workflow catalog: 23 provisional Workflows; it is not yet
  the final strict catalog because the review packet and Pattern promotion are
  incomplete.
- Authenticated model runtime: not yet available in this workspace.
- Therefore no agent success, real token, wall-time, or dollar-cost claim is
  valid yet.

## Artifact layout

- `data/review-samples/round1/`: initial reviewed episodes;
- `data/review-samples/round2/`: expansion candidates and labels;
- `data/strict-catalog/`: frozen strict Workflow/Pattern inputs and reports;
- `data/end-tasks/`: task manifests, qualification, hidden-test and leakage reports;
- `data/runtime-runs/`: model-runtime metrics only;
- `analysis/`: human-readable protocol and result reports.

## Immediate implementation order

1. Generate round-2 candidate packet with 8–12 candidates per repository.
2. Inspect and label round-2 episodes; rebuild strict Workflow catalog.
3. Add deterministic Pattern spec builder and provenance checks.
4. Add end-task manifest, qualification, hidden-test, and leakage commands.
5. Add runtime adapter interface and fail closed when no real runtime is configured.
6. Run the five arms and publish aggregate plus per-task results.
