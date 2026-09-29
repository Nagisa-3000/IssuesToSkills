# Universal Resolution Graph study (2026-09-29)

This document is the execution contract for the six-harness study.  It is
deliberately separate from the historical four-repository/DeepSeek study.  The
new study does not use DeepSeek and does not treat an issue's closed state as
evidence that a reusable Skill exists.

## Scope

The six repositories are:

| Harness | Repository |
| --- | --- |
| Pi | `earendil-works/pi` |
| Aider | `Aider-AI/aider` |
| Hermes | `NousResearch/hermes-agent` |
| Codex | `openai/codex` |
| Gemini CLI | `google-gemini/gemini-cli` |
| Qwen Code | `QwenLM/qwen-code` |

There are ten project-independent problem classes.  Their names describe the
invariant, not a repository feature or UI surface:

1. state-continuity-reconstruction;
2. bounded-resource-budget-control;
3. structured-tool-contract-integrity;
4. effect-control-and-isolation;
5. failure-recovery-and-retry;
6. provider-interface-adaptation;
7. configuration-and-environment-resolution;
8. extension-resource-lifecycle;
9. concurrent-work-coordination;
10. observable-validation-and-diagnostics.

Each repository/class bucket has a `train_candidate` and an independent
`holdout_candidate`, so the seed manifest has 120 candidate rows.  The class
definitions and selection policy are in
`experiments/manifests/universal-problem-classes-v1.json`; the issue seeds are
in `experiments/manifests/universal-issue-seeds-v1.json`.

## Corrected extraction flow

The corrected meta-skill is
`data/skill-extraction/packages/universal-resolution-distiller/SKILL.md`.
It defines the role as an evidence-bound episode distiller, not a patch author
and not an automatic issue-to-skill classifier.

The actual order is:

1. Verify the issue, linked PR/commit, changed files, call sites, and tests in
   the actual checkout.  A closed issue without an implementation-bearing
   resolution remains a rejected/audit record.
2. Produce one canonical ChangeEpisode with explicit before state, after state,
   diff summary, stable evidence ids, and unresolved questions.
3. Extract evidence-backed Change Actions.  Each Action has an intent, semantic
   module role, finite operation, pre-state, post-state, validation oracle,
   parameter slots, and evidence ids.  Paths, symbols, provider names, and
   commit ids stay in evidence/parameters rather than defining the abstraction.
4. Extract the complete Workflow from the episode and its Actions.  The
   Workflow is a partial-order DAG with `requires`, `enables`, `validates`, and
   `repairs` edges; it is not a renamed single Action.
5. Deduplicate Actions only at the same semantic level.  Grounded Actions can
   be proposed for reuse across repositories; unresolved semantics remain
   episode-local until an LLM judge has read the evidence.
6. Derive a Pattern only from multiple resolved Workflows.  Structural support
   is a candidate signal, not a promotion decision.  The Pattern must survive
   LLM adjudication and holdout validation.
7. Refuse all holdout episodes at the graph-building boundary.  Holdout cases
   are only used for retrieval/generalization and the paired agent evaluation.

The JSON contract was extended in
`schemas/codex-change-episode-v1.schema.json` with `semantic_action` and
`workflow_graph`.  The runner in
`experiments/run_codex_issue_episode_extraction.py` injects the corrected
meta-skill into the extraction prompt and now accepts an object manifest with a
`cases` array plus `--role train_candidate|holdout_candidate`.

Before graph construction, `experiments/validate_universal_episodes.py` checks
the stronger admission gates (closed/merged or locally pinned implementation,
qualifying implementation/call-site/test evidence, training-only role, and the
semantic Action/Workflow contracts).

## Graph and catalog

The deterministic structural stage is
`experiments/build_universal_resolution_graph.py`.  It emits the explicit
Action -> Workflow -> Pattern projection and records rejected/holdout episodes.
It does not silently decide semantic equivalence.

`experiments/materialize_universal_resolution_graph.py` is the persistence
boundary.  It maps:

```text
Pattern -> PatternStep -> Action
Workflow -> WorkflowStep -> Action
Action -> Action       (requires/enables/precedes/validates/repairs)
Pattern -> Workflow    (supported_by)
```

The catalog keeps authoritative node metadata/vectors in SQLite.  HNSW is a
rebuildable acceleration cache; exact dense search remains the correctness
oracle for the small-study catalog.

`experiments/adjudicate_universal_resolution_graph.py` is the semantic review
boundary.  It compares only same-level Action peers and judges Pattern
candidates from their supporting Workflows.  It writes proposals/transcripts
without mutating the historical graph; an unavailable LLM is recorded as
`deferred_no_api_key`.

For the local Windows Codex execution path, the equivalent real-model judge is
`experiments/run_codex_graph_adjudication.py`. It consumes only the admitted
training graph, uses the strict adjudication schema, and keeps its raw prompt,
response, stdout, stderr, and validation record beside the graph artifacts.

