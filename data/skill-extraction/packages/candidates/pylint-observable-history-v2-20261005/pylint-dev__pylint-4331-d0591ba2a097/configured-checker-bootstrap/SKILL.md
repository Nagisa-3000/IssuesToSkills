---
name: configured-checker-bootstrap
description: "Repair a Python functional-test harness that parses optional-checker configuration but omits registration before applying options; verify explicit diagnostics and preserve adjacent harness behavior."
---

# Configured checker bootstrap

## Activation

Use this Workflow when a Python functional-test harness reads per-fixture configuration requesting an optional checker, yet the checker's expected enabled diagnostics are absent. First confirm that the requested module is importable and that registration is missing between configuration parsing and option application.

Repository identity and a missing diagnostic alone are not activation conditions. Exclude unavailable modules, misspelled configuration, disabled messages, incompatible interfaces, and checker recognition defects.

## Current probes and operations

1. [Inspect the bootstrap](references/actions/inspect.md): locate current semantic owners, confirm importability and diagnostic enablement, and record the actual parse/register/apply lifecycle.
2. [Repair registration](references/actions/register.md): register only explicitly requested modules after parsing and before applying options.
3. [Strengthen fixtures](references/actions/fixtures.md): add independently justified diagnostic expectations and correct exposed false negatives.
4. [Validate](references/actions/validate.md): check both modifications and adjacent ordinary behavior.

The [Workflow contract](references/workflow.md) supplies semantic dependencies. Registration and fixture authoring need not be ordered relative to each other; both precede validation. Already satisfied operations may be omitted from a current DAG, using observed matching PortValues, but every retained modification retains its validation Action.

Preserve ordinary checker initialization, reporter setup, suppression settings, and missing-configuration handling. Do not load every optional checker, suppress newly exposed valid messages, weaken expectations, or bypass comparison.

## Current execution boundary

Create a TaskContext with the public issue, pinned base, hashed code anchors, observed facts, semantic checks, real owner bindings, observed PortValues, and current Oracle bindings. Resolve owner aliases before read/write conflict checks. Historical paths are evidence, not automatic current bindings.

Checks are PASS, FAIL, or UNKNOWN. UNKNOWN prerequisites authorize probes only; hard failures reject the proposed edit. Matching predicate names do not establish behavior: obtain current evidence. Bind every Oracle's action ID and local Oracle ID to current public instructions, argv, and evidence references under `oracle:<action_id>:<source_oracle_id>`. Render these bound commands before execution. Empty contract command arrays authorize no execution.

Run targeted configured-plugin fixtures and adjacent ordinary fixtures. Verify plugin-specific configuration and exact diagnostic identities, positions, multiplicity, scopes, and text. Refresh stale validation observations after either modification.

Stop if registration already occurs at the correct lifecycle point, the module is unavailable, current APIs cannot be supported, or fixture expectations lack independent justification. Structural PASS predicts compatibility, not repair success. Failed checks prevent a success claim; report unknown coverage. Obtain independent hidden acceptance only after the solver stops, without using hidden tests as guidance.

## Evidence and limits

This is a single-source Workflow, not a Pattern or a verified cross-project template. Consult the [episode](references/episode.md), evidence cards for the [title](references/evidence/title.md), [report](references/evidence/report.md), [implementation](references/evidence/implementation.md), and [assertions](references/evidence/regression.md), and [provenance](references/provenance.json).

Historical CI execution is unknown. Later independent qualification supports only the supplied changed-test selection with original-base controls; whole-project regression and cross-project transfer remain untested. Qualification did not execute this Skill's functional definitions.

The [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json) suites remain **not_executed**.

Keep formal knowledge and checkpoints frozen during evaluation. Never publish a current task plan as newly verified historical knowledge. Time-reconstructed admission excludes the current task's own issue, fix, cluster, aliases, copied sources, and discovery inputs unavailable before query time.
