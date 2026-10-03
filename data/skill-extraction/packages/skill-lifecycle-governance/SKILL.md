---
name: skill-lifecycle-governance
description: Govern the admission, deduplication, merging, revision, failure diagnosis, quarantine, and retirement of Atomic, Workflow, and Pattern skills. Use when a new extracted skill is about to enter the canonical tree or when runtime feedback indicates that an existing skill may be stale, redundant, misapplied, or incorrect.
---

# Skill lifecycle governance

Atomic, Workflow and Pattern graph nodes are candidate knowledge records until
a grounded Workflow/accepted Pattern has a validated Agent Skill Package.
Require package materialization before candidate Skill admission. Preserve
package path, version, content hash, source ids and validation with the graph
record. After a semantic revision, compile and validate a new package version
before serving it; a stale package reference cannot represent revised guidance.
Keep deferred, rejected, quarantined and retired records out of serving
hydration. Package generation does not promote a candidate.

This is an LLM-facing semantic governance skill. It does not replace structural
storage checks. It decides semantic questions that must not be hard-coded:

- whether two same-level skills solve the same problem by the same mechanism;
- whether they are mergeable, a specialization, a generalization, related but
  distinct, or conflicting;
- whether a failure is caused by retrieval, applicability, composition, the
  skill method, or a stale environment;
- what revised skill should be proposed from new code and failure evidence.

## Mandatory operating order

Always process the hierarchy bottom-up:

```text
Atomic change
  -> retrieve same-level Atomic peers
  -> LLM dedup/adjudication
  -> update or create Workflow candidates
  -> retrieve same-level Workflow peers
  -> LLM dedup/adjudication
  -> update or create Pattern candidates
  -> retrieve same-level Pattern peers
  -> LLM dedup/adjudication
```

Do not compare an Atomic directly with a Workflow or a Pattern. Do not create a
Pattern solely because two strings or embeddings are similar.

## Candidate retrieval is not semantic judgment

Before this skill is called, the system may use:

- FTS5/BM25 lexical retrieval;
- exact embedding cosine retrieval;
- HNSW approximate nearest-neighbor retrieval;
- reciprocal-rank fusion of these channels.

These channels only produce a small same-level candidate set. They must not
label a pair as duplicate or mergeable.

## Deduplication output

Return strict JSON with:

```json
{
  "decision": "exact_duplicate|mergeable|specialization|generalization|related_but_distinct|conflicting|no_match",
  "confidence": 0.0,
  "rationale": "mechanism-level comparison grounded in evidence",
  "evidence_ids": [],
  "merged_payload": {}
}
```

Compare, in order:

1. problem signature and observed failure mechanism;
2. solution principle and state/data-flow transformation;
3. preconditions, exclusions, and failure modes;
4. expected outputs and validation oracles;
5. repository/environment boundary;
6. evidence quality and independence.

Do not merge merely because titles, files, APIs, or keywords overlap.

## Merge rules

- `exact_duplicate`: keep one canonical node, preserve the incoming node as an
  alias and attach its evidence.
- `mergeable`: propose a new version; never overwrite either historical node.
- `specialization` or `generalization`: retain both and record the typed relation.
- `related_but_distinct`: retain both; explain the causal distinction.
- `conflicting`: retain both with explicit applicability boundaries until new
  evidence resolves the conflict.
- `no_match`: create a new sibling.

## Failure diagnosis output

For a failed use, first classify the incident as one of:

`retrieval_failure`, `applicability_failure`, `precondition_failure`,
`composition_failure`, `skill_logic_failure`, `stale_skill`,
`execution_failure`, or `validation_failure`.

Use independent tasks and code evidence. A single failure is an investigation
signal, not proof that a skill is wrong. Repeated independent
`skill_logic_failure` or `stale_skill` incidents justify a quarantine proposal.

## Revision protocol

A correction must produce a new version with:

- the old version kept for audit and reproducibility;
- the exact failure evidence and root-cause hypothesis;
- changed preconditions, procedure, or invariants;
- replay/regression cases;
- an explicit canary or review status.

Never silently edit an active historical version and never physically delete a
retired node.

## Boundary of responsibility

The runtime may enforce only non-semantic invariants such as JSON shape,
referential integrity, level scoping, version monotonicity, and event ordering.
All meaning, equivalence, applicability, root-cause, and correction judgments
must be made through this skill by the LLM and recorded with rationale and
provenance.
