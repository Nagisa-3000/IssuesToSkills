# Validate visibility and preserved scope behavior

Bind current public test commands before execution. No supplied historical command authorizes a current invocation.

Check the public single-generator and nested-comprehension assertions. Also inspect and run available adjacent tests for ordinary assignments, annotation behavior, comprehension iteration-variable locality, and enclosing function boundaries. These adjacent checks are preservation obligations derived from the selective implementation, not additional historical regression claims.

Record actual commands, exit status, diagnostics, and scope observations. If broader tests are available, run them and report their scope separately; changed-test success alone does not establish whole-project correctness.

```arex-contract-v4
{
  "id": "workflow:verified-history:fd9457af9cbbabf21f89fac4:validate",
  "intent": "Observe corrected target visibility and preserved adjacent binding behavior after the edit.",
  "mechanism": "Execute public single and nested scope regressions and current adjacent binding checks.",
  "semantic_role": "scope-routing-validation",
  "owner_role": "scope-regression-tests",
  "operation": "Run bound public checks and review preservation results.",
  "kind": "validate",
  "inputs": [
    {
      "name": "scope-routing-patch",
      "semantic_role": "assignment-expression-scope-patch",
      "artifact_kind": "code-and-tests",
      "language": "python",
      "scope": "current-analyzer-checkout",
      "phase": "repair",
      "state": "modified-unvalidated"
    }
  ],
  "outputs": [
    {
      "name": "scope-validation-results",
      "semantic_role": "assignment-expression-scope-validation",
      "artifact_kind": "test-results",
      "language": "python",
      "scope": "current-analyzer-checkout",
      "phase": "validation",
      "state": "observed"
    }
  ],
  "preconditions": [
    {"key": "role:scope-regression-tests", "value": true, "evaluator": "file_exists"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-scope-regressions", "value": "observed", "evaluator": "evidence"},
    {"key": "adjacent-binding-results", "value": "observed", "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "checkout-content", "value": "unchanged", "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "single-and-nested-target-visibility",
      "instruction": "Run adapted public regression assertions: the target y in the single generator example and targets y and z in the nested example must not receive undefined-name diagnostics.",
      "evidence_refs": ["PyCQA/pyflakes:633:regression"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "adjacent-scope-preservation",
      "instruction": "Run current public adjacent scope tests and review the diff for ordinary assignment insertion, annotation behavior, iteration-variable locality, syntax guards, and stopping at enclosing non-comprehension boundaries.",
      "evidence_refs": ["PyCQA/pyflakes:633:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:fd9457af9cbbabf21f89fac4:repair"],
  "read_set": ["role:binding-classifier", "role:binding-inserter", "role:comprehension-scope-model", "role:scope-regression-tests"],
  "write_set": [],
  "source_ids": ["PyCQA/pyflakes:633:repair:e02336c3d47c"],
  "evidence_refs": ["PyCQA/pyflakes:633:fix", "PyCQA/pyflakes:633:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:fd9457af9cbbabf21f89fac4"
}
```

Do not translate UNKNOWN into PASS. A failing target or preservation check stops acceptance and requires diagnosis.