## Retrieval experiment

`experiments/run_universal_retrieval_eval.py` evaluates the holdout cases with
separate arms:

- sparse SQLite FTS;
- exact dense cosine;
- exact dense + hybrid RRF;
- exact dense + typed graph expansion;
- HNSW dense;
- HNSW hybrid;
- HNSW graph expansion.

The relevance label is explicit: a catalog node is relevant to a holdout query
when it belongs to the same universal problem class and came from the
training-derived catalog.  This measures cross-repository problem-class
transfer; it does not claim that retrieval alone repairs the issue.

The output records Recall@K, MRR, first relevant rank, latency/p95 latency,
seed/expanded counts, unresolved closure warnings, and a context-token proxy.
The proxy is only serialized text length divided by four; the agent evaluator
must use the provider's actual token usage.

`experiments/run_llm_retrieval_selection.py` adds the LLM router stage.  It
forms a sparse+dense candidate pool, asks the model to select bounded
`top_k`, `seed_k`, graph hops, exact/HNSW backend, and HNSW search parameters,
then executes the clamped plan deterministically.  Missing credentials or a
failed call is written as an explicit fallback arm and never merged with the
LLM arm.

## Holdout agent evaluation

The evaluator meta-skill is
`data/skill-extraction/packages/resolution-graph-evaluator/SKILL.md`.
`no_skill` and `guided` use fresh workspaces, identical model/provider,
settings, setup, task prompt, visible oracle, and time budget.  The guided arm
gets only the training-derived retrieval context plus its trace and an
applicability judgment.  The evaluator rejects leakage of the solution ref,
post-merge diff, target-only test, target repository's holdout record, or an
earlier transcript.

The existing execution harness is
`experiments/run_cross_project_holdout_agent_eval.py`; its historical manifest
adapter is intentionally kept separate until the six-repository universal
cases have implementation refs, visible-test patches, and setup commands.
`experiments/prepare_universal_agent_cases.py` is the conservative adapter for
that gate: it emits only cases with a resolvable verified solution commit and
records every unprepared row as a blocker.
The paired score must include end-task correctness, first-pass success,
localization, unrelated-file edits, style/lint regressions, omitted mandatory
actions, repair iterations, tool calls, wall time, input/cached/output/reasoning
tokens, and estimated cost.  Retrieval wins without a paired end-task win are
not promotion evidence.  The 60 candidate holdout table has now been audited
into 19 prepared cases; only three currently pass the strict functional-oracle
gate (base test fails and the hidden solution test passes), all from Hermes.
The remaining rows are retained with explicit blockers rather than being
silently promoted to agent cases; see
`data/skill-extraction/codex-universal-batch-20260929/holdout-cases-universal-v1/case-manifest.json`
and the qualification report under
`data/skill-extraction/codex-universal-batch-20260929/holdout-qualification-hermes-functional-v7/`.

## Current status and gates

Completed locally:

- six-repository/no-DeepSeek scope and ten universal classes;
- 120-row train/holdout seed and manifest shape validation;
- corrected extraction prompt/schema and two meta-skills;
- structural graph builder with holdout refusal and same-level Action reuse;
- SQLite catalog materializer;
- sparse/dense/HNSW/hybrid/graph retrieval evaluator;
- bounded LLM retrieval-parameter router with explicit fallback accounting;
- synthetic catalog test plus the repository's full test suite.
- rendered GitHub issue/PR evidence enrichment without spending more REST core
  quota;
- a conservative 30-case training extraction manifest: closed issue plus a
  locally resolvable direct commit or merged PR ref. The current distribution
  is Aider 1, Hermes 9, Qwen 9, Gemini CLI 5, Pi 3, and Codex 3; this is still
  uneven and is not treated as a complete 6 x 10 matrix;
- one real corrected-meta-skill Codex extraction, Aider #1842, admitted by the
  stronger episode gate;
- a real six-harness extraction batch: Aider #1842, Hermes #125235, Qwen #12029,
  Gemini CLI #29080, Pi #9994, and Codex #46960. All six passed the stronger
  episode gate after replacing Pi #10062, whose docs-only change was correctly
  rejected as having no Change Action/Workflow;
- four additional training extractions were then attempted: Hermes #125124,
  Gemini CLI #28518, and Codex #45773 passed; Qwen #11609 was correctly
  rejected because the agent could not ground a Change Action/Workflow;
- a further four were attempted: Hermes #123989, Qwen #12216, and Gemini CLI
  #28339 passed, while Codex #46336 was rejected for the same semantic
  admission failure. The first 14-case set therefore contained 12 admitted
  episodes;
