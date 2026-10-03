# Add an ordinary-decorator regression

Use the current analyzer test harness to analyze:

```python
x = lambda f: f

@x
def t():
    pass

y = lambda f: f

@x
@y
def t():
    pass

@x
@y
def t():
    pass
```

Assert two ordinary unused-redefinition diagnostics and no exception. In the historical harness the assertion was `m.RedefinedWhileUnused, m.RedefinedWhileUnused`. Map the diagnostic through current public semantics rather than silently assuming an identical class name.

```arex-contract-v4
{
  "id": "workflow:verified-history:314f3449f8ccd1beab92c625:regression",
  "intent": "Encode that assignment-backed decorators do not qualify as typing overloads.",
  "mechanism": "Assert ordinary repeated-definition diagnostics for one and stacked identity-lambda decorators.",
  "semantic_role": "ordinary-decorator-regression",
  "owner_role": "decorator-regression-tests",
  "operation": "Add a focused test using the historical three-definition reproduction and the current harness's equivalent unused-redefinition diagnostics.",
  "kind": "edit",
  "inputs": [
    {"name": "guarded-repair-state", "semantic_role": "overload-detection-repair", "artifact_kind": "code_bundle", "language": "python", "scope": "current-checkout", "phase": "repair", "state": "guarded", "optional": false}
  ],
  "outputs": [
    {"name": "regression-ready-state", "semantic_role": "overload-detection-repair", "artifact_kind": "code_bundle", "language": "python", "scope": "current-checkout", "phase": "repair", "state": "regression-ready", "optional": false}
  ],
  "preconditions": [
    {"key": "import-metadata-access-type-guarded", "value": true, "evaluator": "evidence"},
    {"key": "regression-test-owner-exists", "value": true, "evaluator": "file_exists", "description": "role:decorator-regression-tests"},
    {"key": "ordinary-redefinition-diagnostic-mapped", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "ordinary-decorator-regression-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-redefinition-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "supported-import-overload-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-regression-assertion",
      "instruction": "Inspect the added test for three definitions, assignment-backed x/y decorators, and exactly two unused-redefinition diagnostics; ensure no existing assertion was weakened.",
      "evidence_refs": ["PyCQA/pyflakes:422:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:decorator-regression-tests"],
  "write_set": ["role:decorator-regression-tests"],
  "source_ids": ["PyCQA/pyflakes:422:repair:2c29431eaeb9"],
  "evidence_refs": ["PyCQA/pyflakes:422:regression"],
  "resource": "references/actions/regression.md",
  "package_id": "workflow:verified-history:314f3449f8ccd1beab92c625"
}
```
