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
AtomicSkill, WorkflowSkill, and Pattern are reusable knowledge records. Those
legacy graph type names do not imply an executable Agent Skill Package. ProjectBinding
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

    PYTHONPATH=src python3 -m pytest -q

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
artifacts, and candidate knowledge records produced from cross-project issue/PR
episodes. Complete packages have an actual `SKILL.md`; the 80 historical
training Episodes and 83 Workflow records are frozen IR and are not 83 Agent
Skills. The small package materialization experiment currently supplies two
validated candidate Workflow packages with six explicit Action references.

The package roots and examples are:

- data/skill-extraction/packages/repair-shared-capacity-pressure/
- data/skill-extraction/packages/skill-lifecycle-governance/
- data/skill-extraction/packages/candidates/workflows/

`data/skill-extraction/synthesis/residual-budget-family/` contains synthesis
records and evidence, counted separately from packages.

## Complete Skill extraction and small experiment

New extraction directly authors native Skill files:

```text
Issue / PR / commit evidence -> model-authored Skill Package
  -> verbatim persistence + package validation
  -> derived Episode / Action / Workflow graph -> SQLite / retrieval
  -> verified SKILL.md + referenced procedure -> applicability judge
```

The default Codex and HTTP runners request a text file bundle. They do not
request `candidate_atomics` / `candidate_workflows` JSON or render instructions
from an intermediate representation. `direct_skill_extraction.py` splits file
boundaries, rejects incomplete/unsafe bundles and conflicting packages, and
adds deterministic hashes plus a standalone integrity verifier. Authored
Markdown remains unchanged. An explicit defer response preserves uncertainty.

The canonical root is `data/skill-extraction/packages/`; Workflow candidates
use `candidates/workflows/`. Each package contains `SKILL.md`, historical
`references/episode.md`, Workflow and Action/evidence cards, provenance, and
activation/applicability/functional eval definitions. Eval definitions remain
`not_executed`; package validity does not prove repair or transfer success.

The [direct output protocol](data/skill-extraction/packages/universal-resolution-distiller/references/direct-skill-output-protocol.md)
defines required contents and safe file boundaries. A new training run can use:

```bash
python experiments/run_codex_issue_episode_extraction.py \
  --manifest experiments/manifests/agent-core-seven-category-extraction-v2/01-provider-interface-adaptation.json \
  --role train_candidate --max-cases 1 --local-git-only \
  --output data/skill-extraction/my-direct-run
```

Use `--codex` to select the configured executable when it is outside PATH.
Credentials are supplied at runtime, never written to artifacts. Source checkouts
are inspected with the default read-only sandbox. Keep a new output directory
for every model run to preserve history.

Catalog rebuilding re-reads and validates existing package files instead of
compiling them. Summaries and inventories audit exact agreement between authored
bundles and published contents. Guided retrieval requires verified packages,
rechecks hashes/source identity and hydrates the actual Markdown and references.
JSON-only, stale, tampered, deferred or rejected records cannot supply guidance.

Historical IR migration remains explicit: `materialize_candidate_skills.py`,
extractor `--legacy-json`, and catalog `--migrate-legacy-json`. The catalog's
`--allow-structured-ir` and inventory's `--structured-ir-only` are audit modes.
These paths do not define new direct extraction. See
[the direct extraction pilot](analysis/direct-skill-extraction-pilot-20261003.md)
and [the research survey](analysis/agent-software-repair-benchmark-survey-20261003.md).

Replay the frozen real direct extraction without model calls or credentials:

```bash
PYTHONPATH=src python3 experiments/run_direct_skill_smoke.py --output /tmp/arex-direct-replay
```

This checks 19 authored files unchanged, a standalone copied package, graph and
SQLite admission, exact/HNSW retrieval, and actual context hydration. Its one
package has four Actions and eight evidence cards. Functional evals and holdout
repair remain unexecuted; this is delivery/retrieval verification.

Replay the historical JSON-migration two-Workflow smoke experiment with no credentials or model
calls:

```bash
PYTHONPATH=src python3 experiments/run_skill_package_smoke.py
```

It reconstructs an isolated SQLite catalog, retrieves and hydrates the package,
checks standalone verification, and runs the same synthetic constructor oracle
against the broken and current-session Skill-guided repair: **5/14 -> 14/14**.
It audits all 20 holdout URL/ID records without using their solutions. This is a
package execution smoke test, not an independent agent benchmark. Both packages
remain candidates; no Pattern or Skill was promoted. The original 83-Workflow
corpus and legacy Pattern packages have not been batch-migrated.

See `analysis/workflow-records-to-skill-packages-20261003.md` and
`data/skill-extraction/package-materialization-pilot-v1/pilot-report.json` for
the measured result, source-to-package mappings and limitations.

Evidence-grounded episode material, manifests, reviewed samples, profiles, and
validation outputs live under data/skill-extraction/, data/review-samples/,
data/manifests/, and data/profiles/. Generated caches, local virtual
environments, temporary inspection files, and local SQLite catalogs are kept
out of version control by .gitignore; portable JSON/HNSW artifacts remain
available for retrieval experiments.

## Reproducibility

From the repository root:

    python3 -m venv .venv
    .venv/bin/pip install -e '.[dev]'
    PYTHONPATH=src .venv/bin/python -m pytest -q

No API keys or provider credentials are required for the deterministic tests and
local retrieval pilots. External LLM extraction is configured at run time and
credentials must be supplied through environment variables rather than
committed to this repository.


## Native v4 adaptive guidance

The v4 path adds semantic Action ports, evidence-qualified Pattern contracts,
current TaskContext bindings/oracles, constrained Workflow rewriting and CrossBind,
and abstaining Workflow/Plan rankers. Native SKILL.md and supporting authored files
are the authority; current plans remain temporary, and historical packages are
immutable. Legacy routing remains available alongside this optional path.

Read [the implementation and requirement audit](analysis/pattern-crossbind-ranker-implementation-20261003.md)
for CLI examples, schema boundaries and outstanding formal experiment work.
A [portable synthetic package](tests/fixtures/adaptive-v4/type-context-pattern/SKILL.md)
and [measured smoke report](analysis/results/adaptive-contract-synthetic-smoke-20261003.json)
make the implementation reviewable.

```bash
python -m pip install -e '.[dev,ranker]'
python -m pytest -q
python experiments/run_adaptive_contract_smoke.py --output-dir /tmp/arex-adaptive-smoke-new
```

This runs actual local Transformer-head training and an isolated tool/evaluator
loop with synthetic authored/ranking/solver replay. It uses the default 6,000-token
history cap; it makes zero live LLM calls and runs zero formal SWE instances.
The current full-suite result is 198 passing tests. Cross-project repair gains
require the complete temporal corpus, real supervised development and frozen SWE
cohort described in the audit; these have not been executed.
