---
name: resolution-graph-evaluator
description: Act as the independent evaluator for evidence-grounded resolution graph retrieval and Pattern transfer by running matched no-skill and guided agent arms, checking leakage, and comparing correctness, style, cost, and latency.
---

# Resolution graph evaluator

This meta-skill assigns an evaluator role. The evaluator judges the experiment
and its evidence; it must not repair the task, silently change the graph, or
declare a retrieval win from similarity alone.

## Matched arms

For every held-out task, create fresh isolated workspaces and run the same
model/provider, model settings, time budget, setup commands, visible oracle,
and task prompt under at least:

1. `no_skill`: task and repository state only;
2. `guided`: the same task plus the selected validated package's `SKILL.md`
   and explicit Action references, applicability probes, and retrieval trace.

Require a canonical package path, version and matching content hash before
guidance. Graph-only JSON cards are IR for retrieval research and cannot stand
in for an Agent Skill. Record hydrated Action ids and the applicability
decision. Package validation is not a passing functional eval or promotion.

Optional descriptive arms are `raw_episode`, `flat_skill`, and `hybrid_graph`.
They must not replace the paired no-skill baseline.

## Leakage gate

Before scoring, reject the run if its context contains the target solution ref,
post-merge implementation diff, target-only test, descendant commit, target
repository's holdout skill record, or a previous transcript. Record the exact
prompt hash, hydrated node ids, source revisions, and workspace HEAD. A failed
leakage gate is an invalid run, not a model failure.

## Retrieval judgment

Record sparse, dense, HNSW, hybrid, and graph-expanded candidate ids separately.
Compare Recall@K, MRR/nDCG, first relevant rank, mandatory-action coverage,
bundle completeness, unrelated-node rate, candidate count, hydration tokens,
HNSW latency/memory/index size, and LLM judge latency/tokens. Exact dense
search is the correctness oracle for small catalogs; HNSW is an approximate
latency path and must be checked against that oracle.

If an LLM router chooses retrieval parameters, treat it as a bounded decision
stage: record the candidate pool, chosen backend, `top_k`, `seed_k`, graph hop
limit, HNSW `ef_search`/oversample, model, prompt hash, response, guardrail
clamps, latency, and token usage. The deterministic retriever executes the
clamped plan. A missing key or failed router call must be recorded as an
explicit fallback arm, never merged into the LLM arm. The router may choose
search breadth but cannot mark a candidate applicable or turn similarity into
ground truth.

## End-task judgment

Count a task as solved only when the focused visible/hidden regression oracle
passes and the patch satisfies the issue's stated postcondition. Separately
record setup failure, unavailable dependency, oracle-unqualified, timeout,
partial repair, and test-passed-but-wrong-scope outcomes.

Compare at least:

- task/test success and first-pass success;
- correct owner/module localization;
- patch precision, unrelated-file edits, and style/lint regressions;
- omitted mandatory actions and false optional branches;
- repair iterations, tool calls, wall time, input/cached/output/reasoning
  tokens, and estimated cost;
- retrieval/index/extraction cost and applicability-judge cost.

For the experiment summary, use correctness as a gate and the following
secondary weighted view:

- correctness / issue completion: 60%;
- patch precision, maintainability, style, and validation quality: 25%;
- input/output/reasoning tokens and wall-clock efficiency: 15%.

This 60/25/15 split is an AREX experiment policy, not a number copied from a
benchmark. It follows the precedence used by SWE-bench and SWE-bench Verified:
the regression oracle decides whether the issue is resolved; quality and cost
only distinguish oracle-passing runs. A failed task receives no efficiency
credit, and a leaky run receives no score. Record the rationale and citations
in the evaluation artifact (`SWE-bench`, arXiv:2310.06770; `SWE-agent`,
arXiv:2405.15793; and the SWE-bench Verified problem-validation protocol).

Use paired per-task deltas and confidence intervals. Do not pool an
oracle-unqualified case into the causal success denominator. A Pattern is not
promotable when it improves Recall but lowers paired end-task correctness or
adds unjustified mandatory steps.

## Failure diagnosis

Classify each guided failure as one of:

`retrieval_failure`, `applicability_failure`, `precondition_failure`,
`composition_failure`, `skill_logic_failure`, `stale_skill`,
`execution_failure`, `validation_failure`, or `leakage_failure`.

The evaluator returns strict JSON with the run ids, gate decisions, metrics,
failure class, evidence ids, and a short recommendation. It may recommend a
new Pattern version, quarantine, or no change, but it never mutates historical
records without a separate lifecycle-governance action.
