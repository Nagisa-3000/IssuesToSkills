# AREX Skill Graph

This repository is the standalone prototype for evidence-grounded Skill mining,
multi-level organization, and retrieval used by AREX.

The current architecture and evaluation plan is documented in:

    /home/chenyujia/tritonToLlvm/arexskills_pilot/design/
    arex-skill-graph-rebuild-and-harness-eval.md

The system deliberately does not adopt an "everything is a plugin" runtime
model. DeepSeek Harness, Hermes Agent, Pi, Aider, and other agent harnesses are
source repositories to mine and evaluate, not architectural containers for this
project.

## MVP decisions

- Commit and hunk records are evidence nodes.
- Change Action is a concrete Case Action, not a reusable Skill. The smallest reusable knowledge node is an Atomic Skill: a small problem pattern plus a parameterized solution protocol and behavioral oracle.
- WorkflowStep and PatternStep make episode-level and cross-episode structure
  explicit.
- The knowledge store is a typed graph. Execution dependencies and routing
  projections may be DAGs; a tree is only a materialized browsing view.
- The online graph contains positive, retrieval-useful relations only.
- Exclusions, counterexamples, and incompatibilities are node fields and
  ranking/filter features. There is no conflict edge in the MVP.
- Online retrieval does not call an LLM.
- SQLite FTS provides lexical retrieval; the vector API has a deterministic
  exact fallback and an optional HNSW backend.
- Relation and semantic enrichment by an LLM, when used, is an offline,
  versioned, cached step.

## Canonical semantic planes

    Evidence --grounds--> CaseAction --part_of--> CaseWorkflow
                              |                        |
                           realizes                 realizes
                              v                        v
                         AtomicSkill <--uses-- WorkflowSkill --implements--> Pattern

CaseAction and CaseWorkflow are repository-specific instances, not Skills.
AtomicSkill, WorkflowSkill, and Pattern are reusable knowledge. ProjectBinding
is a runtime mapping from semantic roles and parameter slots to one checkout.

## Useful relations in the MVP

Cross-level:

- declares_step
- instantiates
- has_step
- realizes
- executed_by
- conforms_to
- evidenced_by
- supported_by
- applicable_when
- verifies
- grounds

Same-level:

- requires
- enables
- precedes
- validates
- repairs
- alternative_to
- specializes
- composes_with
- requires_pattern

## Multi-level Skill contract

The canonical v2 design is defined by:

- `design/agent-skill-aligned-hierarchy-v2.md`: the concise semantic and
  deployment design aligned with OpenAI, Anthropic, and the Agent Skills
  progressive-disclosure package model.
- `design/generalized-multilevel-skill-spec-v2.md`: the full instance,
  knowledge, runtime, evidence, promotion, and retrieval contract.
- `schemas/generalized-skill-family-v2.schema.json`: the current Draft 2020-12
  structural contract, including Agent Skill package projections.

The v1 design, schema, template, and validator remain in the repository only
for migration and audit. New extraction must not treat repository-specific
Change Actions or Issue Workflows as reusable Skills.

Candidate discovery and provenance are deterministic, but code-to-Skill
semantic extraction is explicitly `llm_code_reading`: the model must read
implementation code, before/after diffs, and test oracles. Commit subjects,
labels, filenames, and embedding similarity are candidate signals only.

Validate the contract and all tests with:

    PYTHONPATH=src python3 -m unittest discover -s tests -v

## Quick start

    python -m venv .venv
    .venv/bin/pip install -e .
    .venv/bin/arex-skill-graph init --db data/catalog.db
    .venv/bin/arex-skill-graph mine-git \
      --db data/catalog.db \
      --repo ../pi-agent \
      --repo-name earendil-works/pi \
      --limit 200
    .venv/bin/arex-skill-graph search \
      --db data/catalog.db \
      --query "prevent duplicate extension runtimes"

Build and explicitly use HNSW when the optional dependency is installed:

    .venv/bin/pip install -e '.[hnsw]'
    PYTHONPATH=src python3 -m arex_skill_graph.cli build-hnsw \
      --db data/catalog.db \
      --output data/catalog.routing.hnsw \
      --m 16 --ef-construction 200 --ef-search 64
    PYTHONPATH=src python3 -m arex_skill_graph.cli search \
      --db data/catalog.db \
      --query "prevent duplicate extension runtimes" \
      --vector-backend hnsw \
      --hnsw-path data/catalog.routing.hnsw

