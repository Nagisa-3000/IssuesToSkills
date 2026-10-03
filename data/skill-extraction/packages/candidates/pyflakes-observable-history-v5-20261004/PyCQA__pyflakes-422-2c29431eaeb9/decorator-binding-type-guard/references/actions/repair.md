# Guard metadata access and add the focused regression

Use the current binding class corresponding to a from-import. Insert its type check after scope membership and before qualified-name metadata access, retaining short-circuit evaluation. Preserve the name comparison and neighboring attribute-form alternative.

Add the regression to the current public test owner. Its historical shape is:

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

Assert exactly two unused-redefinition diagnostics using the current test API. Do not suppress diagnostics merely to avoid the unsafe access. If this binding class or test behavior cannot be mapped from current evidence, stop rather than invent a bridge.

```arex-contract-v4
{
  "id": "workflow:verified-history:314f3449f8ccd1beab92c625:repair",
  "intent": "Prevent import-specific metadata access on ordinary decorator bindings.",
  "mechanism": "Short-circuit on the from-import binding type before comparing the qualified name.",
  "semantic_role": "binding-type-guard-repair",
  "owner_role": "overload-decorator-recognizer",
  "operation": "Edit the recognition guard and add the ordinary-decorator regression assertion.",
  "kind": "edit",
  "inputs": [
    {
      "name": "binding-boundary-review",
      "semantic_role": "recognition-boundary-review",
      "artifact_kind": "review-record",
      "language": "Python",
      "scope": "overload-decorator-recognizer",
      "phase": "pre-edit",
      "state": "unsafe-import-metadata-access-confirmed",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "guarded-recognizer-change",
      "semantic_role": "guarded-recognizer-change",
      "artifact_kind": "patch",
      "language": "Python",
      "scope": "overload-decorator-recognizer-and-tests",
      "phase": "post-edit",
      "state": "guard-and-regression-added",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "role:overload-decorator-recognizer", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:scope-binding-model", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:decorator-recognition-tests", "value": true, "evaluator": "file_exists"},
    {"key": "unsafe-import-metadata-access", "value": "confirmed", "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "non-import-binding-metadata-access", "value": "prevented", "evaluator": "evidence"},
    {"key": "ordinary-decorator-regression", "value": "asserted", "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "from-import-overload-recognition", "value": "preserved", "evaluator": "evidence"},
    {"key": "attribute-decorator-branch", "value": "unchanged", "evaluator": "evidence"},
    {"key": "ordinary-decorator-redefinition-diagnostics", "value": "two", "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-guard-and-regression",
      "instruction": "Review the public patch: membership precedes the binding-class check, the check precedes metadata access, and the added ordinary-decorator test expects exactly two unused-redefinition diagnostics.",
      "evidence_refs": ["PyCQA/pyflakes:422:fix", "PyCQA/pyflakes:422:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:422:repair:2c29431eaeb9"],
  "evidence_refs": ["PyCQA/pyflakes:422:fix", "PyCQA/pyflakes:422:regression"],
  "read_set": ["role:overload-decorator-recognizer", "role:scope-binding-model", "role:decorator-recognition-tests"],
  "write_set": ["role:overload-decorator-recognizer", "role:decorator-recognition-tests"],
  "invalidates": ["current-recognition-boundary", "decorator-test-results", "overload-recognition-results"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:314f3449f8ccd1beab92c625"
}
```

Effects describe the intended repair and require subsequent observation. They are not execution results.
