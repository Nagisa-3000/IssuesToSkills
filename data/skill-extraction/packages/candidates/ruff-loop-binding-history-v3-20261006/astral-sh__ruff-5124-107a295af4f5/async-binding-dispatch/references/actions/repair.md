# Align statement handling and regression assertions

Use the located current owners, not historical paths. Share the synchronous context-manager arm with the asynchronous context-manager variant only when their current binding items and bodies have compatible semantics. Retain the existing target extraction, dummy-variable filtering, semantic context, body visitor, comparison, and diagnostic construction.

The historical implementation also replaced the general `Node` input with `&Stmt`, removed the expression-node panic branch, and updated the checker callers to pass statements. Apply that narrowing only after confirming all current callers and statement types. Keep the unexpected-statement guard for genuinely unsupported statements; do not replace it with silent success.

Add regression inputs for asynchronous context-manager reuse and distinct names, and retain asynchronous-loop reuse. Include the original no-`as` reproduction in current public validation. Tests analyze syntax; their context-manager values need not be executable Python objects.

```arex-contract-v4
{
  "id": "workflow:verified-history:fa7c382943159e4d620bbbba:repair",
  "intent": "Close the dispatched asynchronous context-manager coverage gap without changing adjacent diagnostic semantics.",
  "mechanism": "Use a shared synchronous/asynchronous context-manager match arm and a statement-only rule entry point with consistent callers.",
  "semantic_role": "variant-handler-repair",
  "owner_role": "binding-redefinition-rule",
  "operation": "Edit the located Rust rule and dispatch callers to admit the asynchronous context-manager variant through existing context-manager binding extraction and body traversal; add public positive and negative regression assertions and review expected diagnostics.",
  "kind": "edit",
  "inputs": [
    {
      "name": "coverage-report",
      "semantic_role": "binding-variant-coverage",
      "artifact_kind": "review-report",
      "language": "Rust",
      "scope": "binding-rule",
      "phase": "pre-edit",
      "state": "mismatch-confirmed"
    }
  ],
  "outputs": [
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
  "preconditions": [
    {"key": "variant-mismatch-established", "value": true, "evaluator": "evidence"},
    {"key": "current-owners-bound", "value": true, "evaluator": "evidence"},
    {"key": "role:binding-redefinition-rule", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:binding-rule-dispatch", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:binding-rule-regressions", "value": true, "evaluator": "file_exists"},
    {"key": "context-manager-variants-semantically-compatible", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "async-context-manager-handled", "value": true, "evaluator": "evidence"},
    {"key": "statement-callers-consistent", "value": true, "evaluator": "evidence"},
    {"key": "regression-assertions-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "adjacent-binding-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "distinct-binding-non-diagnostic-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "repair-review",
      "instruction": "Review the diff for a shared context-manager extraction/traversal path, consistent statement callers, positive and negative asynchronous context-manager assertions, retained loop coverage, and no blanket suppression of unexpected statements.",
      "evidence_refs": ["astral-sh/ruff:5124:fix", "astral-sh/ruff:5124:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["astral-sh/ruff:5124:repair:107a295af4f5"],
  "evidence_refs": ["astral-sh/ruff:5124:fix", "astral-sh/ruff:5124:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:fa7c382943159e4d620bbbba",
  "read_set": ["role:binding-rule-dispatch", "role:binding-redefinition-rule", "role:binding-rule-regressions"],
  "write_set": ["role:binding-rule-dispatch", "role:binding-redefinition-rule", "role:binding-rule-regressions"],
  "invalidates": ["public-validation-observed"],
  "exclusions": [
    {"key": "context-manager-variants-semantically-compatible", "value": false, "evaluator": "evidence"}
  ]
}
```

Effects describe the intended changed state and require review. This edit invalidates the freshness of public validation, not the behavioral assurances retained across the Workflow.
