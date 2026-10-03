# Repair registration and add a regression

At the bound scope-classification owner, add the missing asynchronous-function AST kind using the representation already used for ordinary functions. Retain the current supported-version policy. At the bound annotation-test owner, add a regression containing a module class and an identically named annotated asynchronous parameter, including the historical `None` return annotation.

Gate syntax-dependent tests according to supported runtimes. Do not change parent traversal to conceal the symptom or weaken nearby diagnostic assertions.

The [episode](../episode.md) preserves the exact historical assignment, including its trailing comma. These contract effects describe intended changes; they are not observations of a current execution.

```arex-contract-v4
{
  "id": "workflow:verified-history:76dfcbfcb074afe10f1cb891:repair",
  "intent": "Restore missing asynchronous-function scope classification and add a reproducing regression.",
  "mechanism": "Add a compatibility-gated asynchronous AST registration using existing function-scope semantics.",
  "semantic_role": "scope-registration-repair",
  "owner_role": "ast-scope-classification",
  "operation": "Edit the bound scope registry and annotation-test owner to register asynchronous functions like ordinary functions and add the annotated-name-collision regression.",
  "kind": "edit",
  "inputs": [
    {
      "name": "scope-diagnosis",
      "semantic_role": "async-scope-repair-context",
      "artifact_kind": "reviewed-code-and-probe-record",
      "language": "python",
      "scope": "current-checkout",
      "phase": "pre-edit",
      "state": "applicability-established",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "scope-patch",
      "semantic_role": "async-scope-validation-target",
      "artifact_kind": "code-and-test-change",
      "language": "python",
      "scope": "current-checkout",
      "phase": "post-edit",
      "state": "unvalidated",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "missing-async-registration-causal", "value": true, "evaluator": "evidence"},
    {"key": "role:ast-scope-classification", "value": true, "evaluator": "symbol_exists", "description": "Resolve the actual scope-classification symbol in the current checkout."},
    {"key": "role:annotation-regression-tests", "value": true, "evaluator": "file_exists", "description": "Resolve the current annotation-test resource."},
    {"key": "registry-shape-and-version-policy-reviewed", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "async-function-scope-registered", "value": true, "evaluator": "evidence"},
    {"key": "annotated-async-regression-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-function-scope-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-annotation-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "supported-version-import-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-scope-patch",
      "instruction": "Review the actual diff for the minimal registration using ordinary function representation, appropriate compatibility gating, and the annotated asynchronous regression. Confirm no parent-traversal fallback or weakened diagnostics. Retain post-edit validation.",
      "evidence_refs": ["PyCQA/pyflakes:401:fix", "PyCQA/pyflakes:401:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:ast-scope-classification", "role:annotation-regression-tests"],
  "write_set": ["role:ast-scope-classification", "role:annotation-regression-tests"],
  "source_ids": ["PyCQA/pyflakes:401:repair:1f58890b3ea7"],
  "evidence_refs": ["PyCQA/pyflakes:401:fix", "PyCQA/pyflakes:401:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:76dfcbfcb074afe10f1cb891"
}
```

Invalidation concerns freshness of validation observations, not the required preservation of adjacent behavior. An unvalidated patch is not a successful repair.