- the corrected extractor was then run on Qwen #12047 (state continuity),
  Hermes #125942 (provider route adaptation), Gemini #29305 (a valid negative
  extraction: closed without an implementation-bearing resolution), and Qwen
  #12683. The first #12683 run deliberately rejected a stale issue-page ref
  `688e8afa`; a second run pinned the merged PR resolution `c9a9a8ad` and
  passed. Hermes #125942 was re-canonicalized against its locally pinned
  implementation commit because the issue timeline exposed a direct commit
  rather than a merged linked PR. The final admitted set is 15 episodes from
  18 distinct issue candidates and covers all ten universal classes;
- the fifteen-case training-only structural graph contains 42 extracted
  Actions, 19 Workflows, and 10 provisional Pattern candidates. Only the
  bounded-resource and concurrent-coordination candidates have structural
  support from multiple repositories. The expanded Codex semantic judge found
  no unambiguous Action equivalence: its one proposed pair was `unknown`
  because the postconditions/oracles differ. The consistency guard in
  `experiments/apply_universal_graph_adjudication.py` also refuses a
  contradictory `equivalent` row whose rationale says that postconditions or
  oracles differ. All ten Pattern candidates are deferred; none is promoted;
- the fifteen-case catalog is a 113-node SQLite catalog with a built HNSW
  cache. The 60-row holdout retrieval smoke compares sparse, exact dense,
  exact/hybrid graph, HNSW, and graph-expanded arms. On the current
  category-transfer label, sparse reached Recall@8 0.90, dense/HNSW and
  hybrid 0.80, and graph exact/HNSW 1.00. Dense-HNSW/hybrid achieved MRR
  0.9375; graph exact/HNSW achieved MRR 0.7125. These are retrieval signals,
  not end-task repair evidence;
- a real Codex retrieval-router call over all 60 holdout inputs on the final
  catalog. It returned 60/60 bounded plans with no guardrail violations (30
  exact, 30 HNSW; 42 audit-mode and 18 solve-mode plans), and the deterministic
  retriever executed those plans with category-transfer Recall@K 1.00/MRR
  0.6787. The router saw only holdout query text plus training-catalog
  candidate cards, never solution refs or target diffs.
- a first real paired end-task pilot on two strict Hermes holdouts: #125969
  (effect control/isolation) and #124006 (provider interface adaptation). Both
  `no_skill` and `guided` arms passed their visible functional tests, edited
  only the implementation files needed by the task, and did not edit the
  visible tests. The pilot is intentionally reported as n=2, not as a general
  effectiveness claim; #124211 is retained as an infrastructure retry because
  both original arms failed before producing any model event or token usage.

The 120-row manifest is still a discovery table, not 120 admitted episodes.
All 60 `train_candidate` issue pages currently have rendered-HTML state
`closed`; the latest HTML/API enrichment produces 30 rows that pass the
conservative local-ref/direct-commit-or-merged-PR extraction gate and 30
rejections. Eighteen distinct ready rows have now been sent through the real
corrected-meta-skill extractor; fifteen were admitted after the ref-correction
and local-pinned-commit audit, while Qwen #11609, Codex #46336, and Gemini
#29305 remain rejected. The 60 holdout rows remain outside graph construction
and have not been used as extraction evidence. This is coverage of all ten
classes, not a complete 6 x 10 repository/class matrix: the current admitted
repository counts are Aider 1, Hermes 4, Qwen 4, Gemini CLI 3, Pi 1, and
Codex 2. No synthetic issue is invented to fill the missing buckets.

The first Aider #1842 runner attempts exposed two runtime issues: direct WSL
launch of the Windows CLI could not use the UNC checkout, and the Windows
sandbox could not create processes from that path. The runner now has a
PowerShell bridge, stdin prompt delivery, and an explicit, default-off
`--codex-bypass-sandbox` switch for isolated staging checkouts. The successful
raw responses are preserved under
`data/skill-extraction/codex-universal-batch-20260929/`; the earlier Aider
pilot remains under
`data/skill-extraction/codex-universal-pilot-20260929-aider1842-direct/`.
The first six-case semantic judge proposed one same-repository
equivalent-action pair, but the expanded fifteen-case review did not find an
unambiguous merge; the fifteen-case result is the authority for the current
catalog. The real Codex retrieval router then produced 60/60 valid bounded
plans over the final catalog (30 exact, 30 HNSW; 42 audit-mode and 18
solve-mode; 48 plans with two graph hops and 12 with one), with zero
guardrail-error cases. Deterministic execution of those plans reached
category-transfer Recall@K 1.00, MRR 0.6787, mean first relevant rank 3.0,
and mean retrieval latency 14.283 ms. The router turn used 485,000 input
tokens (414,464 cached), 24,354 output tokens, and 12,368 reasoning tokens.
The router saw only holdout query text plus training-catalog candidate cards;
it never saw solution refs or target diffs. No holdout agent repair, no-skill
comparison beyond the two-case pilot, or Pattern promotion has been claimed.
For the two valid paired cases, the guided arm used fewer tokens and less wall
time on #125969, while the no-skill arm used fewer tokens and less wall time on
#124006; there is no consistent direction at n=2. This is descriptive only
because the sample is tiny and the agent model is stochastic. The runner records token/time metrics, changed files, visible
test-edit violations, and `git diff --check`; monetary cost is not reported
because the local Codex login does not expose a tariff. The HTTP-compatible
router artifact is also recorded as an explicit no-API-key fallback; it is
kept separate from the real Codex retrieval-router result and must not be
reported as an LLM-selected-parameter result.

