# Validate diagnostics and adjacent annotation behavior

Bind commands to the current public analyzer and test runner. Run the focused regression and neighboring annotation tests. Review the candidate diff for unchanged guard and continuation semantics. Do not import hidden-test commands or assume a historical command is authorized.

The essential public reproduction is:

```python
x: int
x.__dict__
def f():
    x = 1
```

The expected analyzer outcome is completion without the boolean-subscript exception, together with undefined-name and unused-local diagnostics. This expectation is an oracle definition, not a recorded current result.

```arex-contract-v4
{
  "id": "workflow:verified-history:a9020121b14a346d4f659c0e:validate",
  "intent": "Observe that the repaired metadata resolves the crash without suppressing expected diagnostics or changing adjacent annotation behavior.",
  "mechanism": "Execute the focused public regression and neighboring repository annotation tests against the candidate.",
  "semantic_role": "annotation-usage-repair-validation",
  "owner_role": "annotation-regression-tests",
  "operation": "Execute current bound public checks, inspect diagnostic categories and exceptions, review unchanged branch semantics, and record fresh results with revision and command bindings.",
  "kind": "validate",
  "inputs": [
    {
      "name": "candidate-usage-repair",
      "semantic_role": "annotation-usage-repair-candidate",
      "artifact_kind": "source-and-regression-change",
      "language": "python",
      "scope": "annotation-load-and-nested-store",
      "phase": "post-edit",
      "state": "awaiting-validation",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "usage-repair-validation-record",
      "semantic_role": "annotation-usage-validation",
      "artifact_kind": "public-check-results",
      "language": "python",
      "scope": "annotation-load-and-nested-store",
      "phase": "post-validation",
      "state": "results-recorded",
      "optional": false
    }
  ],
  "preconditions": [
    {
      "key": "annotation-usage-metadata",
      "value": "scope-and-load-node",
      "evaluator": "evidence"
    },
    {
      "key": "target-regression-assertion-present",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "current-public-oracles-bound",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "effects": [
    {
      "key": "target-public-validation-observed",
      "value": true,
      "evaluator": "evidence",
      "description": "Establish only after the reproducer and adjacent checks pass; failed runs still produce a results record but do not establish this effect."
    }
  ],
  "preserves": [
    {
      "key": "annotation-only-load-undefined-diagnostic-preserved",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "nested-unused-local-diagnostic-preserved",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "adjacent-annotation-branch-behavior-preserved",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "oracle": [
    {
      "id": "reproduce-annotation-shadowing",
      "instruction": "Run the public annotation-only outer declaration, attribute load, and nested same-name assignment. Require no analyzer exception and require both undefined-name and unused-local diagnostic categories.",
      "evidence_refs": [
        "PyCQA/pyflakes:764:body",
        "PyCQA/pyflakes:764:regression"
      ],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "neighboring-annotation-checks",
      "instruction": "Run the current repository's focused regression and neighboring annotation tests, including postponed-annotation behavior where supported. Compare against established current expectations and inspect that the annotation guard and continuation are unchanged. Report the exact tested scope; do not infer whole-project safety.",
      "evidence_refs": [
        "PyCQA/pyflakes:764:fix",
        "PyCQA/pyflakes:764:regression"
      ],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": [
    "workflow:verified-history:a9020121b14a346d4f659c0e:repair"
  ],
  "source_ids": [
    "PyCQA/pyflakes:764:repair:e19886e58363"
  ],
  "evidence_refs": [
    "PyCQA/pyflakes:764:body",
    "PyCQA/pyflakes:764:fix",
    "PyCQA/pyflakes:764:regression"
  ],
  "read_set": [
    "role:annotation-usage-tracking",
    "role:scope-sensitive-binding-store",
    "role:annotation-regression-tests"
  ],
  "write_set": [],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:a9020121b14a346d4f659c0e"
}
```

Test execution must not edit tracked implementation or test sources. If tooling does so, those changes require separate review and renewed validation. A failure or UNKNOWN check blocks a successful repair claim.
