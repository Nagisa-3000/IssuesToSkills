# Validate the repair and adjacent behavior

Bind commands to the current public checkout and its test harness. The historical reproduction command is recorded in the episode, not prescribed here. No qualification-runtime binary paths are authorized current commands.

Check the original reproduction without `as`, a reused inner context-manager name, a distinct inner name, and existing rule fixtures. Inspect diagnostics at their inner targets. Confirm preserved ordinary context-manager, synchronous/asynchronous loop, assignment, unpacking, cast-exemption, and nested-scope cases where present in the public suite.

```arex-contract-v4
{
  "id": "workflow:verified-history:fa7c382943159e4d620bbbba:validate",
  "intent": "Observe public repair behavior and verify retained diagnostic semantics after edits.",
  "mechanism": "Run the public panic reproduction plus positive, negative, and adjacent rule regression checks with snapshot acceptance disabled.",
  "semantic_role": "repair-verification",
  "owner_role": "binding-rule-regressions",
  "operation": "Execute current-bound public reproduction and repository rule tests, review expected-output changes, and record fresh results without silently accepting snapshots.",
  "kind": "validate",
  "inputs": [
    {
      "name": "repair-state",
      "semantic_role": "binding-rule-repair",
      "artifact_kind": "checkout-change",
      "language": "Rust",
      "scope": "binding-rule",
      "phase": "post-edit",
      "state": "awaiting-validation"
    }
  ],
  "outputs": [
    {
      "name": "validation-report",
      "semantic_role": "binding-rule-validation",
      "artifact_kind": "test-report",
      "language": "Rust",
      "scope": "binding-rule",
      "phase": "post-validation",
      "state": "observed"
    }
  ],
  "preconditions": [
    {"key": "async-context-manager-handled", "value": true, "evaluator": "evidence"},
    {"key": "statement-callers-consistent", "value": true, "evaluator": "evidence"},
    {"key": "regression-assertions-present", "value": true, "evaluator": "evidence"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "adjacent-binding-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "distinct-binding-non-diagnostic-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "no-binding-reproduction",
      "instruction": "Run the current-bound public reproduction containing async def, async with without an as target, and return await; require no panic and no binding-redefinition diagnostic.",
      "evidence_refs": ["astral-sh/ruff:5124:body", "astral-sh/ruff:5124:fix"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "binding-regressions",
      "instruction": "Run current public rule tests with automatic snapshot acceptance disabled. Require an inner-target diagnostic for async-with name reuse, none for distinct names, retained async-for reuse and adjacent binding diagnostics, and successful compilation of rule callers. Record failures rather than refreshing expectations to hide them.",
      "evidence_refs": ["astral-sh/ruff:5124:fix", "astral-sh/ruff:5124:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "source_ids": ["astral-sh/ruff:5124:repair:107a295af4f5"],
  "evidence_refs": ["astral-sh/ruff:5124:body", "astral-sh/ruff:5124:fix", "astral-sh/ruff:5124:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:fa7c382943159e4d620bbbba",
  "validation_for": ["workflow:verified-history:fa7c382943159e4d620bbbba:repair"],
  "read_set": ["role:binding-rule-dispatch", "role:binding-redefinition-rule", "role:binding-rule-regressions"],
  "write_set": []
}
```

An observed report may contain failures. `public-validation-observed` means results were recorded; acceptance additionally requires every bound semantic oracle and retained behavior assurance to PASS. Tests may write ordinary build artifacts, but must not silently change tracked expectations.
