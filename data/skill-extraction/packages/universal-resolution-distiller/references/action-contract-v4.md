# Native adaptive Skill files, v4

Use this protocol only when the caller selects v4. Preserve the v3 direct-file
protocol and existing packages unchanged. The output is authored Markdown files
in `AREX-SKILL-BUNDLE 1`, not candidate JSON. Use the existing FILE/end delimiters;
return `AREX-SKILL-DEFERRED 1` when evidence is insufficient.

The exact transport markers are `AREX-SKILL-BUNDLE 1`,
`<<<FILE skill-name/SKILL.md>>>`, `<<<END FILE>>>`, and
the terminal line `AREX-SKILL-BUNDLE-END`. The FILE marker has three closing
angle brackets after the complete path. Do not add text between FILE blocks.
For a defer response, write the reason after `AREX-SKILL-DEFERRED 1` and finish
with `AREX-SKILL-DEFERRED-END`.

## Package and authority

Every `<name>/` contains SKILL.md, references/episode.md, references/workflow.md,
references/actions/*.md, references/evidence/*.md, references/provenance.json,
evals/activation-cases.json, evals/applicability-cases.json,
evals/functional-cases.json. Pattern/local-template packages also contain
references/realizations/*.md for additional historical Workflows. All links are
relative and contained; include every supporting resource. The host adds
manifest.json and scripts/verify_package.py, which verifies copied file integrity.
An optional deterministic script is a functional oracle only after actual execution.

SKILL.md begins with `---`, `name: <directory-name>`, and a JSON quoted
`description:` on one line. Write readable activation conditions, exclusions,
current probes, linked operations, validation, failure/stop conditions and limits.
Keep historical paths in references; specify semantic owners in reusable Actions.

provenance.json contains `schema_version: arex-native-provenance-v4`,
`split: train_candidate`, `holdout_used: false`, `package_kind`
(`workflow`, `pattern`, or `local_template`), authoritative `cutoff`, `package`
(`skill_id`, `name`, `version: 1`, `level: <package_kind>`, `status: candidate`),
`sources`, `source_episode_ids`, and `source_workflow_ids`. A workflow package has
one canonical Workflow whose ID equals the package ID. A Pattern ID equals the
package ID; its historical Workflow IDs remain separate. Never claim a task plan
is newly verified historical knowledge or publish it during formal evaluation.

Copy each authoritative SourceRecord exactly: id, repository, bug_cluster_id,
fix_id, revision (40-character SHA), available_at (timezone required),
evidence_refs, aliases, copied_from, verified_resolution. Every source must be
available strictly before cutoff and have independent verified resolution evidence.
Copies, aliases, mirrors and the same fix do not increase independent support.
`source_episode_ids` is exactly the set of packaged SourceRecord `id` values.
These IDs may identify a particular repair of an issue. Do not substitute issue
IDs, bug_cluster_id, or aliases. Action and Workflow `source_ids`, and evidence
`source_id`, use the same authoritative SourceRecord IDs.

## Action ports and state

Each readable Action card contains exactly one fenced `arex-contract-v4` JSON
block. Required fields: id, intent, mechanism, semantic_role, owner_role,
operation, inputs, outputs, preconditions, effects, preserves, oracle,
source_ids, evidence_refs, resource, package_id. `package_hash` is empty or omitted:
the host derives it. Optional fields: kind (probe/read/edit/validate/bridge/cleanup),
read_set, write_set, invalidates, exclusions, validation_for, cleanup_for, estimated_cost.
A `cleanup_for` operation remains in the cut/verification closure after its
associated operation; current semantic dependencies determine whether validation
occurs before or after cleanup. Cleanup that changes state also retains a public
validation Action.

`inputs`, `outputs`, `preconditions`, `effects`, `preserves`, `oracle`,
`source_ids`, and `evidence_refs` are **required JSON arrays**, including when
there is one item. Use `[]` for an allowed empty array. `preconditions`, `effects`,
`preserves`, and `exclusions` contain Predicate **objects**, not predicate strings.
`oracle` contains Oracle **objects**, not oracle ID strings or a single object.
Oracle IDs are local labels; the Oracle's complete object is embedded in its
Action contract. `validation_for` is an array of modifying Action ID strings.
For example, the following shapes demonstrate syntax only; replace their
identities and content with actual supplied evidence:

```json
{
  "preconditions": [{"key": "owner-located", "value": true}],
  "effects": [{"key": "target-behavior", "value": "corrected"}],
  "preserves": [{"key": "adjacent-behavior", "value": "preserved"}],
  "oracle": [{
    "id": "verify-target-behavior",
    "instruction": "Verify the public reproduction and adjacent behavior.",
    "evidence_refs": ["actual-evidence-id"],
    "kind": "public_probe",
    "command": []
  }]
}
```

A Port has name, semantic_role, artifact_kind, language, scope, phase, state,
and optional (boolean, default false). Producer and consumer must agree on all
six semantic dimensions; similar words/types do not establish semantic compatibility.
Concrete Rust objects cannot bind to Python interfaces. Author a separately
supported Python realization or a genuinely agnostic operation, then bind it to
current code. A Bridge is a sourced Action with its own inputs, outputs,
preconditions, preserved behavior and oracle, not an invented adapter.

Inputs may be empty for a source-independent read/probe. An Action must declare
observable outputs or effects. Distinguish expected outputs/effects from observed
execution results. A Predicate has key, value (string or boolean), evaluator
(evidence/file_exists/symbol_exists), and optional description. Descriptions
explain a predicate; its semantic identity is key/value/evaluator. Use
`role:<owner_role>` for file_exists/symbol_exists when the concrete object must
be located in the current checkout; literal file paths denote current public
paths and are never silently reused as historical bindings. Natural-language
semantic claims require current evidence-backed review/probes; they are not proven
by matching Predicate names. `preserves` specifies behavior that must survive;
`invalidates` names facts that must be re-observed after this Action.
Use distinct keys for an observation becoming stale and for behavior that must
remain preserved. An `invalidates` key cannot also appear in `preserves` or a
Workflow invariant: invalidating a required assurance prevents unconditional
execution. For example, `public-validation-observed` may become stale after an
edit while `ordinary-runtime-behavior-preserved` remains a required behavior.
Every `preserves` declaration is retained by a composed plan. Describe a read
operation's lack of side effects in its operation/oracle; a Workflow that edits
code cannot promise `checkout-unchanged` across the whole plan.

Read/write sets name roles or explicit resources. Current bindings resolve aliases
before conflict checks. Every modifying Action retains explicit `validate`
Actions whose `validation_for` lists its ID. Each oracle has id, instruction,
evidence_refs, kind (public_probe/public_mre/repository_test), and optional
command (argv array). Historical commands need adaptation to the current public
checkout; target hidden tests or gold-derived commands never enter guidance.

## Historical Workflow and Pattern

references/workflow.md contains exactly one complete `arex-workflow-v4` JSON
block for the primary historical realization, including in Pattern/local-template
packages. An index or links to realizations alone is insufficient. Additional
realizations each contain one complete block in references/realizations/*.md.
Author the complete bundle or defer; the host never fills in missing contracts.

Each block contains:
id, goal, mechanism, action_ids, source_ids, required_effects, invariants,
dependencies, and optional `optional_action_ids` for evidenced conditional branches.
A dependency has before, after, reason, evidence_refs. Do not embed
or duplicate Action objects. Historical realizations cover every packaged Action;
current task DAGs may drop already satisfied/inapplicable operations. Current
ordering follows ports, prerequisites, semantic dependency evidence and verification,
not historical list position. Historical source/validation details remain immutable.

A Pattern/local-template SKILL contains one `arex-pattern-v4` block with id,
mechanism, roles, required_effects, invariants, applicability, exclusions,
partial_order, supporting_workflow_ids, evidence_refs, cross_project.
Each role has id, effects, alternatives (Action IDs), evidence_refs, required.
Alternatives must implement the declared role/effects. Dependencies connect role
IDs. At least two independent bug clusters and fixes support a template;
a cross-project Pattern additionally requires two repositories. All support,
roles and claimed boundaries must follow actual historical evidence. Defer rather
than force a Pattern from a preset issue family. Preserve upstream source package
hashes/resource locators in provenance when abstracting existing native packages.
Copy `authoritative_upstream_packages` exactly into `source_package_hashes`.
Copy the supplied `authoritative_generation_context` exactly into
`generation_context` in provenance. This records every source/package read in
corpus discovery and inherited abstractions, including sources not selected as
mechanism support. It has schema `arex-generation-context-v1`,
source_corpus_sha256, source_package_hashes, and authoritative SourceRecord
sources. These dependencies do not count as additional independent support.
All generation-context sources must precede the task/query cutoff and avoid its
issue/fix/cluster/alias identities. A later discovery input can invalidate an
earlier-time training candidate even if it is absent from the final support set.
Do not drop, retime or rewrite context records to make a Pattern eligible.
Namespace new Action and realization IDs by the new package ID to avoid catalog
collisions; retain original IDs and resource hashes in historical provenance.

Evidence cards contain one `arex-evidence-v4` block with exactly id, source_id,
available_at, kind, observation. Record actual resolution and tests, including
unexecuted/unknown status; all referenced evidence must be packaged.

## Evaluation and use

Eval suites contain `status: not_executed` and nonempty `cases`. Activation covers
activate/clarify/do_not_activate; applicability covers
applicable/insufficient/not_applicable. Functional cases cover every Action and
include id, action_id, setup and observable checks. Definitions do not claim success.

A current TaskContext contains public issue, pinned base, hashed code anchors,
observed facts, semantic checks, real bindings, observed PortValues, and current
Oracle bindings. Each current Oracle maps action_id/source_oracle_id to public
current instruction, argv command and evidence_refs; its semantic check key is
`oracle:<action_id>:<source_oracle_id>`. Render these bound commands; old commands
remain historical evidence and do not authorize execution. Tri-state
checks are PASS/FAIL/UNKNOWN. Unknown prerequisites authorize probes only; hard
failures reject a plan. Plan structural PASS predicts compatibility, never repair
success. Execute public checks, refresh stale observations, and obtain independent
hidden acceptance after the solver stops. Formal knowledge and checkpoints stay
frozen; time-reconstructed training catalogs exclude own issue, fix, cluster,
aliases, copied sources and every source not available before the query input time.
