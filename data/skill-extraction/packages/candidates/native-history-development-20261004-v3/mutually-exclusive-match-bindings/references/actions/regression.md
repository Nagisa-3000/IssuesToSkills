# Encode the regression assertion

Add an assertion equivalent to the historical reproduction in the bound public
match suite:

```python
def f(x):
    match x:
        case 1:
            def y(): pass
        case _:
            def y(): print(1)
    return y
```

Expect no unused-name redefinition diagnostic. Preserve existing assertions and
runtime gating. Adapt to the current harness rather than assuming the historical
`self.flakes` API. The wildcard avoids adding an exhaustiveness requirement.

```arex-contract-v4
{
  "id": "mutually-exclusive-match-bindings:regression",
  "intent": "Retain a regression for definitions in mutually exclusive match cases.",
  "mechanism": "Encode two case-local definitions followed by a use of the shared name.",
  "semantic_role": "distinct-case-regression",
  "owner_role": "python-match-regression-suite",
  "operation": "Edit the current public suite to assert no distinct-case redefinition diagnostic.",
  "kind": "edit",
  "inputs": [
    {"name": "located-context", "semantic_role": "confirmed-match-alternative-omission", "artifact_kind": "binding-and-probe-record", "language": "python", "scope": "current-analyzer", "phase": "diagnosis", "state": "confirmed", "optional": false}
  ],
  "outputs": [
    {"name": "regression-change", "semantic_role": "distinct-case-regression-implementation", "artifact_kind": "test-change", "language": "python", "scope": "current-analyzer", "phase": "repair", "state": "modified-unvalidated", "optional": false}
  ],
  "preconditions": [
    {"key": "current-mechanism-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "role:python-match-regression-suite", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "distinct-case-regression-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "existing-regression-assertions-preserved", "value": true, "evaluator": "evidence"},
    {"key": "python-ast-availability-respected", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-regression",
      "instruction": "Inspect the assertion for separate case 1 and wildcard definitions of the same name, a post-match use, no expected redefinition diagnostic, and preserved runtime gating.",
      "evidence_refs": ["PyCQA/pyflakes:771:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:771"],
  "evidence_refs": ["PyCQA/pyflakes:771:regression"],
  "read_set": ["role:python-match-regression-suite"],
  "write_set": ["role:python-match-regression-suite"],
  "invalidates": ["current-regression-suite-results"],
  "resource": "references/actions/regression.md",
  "package_id": "mutually-exclusive-match-bindings"
}
```

Adding an assertion does not establish that it passes; retain the validation
Action in the verification closure.
