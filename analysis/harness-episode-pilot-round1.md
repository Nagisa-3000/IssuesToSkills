# Harness Episode Pilot - Round 1

Date: 2026-09-24

## Purpose

This pilot measures whether local Git object graphs can recover semantically useful merged-PR episodes cheaply enough to support AREX Skill extraction, and calibrates the first causal evaluation scale. It does not treat automatic scores as final labels.

## Corpus and extraction path

The profiler recognizes merge subjects shaped as `Merge pull request #N` or `Merge PR #N`. For each match it recovers:

- the PR commit set from first parent to second parent;
- the merged file set from first parent to merge result;
- title and body from the merge record;
- closing references from merge and commit messages;
- implementation, test, docs and generated-file evidence;
- contamination signals such as branch merges, very large commit/file sets and synchronization titles.

The synchronous path reads Git metadata and name-only tree diffs. It does not load blobs, calculate rename similarity, parse ASTs or call an LLM.

## Full-history local merge results

| Repository | All merge commits | Recognized PR merges | Evidence strong | Selection preferred | Selection review | Selection reject |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Hermes Agent | 3,012 | 1,724 | 1,105 | 1,072 | 384 | 268 |
| DeepSeek Harness | 7,939 | 1,782 | 1,261 | 734 | 410 | 638 |
| Pi | 397 | 208 | 91 | 90 | 96 | 22 |
| Aider | 677 | 283 | 38 | 34 | 118 | 131 |
| **Total** | **12,025** | **3,997** | **2,495** | **1,930** | **1,008** | **1,059** |

All 3,997 recognized merge episodes were reconstructed without an extraction error. These numbers are upper bounds: `preferred` means bounded and evidence-rich enough to review first, not automatically valid Workflow Skills.

Observed full-profile wall times were approximately:

| Repository | Recognized episodes | Wall time | Approx. episodes/s |
| --- | ---: | ---: | ---: |
| DeepSeek Harness | 1,782 | 25 s | 71 |
| Hermes Agent | 1,724 | 24 s | 72 |
| Pi | 208 | 1.4 s | 149 |
| Aider | 283 | 1.9 s | 149 |

This establishes that local metadata reconstruction is not the dominant cost. Blob/AST enrichment, semantic normalization, relation validation and end-to-end agent runs will dominate.

## Why evidence quality and extraction suitability are separate

The original evidence score rewards merged state, implementation files, tests, linked Issues and descriptive titles. It over-ranked examples such as a 147-commit "integrate latest master" PR because those facts were present.

The new selection score additionally penalizes:

- sync/rebase/integrate-main titles;
- merge commits inside the PR branch;
- very large commit or file sets;
- overly broad module/top-level surfaces;
- UI-only changes for the first infrastructure pilot;
- missing test evidence.

It retains explicit flags so human review can override the heuristic rather than hiding the reason for a penalty.

## Manual calibration sample

Twenty-four high-scoring episodes were reviewed across four repositories and common harness domains.

| Verdict | Count | Meaning |
| --- | ---: | --- |
| Usable Workflow | 18 | Coherent goal, implementation and validation chain |
| Usable after filtering | 3 | Drop merged-upstream or unrelated release commits before synthesis |
| Split required | 1 | One PR contains two unrelated fixes and must become separate Actions/episodes |
| Action only | 1 | Useful change but insufficient validation evidence for a Workflow |
| Defer domain-specific | 1 | Coherent, but not a common harness capability for the first causal pilot |

The 21 immediately or conditionally usable Workflows out of 24 are deliberately selection-biased. This ratio must not be projected onto all 3,997 episodes. It does show that the profiler can cheaply produce a high-yield manual-review queue.

The authoritative labels are in `data/review-samples/round1/review-labels.json`; the corresponding complete local manifests are beside it under repository subdirectories.

## Strongest initial cross-repository domains

1. **Model/provider adapters and error semantics**
   - DeepSeek per-model capability overrides;
   - Pi provider error bodies and raw stop reasons;
   - Aider OpenRouter/Azure adaptation;
   - Hermes provider fallback isolation.

2. **Context compaction and retry/budget invariants**
   - Hermes output-token reservation;
   - Pi compaction and branch-summary retry policy;
   - DeepSeek compact-record stream reading.

