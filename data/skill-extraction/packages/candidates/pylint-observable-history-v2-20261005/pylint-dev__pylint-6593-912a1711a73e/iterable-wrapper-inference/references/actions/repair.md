# Repair target inference and add a focused regression

Consume the confirmed binding. In the current post-loop analysis, preserve the initial inference of the loop iterable. Only if the inferred value is the recognized built-in `enumerate` instance and the call has an argument, infer argument zero and feed that result into the existing analysis.

Keep this inference inside the existing error-handling boundary. Do not replace the diagnostic logic with a blanket suppression. Add a regression for both post-loop targets of `enumerate(range(3))`; use the current suite's conventions for asserting the absence of the target diagnostic.

The historically evidenced change uses an `astroid.Instance`, qualified name `builtins.enumerate`, and `assign.iter.args[0]`. These are mechanism facts, not permission to assume identical names or AST representation in the current checkout. Stop if the binding requires an unsupported adapter.

```arex-contract-v4
{
  "id": "workflow:verified-history:96e9d9e1d61f613785fc9852:repair",
  "intent": "Analyze the wrapped iterable rather than the enumerate instance and protect the demonstrated behavior with a regression.",
  "mechanism": "Guarded first-argument inference reuses existing length/nonemptiness analysis.",
  "semantic_role": "guarded-inference-repair",
  "owner_role": "loop-variable-inference-owner",
  "operation": "Edit the bound inference branch to unwrap only recognized built-in enumerate with an accessible first argument; retain existing inference-error handling and downstream analysis; add the nonempty enumerate regression to the bound diagnostic suite.",
  "kind": "edit",
  "inputs": [
    {"name": "repair-binding", "semantic_role": "confirmed-wrapper-inference-binding", "artifact_kind": "binding-record", "language": "python", "scope": "current-checkout", "phase": "diagnosis", "state": "confirmed", "optional": false}
  ],
  "outputs": [
    {"name": "modified-checkout", "semantic_role": "guarded-enumerate-repair", "artifact_kind": "checkout", "language": "python", "scope": "current-checkout", "phase": "repair", "state": "modified", "optional": false}
  ],
  "preconditions": [
    {"key": "mechanism-match-observed", "value": true, "evaluator": "evidence"},
    {"key": "current-owner-bound", "value": true, "evaluator": "evidence"},
    {"key": "role:loop-variable-inference-owner", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:loop-variable-regression-owner", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "enumerate-target-inference", "value": "underlying-iterable", "evaluator": "evidence"},
    {"key": "committed-regression-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-iterable-analysis-preserved", "value": true, "evaluator": "evidence"},
    {"key": "inference-error-fallback-preserved", "value": true, "evaluator": "evidence"},
    {"key": "possibly-empty-loop-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "inspect-guarded-edit",
      "instruction": "Review the current diff for a built-in identity guard, argument-presence guard, target inference inside the existing inference-error boundary, unchanged ordinary analysis, and regression reads of both loop targets. Then retain the separate validation action.",
      "evidence_refs": ["pylint-dev/pylint:6593:fix", "pylint-dev/pylint:6593:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:6593:repair:912a1711a73e"],
  "evidence_refs": ["pylint-dev/pylint:6593:fix", "pylint-dev/pylint:6593:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:96e9d9e1d61f613785fc9852",
  "read_set": ["role:loop-variable-inference-owner", "role:loop-variable-regression-owner"],
  "write_set": ["role:loop-variable-inference-owner", "role:loop-variable-regression-owner"],
  "invalidates": ["public-validation-observed", "diagnostic-baseline-fresh"],
  "exclusions": [
    {"key": "current-representation-needs-unsupported-adapter", "value": true, "evaluator": "evidence"}
  ]
}
```

Effects are expected until the diff and validation establish them. The invalidated keys represent observation freshness, not preserved behavior.
