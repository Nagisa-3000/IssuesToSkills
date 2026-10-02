# Agent-core paired Skill evaluation and feedback ingestion — 2026-10-02

## Executive summary

Two independently qualified held-out agent-harness issues were run through matched
no-Skill and Skill-guided Codex arms using the same model, provider, setup, visible
regression tests, and evaluation policy:

- NousResearch/hermes-agent #43547: context budget and compaction.
- earendil-works/pi #9735: premature stream termination and bounded retry.

Both arms solved both issues. The guided arm was faster in both cases and produced a
narrower Hermes patch, but neither score delta crossed the evaluator's two-point
win threshold. The aggregate result is therefore two full ties, not evidence for a
Pattern promotion.

The successful guided uses were ingested into a copied lifecycle registry as two
idempotent success events. The serving nodes, graph edges, embeddings, baseline
catalog, and HNSW index were not changed. Both selected provisional nodes map to
candidate registry records; no Skill was promoted, revised, merged, quarantined,
deprecated, or retired.

## Artifacts

### Qualified holdouts

- Qualification analysis:

  `analysis/agent-core-paired-agent-oracle-qualification-20261002.md`
- Oracle candidate manifest:

  `experiments/manifests/agent-core-seven-category-extraction-v2/paired-agent-oracle-candidates.json`
- Qualification output:

  `data/skill-extraction/agent-core-seven-category-extraction-v2/paired-agent-qualification-20261002/`

### Paired agent evaluation

`data/skill-extraction/agent-core-seven-category-extraction-v2/paired-agent-evaluation-20261002/`

This directory contains the matched manifests, retrieval and judge records, prompts,
patches, validation logs, per-arm measurements, independent weighted evaluations,
and the cross-case aggregate.

### Neutral feedback registry

`data/skill-extraction/agent-core-seven-category-extraction-v2/paired-agent-feedback-20261002/`

- `catalog.sqlite`: copied semantic catalog plus lifecycle registry records and usage
  events.
- `feedback-report.json`: source checksums, gates, accepted events, registry counts,
  non-mutation checks, promotion blockers, and oracle caveats.

The ingestion implementation and tests are:

- `experiments/ingest_paired_agent_feedback.py`
- `tests/test_ingest_paired_agent_feedback.py`

## Experimental controls

Both arms used:

- model: `openai/gpt-5.6-sol`
- OpenAI-compatible endpoint: `https://llm.rvnpu.cn/v1`
- Codex profile: `rvnpu-test`
- graph expansion: one hop
- fresh, independent, ephemeral Codex sessions per arm
- the same parent revision, setup commands, visible tests, and post-run evaluator
- no access to the candidate solution revision

The no-Skill arm received only the issue task. The guided arm additionally received
materialized guidance selected by BM25/embedding/HNSW retrieval, graph expansion,
and an LLM applicability judge. Raw API credentials were not persisted in any
artifact.

## Causal qualification

A held-out case was eligible only when the visible regression failed on the parent
revision and passed on the candidate revision.

| Case | Parent | Candidate | Oracle gate | Caveat |
|---|---:|---:|---:|---|
| Hermes #43547 | fail | pass | qualified | Candidate is a merged pull-request head with focused regression tests. |
| Pi #9735 | fail | pass | qualified | Candidate is an unmerged, non-authoritative pull-request head. It is executable oracle evidence only and must not be described as the official project resolution. |

Both evaluation manifests also retain the public issue title and body and set:

- `extraction_forbidden: true`
- `solution_hidden_from_agent: true`
- `split: held_out_test`

## Retrieval, graph expansion, and LLM selection

### Hermes #43547

The retrieval judge selected:

- `pattern:8105d8c0f3d9ec16`
- **Repair budget decisions at their policy boundary**
- confidence: `0.96`

The judge located the defect at the policy boundary that computes the effective
input budget, rather than in downstream compaction mechanics. Materialized guidance
also included related Workflow and Action nodes, including the requirements to
repair the owning budget policy and lock competing precedence branches with focused
checks.

No deferred or rejected Pattern entered the Hermes prompt.

### Pi #9735

The retrieval judge selected:

- `workflow:bca58288062025eb`
- **recover-recognized-premature-stream-termination**
- confidence: `0.93`

The selected Workflow matched the causal repair: admit a narrowly recognized
premature-close representation into the existing bounded retry policy and validate
both classification and end-to-end retry behavior.

The top-ranked broad streaming Pattern was explicitly excluded:

- `pattern:9cb94d22583f2781`
- **Defer a Unified Streaming Recovery Policy**
- decision: `deferred_by_semantic_judge`

This demonstrates that the guidance gate distinguishes a usable Workflow from a
semantically deferred Pattern instead of passing every high-ranking graph node to
the agent.

## Paired execution results

### Hermes #43547

| Metric | No Skill | Guided | Guided delta |
|---|---:|---:|---:|
| Visible regression | pass | pass | tie |
| Wall time | 426.385 s | 295.328 s | -131.057 s |
| Evaluator usage tokens | 1,167,739 | 1,051,322 | -116,417 |
| Changed files | 4 | 2 | -2 |
| Correctness score | 99.2 | 99.0 | -0.2 |
| Code-quality score | 90.0 | 86.6667 | -3.3333 |
| Efficiency score | 81.7236 | 100.0 | +18.2764 |
| Overall score | 94.2785 | 96.0667 | +1.7882 |

