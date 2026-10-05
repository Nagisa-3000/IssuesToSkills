---
name: iterable-wrapper-inference
description: "Repair possibly-undefined loop-variable false positives when a Python analyzer reasons about built-in enumerate instead of its underlying iterable, after confirming the current inference mechanism."
---

# Iterable-wrapper inference

## Activation

Activate when a Python static analyzer reports possibly undefined loop targets after a loop over built-in `enumerate`, although its underlying iterable is demonstrably nonempty. The supported example is:

```python
for i, num in enumerate(range(3)):
    pass
print(i, num)
```

This is a conditional repair workflow, not a rule that all loops using `enumerate` execute.

Ask for clarification or run public probes if the diagnostic, built-in identity, underlying iterable, or current inference owner is unknown. Do not activate for an actually empty iterable, a shadowed/custom `enumerate`, unrelated name resolution, or a request to suppress all possibly-undefined diagnostics.

## Current binding and operations

1. [Locate and probe the inference owner](references/actions/probe.md). Locate the current checker responsible for post-loop variable diagnostics and its iterable inference/length analysis. Confirm the public reproduction and built-in wrapper identity.
2. [Repair inference and add regression coverage](references/actions/repair.md). Only when the mechanism matches, infer the first argument of recognized built-in `enumerate` before the existing iterable analysis. Keep the existing inference-error fallback and non-wrapper path.
3. [Validate the modification](references/actions/validate.md). Run currently bound public regression and adjacent checks; inspect the repair's guards and error handling.

Historical file locations are recorded in [the episode](references/episode.md), not reusable bindings. The complete historical realization is in [the workflow](references/workflow.md).

Before execution, establish a public TaskContext with the issue, pinned base, hashed code anchors, real semantic-owner bindings, observed facts and PortValues. Bind every oracle to a current public instruction, argv command, and evidence references. Its check key is `oracle:<action_id>:<source_oracle_id>`. Render the bound commands before running them; historical commands are not execution authorization.

Checks are PASS, FAIL, or UNKNOWN. UNKNOWN prerequisites permit probes only. Hard failures reject the repair plan. Structural compatibility does not establish repair success. After modification, refresh stale validation observations and execute the retained validation action.

## Required assurances and stopping conditions

- Do not blanket-exempt `enumerate` from possibly-undefined diagnostics.
- Preserve ordinary iterable analysis and the existing inference-error fallback.
- Preserve warnings for loops whose execution cannot be established; validate this with current public adjacent tests.
- Stop if built-in identity cannot be established, the current representation lacks an accessible first argument, the analyzer already unwraps the iterable, or a different mechanism explains the diagnostic.
- Stop and reassess if target or adjacent validation fails. Do not report success from contract matching or historical qualification alone.

## Evidence and limits

The source supports one Python-analyzer workflow, not a cross-project pattern or arbitrary wrapper-unwrapping abstraction. Its committed regression uses `enumerate(range(3))` inside a function. Other iterables, aliases, nested wrappers, and analyzer architectures require current evidence.

Historical test execution is unknown. Later independent qualification compared the original base, base with the committed regression, and historical fixed revision; its scope is changed-test-file qualification with eight selected functional cases, not whole-project correctness or cross-project transfer. These authored [evaluation definitions](evals/functional-cases.json) remain **not executed**.

[Provenance](references/provenance.json) records the exact source and qualification hash. Formal evaluation must keep knowledge/checkpoints frozen, exclude the evaluated issue/fix/cluster/aliases and copied sources from prior knowledge, and obtain independent hidden acceptance after the solver stops. Never publish a current task plan as newly verified historical knowledge.
