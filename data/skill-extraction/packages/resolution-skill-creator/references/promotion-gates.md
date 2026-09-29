# Resolution Skill promotion gates

A package may be emitted at three statuses:

- `candidate`: structurally valid but not yet semantically or empirically
  promoted;
- `deferred`: missing evidence, action references, oracle, or judge result;
- `promoted`: all gates below pass and the version is published.

## Required gates

### Evidence

- The source Episode has before/after implementation evidence.
- Every Action cites evidence ids and a validation oracle.
- No target holdout solution, descendant commit, or target-only node is loaded.

### Workflow / Pattern semantics

- Every Workflow step resolves to a real Action id.
- `when_to_use`, `anti_goals`, exclusions, and stop conditions are non-empty.
- Pattern promotion requires independent supporting Workflows from at least two
  repositories or an explicitly recorded exception.
- Optional branches and counterexamples are explicit; they are not inferred
  from similarity alone.

### Evaluation

- Activation evals include direct, indirect, contextual, incomplete, negative,
  and edge prompts.
- Functional evals check focused tests, mandatory Action coverage, anti-goal
  violations, unrelated edits, and leakage.
- A Pattern is not promoted from retrieval Recall alone. It needs a successful
  leakage-audited holdout or an explicit `deferred` decision.

### Package quality

- Frontmatter, naming, references, and scripts validate.
- No unfinished placeholders remain.
- The entrypoint is concise and detailed material is progressively disclosed.
- Version, source graph ids, evidence ids, model/prompt version, and eval
  results are recorded.

## Decision output

```json
{
  "status": "candidate|deferred|promoted",
  "skill_id": "...",
  "version": 1,
  "reasons": [],
  "missing_evidence": [],
  "supporting_workflows": [],
  "supporting_repositories": [],
  "holdout": {"status": "pass|fail|unavailable", "run_ids": []}
}
```