## Reproducibility commands

From `arex-skill-graph`:

```bash
python3 experiments/build_universal_issue_manifest.py \
  --fetch \
  --output experiments/manifests/universal-issue-manifest-v1.json

python3 experiments/validate_universal_issue_manifest.py

python3 experiments/enrich_universal_html_evidence.py \
  --manifest experiments/manifests/universal-issue-manifest-v1.json \
  --output experiments/manifests/universal-issue-manifest-v1.json \
  --role train_candidate

python3 experiments/enrich_universal_pr_html_evidence.py \
  --manifest experiments/manifests/universal-issue-manifest-v1.json \
  --output experiments/manifests/universal-issue-manifest-v1.json \
  --role train_candidate

python3 experiments/build_universal_extraction_manifest.py \
  --manifest experiments/manifests/universal-issue-manifest-v1.json \
  --output experiments/manifests/universal-extraction-ready-v1.json \
  --role train_candidate

python3 experiments/run_codex_issue_episode_extraction.py \
  --manifest experiments/manifests/universal-extraction-ready-v1.json \
  --role train_candidate \
  --max-cases 60 \
  --output data/skill-extraction/codex-runs/universal-train-YYYYMMDD

python3 experiments/validate_universal_episodes.py \
  --episodes data/skill-extraction/codex-runs/universal-train-YYYYMMDD/episodes.json \
  --manifest experiments/manifests/universal-issue-manifest-v1.json \
  --output data/skill-extraction/codex-runs/universal-train-YYYYMMDD/admission-report.json \
  --accepted-output data/skill-extraction/codex-runs/universal-train-YYYYMMDD/episodes-admitted.json

python3 experiments/build_universal_resolution_graph.py \
  --episodes data/skill-extraction/codex-runs/universal-train-YYYYMMDD/episodes-admitted.json \
  --manifest experiments/manifests/universal-issue-manifest-v1.json \
  --output data/skill-extraction/graphs/universal-resolution-YYYYMMDD.json

python3 experiments/materialize_universal_resolution_graph.py \
  --graph data/skill-extraction/graphs/universal-resolution-YYYYMMDD.json \
  --db data/skill-extraction/catalogs/universal-resolution-YYYYMMDD.sqlite \
  --hnsw data/skill-extraction/catalogs/universal-resolution-YYYYMMDD.hnsw

python3 experiments/run_universal_retrieval_eval.py \
  --db data/skill-extraction/catalogs/universal-resolution-YYYYMMDD.sqlite \
  --hnsw data/skill-extraction/catalogs/universal-resolution-YYYYMMDD.hnsw \
  --cases experiments/manifests/universal-issue-manifest-v1.json \
  --output data/skill-extraction/evaluation/universal-retrieval-YYYYMMDD.json

python3 experiments/apply_universal_graph_adjudication.py \
  --graph data/skill-extraction/codex-universal-batch-20260929/graph-fifteen-structural.json \
  --adjudication data/skill-extraction/codex-universal-batch-20260929/codex-graph-adjudication-fifteen/adjudication.json \
  --output data/skill-extraction/codex-universal-batch-20260929/graph-fifteen-adjudicated.json

python3 experiments/run_codex_retrieval_router.py \
  --db data/skill-extraction/codex-universal-batch-20260929/catalog-fifteen.sqlite \
  --hnsw data/skill-extraction/codex-universal-batch-20260929/catalog-fifteen.hnsw \
  --cases experiments/manifests/universal-issue-manifest-v1.json \
  --role holdout_candidate \
  --output data/skill-extraction/codex-universal-batch-20260929/codex-retrieval-router-fifteen \
  --codex /mnt/c/Users/W/AppData/Roaming/npm/node_modules/@openai/.codex-hZCwy84M/node_modules/@openai/codex-win32-x64/vendor/x86_64-pc-windows-msvc/bin/codex.exe \
  --checkout /mnt/c/Users/W/AppData/Local/Temp/arex-skill-graph-codex/aider-1842 \
  --codex-bypass-sandbox
```

No command above promotes a candidate automatically.  Promotion requires the
evidence gate, same-level semantic judgment, cross-repository Workflow
support, and a clean holdout/no-skill comparison.
