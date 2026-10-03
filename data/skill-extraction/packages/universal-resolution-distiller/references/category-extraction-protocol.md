# Cross-project category extraction protocol

Use this protocol when building a category corpus for later Pattern induction
and holdout evaluation. It governs only Issue/PR evidence collection,
ChangeEpisode extraction, candidate Actions, Issue Workflows, and mandatory
Workflow Skill Package compilation. Pattern
promotion, retrieval evaluation, and skill-guided patching are later stages.

## 1. Define the category before selecting cases

Write a plain-language invariant, observable inclusion criteria, and explicit
exclusions. A category should describe one transferable failure boundary, not a
repository area or a broad collection of related keywords.

Reject a candidate when its implementation solves a different invariant even
if its title shares category keywords. Record rejected candidates instead of
silently replacing them.

## 2. Establish an eligible evidence pool

Prefer an Issue linked to a merged implementation PR or a directly auditable
implementation PR. Each training candidate must have:

- a pinned implementation commit and parent/base commit;
- implementation-bearing changed files;
- a before/after behavior that can be established from the diff and call sites;
- a focused test or another concrete validation oracle;
- enough local checkout evidence to inspect the implementation without relying
  on the Issue title or model memory.

When an original seed has no implementation-bearing resolution, a same-project
same-category substitute is allowed only if its provenance is explicit. Keep
`seed_issue`, `seed_relation`, and `sample_kind`; never report it as the exact
seed.

## 3. Freeze the split before extraction

Use at least five eligible repositories when the experiment calls for four
training cases and one holdout. Select or preregister one repository-disjoint
holdout before extraction and record the selection method. If selection is
random, record the seed and eligible pool. If it is deterministic, record the
rule and rationale instead of calling it random.

The holdout record must have:

```yaml
role: holdout_candidate
split: holdout_candidate
evidence_status: intentionally_not_extracted
extraction_forbidden: true
```

Do not fetch or place the holdout solution ref, hidden tests, comments that
reveal the fix, or prior solution transcript in any training prompt, evidence
bundle, response, summary, or Pattern input. Public Issue text needed for the
later agent task should be captured only after the training corpus is frozen.

## 4. Run training extraction in isolated parallel processes

Parallelize independent training cases, not semantic decisions:

- use one read-only extraction process and one output directory per case;
- pin the checkout/ref in the manifest rather than sharing mutable branches;
- bound concurrency to the model endpoint and local I/O capacity;
- never share response files, scratch prompts, or mutable worktrees;
- exclude the holdout manifest from every extraction command;
- collect model, prompt/contract version, tokens, latency, exit status, and
  validation result per case.

Retries must reuse the same evidence boundary and case identity. Preserve failed
attempt logs; do not replace an evidence failure with an unsupported answer.

## 5. Admit only grounded outputs

Each admitted response must contain:

- one canonical ChangeEpisode with evidence-backed before, after, and diff;
- evidence units with stable ids and source locators;
- independently testable semantic Actions with pre-state, post-state, and
  validation oracle;
- at least one Issue Workflow with `when_to_use`, `anti_goals`,
  `not_applicable_when`, real Action step references, conditions/dependencies,
  validation ladder, and stop conditions;
- unresolved questions that preserve uncertainty rather than filling gaps.

Every Action and Workflow evidence reference must resolve inside the response.
Every Workflow step, dependency, and edge must resolve to an Action extracted
from the same episode. A later graph materializer may assign global ids, but it
must not invent missing Actions.

## 6. Aggregate without semantic over-merging

Compile and validate each grounded Workflow through the Resolution Skill
Creator before reporting it as an admitted candidate Skill. Record
`package_path`, version, SHA-256, package validation, source Episode/Workflow
ids, and compiler version. JSON-only cases are `materialization_pending` and
must not count as completed Skill extraction. Report Action/Workflow IR counts
separately from materialized package counts.

The extraction inventory should report category, case, repository, sample kind,
model, usage, evidence count, Action count, Workflow count, validation status,
and relative artifact path. At category level, verify:

- the requested number of admitted training episodes;
- one distinct repository per training case;
- a holdout repository absent from the training set;
- schema and manual validation for every response;
- zero holdout URL/id occurrences in case prompts, evidence bundles, responses,
  and validation artifacts.

Do not merge same-named Actions across projects at this stage. Similar verbs are
not proof of a shared state contract or validation oracle.

## 7. Validate and freeze the extraction corpus

Run the deterministic inventory validator from the repository root:

```bash
python data/skill-extraction/packages/universal-resolution-distiller/scripts/validate_extraction_inventory.py \
  data/skill-extraction/<run>/extraction-inventory.json \
  --expected-categories 20 \
  --expected-training-per-category 4 \
  --expected-model openai/gpt-5.6-sol \
  --output data/skill-extraction/<run>/extraction-validation.json
```

Commit the manifests, prompts, evidence bundles, responses, validation records,
inventories, and validator result before inspecting holdout solutions. The Git
commit is the immutable training freeze. Holdout feedback must create a new
version rather than modifying the frozen extraction artifacts in place.

## Completion gate

The Skill extraction stage is complete only when all requested training cases
have validated Workflow packages, the repository-disjoint split is proven,
holdout leakage is zero, and the package-aware inventory validator succeeds.
Use `--structured-ir-only` only to audit frozen historical IR. Such a result
does not mark Skill extraction complete. This gate does not claim that
a Pattern generalizes or that a guided agent outperforms a no-skill agent.
