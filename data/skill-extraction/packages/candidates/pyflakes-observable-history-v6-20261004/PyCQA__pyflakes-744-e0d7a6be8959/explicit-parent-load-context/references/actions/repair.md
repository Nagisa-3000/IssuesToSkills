# Pass explicit parent context and add regression coverage

Edit the load-analysis interface and every affected caller together. Do not replace the missing-parent failure with exception suppression or an unreviewed fallback.

The historical change added a `parent` argument, removed the internal parent lookup from the builtin-print branch, supplied traversal-aware context from ordinary dispatch, and supplied the enclosing assignment from early dispatch. Add the public augmented-assignment no-crash regression using the current test harness.

```arex-contract-v4
{
  "id": "workflow:verified-history:73c1883f7ed05d43025127fa:repair",
  "intent": "Remove early load analysis's dependency on uninitialized traversal parent metadata.",
  "mechanism": "Pass caller-owned parent context explicitly and add an augmented-assignment regression.",
  "semantic_role": "explicit-parent-context-repair",
  "owner_role": "load-analysis-owner",
  "operation": "Edit the bound load-analysis signature and parent-sensitive branch, update all ordinary and early callers with confirmed parent semantics, and add the public no-crash regression in the bound test owner.",
  "kind": "edit",
  "inputs": [
    {
      "name": "diagnosis",
      "semantic_role": "parent-context-diagnosis",
      "artifact_kind": "review-record",
      "language": "python",
      "scope": "bound-load-analysis-and-callers",
      "phase": "pre-edit",
      "state": "confirmed",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "candidate",
      "semantic_role": "explicit-parent-context-candidate",
      "artifact_kind": "source-and-test-change",
      "language": "python",
      "scope": "bound-load-analysis-and-regression-tests",
      "phase": "post-edit",
      "state": "unvalidated",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "parent-context-mechanism-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "caller-parent-semantics-confirmed", "value": true, "evaluator": "evidence"},
    {
      "key": "role:load-analysis-owner",
      "value": true,
      "evaluator": "symbol_exists",
      "description": "The load-analysis interface is bound in the current checkout."
    },
    {
      "key": "role:early-load-dispatch-owner",
      "value": true,
      "evaluator": "symbol_exists",
      "description": "The current early-dispatch handler is located."
    },
    {
      "key": "role:ordinary-load-dispatch-owner",
      "value": true,
      "evaluator": "symbol_exists",
      "description": "The current ordinary-load handler is located."
    },
    {
      "key": "role:regression-test-owner",
      "value": true,
      "evaluator": "file_exists",
      "description": "The current public regression-test owner resolves to an existing file."
    }
  ],
  "effects": [
    {"key": "explicit-parent-context-installed", "value": true, "evaluator": "evidence"},
    {"key": "augmented-load-regression-added", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-load-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "builtin-print-diagnostic-preserved", "value": true, "evaluator": "evidence"},
    {"key": "augmented-value-target-order-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-explicit-parent-edit",
      "instruction": "Review the current diff for complete caller updates, correct parent context, removal of the early branch's unavailable metadata lookup, preserved builtin-sensitive diagnostics and traversal order, and the added public no-crash regression. This review does not replace the validate Action.",
      "evidence_refs": ["PyCQA/pyflakes:744:fix", "PyCQA/pyflakes:744:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": [
    "role:load-analysis-owner",
    "role:early-load-dispatch-owner",
    "role:ordinary-load-dispatch-owner",
    "role:regression-test-owner"
  ],
  "write_set": [
    "role:load-analysis-owner",
    "role:early-load-dispatch-owner",
    "role:ordinary-load-dispatch-owner",
    "role:regression-test-owner"
  ],
  "source_ids": ["PyCQA/pyflakes:744:repair:e0d7a6be8959"],
  "evidence_refs": ["PyCQA/pyflakes:744:fix", "PyCQA/pyflakes:744:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:73c1883f7ed05d43025127fa"
}
```

Effects are expected postconditions. The candidate remains unvalidated until current public checks are executed and reviewed. The explicit validation Action remains in the verification closure of this edit.
