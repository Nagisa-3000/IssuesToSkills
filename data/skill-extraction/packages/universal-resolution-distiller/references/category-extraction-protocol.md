# Cross-project category extraction protocol

Use this protocol when building a category corpus for later Pattern induction
and holdout evaluation. It governs only Issue/PR evidence collection,
direct Skill authoring, Action/evidence cards, Workflow references and package
validation. Pattern
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

Each admitted response is a complete text file bundle using
[the direct output protocol](direct-skill-output-protocol.md). It contains
model-authored SKILL.md, historical Episode Markdown, linked Action/evidence
cards, Workflow dependencies/oracles, authoritative provenance and all three
eval suites. No semantic candidate JSON is needed before authoring.

Every Action/evidence/dependency link resolves inside its package. The publisher
persists file contents unchanged and validates the whole response before
publishing packages. Only then are Episode/Action/Workflow JSON index records
derived. Missing evidence produces the explicit deferred envelope.

## 6. Aggregate without semantic over-merging

Validate each directly authored package through the Resolution Skill Creator
before admitting it. Record package path, version, hash, validation, source
Episode/Workflow ids and publisher/contract version. Historical JSON-only
cases remain structured IR and do not count as completed Skill extraction.

The inventory reports category, repository, sample kind, model, usage,
evidence/Action/Workflow counts, actual validated package counts and output
contract. Verify distinct training repositories, an untouched disjoint
holdout, exact agreement between authored response and published files,
package validation, and zero holdout URL/id occurrences in prompts, bundles,
responses, package references and inventories. The inventory validator
supports both direct file bundles and explicit historical JSON audits.

Do not merge same-named Actions across projects here. Similar verbs are not
proof of a shared state contract or validation oracle.

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