The guided arm was materially faster, used fewer tokens, and kept the change to the
initialization and context-compressor owners. The no-Skill arm received a slightly
higher code-quality score, so the overall delta remained below the evaluator's
2-point decision threshold.

Outcome: `full_tie`.

### Pi #9735

| Metric | No Skill | Guided | Guided delta |
|---|---:|---:|---:|
| Visible regression | pass | pass | tie |
| Wall time | 121.721 s | 109.981 s | -11.740 s |
| Evaluator usage tokens | 176,188 | 183,409 | +7,221 |
| Changed files | 1 | 1 | 0 |
| Correctness score | 96.8 | 98.4 | +1.6 |
| Code-quality score | 93.3333 | 95.3333 | +2.0 |
| Efficiency score | 96.1419 | 97.6377 | +1.4958 |
| Overall score | 95.8346 | 97.5190 | +1.6844 |

The guided arm was faster and received higher semantic-completion, patch-scope, and
maintainability scores. It used 7,221 more aggregate usage tokens because its input
context was larger, although its output and reasoning token counts were lower. The
overall delta again remained below the evaluator threshold.

Outcome: `full_tie`.

## Aggregate decision

The aggregate contains two independent cases and two eligible replicates:

| Aggregate | No Skill | Guided |
|---|---:|---:|
| Solved cases | 2/2 | 2/2 |
| Solved rate | 1.0 | 1.0 |
| Independent advantages | 0 | 0 |

Outcomes: two `full_tie` results.

The configured promotion policy requires:

- at least 3 independent holdout cases;
- at least 2 independent guided-advantage cases;
- a guided solved-rate delta of at least 0.20;
- no leakage or oracle failures.

The current evidence fails the first three requirements. Promotion blockers are:

- `insufficient_independent_holdout_cases`
- `insufficient_independent_guided_advantage_cases`
- `guided_solved_rate_delta_below_threshold`

Therefore `pattern_promotion_supported` is `false`.

## Feedback and lifecycle ingestion

The feedback step accepts only a guided result that passes all of the following:

1. parent-fail/candidate-pass oracle qualification;
2. held-out test and solution-hidden manifest constraints;
3. successful setup, non-empty patch, unchanged visible tests, and passing tests;
4. no solution-reference leakage;
5. independent evaluator confirmation that the issue postcondition is satisfied;
6. an applicable retrieval-judge selection that is both eligible and approved;
7. a selected Skill node that is not terminal, deferred, or rejected.

Accepted events:

| Case | Used Skill | Result | Validation | Event ID |
|---|---|---|---:|---|
| Hermes #43547 | `pattern:8105d8c0f3d9ec16` | success | pass | `usage:c6267d20573a7d2ae53627c3` |
| Pi #9735 | `workflow:bca58288062025eb` | success | pass | `usage:3e25a09b763ae480440de96b` |

Registry result:

- 2 Skill records
- 2 success usage events
- 2 audit-only `paired_agent_feedback` lifecycle events
- 0 failure events
- 0 failure incidents
- 0 lifecycle status mutations
- 0 revisions
- 0 merges
- 0 quarantines
- 0 deprecations
- 0 retirements
- 0 promotions

The serving lifecycle of both selected nodes remains `provisional`. The lifecycle
registry maps `provisional` to `candidate` because `SkillStatus` intentionally has no
separate provisional state. This mapping occurs only in the derived registry; it does
not rewrite the serving node.

## Storage integrity

Baseline semantic catalog:

- SHA-256: `d5cd230faca8787d1918cbc23a58ee92bf33b4badf8ec6290523626d10f969e7`
- unchanged by feedback ingestion: yes

Baseline HNSW index:

- SHA-256: `45cd24da5168255de2c3f446002de4cf32cb44a1051df92b6a39c7231609026e`
- rebuilt: no
- unchanged by feedback ingestion: yes

The copied registry preserves the serving projection exactly:

- nodes: 221 before and after
- edges: 365 before and after
- embeddings: 221 before and after
- content fingerprints for all three tables are unchanged

## Interpretation

The experiment supports three limited conclusions:

1. Retrieval plus LLM applicability judging selected usable guidance for both
   qualified held-out issues.
2. The deferred-Pattern exclusion worked: Pi used the narrower valid Workflow rather
   than a broad Pattern whose own semantic review said not to generalize it.
3. Guidance was compatible with successful task completion and improved wall time in
   both cases, but the sample does not establish a solved-rate advantage or Pattern
   generalization benefit.

It does **not** support promoting the Hermes Pattern, inducing a unified streaming
Pattern from the Pi result, or changing any merge/retirement state.

## Required next evidence

The next evaluation round should add independently qualified holdouts from additional
repositories, preserving one untouched issue per problem class. Priority should be
given to cases whose parent revision reliably fails a focused regression and whose
candidate revision has an implementation-bearing patch. The same paired protocol and
independent evaluator should be retained so that additional cases are comparable to
this baseline.