3. **Tool execution, approval and shell lifecycle**
   - DeepSeek code-mode executor collapse and persistent prompt lifecycle;
   - Hermes approval-timeout clamping;
   - Pi built-in-tool disabling contract.

4. **Authentication and credential persistence**
   - Hermes secret placement and model-list persistence;
   - Pi device-code OAuth factoring;
   - Aider AWS profile discovery;
   - DeepSeek bounded GitHub connectivity/auth fallback.

5. **Session persistence and derived-state recovery**
   - DeepSeek PR #791 is the primary rich Workflow;
   - more independent repository episodes are needed before promoting a cross-repository Pattern.

6. **Skill/plugin provenance and isolation**
   - Pi `.agents` provenance preservation;
   - Hermes plugin-context copy isolation.

Repository-specific UI polish, model catalog bumps, dependency-only changes and editing-format features should not be the first causal tasks.

## Recommended first extraction map

The first useful map should optimize for reviewed structural coverage rather than raw size:

- 60-80 manually reviewed Workflows;
- 4-6 shared harness domains;
- roughly 10-15 Workflows per domain where the corpus permits;
- approximately 3-8 Actions per Workflow, giving 240-500 Action nodes;
- 8-15 provisional cross-episode Patterns;
- all supporting Commit/Hunk evidence retained but excluded from normal solve-mode hydration.

At this size exact vector retrieval remains the correctness oracle. The same data should then be expanded with lower-cost Actions to benchmark 1k, 5k, 10k and 50k nodes before claiming HNSW-scale benefits.

## Retrieval and causal experiment

Retrieval-level arms, under identical candidate and hydration budgets:

1. lexical only;
2. exact dense only;
3. lexical+dense RRF;
4. flat learned ranker;
5. one-hop graph;
6. reverse-aware local PPR;
7. reverse-aware local PPR plus mandatory prerequisite/validation closure.

End-to-end task arms:

1. no Skill;
2. nearest raw commit/episode;
3. flat lexical/vector Skill;
4. graph Skill;
5. graph Skill plus cross-repository Pattern.

The first causal pilot should use 16-24 held-out implementation tasks across 4-6 domains, with at least two repetitions per arm. If cost is restrictive, start with 12 tasks and four arms (`no Skill`, `nearest episode`, `flat Skill`, `graph Skill`) for 96 runs, then add the cross-repository Pattern arm only after retrieval-level gains are demonstrated.

Required measurements:

- task/test success;
- correct module-role localization;
- mandatory-step and prerequisite coverage;
- patch precision and unrelated-file edits;
- repair iterations;
- model tokens, tool calls and wall time;
- p50/p95/p99 retrieval latency;
- extraction, embedding, indexing and graph-construction cost;
- index insertion throughput, memory and size;
- hydration characters/tokens.

## Leakage and transfer controls

- temporal holdout within each repository;
- leave-one-episode-out for Workflow retrieval;
- leave-one-repository-out for Pattern transfer;
- target Issue, final PR, descendant commits and target tests must be absent from the map;
- ranker and embedding snapshots must predate the target cut-off;
- report missing-oracle and unavailable-Skill cases separately from retrieval misses.

Cross-repository evaluation is required. Without it, the experiment cannot distinguish reusable Skill structure from memorizing repository-local names and paths.

## Current limitations and next implementation step

- Merge-based recovery misses squash and rebase merges.
- The module-family classifier is a routing heuristic, not a final label.
- Test-path presence does not yet prove implementation-test correspondence.
- GitHub review comments and checks are absent where public API metadata is unavailable.
- Pattern promotion has not yet been run on the reviewed sample.

The reviewed manifests have now been turned into an explicit deterministic baseline containing Action, WorkflowStep, Workflow and Validation nodes while preserving filtered, split-required and Action-only decisions. The current reviewed map contains 23 Workflows, 91 WorkflowSteps, 92 Actions, 92 Commit evidence nodes and 22 Validation nodes. The next steps are to refine role/partial-order induction, build a retrieval-gold manifest, and benchmark HNSW and local sparse PPR on this reviewed map plus controlled scale expansions.
