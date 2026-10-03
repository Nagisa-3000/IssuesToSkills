# Register async scope and retain the regression

At the bound classifier owner, register asynchronous function definitions with the same function-scope representation as ordinary definitions. Preserve the established runtime capability policy so unsupported runtimes do not access an unavailable AST class.

At the bound annotation-test owner, add a no-diagnostic assertion for:

```python
class c:
    pass

async def func(c: c) -> None:
    pass
```

Use the current harness and supported-runtime test guard. The historical implementation used a tuple-shaped assignment and a Python 3.5 gate; these are historical facts, not unconditionally reusable current bindings.

If equivalent regression coverage is already present, retain it without duplication and record the current evidence. Do not suppress the crash or alter parent links as a substitute for classification. Effects below are required postconditions, not execution claims.

```arex-contract-v4
{
  "id": "workflow:verified-history:76dfcbfcb074afe10f1cb891:repair",
  "intent": "Correct the missing async function scope boundary and retain regression coverage.",
  "mechanism": "Extend node-to-scope classification under the capability policy and add the same-name async annotation checker assertion.",
  "semantic_role": "repair-async-scope-and-cover",
  "owner_role": "python-ast-scope-classifier",
  "operation": "Modify the bound classifier and annotation-test owners to register async function scope and cover the public reproduction.",
  "kind": "edit",
  "inputs": [
    {
      "name": "diagnosis",
      "semantic_role": "async-scope-repair-diagnosis",
      "artifact_kind": "inspection-record",
      "language": "python",
      "scope": "scope-classifier-and-annotation-tests",
      "phase": "current",
      "state": "observed"
    }
  ],
  "outputs": [
    {
      "name": "repair-change",
      "semantic_role": "async-scope-repair-change",
      "artifact_kind": "source-and-test-change",
      "language": "python",
      "scope": "scope-classifier-and-annotation-tests",
      "phase": "current",
      "state": "modified"
    }
  ],
  "preconditions": [
    {"key": "role:python-ast-scope-classifier", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:annotation-regression-tests", "value": true, "evaluator": "file_exists"},
    {"key": "missing-async-classification-explains-failure", "value": true, "evaluator": "evidence"},
    {"key": "function-scope-representation-established", "value": true, "evaluator": "evidence"},
    {"key": "runtime-capability-policy-established", "value": true, "evaluator": "evidence"},
    {"key": "annotation-test-harness-established", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "async-function-scope-classified", "value": true, "evaluator": "evidence"},
    {"key": "annotated-async-regression-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-function-scope-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unrelated-scope-entries-preserved", "value": true, "evaluator": "evidence"},
    {"key": "existing-annotation-tests-preserved", "value": true, "evaluator": "evidence"},
    {"key": "supported-runtime-safety-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-repair-postconditions",
      "instruction": "Inspect the diff for async registration using the current ordinary function representation, guarded AST class access, and a no-diagnostic same-name async annotation assertion with None return annotation and the current runtime guard.",
      "evidence_refs": ["PyCQA/pyflakes:401:fix", "PyCQA/pyflakes:401:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": [
    "role:python-ast-scope-classifier",
    "role:python-runtime-capability-policy",
    "role:annotation-regression-tests"
  ],
  "write_set": [
    "role:python-ast-scope-classifier",
    "role:annotation-regression-tests"
  ],
  "invalidates": [
    "async-function-scope-classified",
    "annotated-async-regression-present",
    "public-annotated-async-check-passes",
    "ordinary-function-scope-preserved",
    "unrelated-scope-entries-preserved",
    "existing-annotation-tests-preserved",
    "supported-runtime-safety-preserved"
  ],
  "exclusions": [
    {"key": "async-function-already-correctly-classified", "value": true, "evaluator": "evidence"}
  ],
  "source_ids": ["PyCQA/pyflakes:401:repair:1f58890b3ea7"],
  "evidence_refs": ["PyCQA/pyflakes:401:body", "PyCQA/pyflakes:401:fix", "PyCQA/pyflakes:401:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:76dfcbfcb074afe10f1cb891"
}
```