The HNSW graph's internal levels are ANN navigation levels only. They are
not the business Skill Graph layers. Business edges remain typed edges between
Pattern/PatternStep, Workflow/WorkflowStep, Action, evidence, and validation
nodes; HNSW does not create or replace those edges.

Batch-profile merge-based PR episodes without GitHub API calls:

    PYTHONPATH=src python3 -m arex_skill_graph.cli profile-local-pr-episodes \
      --repo ../deepseek-harness \
      --repo-name deepseek-ai/deepseek-harness \
      --limit 500 \
      --min-score 0.55 \
      --manifest-dir data/local-episodes \
      --output data/deepseek-local-profile.json

Export a selected manual-review packet:

    PYTHONPATH=src python3 -m arex_skill_graph.cli extract-local-pr-episodes \
      --repo ../deepseek-harness \
      --repo-name deepseek-ai/deepseek-harness \
      --number 791 --number 1873 --number 1977 \
      --output-dir data/review-samples/deepseek

Build the deterministic reviewed-Workflow baseline:

    PYTHONPATH=src python3 -m arex_skill_graph.cli build-reviewed-workflows \
      --db data/reviewed-workflows.db \
      --manifest-root data/review-samples/round1 \
      --labels data/review-samples/round1/review-labels.json

The first pilot uses deterministic commit-to-Action candidates to measure
throughput, storage, index latency, and retrieval behavior before paying for any
LLM semantic normalization.

## 真实案例提取与跨仓库综合

当前已完成的 evidence-grounded 提取与综合：

- `design/vendor-aligned-skill-standard-v3.md`
- `data/skill-extraction/cases/hermes-compaction-reservation/`
- `data/skill-extraction/cases/deepseek-compaction-reservation/`
- `data/skill-extraction/cases/pi-compaction-budget/`
- `data/skill-extraction/cases/aider-context-budget/`
- `data/skill-extraction/synthesis/residual-budget-family/`

Residual-budget family 的 Pattern 仍为 `provisional`；Hermes 与 DeepSeek 是 direct realizations，Pi 是 partial alignment，Aider 是 adjacent family。

## Lifecycle admission and bottom-up updates

The canonical browsing projection remains `Pattern -> Workflow -> Atomic`, but
skill nodes are versioned and can be aliased, merged, superseded, quarantined,
deprecated, or softly retired. New semantic decisions are handled by the
LLM-facing package at:

    data/skill-extraction/packages/skill-lifecycle-governance/SKILL.md

The admission path is intentionally cost-controlled:

1. FTS5/BM25, exact embeddings, and optional HNSW retrieve a small set of
   same-level peers;
2. only the LLM decides duplicate, mergeable, specialization, conflict, or
   no-match;
3. accepted Atomic changes trigger Workflow extraction and same-level Workflow
   adjudication;
4. only new/changed Workflows trigger Pattern extraction and same-level Pattern
   adjudication.

The implementation is in `src/arex_skill_graph/admission.py` and
`src/arex_skill_graph/lifecycle.py`. Structural storage checks remain local,
but semantic equivalence, applicability, failure root cause, and revision
content are not inferred from static keyword/threshold rules.

See `design/skill-lifecycle-and-bottom-up-admission-v1.md` and
`schemas/skill-lifecycle-v1.schema.json` for the contract. Runtime usage and
failure events are recorded for later quarantine/revision; historical versions
are never physically deleted.

## Included extraction artifacts

This checkout includes the reproducible project code, schemas, tests, retrieval
artifacts, and the extracted Agent Skills produced from cross-project issue/PR
episodes. The main published skill packages are:

- data/skill-extraction/packages/repair-shared-capacity-pressure/
- data/skill-extraction/packages/skill-lifecycle-governance/
- data/skill-extraction/synthesis/residual-budget-family/

Evidence-grounded episode material, manifests, reviewed samples, profiles, and
validation outputs live under data/skill-extraction/, data/review-samples/,
data/manifests/, and data/profiles/. Generated caches, local virtual
environments, temporary inspection files, and local SQLite catalogs are kept
out of version control by .gitignore; portable JSON/HNSW artifacts remain
available for retrieval experiments.

## Reproducibility

From the repository root:

    python3 -m venv .venv
    .venv/bin/pip install -e .
    PYTHONPATH=src python3 -m unittest discover -s tests -v

No API keys or provider credentials are required for the deterministic tests and
local retrieval pilots. External LLM extraction is configured at run time and
credentials must be supplied through environment variables rather than
committed to this repository.
