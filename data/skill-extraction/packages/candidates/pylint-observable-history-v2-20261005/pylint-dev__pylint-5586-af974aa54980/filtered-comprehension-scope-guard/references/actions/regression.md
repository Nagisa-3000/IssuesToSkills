# Install the public regression

Use the current repository's public functional-test convention. Do not import historical paths as current bindings.

```arex-contract-v4
{
  "id": "workflow:verified-history:4d5404af23a33d07f9c8cd24:regression",
  "intent": "Retain an assertion for the repaired scope collision.",
  "mechanism": "Commit a generator-expression filter with an exception-handler homonym as a no-E0601 functional case.",
  "semantic_role": "public-regression-edit",
  "owner_role": "python-public-functional-tests",
  "operation": "Add or update a collected public functional case using a generator target named value, a range(1 / 0) iterable and isinstance(value, int) filter inside try, followed by except ZeroDivisionError assigning value = 1 and printing value. Assert absence of used-before-assignment for the filter under the current harness convention. Avoid disabling the checker or broadly ignoring diagnostics.",
  "kind": "edit",
  "inputs": [
    {"name": "guarded-checker", "semantic_role": "filter-guarded-variable-checker", "artifact_kind": "checkout-code", "language": "python", "scope": "current-checkout", "phase": "implementation", "state": "edited"}
  ],
  "outputs": [
    {"name": "regression-candidate", "semantic_role": "guard-and-public-regression", "artifact_kind": "checkout-code-and-tests", "language": "python", "scope": "current-checkout", "phase": "validation", "state": "ready"}
  ],
  "preconditions": [
    {"key": "semantic-owners-bound", "value": true, "evaluator": "evidence"},
    {"key": "role:python-public-functional-tests", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "public-regression-installed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "nonfilter-homonym-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "late-binding-and-loop-checks-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "inspect-regression-assertion",
      "instruction": "Inspect the installed test for the exact generator/filter/handler collision and verify public test collection identifies it. Ensure checker configuration or expected-output edits do not mask the target diagnostic.",
      "evidence_refs": ["pylint-dev/pylint:5586:regression", "pylint-dev/pylint:5586:body"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "read_set": ["role:python-public-functional-tests"],
  "write_set": ["role:python-public-functional-tests"],
  "source_ids": ["pylint-dev/pylint:5586:repair:af974aa54980"],
  "evidence_refs": ["pylint-dev/pylint:5586:regression"],
  "resource": "references/actions/regression.md",
  "package_id": "workflow:verified-history:4d5404af23a33d07f9c8cd24"
}
```

The iterable's division by zero preserves the reported exception context. The test is a static-analysis regression, not a runtime assertion about evaluating the generator body.
