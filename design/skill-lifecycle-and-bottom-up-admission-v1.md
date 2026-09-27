# Skill lifecycle, cost-controlled deduplication, and bottom-up admission v1

Date: 2026-09-27

## Decision

The visible knowledge organization remains a tree:

```text
Pattern
└── Workflow
    └── Atomic
```

The tree is a projection of a versioned lifecycle registry. It is not a flat
append-only list and it is not the complete provenance graph.

Semantic lifecycle decisions are made by the LLM-facing
`skill-lifecycle-governance` Skill. The runtime only performs candidate
retrieval, persistence, structural scoping, version bookkeeping, and event
recording. It must not turn a lexical/vector score into a semantic duplicate
judgment.

## Admission pipeline

```text
new Atomic
  │
  ├─ BM25/FTS5 same-level candidates
  ├─ exact embedding candidates
  ├─ optional HNSW same-level candidates
  └─ reciprocal-rank fusion
          │
          ▼
  LLM: exact duplicate / mergeable / specialization /
       generalization / related / conflict / no-match
          │
          ▼
  accept alias, create version, or keep sibling
          │
          ▼
  LLM extracts/revises Workflow candidates from the Atomic result
          │
          ▼
  same Workflow retrieval + LLM adjudication
          │
          ▼
  LLM extracts/revises Pattern candidates from new Workflows
          │
          ▼
  same Pattern retrieval + LLM adjudication
```

Only the same level is searched for deduplication. The level restriction is a
routing constraint, not a semantic conclusion. HNSW is an optional acceleration
layer; exact vectors remain the fallback.

## Why the order is bottom-up

A Workflow is an arrangement of Atomic mechanisms. A Pattern is an abstraction
of compatible Workflows. Therefore an upper-level comparison made before the
lower-level update would compare stale children and can create a false Pattern
match. Every Atomic insertion/update returns the Workflow parents that need
re-extraction or revalidation; every Workflow update does the same for Pattern
parents.

When there is no new or changed Workflow candidate, no Pattern LLM call is
made. This is the principal token-saving gate in the admission path.

## LLM decision contract

The dedup judge receives the candidate and a small retrieved peer set. It must
return structured JSON with `decision`, `confidence`, `rationale`, evidence IDs,
and an optional merged payload. The accepted decisions are:

- `exact_duplicate`: canonicalize and preserve an alias;
- `mergeable`: create a new version containing both evidence sets;
- `specialization` / `generalization`: keep both nodes and add a typed relation;
- `related_but_distinct`: keep both siblings;
- `conflicting`: preserve both with explicit boundaries;
- 
o_match`: insert a new sibling.

The LLM must compare problem mechanism, state/data flow, preconditions,
exclusions, outputs, failure modes, validation oracles, and environment scope.
Titles, paths, commit messages, and embeddings are only navigation evidence.

## Runtime feedback

Every use records the selected skill ID and version, task, result, validation
outcome, and optional token cost. Failures are classified by the LLM as
retrieval, applicability, precondition, composition, skill logic, stale skill,
execution, or validation failures.

Only independent `skill_logic_failure` and `stale_skill` contexts count toward
an LLM review trigger. The default thresholds only decide when to spend an LLM
investigation call; they never mark a Skill wrong or quarantine it. The governance
Skill must inspect the incidents and explicitly return a lifecycle decision. This
prevents a single noisy task from deleting a Skill while keeping review cost bounded.

A correction always creates a new version. The old version becomes
`superseded` only after the new version is accepted. Quarantine, deprecation,
and retirement are soft lifecycle states; no historical node is physically
deleted.

## Implemented reference API

- `arex_skill_graph.lifecycle.SkillRecord`: versioned node and usage stats.
- `LifecycleManager`: typed dedup proposals, aliases, merge revisions, usage
  events, failure incidents, quarantine, revision activation, and soft
  retirement.
- `arex_skill_graph.admission.SkillCandidateRetriever`: BM25 + exact vector or
  HNSW candidate retrieval with same-level filtering and RRF.
- `BottomUpSkillAdmission`: Atomic -> Workflow -> Pattern orchestration with
  injected LLM judge and LLM-backed extractors.
- `data/skill-extraction/packages/skill-lifecycle-governance/SKILL.md`: the
  semantic governance contract supplied to the LLM.

## Relationship to validation code

Structural checks remain necessary for storage safety: valid JSON, references,
level scoping, version/event shape, and no corrupted tree edges. They are not
semantic skill judgments. Equivalence, applicability, causal correctness,
root-cause analysis, and revision content are delegated to the governance
Skill and recorded as proposals/incidents.

## Current limitations

- The LLM provider is deliberately injected as a callback; no online model is
  called by the offline test suite.
- Lifecycle events are currently held by `LifecycleManager`; the next storage
  step is to persist them in SQLite alongside the catalog.
- HNSW is already supported by the catalog's vector backend, but a full index
  build is still an operational step rather than automatic admission behavior.
- The existing extracted residual-budget family remains provisional; no claim of
  held-out transfer validation or token savings is made yet.


