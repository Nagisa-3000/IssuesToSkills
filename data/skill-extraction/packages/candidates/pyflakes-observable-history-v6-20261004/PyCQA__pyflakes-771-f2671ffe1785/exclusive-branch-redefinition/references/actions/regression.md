# Add the branch-exclusive regression assertion

Add a focused public test to the bound match suite. Keep both definitions in the same surrounding function scope and use the defined name after the match, as in the historical assertion.

```arex-contract-v4
{
  "id": "workflow:verified-history:45a56eede77a20492da56a49:regression",
  "intent": "Keep the reported false positive covered by a public no-diagnostic assertion.",
  "mechanism": "Test identical definition names in distinct match cases followed by a use.",
  "semantic_role": "regression-assertion-edit",
  "owner_role": "match-regression-suite",
  "operation": "Add or confirm a public regression equivalent to a function matching its argument with case 1 and case _, defining y separately in each case, and returning y afterward. Assert no analyzer diagnostics using the current suite's public convention.",
  "kind": "edit",
  "inputs": [
    {
      "name": "bindings",
      "semantic_role": "branch-redefinition-owner-bindings",
      "artifact_kind": "binding-record",
      "language": "python",
      "scope": "current-checkout",
      "phase": "applicability",
      "state": "observed",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "regression",
      "semantic_role": "match-exclusive-definition-regression",
      "artifact_kind": "test-code",
      "language": "python",
      "scope": "current-checkout",
      "phase": "repair",
      "state": "modified",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "match-suite-located", "value": true, "evaluator": "file_exists", "description": "Resolve role:match-regression-suite in the current checkout."},
    {"key": "current-match-test-convention-known", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "match-redefinition-regression-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "existing-if-try-classification-preserved", "value": true, "evaluator": "evidence"},
    {"key": "genuine-redefinition-detection-preserved", "value": true, "evaluator": "evidence"},
    {"key": "supported-runtime-compatibility-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-public-regression",
      "instruction": "Inspect the test for separate case bodies, the same function name in both, a use after the match, and an explicit no-diagnostic expectation under the bound test convention. Respect the suite's version gating.",
      "evidence_refs": ["PyCQA/pyflakes:771:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:match-regression-suite"],
  "write_set": ["role:match-regression-suite"],
  "source_ids": ["PyCQA/pyflakes:771:repair:f2671ffe1785"],
  "evidence_refs": ["PyCQA/pyflakes:771:regression"],
  "resource": "references/actions/regression.md",
  "package_id": "workflow:verified-history:45a56eede77a20492da56a49"
}
```

Bind `match-suite-located` through `role:match-regression-suite`. Adding an assertion is not evidence that it passes.
