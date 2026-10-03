---
name: constant-identity-comparison
description: "Repair Python AST identity-comparison diagnostics that miss recursively constant tuples while preserving singleton exemptions and nonconstant-tuple behavior."
---

# Constant identity-comparison diagnostics

Use this workflow when a Python AST-based analyzer already diagnoses `is` or `is not` against literals but misses an empty tuple or a tuple whose elements are recursively constant.

This is a conditional repair workflow, not a recommendation to replace all identity comparisons with equality. Its historical support is one verified repair. It does not establish cross-project transfer.

## Activation and exclusions

Activate when public code or a reproduction indicates that an identity-comparison diagnostic omits constant tuples, and the current analyzer has an identifiable AST comparison visitor and literal diagnostic.

Clarify or probe first when the AST representation, supported Python versions, diagnostic owner, or existing behavior is unknown.

Do not activate for:
- Runtime identity semantics, compiler changes, or automatic equality rewrites.
- A request to flag `None`, booleans, or Ellipsis merely because they are singletons.
- A request to classify every tuple expression, including tuples containing variables, as a constant.
- A non-Python AST implementation without a separately supported realization.

## Current probes and binding

Locate the current semantic owners rather than assuming historical file paths:
- `comparison-classifier`: identity-comparison traversal and literal classification.
- `literal-diagnostic`: message emitted for inappropriate identity comparison.
- `comparison-regressions`: public tests of this diagnostic.

Inspect the actual AST representation on the supported runtimes. Establish whether literals use `ast.Constant`, older dedicated node types, or a supported compatibility branch. Inspect chained comparisons and whether each adjacent operand pair is checked.

Follow [inspect owners](references/actions/inspect.md), then [repair classifier and regressions](references/actions/repair.md), and finally [validate public behavior](references/actions/validate.md). The canonical historical ordering and dependency evidence are in [the workflow](references/workflow.md).

## Repair boundary

The supported mechanism separates:
1. Singleton recognition.
2. Recursive constant recognition, including tuples.
3. Non-singleton constant recognition.
4. Identity-operator checks against either operand of each adjacent comparison pair.

An empty tuple is constant because every element of its empty element list satisfies the constant predicate. A tuple containing only constants, including nested tuples and singleton elements, is constant as a whole; the tuple itself is not a singleton. A tuple containing a variable is not constant under this mechanism.

Preserve singleton exemptions, existing ordinary-literal diagnostics, non-identity comparison behavior, and the nonconstant-tuple exclusion.

## Validation and stop conditions

Bind each Action oracle to current public commands before execution. Record PASS, FAIL, or UNKNOWN for prerequisites and oracle observations. UNKNOWN prerequisites authorize inspection only; failed applicability checks reject this repair plan.

After editing, run the targeted regression tests and adjacent behavior checks. Refresh the validation observation invalidated by editing. A structurally compatible plan does not prove a successful repair.

Stop and reconsider if:
- Current AST representations differ from the supported mechanism.
- Existing singleton handling cannot be confirmed.
- Tuples with variable elements become newly diagnosed.
- Existing literal or chained-comparison diagnostics regress.
- The current diagnostic has materially different semantics.

A current TaskContext should record the public issue, pinned base, hashed code anchors, owner bindings, observed facts, semantic checks, observed PortValues, and current oracle bindings. Map each oracle using `action_id` and `source_oracle_id`, with semantic check key `oracle:<action_id>:<source_oracle_id>`. Render and execute only bound public current commands; historical commands are evidence, not execution authorization.

## Evidence and limits

[The episode](references/episode.md) distinguishes the original report, merged implementation, historical regression assertions, and later qualification. [Provenance](references/provenance.json) records the source and qualification limits.

The historical commit supplied regression assertions, not a historical test-run transcript. A later qualification reported two fail-to-pass and 28 pass-to-pass cases within changed test files only. Whole-project regression and cross-project transfer remain untested. The packaged [evaluation definitions](evals/functional-cases.json) are not executed.

During formal evaluation, keep this knowledge and checkpoints frozen. Do not publish a current task plan as newly verified historical knowledge. Time-reconstructed catalogs must exclude the query's own issue, fix, cluster, aliases, copied sources, and sources not available before the query input time. Independent hidden acceptance is obtained after the solver stops, not used to construct guidance.
